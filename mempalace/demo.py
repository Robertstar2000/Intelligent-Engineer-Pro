#!/usr/bin/env python3
"""
Demo script for MemPalace complete implementation.
Shows basic usage of the MemPalace system.
"""
import json
import os
import sys

def demo_basic_usage():
    """Demonstrate basic MemPalace usage."""
    print("=== MemPalace Basic Usage Demo ===\n")
    
    # Initialize MemPalace
    try:
        from mempalace import init_mempalace
        storage_path = init_mempalace()
        print(f"✓ MemPalace initialized at: {storage_path}")
    except Exception as e:
        print(f"✗ Failed to initialize MemPalace: {e}")
        return False
    
    # Capture a sample memory
    try:
        from mempalace.capture import capture_memory
        from mempalace.tag import tag_memory
        
        sample_event = {
            'type': 'user_interaction',
            'content': 'User asked about implementing a long-term memory system for AI agents',
            'context': 'Discussion about MemPalace architecture and FAISS integration',
            'timestamp': '2026-04-28T03:00:00Z'
        }
        
        # Tag the event
        tagged_event = tag_memory(sample_event.copy())
        print(f"✓ Event tagged with context tags: {tagged_event.get('context_tags', [])}")
        print(f"✓ Event tagged with palace tags: {tagged_event.get('palace_tags', [])}")
        
        # Capture to raw store
        memory_id = capture_memory(tagged_event)
        print(f"✓ Memory captured with ID: {memory_id}")
        
    except Exception as e:
        print(f"✗ Failed to capture memory: {e}")
        return False
    
    # Score the memory
    try:
        from mempalace.score import score_memory
        scored_event = score_memory(tagged_event)
        score = scored_event.get('score', 0.0)
        print(f"✓ Memory scored: {score:.4f}")
    except Exception as e:
        print(f"✗ Failed to score memory: {e}")
        return False
    
    # Try to add embedding (if FAISS and sentence-transformers are available)
    try:
        from mempalace.faiss_index import add_embedding
        raw_text = sample_event.get('content', '')
        if raw_text.strip():
            success = add_embedding(memory_id, raw_text)
            if success:
                print("✓ Embedding added to FAISS index")
            else:
                print("⚠ Failed to add embedding (FAISS or model may not be available)")
    except Exception as e:
        print(f"⚠ Embedding addition skipped: {e}")
    
    # Retrieve memories
    try:
        from mempalace.retrieve import retrieve_memory
        memories = retrieve_memory("long-term memory", limit=5)
        print(f"✓ Retrieved {len(memories)} memories for query 'long-term memory'")
        for i, mem in enumerate(memories[:3]):  # Show first 3
            print(f"  {i+1}. [{mem.get('retrieval_layer', 'unknown')}] {mem.get('content', '')[:50]}...")
    except Exception as e:
        print(f"✗ Failed to retrieve memories: {e}")
        return False
    
    # Explain retrieval
    try:
        from mempalace.explain import explain_retrieval
        explanation = explain_retrieval("long-term memory", memories)
        print(f"✓ Generated explanation for {explanation.get('memories_explained', 0)} memories")
    except Exception as e:
        print(f"✗ Failed to explain retrieval: {e}")
        return False
    
    # Run consolidation (if score is high enough)
    try:
        from mempalace.consolidate import run_consolidation_job
        result = run_consolidation_job(threshold=0.3, store_type='semantic')  # Low threshold for demo
        print(f"✓ Consolidation job: {result.get('consolidated_count', 0)} memories consolidated")
    except Exception as e:
        print(f"✗ Failed to run consolidation: {e}")
        return False
    
    print("\n=== Demo completed successfully ===")
    return True

def demo_hermes_hook():
    """Demonstrate Hermes-MemPalace integration hook."""
    print("\n=== Hermes-MemPalace Integration Demo ===\n")
    
    try:
        from mempalace.hermes_hook import (
            init_mempalace_hook,
            capture_to_mempalace,
            retrieve_from_mempalace,
            reinforce_in_mempalace,
            get_mempalace_status
        )
        
        # Initialize hook
        init_mempalace_hook()
        print("✓ Hermes-MemPalace hook initialized")
        
        # Capture a memory through the hook
        hook_event = {
            'type': 'task_execution',
            'content': 'Implemented MemPalace FAISS indexing system',
            'context': 'Working on long-term memory enhancement for Hermes Agent',
            'timestamp': '2026-04-28T03:15:00Z'
        }
        
        memory_id = capture_to_mempalace(hook_event)
        if memory_id:
            print(f"✓ Memory captured via hook: {memory_id}")
            
            # Reinforce the memory (simulate successful use)
            reinforced = reinforce_in_mempalace(
                memory_id, 
                context="User applied the memory system to solve a problem",
                outcome="success"
            )
            if reinforced:
                print("✓ Memory reinforced via hook")
            
            # Retrieve related memories
            memories = retrieve_from_mempalace("FAISS indexing", limit=3)
            print(f"✓ Retrieved {len(memories)} related memories via hook")
            
            # Get status
            status = get_mempalace_status()
            print(f"✓ MemPalace status: {'initialized' if status.get('initialized') else 'not initialized'}")
        else:
            print("✗ Failed to capture memory via hook")
            return False
            
    except Exception as e:
        print(f"✗ Hermes hook demo failed: {e}")
        return False
    
    print("\n=== Hermes hook demo completed ===")
    return True

if __name__ == "__main__":
    # Add the mempalace directory to the path so we can import it
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.hermes', 'mempalace'))
    
    success1 = demo_basic_usage()
    success2 = demo_hermes_hook()
    
    if success1 and success2:
        print("\n🎉 All demos completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Some demos failed.")
        sys.exit(1)