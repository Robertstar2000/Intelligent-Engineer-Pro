# Weekly Skill Registry Sync Pattern

This reference documents the pattern used by the weekly cron job to keep the MemPalace skill registry synchronized with the filesystem.

## Purpose

- Detect new skills added to the filesystem
- Detect skills removed from the filesystem
- Keep enabled/disabled status in sync with `~/.hermes/config.yaml`
- Generate a summary report (only if changes detected)

## Cron Job Implementation

The cron job runs this exact flow each week:

**⚠️ CRITICAL: `capture.load_recent_events()` does NOT exist.** Events are stored as individual files in `~/.hermes/mempalace/raw/`. Read them by scanning the raw directory directly. Also note that events can be in **two formats**: old dated JSONL files nest data under a `data` key, while new events from `capture_event()` store data at the top level. Both must be handled.

```python
import sys, os, yaml, json
sys.path.insert(0, os.path.expanduser('~/.hermes/mempalace'))
import capture

capture.init_capture(os.path.expanduser('~/.hermes/mempalace'))

# 1. Load existing skills from MemPalace by scanning raw directory
raw_dir = os.path.expanduser('~/.hermes/mempalace/raw')
existing_skills = {}
for fname in sorted(os.listdir(raw_dir)):
    if fname == 'archive':
        continue
    fpath = os.path.join(raw_dir, fname)
    try:
        with open(fpath) as f:
            content = f.read().strip()
            if not content:
                continue
            # Try single JSON first, then JSONL
            try:
                evt = json.loads(content)
                items = [evt]
            except:
                items = [json.loads(line) for line in content.split('\n') if line.strip()]
            for evt in items:
                # Handle both formats: nested under 'data' key (old) or top-level (new)
                data = evt.get('data', {})
                if not isinstance(data, dict) or data.get('type') != 'skill_registry':
                    if evt.get('type') == 'skill_registry':
                        data = evt
                if isinstance(data, dict) and data.get('type') == 'skill_registry':
                    existing_skills[data['skill_name']] = data
    except:
        pass

# 2. Scan current SKILL.md files via os.walk (no agent.skill_utils dependency)
skill_roots = [
    os.path.expanduser('~/.hermes/skills'),
    os.path.expanduser('~/.hermes/hermes-agent/skills'),
]
all_current_skills = []
for root in skill_roots:
    if not os.path.exists(root):
        continue
    for dirpath, dirnames, filenames in os.walk(root):
        if 'SKILL.md' not in filenames:
            continue
        fpath = os.path.join(dirpath, 'SKILL.md')
        try:
            content = open(fpath).read()
            if content.startswith('---'):
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    fm = yaml.safe_load(parts[1])
                    name = fm.get('name', '') or os.path.basename(dirpath)
                    desc = fm.get('description', '')
                    rel = os.path.relpath(dirpath, root)
                    parts2 = rel.split(os.sep)
                    category = parts2[0] if len(parts2) > 1 else 'general'
                    # Skip archived skills
                    if category.startswith('.archive'):
                        continue
                    # User skills override agent skills
                    if name not in {s['name'] for s in all_current_skills} or root == skill_roots[0]:
                        all_current_skills.append({'name': name, 'description': str(desc)[:500], 'category': category})
        except:
            pass

# 3. Load disabled list from config
with open(os.path.expanduser('~/.hermes/config.yaml')) as f:
    cfg = yaml.safe_load(f)
disabled = set(cfg.get('skills', {}).get('disabled', []))

# 4. Find new skills (in filesystem but not MemPalace)
new_skills = [s for s in all_current_skills if s['name'] not in existing_skills]

# 5. Find removed skills (in MemPalace but not filesystem)
current_names = {s['name'] for s in all_current_skills}
removed = [name for name in existing_skills if name not in current_names]

# 6. Find status mismatches (MemPalace vs config.yaml)
status_changed = []
for s in current_names & set(existing_skills.keys()):
    mem_status = existing_skills[s].get('status', 'enabled')
    expected = 'disabled' if s in disabled else 'enabled'
    if mem_status != expected:
        status_changed.append((s, mem_status, expected))

# 7. Add new skills and fix status mismatches
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

for name, old_status, new_status in status_changed:
    event_data = {
        'type': 'skill_registry',
        'skill_name': name,
        'status': new_status,
    }
    capture.capture_event(event_data)

# 8. Report summary (only if changes)
if new_skills or removed or status_changed:
    print(f'Total skills: {len(all_current_skills)}')
    print(f'New added: {len(new_skills)}')
    for s in new_skills:
        print(f'  + {s["name"]} [{s["category"]}]')
    print(f'Removed: {len(removed)}')
    for r in removed:
        print(f'  - {r}')
    print(f'Status changes: {len(status_changed)}')
    for name, old, new in status_changed:
        print(f'  ~ {name}: {old} -> {new}')
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
import sys, os, json
sys.path.insert(0, os.path.expanduser('~/.hermes/mempalace'))
import embed, capture

embed.init_embedding(os.path.expanduser('~/.hermes/mempalace'))
capture.init_capture(os.path.expanduser('~/.hermes/mempalace'))

# Read events by scanning raw directory (load_recent_events does NOT exist)
raw_dir = os.path.expanduser('~/.hermes/mempalace/raw')
for fname in os.listdir(raw_dir):
    if fname == 'archive':
        continue
    fpath = os.path.join(raw_dir, fname)
    try:
        with open(fpath) as f:
            content = f.read().strip()
            if not content:
                continue
            try:
                evt = json.loads(content)
                items = [evt]
            except:
                items = [json.loads(line) for line in content.split('\n') if line.strip()]
            for evt in items:
                # Handle both formats: nested under 'data' key (old) or top-level (new)
                data = evt.get('data', {})
                if not isinstance(data, dict) or data.get('type') != 'skill_registry':
                    if evt.get('type') == 'skill_registry':
                        data = evt
                if data.get('type') == 'skill_registry':
                    memory_id = evt.get('event_id') or evt.get('id', '')
                    text = f"{data['skill_name']} {data.get('skill_category', '')} {data.get('skill_description', '')}"
                    embed.add_embedding(memory_id, text)
    except:
        pass
embed._persist()
```

