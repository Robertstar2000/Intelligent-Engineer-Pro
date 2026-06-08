#!/usr/bin/env python3
"""
Capture a memory event and store it in the MemPalace raw layer.
"""
import json
import uuid
import sys
import os
from datetime import datetime

def capture_memory(raw_text, source_type="chat", provisional_type="semantic", 
                   user_id="default", session_id="default", entities=None, 
                   topics=None, salience=0.5, reliability=0.5, evidence_ref=None):
    """Capture a memory event."""
    memory_id = str(uuid.uuid4())
    timestamp = datetime.utcnow().isoformat() + "Z"
    
    event = {
        "memory_id": memory_id,
        "user_id": user_id,
        "session_id": session_id,
        "timestamp": timestamp,
        "raw_text": raw_text,
        "source_type": source_type,
        "provisional_type": provisional_type,
        "entities": entities or [],
        "topics": topics or [],
        "salience": salience,
        "reliability": reliability,
        "evidence_ref": evidence_ref or f"chat:{session_id}:0"
    }
    
    # Store in raw layer (append-only)
    raw_dir = os.path.expanduser("~/.hermes/mempalace/raw")
    os.makedirs(raw_dir, exist_ok=True)
    
    # Store as individual JSON files per event (could also be a log file)
    event_file = os.path.join(raw_dir, f"{memory_id}.json")
    with open(event_file, 'w') as f:
        json.dump(event, f, indent=2)
    
    return memory_id

if __name__ == "__main__":
    # Example usage: read from stdin or command line
    if len(sys.argv) > 1:
        raw_text = " ".join(sys.argv[1:])
    else:
        raw_text = sys.stdin.read().strip()
    
    if not raw_text:
        print("Error: No raw text provided", file=sys.stderr)
        sys.exit(1)
    
    memory_id = capture_memory(raw_text)
    print(f"Captured memory: {memory_id}")