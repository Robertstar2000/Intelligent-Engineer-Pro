"""MemPalace Retrieval System - Layered retrieval with semantic search."""

import json
import os
import sys
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional, Tuple

# Add the mempalace directory to path for imports
sys.path.insert(0, os.path.expanduser('~/.hermes/mempalace'))

try:
    from capture import get_raw_event_count
    from tag import extract_context_tags, get_palace_tags
    from score import score_memory
    from embed import search_embeddings, HAS_DEPENDENCIES as EMBED_ENABLED
except ImportError as e:
    print(f"Warning: Could not import MemPalace modules: {e}")
    # Define fallback functions
    def get_raw_event_count(): return 0
    def extract_context_tags(content, event_type=None): return []
    def get_palace_tags(context_tags): return []
    def score_memory(event, weights=None): return 0.5, {}
    def search_embeddings(query_text, k=5): return []
    EMBED_ENABLED = False

_storage_path: str = None


def init_retrieval(storage_path: str):
    """Initialize the retrieval system."""
    global _storage_path
    _storage_path = storage_path
    print(f"Retrieval system initialized at {_storage_path}")


def _load_json_file(filepath: str) -> Optional[Dict[Any, Any]]:
    """Safely load a JSON file."""
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError, IOError):
        return None


def _load_jsonl_file(filepath: str) -> List[Dict[Any, Any]]:
    """Safely load a JSONL file."""
    results = []
    try:
        with open(filepath, 'r') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                try:
                    data = json.loads(line)
                    if isinstance(data, dict):
                        results.append(data)
                except json.JSONDecodeError:
                    continue
    except (FileNotFoundError, IOError):
        pass
    return results


def _load_memory_by_id(memory_id: str) -> Optional[Dict[Any, Any]]:
    """Load a memory event by its ID from the raw store.
    
    Handles multiple event schemas:
    - Standard: {memory_id/id/event_id, content, ...}
    - Nested data: {id, data: {content, ...}}
    - Legacy: {memory_id, raw_text, ...}
    """
    if _storage_path is None:
        return None

    raw_dir = os.path.join(_storage_path, 'raw')
    if not os.path.exists(raw_dir):
        return None

    for fname in os.listdir(raw_dir):
        if fname == 'archive':
            continue
        fpath = os.path.join(raw_dir, fname)
        if not os.path.isfile(fpath):
            continue

        try:
            if fname.endswith('.jsonl'):
                with open(fpath, 'r') as f:
                    for line in f:
                        line = line.strip()
                        if not line:
                            continue
                        try:
                            event = json.loads(line)
                            if isinstance(event, dict):
                                eid = event.get('memory_id') or event.get('id') or event.get('event_id')
                                if str(eid) == str(memory_id):
                                    # Normalize: if content is in data dict, hoist it
                                    return _normalize_event(event)
                        except json.JSONDecodeError:
                            continue
            elif fname.endswith('.json'):
                with open(fpath, 'r') as f:
                    event = json.load(f)
                    if isinstance(event, dict):
                        eid = event.get('memory_id') or event.get('id') or event.get('event_id')
                        if str(eid) == str(memory_id):
                            return _normalize_event(event)
        except (json.JSONDecodeError, IOError):
            continue
    return None


def _normalize_event(event: Dict[Any, Any]) -> Dict[Any, Any]:
    """Normalize an event dict so content is always at the top level.
    
    Handles the nested data schema where content lives inside data dict.
    """
    # If content already exists at top level, return as-is
    if event.get('content'):
        return event
    
    # Check if content is nested in data dict
    data = event.get('data', {})
    if isinstance(data, dict) and data.get('content'):
        # Merge data fields into top level
        normalized = {**event, **data}
        return normalized
    
    # Check for raw_text
    if event.get('raw_text') and not event.get('content'):
        normalized = event.copy()
        normalized['content'] = event['raw_text']
        return normalized
    
    return event


