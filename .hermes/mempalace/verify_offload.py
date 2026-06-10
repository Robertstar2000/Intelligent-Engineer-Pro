#!/usr/bin/env python3
"""Verification script for MemPalace after memory offload"""

import sys
import os
sys.path.insert(0, os.path.expanduser('~/.hermes/mempalace'))

def test_mempalace():
    print("Testing MemPalace system after memory offload...")
    
    try:
        import embed
        import capture
        import tag
        
        storage_path = os.path.expanduser('~/.hermes/mempalace')
        embed.init_embedding(storage_path)
        capture.init_capture(storage_path)
        tag.init_tagging(storage_path)
        
        print("✓ Components initialized")
        
        # Test search with a query related to the offloaded content
        test_queries = [
            "MemPalace long-term memory",
            "MIFECO Virtual Consulting",
            "SaaS Stack Cloud Run",
            "memory consolidation procedure",
            "user profile Bob Mills"
        ]
        
        for query in test_queries:
            print(f"\nTesting query: '{query}'")
            results = embed.search_embeddings(query, k=3)
            if results:
                print(f"  Found {len(results)} results:")
                for mem_id, score in results:
                    print(f"    - ID: {mem_id}, Score: {score:.4f}")
            else:
                print("  No results found")
        
        # Test getting system stats
        print("\n=== System Statistics ===")
        raw_count = len([f for f in os.listdir(os.path.join(storage_path, 'raw')) 
                        if f not in ['archive', '__pycache__'] and not f.startswith('.')])
        faiss_idx = __import__('faiss').read_index(os.path.join(storage_path, 'indexes', 'faiss.index'))
        vector_count = faiss_idx.ntotal
        
        print(f"Raw event files: {raw_count}")
        print(f"FAISS vectors: {vector_count}")
        print(f"Embedding dimension: {faiss_idx.d}")
        
        print("\n✓ MemPalace system verification complete")
        return True
        
    except Exception as e:
        print(f"✗ Verification failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_mempalace()
    sys.exit(0 if success else 1)