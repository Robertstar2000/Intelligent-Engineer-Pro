---
name: hermes-agent-daily-briefing
description: "Generate a daily briefing for Hermes agent covering system status, cron jobs, book projects, and insights."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [hermes, daily-briefing, system-status, cron-jobs, book-project]
    homepage: https://github.com/NousResearch/hermes-agent
    related_skills: [daily-briefing-workflow, hermes-agent]
---

## Hermes Agent Daily Briefing Workflow

This skill provides a systematic approach for generating a daily briefing for the Hermes agent, covering system status, cron job health, book project status, system issues, and an insight.

### When to Use
- Generating a daily status report for Hermes agent.
- Checking on the health of the agent and its scheduled jobs.
- Monitoring book projects (if any) for publishing status.
- Identifying and alerting on system issues.

### Workflow Steps

#### 1. Check Hermes Agent Status
- Run `hermes doctor` to get overall system status and identify any issues.
- Run `hermes config` to see the current model and configuration.
- Run `hermes tools list` to check enabled/disabled tools.
- Run `hermes skills list` to see installed skills.

#### 2. Check Cron Job Health
- Run `hermes cron status` to see if the gateway and cron service are running.
- Run `hermes cron list --all` to get details on all scheduled jobs, including any errors.

#### 3. Check Book Project Status
- For each book project in `/home/bob/books/`, check if the `book_source` directory exists and has chapter files.
- If `book_source` is empty, check the `output` directory for compiled manuscripts (indicating the book is published).
- For "Tomorrow Remembered", note that it is published and in the promotion phase.

#### 4. Check for System Issues or Alerts
- Review the errors log: `/home/bob/.hermes/logs/errors.log` for recent errors.
- Review the gateway log: `/home/bob/.hermes/logs/gateway.log` for gateway issues.
- Look for patterns like model not found, connection failures, etc.

#### 5. Formulate an Insight or Reminder
- Based on the findings, provide one actionable insight or reminder for the day.
- Example: Run `hermes doctor --fix` to resolve configuration issues, or check on a specific cron job that has been failing.

### Tools Utilized
- `hermes doctor`: System health check.
- `hermes config`: View current configuration.
- `hermes tools list`: Check tool availability.
- `hermes skills list`: List installed skills.
- `hermes cron status` and `hermes cron list --all`: Cron job health.
- `ls`: Directory listing for book projects.
- `grep`: Log file inspection.

### Template
- Use the reference template: `references/daily-briefing-template.md` to structure your briefing.
- Fill in each section with the results from the corresponding checks.
- Keep the language concise and suitable for Telegram delivery.

### Quality Standards
- The briefing should be concise and formatted as bullet points for easy reading on Telegram.
- Focus on actionable items and avoid unnecessary detail.
- Highlight any issues that require immediate attention.
- End with a clear insight or reminder.

### Example Output
- See the daily briefing generated in the cron job session.