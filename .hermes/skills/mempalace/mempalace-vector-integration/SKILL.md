---
name: mempalace-vector-integration
title: MemPalace Vector Integration
description: Semantic vector memory using FAISS + sentence-transformers — 384-dim embeddings, ~3ms per query after cache warm
tags: [mempalace, vector, faiss, embeddings, semantic-search, sentence-transformers]
required_commands: [python3]
required_environment_variables: []
setup_needed: false
---

## 🔍 MemPalace Query (MANDATORY FIRST STEP)
Before proceeding, query MemPalace for existing context:
```python
import sys, os; sys.path.insert(0, os.path.expanduser('~/.hermes/mempalace'))
import embed; embed.init_embedding(os.path.expanduser('~/.hermes/mempalace'))
results = embed.search_embeddings("domain-specific terms", k=5)
```
This retrieves previous decisions, domain-specific context, and lessons learned from the vector memory store.

# MemPalace Vector Integration

FAISS (vector index) + sentence-transformers (embedding model) for MemPalace's semantic memory layer.

> **NOTE:** The previous ONNX Runtime + ChromaDB architecture has been replaced. The live system uses `faiss-cpu` + `sentence-transformers` + a custom `embed.py` module at `~/.hermes/mempalace/`.

## System Architecture

```
Text => [all-MiniLM-L6-v2 via sentence-transformers] => 384-dim vector => [FAISS IndexFlatIP] => Search Results
```

## Location

- Module: `~/.hermes/mempalace/embed.py`
- FAISS index: `~/.hermes/mempalace/indexes/faiss.index`
- ID map: `~/.hermes/mempalace/indexes/id_map.json`
- Model: `all-MiniLM-L6-v2` (384-dim) via sentence-transformers

## Dependencies

| Package | Version (tested) | Install |
|---------|:-----------------:|---------|
| faiss-cpu | 1.14.2 | `pip install faiss-cpu` |
| sentence-transformers | 5.5.1 | `pip install sentence-transformers` |
| transformers | 5.10.2 | `pip install transformers` |
| torch | (latest CPU) | `pip install torch --index-url https://download.pytorch.org/whl/cpu` |

> **⚠️ PyTorch install note:** The CPU wheel is ~600MB. Inline `pip install torch` will time out (600s limit). **Always use** `terminal(background=true, notify_on_complete=true)` for torch installs. Do NOT combine `&` backgrounding with a foreground `pip` call — the parent shell exits before pip finishes.

## Quick Usage

```python
import sys, os
sys.path.insert(0, os.path.expanduser('~/.hermes/mempalace'))
import embed

# Initialize (loads model + existing index)
embed.init_embedding(os.path.expanduser('~/.hermes/mempalace'), 'all-MiniLM-L6-v2')

# Add a memory
embed.add_embedding("mem_001", "MIFECO provides AI consulting for small businesses")

# Semantic search
results = embed.search_embeddings("AI readiness assessment", k=5)
for memory_id, score in results:
    print(f"[{memory_id}] score={score:.4f}")

# Index stats
print(embed.get_index_stats())
```

## Full End-to-End Test

```python
import sys, os
sys.path.insert(0, os.path.expanduser('~/.hermes/mempalace'))
import embed

storage = os.path.expanduser('~/.hermes/mempalace')
embed.init_embedding(storage, 'all-MiniLM-L6-v2')

# Add test vector
embed.add_embedding('test_001', 'Test memory about FAISS vector search')
# Search
results = embed.search_embeddings('vector search test', k=3)
print(results)
# Verify
stats = embed.get_index_stats()
print(f"Vectors: {stats['total_vectors']}")
```

## Rebuilding the Index

If the index is corrupted or vectors are missing:

```python
import sys, os
sys.path.insert(0, os.path.expanduser('~/.hermes/mempalace'))
import embed
embed.init_embedding(os.path.expanduser('~/.hermes/mempalace'))
embed.rebuild_index()  # Scans all mem_*.json files across memory dirs
```

## Performance

| Operation | Time |
|--------|:----:|
| First model load (cold) | ~4-8s |
| Embedding (cached) | ~3ms |
| Search (100 vectors) | <1ms |
| Search (10k vectors) | ~2ms |

## Known Pitfalls

1. **Pass text as list to model.encode()** — `model.encode("text")` returns shape `(384,)` (flat). Always use `model.encode(["text"])` → shape `(1, 384)`. The embed.py module already handles this.
2. **Import as module, not package** — Use `import embed`, NOT `from mempalace import embed`. Add `~/.hermes/mempalace/` to `sys.path` first.
3. **PyTorch must be installed** — sentence-transformers 5.x hard-depends on torch. The ONNX fallback does not apply here.
4. **faiss-cpu vs faiss-gpu** — Use `faiss-cpu`. `faiss-gpu` is unnecessary for this workload and adds CUDA dependencies.

## Skill Registry Storage

Skills can be stored as MemPalace events for semantic search beyond `skills_list()`. See `mempalace-skill-augmentation/references/skill-registry.md` for the full pattern. Key points:

- Store each skill as a raw event with `type: skill_registry` containing name, category, description, status
- Embed with `embed.add_embedding(event_id, text)` for semantic search
- Search with `embed.search_embeddings("task description", k=10)` 
- Current registry: 220 skills stored, 267 FAISS vectors (including test vectors)
- Disabled skills remain in MemPalace but are excluded from the system prompt via `skills.disabled` in config.yaml
