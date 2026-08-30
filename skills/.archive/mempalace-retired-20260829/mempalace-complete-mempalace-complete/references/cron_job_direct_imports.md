# Direct Module Imports for MemPalace in Cron Jobs

## Problem
When running MemPalace operations in cron jobs or isolated environments, package-level imports like `from mempalace import init_mempalace` can fail with `ModuleNotFoundError` due to path resolution issues.

## Solution
Use direct module imports at the top level and initialize each component individually.

## Implementation

```python
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
    # Initialize each component individually
    storage_path = MEMPALACE_DIR
    
    capture.init_capture(storage_path)
    tag.init_tagging(storage_path)
    score.init_scoring(storage_path)
    consolidate.init_consolidation(storage_path)
    retrieve.init_retrieval(storage_path)
    reinforce.init_reinforcement(storage_path)
    prune.init_pruning(storage_path)
    explain.init_explainability(storage_path)
    embed.init_embedding(storage_path)
    
    # Now use the functions directly
    # Example: capture an event
    event_id = capture.capture_event({
        'type': 'user_interaction',
        'content': 'User asked about system status',
        'context': 'cron job health check',
        'timestamp': datetime.now(timezone.utc).isoformat()
    })
    
    # Run maintenance operations
    consolidated_count = consolidate.consolidate_memories()
    prune_stats = prune.prune_memories()
    stats = explain.get_explanation_stats()
    
    return {
        'consolidated': consolidated_count,
        'pruning': prune_stats,
        'stats': stats
    }

if __name__ == "__main__":
    main()
```

## Key Points
1. **Path Configuration**: Always add the mempalace directory to sys.path before importing
2. **Direct Imports**: Import each module directly (`import capture`) rather than through the package
3. **Individual Initialization**: Call each component's init function explicitly
4. **Component Order**: Initialize in dependency order (capture → tag → score → consolidate → retrieve → reinforce → prune → explain → embed)
5. **Timezone Handling**: Use timezone-aware datetime objects for timestamp consistency

## Verification
This approach has been tested and verified to work in:
- Hermes cron job environments
- Isolated subprocess contexts
- Non-interactive sessions
- Systems with restricted package import capabilities

## Related Files
- See `scripts/cron_maintenance_direct.py` for a complete implementation
- Refer to the existing "Maintenance Script Fixes for Cron Jobs" section in SKILL.md for additional guidelines