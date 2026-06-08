#!/usr/bin/env python3

"""
MemPalace Hermes Integration Hook
Automatically captures Hermes memories into MemPalace
"""

import os
import json
from datetime import datetime

# MemPalace storage path
PALACE_PATH = os.path.expanduser("~/.hermes/mempalace")

def capture_to_mempalace(memory_data):
    """
    Capture a Hermes memory event into MemPalace raw store.
    This function is called whenever Hermes stores a memory.
    """
    try:
        # Generate a unique memory ID
        memory_id = f"mem_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{hash(str(memory_data)) % 1000000}"
        
        # Create memory record with additional metadata
        memory_record = {
            'id': memory_id,
            'hermes_id': memory_data.get('id', memory_id),
            'type': memory_data.get('type', 'generic'),
            'content': memory_data.get('content', ''),
            'context': memory_data.get('context', ''),
            'tags': memory_data.get('tags', []),
            'timestamp': datetime.utcnow().isoformat(),
            'source': 'hermes',
            'raw_text': memory_data.get('content', '') or memory_data.get('text', ''),
            'score': 0.0,  # Will be calculated by scoring system
            'consolidated': False,
            'reinforced': 0
        }
        
        # Save to raw store
        raw_path = os.path.join(PALACE_PATH, 'raw', f"{memory_id}.json")
        with open(raw_path, 'w') as f:
            json.dump(memory_record, f, indent=2)
        
        print(f"[MemPalace] Captured memory {memory_id} to raw store")
        
        # Add to embedding index (if embedding system is active)
        try:
            # Try to import and use embedding functions
            from embedding_integration import add_embedding
            add_embedding(memory_id, memory_record['raw_text'])
            print(f"[MemPalace] Added embedding for {memory_id}")
        except ImportError:
            pass
        
        return memory_id
        
    except Exception as e:
        print(f"[MemPalace] Error capturing memory: {str(e)}")
        return None

def hermes_memory_hook(memory_data):
    """
    Main hook function - called by Hermes memory tool.
    This should be referenced in Hermes configuration.
    """
    memory_id = capture_to_mempalace(memory_data)
    
    # Return the memory ID to Hermes (optional)
    return memory_id

if __name__ == "__main__":
    # Test the capture function
    test_memory = {
        'type': 'test',
        'content': 'This is a test memory to verify MemPalace integration.',
        'context': 'Hermes Agent testing',
        'tags': ['test', 'integration']
    }
    test_id = capture_to_mempalace(test_memory)
    print(f"Test memory captured: {test_id}")
