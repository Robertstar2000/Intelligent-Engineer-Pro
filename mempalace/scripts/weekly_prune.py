"""
Weekly Pruning Script for MemPalace
Removes low-value memories from raw store to manage storage.
"""

import os
import json
from datetime import datetime, timedelta, timezone

def _ensure_timezone_aware(dt_str: str) -> datetime:
    """
    Ensure datetime string is timezone-aware (UTC).
    Handles both timezone-aware and naive strings.
    """
    # If ends with Z, replace with +00:00
    if dt_str.endswith('Z'):
        dt_str = dt_str[:-1] + '+00:00'
    # If no timezone info, assume UTC
    if '+' not in dt_str and '-' not in dt_str[-6:]:
        dt_str += '+00:00'
    return datetime.fromisoformat(dt_str)

PALACE_PATH = os.path.expanduser("~/.hermes/mempalace")

PRUNING_THRESHOLD = 0.2
DAYS_TO_RETAIN = 365

def should_prune_memory(memory):
    score = float(memory.get('score', 0.0))
    if score < PRUNING_THRESHOLD:
        return True

    try:
        timestamp_str = memory['timestamp']
        timestamp = _ensure_timezone_aware(timestamp_str)
        now = datetime.now(timezone.utc)
        
        # Now both are timezone-aware, subtraction works
        if (now - timestamp).days > DAYS_TO_RETAIN:
            memory_type = memory.get('type', '')
            if memory_type not in ['user_interaction', 'important_decision', 'task_completion']:
                return True
    except Exception as e:
        print(f"Error processing timestamp {memory.get('timestamp')}: {e}")
        # If we can't parse the timestamp, don't prune based on age
        pass

    return False

def prune_memories():
    raw_dir = os.path.join(PALACE_PATH, 'raw')
    pruned_count = 0
    total_count = 0

    for filename in os.listdir(raw_dir):
        if filename.endswith('.json'):
            total_count += 1
            filepath = os.path.join(raw_dir, filename)
            try:
                with open(filepath, 'r') as f:
                    memory = json.load(f)

                if memory.get('pruned', False):
                    continue

                if should_prune_memory(memory):
                    os.remove(filepath)
                    pruned_count += 1
                else:
                    memory['retained'] = True
                    with open(filepath, 'w') as f:
                        json.dump(memory, f, indent=2)
            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")

    print(f"Weekly pruning complete: {pruned_count} memories pruned, {total_count} total")

    # Also prune semantic store
    semantic_dir = os.path.join(PALACE_PATH, 'semantic')
    if os.path.exists(semantic_dir):
        semantic_pruned = 0
        for filename in os.listdir(semantic_dir):
            if filename.endswith('.json'):
                filepath = os.path.join(semantic_dir, filename)
                try:
                    with open(filepath, 'r') as f:
                        memory = json.load(f)
                    score = float(memory.get('score', 0.0))
                    if score < 0.3:
                        os.remove(filepath)
                        semantic_pruned += 1
                except:
                    pass
        print(f"Also pruned {semantic_pruned} low-value memories from semantic store")

if __name__ == "__main__":
    prune_memories()
