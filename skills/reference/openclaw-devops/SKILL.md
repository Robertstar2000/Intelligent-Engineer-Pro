---
name: DevOps
description: Automate deployments, manage infrastructure, and build reliable CI/CD pipelines.
metadata: {"clawdbot":{"emoji":"🔧","os":["linux","darwin","win32"]}}
---


## 🔍 MemPalace Query (MANDATORY FIRST STEP)
Before proceeding, query MemPalace for existing context:
```python
import sys, os; sys.path.insert(0, os.path.expanduser('~/.hermes/mempalace'))
import embed; embed.init_embedding(os.path.expanduser('~/.hermes/mempalace'))
results = embed.search_embeddings("DevOps deployment infrastructure CI/CD pipeline", k=5)
```
This retrieves previous decisions, domain-specific context, and lessons learned from the vector memory store.

# DevOps Rules

## CI/CD Pipelines
- Fail fast: run linting and unit tests before expensive integration tests — saves time and compute
- Cache dependencies between runs — `npm install` on every build wastes minutes
- Pin action versions with SHA, not tags — `actions/checkout@v3` can change, SHA is immutable
- Secrets in environment variables, never in code or logs — mask them in CI output
- Parallel jobs for independent steps — test, lint, and build can run simultaneously

## Deployment Strategies
- Blue-green: run new version alongside old, switch traffic atomically — instant rollback by switching back
- Canary: route percentage of traffic to new version — catch issues before full rollout
- Rolling: update instances incrementally — balance between speed and risk
- Always have rollback plan before deploying — know exactly how to revert
- Deploy the same artifact to all environments — build once, promote through stages

## Infrastructure as Code
- Version control all infrastructure — terraform, ansible, cloudformation in git
- Never apply changes without plan/diff review — `terraform plan` before `apply`
- State files contain secrets — store remotely with encryption, never in git
- Modules for reusable components — don't copy-paste infrastructure definitions
- Separate environments with workspaces or directories — dev changes shouldn't affect prod

## Containers
- One process per container — containers are not VMs
- Health checks are mandatory — orchestrators need them for routing and restarts
- Don't run as root — use non-root USER in Dockerfile
- Immutable images: config via environment, not baked in — same image in all environments
- Tag images with git SHA, not just `latest` — know exactly what's deployed

## Secrets Management
- Never store secrets in environment files committed to git — use vault, sealed secrets, or CI secret storage
- Rotate secrets regularly — automation makes rotation painless
- Different secrets per environment — dev leak shouldn't compromise prod
- Audit secret access — know who accessed what and when
- Secrets in memory, not disk when possible — temp files persist longer than expected

## Monitoring & Alerting
- Four golden signals: latency, traffic, errors, saturation — start here
- Alert on symptoms, not causes — "users seeing errors" not "CPU high"
- Every alert must be actionable — if you can't do anything, it's noise
- Dashboard per service with key metrics — one glance shows health
- Structured logs (JSON) for machine parsing — grep works, but queries are better

## Reliability
- Define SLOs before building alerting — what does "healthy" mean for this service?
- Error budgets: some failures are acceptable — 99.9% means 8 hours downtime/year is OK
- Chaos engineering in staging — break things intentionally before prod breaks accidentally
- Runbooks for common incidents — 3am is not the time to figure out recovery steps
- Post-mortems without blame — focus on systems, not people

## Common Mistakes
- SSH into prod to fix things — all changes through automation, or you'll forget what you did
- No staging environment — "works on my machine" doesn't mean works in prod
- Ignoring flaky tests — they erode trust in CI, either fix or delete
- Manual steps in deployment — if it's not automated, it'll be done wrong eventually
- Monitoring only happy paths — check error rates and edge cases too

## Networking
- Internal services don't need public IPs — use private subnets, expose only load balancers
- TLS everywhere, including internal traffic — zero trust, even behind firewall
- DNS for service discovery — hardcoded IPs break when things move
- Load balancer health checks separate from app health — LB needs fast response, app health can be thorough
- Firewall default deny — explicitly allow what's needed, block everything else

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
