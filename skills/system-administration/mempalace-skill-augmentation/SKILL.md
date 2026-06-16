---
name: mempalace-skill-augmentation
description: "Use when updating, creating, or managing Hermes skills at scale. Covers the pattern for batch-updating skills with MemPalace query preambles, storing domain knowledge in MemPalace, and maintaining the skill library architecture. Triggered by: skill updates, skill library maintenance, MemPalace knowledge storage, batch operations on skills."
version: 1.0.0
author: OWL (ZOO)
license: MIT
metadata:
  hermes:
    tags: [mempalace, skills, batch-update, knowledge-management, skill-library]
    related_skills: [mempalace-complete, hermes-agent-skill-authoring]
---

# MemPalace-Augmented Skill Management

## Overview

This skill governs how to maintain the Hermes skill library with MemPalace integration. The key principle: **every skill should advise querying MemPalace first** to retrieve domain-specific context from previous sessions before proceeding.

## Skill Library Architecture

### Class-Level Umbrella Structure
Skills are organized as **class-level umbrellas**, not flat one-session-one-skill entries:
- Each skill covers a **class of work** (e.g., `book-publishing` covers all KDP publishing, not just one book)
- Rich SKILL.md with comprehensive workflows, pitfalls, and examples
- `references/` directory for session-specific detail, error transcripts, and domain knowledge banks
- `templates/` directory for boilerplate configs and scaffolding
- `scripts/` directory for re-runnable verification and generation scripts

### MemPalace Query Preamble (MANDATORY)
Every skill's SKILL.md must include this preamble immediately after the frontmatter:

```markdown
## 🔍 MemPalace Query (MANDATORY FIRST STEP)
Before proceeding, query MemPalace for existing context:
\```python
import sys, os; sys.path.insert(0, os.path.expanduser('~/.hermes/mempalace'))
import embed; embed.init_embedding(os.path.expanduser('~/.hermes/mempalace'))
results = embed.search_embeddings("[domain-specific terms]", k=5)
\```
This retrieves previous decisions, domain-specific context, and lessons learned from the vector memory store.
```

## Batch Skill Update Pattern

When updating many skills at once (e.g., adding MemPalace preambles):

### 1. Scope Narrowing
- **User preference**: When user says "just the skills associated with X", narrow scope to relevant domains only
- Don't blindly update all 220+ skills — focus on the class of work at hand
- MIFECO-relevant categories: publishing, writing, consulting, SaaS, devops, business, manuscript-preparation, reference agents

### 2. Batch Processing via delegate_task
- Split into batches of 8-10 skills per subagent
- Each subagent uses `skill_manage(action='patch')` to insert the preamble
- Pattern: insert between frontmatter closing `---` and first `# heading`

### 3. Direct File I/O for Unresolvable Skills
Some skills can't be resolved by `skill_manage()` (different registry). For these:
```python
import os, re
# Find actual path
path = '/home/bob/.hermes/skills/{category}/{skill_name}/SKILL.md'
with open(path) as f:
    content = f.read()
# Insert preamble after frontmatter
match = re.search(r'^---\s*\n.*?\n---\n\n(#+|##+)', content, re.MULTILINE | re.DOTALL)
if match:
    new_content = content[:pos] + preamble + '\n' + content[pos:]
    with open(path, 'w') as f:
        f.write(new_content)
```

### 4. Recursive glob for Complete Coverage
```python
import glob
all_skills = glob.glob('/home/bob/.hermes/skills/**/SKILL.md', recursive=True)
```

## MemPalace Knowledge Storage Pattern

When storing domain knowledge in MemPalace:

### 1. Capture
```python
import sys, os; sys.path.insert(0, os.path.expanduser('~/.hermes/mempalace'))
import capture, tag, embed
from datetime import datetime, timezone
storage = os.path.expanduser('~/.hermes/mempalace')
capture.init_capture(storage); tag.init_tagging(storage); embed.init_embedding(storage)

event = {
    'type': 'memory_dump',
    'content': comprehensive_text,
    'context': 'comma, separated, tags',
    'timestamp': datetime.now(timezone.utc).isoformat(),
    'source': 'hermes-memory',
    'category': 'descriptive-category-name'
}
event_id = capture.capture_event(event)
```

