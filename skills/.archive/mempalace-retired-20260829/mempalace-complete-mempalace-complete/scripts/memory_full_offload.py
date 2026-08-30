#!/usr/bin/env python3
"""
Memory-Full Offload Procedure for MemPalace.

This script offloads all entries from Hermes memory files (MEMORY.md and USER.md)
into the MemPalace long-term memory layer (raw store, context tags, FAISS embeddings),
then compacts the memory files.

Intended for use when the Hermes memory store approaches capacity (e.g., in cron jobs).
"""

import sys
import os
import json
import datetime
from pathlib import Path

# Add MemPalace to path
mempalace_dir = Path.home() / '.hermes' / 'mempalace'
sys.path.insert(0, str(mempalace_dir))

def main():
    print("=== MemPalace Memory-Full Offload Procedure ===")

    # Import MemPalace components (direct module import for cron job safety)
    try:
        import capture
        import tag
        import embed
        print("✓ Imported MemPalace modules")
    except Exception as e:
        print(f"✗ Failed to import MemPalace modules: {e}")
        sys.exit(1)

    # Initialize each component
    storage_path = str(mempalace_dir)
    try:
        capture.init_capture(storage_path)
        tag.init_tagging(storage_path)
        embed.init_embedding(storage_path)
        print("✓ Initialized MemPalace components")
    except Exception as e:
        print(f"✗ Failed to initialize components: {e}")
        sys.exit(1)

    # Define memory file paths
    memories_dir = Path.home() / '.hermes' / 'memories'
    memory_file = memories_dir / 'MEMORY.md'
    user_file = memories_dir / 'USER.md'

    def parse_memory_file(filepath):
        """Parse memory file, return list of entries with source and content."""
        if not filepath.exists():
            return []
        content = filepath.read_text(encoding='utf-8')
        # Split by '§' markers, ignoring empty lines
        sections = [s.strip() for s in content.split('§') if s.strip()]
        # Skip offload marker and the § marker if present
        if len(sections) >= 2 and sections[0].startswith('# Memory offloaded to MemPalace at'):
            entries = sections[2:]  # Skip offload marker and the § marker
        else:
            entries = sections  # No offload marker, treat all as entries
        return [{'source': filepath.name.replace('.md', ''), 'content': entry} for entry in entries if entry]

    # Read entries
    memory_entries = parse_memory_file(memory_file)
    user_entries = parse_memory_file(user_file)
    all_entries = memory_entries + user_entries

    print(f"📄 Found {len(memory_entries)} memory entries, {len(user_entries)} user entries, total {len(all_entries)}")

    if not all_entries:
        print("ℹ️  No new entries to offload. Exiting.")
        return

    # Process each entry
    captured_count = 0
    for idx, entry in enumerate(all_entries):
        try:
            # Create event
            event = {
                'type': 'memory_dump' if entry['source'] == 'MEMORY' else 'user_profile',
                'content': entry['content'],
                'context': f'memory-consolidation, {entry["source"].lower()}',
                'timestamp': datetime.datetime.now(datetime.timezone.utc).isoformat(),
                'source': f'hermes-{entry["source"].lower()}',
                'original_index': idx
            }
            # Capture event
            event_id = capture.capture_event(event)
            # Extract and save context tags
            tags = tag.extract_context_tags(entry['content'])
            if tags:
                tag.save_context_tags(event_id, tags)
            # Add embedding
            embed.add_embedding(event_id, entry['content'])
            captured_count += 1
            print(f"  📥 Captured entry {idx+1}/{len(all_entries)}: {entry['content'][:50]}...")
        except Exception as e:
            print(f"  ✗ Failed to capture entry {idx+1}: {e}")
            continue

    print(f"✅ Successfully captured {captured_count}/{len(all_entries)} entries.")

    # Verify storage
    try:
        raw_count = len(list((mempalace_dir / 'raw').glob('*')))
        faiss_index = mempalace_dir / 'indexes' / 'faiss.index'
        if faiss_index.exists():
            import faiss
            index = faiss.read_index(str(faiss_index))
            vector_count = index.ntotal
        else:
            vector_count = 0
        id_map_file = mempalace_dir / 'indexes' / 'id_map.json'
        if id_map_file.exists():
            id_map = json.loads(id_map_file.read_text())
            id_map_count = len(id_map)
        else:
            id_map_count = 0
        print(f"🔍 Verification: {raw_count} raw files, {vector_count} FAISS vectors, {id_map_count} ID map entries")
    except Exception as e:
        print(f"⚠️  Verification failed: {e}")

    # Compact the in-memory store: write new offload marker and just the § marker
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    memory_file.write_text(f'# Memory offloaded to MemPalace at {now}\n§\n', encoding='utf-8')
    user_file.write_text(f'# User profile offloaded to MemPalace at {now}\n§\n', encoding='utf-8')
    print("🗜️  Compacted memory files.")

    print("🎉 Memory-Full Offload Procedure completed.")

if __name__ == '__main__':
    main()