#!/usr/bin/env python3
"""
MemPalace Capture Hook
Called by Hermes memory tool to also store in MemPalace raw layer.
"""
import json
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

def capture_memory(event):
    """Capture a memory event to MemPalace raw layer."""
    # Ensure required fields
    if 'memory_id' not in event:
        event['memory_id'] = str(uuid.uuid4())
    if 'timestamp' not in event:
        event['timestamp'] = datetime.now(timezone.utc).isoformat()
    if 'session_id' not in event:
        event['session_id'] = 'unknown'  # Should be provided by Hermes
    if 'user_id' not in event:
        event['user_id'] = 'default'  # Should be provided by Hermes
    
    # Set defaults
    event.setdefault('source_type', 'chat')
    event.setdefault('provisional_type', 'episodic')
    event.setdefault('entities', [])
    event.setdefault('topics', [])
    event.setdefault('context_tags', [])
    event.setdefault('palace_tags', [])
    event.setdefault('salience_signals', {})
    
    # Write to raw layer (append-only JSONL)
    raw_dir = Path.home() / '.hermes' / 'mempalace' / 'raw'
    raw_dir.mkdir(parents=True, exist_ok=True)
    raw_file = raw_dir / 'events.jsonl'
    
    with open(raw_file, 'a') as f:
        f.write(json.dumps(event) + '\\n')
    
    return event['memory_id']

if __name__ == '__main__':
    # Read JSON from stdin
    try:
        data = sys.stdin.read().strip()
        if not data:
            sys.exit(0)
        event = json.loads(data)
        memory_id = capture_memory(event)
        # Output the memory_id for confirmation
        print(json.dumps({'memory_id': memory_id, 'status': 'captured'}))
    except json.JSONDecodeError as e:
        print(json.dumps({'error': f'Invalid JSON: {e}'}), file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(json.dumps({'error': str(e)}), file=sys.stderr)
        sys.exit(1)