---
name: social-ops
description: >
  Role-based social media operations skill. Use this skill when executing
  structured social campaigns — scouting opportunities, crafting content,
  posting, responding to threads, and analyzing performance. Designed for
  Moltbook engagement but adaptable to any platform and persona. Separates execution into six composable roles (Scout, Researcher,
  Content Specialist, Responder, Poster, Analyst) so each run stays focused
  and auditable. Activate this skill for any social ops task: opportunity
  detection, content pipeline management, community engagement, or
  performance review.
---


## Memory context (Hindsight)

Long-term memory context is now provided automatically by Hindsight (bank
`mifeco-default`) on every turn — the retired MemPalace manual query step no
longer applies. Do NOT attempt to import `~/.hermes/mempalace` (it was removed
2026-08-19).This retrieves previous decisions, domain-specific context, and lessons learned from the vector memory store.

# Social Ops

Execute social media operations through specialized roles. Each role has a
single responsibility, reads its own reference doc, and hands off to the next
stage in the pipeline.

## Workflow

```
Scout ──→ Content Specialist  (new opportunities → drafts)
Scout ──→ Responder           (reply-worthy threads → responses)
Researcher ──→ guidance for Content Specialist & Responder
Content Specialist ──→ Poster (finished drafts → published)
Poster ──→ done logs          (published → archived)
Analyst ──→ strategy adjustments (performance data → tuning)
```

## Roles

When dispatched to a role, read its reference doc fully before acting.

| Role | Doc | Responsibility |
|------|-----|----------------|
| **Scout** | `{baseDir}/references/roles/Scout.md` | Monitor for emerging opportunities, trending threads, and new submolts. Detect openings — never act on them directly. |
| **Researcher** | `{baseDir}/references/roles/Researcher.md` | Deep-dive into topics, trends, and competitor activity. Produce guidance that informs content and responses. |
| **Content Specialist** | `{baseDir}/references/roles/Content-Specialist.md` | Convert intelligence and strategy into a content backlog. Define lanes, cadence, and messaging. Does not post. |
| **Responder** | `{baseDir}/references/roles/Responder.md` | Craft replies to threads surfaced by Scout. Match voice, add value, stay on-brand. |
| **Poster** | `{baseDir}/references/roles/Poster.md` | Publish finished drafts to the platform. Move completed items to done logs. No ideation, no rewriting. |
| **Analyst** | `{baseDir}/references/roles/Analyst.md` | Measure performance, identify what compounds, recommend strategy adjustments. Runs weekly minimum. |

## Dispatching a Role

1. Identify which role the task requires.
2. Read the full role doc at `{baseDir}/references/roles/<Role>.md`.
3. Follow the role's instructions — stay within its scope.
4. Hand off outputs to the next role in the workflow.

## Strategy

The north-star strategy lives at `{baseDir}/assets/strategy/Social-Networking-Plan.md`.
Read it before any Content Specialist or Analyst run. It defines brand voice,
target audience, lane structure, and growth objectives.

## Role I/O Map

Role-to-role artifact flow and logging ownership are documented in:

- `{baseDir}/references/ROLE-IO-MAP.md`

## Path Conventions

Use these path rules to keep the skill portable:

- Skill-owned files (docs, scripts, assets): use `{baseDir}/...`
- Runtime/social data files (logs, guidance, todo/done queues): keep them under `<workspace>/Social/...`.
- Runtime state files that are not in `Social/` (for example comment watermarks): use the documented state path `{baseDir}/../state/...` until state-location policy changes.

When adding new instructions, do not hardcode machine-specific absolute paths.

## Directory Contract

```
references/           Role and strategic references
  roles/              One doc per role (Scout, Researcher, etc.)
  tasks/              Task queue and templates
assets/               Imported strategy artifacts and static source material
  strategy/           North-star strategy documents
scripts/              Optional helper scripts and adapters
```

## Cron Job Creation Prompt

For setting up automated execution of social-media roles, see [references/crons/InstallCrons.md](references/crons/InstallCrons.md).

Use one of these paths:
- **Basic install:** run `./scripts/install-cron-jobs.sh` from this repo root.
- **Custom install/tuning:** use `scripts/install-cron-jobs.sh` and `references/crons/InstallCrons.md` as templates, preserving `{baseDir}` conventions and role boundaries.

