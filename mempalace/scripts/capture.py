import json
import uuid
from datetime import datetime, timezone
import os

def capture_memory(event_data, storage_path=None):
    """
    Capture a memory event and append it to the raw store.
    
    Args:
        event_data (dict): The memory event data. Must contain at least 'content'.
        storage_path (str, optional): Path to the mempalace storage directory.
                                     Defaults to ~/.hermes/mempalace.
    
    Returns:
        str: The unique ID of the captured memory.
    """
    if storage_path is None:
        storage_path = os.path.expanduser("~/.hermes/mempalace")
    
    # Generate a unique ID if not provided
    memory_id = event_data.get('id', str(uuid.uuid4()))
    
    # Ensure timestamp is present and in ISO format with timezone
    if 'timestamp' not in event_data:
        event_data['timestamp'] = datetime.now(timezone.utc).isoformat()
    else:
        # Convert timestamp to proper ISO format if needed
        ts = event_data['timestamp']
        if isinstance(ts, str):
            if ts.endswith('Z'):
                event_data['timestamp'] = ts[:-1] + '+00:00'
        # If it's already a datetime object, convert to ISO string
        elif hasattr(ts, 'isoformat'):
            event_data['timestamp'] = ts.isoformat()
    
    # Create the memory event object
    memory_event = {
        'id': memory_id,
        'type': event_data.get('type', 'user_interaction'),
        'content': event_data.get('content', ''),
        'context': event_data.get('context', ''),
        'timestamp': event_data['timestamp'],
        'raw_text': event_data.get('raw_text', event_data.get('content', ''))
    }
    
    # Append to raw store
    raw_file = os.path.join(storage_path, 'raw', f"{memory_id}.jsonl")
    try:
        with open(raw_file, 'a') as f:
            f.write(json.dumps(memory_event) + '\n')
    except Exception as e:
        print(f"Failed to write memory event to {raw_file}: {e}")
        return None
    
    return memory_id

def capture_memory_batch(events, storage_path=None):
    """
    Capture multiple memory events.
    
    Args:
        events (list): List of event data dictionaries.
        storage_path (str, optional): Path to the mempalace storage directory.
    
    Returns:
        list: List of memory IDs for the captured events.
    """
    ids = []
    for event in events:
        memory_id = capture_memory(event, storage_path)
        if memory_id:
            ids.append(memory_id)
    return ids