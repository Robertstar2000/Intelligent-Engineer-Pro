# Weekly Skill Registry Sync Pattern

This reference documents the pattern used by the weekly cron job to keep the MemPalace skill registry synchronized with the filesystem.

## Purpose

- Detect new skills added to the filesystem
- Detect skills removed from the filesystem
- Keep enabled/disabled status in sync with `~/.hermes/config.yaml`
- Generate a summary report (only if changes detected)

## Cron Job Implementation

The cron job runs this exact flow each week:

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

# 7. Fix status mismatches (MemPalace vs config.yaml)
# Get latest status for each skill
latest_skills = {}
for event in events:
    data = event.get('data', {})
    if data.get('type') == 'skill_registry':
        name = data['skill_name']
        if name not in latest_skills:
            latest_skills[name] = data

for name, data in latest_skills.items():
    config_status = 'disabled' if name in disabled else 'enabled'
    mempalace_status = data.get('status', 'enabled')
    if config_status != mempalace_status:
        # Update to match config
        event_data = {
            'type': 'skill_registry',
            'skill_name': name,
            'skill_category': data.get('skill_category', 'general'),
            'skill_description': data.get('skill_description', ''),
            'status': config_status,
        }
        capture.capture_event(event_data)

# 8. Report summary (only if changes)
if new_skills or removed:
    print(f'Total skills: {len(all_current_skills)}')
    print(f'New added: {len(new_skills)}')
    print(f'Removed: {len(removed)}')
    for s in new_skills:
        print(f'  + {s["name"]} [{s["category"]}]')
    for r in removed:
        print(f'  - {r}')
    print(f'Enabled: {sum(1 for s in all_current_skills if s["name"] not in disabled)}')
    print(f'Disabled: {sum(1 for s in all_current_skills if s["name"] in disabled)}')
else:
    # Stay silent - no changes to report
    pass
```

## Handling Duplicate Skill Names

Some skills exist in multiple categories with the same name (e.g., `openclaw-social-scheduler` in both `reference/` and `social-media/`). The registry stores each with a unique key:

- Primary: `<name>` (first occurrence)
- Secondary: `<name>-<category>` (e.g., `openclaw-social-scheduler-social-media`)

## Embedding Generation (Optional)

To enable semantic search over skills, install dependencies and add embeddings:

```bash
/home/bob/.hermes/hermes-agent/venv/bin/pip3 install sentence-transformers faiss-cpu
```

Then run embedding pass:

```python
import sys, os
sys.path.insert(0, os.path.expanduser('~/.hermes/mempalace'))
import embed, capture

embed.init_embedding(os.path.expanduser('~/.hermes/mempalace'))
capture.init_capture(os.path.expanduser('~/.hermes/mempalace'))

events = capture.load_recent_events(days=365)
for event in events:
    data = event.get('data', {})
    if data.get('type') == 'skill_registry':
        memory_id = event['id']
        text = f"{data['skill_name']} {data['skill_category']} {data['skill_description']}"
        embed.add_embedding(memory_id, text)
embed._persist()
```

## Key Learnings from This Session

1. **Capture system must be initialized** before calling `capture_event()` — call `capture.init_capture(storage_path)` first
2. **Duplicate skill names** require special handling — the registry stores both with category suffix
3. **Status mismatches** between MemPalace and config.yaml are common — always reconcile during sync
4. **Sentence-transformers/FAISS not pre-installed** in Hermes venv — embeddings require separate install
5. **Silent mode** when no changes — don't notify user if registry is already current

## Files Modified This Session

- `mempalace-skill-augmentation/SKILL.md` — Added this weekly sync pattern to the main skill
- `mempalace-skill-augmentation/references/weekly-skill-registry-sync.md` — This reference file