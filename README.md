# FL-Hermes

Complete backup of Hermes Agent configuration, customizations, and supporting files for the MIFECO production environment.

## What's Included

| Directory | Contents |
|---|---|
| `config/` | `config.yaml` (API keys redacted) |
| `skills/` | All custom skills (127 directories) |
| `mempalace/` | Vector memory system + FAISS index |
| `memories/` | MEMORY.md, USER.md |
| `scripts/` | All utility scripts |
| `cron/` | Job definitions (jobs.json) |
| `consulting-reports/` | Generated consulting reports |
| `pipeline-engine/` | MIFECO pipeline automation |

## What's Excluded

- `.env` — contains API keys (see `.env.example` for template)
- `auth.json` — contains OAuth tokens
- `hermes-agent/` — the Hermes source code (already on GitHub)
- `sessions/`, `checkpoints/`, `state-snapshots/` — runtime state (large, regenerable)
- `node/`, `lsp/`, `bin/` — installed dependencies (regenerable)
- `logs/` — runtime logs
- `cache/`, `image_cache/`, `audio_cache/` — temporary caches

## Setup

1. Clone this repo to `~/.hermes/`
2. Copy `.env.example` to `.env` and fill in your API keys
3. Run `hermes setup` to initialize
4. Skills are auto-loaded from `~/.hermes/skills/`

## Repository

https://github.com/Robertstar2000/FL-Hermes
