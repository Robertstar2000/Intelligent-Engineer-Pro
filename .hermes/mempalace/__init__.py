"""MemPalace Long-Term Memory Enhancement Layer for Hermes Agent."""

__version__ = "1.2.0"
__author__ = "Hermes Agent"

import os
import sys

# Ensure the mempalace directory is in the path for direct module imports
_mempalace_dir = os.path.dirname(os.path.abspath(__file__))
if _mempalace_dir not in sys.path:
    sys.path.insert(0, _mempalace_dir)

# Import and expose key functions for easy access
try:
    # Use direct imports (not relative) for reliability across all contexts
    import capture
    import tag
    import score
    import consolidate as consolidate_mod
    import retrieve
    import reinforce
    import prune
    import explain
    import embed

    init_capture = capture.init_capture
    capture_event = capture.capture_event
    init_tagging = tag.init_tagging
    extract_context_tags = tag.extract_context_tags
    save_context_tags = tag.save_context_tags
    init_scoring = score.init_scoring
    score_memory = score.score_memory
    init_consolidation = consolidate_mod.init_consolidation
    consolidate_memories = consolidate_mod.consolidate_memories
    init_retrieval = retrieve.init_retrieval
    retrieve_memories = retrieve.retrieve_memories
    init_reinforcement = reinforce.init_reinforcement
    reinforce_memory = reinforce.reinforce_memory
    init_pruning = prune.init_pruning
    prune_memories = prune.prune_memories
    init_explainability = explain.init_explainability
    get_system_stats = explain.get_component_status
    init_embedding = embed.init_embedding
    add_embedding = embed.add_embedding
    search_embeddings = embed.search_embeddings
    rebuild_index = embed.rebuild_index

    _initialized = False

    def init_mempalace(storage_path=None):
        """Initialize all MemPalace components."""
        global _initialized
        if _initialized:
            return

        if storage_path is None:
            storage_path = os.path.expanduser('~/.hermes/mempalace')

        init_capture(storage_path)
        init_tagging(storage_path)
        init_scoring(storage_path)
        init_consolidation(storage_path)
        init_retrieval(storage_path)
        init_reinforcement(storage_path)
        init_pruning(storage_path)
        init_explainability(storage_path)
        init_embedding(storage_path)

        _initialized = True

except ImportError as e:
    _initialized = False
    init_mempalace = None
    print(f"MemPalace initialization warning: {e}")
