#!/usr/bin/env python3
"""
Memory-Full Offload Procedure for MemPalace
Offloads all entries from HERMES memory files to MemPalace vector store
"""

import sys
import os
import json

# Add mempalace to path
sys.path.insert(0, os.path.expanduser('~/.hermes/mempalace'))

def parse_memory_file(filepath):
    """Parse a memory file and return list of entries with source info"""
    with open(filepath, 'r') as f:
        content = f.read()
   
    # Split by § markers
    sections = content.split('§')
    entries = []
   
    for i, section in enumerate(sections):
        section = section.strip()
        if not section:
            continue
           
        # Extract content (remove line numbers if present)
        lines = section.split('\\n')
        content_lines = []
        for line in lines:
            # Skip line numbers like "1|", "2|", etc.
            if '|' in line and line.split('|')[0].strip().isdigit():
                content_lines.append('|'.join(line.split('|')[1:]))
            else:
                content_lines.append(line)
       
        entry_content = '\\n'.join(content_lines).strip()
        if entry_content:
            entries.append({
                'content': entry_content,
                'index': i,
                'source': 'memory' if 'MEMORY.md' in filepath else 'user_profile'
            })
   
    return entries

def main():
    from datetime import datetime, timezone
    print("Starting MemPalace Memory-Full Offload Procedure...")
   
    # Initialize MemPalace components
    try:
        import capture
        import tag
        import embed
       
        storage_path = os.path.expanduser('~/.hermes/mempalace')
        capture.init_capture(storage_path)
        tag.init_tagging(storage_path)
        embed.init_embedding(storage_path)
        print("✓ MemPalace components initialized")
    except Exception as e:
        print(f"✗ Failed to initialize MemPalace components: {e}")
        return 1
   
    # Read memory files
    memory_file = os.path.expanduser('~/.hermes/memories/MEMORY.md')
    user_file = os.path.expanduser('~/.hermes/memories/USER.md')
   
    print(f"Reading {memory_file}...")
    memory_entries = parse_memory_file(memory_file)
    print(f"Found {len(memory_entries)} memory entries")
   
    print(f"Reading {user_file}...")
    user_entries = parse_memory_file(user_file)
    print(f"Found {len(user_entries)} user profile entries")
   
    all_entries = memory_entries + user_entries
    print(f"Total entries to process: {len(all_entries)}")
   
    # Process each entry
    success_count = 0
    for entry in all_entries:
        try:
            # Create event
            event = {
                'type': 'memory_dump' if entry['source'] == 'memory' else 'user_profile',
                'content': entry['content'],
                'context': f'memory-consolidation, {entry["source"]}',
                'timestamp': datetime.now(timezone.utc).isoformat(),
                'source': f'hermes-{entry["source"]}',
                'original_index': entry['index']
            }
           
            # Capture event
            event_id = capture.capture_event(event)
           
            # Extract and save context tags
            tags = tag.extract_context_tags(entry['content'])
            if tags:
                tag.save_context_tags(event_id, tags)
           
            # Add embedding
            embed.add_embedding(event_id, entry['content'])
           
            success_count += 1
            if success_count % 10 == 0:
                print(f"  Processed {success_count} entries...")
               
        except Exception as e:
            print(f"  ✗ Failed to process entry {entry['index']}: {type(e).__name__}: {e}")
            continue
   
    print(f"✓ Successfully processed {success_count}/{len(all_entries)} entries")
   
    # Verify results
    try:
        raw_count = len([f for f in os.listdir(os.path.join(storage_path, 'raw'))
                        if f not in ['archive', '__pycache__'] and not f.startswith('.')])
        faiss_idx = __import__('faiss').read_index(os.path.join(storage_path, 'indexes', 'faiss.index'))
        vector_count = faiss_idx.ntotal
        id_map_path = os.path.join(storage_path, 'indexes', 'id_map.json')
        id_map_count = len(json.load(open(id_map_path))) if os.path.exists(id_map_path) else 0
       
        print(f"Verification:")
        print(f"  Raw event files: {raw_count}")
        print(f"  FAISS vectors: {vector_count}")
        print(f"  ID map entries: {id_map_count}")
    except Exception as e:
        print(f"Verification warning: {e}")
   
    # Compact memory files (optional - based on preference)
    # According to the skill: "Compact the in-memory store — After offloading to MemPalace,
    # consolidate/shrink the entries in MEMORY.md and USER.md, knowing the full content
    # is safely preserved in the vector index."
   
    print("\\nMemory files will be compacted in a separate step if desired.")
    print("Offload procedure complete!")
   
    return 0

if __name__ == '__main__':
    sys.exit(main())
