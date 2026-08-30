---
name: Docker (Essentials + Advanced)
slug: docker
version: 1.0.3
homepage: https://clawic.com/skills/docker
description: Build, secure, and deploy Docker containers with image optimization, networking, and production-ready patterns.
changelog: Added essential commands reference and production patterns
metadata: {"clawdbot":{"emoji":"🐳","requires":{"bins":["docker"]},"os":["linux","darwin","win32"]}}
---


## Memory context (Hindsight)

Long-term memory context is now provided automatically by Hindsight (bank
`mifeco-default`) on every turn — the retired MemPalace manual query step no
longer applies. Do NOT attempt to import `~/.hermes/mempalace` (it was removed
2026-08-19).This retrieves previous decisions, domain-specific context, and lessons learned from the vector memory store.

## Setup

On first use, read `setup.md` for user preference guidelines.

## When to Use

User needs Docker expertise. Agent handles containers, images, Compose, networking, volumes, and production deployment.

## Architecture

Memory in `~/docker/`. See `memory-template.md` for structure.

```
~/docker/
└── memory.md    # Preferences and context
```

## Quick Reference

| Topic | File |
|-------|------|
| Essential commands | `commands.md` |
| Dockerfile patterns | `images.md` |
| Compose orchestration | `compose.md` |
| Networking & volumes | `infrastructure.md` |
| Security hardening | `security.md` |
| Setup | `setup.md` |
| Memory | `memory-template.md` |

## Core Rules

### 1. Pin Image Versions
- `python:3.11.5-slim` not `python:latest`
- Today's latest differs from tomorrow's — breaks immutable builds

### 2. Combine RUN Commands
- `apt-get update && apt-get install -y pkg` in ONE layer
- Separate layers = stale package cache weeks later

### 3. Non-Root by Default
- Add `USER nonroot` in Dockerfile
- Running as root fails security scans and platform policies

### 4. Set Resource Limits
- `-m 512m` on every container
- OOM killer strikes without warning otherwise

### 5. Configure Log Rotation
- Default json-file driver has no size limit
- One chatty container fills disk and crashes host

## Image Traps

- Multi-stage builds: forgotten `--from=builder` copies from wrong stage silently
- COPY before RUN invalidates cache on every file change — copy requirements first, install, then copy code
- `ADD` extracts archives automatically — use `COPY` unless you need extraction
- Build args visible in image history — never use for secrets

## Runtime Traps

- `localhost` inside container is container's localhost — bind to `0.0.0.0`
- Port already in use: previous container still stopping — wait or force remove
- Exit code 137 = OOM killed, 139 = segfault — check with `docker inspect --format='{{.State.ExitCode}}'`
- No shell in distroless images — `docker cp` files out or use debug sidecar

## Networking Traps

- Container DNS only works on custom networks — default bridge can't resolve names
- Published ports bind to `0.0.0.0` — use `127.0.0.1:5432:5432` for local-only
- Zombie connections from killed containers — set health checks and restart policies

## Compose Traps

- `depends_on` waits for container start, not service ready — use `condition: service_healthy`
- `.env` file in wrong directory silently ignored — must be next to docker-compose.yml
- Volume mounts overwrite container files — empty host dir = empty container dir
- YAML anchors don't work across files — use multiple compose files instead

## Volume Traps

- Anonymous volumes accumulate silently — use named volumes
- Bind mounts have permission issues — container user must match host user
- `docker system prune` doesn't remove named volumes — add `--volumes` flag
- Stopped container data persists until container removed

## Resource Leaks

- Dangling images grow unbounded — `docker image prune` regularly
- Build cache grows forever — `docker builder prune` reclaims space
- Stopped containers consume disk — `docker container prune` or `--rm` on run
- Networks pile up from compose projects — `docker network prune`

## Secrets and Security

- ENV and COPY bake secrets into layer history permanently — use secrets mount or runtime env
- `--privileged` disables all security — almost never needed, find specific capability instead
- Images from unknown registries may be malicious — verify sources
- Build args visible in image history — don't use for secrets

## Debugging

- Exit code 137 = OOM killed, 139 = segfault — check `docker inspect --format='{{.State.ExitCode}}'`
- Container won't start: check logs even for failed containers — `docker logs <container>`
- No shell in distroless images — `docker cp` files out or use debug sidecar
- Inspect filesystem of dead container — `docker cp deadcontainer:/path ./local`

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `devops` — deployment pipelines
- `linux` — host system management
- `server` — server administration

## Feedback

- If useful: `clawhub star docker`
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
