"""
Capture system for MemPalace - append-only event logging
"""

import os
import json
import uuid
from datetime import datetime, timezone

# Storage path - will be set by init_capture
_STORAGE_PATH = None

def init_capture(storage_path):
    """Initialize capture system"""
    global _STORAGE_PATH
    _STORAGE_PATH = storage_path
    raw_dir = os.path.join(_STORAGE_PATH, 'raw')
    os.makedirs(raw_dir, exist_ok=True)

def capture_event(event_data):
    """Capture a memory event to raw storage"""
    if not _STORAGE_PATH:
        raise RuntimeError("Capture system not initialized. Call init_capture first.")
    
    # Generate unique ID
    event_id = str(uuid.uuid4())
    
    # Prepare event with metadata
    event = {
        'id': event_id,
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'data': event_data
    }
    
    # Append to raw events file (daily partitioning)
    date_str = datetime.now(timezone.utc).strftime('%Y-%m-%d')
    raw_file = os.path.join(_STORAGE_PATH, 'raw', f'events_{date_str}.jsonl')
    
    try:
        with open(raw_file, 'a') as f:
            f.write(json.dumps(event) + '\n')
    except Exception as e:
        print(f"Failed to write capture event: {e}")
        return None
    
    return event_id

def load_recent_events(days=7):
    """Load recent events for processing"""
    events = []
    if not _STORAGE_PATH:
        return events
    
    raw_dir = os.path.join(_STORAGE_PATH, 'raw')
    if not os.path.exists(raw_dir):
        return events
    
    # Load events from recent days
    from datetime import timedelta
    for i in range(days):
        date = datetime.now(timezone.utc) - timedelta(days=i)
        date_str = date.strftime('%Y-%m-%d')
        filename = os.path.join(raw_dir, f'events_{date_str}.jsonl')
        
        if os.path.exists(filename):
            try:
                with open(filename, 'r') as f:
                    for line in f:
                        line = line.strip()
                        if line:
                            try:
                                event = json.loads(line)
                                # Validate it's a dict
                                if isinstance(event, dict):
                                    events.append(event)
                                else:
                                    print(f"Skipping non-dict event in {filename}: {type(event)}")
                            except json.JSONDecodeError as e:
                                print(f"Invalid JSON in {filename}: {e}")
            except Exception as e:
                print(f"Error reading {filename}: {e}")
    
    # Sort by timestamp (newest first)
    events.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
    return events