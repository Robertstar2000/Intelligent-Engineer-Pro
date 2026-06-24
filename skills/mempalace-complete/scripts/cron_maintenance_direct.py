#!/usr/bin/env python3
"""
MemPalace maintenance script to be run as a cron job.
This script runs consolidation, pruning, and reports system statistics.
Using direct module imports for reliability in cron jobs.
"""

import sys
import os
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
    except Exception as e:
        print(f"✗ Error during consolidation: {e}")
        import traceback
        traceback.print_exc()
    
    # Run pruning
    try:
        print("\nRunning memory pruning...")
        pruned_count = prune.prune_memories()  # Returns integer count
        archive_size = prune.get_archive_size()  # Returns size in MB
        print(f"✓ Pruning complete: {pruned_count} memories pruned")
        print(f"  Archive size: {archive_size:.2f} MB")
    except Exception as e:
        print(f"✗ Error during pruning: {e}")
        import traceback
        traceback.print_exc()
    
    # Get system statistics
    try:
        print("\nGetting system statistics...")
        # Directory counts
        directories = {}
        for subdir in ['raw', 'semantic', 'episodic', 'procedural', 'preferences', 'indexes', 'palace']:
            dir_path = os.path.join(storage_path, subdir)
            if os.path.exists(dir_path):
                try:
                    files = [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))]
                    directories[subdir] = len(files)
                except Exception:
                    directories[subdir] = 0
            else:
                directories[subdir] = 0
        
        # Embedding stats
        index_stats = embed.get_index_stats()
        # Reinforcement stats: read reinforcement.jsonl
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
        print(f"  Directories: {directories}")
        print(f"  Embedding: {index_stats}")
        print(f"  Reinforcement: {reinforced_count} memories reinforced")
        print(f"  MemPalace components initialized: capture, tag, score, consolidate, retrieve, reinforce, prune, explain, embed")
    except Exception as e:
        print(f"✗ Error getting system stats: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n=== MemPalace Maintenance Completed ===")

if __name__ == "__main__":
    main()