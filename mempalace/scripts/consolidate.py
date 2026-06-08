import json
import os
from datetime import datetime, timezone
import math

# Import scoring functions
import sys
sys.path.append(os.path.join(os.path.dirname(__file__)))
from score import compute_memory_score, _parse_timestamp

# Consolidation threshold - memories with score >= this will be considered for consolidation
CONSOLIDATION_THRESHOLD = 0.6

def _load_memory_event(filepath):
    """
    Load a memory event from a JSONL file.
    
    Args:
        filepath (str): Path to the JSONL file.
    
    Returns:
        dict: The memory event, or None if failed.
    """
    try:
        with open(filepath, 'r') as f:
            line = f.readline().strip()
            if not line:
                return None
            data = json.loads(line)
            # Validate that data is a dict
            if not isinstance(data, dict):
                print(f"Warning: Expected dict in {filepath}, got {type(data)}")
                return None
            return data
    except Exception as e:
        print(f"Error loading memory file {filepath}: {e}")
        return None

def _save_memory_event(memory_event, filepath):
    """
    Save a memory event to a JSONL file.
    
    Args:
        memory_event (dict): The memory event to save.
        filepath (str): Path to the JSONL file.
    """
    try:
        # Ensure directory exists
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'a') as f:
            f.write(json.dumps(memory_event) + '\n')
    except Exception as e:
        print(f"Error saving memory event to {filepath}: {e}")

def consolidate_memory(memory_event, storage_path=None):
    """
    Consolidate a memory event by creating a summary and storing it in the semantic store.
    
    Args:
        memory_event (dict): The memory event to consolidate.
        storage_path (str, optional): Path to the mempalace storage directory.
    
    Returns:
        str: The ID of the consolidated memory, or None if failed.
    """
    if storage_path is None:
        storage_path = os.path.expanduser("~/.hermes/mempalace")
    
    memory_id = memory_event.get('id')
    if not memory_id:
        print("Error: Memory event missing ID")
        return None
    
    # Create consolidated memory (semantic version)
    consolidated_event = memory_event.copy()
    consolidated_event['type'] = 'semantic_' + consolidated_event.get('type', 'memory')
    consolidated_event['consolidated_from'] = memory_id
    consolidated_event['consolidation_timestamp'] = datetime.now(timezone.utc).isoformat()
    
    # Generate a summary (in a real system, this might use LLM summarization)
    # For now, we'll create a simple summary
    content = consolidated_event.get('content', '')
    context = consolidated_event.get('context', '')
    if len(content) > 100:
        # Simple truncation for demo - in reality, use proper summarization
        summary = content[:100] + "..."
    else:
        summary = content
    
    consolidated_event['summary'] = summary
    consolidated_event['content'] = f"[CONSOLIDATED] {summary}"
    
    # Save to semantic store
    semantic_dir = os.path.join(storage_path, 'semantic')
    semantic_file = os.path.join(semantic_dir, f"{memory_id}.jsonl")
    _save_memory_event(consolidated_event, semantic_file)
    
    return memory_id

def should_consolidate_memory(memory_event):
    """
    Determine if a memory event should be consolidated based on its score.
    
    Args:
        memory_event (dict): The memory event to check.
    
    Returns:
        bool: True if the memory should be consolidated, False otherwise.
    """
    score = compute_memory_score(memory_event)
    return score >= CONSOLIDATION_THRESHOLD

def consolidate_all_memories(storage_path=None):
    """
    Consolidate all memories in the raw store that meet the threshold.
    
    Args:
        storage_path (str, optional): Path to the mempalace storage directory.
    
    Returns:
        list: List of memory IDs that were consolidated.
    """
    if storage_path is None:
        storage_path = os.path.expanduser("~/.hermes/mempalace")
    
    raw_dir = os.path.join(storage_path, 'raw')
    if not os.path.exists(raw_dir):
        return []
    
    consolidated_ids = []
    for filename in os.listdir(raw_dir):
        if filename.endswith('.jsonl'):
            filepath = os.path.join(raw_dir, filename)
            memory_event = _load_memory_event(filepath)
            if memory_event is not None:
                if should_consolidate_memory(memory_event):
                    consolidated_id = consolidate_memory(memory_event, storage_path)
                    if consolidated_id is not None:
                        consolidated_ids.append(consolidated_id)
    
    return consolidated_ids