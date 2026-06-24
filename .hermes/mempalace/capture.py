"""MemPalace Capture System - Append-only event logging with auto-embedding."""

import json
import os
from datetime import datetime, timezone
from typing import Dict, Any, Optional

_storage_path: str = None
_auto_embed: bool = True  # Whether to auto-embed captured events


def init_capture(storage_path: str):
    """Initialize the capture system."""
    global _storage_path
    _storage_path = storage_path
    raw_dir = os.path.join(_storage_path, 'raw')
    os.makedirs(raw_dir, exist_ok=True)
    print(f"Capture system initialized at {_storage_path}")


def capture_event(event: Dict[Any, Any], auto_embed: bool = True) -> str:
    """
    Capture an event to the raw store.
    
    After storing the event, automatically generates a FAISS embedding
    if embedding dependencies are available and auto_embed is True.
    
    Args:
        event: Dictionary containing event data
        auto_embed: Whether to auto-generate embedding for this event
        
    Returns:
        str: Generated event ID
    """
    if _storage_path is None:
        raise RuntimeError("Capture system not initialized. Call init_capture() first.")
    
    # Generate event ID based on timestamp and content hash
    timestamp = datetime.now(timezone.utc).isoformat()
    content_str = json.dumps(event, sort_keys=True)
    event_id = f"evt_{hash(content_str)}_{int(datetime.now(timezone.utc).timestamp())}"
    
    # Add metadata
    event_with_meta = {
        **event,
        'event_id': event_id,
        'captured_at': timestamp,
        'storage_version': '1.2.0'
    }
    
    # Write to raw store as JSONL (one event per line)
    raw_file = os.path.join(_storage_path, 'raw', f'{event_id}.jsonl')
    with open(raw_file, 'w') as f:
        f.write(json.dumps(event_with_meta) + '\n')
    
    # Auto-generate embedding if enabled
    if auto_embed and _auto_embed:
        _try_embed_event(event_id, event)
    
    return event_id


def _try_embed_event(event_id: str, event: Dict[Any, Any]):
    """
    Try to generate and store a FAISS embedding for a captured event.
    
    Silently skips if embedding dependencies are not available.
    Only embeds events that have meaningful 'content' text.
    
    Args:
        event_id: The event ID
        event: The event dictionary
    """
    try:
        # Import embed module dynamically to avoid hard dependency
        from embed import HAS_DEPENDENCIES, add_embedding, _model, _index
        
        if not HAS_DEPENDENCIES or _model is None or _index is None:
            return
        
        # Extract text to embed - prefer 'content' field
        content = event.get('content', '')
        if not content or not isinstance(content, str):
            return
        
        # Skip very short content (noise)
        if len(content.strip()) < 10:
            return
        
        # Generate and store embedding
        add_embedding(event_id, content)
        
    except Exception:
        # Silently fail - embedding is best-effort, not critical
        pass


def get_raw_event_count() -> int:
    """Get count of raw events stored."""
    if _storage_path is None:
        return 0
    raw_dir = os.path.join(_storage_path, 'raw')
    if not os.path.exists(raw_dir):
        return 0
    
    count = 0
    for fname in os.listdir(raw_dir):
        if fname == 'archive':
            continue
        if fname.endswith('.jsonl'):
            fpath = os.path.join(raw_dir, fname)
            try:
                with open(fpath, 'r') as f:
                    count += sum(1 for line in f if line.strip())
            except:
                pass
        elif fname.endswith('.json'):
            count += 1
    return count
