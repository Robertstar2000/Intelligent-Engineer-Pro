# Daily CEO Briefing Template (Mon-Sat)

> Used by ceo-agent-orchestrator for daily cron runs (Monday through Saturday). This is the standard format for the CEO's daily report to Bob.

## Format

```
# 🏢 MIFECO CEO DAILY BRIEFING — [Day], [DATE]

## 📊 STATE OF THE UNION

| Product Line | Status | Notes |
|---|---|---|
| **SaaS (3 apps)** | 🟢/🟡/🔴 | One-line: all operational / specific issue |
| **Books Pipeline** | 🟢/🟡/🔴 | One-line: X/Y KDP-ready / regression detected / etc. |
| **Consulting** | 🟢/🟡/🔴 | One-line: active engagements / email deadlock / etc. |
| **Website** | 🟢/🟡/🔴 | One-line: up / down / issues |

## 📋 TASKS ASSIGNED TODAY

| Task ID | Agent | Task | Priority |
|---|---|---|---|
| `ceo-[agent]-[YYYYMMDD]-[seq]` | **[agent]** | Brief description | High/Normal/Low |

## ⚡ EXECUTED ACTIONS (CEO Direct)

1. **Action name** — Brief description of what was done inline
2. ...

## 🚨 URGENT ITEMS FOR BOB

### 🔴 P0: [Title]
- **Description**: What's wrong and what's at stake
- **Action needed**: Specific step Bob should take

### 🟡 P1: [Title]
- **Description**: Context
- **Action needed**: What would help

## 🔮 TOMORROW'S FOCUS ([Next Day] — [Rotation Theme])

- [Specific task/check based on rotation]
- [Second priority]

## 📈 MARKET INTELLIGENCE SNAPSHOT (if applicable)

- [One-line insight from latest market data]
- [Competitor/market movement]

---

*CEO Agent | MIFECO | [YYYY-MM-DD] [HH:MM] UTC*
```

## Section Guidelines

### State of the Union
- Always include all 4 product lines: SaaS, Books, Consulting, Website
- Use status emojis: 🟢 (healthy) / 🟡 (warning/issue) / 🔴 (critical/down)
- Keep to one line per product — detail goes in Urgent Items if needed

### Tasks Assigned Today
- Include ALL entries written to agent-communications.jsonl
- Include the system status entry for transparency
- Priority column uses High/Normal/Low (match JSONL payload)

### Executed Actions
- List what the CEO did directly (browser checks, JSONL cleanup, SOUL tracking)
- Keep to bullet points — concise
- Include validation results (e.g., "152/152 valid JSON entries")

### Urgent Items
- Prioritize: P0 (action required now) > P1 (should address this week) > P2 (monitor)
- Each item has: what's wrong, what's at stake, what Bob should do
- Flag recurring issues (e.g., "KDP pipeline regression — 5th time this week")

### Tomorrow's Focus
- Reference the daily rotation (Mon=SaaS, Tue=Books, etc.)
- List 2-3 specific priorities for next session

### Market Intelligence
- Include only on days when fresh market data was gathered (typically Mon, Thu, Sat)
- One-line insight + any competitor movement
- Reference the source file (e.g., "Source: market-intelligence-june20-2026.md")

## Pitfalls

- **Don't pad the briefing** — if everything is healthy, keep it short. "All systems operational" is a valid State of the Union.
- **Don't re-discover known issues** — reference prior briefings for recurring problems (e.g., "KDP regression — 5th cleanup this week, P0 until pipeline fixed")
- **Don't skip the JSONL validation** — always report valid/total count
- **Don't assign tasks without logging** — every task in the Tasks Assigned table must have a matching JSONL entry

## Trigger
- Every daily cron run (Mon-Sat) produces this briefing
- On Sunday, use `references/sunday-briefing-template.md` instead (no task assignments)
