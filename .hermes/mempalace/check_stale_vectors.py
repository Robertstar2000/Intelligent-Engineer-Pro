#!/usr/bin/env python3
"""Check for stale FAISS vectors after MemPalace maintenance"""

import json
import os
import sys

try:
    import faiss
except ImportError:
    print("ERROR: FAISS not available")
    sys.exit(1)

def check_stale_vectors():
    print("Checking for stale FAISS vectors...")
    
    storage_path = os.path.expanduser('~/.hermes/mempalace')
    index_path = os.path.join(storage_path, 'indexes', 'faiss.index')
    id_map_path = os.path.join(storage_path, 'indexes', 'id_map.json')
    
    # Load FAISS index and ID map
    try:
        index = faiss.read_index(index_path)
        print(f"Loaded FAISS index with {index.ntotal} vectors")
    except Exception as e:
        print(f"ERROR: Failed to load FAISS index: {e}")
        return 1
        
    try:
        with open(id_map_path, 'r') as f:
            id_map = json.load(f)
        # Convert keys to int for consistency
        id_map = {int(k): v for k, v in id_map.items()}
        print(f"Loaded ID map with {len(id_map)} entries")
    except Exception as e:
        print(f"ERROR: Failed to load ID map: {e}")
        return 1
    
    # Collect all live memory IDs from raw store
    raw_path = os.path.join(storage_path, 'raw')
    live_ids = set()
    
    if os.path.exists(raw_path):
        for filename in os.listdir(raw_path):
            if filename == 'archive' or filename.startswith('.'):
                continue
            filepath = os.path.join(raw_path, filename)
            try:
                if filename.endswith('.jsonl'):
                    # Handle .jsonl format (one event per line)
                    with open(filepath, 'r') as f:
                        for line_num, line in enumerate(f, 1):
                            line = line.strip()
                            if not line:
                                continue
                            try:
                                event = json.loads(line)
                                if isinstance(event, dict):
                                    # Try different possible ID field names
                                    memory_id = (event.get('memory_id') or 
                                               event.get('id') or 
                                               event.get('event_id'))
                                    if memory_id:
                                        live_ids.add(str(memory_id))
                            except json.JSONDecodeError:
                                # Skip invalid JSON lines
                                continue
                elif filename.endswith('.json'):
                    # Handle .json format (single event per file)
                    with open(filepath, 'r') as f:
                        try:
                            event = json.load(f)
                            if isinstance(event, dict):
                                memory_id = (event.get('memory_id') or 
                                           event.get('id') or 
                                           event.get('event_id'))
                                if memory_id:
                                    live_ids.add(str(memory_id))
                            # Also handle case where file contains list of events
                            elif isinstance(event, list):
                                for item in event:
                                    if isinstance(item, dict):
                                        memory_id = (item.get('memory_id') or 
                                                   item.get('id') or 
                                                   item.get('event_id'))
                                        if memory_id:
                                            live_ids.add(str(memory_id))
                        except json.JSONDecodeError:
                            pass
            except Exception as e:
                print(f"Warning: Could not read {filepath}: {e}")
    
    print(f"Found {len(live_ids)} live memory IDs in raw store")
    
    # Find stale entries in ID map
    stale_entries = []
    for fid, memory_id in id_map.items():
        if str(memory_id) not in live_ids:
            stale_entries.append((fid, memory_id))
    
    print(f"Found {len(stale_entries)} stale FAISS entries")
    
    if stale_entries:
        print("\nStale entries (first 10):")
        for fid, memory_id in stale_entries[:10]:
            print(f"  FAISS ID {fid} -> Memory ID {memory_id}")
        
        if len(stale_entries) > 10:
            print(f"  ... and {len(stale_entries) - 10} more")
        
        print(f"\nStale percentage: {len(stale_entries)/len(id_map)*100:.1f}%")
        
        # Ask if user wants to rebuild index to remove stale vectors
        print("\nRecommendation: Run index rebuild to remove stale vectors.")
        print("You can use: python3 -c \"import sys, os; sys.path.insert(0, os.path.expanduser('~/.hermes/mempalace')); import embed; embed.init_embedding(os.path.expanduser('~/.hermes/mempalace')); embed.rebuild_index()\"")
        
        return 0  # Not an error, just stale vectors found
    else:
        print("✓ No stale FAISS vectors found")
        return 0

if __name__ == '__main__':
    sys.exit(check_stale_vectors())