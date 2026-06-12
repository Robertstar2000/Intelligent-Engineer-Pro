import os
import sys
sys.path.insert(0, os.path.expanduser('~/.hermes/mempalace'))
try:
    import embed
    embed_path = os.path.expanduser('~/.hermes/mempalace')
    embed.init_embedding(embed_path)
    results = embed.search_embeddings("MemPalace long-term memory FAISS embedding vector store", k=5)
    print(f"QUERY_SUCCESS:{len(results)}")
except Exception as e:
    print(f"QUERY_FAILED:{str(e)}")
