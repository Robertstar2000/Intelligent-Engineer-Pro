---
name: linkedin
description: LinkedIn automation via browser relay or cookies for messaging, profile viewing, and network actions.
homepage: https://linkedin.com
metadata: {"clawdbot":{"emoji":"💼"}}
---


## Memory context (Hindsight)

Long-term memory context is now provided automatically by Hindsight (bank
`mifeco-default`) on every turn — the retired MemPalace manual query step no
longer applies. Do NOT attempt to import `~/.hermes/mempalace` (it was removed
2026-08-19).This retrieves previous decisions, domain-specific context, and lessons learned from the vector memory store.

# LinkedIn

Use browser automation to interact with LinkedIn - check messages, view profiles, search, and send connection requests.

## Connection Methods

### Option 1: Chrome Extension Relay (Recommended)
1. Open LinkedIn in Chrome and log in
2. Click the Clawdbot Browser Relay toolbar icon to attach the tab
3. Use `browser` tool with `profile="chrome"`

### Option 2: Isolated Browser
1. Use `browser` tool with `profile="clawd"` 
2. Navigate to linkedin.com
3. Log in manually (one-time setup)
4. Session persists for future use

## Common Operations

### Check Connection Status
```
browser action=snapshot profile=chrome targetUrl="https://www.linkedin.com/feed/"
```

### View Notifications/Messages
```
browser action=navigate profile=chrome targetUrl="https://www.linkedin.com/messaging/"
browser action=snapshot profile=chrome
```

### Search People
```
browser action=navigate profile=chrome targetUrl="https://www.linkedin.com/search/results/people/?keywords=QUERY"
browser action=snapshot profile=chrome
```

### View Profile
```
browser action=navigate profile=chrome targetUrl="https://www.linkedin.com/in/USERNAME/"
browser action=snapshot profile=chrome
```

### Send Message (confirm with user first!)
1. Navigate to messaging or profile
2. Use `browser action=act` with click/type actions
3. Always confirm message content before sending

## Safety Rules
- **Never send messages without explicit user approval**
- **Never accept/send connection requests without confirmation**
- **Avoid rapid automated actions** - LinkedIn is aggressive about detecting automation
- Rate limit: ~30 actions per hour max recommended

## Session Cookie Method (Advanced)
If browser relay isn't available, extract the `li_at` cookie from browser:
1. Open LinkedIn in browser, log in
2. DevTools → Application → Cookies → linkedin.com
3. Copy `li_at` value
4. Store securely for API requests

## Troubleshooting
- If logged out: Re-authenticate in browser
- If rate limited: Wait 24 hours, reduce action frequency
- If CAPTCHA: Complete manually in browser, then resume

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
