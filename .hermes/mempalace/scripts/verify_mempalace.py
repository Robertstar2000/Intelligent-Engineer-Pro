import os
import sys
sys.path.insert(0, os.path.expanduser('~/.hermes/mempalace'))
try:
    import embed
    embed_path = os.path.expanduser('~/.hermes/mempalace')
    embed.init_embedding(embed_path)
    # Check index
    index_path = os.path.join(embed_path, 'indexes', 'faiss.index')
    if os.path.exists(index_path):
        import faiss
        index = faiss.read_index(index_path)
        ntotal = index.ntotal
    else:
        ntotal = 0
    # Try a search
    results = embed.search_embeddings("test", k=1)
    print(f"VERIFY_SUCCESS: index_vectors={ntotal}, search_results={len(results)}")
except Exception as e:
    print(f"VERIFY_FAILED:{str(e)}")
