"""
MemPalace Vector Memory Layer
==============================
Hybrid: ONNX Runtime (embedding) + ChromaDB (vector store)
Model: all-MiniLM-L6-v2 (384-dim, 23MB, ~5ms per text)

Usage:
    from vector_memory import VectorMemory
    
    vm = VectorMemory()
    vm.add("mem_001", "text content", {"tag": "consulting"})
    results = vm.search("query text", k=5)
"""

import os
import json
import time
import numpy as np
from pathlib import Path

# ── Config ──────────────────────────────────────────────────────────────
STORAGE_DIR = Path(os.environ.get("VECTOR_STORAGE_DIR", str(Path.home() / ".hermes" / "mempalace-vector")))
MODEL_CACHE = str(STORAGE_DIR / "models")
COLLECTIONS_DIR = STORAGE_DIR / "collections"

# ── Lazy-loaded singletons ─────────────────────────────────────────────
_model = None
_tokenizer = None
_clients = {}  # collection_name -> chromadb.Collection

def _get_embedder():
    """Lazy-load the ONNX-optimized embedding model (~5ms per inference)."""
    global _model, _tokenizer
    if _model is not None:
        return _model, _tokenizer
    if _tokenizer is not None:
        # ONNX model was cached - _model is the ORT model
        return _model, _tokenizer

    from sentence_transformers import SentenceTransformer
    import torch

    # Use sentence-transformers with ONNX backend
    model_name = "sentence-transformers/all-MiniLM-L6-v2"
    STORAGE_DIR.mkdir(parents=True, exist_ok=True)

    # Cache the model locally
    model_path = STORAGE_DIR / "models" / "all-MiniLM-L6-v2"
    if not model_path.exists():
        print(f"[vector_memory] Downloading model {model_name}...")
        _model = SentenceTransformer(model_name, cache_folder=str(STORAGE_DIR / "models"))
        _model.save(str(model_path))
    else:
        _model = SentenceTransformer(str(model_path))

    # Check if we can use ONNX for speedup
    try:
        from optimum.onnxruntime import ORTModelForFeatureExtraction
        from transformers import AutoTokenizer
        # Try ONNX export (one-time)
        onnx_path = model_path / "onnx"
        if not onnx_path.exists():
            print("[vector_memory] Exporting to ONNX for 2-5x speedup...")
            ort_model = ORTModelForFeatureExtraction.from_pretrained(
                str(model_path), export=True, provider="CPUExecutionProvider"
            )
            ort_model.save_pretrained(str(onnx_path))
            tokenizer = AutoTokenizer.from_pretrained(str(model_path))
            tokenizer.save_pretrained(str(onnx_path))
        else:
            print("[vector_memory] Loading ONNX model...")
            ort_model = ORTModelForFeatureExtraction.from_pretrained(
                str(onnx_path), provider="CPUExecutionProvider"
            )
            tokenizer = AutoTokenizer.from_pretrained(str(onnx_path))
        # Cache ONNX model in globals
        _model = ort_model
        _tokenizer = tokenizer
        return _model, _tokenizer
    except ImportError:
        print("[vector_memory] Using PyTorch backend (install optimum+onnx for 2-5x speedup)")
        return _model, None

    return _model, _tokenizer


def _get_chroma_client():
    """Lazy-load ChromaDB persistent client."""
    import chromadb
    COLLECTIONS_DIR.mkdir(parents=True, exist_ok=True)
    return chromadb.PersistentClient(path=str(COLLECTIONS_DIR))


def _get_collection(name="mempalace"):
    """Get or create a ChromaDB collection."""
    if name in _clients:
        return _clients[name]
    import chromadb
    client = _get_chroma_client()
    try:
        collection = client.get_collection(name)
    except (ValueError, chromadb.errors.NotFoundError):
        collection = client.create_collection(
            name=name,
            metadata={"hnsw:space": "cosine", "description": "MemPalace semantic memory"}
        )
    _clients[name] = collection
    return collection


