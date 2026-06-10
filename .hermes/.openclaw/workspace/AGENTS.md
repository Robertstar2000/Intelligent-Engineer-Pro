# AGENTS.md — MIFECO Unified Multi-Agent System
# Merged: CEO Orchestrator + Hermes Kanban + Agent Communications Protocol
# Version: 2.0 — June 2026

## Architecture Overview

The MIFECO agent ecosystem uses THREE integrated layers:

1. **CEO Orchestrator** (this session / cron) — strategic direction, task assignment, reporting to Bob
2. **Kanban Board** — task dispatch, tracking, auto-retry, dependency management
3. **Agent Communications** (`memory/agent-communications.jsonl`) — inter-agent messaging

### How They Connect

```
CEO Orchestrator (this session)
    │
    ├── Writes tasks → Kanban board (via kanban_create)
    │                   ↓
    │               Kanban Dispatcher spawns worker sessions
    │                   ↓
    │               Workers execute tasks, report back via kanban_complete
    │                   ↓
    │               CEO monitors via Kanban dashboard + agent-communications.jsonl
    │
    └── Also writes/reads → agent-communications.jsonl (for cross-agent messaging)
```

**KEY CHANGE**: CEO now dispatches via Kanban instead of `delegate_task`. This gives:
- Task persistence (survives crashes/restarts)
- Dependency tracking (T3 waits for T1+T2)
- Auto-retry on failure (up to `failure_limit`)
- Visibility (Kanban dashboard shows all agent activity)
- Audit trail (SQLite-backed history)

---

## Agent Registry (9 Agents)

| Agent ID | Role | Skills | Product Lines | Status |
|----------|------|--------|---------------|--------|
| `ceo` | Chief Executive Orchestrator | ceo-agent-orchestrator | All (strategy) | ✅ Active (this session) |
| `writer` | Book/content writing | manuscript-creation, novel-writing, humanizer | Books | ✅ Active |
| `researcher` | Market & competitive research | exa-web-search, web_search | Books, SaaS, Consulting | ✅ Active (watch mode) |
| `engineer` | Software dev & architecture | terraform-engineer, github | SaaS | ⚠️ Needs config |
| `publisher** | Book publishing (KDP) | book-deliverable-kdp, book-publishing | Books | ⚠️ Needs config |
| `consultant` | Virtual consulting delivery | virtual-consulting | Consulting | ⚠️ Needs config |
| `sales` | Outbound sales & pipeline | sales-pipeline, seo-backlink | Books, SaaS | ⚠️ Needs config |
| `security` | Security audits | security-auditor | All | ⚠️ Needs config |
| `brand-advocate` | Brand content distribution | brand-advocacy, content-marketing | All | ⚠️ Needs config |
| `saas-ops` | SaaS deployment & ops | saas-operations | SaaS | ⚠️ Needs config |

### Getting Non-Operational Agents Online

For each ⚠️ agent, the CEO should:

1. **Verify the skill exists** — `skill_view(name='<skill>')` to confirm
2. **Create a Kanban profile** (or use `default` profile with skill injection)
3. **Dispatch an activation task** via Kanban to verify the agent can start
4. **Report to Bob** any blockers (missing API keys, broken deps)

---

## CEO Orchestrator Protocol

### Task Assignment Flow (Kanban-Native)

**Instead of `delegate_task`**, use Kanban:

```python
# 1. DISCOVER AVAILABLE PROFILES
#    Run: hermes profile list
#    Or check Kanban: kanban_list(assignee="<name>")

# 2. CREATE TASKS
t1 = kanban_create(
    title="writer: Draft Chapter 5 of 'The Red Charter'",
    assignee="default",  # or dedicated profile name
    body="Write 3000-4000 words. Context: Chapters 1-4 complete. Focus on the colony's first conflict with Earth forces.",
    tenant="mifeco",
)["task_id"]

t2 = kanban_create(
    title="researcher: Competitive analysis for PM Accelerator",
    assignee="default",
    body="Identify top 5 PM SaaS competitors, their pricing, features, and gaps. Use web_search and web_extract.",
    tenant="mifeco",
)["task_id"]

# SYNTHESIS TASK (depends on T1 and T2)
t3 = kanban_create(
    title="ceo: Synthesize writer output + research into board report",
    assignee="default",
    body="Read results from T1 (chapter draft) and T2 (competitive analysis). Write executive summary for Bob.",
    parents=[t1, t2],
    tenant="mifeco",
)["task_id"]

