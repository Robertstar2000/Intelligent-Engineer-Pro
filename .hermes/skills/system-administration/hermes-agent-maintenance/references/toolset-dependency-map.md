# Toolset Dependency Map

Quick reference for what each toolset needs to function, gathered from `toolsets.py`, `pytool.toml`, and individual tool source files.

## Toolsets That Work Out of the Box (No Extra Setup)
| Toolset | Key libs | Notes |
|---------|----------|-------|
| `web` | `requests` (built-in) | Needs search backend configured |
| `terminal` | — | Uses local shell by default |
| `file` | — | Pure Python stdlib |
| `vision` | `pillow` | Already in venv |
| `skills` | — | Core tool, always available |
| `todo` | — | Core tool, always available |
| `memory` | `aiosqlite` | Already in venv |
| `session_search` | `aiosqlite` | FTS5 in SQLite, already works |
| `cronjob` | — | Core tool |
| `clarify` | — | Core tool |
| `execute_code` | — | Core tool |
| `delegate_task` | — | Core tool |
| `messaging` | — | Needs gateway running |
| `browser` | Playwright (node) | Already installed |

## Toolsets That Need Python Packages (Already in venv as of May 2026)
| Toolset | Package | Status | Activates When |
|---------|---------|--------|----------------|
| `image_gen` | `fal_client==0.13.2` | ✅ Installed | `FAL_KEY` set in env |
| `video_gen` | `fal_client` (FAL backend) or `requests` (xai backend) | ✅ Plugins in repo | Plugin enabled + API key |
| `tts` | `edge-tts==7.2.7` | ✅ Installed | Always active (free) |
| `computer_use` | `mcp==1.26.0` | ✅ Installed | `cua-driver` binary present (macOS only) |

## Toolsets That Need System Packages (Require root / user install)
| Toolset | System Package | Install Command | Status on this system |
|---------|---------------|-----------------|----------------------|
| `search` / `web` | `ripgrep` (rg) | `sudo apt install -y ripgrep` or static binary to `~/.local/bin/rg` | ❌ Not installed (network timeout prevented download) |
| Docker backend | `docker.io` | `sudo apt install -y docker.io` | ❌ Not installed (needs root password) |

## Toolsets That Need API Keys (Software installed, needs credentials)
| Toolset | Required Credential | Config Location |
|---------|-------------------|-----------------|
| `x_search` | `XAI_API_KEY` or SuperGrok OAuth | `~/.hermes/.env` or `hermes auth add xai-oauth` |
| `image_gen` | `FAL_KEY` | `~/.hermes/.env` |
| `video_gen` (FAL) | `FAL_KEY` | `~/.hermes/.env` |
| `video_gen` (xai) | `XAI_API_KEY` | `~/.hermes/.env` |

## Key Source Files for Reference
- Toolset definitions: `~/.hermes/hermes-agent/toolsets.py` — `TOOLSETS` dict maps toolset name → tool list
- Dependency pins: `~/.hermes/hermes-agent/pyproject.toml` — `[project.optional-dependencies]` section
- Image gen plugin: `plugins/image_gen/fal/` — uses `fal_client`
- Video gen plugins: `plugins/video_gen/fal/` and `plugins/video_gen/xai/`
- x_search tool: `tools/x_search_tool.py` — uses `tools/xai_http.py` for credential resolution
- Computer use: `tools/computer_use/` — uses `mcp` stdio client to talk to `cua-driver` binary
- yuanbao: `tools/yuanbao_tools.py` — gateway platform adapter, no extra deps
