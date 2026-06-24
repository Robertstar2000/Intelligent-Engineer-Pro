import sys, os
sys.path.insert(0, os.path.expanduser('~/.hermes/mempalace'))

# Direct module imports
import capture
import tag
import score
import consolidate
import retrieve
import reinforce
import prune
import explain
import embed

storage_path = os.path.expanduser('~/.hermes/mempalace')
print(f'Initializing MemPalace components at {storage_path}')

capture.init_capture(storage_path)
tag.init_tagging(storage_path)
score.init_scoring(storage_path)
consolidate.init_consolidation(storage_path)
retrieve.init_retrieval(storage_path)
reinforce.init_reinforcement(storage_path)
prune.init_pruning(storage_path)
explain.init_explainability(storage_path)
embed.init_embedding(storage_path)

print('✓ MemPalace initialized')

# Run consolidation
try:
    print('\\nRunning memory consolidation...')
    consolidated_count = consolidate.consolidate_memories()
    print(f'✓ Consolidated {consolidated_count} memories')
except Exception as e:
    print(f'✗ Error during consolidation: {e}')
    import traceback
    traceback.print_exc()

# Run pruning
try:
    print('\\nRunning memory pruning...')
    pruned_count = prune.prune_memories()  # This returns an integer
    print(f'✓ Pruning complete: {pruned_count} memories pruned')
    # Get archive size
    archive_size = prune.get_archive_size()
    print(f'  Archive size: {archive_size:.2f} MB')
except Exception as e:
    print(f'✗ Error during pruning: {e}')
    import traceback
    traceback.print_exc()

# Get system statistics
try:
    print('\\nGetting system statistics...')
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
    # Embedding stats via embed.get_index_stats()
    embed_stats = embed.get_index_stats()
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
    print('✓ System stats:')
    print(f'  Directories: {dirs}')
    print(f'  Embedding: {embed_stats}')
    print(f'  Reinforcement: {reinforced_count} memories reinforced')
except Exception as e:
    print(f'✗ Error getting system stats: {e}')
    import traceback
    traceback.print_exc()

print('\\n=== MemPalace Maintenance Completed ===')