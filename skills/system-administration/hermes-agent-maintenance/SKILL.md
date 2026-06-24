---
name: hermes-agent-maintenance
description: Maintenance and troubleshooting for Hermes Agent system including memory management, gateway services, cron jobs, and general system health
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
---

# Hermes Agent Maintenance

A systematic approach to maintaining and troubleshooting Hermes Agent system components including memory, gateway services, cron jobs, and general system health.

## When to Use
- Memory limit warnings or tool failures due to memory constraints
- Gateway service issues (duplicate services, startup failures, restart problems)
- Cron job failures or monitoring
- General system health checks and optimization
- Preparing for extended agent operation

## Maintenance Procedures

### 1. Memory Management
When encountering memory limit errors like "Memory at X/Y chars. Adding this entry would exceed the limit":

```bash
# Check current memory usage
hermes memory status

# View memory entries to identify what can be cleared
hermes memory list

# Remove outdated or less important entries
hermes memory remove --target memory --old_text "specific_outdated_entry"

# Or replace entries with more concise versions
hermes memory replace --target memory --old_text "verbose_entry" --content "concise_version"

# Increase memory limit if needed (in config.yaml)
# memory:
#   max_chars: 4000  # increased from default 2200
```

### 2. Gateway Service Troubleshooting

#### Duplicate Services Issue
If you see both user and system gateway services installed:

```bash
# Check status of both services
systemctl --user status hermes-gateway
systemctl status hermes-gateway  # requires sudo

# Keep only one service (typically user service is preferred)
# Remove system service:
sudo hermes gateway uninstall --system

# Or remove user service if system service is preferred:
hermes gateway uninstall

# Verify only one service remains active
hermes gateway status
```

#### Gateway Restart Without Sudo
When gateway restart requires sudo but password is unavailable:

```bash
# Find main PID and send USR1 signal (no root needed)
mainpid=$(systemctl show hermes-gateway -p MainPID --value)
kill -USR1 "$mainpid"

# Verify restart with
systemctl status hermes-gateway
```

#### Gateway Dies on Logout/Close
- **SSH logout**: Enable linger: `sudo loginctl enable-linger $USER`
- **WSL2 close**: Ensure `systemd=true` in `/etc/wsl.conf`

### 3. Cron Job Maintenance
When cron jobs fail or need attention:

```bash
# List all cron jobs with status
hermes cron list

# Check logs for specific failed job
hermes cron log <job_id>

# Manually run a job to test
hermes cron run <job_id>

# Pause/resume problematic jobs
hermes cron pause <job_id>
hermes cron resume <job_id>

# Edit job schedule or configuration
hermes cron edit <job_id>
```

### 4. Common Tool Failures and Fixes

#### Browser Click Errors (Unknown Ref)
When getting "Unknown ref: e5" errors:
1. Always call `browser_snapshot` after navigation and before clicking
2. Wait for dynamic content to load with `browser_wait_for` or `browser_sleep`
3. Verify element is visible and interactable

#### Execute Code Sandbox Issues (Windows)
For WinError 10106 on Windows:
1. Ensure `SYSTEMROOT` is not stripped from child environment
2. The fix is already applied in Hermes via `_WINDOWS_ESSENTIAL_ENV_VARS` allowlist
3. If still occurring, verify environment inside execute_code block

#### Skill Management Errors
When skill_manage fails with "Could not find a match" or "Found 2 matches":
1. Provide more context in old_string to ensure uniqueness
2. Use `replace_all=True` if intentional multiple replacements
3. Verify the skill file content matches expectations

### 5. System Health Checks
Regular health monitoring:

```bash
# Run doctor check
hermes doctor [--fix]

# Check overall status
hermes status [--all]

# Review gateway logs for errors
grep -i "failed to send\|error" ~/.hermes/logs/gateway.log | tail -20

# Check memory usage trends
hermes memory stats

# Verify configuration is valid
hermes config check
```

### 6. Proactive Maintenance Schedule
Consider setting up these regular checks:
- Weekly: Memory cleanup and optimization
- Monthly: Gateway service verification
- Quarterly: Full system health check with `hermes doctor --fix`
- As needed: After system updates or configuration changes
- After any memory limit warnings: Run memory cleanup immediately

## Toolset Dependency Map
For a quick-reference of what each toolset needs (packages, API keys, system binaries), see:
[references/toolset-dependency-map.md](references/toolset-dependency-map.md)

## USB Data Migration
When relocating large directories to external storage, see [references/usb-data-migration.md](references/usb-data-migration.md) for the rsync + symlink pattern.

## References
- [Memory Management Docs](https://hermes-agent.nousresearch.com/docs/user-guide/features/memory)
- [Gateway Troubleshooting](https://hermes-agent.nousresearch.com/docs/user-guide/messaging/#troubleshooting)
- [Cron Job Documentation](https://hermes-agent.nousresearch.com/docs/user-guide/features/cron)
- [Configuration Guide](https://hermes-agent.nousresearch.com/docs/user-guide/configuration)