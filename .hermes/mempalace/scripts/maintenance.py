#!/usr/bin/env python3
"""
MemPalace Maintenance - Run all systems
"""
import sys
import os
import json
import logging
from datetime import datetime, timezone

sys.path.insert(0, os.path.expanduser("~/.hermes"))

from mempalace import init_mempalace
from mempalace.consolidate import consolidate_memories
from mempalace.prune import prune_memories
from mempalace.embed import get_index_stats, add_embedding, search_embeddings
from mempalace.reinforce import get_reinforced_memories
from mempalace.score import score_event

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

def main():
    storage = os.path.expanduser("~/.hermes/mempalace")
    log.info("Initializing MemPalace at %s", storage)
    init_mempalace(storage)

    # System stats
    raw_count = len(os.listdir(os.path.join(storage, "raw")))
    semantic_count = len(os.listdir(os.path.join(storage, "semantic")))
    episodic_count = len(os.listdir(os.path.join(storage, "episodic")))
    procedural_count = len(os.listdir(os.path.join(storage, "procedural")))
    
    faiss_stats = get_index_stats()
    
    log.info("=== SYSTEM STATS ===")
    log.info(f"RAW: {raw_count}")
    log.info(f"SEMANTIC: {semantic_count}")
    log.info(f"EPISODIC: {episodic_count}")
    log.info(f"PROCEDURAL: {procedural_count}")
    log.info(f"FAISS: {faiss_stats}")

    # Run consolidation
    log.info("Running consolidation...")
    try:
        consolidated = consolidate_memories()
        log.info(f"Consolidation complete: {len(consolidated) if consolidated else 0} memories promoted")
    except Exception as e:
        log.error(f"Consolidation failed: {e}")

    # Run pruning
    log.info("Running pruning...")
    try:
        pruned = prune_memories()
        log.info(f"Pruning complete: {len(pruned) if pruned else 0} memories pruned")
    except Exception as e:
        log.error(f"Pruning failed: {e}")

    log.info("=== MAINTENANCE COMPLETE ===")
    
    # Test retrieval
    try:
        results = search_embeddings("book publishing", k=1)
        log.info(f"Retrieval test: {len(results)} results")
        for mid, score in results:
            log.info(f"  Result: {mid} (similarity: {score:.3f})")
    except Exception as e:
        log.error(f"Retrieval test failed: {e}")

if __name__ == "__main__":
    main()
