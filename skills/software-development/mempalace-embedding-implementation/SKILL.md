---
name: mempalace-embedding-implementation
description: Practical implementation guide for MemPalace embedding integration with FAISS and sentence-transformers
version: 1.0.0
author: Hermes Agent
license: MIT
tags: [memory, mempalace, embedding, faiss, sentence-transformers, implementation]
related_skills: [mempalace-embedding-integration, mempalace-implementation]
---


## 🔍 MemPalace Query (MANDATORY FIRST STEP)
Before proceeding, query MemPalace for existing context:
```python
import sys, os; sys.path.insert(0, os.path.expanduser('~/.hermes/mempalace'))
import embed; embed.init_embedding(os.path.expanduser('~/.hermes/mempalace'))
results = embed.search_embeddings("MIFECO business process", k=5)
```
This retrieves previous decisions, domain-specific context, and lessons learned from the vector memory store.

# MemPalace Embedding Implementation

Practical implementation guide for adding vector embedding capabilities to MemPalace using FAISS and sentence-transformers. This skill captures the working approach developed through hands-on implementation, including solutions to common pitfalls.

## When to Use

Use this skill when you need to implement semantic search and cross-session recall for MemPalace memories. This is particularly useful when:
- You want to find memories based on conceptual similarity, not just keywords
- You need efficient similarity search for large memory stores
- You want to enhance Hermes' long-term memory with vector-based retrieval

## Prerequisites

1. **MemPalace directory structure** must exist at `~/.hermes/mempalace/`
2. **Raw memories** should be populated (at least a few sample files)
3. **Python environment** with ability to install packages

### Full Dependency Chain

sentence-transformers requires a deep dependency chain. Install all at once:
```bash
pip install faiss-cpu sentence-transformers transformers torch scikit-learn scipy numpy
```

**Do NOT install torch separately via `pip install torch torchvision torchaudio`** — the full package is ~600MB and pip will timeout. Use `pip install torch` (CPU-only) or the sentence-transformers bundle above which resolves the correct torch version automatically.

**If torch install times out** (common on slow connections), install in background:
```bash
pip install torch 2>&1 | tail -20 &
# Wait for completion notification, then proceed
```

Missing `scikit-learn` produces `ModuleNotFoundError: No module named 'sklearn'` even when torch and sentence-transformers appear installed. The error surfaces at import time, not install time.

## Implementation Approach

### 1. Install Required Dependencies

```bash
pip install faiss-cpu sentence-transformers numpy
```

### 2. Create the MemPalaceEmbeddingIntegration Class

The class encapsulates all embedding functionality:

```python
import json
from pathlib import Path
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

class MemPalaceEmbeddingIntegration:
    def __init__(self, base_path=None, embedding_model_name='all-MiniLM-L6-v2'):
        """
        Initialize MemPalace embedding integration.
        
        Args:
            base_path: Path to MemPalace directory (defaults to ~/.hermes/mempalace)
            embedding_model_name: Sentence Transformers model name
        """
        if base_path is None:
            base_path = Path.home() / ".hermes" / "mempalace"
        else:
            base_path = Path(base_path)
        
        self.base_path = base_path
        self.indexes_path = base_path / "indexes"
        self.id_map_path = self.indexes_path / "id_map.json"
        
        # Create necessary directories
        self.indexes_path.mkdir(parents=True, exist_ok=True)
        
        # Load or initialize FAISS index
        self.index = self._load_or_create_index()
        
        # Load or initialize ID map
        self.id_map = self._load_or_create_id_map()
        
        # Load embedding model
        print(f"Loading embedding model: {embedding_model_name}")
        self.model = SentenceTransformer(embedding_model_name)
        
        # Check if index and ID map sizes match
        if len(self.id_map) != self.index.ntotal:
            print(f"Warning: Index size ({self.index.ntotal}) doesn't match ID map size ({len(self.id_map)})")
        
        print(f"Initialized embedding integration. Index size: {self.index.ntotal}, ID map size: {len(self.id_map)}")
```

