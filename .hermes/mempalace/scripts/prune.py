import json
import os
from datetime import datetime, timezone
import shutil

# Pruning thresholds
PRUNING_SCORE_THRESHOLD = 0.2   # memories with score below this are candidates
PRUNING_AGE_DAYS = 30           # memories older than this are candidates
PRUNING_REHEARSAL_THRESHOLD = 1 # memories with rehearsal count below this are candidates

def _parse_timestamp(timestamp_str):
    """
    Parse a timestamp string into a timezone-aware datetime object.
    Handles both timezone-aware and naive datetime strings.
    """
    if isinstance(timestamp_str, str):
        if timestamp_str.endswith('Z'):
            timestamp_str = timestamp_str[:-1] + '+00:00'
        try:
            dt = datetime.fromisoformat(timestamp_str)
        except ValueError:
            # Fallback for other formats if needed
            dt = datetime.strptime(timestamp_str, '%Y-%m-%dT%H:%M:%S')
    else:
        dt = timestamp_str
    
    # Ensure timezone-aware (assume UTC if naive)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt

def compute_memory_age_days(timestamp_str):
    """
    Compute the age of a memory in days.
    """
    try:
        dt = _parse_timestamp(timestamp_str)
        now = datetime.now(timezone.utc)
        delta = now - dt
        return delta.total_seconds() / (3600 * 24)
    except Exception:
        return 0.0

def should_prune_memory(memory_event):
    """
    Determine if a memory event should be pruned.
    
    Args:
        memory_event (dict): The memory event to check.
    
    Returns:
        bool: True if the memory should be pruned, False otherwise.
    """
    # Import scoring functions to compute current score
    import sys
    sys.path.append(os.path.join(os.path.dirname(__file__)))
    from score import compute_memory_score
    
    # Compute current score
    score = compute_memory_score(memory_event)
    
    # Get age in days
    timestamp_str = memory_event.get('timestamp')
    if not timestamp_str:
        # If no timestamp, we might want to keep it? Or prune? Let's keep for safety.
        age_days = 0
    else:
        age_days = compute_memory_age_days(timestamp_str)
    
    # Get rehearsal count
    rehearsal_count = memory_event.get('rehearsal_count', 0)
    
    # Prune if:
    #   score is low AND
    #   age is high AND
    #   rehearsal count is low
    if score < PRUNING_SCORE_THRESHOLD and age_days > PRUNING_AGE_DAYS and rehearsal_count < PRUNING_REHEARSAL_THRESHOLD:
        return True
    
    # Additionally, we might want to prune memories that are extremely old regardless of score?
    # Let's add: if age > 2 * PRUNING_AGE_DAYS, prune regardless of score and rehearsal (but keep if rehearsal is high?)
    # For safety, we'll only prune extremely old if rehearsal is also low.
    if age_days > 2 * PRUNING_AGE_DAYS and rehearsal_count < PRUNING_REHEARSAL_THRESHOLD:
        return True
    
    return False

def prune_memory(memory_event, storage_path=None):
    """
    Prune a memory event by moving it to the archive directory.
    
    Args:
        memory_event (dict): The memory event to prune.
        storage_path (str, optional): Path to the mempalace storage directory.
    
    Returns:
        bool: True if pruning was successful, False otherwise.
    """
    if storage_path is None:
        storage_path = os.path.expanduser("~/.hermes/mempalace")
    
    memory_id = memory_event.get('id')
    if not memory_id:
        print("Error: Memory event missing ID")
        return False
    
    # Determine which store the memory is in (by checking where the file exists)
    store_type = None
    for store in ['semantic', 'episodic', 'raw', 'procedural']:
        store_dir = os.path.join(storage_path, store)
        filepath = os.path.join(store_dir, f"{memory_id}.jsonl")
        if os.path.exists(filepath):
            store_type = store
            break
    
    if store_type is None:
        print(f"Memory {memory_id} not found in any store for pruning")
        return False
    
    # Create archive directory if it doesn't exist
    archive_dir = os.path.join(storage_path, 'archive', store_type)
    os.makedirs(archive_dir, exist_ok=True)
    
    # Move the file to archive
    src_file = os.path.join(storage_path, store_type, f"{memory_id}.jsonl")
    dst_file = os.path.join(archive_dir, f"{memory_id}.jsonl")
    
    try:
        shutil.move(src_file, dst_file)
        print(f"Pruned memory {memory_id} from {store_type} to archive")
        return True
    except Exception as e:
        print(f"Error pruning memory {memory_id}: {e}")
        return False

def prune_all_memories(storage_path=None):
    """
    Prune all memories in the stores that meet the pruning criteria.
    
    Args:
        storage_path (str, optional): Path to the mempalace storage directory.
    
    Returns:
        dict: Count of pruned memories per store type.
    """
    if storage_path is None:
        storage_path = os.path.expanduser("~/.hermes/mempalace")
    
    # Ensure archive directory exists
    os.makedirs(os.path.join(storage_path, 'archive'), exist_ok=True)
    
    pruned_counts = {'semantic': 0, 'episodic': 0, 'raw': 0, 'procedural': 0}
    
    for store_type in ['semantic', 'episodic', 'raw', 'procedural']:
        store_dir = os.path.join(storage_path, store_type)
        if not os.path.exists(store_dir):
            continue
        
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
                            print(f"Warning: Expected dict in {filepath}, got {type(data)}")
                            continue
                        
                        if should_prune_memory(data):
                            if prune_memory(data, storage_path):
                                pruned_counts[store_type] += 1
                except Exception as e:
                    print(f"Error processing {filepath} for pruning: {e}")
                    continue
    
    return pruned_counts

def get_archive_size(storage_path=None):
    """
    Get the size of the archive (number of archived memories).
    
    Args:
        storage_path (str, optional): Path to the mempalace storage directory.
    
    Returns:
        dict: Number of archived memories per store type.
    """
    if storage_path is None:
        storage_path = os.path.expanduser("~/.hermes/mempalace")
    
    archive_dir = os.path.join(storage_path, 'archive')
    if not os.path.exists(archive_dir):
        return {'semantic': 0, 'episodic': 0, 'raw': 0, 'procedural': 0}
    
    archive_counts = {}
    for store_type in ['semantic', 'episodic', 'raw', 'procedural']:
        store_archive_dir = os.path.join(archive_dir, store_type)
        if os.path.exists(store_archive_dir):
            count = len([f for f in os.listdir(store_archive_dir) if f.endswith('.jsonl')])
            archive_counts[store_type] = count
        else:
            archive_counts[store_type] = 0
    
    return archive_counts