#!/usr/bin/env python3
"""
MemPalace maintenance script to be run as a cron job.
This script runs consolidation, pruning, and reports system statistics.
Using direct module imports for reliability in cron jobs.
"""
import sys
import os
import json
from datetime import datetime, timezone

# Add the mempalace directory to the path so we can import its modules directly
MEMPALACE_DIR = os.path.join(os.path.expanduser("~"), ".hermes", "mempalace")
sys.path.insert(0, MEMPALACE_DIR)

# Direct module imports (more reliable in cron jobs)
import capture
import tag
import score
import consolidate
import retrieve
import reinforce
import prune
import explain
import embed

def main():
    print("=== MemPalace Maintenance Started ===")
    
    # Initialize each component individually
    storage_path = MEMPALACE_DIR
    print(f"Initializing MemPalace components at {storage_path}")
    
    capture.init_capture(storage_path)
    tag.init_tagging(storage_path)
    score.init_scoring(storage_path)
    consolidate.init_consolidation(storage_path)
    retrieve.init_retrieval(storage_path)
    reinforce.init_reinforcement(storage_path)
    prune.init_pruning(storage_path)
    explain.init_explainability(storage_path)
    embed.init_embedding(storage_path)
    
    print("✓ MemPalace initialized")
    
    # Run consolidation
    try:
        print("\nRunning memory consolidation...")
        consolidated_count = consolidate.consolidate_memories()
        print(f"✓ Consolidated {consolidated_count} memories")
        if consolidated_count > 0:
            # Load some consolidated memories to show an example
            consolidated_memories = consolidate.load_consolidated_memories(limit=1)
            if consolidated_memories:
                first = consolidated_memories[0]
                print(f"  Example: {first.get('type', 'N/A')} - {first.get('summary', '')[:100]}...")
    except Exception as e:
        print(f"✗ Error during consolidation: {e}")
        import traceback
        traceback.print_exc()
    
    # Run pruning
    try:
        print("\nRunning memory pruning...")
        prune_stats = prune.prune_memories()
        print(f"✓ Pruning complete:")
        print(f"  Kept: {prune_stats.get('kept', 0)}")
        print(f"  Pruned: {prune_stats.get('pruned', 0)}")
        print(f"  Archived: {prune_stats.get('archived', 0)}")
        if prune_stats.get('errors'):
            print(f"  Errors: {len(prune_stats['errors'])}")
            for err in prune_stats['errors'][:3]:  # Show first 3 errors
                print(f"    - {err}")
    except Exception as e:
        print(f"✗ Error during pruning: {e}")
        import traceback
        traceback.print_exc()
    
    # Get system statistics
    try:
        print("\\nGetting system statistics...")
        # Directory counts
        dirs = {}
        for subdir in ['raw', 'semantic', 'episodic', 'procedural', 'preferences', 'indexes', 'palace']:
            dir_path = os.path.join(storage_path, subdir)
            if os.path.exists(dir_path):
                try:
                    files = [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))]
                    dirs[subdir] = len(files)
                except Exception:
                    dirs[subdir] = 0
            else:
                dirs[subdir] = 0
        # Embedding stats
        embed_initialized = embed._INDEX is not None
        embed_vectors = embed._INDEX.ntotal if embed._INDEX is not None else 0
        # Reinforcement stats
        reinforcement_path = os.path.join(storage_path, 'reinforcement.jsonl')
        reinforced_count = 0
        if os.path.exists(reinforcement_path):
            try:
                with open(reinforcement_path, 'r') as f:
                    lines = [line.strip() for line in f if line.strip()]
                    reinforced_count = len(lines)
            except Exception:
                reinforced_count = 0
        print("✓ System stats:")
        print(f"  Directories: {dirs}")
        print(f"  Embedding: {embed_initialized} (vectors: {embed_vectors})")
        print(f"  Reinforcement: {reinforced_count} memories reinforced")
    except Exception as e:
        print(f"✗ Error getting system stats: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n=== MemPalace Maintenance Completed ===")

if __name__ == "__main__":
    main()