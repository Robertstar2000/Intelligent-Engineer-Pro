#!/usr/bin/env python3
"""MemPalace health check script"""
import sys
import os
import json

sys.path.insert(0, os.path.expanduser("~/.hermes"))

from mempalace import init_mempalace
from mempalace.score import score_event
from mempalace.consolidate import consolidate_memories, load_consolidated_memories
from mempalace.embed import get_index_stats, add_embedding, search_embeddings
from mempalace.reinforce import get_reinforced_memories

storage = os.path.expanduser("~/.hermes/mempalace")
init_mempalace(storage)

# Count files
raw_count = len(os.listdir(os.path.join(storage, "raw")))
semantic_count = len(os.listdir(os.path.join(storage, "semantic")))
episodic_count = len(os.listdir(os.path.join(storage, "episodic")))
procedural_count = len(os.listdir(os.path.join(storage, "procedural")))

# FAISS stats
stats = get_index_stats()

print(f"RAW: {raw_count}")
print(f"SEMANTIC: {semantic_count}")
print(f"EPISODIC: {episodic_count}")
print(f"PROCEDURAL: {procedural_count}")
print(f"FAISS: {stats}")

# ID map consistency
id_map_path = os.path.join(storage, "indexes", "id_map.json")
with open(id_map_path) as f:
    loaded_id = json.load(f)
missing_raw = sum(1 for mid in loaded_id.values() if not os.path.exists(os.path.join(storage, "raw", f"{mid}.json")))
print(f"Missing raw files for FAISS IDs: {missing_raw}/{len(loaded_id)}")

# Test embedding
test_results = search_embeddings("book publishing", k=2)
print(f"Embedding search test: {len(test_results)} results returned")
if test_results:
    for mid, score in test_results[:2]:
        print(f"  - {mid}: sim={score:.4f}")

# Test scoring
test_event = {
    "type": "test",
    "content": "Test memory for scoring",
    "context": "health check",
    "timestamp": "2026-05-11T03:00:00Z",
}
test_score = score_event(test_event)
print(f"Scoring test: {test_score}")

print("Health check PASSED")
