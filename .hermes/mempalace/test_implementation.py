"""
Test implementation for MemPalace system
"""

import os
import sys
import json
from datetime import datetime, timezone

# Add the mempalace directory to path
sys.path.insert(0, os.path.join(os.path.expanduser("~"), ".hermes", "mempalace"))

import mempalace

def test_basic_functionality():
    """Test basic MemPalace functionality"""
    print("=== Testing MemPalace Basic Functionality ===")
    
    # Initialize MemPalace
    print("1. Initializing MemPalace...")
    mempalace.init_mempalace()
    print(f"   Storage path: {mempalace.get_storage_path()}")
    
    # Test capture
    print("\n2. Testing memory capture...")
    test_event = {
        'type': 'user_interaction',
        'content': 'User asked about machine learning algorithms',
        'context': 'Discussion about ML projects',
        'timestamp': datetime.now(timezone.utc).isoformat()
    }
    
    event_id = mempalace.capture_memory(test_event)
    print(f"   Captured event with ID: {event_id}")
    
    # Test retrieval
    print("\n3. Testing memory retrieval...")
    memories = mempalace.retrieve_memory('machine learning', k=5)
    print(f"   Retrieved {len(memories)} memories")
    for i, mem in enumerate(memories):
        print(f"   {i+1}. [{mem.get('retrieval_layer', 'unknown')}] {mem.get('content', str(mem)[:100])}")
    
    # Test scoring
    print("\n4. Testing scoring system...")
    from mempalace import capture, score
    recent_events = capture.load_recent_events(days=1)
    if recent_events:
        scored = score.score_events(recent_events)
        print(f"   Scored {len(scored)} events")
        for event in scored[:3]:
            print(f"   Event {event.get('id', 'unknown')[:8]}: score = {event.get('mempalace_score', 0):.3f}")
    
    # Test consolidation
    print("\n5. Testing consolidation...")
    from mempalace import consolidate
    consolidated_count = consolidate.consolidate_memories(recent_events)
    print(f"   Consolidated {consolidated_count} memories")
    
    # Test tagging
    print("\n6. Testing tagging system...")
    from mempalace import tag
    test_text = "User discussed Python programming and machine learning algorithms"
    context_tags = tag.extract_context_tags(test_text)
    palace_tags = tag.extract_palace_tags(context_tags)
    print(f"   Text: '{test_text}'")
    print(f"   Context tags: {context_tags}")
    print(f"   Palace tags: {palace_tags}")
    
    # Test embedding system
    print("\n7. Testing embedding system...")
    from mempalace import embed
    stats = embed.get_index_stats()
    print(f"   Embedding index stats: {stats}")
    
    if stats.get('status') == 'initialized':
        # Test adding an embedding
        test_id = "test_embedding_" + datetime.now().strftime('%Y%m%d_%H%M%S')
        success = embed.add_embedding(test_id, "This is a test about artificial intelligence")
        print(f"   Adding embedding: {'Success' if success else 'Failed'}")
        
        # Test searching
        if success:
            results = embed.search_embeddings("artificial intelligence", k=3)
            print(f"   Search results: {len(results)} found")
            for mem_id, score in results:
                print(f"     - {mem_id}: {score:.3f}")
    
    print("\n=== Test Complete ===")
    return True

if __name__ == "__main__":
    test_basic_functionality()