# Sunday CEO Strategic Briefing Template

> Used by ceo-agent-orchestrator for Sunday cron runs. The CEO does NOT assign tasks on Sunday — instead delivers a strategic briefing to Bob covering the week ahead.

## Format

```
# 📋 MIFECO CEO STRATEGIC BRIEFING — Sunday, [DATE]

---

## 1. STATE OF THE UNION
[Table: one row per product line with Status emoji + one-line detail]

## 2. TASKS ASSIGNED TODAY
[Table: Task ID | To | Priority | Description — Sunday typically has 0-2 tasks]

## 3. EXECUTED ACTIONS
[Bullet list of what CEO did inline — checks, scans, cleanups]

## 4. URGENT ITEMS — BOB ACTION NEEDED
[Prioritized P0-P3 list with specific actions Bob can take]

## 5. TOMORROW'S FOCUS — [Day of week], [DATE]
[Table: Priority | Task | Owner — based on daily rotation]

## 6. PIPELINE HEALTH DASHBOARD
[Table: 10 pipelines with Status emoji + one-line note]
```

## Notes
- Sunday = **briefing-only day** per rotation (no task assignments to agents)
- Market research IS run on Sunday to prepare for the week ahead
- Always include KDP regression check (daily pattern as of June 2026)
- Always include tomorrow's focus (Monday = SaaS Growth & Engineering)
- Pipeline health table covers all 10 pipelines defined in ceo-agent-orchestrator SKILL.md
