---
name: Content Marketing
slug: content-marketing
version: 1.0.0
homepage: https://clawic.com/skills/content-marketing
description: Plan, create, and distribute content with editorial calendars, funnel strategy, and repurposing workflows.
metadata: {"clawdbot":{"emoji":"📝","requires":{"bins":[]},"os":["linux","darwin","win32"]}}
---


## Memory context (Hindsight)

Long-term memory context is now provided automatically by Hindsight (bank
`mifeco-default`) on every turn — the retired MemPalace manual query step no
longer applies. Do NOT attempt to import `~/.hermes/mempalace` (it was removed
2026-08-19).This retrieves previous decisions, domain-specific context, and lessons learned from the vector memory store.

## Setup

On first use, read `setup.md` for integration guidelines.

## When to Use

User needs help with content strategy, editorial planning, blog posts, social media content, or content distribution. Agent handles calendar management, topic ideation, funnel alignment, and repurposing workflows.

## Architecture

With user consent, data is stored locally in `~/content-marketing/`. See `memory-template.md` for structure.

```
~/content-marketing/
├── memory.md           # Strategy, voice, goals
├── calendar.md         # Editorial calendar
├── content-bank/       # Drafts and ideas
└── analytics/          # Performance notes
```

**First use:** Ask user for permission before creating this folder. The skill works without storage but cannot remember preferences between sessions.

## Quick Reference

| Topic | File |
|-------|------|
| Setup process | `setup.md` |
| Memory template | `memory-template.md` |
| Funnel strategy | `funnels.md` |
| Repurposing workflows | `repurposing.md` |

## Core Rules

### 1. Align Every Piece to Funnel Stage
Before creating content, identify:
- **TOFU** (Top of Funnel): Awareness, broad topics, SEO-focused
- **MOFU** (Middle): Consideration, comparisons, how-tos
- **BOFU** (Bottom): Decision, case studies, demos, pricing

Content without funnel alignment wastes effort.

### 2. One Core Idea, Multiple Formats
Every pillar content piece should generate:
- 1 long-form article or video
- 3-5 social posts
- 1 email newsletter section
- Quote graphics or carousels

Never create once and forget. Repurpose systematically.

### 3. Editorial Calendar is Sacred
Track in the editorial calendar:
- Publication dates
- Content type and funnel stage
- Status (idea / draft / review / published)
- Distribution channels

Review calendar weekly. Gaps in calendar = gaps in pipeline.

### 4. Voice Consistency
Document brand voice in memory:
- Tone (professional, casual, provocative)
- Words to use and avoid
- Example sentences that nail the voice

Every piece should sound like the same person wrote it.

### 5. Distribution > Creation
80% of effort should go to distribution:
- Cross-post to all relevant channels
- Repurpose for each platform's format
- Engage with comments and shares
- Update and republish evergreen content

Creating content nobody sees is content that doesn't exist.

### 6. Measure What Matters
Track per content type:
- Traffic and engagement
- Conversion to next funnel stage
- Time on page / completion rate
- Social shares and saves

Stop producing what doesn't perform.

### 7. Content Bank Never Empty
Always maintain 10+ ideas in content-bank/:
- Problems your audience has
- Questions they ask
- Trends in your space
- Competitor gaps

If you run out of ideas, you're not listening enough.

## Common Traps

- **No funnel alignment** → Content gets views but no conversions
- **Create and forget** → Single-use content wastes 80% of value
- **Inconsistent voice** → Brand feels fragmented
- **Publishing without distribution plan** → Content dies in silence
- **Chasing trends over evergreen** → Constant treadmill, no compounding
- **Ignoring analytics** → Repeating failures, missing wins

## Security & Privacy

**Data that stays local (with user consent):**
- Content strategy and voice preferences in `~/content-marketing/memory.md`
- Editorial calendar in `~/content-marketing/calendar.md`
- Content ideas in `~/content-marketing/content-bank/`

**This skill does NOT:**
- Send data to external services
- Access files outside `~/content-marketing/`
- Create files without explicit user permission
- Collect or transmit analytics

**User control:**
- Storage is optional — decline and the skill still works for ideation and advice
- Delete `~/content-marketing/` anytime to remove all stored data

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `seo` — Optimize content for search
- `writing` — Craft better copy
- `growth-hacker` — Distribution tactics
- `branding` — Maintain brand consistency

## Feedback

- If useful: `clawhub star content-marketing`
- Stay updated: `clawhub sync`

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
