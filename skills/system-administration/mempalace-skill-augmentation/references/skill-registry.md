# Skill Registry in MemPalace

## Pattern: Storing Skills as MemPalace Events

To make skills semantically searchable (beyond the built-in `skills_list()`), store them as MemPalace events with FAISS embeddings:

```python
import sys, os, json, yaml
sys.path.insert(0, os.path.expanduser('~/.hermes/mempalace'))
import capture, embed
from pathlib import Path

# Initialize
storage = Path.home() / '.hermes' / 'mempalace'
capture.init_capture(str(storage))
embed.init_embedding(str(storage))

# Load disabled list
config_path = Path.home() / '.hermes' / 'config.yaml'
with open(config_path) as f:
    cfg = yaml.safe_load(f)
disabled = set(cfg.get('skills', {}).get('disabled', []))

# Scan all SKILL.md files
sys.path.insert(0, str(Path.home() / '.hermes' / 'hermes-agent'))
from agent.skill_utils import get_all_skills_dirs, iter_skill_index_files, parse_frontmatter

all_skills = []
for skills_dir in get_all_skills_dirs():
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
            all_skills.append({
                'name': name,
                'description': desc[:500],
                'category': category,
            })
        except:
            pass

# Deduplicate and store
seen = set()
added = 0
for skill in all_skills:
    if skill['name'] in seen:
        continue
    seen.add(skill['name'])
    status = 'disabled' if skill['name'] in disabled else 'enabled'
    event_data = {
        'type': 'skill_registry',
        'skill_name': skill['name'],
        'skill_category': skill['category'],
        'skill_description': skill['description'],
        'status': status,
    }
    event_id = capture.capture_event(event_data)
    if event_id:
        text = f"{skill['name']} {skill['category']} {skill['description']}"
        embed.add_embedding(event_id, text)
        added += 1

embed._persist()
print(f'Stored {added} skills')
print(f'FAISS index: {embed.get_index_stats()["total_vectors"]} vectors')
```

## Searching for Skills via MemPalace

```python
import sys, os
sys.path.insert(0, os.path.expanduser('~/.hermes/mempalace'))
import embed, capture

embed.init_embedding(os.path.expanduser('~/.hermes/mempalace'))
results = embed.search_embeddings("task description", k=10)

# Load raw events to get skill details
events = capture.load_recent_events(days=365)
event_map = {e['id']: e for e in events}

for memory_id, score in results:
    event = event_map.get(memory_id, {})
    data = event.get('data', {})
    if data.get('type') == 'skill_registry':
        print(f"  {data['skill_name']} [{data['skill_category']}] "
              f"score={score:.3f} status={data.get('status', '?')}")
```

## Re-enabling a Disabled Skill

When a disabled skill is needed:

```python
import yaml
from pathlib import Path

config_path = Path.home() / '.hermes' / 'config.yaml'
with open(config_path) as f:
    cfg = yaml.safe_load(f)

disabled = cfg.get('skills', {}).get('disabled', [])
skill_name = 'target-skill-name'

if skill_name in disabled:
    disabled.remove(skill_name)
    cfg['skills']['disabled'] = disabled
    with open(config_path, 'w') as f:
        yaml.dump(cfg, f, default_flow_style=False, allow_unicode=True)
    print(f'Re-enabled {skill_name}')

    # Clear snapshot cache
    snapshot = Path.home() / '.hermes' / '.skills_prompt_snapshot.json'
    if snapshot.exists():
        snapshot.unlink()
    print('Snapshot cleared — restart gateway to apply')
else:
    print(f'{skill_name} is already enabled')
```

Note: `skill_view(name)` works regardless of disabled status — disabling only affects the system prompt index, not direct loading.
