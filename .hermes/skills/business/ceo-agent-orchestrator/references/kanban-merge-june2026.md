# CEO Orchestrator + Kanban Merge (June 2026)

## Architecture
CEO dispatches via Kanban board instead of `delegate_task`. All tasks are Kanban cards with matching `agent-communications.jsonl` entries for audit trail.

## Config Requirements
```yaml
kanban:
  orchestrator_profile: "default"
plugins:
  enabled: ["kanban"]
```

## Dispatch Pattern
```python
# 1. Discover profiles
hermes profile list

# 2. Create Kanban tasks
t1 = kanban_create(
    title="writer: Draft Chapter 5",
    assignee="default",
    body="Write 3000-4000 words...",
)["task_id"]

# 3. Log to agent-communications.jsonl (audit trail)
```

## Fallback: `delegate_task`
Only for simple, single-turn tasks needing immediate response. Kanban for everything else.

## Agent Health Protocol
At each daily run:
1. Check agent-communications.jsonl for completed tasks per agent
2. Agent with NO completed tasks in 14+ days = OFFLINE
3. Diagnose: skill enabled? API keys? functional?
4. Dispatch Kanban activation task to offline agents
5. Report blockers to Bob

## Gateway Restart Required
After config changes, run: `hermes gateway restart`
