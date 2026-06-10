# CEO Orchestrator + Kanban Merge — Architecture Reference
# Date: 2026-06-09

## What Changed

The CEO Orchestrator (v1.9 → v2.0) was merged with the Hermes Kanban multi-agent dispatch system.

### Before (v1.9)
- CEO used `delegate_task` for all work
- Tasks written to `agent-communications.jsonl` only
- No task persistence, no dependency tracking, no auto-retry

### After (v2.0)
- CEO uses `kanban_create` as PRIMARY dispatch mechanism
- `delegate_task` reserved for simple blocking-only tasks
- Every Kanban task gets a matching `agent-communications.jsonl` entry (audit trail)
- Kanban provides: persistence, dependency tracking, auto-retry, dashboard visibility

## Config Changes Made

```yaml
# ~/.hermes/config.yaml
kanban:
  orchestrator_profile: "default"  # was empty

plugins:
  enabled: ["kanban"]  # was empty

skills:
  enabled:  # added these 11 agent skills
    - writer, researcher, engineer, publisher, consultant,
      sales, security, brand-advocacy, saas-ops, designer, coder
```

## Agent Registry (9 agents + CEO)

See AGENTS.md at `~/.hermes/.openclaw/workspace/AGENTS.md` for the full registry.

## Key Files
- `~/.hermes/.openclaw/workspace/AGENTS.md` — unified multi-agent protocol
- `~/.hermes/.openclaw/workspace/HEARTBEAT.md` — CEO daily routine
- `~/.hermes/.openclaw/workspace/memory/agent-communications.jsonl` — audit trail
- `~/.hermes/skills/business/ceo-agent-orchestrator/SKILL.md` — updated to v2.0

## Gateway Restart Required

After config changes:
```bash
hermes gateway restart
```

## Kanban Task Lifecycle
1. CEO creates task via `kanban_create(assignee="default", ...)`
2. Kanban dispatcher spawns worker session
3. Worker executes, reports via `kanban_complete(summary, metadata)`
4. CEO monitors via dashboard or `hermes kanban tail <id>`
5. On failure: auto-retry up to `failure_limit` (default: 2)
