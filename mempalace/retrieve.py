"""Retrieval system for MemPalace - layered retrieval system"""

import os
import json
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
import capture
import consolidate
import reinforce
import embed

# Storage path - will be set by init_retrieval
_STORAGE_PATH = None

def init_retrieval(storage_path):
    """Initialize retrieval system"""
    global _STORAGE_PATH
    _STORAGE_PATH = storage_path

def retrieve_memories(query: str, layers: Optional[List[str]] = None, k: int = 10) -> List[Dict[str, Any]]:
    """Retrieve memories using layered approach: working → high-confidence → episodic → raw"""
    if not _STORAGE_PATH:
        raise RuntimeError("Retrieval system not initialized. Call init_retrieval first.")
    
    # Default layers: working (reinforced), high-confidence (semantic), episodic, raw
    if layers is None:
        layers = ['working', 'high_confidence', 'episodic', 'raw']
    
    all_results = []
    seen_ids = set()
    
    # Layer 1: Working memory (reinforced memories)
    if 'working' in layers:
        working_results = _get_working_memory(query, k)
        for result in working_results:
            mem_id = result.get('id')
            if mem_id not in seen_ids:
                seen_ids.add(mem_id)
                result['retrieval_layer'] = 'working'
                result['retrieval_score'] = result.get('reinforcement_count', 0)
                all_results.append(result)
    
    # Layer 2: High-confidence memory (semantic store)
    if 'high_confidence' in layers:
        hc_results = _get_high_confidence_memory(query, k - len(all_results))
        for result in hc_results:
            mem_id = result.get('id')
            if mem_id not in seen_ids:
                seen_ids.add(mem_id)
                result['retrieval_layer'] = 'high_confidence'
                result['retrieval_score'] = result.get('mempalace_score', 0.0)
                all_results.append(result)
    
    # Layer 3: Episodic memory
    if 'episodic' in layers:
        ep_results = _get_episodic_memory(query, k - len(all_results))
        for result in ep_results:
            mem_id = result.get('id')
            if mem_id not in seen_ids:
                seen_ids.add(mem_id)
                result['retrieval_layer'] = 'episodic'
                result['retrieval_score'] = result.get('mempalace_score', 0.0)
                all_results.append(result)
    
    # Layer 4: Raw memory (with embedding search)
    if 'raw' in layers:
        raw_results = _get_raw_memory(query, k - len(all_results))
        for result in raw_results:
            mem_id = result.get('id')
            if mem_id not in seen_ids:
                seen_ids.add(mem_id)
                result['retrieval_layer'] = 'raw'
                result['retrieval_score'] = result.get('embedding_score', 0.0)
                all_results.append(result)
    
    # Sort by retrieval score (descending) and return top k
    all_results.sort(key=lambda x: x.get('retrieval_score', 0), reverse=True)
    return all_results[:k]

def _get_working_memory(query: str, k: int) -> List[Dict[str, Any]]:
    """Get reinforced memories (working memory layer)"""
    try:
        # Get reinforced memories from reinforcement system
        reinforced = reinforce.get_reinforced_memories(limit=k*2)  # Get extra for filtering
        
        # Simple text matching for now (can be enhanced with embeddings)
        query_lower = query.lower()
        results = []
        for mem in reinforced:
            # Check if query matches content
            content = str(mem.get('data', {}).get('content', '')) + \
                     str(mem.get('data', {}).get('text', '')) + \
                     str(mem.get('data', {}).get('message', ''))
            
            if query_lower in content.lower():
                results.append(mem)
                if len(results) >= k:
                    break
        return results
    except Exception as e:
        print(f"Error getting working memory: {e}")
        return []

def _get_high_confidence_memory(query: str, k: int) -> List[Dict[str, Any]]:
    """Get high-confidence memories from semantic store"""
    try:
        # Get semantic memories
        semantic_memories = consolidate.load_consolidated_memories('semantic', limit=k*2)
        
        # Use embedding search if available, otherwise text matching
        embedding_results = embed.search_embeddings(query, k=k*2)
        embedding_ids = {mem_id for mem_id, _ in embedding_results}
        
        # Filter semantic memories by embedding results or text match
        query_lower = query.lower()
        results = []
        for mem in semantic_memories:
            # Ensure mem is a dictionary
            if not isinstance(mem, dict):
                print(f"Warning: Expected dict in semantic_memories, got {type(mem)}: {mem}")
                continue
            mem_id = mem.get('id')
            content = str(mem.get('original_data', {}).get('content', '')) + \
                     str(mem.get('original_data', {}).get('text', '')) + \
                     str(mem.get('original_data', {}).get('message', '')) + \
                     str(mem.get('summary', ''))
            
            # Match if in embedding results or text contains query
            if mem_id in embedding_ids or query_lower in content.lower():
                # Add embedding score if available
                embedding_score = 0.0
                for emb_id, score in embedding_results:
                    if emb_id == mem_id:
                        embedding_score = score
                        break
                
                mem_copy = mem.copy()
                mem_copy['embedding_score'] = embedding_score
                results.append(mem_copy)
                if len(results) >= k:
                    break
        return results
    except Exception as e:
        print(f"Error getting high-confidence memory: {e}")
        return []

def _get_episodic_memory(query: str, k: int) -> List[Dict[str, Any]]:
    """Get episodic memories"""
    try:
        # Get episodic memories
        episodic_memories = consolidate.load_consolidated_memories('episodic', limit=k*2)
        
        # Simple text matching
        query_lower = query.lower()
        results = []
        for mem in episodic_memories:
            content = str(mem.get('original_data', {}).get('content', '')) + \
                     str(mem.get('original_data', {}).get('text', '')) + \
                     str(mem.get('original_data', {}).get('message', '')) + \
                     str(mem.get('summary', ''))
            
            if query_lower in content.lower():
                results.append(mem)
                if len(results) >= k:
                    break
        return results
    except Exception as e:
        print(f"Error getting episodic memory: {e}")
        return []

def _get_raw_memory(query: str, k: int) -> List[Dict[str, Any]]:
    """Get raw memories with embedding search"""
    try:
        # Use embedding search for raw memories
        embedding_results = embed.search_embeddings(query, k=k*2)
        
        if not embedding_results:
            return []
        
        # Load raw events and match by ID
        recent_events = capture.load_recent_events(days=30)  # Last month
        
        # Create lookup dict
        event_lookup = {event.get('id'): event for event in recent_events if event.get('id')}
        
        results = []
        for mem_id, score in embedding_results:
            if mem_id in event_lookup:
                event = event_lookup[mem_id]
                event_copy = event.copy()
                event_copy['embedding_score'] = score
                results.append(event_copy)
                if len(results) >= k:
                    break
        return results
    except Exception as e:
        print(f"Error getting raw memory: {e}")
        return []

def get_memory_by_id(memory_id: str) -> Optional[Dict[str, Any]]:
    """Get a specific memory by ID from any store"""
    if not _STORAGE_PATH:
        return None
    
    # Check raw storage first
    recent_events = capture.load_recent_events(days=30)
    for event in recent_events:
        if event.get('id') == memory_id:
            return event
    
    # Check consolidated stores
    for store_type in ['semantic', 'episodic', 'procedural']:
        store_dir = os.path.join(_STORAGE_PATH, store_type)
        if os.path.exists(store_dir):
            for filename in os.listdir(store_dir):
                if filename.endswith('.json'):
                    filepath = os.path.join(store_dir, filename)
                    try:
                        with open(filepath, 'r') as f:
                            memory = json.load(f)
                            if memory.get('id') == memory_id:
                                return memory
                    except Exception:
                        continue
    
    return None