def retrieve_semantic(query: str, limit: int = 5) -> List[Dict[Any, Any]]:
    """
    Semantic search layer: Use FAISS embeddings to find semantically similar memories.
    
    This layer uses vector similarity search to find memories that are semantically
    related to the query, even if they don't share exact keywords.
    
    Args:
        query: Search query
        limit: Maximum results to return
        
    Returns:
        List of memory dictionaries with semantic similarity scores
    """
    if not EMBED_ENABLED:
        return []
    
    results = []
    
    try:
        # Search FAISS index for similar memories
        semantic_results = search_embeddings(query, k=limit * 2)  # Get extra for filtering
        
        for memory_id, similarity_score in semantic_results:
            # Load the full memory event
            memory = _load_memory_by_id(memory_id)
            if memory is None:
                continue
            
            memory_copy = memory.copy()
            memory_copy['retrieval_layer'] = 'semantic'
            memory_copy['retrieval_score'] = similarity_score
            memory_copy['store_type'] = 'semantic_search'
            results.append(memory_copy)
            
            if len(results) >= limit:
                break
                
    except Exception as e:
        print(f"Semantic search error: {e}")
    
    return results[:limit]


def retrieve_from_working_memory(query: str, limit: int = 5) -> List[Dict[Any, Any]]:
    """
    Layer 1: Working memory - very recent, high-context memories.
    
    Args:
        query: Search query
        limit: Maximum results to return
        
    Returns:
        List of memory dictionaries
    """
    # Working memory is handled by Hermes' native memory system
    # MemPalace focuses on longer-term storage
    return []


def retrieve_from_high_confidence(query: str, limit: int = 5) -> List[Dict[Any, Any]]:
    """
    Layer 2: High-confidence consolidated memories (semantic/episodic/procedural).
    
    Args:
        query: Search query
        limit: Maximum results to return
        
    Returns:
        List of memory dictionaries with confidence scores
    """
    if _storage_path is None:
        return []
    
    results = []
    query_lower = query.lower()
    
    # Search consolidated stores
    for store_type in ['semantic', 'episodic', 'procedural']:
        store_dir = os.path.join(_storage_path, store_type)
        if not os.path.exists(store_dir):
            continue
            
        for fname in os.listdir(store_dir):
            if not fname.endswith('.json'):
                continue
                
            fpath = os.path.join(store_dir, fname)
            memory = _load_json_file(fpath)
            if memory is None:
                continue
                
            # Calculate relevance score
            content = memory.get('content', '').lower()
            event_type = memory.get('type', '').lower()
            
            relevance = 0.0
            if query_lower in content:
                relevance += 0.5
            if query_lower in event_type:
                relevance += 0.3
            
            # Check for word matches
            query_words = set(query_lower.split())
            content_words = set(content.split())
            if query_words & content_words:
                word_match_ratio = len(query_words & content_words) / len(query_words)
                relevance += 0.4 * word_match_ratio
            
            if relevance > 0.1:
                memory_copy = memory.copy()
                memory_copy['retrieval_layer'] = 'high_confidence'
                memory_copy['retrieval_score'] = min(1.0, relevance)
                memory_copy['store_type'] = store_type
                results.append(memory_copy)
    
    # Sort by retrieval score descending
    results.sort(key=lambda x: x['retrieval_score'], reverse=True)
    return results[:limit]


def retrieve_from_episodic(query: str, limit: int = 5) -> List[Dict[Any, Any]]:
    """
    Layer 3: Episodic memories - personal experiences and specific events.
    
    Args:
        query: Search query
        limit: Maximum results to return
        
    Returns:
        List of memory dictionaries
    """
    return retrieve_from_high_confidence(query, limit)


