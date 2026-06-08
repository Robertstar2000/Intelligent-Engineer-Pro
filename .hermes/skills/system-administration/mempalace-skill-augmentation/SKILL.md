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
