#!/usr/bin/env python3
"""
Simple MemPalace maintenance script for cron jobs.
Runs consolidation and actual pruning.
"""

import sys
import os
import time

# Add the mempalace directory to the path
MEMPALACE_PATH = os.path.join(os.path.expanduser("~"), ".hermes", "mempalace")
sys.path.insert(0, MEMPALACE_PATH)

def main():
    print("=== MemPalace Maintenance Started ===")
    start_time = time.time()
    
    storage_path = MEMPALACE_PATH
    
    try:
        # Import and initialize components
        import capture
        import tag
        import score
        import consolidate
        import prune
        import reinforce
        import explain
        import embed
        
        print("Initializing MemPalace components...")
        capture.init_capture(storage_path)
        tag.init_tagging(storage_path)
        score.init_scoring(storage_path)
        consolidate.init_consolidation(storage_path)
        prune.init_pruning(storage_path)
        reinforce.init_reinforcement(storage_path)
        explain.init_explainability(storage_path)
        embed.init_embedding(storage_path)
        print("✓ All components initialized")
        
    except Exception as e:
        print(f"Failed to initialize MemPalace components: {e}")
        sys.exit(1)
    
    # Run consolidation
    try:
        print("\nRunning memory consolidation...")
        consolidated_count = consolidate.consolidate_memories()
        print(f"✓ Consolidated {consolidated_count} memories")
    except Exception as e:
        print(f"✗ Error during consolidation: {e}")
        import traceback
        traceback.print_exc()
    
    # Run actual pruning (not dry run)
    try:
        print("\nRunning memory pruning...")
        prune_stats = prune.prune_memories(dry_run=False)
        print(f"✓ Pruning complete:")
        print(f"  Pruned: {prune_stats.get('pruned', 0)} memories")
        print(f"  Archived: {prune_stats.get('archived', 0)} memories")
    except Exception as e:
        print(f"✗ Error during pruning: {e}")
        import traceback
        traceback.print_exc()
    
    # Get basic system statistics
    try:
        print("\nGetting system statistics...")
        stats = {}
        
        # Count files in each directory
        for subdir in ["raw", "semantic", "episodic", "procedural", "preferences"]:
            dir_path = os.path.join(storage_path, subdir)
            if os.path.exists(dir_path):
                files = [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))]
                stats[subdir] = len(files)
            else:
                stats[subdir] = 0
        
        # Get FAISS vector count
        if hasattr(embed, '_INDEX') and embed._INDEX is not None:
            stats["faiss_vectors"] = embed._INDEX.ntotal
        else:
            stats["faiss_vectors"] = 0
            
        # Count reinforcement entries
        reinforcement_path = os.path.join(storage_path, "reinforcement.jsonl")
        if os.path.exists(reinforcement_path):
            with open(reinforcement_path, "r") as f:
                lines = [line.strip() for line in f if line.strip()]
                stats["reinforcement_entries"] = len(lines)
        else:
            stats["reinforcement_entries"] = 0
        
        print("✓ System stats:")
        for key, value in stats.items():
            print(f"  {key}: {value}")
            
    except Exception as e:
        print(f"✗ Error getting system stats: {e}")
        import traceback
        traceback.print_exc()
    
    total_time = time.time() - start_time
    print(f"\n=== MemPalace Maintenance Completed in {total_time:.2f} seconds ===")

if __name__ == "__main__":
    main()