## Key Learnings from This Session

1. **Capture system must be initialized** before calling `capture_event()` — call `capture.init_capture(storage_path)` first
2. **Duplicate skill names** require special handling — the registry stores both with category suffix
3. **Status mismatches** between MemPalace and config.yaml are common — always reconcile during sync
4. **Sentence-transformers/FAISS not pre-installed** in Hermes venv — embeddings require separate install
5. **Silent mode** when no changes — don't notify user if registry is already current
6. **`capture.load_recent_events()` does NOT exist** — read events by scanning `~/.hermes/mempalace/raw/` directly with `os.listdir` + `json.loads`
7. **Dual event format**: old dated JSONL files nest data under a `data` key (`{"data": {"type": "skill_registry", ...}}`), while new events from `capture_event()` store data at the top level (`{"type": "skill_registry", ...}`). Always check both formats.
8. **No `agent.skill_utils` dependency needed** — use `os.walk` over `~/.hermes/skills` and `~/.hermes/hermes-agent/skills` directly, with user-dir-overrides-agent-dir dedup logic
9. **Archived skills** (in `.archive/` subdirectories) should be excluded from the active scan — they still exist on disk but aren't in active rotation
10. **Status change tracking** should be a separate step from new-skill detection — both produce registry updates but need different event data shapes

## Files Modified This Session

- `mempalace-skill-augmentation/SKILL.md` — Added this weekly sync pattern to the main skill
- `mempalace-skill-augmentation/references/weekly-skill-registry-sync.md` — This reference file
- `mempalace-skill-augmentation/references/skill-registry.md` — Fixed `load_recent_events` references

### 2026-06-21: Major fixes
- Replaced all `capture.load_recent_events()` calls with raw directory scanning (`os.listdir` + `json.loads`)
- Added dual-format event handling (nested `data` key vs top-level)
- Replaced `agent.skill_utils` imports with direct `os.walk` approach
- Added `.archive` directory exclusion
- Added status change tracking as a separate step
- Added 5 new key learnings (items 6-10)