### Weekly Skill Registry Sync Pattern
This session's weekly cron job uses a streamlined version — sync registry only (no embeddings):

```python
import sys, os, yaml
sys.path.insert(0, os.path.expanduser('~/.hermes/mempalace'))
sys.path.insert(0, os.path.expanduser('~/.hermes/hermes-agent'))
import capture
from agent.skill_utils import get_all_skills_dirs, iter_skill_index_files, parse_frontmatter

capture.init_capture(os.path.expanduser('~/.hermes/mempalace'))

# 1. Load existing skills from MemPalace
events = capture.load_recent_events(days=365)
existing_skills = {}
for event in events:
    data = event.get('data', {})
    if data.get('type') == 'skill_registry':
        existing_skills[data['skill_name']] = data

# 2. Scan current SKILL.md files
skills_dirs = get_all_skills_dirs()
all_current_skills = []
for skills_dir in skills_dirs:
    if not skills_dir.exists():
        continue
    for skill_file in iter_skill_index_files(skills_dir, 'SKILL.md'):
        try:
            content = skill_file.read_text(encoding='utf-8')
            fm, body = parse_frontmatter(content)
            name = fm.get('name', '') or skill_file.parent.name
            desc = fm.get('description', '')
            try:
                rel = skill_file.relative_to(skills_dir)
                category = rel.parts[0] if len(rel.parts) > 1 else 'general'
            except:
                category = 'general'
            all_current_skills.append({'name': name, 'description': desc[:500], 'category': category})
        except Exception as e:
            print(f'Error processing {skill_file}: {e}')

# 3. Load disabled list from config
with open(os.path.expanduser('~/.hermes/config.yaml')) as f:
    cfg = yaml.safe_load(f)
disabled = set(cfg.get('skills', {}).get('disabled', []))

# 4. Find new skills (in filesystem but not MemPalace)
new_skills = [s for s in all_current_skills if s['name'] not in existing_skills]

# 5. Find removed skills (in MemPalace but not filesystem)
current_names = {s['name'] for s in all_current_skills}
removed = [name for name in existing_skills if name not in current_names]

# 6. Add new skills
for skill in new_skills:
    status = 'disabled' if skill['name'] in disabled else 'enabled'
    event_data = {
        'type': 'skill_registry',
        'skill_name': skill['name'],
        'skill_category': skill['category'],
        'skill_description': skill['description'],
        'status': status,
    }
    capture.capture_event(event_data)

# 7. Report summary
print(f'Total skills: {len(all_current_skills)}')
print(f'New added: {len(new_skills)}')
print(f'Removed: {len(removed)}')
print(f'Enabled: {sum(1 for s in all_current_skills if s[\"name\"] not in disabled)}')
print(f'Disabled: {sum(1 for s in all_current_skills if s[\"name\"] in disabled)}')
```

**Note:** Embeddings require `sentence-transformers` + `faiss-cpu` in the Hermes venv. Install with:
```bash
/home/bob/.hermes/hermes-agent/venv/bin/pip3 install sentence-transformers faiss-cpu
```
Then run the embedding pass separately using `embed.add_embedding(event_id, text)` + `embed._persist()`.

### 2. Tag and Embed
```python
tags = tag.extract_context_tags(content)
if tags:
    tag.save_context_tags(event_id, tags)
embed.add_embedding(event_id, content)
```

### 3. Verify Retrieval
```python
results = embed.search_embeddings("relevant query", k=3)
for memory_id, score in results:
    print(f"Score: {score:.4f} | ID: {memory_id}")
```

### 4. Direct Module Import (for cron/non-interactive)
```python
import sys, os; sys.path.insert(0, os.path.expanduser('~/.hermes/mempalace'))
import capture, tag, embed  # NOT from mempalace import ...
capture.init_capture(storage)
tag.init_tagging(storage)
embed.init_embedding(storage)
```

## Skill Update Triggers

