"""
Hermes-MemPalace integration hook.
This module provides hooks to integrate MemPalace with Hermes' memory system.
"""
import json
import os
from typing import Dict, Any, Optional, List

# Global flag to track if MemPalace is initialized
_MempalaceInitialized = False

def init_mempalace_hook():
    """
    Initialize the MemPalace hook for Hermes integration.
    This should be called when Hermes starts up.
    """
    global _MempalaceInitialized
    if _MempalaceInitialized:
        return
    
    try:
        # Import and initialize MemPalace
        from mempalace import init_mempalace
        storage_path = init_mempalace()
        print(f"MemPalace initialized at {storage_path}")
        _MempalaceInitialized = True
    except Exception as e:
        print(f"Failed to initialize MemPalace hook: {e}")
        # Don't raise - we want Hermes to continue working even if MemPalace fails

def capture_to_mempalace(event: Dict[str, Any]) -> Optional[str]:
    """
    Hook to capture a memory event to MemPalace.
    This function should be called whenever Hermes stores a memory.
    Returns the memory ID if successful, None otherwise.
    """
    if not _MempalaceInitialized:
        init_mempalace_hook()
    
    if not _MempalaceInitialized:
        print("MemPalace not initialized, skipping capture")
        return None
    
    try:
        from mempalace.capture import capture_memory
        from mempalace.tag import tag_memory
        from mempalace.faiss_index import add_embedding
        
        # Tag the event first
        tagged_event = tag_memory(event.copy())
        
        # Capture to raw store
        memory_id = capture_memory(tagged_event)
        
        # Add embedding for semantic search
        raw_text = event.get('content', '')
        if raw_text.strip():
            add_embedding(memory_id, raw_text)
        
        return memory_id
    except Exception as e:
        print(f"Failed to capture to MemPalace: {e}")
        return None

def retrieve_from_mempalace(
    query: str,
    context: Optional[str] = None,
    event_type: Optional[str] = None,
    limit: int = 10
) -> List[Dict[str, Any]]:
    """
        Hook to retrieve memories from MemPalace.
    This function enhances Hermes' memory retrieval with long-term memories.
    Returns list of memories from MemPalace.
    """
    if not _MempalaceInitialized:
        init_mempalace_hook()
    
    if not _MempalaceInitialized:
        print("MemPalace not initialized, returning empty results")
        return []
    
    try:
        from mempalace.retrieve import retrieve_memory
        return retrieve_memory(query, context, event_type, limit)
    except Exception as e:
        print(f"Failed to retrieve from MemPalace: {e}")
        return []

def reinforce_in_mempalace(
    memory_id: str,
    context: str = "",
    outcome: str = "success",
    details: Optional[Dict[str, Any]] = None
) -> bool:
    """
    Hook to reinforce a memory in MemPalace based on successful use.
    """
    if not _MempalaceInitialized:
        init_mempalace_hook()
    
    if not _MempalaceInitialized:
        return False
    
    try:
        from mempalace.reinforce import reinforce_memory
        return reinforce_memory(memory_id, context, outcome, details)
    except Exception as e:
        print(f"Failed to reinforce in MemPalace: {e}")
        return False

def explain_mempalace_retrieval(
    query: str,
    memories: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Generate explanation for MemPalace retrieval results.
    """
    if not _MempalaceInitialized:
        init_mempalace_hook()
    
    if not _MempalaceInitialized:
        return {'error': 'MemPalace not initialized'}
    
    try:
        from mempalace.explain import explain_retrieval
        return explain_retrieval(query, memories)
    except Exception as e:
        print(f"Failed to explain MemPalace retrieval: {e}")
        return {'error': str(e)}

def run_mempalace_maintenance(
    operation: str = "consolidate",
    **kwargs
) -> Dict[str, Any]:
    """
    Run MemPalace maintenance operations.
    Operations: consolidate, prune, rebuild_index
    """
    if not _MempalaceInitialized:
        init_mempalace_hook()
    
    if not _MempalaceInitialized:
        return {'error': 'MemPalace not initialized'}
    
    try:
        if operation == "consolidate":
            from mempalace.consolidate import run_consolidation_job
            return run_consolidation_job(**kwargs)
        elif operation == "prune":
            from mempalace.prune import run_pruning_job
            return run_pruning_job(**kwargs)
        elif operation == "rebuild_index":
            from mempalace.faiss_index import rebuild_index_from_memories
            success = rebuild_index_from_memories()
            return {'success': success, 'operation': 'rebuild_index'}
        else:
            return {'error': f'Unknown operation: {operation}'}
    except Exception as e:
        print(f"Failed to run MemPalace maintenance {operation}: {e}")
        return {'error': str(e)}

def get_mempalace_status() -> Dict[str, Any]:
    """
    Get status information about MemPalace integration.
    """
    if not _MempalaceInitialized:
        init_mempalace_hook()
    
    status = {
        'initialized': _MempalaceInitialized,
        'components': {}
    }
    
    if _MempalaceInitialized:
        try:
            from mempalace.retrieve import get_retrieval_statistics
            status['components']['retrieval'] = get_retrieval_statistics()
        except Exception as e:
            status['components']['retrieval'] = {'error': str(e)}
        
        try:
            from mempalace.faiss_index import get_index_statistics
            status['components']['faiss_index'] = get_index_statistics()
        except Exception as e:
            status['components']['faiss_index'] = {'error': str(e)}
        
        try:
            from mempalace.score import score_raw_events
            # Get a quick count of recent events
            recent_events = score_raw_events(from_date='2026-04-27')  # yesterday
            status['components']['recent_scored_events'] = len(recent_events)
        except Exception as e:
            status['components']['recent_scored_events'] = {'error': str(e)}
    
    return status

# Auto-initialize when imported (optional)
# init_mempalace_hook()