# 3. LOG to agent-communications.jsonl (for audit trail)
#    Every Kanban creation should have a matching jsonl entry
```

### Direct `delegate_task` (for simple, blocking tasks only)

For tasks that NEED an immediate response (e.g., "look up this one fact"), `delegate_task` is still appropriate. Rule of thumb:

- **`delegate_task`** — Need answer in this turn. Simple. No audit trail needed.
- **Kanban** — Multi-step work. Needs persistence. Other agents depend on it. Audit trail matters.

### Step 0: Discover Profiles (MANDATORY before Kanban dispatch)

Before creating Kanban tasks, ALWAYS run:

```bash
hermes profile list
```

Cache the result. If `hermes` CLI isn't available from your context, create tasks with `assignee="default"` — the Kanban dispatcher will route `default` assignees to the active profile.

---

## Agent Communications Protocol

### File: `memory/agent-communications.jsonl`

**Format:**
```json
{"timestamp":"2026-06-09T10:00:00Z","task_id":"kanban-uuid","from":"ceo","to":"writer","type":"request","priority":"high","task":"Write chapter 5","payload":{"instructions":"...","deadline":"2026-06-10T08:00:00Z"},"status":"pending"}
```

**Status values:** `pending → assigned → active → completed` (or `failed`)

**Every Kanban task creation should have a matching jsonl entry.** That's how the CEO tracks what was dispatched without querying Kanban directly.

**Every Kanban completion should have a matching jsonl entry.** That's how the CEO knows the work is done.

### Daily Focus Rotation

| Day | Primary | Secondary |
|-----|---------|-----------|
| Monday | SaaS Growth & Engineering | Security Audit |
| Tuesday | Books & Publishing | Marketing |
| Wednesday | Consulting & Sales | Brand Advocacy |
| Thursday | SaaS UX & Features | Market Research |
| Friday | Strategy & Planning | Financial Review |
| Saturday | Deep Work (Writer or Engineer) | System Maintenance |
| Sunday | Weekly Briefing | Board Report to Bob |

---

## Kanban Task Lifecycle

### For CEO (Orchestrator):
1. Create tasks via `kanban_create(assignee="<profile>", ...)`
2. Log to `agent-communications.jsonl`
3. Monitor via `hermes kanban tail <id>` or dashboard
4. On completion: read result, synthesize, report to Bob

### For Workers (when spawned by Kanban):
1. **Orient** — read task body, check `agent-communications.jsonl` for context
2. **Claim** — Kanban auto-claims on dispatch
3. **Execute** — do the work
4. **Report** — `kanban_complete(summary="...", metadata={...})`
5. **Communicate** — log to `agent-communications.jsonl`

### Recovery (CEO responsibility):
- If worker fails: Kanban auto-retries up to `failure_limit` (default: 2)
- If task stuck >4hrs: `hermes kanban reclaim <id>` and reassign
- If agent skill missing: log to Bob via Telegram for manual fix

---

## Heartsbeat & Self-HeartBEAT.md

If `HEARTBEAT.md` exists at `/home/bob/.hermes/.openclaw/workspace/HEARTBEAT.md`, it should contain the CEO agent's daily routine:

1. Read `agent-communications.jsonl` for pending/completed tasks
2. Check Kanban board status
3. Assign new tasks per the day's focus
4. Report to Bob if urgent issues

If the file doesn't exist, initialize it with:
```
# HEARTBEAT.md — CEO Agent Daily Routine

1. Read last 50 lines of memory/agent-communications.jsonl
2. Check Kanban: any failed or stuck tasks?
3. Assign today's focus tasks per the rotation table
4. If nothing needs attention, stay quiet
5. Alert Bob only on: failed tasks, security issues, client escalations
```

---

## Profiles Configuration

For dedicated agent profiles (recommended for production):

```yaml
# In ~/.hermes/config.yaml → profiles:
writer:
  model: google/gemini-3.1-flash-lite-preview:nitro
  skills: [manuscript-creation, novel-writing, humanizer]
engineer:
  model: anthropic/claude-sonnet-4
  skills: [terraform-engineer, github]
# ... etc
```

For now, all agents can run on the `default` profile with skill injection via Kanban task body.

---

## Board of Directors
- **Bob (Human)**: CEO, Chairman, final authority
- **CEO Agent**: Orchestrator, reports to Bob, manages agent team
- **CIO**: Same as CEO in this architecture (merged role)

## Escalation Path
- Agent → CEO (via Kanban failure + jsonl alert)
- CEO → Bob (via Telegram, only for urgent/critical)
- Auto-escalate: security breach, client complaint, deadline <24hrs, cost spike >20%

## Reliability Rules
- `timeoutSeconds: 3600` minimum for all Kanban tasks
- Auto-save progress every 500 words (writer agent)
- On error: Kanban marks "failed", auto-retries once
- If terminated: On restart, CEO reads jsonl + Kanban state to resume

## What Changed (v2.0)
- CEO now dispatches via Kanban instead of `delegate_task`
- `agent-communications.jsonl` is the audit trail for all Kanban tasks
- Workers are spawned by Kanban dispatcher, not CEO directly
- Recovery is Kanban-native (reclaim/reassign)
- All 9 agents from AGENTS.md registry are now in the task routing table
