# Skill Registry Quick Reference

See the full skill registry pattern in `mempalace-skill-augmentation/references/skill-registry.md`.

## Key Numbers (2026-07-03)

- **Total skills in registry:** 220
- **FAISS vectors:** 267 (includes skill embeddings + other MemPalace events)
- **Disabled:** 91 skills (~36% token reduction)
- **Enabled:** ~129 skills

## Weekly Cron

Job ID: `bcd209af7131` — "Weekly Skill Registry Review"
- Schedule: Sundays at 9:00 AM
- Action: Scans for new skills, compares with MemPalace registry, adds/removes as needed
- Only reports if changes found (stays silent otherwise)

## Re-enable a Skill

```python
import yaml
from pathlib import Path

config_path = Path.home() / '.hermes' / 'config.yaml'
with open(config_path) as f:
    cfg = yaml.safe_load(f)

disabled = cfg.get('skills', {}).get('disabled', [])
if '<skill_name>' in disabled:
    disabled.remove('<skill_name>')
    cfg['skills']['disabled'] = disabled
    with open(config_path, 'w') as f:
        yaml.dump(cfg, f, default_flow_style=False, allow_unicode=True)

# Clear cache
snapshot = Path.home() / '.hermes' / '.skills_prompt_snapshot.json'
if snapshot.exists():
    snapshot.unlink()

# Inform user to restart gateway
```

## Search Skills

```python
import sys; sys.path.insert(0, '~/.hermes/mempalace')
import embed
embed.init_embedding('~/.hermes/mempalace')
results = embed.search_embeddings("<task>", k=10)
```