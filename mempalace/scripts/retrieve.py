import json
import os
from datetime import datetime, timezone
import sys

# Add scripts directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'scripts'))

def retrieve_memory(query, storage_path=None, layers=None):
    """
    Retrieve memories using layered approach: working → high-confidence → episodic → raw.
    
    Args:
        query (str): The query text to search for.
        storage_path (str, optional): Path to the mempalace storage directory.
        layers (list, optional): Which layers to search. Defaults to all layers.
    
    Returns:
        list: List of memory events with explainability metadata.
    """
    if storage_path is None:
        storage_path = os.path.expanduser("~/.hermes/mempalace")
    
    if layers is None:
        layers = ['working', 'high_confidence', 'episodic', 'raw']
    
    results = []
    
    # Layer 1: Working memory (recent, high rehearsal)
    if 'working' in layers:
        working_results = _search_working_memory(query, storage_path)
        results.extend(working_results)
    
    # Layer 2: High-confidence consolidated memories (semantic)
    if 'high_confidence' in layers:
        hc_results = _search_high_confidence_memory(query, storage_path)
        results.extend(hc_results)
    
    # Layer 3: Episodic memories (context-rich)
    if 'episodic' in layers:
        episodic_results = _search_episodic_memory(query, storage_path)
        results.extend(episodic_results)
    
    # Layer 4: Raw memories (everything else)
    if 'raw' in layers:
        raw_results = _search_raw_memory(query, storage_path)
        results.extend(raw_results)
    
    # Deduplicate by memory ID, keeping the highest layer occurrence
    seen_ids = {}
    for result in results:
        mem_id = result.get('id')
        if mem_id not in seen_ids:
            seen_ids[mem_id] = result
        else:
            # Keep the one from the higher layer (earlier in our layer list)
            current_layer = result.get('_layer', 999)
            existing_layer = seen_ids[mem_id].get('_layer', 999)
            if current_layer < existing_layer:
                seen_ids[mem_id] = result
    
    # Convert back to list and sort by layer priority then score
    final_results = list(seen_ids.values())
    final_results.sort(key=lambda x: (x.get('_layer', 999), -x.get('_score', 0)))
    
    return final_results

def _search_working_memory(query, storage_path):
    """Search working memory (recent, high rehearsal)."""
    # For demo, we'll look at recent raw memories with high scores
    # In reality, this might be a separate working memory store
    return _search_with_scoring(query, storage_path, 'raw', layer=1, limit=5)

def _search_high_confidence_memory(query, storage_path):
    """Search high-confidence consolidated memories."""
    return _search_with_scoring(query, storage_path, 'semantic', layer=2, limit=10)

def _search_episodic_memory(query, storage_path):
    """Search episodic memories."""
    return _search_with_scoring(query, storage_path, 'episodic', layer=3, limit=10)

def _search_raw_memory(query, storage_path):
    """Search raw memories."""
    return _search_with_scoring(query, storage_path, 'raw', layer=4, limit=15)

def _search_with_scoring(query, storage_path, store_type, layer, limit=10):
    """
    Search a specific store type with scoring and explainability.
    
    Args:
        query (str): The query text.
        storage_path (str): Path to mempalace storage.
        store_type (str): Type of store ('raw', 'semantic', 'episodic', etc.).
        layer (int): Layer number for explainability (lower = higher priority).
        limit (int): Maximum results to return.
    
    Returns:
        list: List of memory results with explainability metadata.
    """
    store_dir = os.path.join(storage_path, store_type)
    if not os.path.exists(store_dir):
        return []
    
    results = []
    query_lower = query.lower()
    
    for filename in os.listdir(store_dir):
        if filename.endswith('.jsonl'):
            filepath = os.path.join(store_dir, filename)
            try:
                with open(filepath, 'r') as f:
                    line = f.readline().strip()
                    if not line:
                        continue
                    data = json.loads(line)
                    # Validate that data is a dict
                    if not isinstance(data, dict):
                        continue
                    
                    # Simple text matching for demo
                    content = data.get('content', '').lower()
                    context = data.get('context', '').lower()
                    raw_text = data.get('raw_text', '').lower()
                    
                    # Calculate basic relevance score
                    score = 0.0
                    if query_lower in content:
                        score += 0.5
                    if query_lower in context:
                        score += 0.3
                    if query_lower in raw_text:
                        score += 0.2
                    
                    # Boost score with memory score if available
                    memory_score = data.get('_score', 0.0)  # Pre-computed score
                    if memory_score:
                        score = score * 0.7 + memory_score * 0.3
                    
                    if score > 0.1:  # Minimum threshold
                        result = data.copy()
                        result['_score'] = score
                        result['_layer'] = layer
                        result['_store_type'] = store_type
                        # Add explainability metadata
                        result['_explainability'] = {
                            'query_match': {
                                'content': query_lower in content,
                                'context': query_lower in context,
                                'raw_text': query_lower in raw_text
                            },
                            'scoring_factors': {
                                'text_match_score': score,
                                'memory_score': memory_score,
                                'final_score': score
                            },
                            'layer_info': {
                                'layer': layer,
                                'store_type': store_type,
                                'layer_description': _get_layer_description(layer)
                            }
                        }
                        results.append(result)
            except Exception as e:
                print(f"Error reading {filepath}: {e}")
                continue
    
    # Sort by score descending and limit
    results.sort(key=lambda x: x['_score'], reverse=True)
    return results[:limit]

def _get_layer_description(layer):
    """Get human-readable description of a layer."""
    descriptions = {
        1: "Working memory (recent, high rehearsal)",
        2: "High-confidence consolidated memories",
        3: "Episodic memories (context-rich)",
        4: "Raw memories (everything else)"
    }
    return descriptions.get(layer, f"Unknown layer {layer}")

def retrieve_with_faiss(query, storage_path=None, k=5):
    """
    Retrieve memories using FAISS vector search.
    
    Args:
        query (str): The query text.
        storage_path (str, optional): Path to mempalace storage.
        k (int): Number of results to return.
    
    Returns:
        list: List of memory events from vector search.
    """
    # Import FAISS functions
    sys.path.append(os.path.join(os.path.dirname(__file__), 'scripts'))
    try:
        from faiss_integration import search_embeddings
        # Get candidate IDs from FAISS
        candidate_ids = search_embeddings(query, k=k)
        
        # Fetch the actual memory records
        results = []
        for memory_id, score in candidate_ids:
            memory_event = _load_memory_by_id(memory_id, storage_path)
            if memory_event:
                memory_event['_score'] = score
                memory_event['_layer'] = 0  # Vector search layer (highest priority)
                memory_event['_store_type'] = 'vector'
                memory_event['_explainability'] = {
                    'vector_search': {
                        'faiss_score': score,
                        'method': 'FAISS similarity search'
                    }
                }
                results.append(memory_event)
        return results
    except ImportError:
        print("FAISS integration not available")
        return []
    except Exception as e:
        print(f"Error in FAISS retrieval: {e}")
        return []

def _load_memory_by_id(memory_id, storage_path=None):
    """Load a memory event by its ID from any store."""
    if storage_path is None:
        storage_path = os.path.expanduser("~/.hermes/mempalace")
    
    # Search in order of preference: semantic, episodic, raw
    for store_type in ['semantic', 'episodic', 'raw']:
        store_dir = os.path.join(storage_path, store_type)
        filepath = os.path.join(store_dir, f"{memory_id}.jsonl")
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r') as f:
                    line = f.readline().strip()
                    if line:
                        data = json.loads(line)
                        if isinstance(data, dict):
                            return data
            except Exception:
                continue
    return None