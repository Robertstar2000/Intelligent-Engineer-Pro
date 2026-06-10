# HEARTBEAT.md — CEO Agent Daily Routine

## Every Heartbeat (or daily cron at 8:00 AM):

1. **Check agent-communications.jsonl** — read last 50 lines
   - Any failed tasks? → Diagnose and retry or report to Bob
   - Any completed tasks? → Update mental model of agent health

2. **Check Kanban board** — `hermes kanban` or dashboard
   - Stuck tasks (>4hrs)? → Reclaim and reassign
   - Failed tasks? → Check failure count, auto-retry or escalate to Bob

3. **Count active agents** — agents with completed task in last 7 days
   - If any of the 9 agents show no activity → dispatch activation task
   - If agent skill is disabled → report to Bob for manual fix

4. **Assign today's focus tasks per rotation:**
   - Mon: SaaS + Security | Tue: Books + Marketing | Wed: Consulting + Sales
   - Thu: SaaS UX + Research | Fri: Strategy | Sat: Deep Work | Sun: Briefing only

5. **Report to Bob** ONLY if:
   - Urgent: security breach, client escalation, deadline <24hrs
   - Critical: agent failure that can't be auto-recovered
   - Summary: daily activity report (normal priority)

6. **If nothing needs attention** → stay quiet, NO_REPLY
