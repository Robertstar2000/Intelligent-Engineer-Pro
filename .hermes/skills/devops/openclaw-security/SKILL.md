---
name: security
description: "Scan AgentSkills (OpenClaw/Codex/Cursor-style skill folders) for prompt injection, data exfiltration risks, and suspicious code patterns using Cisco AI Defense Skill Scanner. Use when reviewing third-party skills, before installing/enabling new skills/plugins, or when auditing your own skills for security."
---


## 🔍 MemPalace Query (MANDATORY FIRST STEP)
Before proceeding, query MemPalace for existing context:
```python
import sys, os; sys.path.insert(0, os.path.expanduser('~/.hermes/mempalace'))
import embed; embed.init_embedding(os.path.expanduser('~/.hermes/mempalace'))
results = embed.search_embeddings("MIFECO business process", k=5)
```
This retrieves previous decisions, domain-specific context, and lessons learned from the vector memory store.

# Security - Skill Scanner (Cisco AI Defense)

Use this skill to **security-scan skill folders** (like `workspace/skills/*`) before you trust or install them.

What it does (at a high level)
- Static scanning (YAML + YARA-like patterns)
- Optional deeper analyzers (behavioral/dataflow, LLM judge, meta-analyzer)
- CI-friendly outputs (e.g., SARIF)

Repo (reference)
- https://github.com/cisco-ai-defense/skill-scanner

## Quick start (most common)
Scan one skill directory:

```bash
python3 -m pip install --user cisco-ai-skill-scanner
skill-scanner scan /path/to/skill
```

Scan all skills in your workspace:

```bash
python3 -m pip install --user cisco-ai-skill-scanner
skill-scanner scan-all /home/bob/.openclaw/workspace/skills --recursive
```

Fail a build (or your check) if findings exist:

```bash
skill-scanner scan-all ./skills --recursive --fail-on-findings
```

## When to use which mode
- **Default (static only)**: fast, good baseline, low friction.
- **Behavioral** (`--use-behavioral`): when scanning Python-heavy skills.
- **LLM + meta** (`--use-llm --enable-meta`): when you can provide an API key and want fewer false positives.

## Suggested workflow for OpenClaw
1) Before adding a new external/community skill: run a scan on the unpacked skill folder.
2) Review any findings, especially:
   - network calls / webhooks
   - credential access / environment variable grabs
   - filesystem reads outside the workspace
   - "execute arbitrary code" patterns
3) Only then install/enable the skill.

## Scripts in this skill
- `scripts/scan_workspace_skills.sh` - convenience wrapper to scan the workspace skills folder.

## Notes
- This skill does **not** automatically install the scanner or modify your system.
- If you want, ask: "Install skill-scanner and run it on my skills folder."

## Inter-Agent Communication Protocol

## Skill Usage Rule (CRITICAL)

Each agent is limited to **4 skills maximum per session**:
- 1 primary skill assigned to this agent (the one in this file's name)
- Up to 3 additional skills for the current task

**Rule:** If a task requires skills beyond your 4-skill limit, do NOT try to add more skills. Instead, spawn a subagent or delegate to another agent who has the required skill for that specific subtask.

**Examples:**
- If `coder` needs `designer` skills for a UI task, spawn a `designer` subagent
- If `writer` needs `saas-operations` knowledge, spawn a `saas-operations` subagent
- If you need `web-search-priority` or `weather` (always available), those are excluded from the 4-skill count

**What to do when you hit the 4-skill limit:**
1. Complete the work you can with your current 4 skills
2. Spawn a subagent with the additional skill needed to handle that subtask
3. Integrate the subagent's output into your final response

This keeps context windows manageable and ensures the right agent handles each specialized task.
### Accepting Direction from AI Bob and CEO
The Security agent receives direction from AI Bob, CEO, and other agents via the inter-agent communication system:

**Communication Channel:** `memory/agent-communications.jsonl`

**On Every Heartbeat, the Security Agent MUST:**
1. Check `memory/agent-communications.jsonl` for pending tasks
2. Look for entries where:
   - `"to"` matches "security" OR "any" OR "all"
   - `"status"` is "pending" or "assigned"
3. Claim the task by updating status to "active" with `claimed_by: "security"`
4. Execute the security task according to instructions
5. Report progress and completion back to the communication file

**Completion Reporting Format:**
```json
{
  "timestamp": "2026-02-27T08:30:00Z",
  "task_id": "security-001-audit",
  "from": "security",
  "to": "ceo",
  "type": "response",
  "task": "Security audit complete",
  "payload": {
    "result_summary": "Completed nightly codebase review, no critical issues found",
    "artifacts": [
      {"type": "file", "path": "security/audit-2026-02-27.md", "description": "Security audit report"}
    ],
    "time_taken_minutes": 45
  },
  "status": "completed"
}
```

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

## Telegram Topic Routing

Route operational communication to the **Ai Topics** Telegram forum supergroup.

**Forum chat ID:** `-1003883088282`

**Topic mapping:**
- `AiBob / CEO` — topic ID `11`
  - Use for: human ↔ AI Bob coordination, CEO updates, board-level summaries, cross-product decisions
- `Books product line` — topic ID `10`
  - Use for: writer, designer, presentations, publishing, manuscript and cover progress
- `Virtual consulting product line` — topic ID `12`
  - Use for: consultant delivery, client work, briefings, research for consulting engagements
- `SaaS / AaaS product line` — topic ID `13`
  - Use for: engineering, coder, security, SaaS ops, customer support, sales, brand advocacy, product operations

**Routing rule:**
When you proactively send Telegram updates with the `message` tool, send them to the relevant forum topic instead of the user's DM unless the user explicitly asks for DM-only delivery.

**Default per-agent routing:**
- `main` → topic `11`
- `ceo` → topic `11`
- `writer` → topic `10`
- `designer` → topic `10`
- `presentations` → topic `10`
- `consultant` → topic `12`
- `researcher` → topic `12` for consulting research, otherwise topic `11` for board/strategy research
- `engineer` → topic `13`
- `coder` → topic `13`
- `saas-operations` → topic `13`
- `security` → topic `13`
- `customer-support` → topic `13`
- `sales` → topic `13`
- `brand-advocacy` → topic `13`

**Implementation detail:**
For Telegram sends, use:
- `channel: "telegram"`
- `target: "-1003883088282"`
- `threadId: "<topic-id>"`

If an update spans multiple product lines, send the executive summary to topic `11` and the detailed operational update to the relevant product-line topic.

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