def retrieve_from_raw_evidence(query: str, limit: int = 5) -> List[Dict[Any, Any]]:
    """
    Layer 4: Raw evidence - complete, unfiltered memory trace.
    
    Args:
        query: Search query
        limit: Maximum results to return
        
    Returns:
        List of memory dictionaries
    """
    if _storage_path is None:
        return []
    
    results = []
    query_lower = query.lower()
    raw_dir = os.path.join(_storage_path, 'raw')
    
    if not os.path.exists(raw_dir):
        return results
    
    # Process raw JSONL files
    for fname in os.listdir(raw_dir):
        if fname == 'archive':
            continue
        if not fname.endswith('.jsonl'):
            continue
            
        fpath = os.path.join(raw_dir, fname)
        memories = _load_jsonl_file(fpath)
        
        for memory in memories:
            if not isinstance(memory, dict):
                continue
                
            content = memory.get('content', '').lower()
            event_type = memory.get('type', '').lower()
            
            relevance = 0.0
            if query_lower in content:
                relevance += 0.4
            if query_lower in event_type:
                relevance += 0.2
            
            query_words = set(query_lower.split())
            content_words = set(content.split())
            if query_words & content_words:
                word_match_ratio = len(query_words & content_words) / len(query_words)
                relevance += 0.4 * word_match_ratio
            
            if relevance > 0.05:
                memory_copy = memory.copy()
                memory_copy['retrieval_layer'] = 'raw_evidence'
                memory_copy['retrieval_score'] = min(1.0, relevance)
                memory_copy['store_type'] = 'raw'
                results.append(memory_copy)
    
    results.sort(key=lambda x: x['retrieval_score'], reverse=True)
    return results[:limit]


def retrieve_memories(query: str, limit_per_layer: int = 3, use_semantic: bool = True) -> Dict[str, List[Dict[Any, Any]]]:
    """
    Retrieve memories using layered approach with optional semantic search.
    
    The retrieval order is:
    1. Working memory (Hermes native)
    2. Semantic search (FAISS vector similarity) - if enabled
    3. High-confidence consolidated memories (keyword matching)
    4. Episodic memories
    5. Raw evidence
    
    Args:
        query: Search query
        limit_per_layer: Maximum results per layer
        use_semantic: Whether to include FAISS semantic search layer
        
    Returns:
        Dictionary with layers as keys and lists of memories as values
    """
    layers = {
        'working': retrieve_from_working_memory(query, limit_per_layer),
    }
    
    # Add semantic search layer if embeddings are available
    if use_semantic and EMBED_ENABLED:
        layers['semantic'] = retrieve_semantic(query, limit_per_layer)
    
    layers.update({
        'high_confidence': retrieve_from_high_confidence(query, limit_per_layer),
        'episodic': retrieve_from_episodic(query, limit_per_layer),
        'raw_evidence': retrieve_from_raw_evidence(query, limit_per_layer),
    })
    
    # Filter out empty layers
    return {k: v for k, v in layers.items() if v}


def get_retrieval_stats() -> Dict[str, Any]:
    """Get statistics about retrieval system."""
    if _storage_path is None:
        return {}
    
    stats = {}
    raw_count = get_raw_event_count()
    stats['raw_memories'] = raw_count
    
    consolidated_counts = {}
    for store_type in ['semantic', 'episodic', 'procedural']:
        store_dir = os.path.join(_storage_path, store_type)
        if os.path.exists(store_dir):
            count = len([f for f in os.listdir(store_dir) if f.endswith('.json')])
            consolidated_counts[store_type] = count
        else:
            consolidated_counts[store_type] = 0
    
    stats['consolidated_memories'] = consolidated_counts
    stats['total_consolidated'] = sum(consolidated_counts.values())
    stats['semantic_search_enabled'] = EMBED_ENABLED
    
    return stats


def get_component_status() -> Dict[str, Any]:
    """Get status of retrieval component."""
    return {
        'initialized': _storage_path is not None,
        'storage_path': _storage_path,
        'semantic_search_enabled': EMBED_ENABLED,
        'stats': get_retrieval_stats(),
    }
