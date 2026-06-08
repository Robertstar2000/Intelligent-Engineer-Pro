---
name: daily-briefing-generation
description: A skill for generating comprehensive daily briefings covering agent status, health alerts, news, events, and sports with intelligent fallback handling when automated data fetching is limited due to tool configuration.
category: productivity
---


## 🔍 MemPalace Query (MANDATORY FIRST STEP)
Before proceeding, query MemPalace for existing context:
```python
import sys, os; sys.path.insert(0, os.path.expanduser('~/.hermes/mempalace'))
import embed; embed.init_embedding(os.path.expanduser('~/.hermes/mempalace'))
results = embed.search_embeddings("MIFECO business process", k=5)
```
This retrieves previous decisions, domain-specific context, and lessons learned from the vector memory store.

# Daily Briefing Generation with Fallback Handling

A skill for generating comprehensive daily briefings covering agent status, health alerts, news, events, sports, project progress, and system updates with intelligent fallback handling when automated data fetching is limited due to tool configuration or missing API keys.

## When to Use
- Creating regular daily briefings for personal or team consumption
- When you want automated data fetching but need graceful degradation
- For briefings that include multiple sections: system status, news, events, sports, project progress
- When deploying in environments where API keys or tools may not be fully configured
- For operational briefings covering system health, cron jobs, backups, and task tracking
- For agent-specific status reporting (OpenClaw, Codex, etc.) and project tracking
- For comprehensive operational briefings including manuscript progress, business operations, and system maintenance alerts

## Workflow Steps

### 1. Pre-flight Configuration Check
Before attempting data fetching:
- Check if required tools are enabled (`hermes tools list`)
- Run `hermes doctor` to identify configuration issues
- Note: Web search tool requires proper configuration via `hermes setup` for full functionality

### 2. Agent Status Section
- Check for specific agent processes using process listing commands (excluding grep itself)
- Check for OpenClaw agent status and pending tasks by examining AGENTS.md and agent-communications.jsonl
- Look for agent-related files in the Hermes directory for historical context
- Report: active processes detected or historical data presence

### 3. Project Progress Section
- Check manuscript status for all active book projects
- Verify cover completion, EPUB readiness, and publishing checklists
- Track specific manuscript revisions and changes applied
- Note business operations status and SaaS application development

### 3. Health & Alerts Section
- Run `hermes doctor` and parse output
- Extract:
  - ✅ Health status items (working components)
  - ⚠️ Alerts and action items (configuration or dependency notes)
- Format as:
  - HEALTH STATUS: List key working components
  - ALERTS & ACTION ITEMS: List items requiring attention or configuration
- Common notes to watch for:
  - Config version outdated (suggest running `hermes doctor --fix`)
  - Auth provider status (suggest running `hermes auth` if needed)
  - Optional tool dependencies (suggest configuration via `hermes setup`)
  - Skills hub rate limits (suggest configuring GITHUB_TOKEN for better rates)
  - Cron job status and scheduling
  - Backup status and last run times
  - Memory system status
  - Missing dependencies (ripgrep, docker, etc.)
  - Vulnerability alerts (npm audit findings)
  - Update availability notifications

### 4. News Briefing Section (with Fallback)
**Attempt Automated Fetch (when web tool is enabled and configured):**
- Use `hermes chat -q "[location] news today" --toolsets web --quiet`
- Parse response for headline, summary, source
- Target: 2 local items per region, 5 science/tech, 3 world

**Fallback when Automated Fetch is Limited:**
- Provide clear notification: "Automated news fetch limited - suggest checking preferred news sources"
- Suggest checking:
  * Local news: Check preferred local outlets
  * Science/Tech: Science outlets (ScienceDaily, MIT Tech Review, Reuters Science, Nature, Science Magazine)
  * World News: International outlets (BBC World News, Reuters World, Associated Press)

### 5. Local Events Section (with Fallback)
**Attempt Automated Fetch:**
- Query for events in target areas for the specified time window
- Parse for: event name, day, start/end time, venue, city

**Fallback when Automated Fetch is Limited:**
- Suggest checking:
  * Local visitor bureau websites for both areas
  * Event aggregation platforms (Eventbrite, Facebook Events)
  * Specific venue calendars (e.g., Musical Fountain, Farmers Market, Al Lang Stadium, Pier 60, Dalí Museum)

### 6. Book Publishing Progress Section
- Check status of all active book projects (KDP titles)
- For each book, note: manuscript status, cover status, EPUB readiness, pending work
- Track completion status across all titles

### 7. Manuscript Report Section
- Check latest version of specified manuscripts
- Review PDF review copies when available
- Document specific changes applied (chapter modifications, character updates, etc.)
- Note EPUB rebuild status

### 8. Business Operations Status Section
- Check business dashboard systems (MIFECO, SaaS apps)
- Report on active development and deployment status
- Note any business-critical system status

### 9. Sports Watchlist Section (with Fallback)
**Attempt Automated Fetch:**
- Query for recent games, scores, or highlights for specified teams
- Parse for: team, event, date, time, opponent, score/highlight

**Fallback when Automated Fetch is Limited:**
- Provide manual checking guidance:
  * Team official websites and sports news outlets
  * League official sites (e.g., USL Championship for Rowdies)
  * Sports apps for live scores (ESPN, theScore, league official apps)

### 10. Upcoming Tasks & Reminders Section
- List scheduled cron jobs with next run times
- Include any known deadlines or scheduled maintenance
- Note regular recurring tasks

### 11. System Alerts & Maintenance Needed Section
- Compile action items from health check
- Include security vulnerabilities, config updates needed
- Note missing dependencies and recommended fixes
- Highlight update availability and backward compatibility notes

### 7. Briefing Assembly
- Format with clear section headers and emojis for visual scanning
- Use consistent bullet point formatting
- Include timestamp in header: "📰 DAILY BRIEFING FOR [NAME] - [Day, Month Date, Year]"
- Add actionable tip at end: "💡 To enhance automation: Configure web search via hermes setup and run hermes doctor --fix"
- Keep sections concise but informative for quick consumption

## Quality Standards
- Always indicate when automated fetching is limited and provide constructive alternatives
- Provide actionable suggestions, not just notifications of limitations
- Keep briefing scannable with clear section separation
- Update health alerts based on actual `hermes doctor` output
- Verify agent status checks are specific and accurate
- Include timestamp for freshness indication

## Customization Points
- Adjust news item counts per section based on preference
- Modify suggested sources based on user's preferred outlets
- Change sports teams watched
- Adjust event lookup window (e.g., 24h vs 48h)
- Add or remove sections (e.g., weather, personal reminders)

## Troubleshooting
- **Limited automated fetching**: Check if web tool is enabled and properly configured via `hermes tools` and `hermes setup`
- **Health check issues**: Run `hermes doctor` for detailed diagnostics
- **Process visibility variations**: Process checks may show different levels of detail based on execution context
- **Response parsing variations**: Implement flexible parsing when structured output is unavailable

## Example Usage
This skill is designed to be invoked programmatically or as part of a cron job for automated briefing generation. The approach handles both fully automated scenarios (when configured) and semi-automated scenarios (with guidance fallbacks).

## Related Skills
- daily-session-insights: For extracting insights from Hermes agent sessions
- hermes-agent: For general Hermes configuration and troubleshooting
- novel-writing-workflow: For structured long-form writing approaches