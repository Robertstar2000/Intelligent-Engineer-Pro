#!/usr/bin/env python3
"""Test script for MemPalace implementation."""

import sys
import os
import json
from datetime import datetime, timezone

# Add the mempalace directory to path
sys.path.insert(0, os.path.expanduser('~/.hermes/mempalace'))

def test_basic_functionality():
    """Test basic MemPalace functionality."""
    print("Testing MemPalace basic functionality...")
    
    storage_path = os.path.expanduser('~/.hermes/mempalace')
    
    # Import modules
    try:
        import capture
        import tag
        import score
        import consolidate
        import retrieve
        import reinforce
        import prune
        import explain
        import embed
        print("✓ All modules imported successfully")
    except Exception as e:
        print(f"✗ Failed to import modules: {e}")
        return False
    
    # Initialize components
    try:
        capture.init_capture(storage_path)
        tag.init_tagging(storage_path)
        score.init_scoring(storage_path)
        consolidate.init_consolidation(storage_path)
        retrieve.init_retrieval(storage_path)
        reinforce.init_reinforcement(storage_path)
        prune.init_pruning(storage_path)
        explain.init_explainability(storage_path)
        embed.init_embedding(storage_path)
        print("✓ All components initialized successfully")
    except Exception as e:
        print(f"✗ Failed to initialize components: {e}")
        return False
    
    # Test capture
    try:
        test_event = {
            'type': 'user_interaction',
            'content': 'User asked about book progress and editorial criteria',
            'context': 'MIFECO dashboard, book writing session',
            'timestamp': datetime.now(timezone.utc).isoformat()
        }
        event_id = capture.capture_event(test_event)
        print(f"✓ Event captured with ID: {event_id}")
    except Exception as e:
        print(f"✗ Failed to capture event: {e}")
        return False
    
    # Test tagging
    try:
        context_tags = tag.extract_context_tags(
            test_event['content'], 
            test_event['type']
        )
        palace_tags = tag.get_palace_tags(context_tags)
        tag.save_context_tags(event_id, context_tags)
        print(f"✓ Context tags extracted: {context_tags}")
        print(f"✓ Palace tags mapped: {palace_tags}")
    except Exception as e:
        print(f"✗ Failed in tagging: {e}")
        return False
    
    # Test scoring
    try:
        composite_score, individual_scores = score.score_memory(test_event)
        print(f"✓ Memory scored: {composite_score:.3f}")
        print(f"  Individual scores: {individual_scores}")
    except Exception as e:
        print(f"✗ Failed to score memory: {e}")
        return False
    
    # Test consolidation
    try:
        memory_id = consolidate.consolidate_memory(test_event)
        if memory_id:
            print(f"✓ Memory consolidated with ID: {memory_id}")
        else:
            print("○ Memory not consolidated (below threshold or other criteria)")
    except Exception as e:
        print(f"✗ Failed to consolidate memory: {e}")
        return False
    
    # Test retrieval
    try:
        results = retrieve.retrieve_memories("book progress", limit_per_layer=2)
        total_results = sum(len(layer) for layer in results.values())
        print(f"✓ Retrieval test: {total_results} results found")
        for layer, memories in results.items():
            if memories:
                print(f"  {layer}: {len(memories)} memories")
    except Exception as e:
        print(f"✗ Failed in retrieval: {e}")
        return False
    
    # Test explainability
    try:
        exp_id = explain.log_consolidation_decision(
            test_event, composite_score, individual_scores, 
            'semantic', True
        )
        print(f"✓ Explanation logged: {exp_id}")
    except Exception as e:
        print(f"✗ Failed to log explanation: {e}")
        return False
    
    # Test embedding (if dependencies available)
    try:
        if embed.HAS_DEPENDENCIES:
            embed_success = embed.add_embedding(event_id, test_event['content'])
            if embed_success:
                search_results = embed.search_embeddings("book progress", k=3)
                print(f"✓ Embedding test: {len(search_results)} search results")
            else:
                print("○ Embedding add failed")
        else:
            print("○ Embedding test skipped (dependencies missing)")
    except Exception as e:
        print(f"✗ Failed in embedding test: {e}")
        return False
    
    print("\n✓ All basic functionality tests passed!")
    return True

