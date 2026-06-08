---
name: skill-finder
description: "Find and enable/disable Hermes skills. Searches MemPalace for skills matching a task, shows which are enabled or disabled, and can re-enable disabled skills. Use when the agent needs a skill that might be disabled, when the user asks to find a skill for a task, or when the user wants to enable/disable skills."
version: 1.0.0
author: OWL for Bob Mills / MIFECO
license: MIT
metadata:
  hermes:
    tags: [skills, skill-management, mempalace, search, enable, disable]
    related_skills: [hermes-agent-skill-authoring, mempalace-vector-integration]
---

# Skill Finder

## Overview

Manages the Hermes skill registry stored in MemPalace. Skills are categorized and indexed via FAISS embeddings for fast semantic search. Disabled skills are kept in MemPalace but excluded from the system prompt. This skill can find skills by task description, show their status (enabled/disabled), and re-enable skills when needed.

## When to Use

- The agent encounters a task and needs to find a relevant skill that might be disabled
- The user asks "find a skill for X" or "is there a skill that does Y?"
- The user wants to enable or disable a specific skill
- The agent realizes it loaded a disabled skill via `skill_view()` and needs to re-enable it
- Weekly cron job reviews all skills and adds newly discovered ones to MemPalace

## How the Skill Registry Works

- **220 skills** are registered in MemPalace (raw events with type `skill_registry`)
- Each skill has: name, category, description, status (enabled/disabled)
- Disabled skills are listed in `~/.hermes/config.yaml` under `skills.disabled`
- The system prompt only shows enabled skills (currently ~127 enabled, ~90 disabled)
- Disabling saves ~36% system prompt tokens (~2,070 tokens)

## Search Flow

### Step 1: Search MemPalace

```python
import sys, os, json
sys.path.insert(0, os.path.expanduser('~/.hermes/mempalace'))
import embed

embed.init_embedding(os.path.expanduser('~/.hermes/mempalace'))
results = embed.search_embeddings("<task description>", k=10)
```

Results are `(memory_id, score)` tuples sorted by relevance.

### Step 2: Check Skill Status

```python
import yaml

with open(os.path.expanduser('~/.hermes/config.yaml')) as f:
    cfg = yaml.safe_load(f)
disabled = set(cfg.get('skills', {}).get('disabled', []))

# For each search result, check if the skill name is in the disabled list
# Load the raw event to get the skill name
import capture
raw_events = capture.load_recent_events(days=365)
for mem_id, score in results:
    for event in raw_events:
        if event.get('id') == mem_id:
            data = event.get('data', {})
            name = data.get('skill_name', '')
            category = data.get('skill_category', '')
            status = data.get('status', 'enabled')
            print(f'{name} [{category}] - score: {score:.3f} - {status}')
            break
```

### Step 3: Load or Re-enable the Skill

**If the skill is enabled:** Just use `skill_view(name)` as normal.

**If the skill is disabled and the user needs it:**

1. The agent can still call `skill_view(name)` to load the skill's content — disabling only removes it from the system prompt index
2. To re-enable, remove from disabled list:
   ```python
   import yaml
   
   with open(os.path.expanduser('~/.hermes/config.yaml')) as f:
       cfg = yaml.safe_load(f)
   
   disabled = cfg.get('skills', {}).get('disabled', [])
   if '<skill_name>' in disabled:
       disabled.remove('<skill_name>')
       cfg['skills']['disabled'] = disabled
   
   with open(os.path.expanduser('~/.hermes/config.yaml'), 'w') as f:
       yaml.dump(cfg, f, default_flow_style=False, allow_unicode=True)
   
   # Clear cached snapshot to pick up the change
   import pathlib
   snapshot = pathlib.Path(os.path.expanduser('~/.hermes')) / '.skills_prompt_snapshot.json'
   if snapshot.exists():
       snapshot.unlink()
   ```
3. Inform the user that the skill was re-enabled and a gateway restart is needed for it to appear in the system prompt
4. After re-enable, update MemPalace status to 'enabled'

## Update MemPalace After Status Change

