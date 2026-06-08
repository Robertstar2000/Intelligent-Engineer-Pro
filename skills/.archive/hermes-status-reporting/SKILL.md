---
name: hermes-status-reporting
description: A systematic approach for generating status reports on Hermes Agent health, cron jobs, and project status for daily briefings.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [hermes, status, reporting, cron, monitoring, briefing]
---

# Hermes Status Reporting Skill

A systematic approach for generating status reports on Hermes Agent health, cron jobs, and project status for daily briefings.

## Overview
This skill provides a standardized method to check Hermes Agent system health, scheduled jobs, and project-specific status (like book projects) to compile concise briefings for stakeholders.

## When to Use
- Generating daily or periodic status briefings for team members
- Monitoring Hermes Agent health and cron job reliability
- Checking on long-running project status (e.g., book publishing)
- Preparing reports for platform delivery (Telegram, email, etc.)

## Workflow Steps

### 1. Check Hermes Agent Status
Run `hermes status --all` to capture:
- Environment details (Python version, project path)
- Model and provider configuration
- API key status for configured providers
- Auth provider login status
- Terminal backend information
- Messaging platform connection status
- Gateway service status
- Active sessions count

### 2. Review Cron Job Health
Run `hermes cron list` to verify:
- All scheduled jobs are active (check for disabled jobs)
- Last run status (look for "ok" or error indicators)
- Next run times to ensure schedules are correct
- Job delivery platforms (Telegram, local, origin, etc.)

### 3. Run System Health Check
Execute `hermes doctor` to identify:
- Missing dependencies or optional tools
- Configuration issues
- Security advisories
- Provider connectivity problems
- Directory structure integrity

### 4. Check Project-Specific Status
For book projects or other long-running efforts:
- Search for source files in expected directories (e.g., `~/books/`, `~/projects/`)
- Check platform-specific data stores (e.g., Telegram temp directory for PDF artifacts)
- Look for published artifacts, review files, or promotion materials
- Verify file naming consistency and completeness

### 5. Compile the Briefing
Format findings as a clean bullet-point report:
- **Hermes Agent Status**: Key health indicators
- **Cron Job Health**: Active jobs, recent outputs, any failures
- **Project Status**: Current phase (writing, published, promotion), key artifacts
- **System Alerts**: Critical issues needing attention
- **Insight/Reminder**: One actionable item or observation for the day

## Tools Utilized
- `terminal`: To run `hermes status`, `hermes cron list`, `hermes doctor`
- `search_files`: To locate project source files and artifacts
- `todo`: (Optional) To track briefing preparation steps if needed

## Support Files
- `references/telegram-book-artifacts.md`: Guidance on checking Telegram for published book artifacts

## Quality Standards
- Keep briefings concise for platform delivery (Telegram-friendly length)
- Focus on actionable information and health indicators
- Highlight issues that require intervention
- Include one practical insight or reminder
- Avoid excessive technical detail unless specifically requested

## Example Output Structure
- **Hermes Agent Status**: [Summary of model, provider, gateway]
- **Cron Job Health**: [Number of active jobs, any failed jobs]
- **Project Status**: [Published/promotion phase evidence]
- **System Alerts**: [Critical missing dependencies or config issues]
- **Insight/Reminder**: [One specific recommendation]

## Customization Points
- Adjust checks based on specific projects being monitored
- Add platform-specific delivery checks (e.g., Telegram bot status)
- Include cost/usage analytics if relevant (`hermes insights`)
- Tailor insight frequency to project cadence (daily, weekly)

## Troubleshooting
- **Incomplete status output**: Ensure `hermes` command is in PATH and configured
- **Missing cron jobs**: Verify scheduler is running (`hermes cron status`)
- **Health check failures**: Address missing dependencies or API key gaps
- **Project artifacts not found**: Verify search paths and platform data locations