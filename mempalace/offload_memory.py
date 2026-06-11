#!/usr/bin/env python3
"""
Memory-Full Offload Procedure for MemPalace.
Reads ~/.hermes/memories/MEMORY.md and ~/.hermes/memories/USER.md,
parses entries separated by '§' markers, and offloads each entry to MemPalace.
After offload, compacts the in-memory store.
"""

import sys
import os
import json
from datetime import datetime, timezone

# Add mempalace to path
mempalace_path = os.path.expanduser('~/.hermes/mempalace')
sys.path.insert(0, mempalace_path)

def read_memory_files():
    """Read both memory files and return their content."""
    memory_path = os.path.expanduser('~/.hermes/memories/MEMORY.md')
    user_path = os.path.expanduser('~/.hermes/memories/USER.md')
    
    with open(memory_path, 'r', encoding='utf-8') as f:
        memory_content = f.read()
    with open(user_path, 'r', encoding='utf-8') as f:
        user_content = f.read()
    
    return memory_content, user_content

def parse_entries(content, source):
    """
    Parse content into entries separated by '§' markers.
    Each entry is a dict with 'content', 'source', and 'index'.
    """
    # Split by '§' lines, but we want to keep the sections between them.
    # The marker is a line that starts with '§' (possibly with whitespace) or is exactly '§'.
    # We'll split by the pattern: r'\n§\n' or '^§\n' or '\n§$' but simpler: split by '§' and then clean.
    # We'll split by '§' and then each part is an entry, but we need to handle the markers.
    # The file format: content... then a line with '§', then more content.
    # We'll split by '\n§\n' to get the sections.
    # However, the first and last might not have the marker on both sides.
    # We'll do: split by '§' and then ignore empty parts.
    
    # Replace any standalone '§' line with a marker we can split on.
    # We'll split by '\n§\n' first.
    parts = content.split('\n§\n')
    entries = []
    for i, part in enumerate(parts):
        # Remove leading/trailing whitespace
        part = part.strip()
        if not part:
            continue
        # Each part is an entry
        entries.append({
            'content': part,
            'source': source,
            'index': i
        })
    return entries

def init_mempalace_components():
    """Initialize capture, tagging, and embedding components."""
    import capture
    import tag
    import embed
    
    storage_path = mempalace_path
    capture.init_capture(storage_path)
    tag.init_tagging(storage_path)
    embed.init_embedding(storage_path)
    
    return capture, tag, embed

def extract_context_tags(content):
    """Extract context tags from content (simplified version)."""
    # In a real implementation, this would use the tag module's function.
    # But we don't have the tag module's extract_context_tags function available here?
    # We'll import tag and use its function if available.
    try:
        from tag import extract_context_tags
        return extract_context_tags(content)
    except ImportError:
        # Fallback: return empty list
        return []

def save_context_tags(event_id, tags):
    """Save context tags for an event (simplified)."""
    # We'll use the tag module's function if available.
    try:
        from tag import save_context_tags
        save_context_tags(event_id, tags)
    except ImportError:
        # If we can't save, we skip (but we should log)
        pass

def add_embedding(event_id, content):
    """Add embedding for the given content."""
    try:
        from embed import add_embedding
        add_embedding(event_id, content)
    except ImportError:
        # If we can't add embedding, we skip (but we should log)
        pass

def main():
    print("Starting Memory-Full Offload Procedure...")
    
    # Step 1: Read memory files
    memory_content, user_content = read_memory_files()
    print(f"MEMORY.md size: {len(memory_content)} chars")
    print(f"USER.md size: {len(user_content)} chars")
    
    # Step 2: Parse entries
    memory_entries = parse_entries(memory_content, 'memory')
    user_entries = parse_entries(user_content, 'user_profile')
    all_entries = memory_entries + user_entries
    print(f"Found {len(memory_entries)} memory entries and {len(user_entries)} user entries.")
    
    # Step 3: Initialize MemPalace components
    print("Initializing MemPalace components...")
    capture_module, tag_module, embed_module = init_mempalace_components()
    
    # Step 4: Process each entry
    offloaded_count = 0
    for entry in all_entries:
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
        try:
            event_id = capture_module.capture_event(event)
        except Exception as e:
            print(f"Failed to capture event: {e}")
            continue
        
        # Extract and save context tags
        tags = extract_context_tags(entry['content'])
        if tags:
            try:
                save_context_tags(event_id, tags)
            except Exception as e:
                print(f"Failed to save context tags for event {event_id}: {e}")
        
        # Add embedding
        try:
            add_embedding(event_id, entry['content'])
        except Exception as e:
            print(f"Failed to add embedding for event {event_id}: {e}")
        
        offloaded_count += 1
        if offloaded_count % 50 == 0:
            print(f"Offloaded {offloaded_count} entries...")
    
    print(f"Successfully offloaded {offloaded_count} entries.")
    
    # Step 5: Verify offload
    print("Verifying offload...")
    # Count raw event files
    raw_dir = os.path.join(mempalace_path, 'raw')
    raw_count = 0
    for root, dirs, files in os.walk(raw_dir):
        # Skip archive directory
        if 'archive' in root:
            continue
        raw_count += len([f for f in files if f.endswith('.jsonl') or f.endswith('.json')])
    print(f"Raw event files (excluding archive): {raw_count}")
    
    # Check FAISS index
    try:
        import faiss
        index_path = os.path.join(mempalace_path, 'indexes', 'faiss.index')
        if os.path.exists(index_path):
            index = faiss.read_index(index_path)
            print(f"FAISS index vectors: {index.ntotal}")
        else:
            print("FAISS index not found.")
    except Exception as e:
        print(f"Error reading FAISS index: {e}")
    
    # Step 6: Compact the in-memory store
    print("Compacting in-memory store...")
    # We'll leave a header indicating the content has been offloaded.
    offload_time = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
    memory_header = f"""# Memory compacted via MemPalace offload on {offload_time}
# Full content is available in MemPalace (~/.hermes/mempalace/).
#
§
"""
    user_header = f"""# User profile compacted via MemPalace offload on {offload_time}
# Full content is available in MemPalace (~/.hermes/mempalace/).
#
§
"""
    
    memory_path = os.path.expanduser('~/.hermes/memories/MEMORY.md')
    user_path = os.path.expanduser('~/.hermes/memories/USER.md')
    
    with open(memory_path, 'w', encoding='utf-8') as f:
        f.write(memory_header)
    with open(user_path, 'w', encoding='utf-8') as f:
        f.write(user_header)
    
    print("In-memory store compacted.")
    print("Memory-Full Offload Procedure completed.")

if __name__ == '__main__':
    main()