```python
import sys, os, json
sys.path.insert(0, os.path.expanduser('~/.hermes/mempalace'))
import capture, embed

capture.init_capture(os.path.expanduser('~/.hermes/mempalace'))

# Capture a re-enable event
capture.capture_event({
    'type': 'skill_status_change',
    'skill_name': '<name>',
    'old_status': 'disabled',
    'new_status': 'enabled',
})

# Update the embedding text for this skill
embed.init_embedding(os.path.expanduser('~/.hermes/mempalace'))
# Find and update the skill's event
embed._persist()
```

## View Full Registry

To see all skills currently in MemPalace:

```python
import sys, os, json
sys.path.insert(0, os.path.expanduser('~/.hermes/mempalace'))
import capture, yaml

events = capture.load_recent_events(days=365)
skills = []
for event in events:
    data = event.get('data', {})
    if data.get('type') == 'skill_registry':
        skills.append(data)

with open(os.path.expanduser('~/.hermes/config.yaml')) as f:
    cfg = yaml.safe_load(f)
disabled = set(cfg.get('skills', {}).get('disabled', []))

print(f'Total skills in MemPalace: {len(skills)}')
print(f'Enabled: {len([s for s in skills if s["name"] not in disabled])}')
print(f'Disabled: {len([s for s in skills if s["name"] in disabled])}')
print()
# Group by category
from collections import defaultdict
by_cat = defaultdict(list)
for s in skills:
    by_cat[s['skill_category']].append(s['name'])
for cat, names in sorted(by_cat.items()):
    print(f'  {cat}: {len(names)} skills')
```

## Categories

Current skill categories in the registry:
- `autonomous-ai-agents` — subagent delegation, encoding tools
- `book-publishing` — KDP pipeline skills
- `browser-harness` — browser automation
- `business` — MIFECO business operations, marketing, sales, Stripe
- `business-improvements` — improvement proposals
- `creative` — writing, design, diagrams, manuscripts
- `data-science` — Jupyter, data analysis
- `devops` — deployment, security, infrastructure
- `github` — PR workflow, issues, code review
- `manuscript-preparation` — book manuscript workflows
- `mcp` — MCP server/client tools
- `media` — GIF, image, YouTube, Spotify
- `mempalace` — vector memory skills
- `mlops` — image generation
- `note-taking` — Obsidian
- `productivity` — Airtable, Google Workspace, Notion, PowerPoint
- `research` — paper writing
- `social-media` — LinkedIn writing
- `software-development` — debugging, testing, planning, review
- `system-administration` — cron, backup, monitoring, operations
- `telegram-gateway-troubleshooting` — Telegram gateway
- `virtual-consulting` — MIFECO consulting
- `yuanbao` — Yuanbao groups

## Related Skills

- `hermes-agent-skill-authoring` — how to create/edit skills
- `mempalace-vector-integration` — embedding system for skill registry
- Cron ticker optimization — see `references/cron-ticker-optimization.md` for auto_nap() pattern and token reduction via skills.disabled

## Common Pitfalls

1. **Disabled skill can still be loaded.** `skill_view(name)` works regardless of disabled status. Disabling only affects the system prompt index.
2. **Config edit requires YAML-safe format.** Don't use JSON strings in `hermes config set` for the disabled list — it mangles the YAML. Use Python to edit the file directly.
3. **Gateway restart needed.** After re-enabling a skill, the user must restart the gateway for it to appear in the system prompt.
4. **Snapshot cache.** If token counts don't change after editing config, delete `~/.hermes/.skills_prompt_snapshot.json`.
5. **Don't disable core skills.** Skills like `hermes-agent`, `systematic-debugging`, `requesting-code-review`, and `security-auditor` should stay enabled.

## See Also

- `references/auto-nap-pattern.md` — auto_nap() adaptive cron ticker pattern (60s normal / 30min idle / reset on input)

- [ ] MemPalace search returned relevant results (score > 0.2)
- [ ] Checked disabled list in config.yaml
- [ ] If re-enabling: config.yaml updated, snapshot cleared, user notified
- [ ] MemPalace updated with status change event