### 3. Key Methods

#### `_load_or_create_index()`
Handles loading existing FAISS index or creating a new one. Uses `IndexFlatIP` (inner product) which is equivalent to cosine similarity for normalized vectors.

#### `_load_or_create_id_map()`
Manages the mapping between FAISS vector IDs and memory IDs.

#### `extract_text_content(memory_data)`
**CRITICAL:** Handles the varied structures found in raw memory files:
- Direct text fields: 'text', 'raw_text', 'content', 'body', 'message', 'summary', 'description'
- Nested structures (payload field)
- Fallback to memory_id and source_type
- Handles lists of strings

#### `add_embedding(memory_id, text)`
- Encodes text to embedding using sentence-transformers
- **Ensures float32 dtype** (common pitfall - FAISS requires float32)
- Adds to FAISS index
- Updates ID map
- Persists to disk

#### `search_embeddings(query_text, k=5)`
- Encodes query to embedding
- Searches FAISS index
- Returns list of (memory_id, score) tuples
- Scores are cosine similarities (dot products of normalized vectors)

#### `_persist()`
Writes FAISS index and ID map to disk for cross-session persistence.

### 4. Common Pitfalls and Solutions

#### **Pitfall 1: FAISS dtype mismatch**
**Issue:** `TypeError: in method 'Index_add_ex', argument 4 of type 'faiss::NumericType'` when adding vectors.
**Solution:** Ensure all embeddings are `np.float32`. Convert if necessary:
```python
if embedding.dtype != np.float32:
    embedding = embedding.astype(np.float32)
```

#### **Pitfall 2: Memory data structure variations**
**Issue:** Raw memory files have different structures - some have 'text', others have 'raw_text' or nested 'content'.
**Solution:** Implement robust `extract_text_content()` method that tries multiple field names and handles nested structures.

#### **Pitfall 3: FAISS index creation**
**Issue:** Using wrong index type or dimension.
**Solution:** Use `IndexFlatIP(384)` for `all-MiniLM-L6-v2` model (384-dimensional embeddings). For other models, adjust dimension accordingly.

#### **Pitfall 4: sentence-transformers returns different shapes for single strings vs lists**
**Issue:** `model.encode("text")` returns shape `(384,)` — a flat array of 384 floats. But `model.encode(["text"])` returns shape `(1, 384)`. If your code does `embeddings[0].tolist()` on the flat array, you get a **single float** (the first element) instead of the 384-dim vector. This silently corrupts your FAISS index — every embedding becomes garbage.
**Symptom:** Index has vectors but semantic search returns nonsense results. Only a tiny fraction of memories end up indexed since most embeddings crash or are wrong-sized.
**Solution:** Always wrap single strings in a list before calling `model.encode()`:
```python
if isinstance(texts, str):
    texts = [texts]
embeddings = model.encode(texts, normalize_embeddings=True)
```
When iterating results, check `embeddings.shape` (2D = multiple texts, 1D = edge case), never assume the input type.

#### **Pitfall 5: Unauthenticated requests to HuggingFace**
**Issue:** Warning about unauthenticated requests when downloading model.
**Solution:** Set `HF_TOKEN` environment variable for higher rate limits, but not required for basic usage.