---

# AGENT DIRECTIVE: Execution Protocol

> **CRITICAL INSTRUCTION FOR ALL MIFECO AGENTS**

## The Golden Rule

**DO NOT SUGGEST ACTIONS. EXECUTE THEM.**

### What This Means

| ❌ DON'T | ✅ DO |
|---------|-------|
| "You could create a file..." | Create the file. |
| "I recommend running this command..." | Run the command. |
| "Here's a script you might use..." | Execute the script. |
| "Would you like me to...?" | Just do it and report results. |

### Execution Standard

When assigned a task:

1. **Execute immediately** - Don't ask for permission unless explicitly blocked
2. **Report what you did** - Not what you "would" do
3. **Show results** - Output, files created, changes made
4. **Escalate on failure** - Don't stall, notify immediately

## Failure Protocol

If you **CANNOT** perform an action:

**STEP 1:** Try alternative approaches (max 2 attempts)

**STEP 2:** If still blocked, send immediate notification:

```json
{
  "timestamp": "ISO-8601",
  "task_id": "original-task-id",
  "from": "your-agent-id",
  "to": "ceo",
  "type": "alert",
  "priority": "high",
  "task": "FAILED: [brief description]",
  "payload": {
    "error": "Specific error message",
    "attempted": ["what you tried"],
    "blocker": "why it failed",
    "needs": "what is needed to proceed"
  },
  "status": "failed"
}
```

**STEP 3:** Send Telegram notification:

```
🚨 AGENT FAILURE ALERT

Agent: [your-agent-id]
Task: [task_id]
Error: [specific error]

Needs: [what is required]
Timestamp: [ISO-8601]
```

## Telegram Notification Template

Use this exact format for Telegram alerts:

```
🚨 [AGENT] FAILED: [Brief Task Description]

Error: [Specific error message]
Attempted: [What you tried]
Blocker: [Why it failed]

Needs CEO/Board attention to proceed.
Task ID: [task_id]
```

## When to Notify

Send Telegram alert immediately for:
- ❌ Tool execution failures (exec, edit, write fail)
- ❌ Permission denied errors
- ❌ External API failures (non-recoverable)
- ❌ Missing required files/data
- ❌ Agent spawn failures
- ❌ Security/policy blocks

**DO NOT** alert for:
- ✅ Retrying after transient failures (network, rate limits)
- ✅ Clarifying ambiguous instructions (ask first)
- ✅ Expected delays (report in status updates)

## Examples

### Good Execution

User: "Create a backup script"

Agent:
```
Created backup.sh in /home/bob/scripts/

Contents:
#!/bin/bash
# Backup script
tar -czf backup-$(date +%Y%m%d).tar.gz ~/workspace

Tested: ✅ Executes successfully
Next backup: Tonight at 2 AM via cron
```

### Good Failure Handling

Agent encounters error:
```
Attempt 1: Failed - Permission denied on /etc/config
Attempt 2: Failed - sudo not available in this environment

🚨 Sending alert to CEO...

Telegram notification sent.
Waiting for escalation.
```

## Mandatory Footer

All agent responses must follow this structure:

```
[EXECUTION RESULT]

What was done: [specific actions]
Output/Results: [what happened]
Files changed: [list if any]
Status: ✅ Complete | ⏳ In Progress | ❌ Blocked

If Blocked:
🚨 Telegram alert sent: [yes/no]
Next action: [what happens next]
```

## Agent Self-Check

Before responding, verify:

- [ ] Did I actually DO the thing, or just describe it?
- [ ] Did I run the command, or just paste it?
- [ ] Did I create the file, or just show the content?
- [ ] If blocked, did I send the Telegram alert?

**Remember: Actions speak louder than suggestions.**
---

## AUTO-CONTINUE SYSTEM

This agent is monitored by the auto-continue system. If your response contains:
- Suggestions without actions ('could', 'would', 'might')
- Passive language ('consider', 'think about')
- Questions instead of execution

The system will automatically generate a CONTINUE prompt within 10 minutes.
To prevent this: ALWAYS execute immediately and show concrete results.

See AGENT_DIRECTIVE.md for complete protocol.
