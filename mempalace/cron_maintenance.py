#!/usr/bin/env python3
"""
MemPalace maintenance script to be run as a cron job.
This script runs consolidation, pruning, and reports system statistics.
"""
import sys
import os

# Add the mempalace directory to the path so we can import its modules directly
MEMPALACE_PATH = os.path.join(os.path.expanduser("~"), ".hermes", "mempalace")
sys.path.insert(0, MEMPALACE_PATH)

try:
    import capture
    import tag
    import score
    import consolidate
    import retrieve
    import reinforce
    import prune
    import explain
    import embed
    print("Successfully imported MemPalace modules")
except Exception as e:
    print(f"Failed to import MemPalace modules: {e}")
    sys.exit(1)

def main():
    print("=== MemPalace Maintenance Started ===")
    
    storage_path = MEMPALACE_PATH

    # Initialize components
    try:
        capture.init_capture(storage_path)
        print("✓ Capture initialized")
    except Exception as e:
        print(f"✗ Failed to initialize capture: {e}")

    try:
        tag.init_tagging(storage_path)
        print("✓ Tagging initialized")
    except Exception as e:
        print(f"✗ Failed to initialize tagging: {e}")

    try:
        score.init_scoring(storage_path)
        print("✓ Scoring initialized")
    except Exception as e:
        print(f"✗ Failed to initialize scoring: {e}")

    try:
        consolidate.init_consolidation(storage_path)
        print("✓ Consolidation initialized")
    except Exception as e:
        print(f"✗ Failed to initialize consolidation: {e}")

    try:
        retrieve.init_retrieval(storage_path)
        print("✓ Retrieval initialized")
    except Exception as e:
        print(f"✗ Failed to initialize retrieval: {e}")

    try:
        reinforce.init_reinforcement(storage_path)
        print("✓ Reinforcement initialized")
    except Exception as e:
        print(f"✗ Failed to initialize reinforcement: {e}")

    try:
        prune.init_pruning(storage_path)
        print("✓ Pruning initialized")
    except Exception as e:
        print(f"✗ Failed to initialize pruning: {e}")

    try:
        explain.init_explainability(storage_path)
        print("✓ Explainability initialized")
    except Exception as e:
        print(f"✗ Failed to initialize explainability: {e}")

    try:
        embed.init_embedding(storage_path)
        print("✓ Embedding initialized")
    except Exception as e:
        print(f"✗ Failed to initialize embedding: {e}")

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
        print(f"  Archived: {prune_stats.get('archived', False)}")
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
        print("\nGetting system statistics...")
        stats = {
            "directories": {},
            "embedding": {"initialized": embed._index is not None, "total_vectors": embed._index.ntotal if embed._index else 0},
            "reinforcement": {"total_memories_reinforced": 0}
        }
        # Count files in each directory
        for subdir in ["raw", "semantic", "episodic", "procedural", "preferences", "indexes", "palace"]:
            dir_path = os.path.join(storage_path, subdir)
            if os.path.exists(dir_path):
                try:
                    files = [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))]
                    stats["directories"][subdir] = len(files)
                except Exception:
                    stats["directories"][subdir] = 0
            else:
                stats["directories"][subdir] = 0
        # Reinforcement stats
        reinforcement_path = os.path.join(storage_path, "reinforcement.jsonl")
        if os.path.exists(reinforcement_path):
            with open(reinforcement_path, "r") as f:
                lines = [line.strip() for line in f if line.strip()]
                stats["reinforcement"]["total_memories_reinforced"] = len(lines)
        print("✓ System stats:")
        print(f"  Directories: {stats['directories']}")
        print(f"  Embedding: {stats['embedding']}")
        print(f"  Reinforcement: {stats['reinforcement']}")
    except Exception as e:
        print(f"✗ Error getting system stats: {e}")
        import traceback
        traceback.print_exc()

    print("\n=== MemPalace Maintenance Completed ===")

if __name__ == "__main__":
    main()