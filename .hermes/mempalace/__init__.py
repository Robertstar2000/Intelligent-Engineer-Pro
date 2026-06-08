"""
MemPalace Long-Term Memory Enhancement Layer for Hermes Agent
"""

import os
import json
from datetime import datetime
import capture
import tag
import score
import consolidate
import retrieve
import reinforce
import prune
import explain
import embed

# Storage path
_STORAGE_PATH = os.path.join(os.path.expanduser("~"), ".hermes", "mempalace")

def init_mempalace(storage_path=None):
    """Initialize MemPalace system"""
    global _STORAGE_PATH
    if storage_path:
        _STORAGE_PATH = storage_path
    
    # Ensure directory structure exists
    for subdir in ['raw', 'semantic', 'episodic', 'procedural', 'preferences', 'indexes', 'palace']:
        os.makedirs(os.path.join(_STORAGE_PATH, subdir), exist_ok=True)
    
    # Initialize components
    capture.init_capture(_STORAGE_PATH)
    tag.init_tagging(_STORAGE_PATH)
    score.init_scoring(_STORAGE_PATH)
    consolidate.init_consolidation(_STORAGE_PATH)
    retrieve.init_retrieval(_STORAGE_PATH)
    reinforce.init_reinforcement(_STORAGE_PATH)
    prune.init_pruning(_STORAGE_PATH)
    explain.init_explainability(_STORAGE_PATH)
    embed.init_embedding(_STORAGE_PATH)
    
    print(f"MemPalace initialized at {_STORAGE_PATH}")

def consolidate_memories(events=None):
    """Consolidate high-scoring memories to appropriate stores"""
    return consolidate.consolidate_memories(events)

def prune_memories(dry_run=False):
    """Prune low-value, old memories"""
    return prune.prune_memories(dry_run)

def get_system_stats():
    """Get system statistics"""
    if not _STORAGE_PATH:
        return {}
    
    stats = {
        "directories": {},
        "embedding": {"initialized": False, "total_vectors": 0},
        "reinforcement": {"total_memories_reinforced": 0}
    }
    
    # Count files in each directory
    for subdir in ["raw", "semantic", "episodic", "procedural", "preferences", "indexes", "palace"]:
        dir_path = os.path.join(_STORAGE_PATH, subdir)
        if os.path.exists(dir_path):
            try:
                files = [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))]
                stats["directories"][subdir] = len(files)
            except Exception:
                stats["directories"][subdir] = 0
        else:
            stats["directories"][subdir] = 0
    
    # Embedding stats
    try:
        import embed
        if embed._INDEX is not None:
            stats["embedding"]["initialized"] = True
            stats["embedding"]["total_vectors"] = embed._INDEX.ntotal
    except Exception:
        pass
    
    # Reinforcement stats
    try:
        reinforcement_path = os.path.join(_STORAGE_PATH, "reinforcement.jsonl")
        if os.path.exists(reinforcement_path):
            with open(reinforcement_path, "r") as f:
                lines = [line.strip() for line in f if line.strip()]
                stats["reinforcement"]["total_memories_reinforced"] = len(lines)
    except Exception:
        pass
    
    return stats


def capture_memory(event_data):
    """Capture a memory event"""
    return capture.capture_event(event_data)

def retrieve_memory(query, layers=None, k=10):
    """Retrieve memories using layered approach"""
    return retrieve.retrieve_memories(query, layers, k)

def get_storage_path():
    """Get the current storage path"""
    return _STORAGE_PATH

# Auto-initialize if imported directly
if __name__ != "__main__":
    init_mempalace()