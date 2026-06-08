"""
Reinforcement system for MemPalace - usage-based memory reinforcement
"""

import os
import json
from datetime import datetime, timezone

# Storage path - will be set by init_reinforcement
_STORAGE_PATH = None
_REINFORCEMENT_FILE = None

def init_reinforcement(storage_path):
    """Initialize reinforcement system"""
    global _STORAGE_PATH, _REINFORCEMENT_FILE
    _STORAGE_PATH = storage_path
    prefs_dir = os.path.join(_STORAGE_PATH, 'preferences')
    os.makedirs(prefs_dir, exist_ok=True)
    _REINFORCEMENT_FILE = os.path.join(prefs_dir, 'reinforcement.jsonl')
    
    # Ensure file exists
    if not os.path.exists(_REINFORCEMENT_FILE):
        with open(_REINFORCEMENT_FILE, 'w') as f:
            pass  # Create empty file

def reinforce_memory(memory_id, context=""):
    """Reinforce a memory by logging its successful use"""
    if not _STORAGE_PATH or not _REINFORCEMENT_FILE:
        raise RuntimeError("Reinforcement system not initialized. Call init_reinforcement first.")
    
    reinforcement_event = {
        'memory_id': memory_id,
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'context': context
    }
    
    try:
        with open(_REINFORCEMENT_FILE, 'a') as f:
            f.write(json.dumps(reinforcement_event) + '\n')
    except Exception as e:
        print(f"Failed to write reinforcement event: {e}")

def get_reinforced_memories(limit=100):
    """Get memories sorted by reinforcement count"""
    if not _STORAGE_PATH or not _REINFORCEMENT_FILE:
        return []
    
    # Count reinforcements per memory ID
    reinforcement_counts = {}
    
    try:
        with open(_REINFORCEMENT_FILE, 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        event = json.loads(line)
                        mem_id = event.get('memory_id')
                        if mem_id:
                            reinforcement_counts[mem_id] = reinforcement_counts.get(mem_id, 0) + 1
                    except json.JSONDecodeError:
                        continue
    except Exception as e:
        print(f"Error reading reinforcement file: {e}")
        return []
    
    # Sort by count (descending) and get top memories
    sorted_memories = sorted(reinforcement_counts.items(), key=lambda x: x[1], reverse=True)
    
    # Get the actual memory objects for top memories
    results = []
    # Import locally to avoid circular import
    import retrieve
    for mem_id, count in sorted_memories[:limit]:
        memory = retrieve.get_memory_by_id(mem_id)
        if memory:
            memory['reinforcement_count'] = count
            results.append(memory)
    
    return results

def get_reinforcement_count(memory_id):
    """Get reinforcement count for a specific memory"""
    if not _STORAGE_PATH or not _REINFORCEMENT_FILE:
        return 0
    
    count = 0
    try:
        with open(_REINFORCEMENT_FILE, 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        event = json.loads(line)
                        if event.get('memory_id') == memory_id:
                            count += 1
                    except json.JSONDecodeError:
                        continue
    except Exception:
        pass
    
    return count