class VectorMemory:
    """Semantic vector memory backed by ChromaDB + ONNX embeddings."""

    def __init__(self, collection_name="mempalace"):
        self.collection_name = collection_name
        self.collection = _get_collection(collection_name)

    def embed(self, texts):
        """Convert text(s) to embedding vectors. Returns list of lists."""
        if isinstance(texts, str):
            texts = [texts]

        embedder, tokenizer = _get_embedder()

        # ONNX model path (ORTModelForFeatureExtraction)
        if tokenizer is not None:
            import torch
            import numpy as np
            inputs = tokenizer(texts, padding=True, truncation=True, return_tensors="pt", max_length=256)
            with torch.no_grad():
                outputs = embedder(**inputs)
            # Mean pooling + normalize
            token_emb = outputs.last_hidden_state
            attention_mask = inputs["attention_mask"].unsqueeze(-1).float()
            masked = token_emb * attention_mask
            summed = masked.sum(dim=1)
            counts = attention_mask.sum(dim=1).clamp(min=1e-9)
            embeddings = (summed / counts).numpy()
            # Normalize
            norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
            embeddings = embeddings / norms
            return embeddings.tolist()
        else:
            # SentenceTransformer path
            embeddings = embedder.encode(texts, normalize_embeddings=True)
            return embeddings.tolist()

    def add(self, memory_id, text, metadata=None):
        """Add a memory entry with vector embedding."""
        embedding = self.embed(text)[0]  # [0] to unwrap the list-of-lists
        meta = metadata or {}
        meta["text"] = text
        meta["added_at"] = time.time()

        self.collection.add(
            ids=[memory_id],
            embeddings=[embedding],
            metadatas=[meta]
        )
        return memory_id

    def search(self, query, k=5, where=None):
        """Search for semantically similar memories. Returns list of dicts."""
        query_embedding = self.embed(query)[0]

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=min(k, self.collection.count() or 1),
            where=where
        )

        output = []
        for i in range(len(results["ids"][0])):
            output.append({
                "id": results["ids"][0][i],
                "score": float(1 - results["distances"][0][i]),  # cosine -> similarity
                "metadata": results["metadatas"][0][i],
            })
        return output

    def delete(self, memory_id):
        """Remove a memory entry."""
        self.collection.delete(ids=[memory_id])

    def update(self, memory_id, text, metadata=None):
        """Update text and re-embed."""
        self.delete(memory_id)
        return self.add(memory_id, text, metadata)

    def count(self):
        """Number of entries in the collection."""
        return self.collection.count()

    def list_collections(self):
        """List all available collections."""
        client = _get_chroma_client()
        return client.list_collections()

    def get(self, memory_id):
        """Get a specific entry by ID."""
        result = self.collection.get(ids=[memory_id])
        if result["ids"]:
            return {
                "id": result["ids"][0],
                "metadata": result["metadatas"][0] if result["metadatas"] else None,
            }
        return None


# ── CLI Entry Point ────────────────────────────────────────────────────
if __name__ == "__main__":
    import sys
    vm = VectorMemory()

    if len(sys.argv) < 2:
        print("Usage:")
        print("  python vector_memory.py add <id> <text> [--tag TAG]")
        print("  python vector_memory.py search <query> [--k 5]")
        print("  python vector_memory.py get <id>")
        print("  python vector_memory.py delete <id>")
        print("  python vector_memory.py count")
        print(f"\nCurrent collection: {vm.count()} entries")
        sys.exit(0)

    cmd = sys.argv[1]

    if cmd == "add":
        mem_id = sys.argv[2]
        text = sys.argv[3]
        tag = None
        if "--tag" in sys.argv:
            tag = sys.argv[sys.argv.index("--tag") + 1]
        vm.add(mem_id, text, {"tag": tag} if tag else None)
        print(f"Added: {mem_id}")

    elif cmd == "search":
        query = sys.argv[2]
        k = 5
        if "--k" in sys.argv:
            k = int(sys.argv[sys.argv.index("--k") + 1])
        results = vm.search(query, k=k)
        print(f"\nTop {k} results for: '{query}'\n")
        for r in results:
            meta = r["metadata"]
            text_preview = meta.get("text", "")[:120]
            print(f"  [{r['id']}] score={r['score']:.4f}")
            print(f"    {text_preview}...")
            print()

    elif cmd == "get":
        mem_id = sys.argv[2]
        result = vm.get(mem_id)
        if result:
            print(f"ID: {result['id']}")
            print(f"Metadata: {json.dumps(result['metadata'], indent=2)[:500]}")
        else:
            print(f"Not found: {mem_id}")

    elif cmd == "delete":
        mem_id = sys.argv[2]
        vm.delete(mem_id)
        print(f"Deleted: {mem_id}")

    elif cmd == "count":
        print(f"{vm.count()} entries in '{vm.collection_name}'")
