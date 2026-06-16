# Round-Robin State File Pattern for Cron Jobs

Used for the SaaS External Comparison Posts cron job. This pattern maintains rotation state across cron runs so each execution picks the "next" item in a pool without repeating.

## When to Use

You have a cron job that needs to:
- Rotate through a list of items round-robin style
- Pick a "next" item that hasn't been used yet
- Maintain state between runs
- Reset when the pool is exhausted

## Pattern

### State File Format (`saas-comparison-state.json`)

```json
{
  "next_internal_index": 0,
  "used_external_apps": [],
  "last_run": null,
  "total_posts_generated": 0
}
```

### Rotation Logic (Python)

```python
import json
import os

STATE_FILE = "~/.hermes/pipeline-engine/data/my-state.json"

# Internal pool (items to rotate through)
INTERNAL_POOL = ["Item A", "Item B", "Item C"]

# External pool (items to pick uniquely until exhausted)
EXTERNAL_POOL = ["Thing 1", "Thing 2", "Thing 3", ...]

# Load or create state
if os.path.exists(os.path.expanduser(STATE_FILE)):
    with open(os.path.expanduser(STATE_FILE)) as f:
        state = json.load(f)
else:
    state = {
        "next_internal_index": 0,
        "used_external_apps": [],
        "last_run": None,
        "total_posts_generated": 0
    }

# Pick next internal item (round-robin)
internal_index = state["next_internal_index"]
internal_pick = INTERNAL_POOL[internal_index]
state["next_internal_index"] = (internal_index + 1) % len(INTERNAL_POOL)

# Pick next unused external item
used = set(state["used_external_apps"])
available = [a for a in EXTERNAL_POOL if a not in used]
if not available:
    # All used — reset
    state["used_external_apps"] = []
    available = list(EXTERNAL_POOL)
external_pick = available[0]
state["used_external_apps"].append(external_pick)

# Record run
state["last_run"] = datetime.now().isoformat()
state["total_posts_generated"] += 1

# Save state
with open(os.path.expanduser(STATE_FILE), 'w') as f:
    json.dump(state, f, indent=2)

# Use the picks
result = f"Comparing {internal_pick} vs {external_pick}..."
```

## Key Design Decisions

1. **Separate state from generated-content log**: The state file tracks only rotation position. The `generated-blog-posts.json` file tracks what was actually published. Two different concerns.

2. **Reset on pool exhaustion**: When all external items have been used, clear `used_external_apps` and start over. This prevents the job from stalling.

3. **Modulo arithmetic for internal rotation**: `(index + 1) % len(pool)` wraps around automatically when the end is reached.

4. **Run on every cron tick**: The cron schedule controls timing; the state file ensures each run gets a unique pairing until the pool wraps.

## Example: SaaS External Comparison Cron Job

The `SaaS External Comparison Posts` cron job (daily at 10:00 AM) uses this pattern:
- Internal pool: 11 MIFECO products/servicess (Project Hypatia Pro → Risk Management, round-robin)
- External pool: 20 business applications (Microsoft Project → Planview)
- State file: `~/.hermes/pipeline-engine/data/saas-comparison-state.json`

First run: Project Hypatia Pro vs Microsoft Project
Second run: PM Accelerator vs Asana
Third run: VibraEngineer vs Jira
etc. through all 220 unique pairings (11 × 20), then the external pool resets.