Update a skill when ANY of these occur:
1. **User corrected style/tone/format** → Update the relevant skill's SKILL.md body (not just memory)
2. **User corrected workflow/approach** → Add pitfall or explicit step
3. **New technique/fix/workaround emerged** → Capture in references/ or as pitfall
4. **Skill was wrong/missing/outdated** → Patch NOW
5. **Two skills overlap** → Note for curator consolidation

## Skill Token Management

### Measuring the Skills Block

To check how many tokens the skills system prompt consumes:

```python
import sys
sys.path.insert(0, os.path.expanduser('~/.hermes/hermes-agent'))
from agent.prompt_builder import build_skills_system_prompt

result = build_skills_system_prompt()
chars = len(result)
tokens_est = chars // 4
import re
entries = re.findall(r'^    - (\S+):', result, re.MULTILINE)
print(f'Skills block: {chars:,} chars / ~{tokens_est:,} tokens')
print(f'Skill entries: {len(entries)}')
print(f'Lines: {len(result.split(chr(10)))}')
```

### Disabling Skills to Reduce Tokens

Skills can be excluded from the system prompt via `skills.disabled` in `~/.hermes/config.yaml`:

```yaml
skills:
  disabled:
    - skill-name-1
    - skill-name-2
```

**⚠️ CRITICAL: Do NOT use `hermes config set` for the disabled list.** The command mangles YAML — it splits JSON-style strings by commas, producing 1,500+ garbage entries. Always edit the file directly with Python:

```python
import yaml
from pathlib import Path

config_path = Path.home() / '.hermes' / 'config.yaml'
with open(config_path) as f:
    cfg = yaml.safe_load(f)

cfg['skills']['disabled'] = [
    'skill-name-1',
    'skill-name-2',
    # ... use proper YAML list, not JSON string
]

with open(config_path, 'w') as f:
    yaml.dump(cfg, f, default_flow_style=False, allow_unicode=True)
print(f"Disabled {len(cfg['skills']['disabled'])} skills")
```

After editing, delete the cached snapshot so the change takes effect on next gateway start:

```python
snapshot = Path.home() / '.hermes' / '.skills_prompt_snapshot.json'
if snapshot.exists():
    snapshot.unlink()
```

Inform the user that a gateway restart is needed: `hermes gateway restart` (must be run from outside the gateway process).

### What to Disable

Good candidates for disabling (large categories, not needed in every session):
- ML/AI ops skills (torch, transformers, training, inference — 25+ skills)
- Gaming, media generation, social media, email (20+ skills)
- Book publishing, heavy dev workflows, reference profiles (30+ skills)
- Red teaming, OS-specific desktop tools (10+ skills)

Always keep enabled: `hermes-agent`, `systematic-debugging`, `requesting-code-review`, `security-auditor`, and MIFECO-specific skills.

Typical savings: ~36% reduction (~2,070 tokens on a 5,704-token skills block with ~90 skills disabled).

## GitHub Backup Integration

The Hermes skill library, config, memories, and MemPalace data are backed up to a private GitHub repository (`FL-Hermes`). See `github-repo-management/references/hermes-backup-pattern.md` for the full backup procedure.

Key points:
- `.env` and `auth.json` are NEVER committed
- `config.yaml` is redacted (all key/token/password values → `***`)
- `.env.example` is generated as a template
- Backup runs weekly via cron job

## What NOT to Capture
- Environment-dependent failures (missing binaries, fresh-install errors)
- Negative claims about tools ("X tool is broken")
- Session-specific transient errors that resolved
- One-off task narratives

## Verification Checklist
- [ ] All target skills have MemPalace preamble
- [ ] Preamble includes domain-specific search terms
- [ ] MemPalace knowledge is searchable (test with `embed.search_embeddings`)
- [ ] FAISS index count increased after storage
- [ ] Raw files created in `~/.hermes/mempalace/raw/`

## See Also
- `references/skill-registry.md` — Full pattern for storing skills as MemPalace events, searching via FAISS, and managing disabled/enabled status
- `references/weekly-skill-registry-sync.md` — Cron job pattern for weekly registry synchronization with filesystem
