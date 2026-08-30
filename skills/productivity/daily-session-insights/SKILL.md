---
name: daily-session-insights
description: Extract meaningful insights from Hermes agent sessions for daily briefings and reports
category: productivity
---


## Memory context (Hindsight)

Long-term memory context is now provided automatically by Hindsight (bank
`mifeco-default`) on every turn — the retired MemPalace manual query step no
longer applies. Do NOT attempt to import `~/.hermes/mempalace` (it was removed
2026-08-19).This retrieves previous decisions, domain-specific context, and lessons learned from the vector memory store.

# Daily Session Insights Skill

A reusable approach for extracting meaningful insights from Hermes agent sessions for daily briefings or reports.

## When to Use
- Creating daily/weekly summaries of agent activity
- Preparing reports on what was accomplished in previous sessions
- Tracking progress on ongoing projects
- Identifying patterns in user interactions

## Approach

### 1. Check Session Availability
First verify that sessions exist and are accessible:
```bash
hermes sessions list
```

### 2. Get Yesterday's Date
Calculate yesterday's date in YYYY-MM-DD format for filtering:
```bash
date -d "yesterday" '+%Y-%m-%d'
```

### 3. Search Sessions by Date
Use the sessions browse functionality to find sessions from a specific date:
```bash
hermes sessions browse
```
Then manually filter, or use:
```bash
ls ~/.hermes/sessions/ | grep "^$(date -d "yesterday" '+%Y%m%d')"
```

### 4. Extract Meaningful Content
Session files are stored as JSONL in ~/.hermes/sessions/. To extract insights:

#### Method A: Using hermes command line (recommended)
```bash
# Get summary of recent sessions
hermes sessions list
# For specific date, use session_search with the date
hermes sessions search "2026-04-15"  # Note: use quote marks around date
```

#### Method B: Direct file parsing (for custom processing)
Each line in a session file is a JSON object with:
- `role`: system/user/assistant/tool
- `content`: the message content
- `tools`: tool calls made (if any)
- `session_meta`: metadata at start (first line)

Extract user queries and assistant responses:
```python
# Example Python approach:
import json
with open(session_file) as f:
    for line in f:
        try:
            obj = json.loads(line)
            if obj.get('role') in ['user', 'assistant']:
                content = obj.get('content', '')
                # Process content for insights
        except:
            pass
```

#### Method C: Using the session_search tool (most effective)
The session_search tool provides LLM-generated summaries of matching sessions:
```bash
# This gives you a ready-made summary
hermes session_search --query "2026-04-15" --limit 1
```

### 5. Generate Insights Summary
Look for:
- Project names mentioned (e.g., "Second Generation")
- Technical topics discussed (e.g., "Hermes dashboard", "gateway")
- Tasks completed or attempted
- Errors or issues encountered
- Decisions made

### 6. Combine with System Health
For a complete briefing, also gather:
- **Gateway status**: `hermes gateway status`
- **Cron jobs**: `hermes cron list`
- **Memory status**: `hermes memory status`
- **System health**: `hermes doctor`
- **OpenClaw processes**: `ps aux | grep -i openclaw | grep -v grep`
- **Book progress**: Count chapter files in book directories
- **Weather**: `curl -s wttr.in?format=3`
- **Calendar**: `calendar`

## Example Output Format
```
=== DAILY BRIEFING FOR [USER] ===
Generated: [timestamp]

1. [PROJECT/PROJECT_NAME] STATUS
   [Brief status update]

2. HERMES SYSTEM HEALTH
   Doctor: [key health indicators]
   Gateway: [status]
   Cron jobs: [count/status]
   Memory: [status]

3. [PROJECT] PROGRESS
   [Specific metrics: chapters written, features implemented, etc.]

4. YESTERDAY'S INSIGHTS
   [Summary of what was worked on yesterday]

5. WEATHER & CALENDAR
   Weather: [condition]
   Calendar: [events or "No events"]
```

## Tips
- Focus on user queries and assistant responses for insights
- Skip tool output and system metadata unless relevant
- Look for repeated themes or project names
- Keep insights concise but informative
- If no sessions found for yesterday, check the last 2-3 days
- Session files are named: YYYYMMDD_HHMMSS_[random].jsonl

## Dependencies
- Access to ~/.hermes/sessions/ directory
- Basic text processing tools (grep, date, etc.)
- Optional: JSON parsing capability for deeper analysis

## Related Skills
- hermes-agent: Core Hermes agent usage and configuration
- novel-writing-workflow: For fiction writing project tracking