#### **Pitfall 7: hermes config set mangles YAML lists**
**Issue:** `hermes config set skills.disabled '["item1","item2"]'` passes a JSON string that YAML parses by splitting on commas — producing `["a", "-", "i", "t", "e", "m", "1", ...]` instead of a proper list.
**Solution:** Use Python's yaml module directly:
```python
import yaml
with open('/home/bob/.hermes/config.yaml') as f:
    cfg = yaml.safe_load(f)
cfg['skills']['disabled'] = ['skill-1', 'skill-2']
with open('/home/bob/.hermes/config.yaml', 'w') as f:
    yaml.dump(cfg, f, default_flow_style=False, allow_unicode=True)
```
**Issue:** If the embedding function is fixed, or new memories are added without embedding, the FAISS index and ID map fall out of sync with raw files. MemPalace can have thousands of raw memories with only a handful indexed.
**Solution:** Use a bulk rebuild script (`bulk_rebuild_index.py`) that reads all raw `.json` files, extracts text, generates embeddings in batches (128 at a time), and completely rebuilds the FAISS index + ID map. Run this after fixing any embedding bugs or as part of periodic maintenance.
```bash
python3 ~/.hermes/mempalace/scripts/bulk_rebuild_index.py
```

### 5. Integration with Hermes

The embedding integration is designed to work with Hermes' existing memory system:

1. **Capture hook**: When a new memory is captured, call `add_embedding(memory_id, text_content)`
2. **Retrieval enhancement**: When searching memories, use `search_embeddings(query_text)` to get semantically similar memories
3. **Maintenance**: The FAISS index and ID map are persisted, so they persist across sessions

### 6. Verification Checklist

After implementation, verify:

- [ ] FAISS index file exists at `~/.hermes/mempalace/indexes/faiss.index`
- [ ] ID map file exists at `~/.hermes/mempalace/indexes/id_map.json`
- [ ] Index size matches ID map size
- [ ] Adding a new memory increases index size by 1
- [ ] Searching for relevant queries returns appropriate memories
- [ ] Searching across sessions returns consistent results

### 7. Example Usage

```python
# Initialize
embedding_integration = MemPalaceEmbeddingIntegration()

# Add embeddings from existing memories
raw_path = Path.home() / ".hermes" / "mempalace" / "raw"
for memory_file in raw_path.glob("*.json"):
    with open(memory_file, 'r') as f:
        memory_data = json.load(f)
    text_content = embedding_integration.extract_text_content(memory_data)
    embedding_integration.add_embedding(memory_data['memory_id'], text_content)

# Search
results = embedding_integration.search_embeddings("What is Hermes?", k=5)
for memory_id, score in results:
    print(f"{memory_id}: {score:.4f}")
```

### 8. Performance Considerations

- **Model choice**: `all-MiniLM-L6-v2` offers good balance of speed/accuracy (384-dim). Larger models provide better accuracy but are slower.
- **Index type**: `IndexFlatIP` is simple and effective for smaller datasets. For larger datasets, consider `IndexIVFFlat` with quantization.
- **Batch processing**: For adding many memories, consider batching embeddings to reduce model calls.

### 9. Maintenance

- **Nightly rebuild**: Consider rebuilding the index periodically if using different embedding models
- **Memory pruning**: When memories are pruned from MemPalace, also update the embedding index (currently simplified with lazy rebuild)
- **Model updates**: If changing embedding model, recreate the index as dimensions may differ

## Lessons Learned

1. **Always validate data types** when working with FAISS - it's strict about float32
2. **Handle real-world data variability** - memory structures vary, so build robust extraction
3. **Persist early and often** - FAISS index and ID map should be saved after each modification
4. **Start small and test** - test with a few sample memories before scaling to thousands
5. **Document assumptions** - note which fields are expected and fallback strategies
6. **sentence-transformers shape inconsistency** is the most insidious bug: `encode("text")` returns flat `(384,)`, `encode(["text"])` returns `(1, 384)`. Always wrap in list. This bug silently corrupted a 6,768-document index — only 6 entries survived. Test encoding with your actual data path before scaling.
7. **Bulk rebuild is cheap** — rebuilding the full FAISS index for 6,768 memories takes ~2 minutes. Don't hesitate to rebuild from scratch after debugging.

## When to Extend

Consider extending this implementation when:
- You need to support multiple embedding models
- You have very large memory stores (millions of vectors) and need approximate nearest neighbor search
- You want to add metadata filtering alongside semantic search
- You need to support different languages or multimodal embeddings