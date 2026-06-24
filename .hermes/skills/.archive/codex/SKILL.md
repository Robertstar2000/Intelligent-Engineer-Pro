---
name: codex
description: Delegate coding tasks to OpenAI Codex CLI agent. Use for building features, refactoring, PR reviews, and batch issue fixing. Requires the codex CLI and a git repository.
version: 1.4.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [Coding-Agent, Codex, OpenAI, Code-Review, Refactoring]
    related_skills: [claude-code, hermes-agent]
---

## 🔍 MemPalace Query (MANDATORY FIRST STEP)
Before proceeding, query MemPalace for existing context:
```python
import sys, os; sys.path.insert(0, os.path.expanduser('~/.hermes/mempalace'))
import embed; embed.init_embedding(os.path.expanduser('~/.hermes/mempalace'))
results = embed.search_embeddings("Codex CLI OpenAI coding agent delegation PR review", k=5)
```
This retrieves previous decisions, domain-specific context, and lessons learned from the vector memory store.

# Codex CLI

Delegate coding tasks to [Codex](https://github.com/openai/codex) via the Hermes terminal. Codex is OpenAI's autonomous coding agent CLI.

## Prerequisites

- Codex installed: `npm install -g @openai/codex`
- **Authentication completed** — API key method recommended (see below). Device auth login works but `codex exec` does not.
- **Must run inside a git repository** — Codex refuses to run outside one. Use `--skip-git-repo-check` for temp dirs.
- Use `pty=true` in terminal calls — Codex is an interactive terminal app

## Setup & Authentication

### Step 1: Install

```bash
npm install -g @openai/codex
```

### Step 2: Resolve the binary

The npm global install may not automatically add `codex` to PATH. If `codex` is not found after install:

```bash
# Find where npm put it
npm root -g
# Usually at: /home/user/.local/lib/node_modules/@openai/codex/
# The binary is at: bin/codex.js inside the package dir

# Symlink it to a PATH location
ln -sf $(npm root -g)/@openai/codex/bin/codex.js /home/user/.local/bin/codex
chmod +x /home/user/.local/bin/codex

# Verify
codex --version
```

### Step 3: Authenticate

Codex CLI v0.128.0+ supports **two authentication methods**:

#### Method A — Agent Identity Token

If you have a Codex agent identity JWT token (contains Ed25519 private key):

```bash
# Store token securely (one-time setup)
mkdir -p ~/.codex && chmod 700 ~/.codex
echo "<token>" > ~/.codex/agent-identity.token
chmod 600 ~/.codex/agent-identity.token

# Authenticate
cat ~/.codex/agent-identity.token | codex login --with-agent-identity
```

Verify: `codex login status` → should show "Logged in using Agent Identity"

> **Security**: Token file is chmod 600 (owner-only). Token contains an Ed25519 agent private key — treat it as a credential. Do not log it, do not pass it through chat, do not commit it.

> ⚠️ **CRITICAL: Device auth currently non-functional.** As of v0.128.0, device auth login succeeds but ALL models are rejected with "model is not supported when using Codex with a ChatGPT account." The **only working method** for `codex exec` is **Method C (API key)**. Update this skill when OpenAI changes model access policies.

#### Method C — OpenAI API Key (RECOMMENDED — only working method)

If you have an OpenAI API key (from https://platform.openai.com/api-keys):

```bash
echo "sk-..." | codex login --with-api-key
```

Verify: `codex login status` → should show logged in.

This bypasses the OAuth/device-auth flow entirely. Useful when device auth is rate-limited or no browser is available. Requires a separate OpenAI API key (not the OpenRouter key).

**Confirmed working (v0.136.0):** Model `gpt-5.3-codex` works with API key auth. Codex can write and execute Python code, generate files, and perform complex multi-step coding tasks.

#### Method B — Device Auth (interactive, no pre-existing token)

**Device auth (headless/remote server — no browser):**
```bash
codex login --device-auth
# Prints:
# 1. Open this link in your browser: https://auth.openai.com/codex/device
# 2. Enter this one-time code: XXXXX-XXXXX (expires in 15 minutes)
#
# User completes auth in their browser; CLI auto-completes when they do.
```

Best practice for headless:
```bash
# Run in background so it waits for user to authenticate in their browser
terminal(command="codex login --device-auth", background=true, pty=true, timeout=600)
# Then poll to see the printed code
process(action="poll", session_id="<id>")
```

> ⚠️ **Pitfall — `process(action="wait")` clamps to 60s max.** The device-auth code expires in 15 minutes, but `wait` will time out after 60s and return the process still running. **Do NOT use `wait`** for the login flow — use repeated `poll` calls instead. Only after `poll` shows `status: "completed"` (or the process exits) is auth done.

> ⚠️ **Pitfall — Device auth can 429 if retried too fast.** If you get `Error logging in with device code: device auth failed with status 429 Too Many Requests`, wait several minutes before retrying.

> ⚠️ **CRITICAL — Device auth login succeeds but `codex exec` does NOT work.** As of v0.128.0–v0.136.0, ALL models are rejected with "model is not supported when using Codex with a ChatGPT account." Device auth is only useful for `codex login status` verification. **Use Method C (API key) for actual `codex exec` work.**

> ⚠️ **Pitfall — v0.136.0 renamed `--with-agent-identity` to `--with-access-token`.** If you have a JWT agent identity token, use `cat ~/.codex/agent-identity.token | codex login --with-access-token`. However, this still won't work for `codex exec` (401 errors) — the token's `aud` doesn't match the CLI's backend.

> ⚠️ **Pitfall — Codex sandbox filesystem is read-only.** Even with `sandbox="danger-full-access"` and `approvals="never"` in `~/.codex/config.toml`, the exec tool's filesystem is mounted read-only at the OS level. Codex CAN write files to `/tmp` via Python `open()` calls inside `exec`, but `apply_patch` and direct file writes are blocked. **Workaround:** Use codex to generate Python code, then run the code directly on the host machine (not through codex's exec). This is the confirmed pattern for image generation, file creation, and any task requiring writes.

> ⚠️ **Pitfall — v0.136.0 confirmed: API key auth works, agent identity does not.** As of v0.136.0, `echo "sk-proj-..." | codex login --with-api-key` works for `codex exec` with model `gpt-5.3-codex`. Agent identity JWT tokens (stored at `~/.codex/agent-identity.token`) cause 401 errors — the token's `aud: "codex-app-server"` doesn't match the CLI's `chatgpt.com/backend-api` endpoint. Device auth login succeeds but all models are rejected with "not supported when using Codex with a ChatGPT account." **Only API key auth works for `codex exec`.**

## Hermes `openai-codex` Provider Auth (Separate from Codex CLI)

When the user asks to "set up Codex auth" for Hermes (not the CLI), they mean configuring Hermes's `openai-codex` model provider using a ChatGPT OAuth JWT token. This is **completely separate** from `codex login`.

### Key Distinction
- **Codex CLI auth** → `codex login --with-api-key` → stored in `~/.codex/auth.json` → used by `codex exec`
- **Hermes provider auth** → `CODEX_OAUTH_TOKEN` in `~/.hermes/.env` → stored in `~/.hermes/auth.json` → used by Hermes delegation

### Setup Steps

1. **Verify token exists in `.env`:**
   ```bash
   grep CODEX_OAUTH_TOKEN ~/.hermes/.env
   ```
   Token is a JWT starting with `eyJhbG...`.

2. **Add to `auth.json`** — Must be in BOTH `providers` and `credential_pool` (see `references/auth-methods.md` for full JSON structure). ⚠️ The gateway overwrites `auth.json` on restart — the reliable approach is to set `CODEX_OAUTH_TOKEN` in `.env` and let the gateway auto-populate auth.json.

3. **Add delegation config in `config.yaml`:**
   ```yaml
   delegation:
     subagent_providers:
       codex:
         provider: openai-codex
         model: openai-codex
         api_mode: codex_responses
         base_url: https://chatgpt.com/backend-api/codex
   ```

4. **Restart gateway and verify:**
   ```
   hermes doctor
   ```
   Should show: `✓ OpenAI Codex auth (logged in)`

### Pitfall: `auth.json` Gateway Overwrite
The gateway process rewrites `auth.json` on each startup. Manual edits to `auth.json` may be lost. Always set `CODEX_OAUTH_TOKEN` in `~/.hermes/.env` as the source of truth, then restart the gateway to let it auto-populate.

### Step 4: Verify authentication

```bash
codex login status
# Should show "Logged in using Agent Identity" or similar
codex --version
# Should return "codex-cli X.Y.Z" — no auth error
```

If you get auth errors, re-run the login flow. Tokens are stored locally and refresh automatically.

## One-Shot Tasks

```
terminal(command="codex exec 'Add dark mode toggle to settings'", workdir="~/project", pty=true)
```

For scratch work (Codex needs a git repo):
```
terminal(command="cd $(mktemp -d) && git init && codex exec 'Build a snake game in Python'", pty=true)
```

## Background Mode (Long Tasks)

```
# Start in background with PTY
terminal(command="codex exec --full-auto 'Refactor the auth module'", workdir="~/project", background=true, pty=true)
# Returns session_id

# Monitor progress
process(action="poll", session_id="<id>")
process(action="log", session_id="<id>")

# Send input if Codex asks a question
process(action="submit", session_id="<id>", data="yes")

# Kill if needed
process(action="kill", session_id="<id>")
```

## Key Flags

| Flag | Effect |
|------|--------|
| `exec "prompt"` | One-shot execution, exits when done |
| `--full-auto` | Sandboxed but auto-approves file changes in workspace |
| `--yolo` | No sandbox, no approvals (fastest, most dangerous) |

## PR Reviews

Clone to a temp directory for safe review:

```
terminal(command="REVIEW=$(mktemp -d) && git clone https://github.com/user/repo.git $REVIEW && cd $REVIEW && gh pr checkout 42 && codex review --base origin/main", pty=true)
```

## Parallel Issue Fixing with Worktrees

```
# Create worktrees
terminal(command="git worktree add -b fix/issue-78 /tmp/issue-78 main", workdir="~/project")
terminal(command="git worktree add -b fix/issue-99 /tmp/issue-99 main", workdir="~/project")

# Launch Codex in each
terminal(command="codex --yolo exec 'Fix issue #78: <description>. Commit when done.'", workdir="/tmp/issue-78", background=true, pty=true)
terminal(command="codex --yolo exec 'Fix issue #99: <description>. Commit when done.'", workdir="/tmp/issue-99", background=true, pty=true)

# Monitor
process(action="list")

# After completion, push and create PRs
terminal(command="cd /tmp/issue-78 && git push -u origin fix/issue-78")
terminal(command="gh pr create --repo user/repo --head fix/issue-78 --title 'fix: ...' --body '...'")

# Cleanup
terminal(command="git worktree remove /tmp/issue-78", workdir="~/project")
```

## Batch PR Reviews

```
# Fetch all PR refs
terminal(command="git fetch origin '+refs/pull/*/head:refs/remotes/origin/pr/*'", workdir="~/project")

# Review multiple PRs in parallel
terminal(command="codex exec 'Review PR #86. git diff origin/main...origin/pr/86'", workdir="~/project", background=true, pty=true)
terminal(command="codex exec 'Review PR #87. git diff origin/main...origin/pr/87'", workdir="~/project", background=true, pty=true)

# Post results
terminal(command="gh pr comment 86 --body '<review>'", workdir="~/project")
```

## Rules

1. **Always use `pty=true`** — Codex is an interactive terminal app and hangs without a PTY
2. **Git repo required** — Codex won't run outside a git directory. Use `mktemp -d && git init` for scratch. Pass `--skip-git-repo-check` to skip the trusted-directory check in temp dirs.
3. **Use `exec` for one-shots** — `codex exec "prompt"` runs and exits cleanly
4. **`--full-auto` for building** — auto-approves changes within the sandbox
5. **Background for long tasks** — use `background=true` and monitor with `process` tool
6. **Don't interfere** — monitor with `poll`/`log`, be patient with long-running tasks
7. **Parallel is fine** — run multiple Codex processes at once for batch work
8. **Device auth: poll, don't wait** — `codex login --device-auth` requires the user to enter a code in their browser within 15 min. `process(action="wait")` clamps to 60s and will timeout before auth completes. Use repeated `process(action="poll")` calls and only proceed once the process shows `status: "completed"` or exits on its own.
9. **Agent identity tokens ≠ CLI auth** — Agent identity JWTs (`aud: "codex-app-server"`) authenticate to the app-server, NOT to the CLI's backend API. They will cause 401 errors if used for `codex exec`. Use device auth or API key instead. See `references/auth-methods.md` for full comparison.
10. **Device auth models don't work** — Even after successful device-auth login, `codex exec` rejects ALL models with "not supported when using Codex with a ChatGPT account." Only API key auth works for `codex exec`. See `references/auth-methods.md`.
11. **Image generation is NOT a codex task** — Codex writes code, it doesn't generate images. For infographics and image generation, use the `image-generation-workflow` or `baoyu-infographic` skills instead.
