# Hermes Agent Full Backup to Private GitHub Repository

## Overview

Complete procedure for backing up a Hermes Agent installation to a private GitHub repository. Covers config redaction, skill/memory/mempalace copying, cron job export, and recurring auto-backup.

## When to Use

- Setting up a new backup repository for the first time
- Periodically updating the backup (via cron or manual trigger)
- Migrating Hermes to a new machine (clone + restore)

## Prerequisites

- SSH key configured on GitHub (`ssh -T git@github.com` returns success)
- Target private repo created on GitHub (e.g., `FL-Hermes`)

## Procedure

### 1. Create .gitignore First

Create a `.gitignore` BEFORE copying anything. Key exclusions:
- `.env` and all `*.env` files (contain API keys)
- `auth.json` (contains OAuth tokens)
- `__pycache__/`, `*.pyc`, `*.log`, `*.cache`
- Large binaries: `*.bin`, `*.gguf`, `*.safetensors`, `*.onnx`
- Runtime state: `sessions/`, `checkpoints/`, `state-snapshots/`
- Installed dependencies: `node/`, `lsp/`, `bin/`
- Logs: `logs/`

### 2. Redact and Copy Config

Use Python to redact secrets — NEVER use `hermes config set` for this:

```python
import yaml
from pathlib import Path

def redact(obj):
    if isinstance(obj, dict):
        return {k: ('***' if any(s in k.lower() for s in ['key','token','secret','password','api_key','credential','auth','pat','bearer'])) else redact(v)) for k,v in obj.items()}
    elif isinstance(obj, list):
        return [redact(i) for i in obj]
    return obj

cfg = yaml.safe_load(Path.home() / '.hermes/config.yaml').read_text())
safe = redact(cfg)
Path('config/config.yaml').write_text(yaml.dump(safe, default_flow_style=False))
```

Also create `.env.example` from the real `.env` with all values replaced by placeholders.

### 3. Verify No Secrets

```python
import re, yaml
from pathlib import Path

text = (Path.home() / 'FL-Hermes/config/config.yaml').read_text()
for p in [r'sk-[a-zA-Z0-9]{20,}', r'ghp_[a-zA-Z0-9]{36}', r'gho_[a-zA-Z0-9]{36}', r'Bearer\s+[a-zA-Z0-9]{20,}']:
    assert not re.search(p, text), f'FAIL: secret pattern found: {p}'
print('PASS: no secrets in config')
```

### 4. Copy Files via rsync

```bash
cd ~/FL-Hermes
mkdir -p skills mempalace memories scripts cron consulting-reports pipeline-engine

# Skills (exclude caches)
rsync -a --exclude='__pycache__' --exclude='*.pyc' ~/.hermes/skills/ skills/

# MemPalace (exclude raw/ if very large, keep indexes/)
rsync -a --exclude='__pycache__' --exclude='*.pyc' --exclude='raw/' ~/.hermes/mempalace/ mempalace/

# Memories
cp ~/.hermes/memories/MEMORY.md memories/
cp ~/.hermes/memories/USER.md memories/

# Scripts, cron, reports, pipeline
rsync -a ~/.hermes/scripts/ scripts/
cp ~/.hermes/cron/jobs.json cron/
rsync -a ~/.hermes/consulting-reports/ consulting-reports/
rsync -a --exclude='__pycache__' --exclude='data/' ~/.hermes/pipeline-engine/ pipeline-engine/
```

### 5. Commit and Push

```bash
git add -A
git commit -m "Hermes backup: $(date +%Y-%m-%d)"
GIT_SSH_COMMAND="ssh -i ~/.ssh/id_ed25519" git push -u origin main
```

## Excluded Items (Never Back Up)

- `.env` — API keys (38+ secrets)
- `auth.json` — OAuth tokens
- `hermes-agent/` — source code (already on GitHub)
- `sessions/`, `checkpoints/`, `state-snapshots/` — runtime state, large
- `node/`, `lsp/`, `bin/` — installed dependencies
- `logs/`, `cache/`, `image_cache/`, `audio_cache/` — temporary files

## Auto-Backup Cron

Schedule a weekly cron job that:
1. Runs the rsync + redaction steps above
2. `git add -A && git commit -m "Weekly backup: $(date)"`
3. `GIT_SSH_COMMAND="ssh -i ~/.ssh/id_ed25519" git push`
4. Reports status