def test_memory_offload_procedure():
    """Test the Memory-Full Offload Procedure."""
    print("\nTesting Memory-Full Offload Procedure...")
    
    storage_path = os.path.expanduser('~/.hermes/mempalace')
    
    # Read current memory files
    memory_file = os.path.join(storage_path, '..', 'memories', 'MEMORY.md')
    user_file = os.path.join(storage_path, '..', 'memories', 'USER.md')
    
    try:
        # Read memory files
        memory_content = ""
        user_content = ""
        
        if os.path.exists(memory_file):
            with open(memory_file, 'r') as f:
                memory_content = f.read()
        
        if os.path.exists(user_file):
            with open(user_file, 'r') as f:
                user_content = f.read()
        
        print(f"MEMORY.md size: {len(memory_content)} chars")
        print(f"USER.md size: {len(user_content)} chars")
        
        # Parse entries separated by § markers
        def parse_entries(content, source_type):
            entries = []
            if not content:
                return entries
            
            # Split by § markers
            sections = content.split('§')
            for i, section in enumerate(sections):
                section = section.strip()
                if section and not section.startswith('#'):  # Skip headers
                    entries.append({
                        'content': section,
                        'source': source_type,
                        'index': i
                    })
            return entries
        
        memory_entries = parse_entries(memory_content, 'memory')
        user_entries = parse_entries(user_content, 'user_profile')
        all_entries = memory_entries + user_entries
        
        print(f"Found {len(memory_entries)} memory entries and {len(user_entries)} user entries")
        
        if not all_entries:
            print("○ No entries to offload")
            return True
        
        # Initialize MemPalace components (using direct import approach as recommended for cron jobs)
        import capture
        import tag
        import embed
        
        capture.init_capture(storage_path)
        tag.init_tagging(storage_path)
        embed.init_embedding(storage_path)
        
        # Process each entry
        offloaded_count = 0
        for entry in all_entries:
            try:
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
                
                # Extract and save tags
                context_tags = tag.extract_context_tags(
                    event['content'], 
                    event['type']
                )
                tag.save_context_tags(event_id, context_tags)
                
                # Add embedding
                embed.add_embedding(event_id, event['content'])
                
                offloaded_count += 1
                print(f"✓ Offloaded {entry['source']} entry {entry['index']} -> {event_id}")
                
            except Exception as e:
                print(f"✗ Failed to offload entry {entry['index']}: {e}")
                continue
        
        print(f"✓ Memory-Full Offload Procedure completed: {offloaded_count} entries offloaded")
        
        # Verify offload
        raw_count = 0
        raw_dir = os.path.join(storage_path, 'raw')
        if os.path.exists(raw_dir):
            for fname in os.listdir(raw_dir):
                if fname.endswith('.jsonl') and fname != 'archive':
                    fpath = os.path.join(raw_dir, fname)
                    try:
                        with open(fpath, 'r') as f:
                            raw_count += sum(1 for line in f if line.strip())
                    except:
                        pass
        
        print(f"✓ Raw event count after offload: {raw_count}")
        
        # Check FAISS index
        if embed.HAS_DEPENDENCIES:
            index_stats = embed.get_index_stats()
            print(f"✓ FAISS index vectors: {index_stats.get('index_ntotal', 0)}")
            print(f"✓ ID map entries: {index_stats.get('id_map_size', 0)}")
        
        return True
        
    except Exception as e:
        print(f"✗ Memory-Full Offload Procedure failed: {e}")
        return False

if __name__ == '__main__':
    print("=" * 60)
    print("MemPalace Implementation Test")
    print("=" * 60)
    
    success = True
    success &= test_basic_functionality()
    success &= test_memory_offload_procedure()
    
    print("\n" + "=" * 60)
    if success:
        print("✓ ALL TESTS PASSED - MemPalace implementation is working!")
    else:
        print("✗ SOME TESTS FAILED - Please check the output above")
    print("=" * 60)