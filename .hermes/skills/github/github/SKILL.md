---
name: github
description: "Complete GitHub workflow: authentication, repositories, issues, pull requests, code review, and CI/CD. Unified class-level skill covering all GitHub operations via gh CLI or REST API fallbacks."
version: 2.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [GitHub, Authentication, Repositories, Issues, Pull-Requests, Code-Review, CI-CD, gh-cli, REST-API]
    related_skills: [github-auth, github-code-review, github-issues, github-pr-workflow, github-repo-management]
---

# GitHub Complete Workflow

Class-level umbrella for all GitHub operations. Each section below corresponds to a former standalone skill whose detailed content has been preserved in `references/` and `templates/`.

## Quick Start

```bash
# Load the auth helper (sets GH_AUTH_METHOD, GITHUB_TOKEN, GH_USER, GH_OWNER, GH_REPO)
source "${HERMES_HOME:-$HOME/.hermes}/skills/github/github/scripts/gh-env.sh"
```

## 1. Authentication
**Trigger:** Setting up GitHub access, configuring SSH keys, or authenticating `gh` CLI.

- **Full guide:** `references/github-environment.md` — HTTPS tokens, SSH keys, gh CLI login, API token extraction, auth detection flow
- **Headless auth:** `references/headless-auth.md` — why `--web` fails silently, correct headless patterns, GH_TOKEN vs GITHUB_TOKEN
- **Auth script:** `scripts/gh-env.sh` — source this to set up the environment for any GitHub operation

Covers: git-only auth (HTTPS PAT, SSH keys), gh CLI auth (interactive browser, headless token), API auth detection, multi-account setup, troubleshooting.

### ⚠️ Headless/Server Auth (CRITICAL)

`gh auth login --web` opens a browser and **fails silently** in headless environments (SSH sessions, containers, CI). It returns exit code 0 but writes no token.

**Correct headless approaches (in order of preference):**

```bash
# Option A: PAT via stdin (best for automation)
echo "ghp_xxxxxxxxxxxx" | gh auth login --with-token

# Option B: Environment variable (fine-grained PAT recommended)
export GH_TOKEN="ghp_xxxxxxxxxxxx"
# gh CLI will use GH_TOKEN automatically — no gh auth login needed

# Option C: Check if already authenticated
gh auth status 2>&1 | grep -q "Logged in" && echo "OK" || echo "Need auth"
```

**Verify before use:**
```bash
gh auth status 2>&1
# Should show: "Logged in to github.com as <username>"
# If it shows "token is invalid", the token expired or was revoked
```

**Pitfall:** `GITHUB_TOKEN` env var and `GH_TOKEN` env var are different. `gh` CLI uses `GH_TOKEN`; GitHub Actions uses `GITHUB_TOKEN`. If both are set, `GH_TOKEN` takes precedence for `gh` CLI.

### ⚠️ Writing Tokens to `.env` — Tool Limitations

Hermes security features prevent writing tokens through normal tool calls:

- `write_file` replaces token values with `***` in the output file
- `read_file` and `patch` are blocked on `~/.hermes/.env`
- `execute_code` sandbox rewrites tokens in source code

**To persist a token in `.env`, tell the user to write it manually:**
```bash
echo 'GH_TOKEN=ghp_xxxxxxxxxxxx' >> ~/.hermes/.env
```

Or use keyring auth (preferred — bypasses `.env` entirely):
```bash
echo "ghp_xxxxxxxxxxxx" | gh auth login --with-token
```

## 2. Repository Management
**Trigger:** Cloning, creating, forking, or managing GitHub repos; releases; secrets; Actions workflows.

- **Full guide:** `references/github-api-cheatsheet.md` — clone/create/fork, remotes, releases, secrets, Actions, Gists, branch protection
- **Backup pattern:** `references/hermes-backup-pattern.md` — backing up Hermes config/skills to a private GitHub repo

Covers: `gh repo` commands and curl equivalents, repository settings, branch protection, Actions secrets (gh + encrypted curl), releases + asset uploads, workflow triggers, Gists.

## 3. Issues
**Trigger:** Creating, triaging, labeling, or assigning GitHub issues.

- **Bug report template:** `templates/bug-report.md`
- **Feature request template:** `templates/feature-request.md`

Covers: `gh issue` list/view/create/edit/close, label management, assignment, commenting, triage workflow, bulk operations, linking issues to PRs.

## 4. Pull Request Workflow
**Trigger:** Creating PRs, monitoring CI, auto-fixing failures, merging.

- **CI troubleshooting:** `references/ci-troubleshooting.md`
- **Conventional commits:** `references/conventional-commits.md`
- **PR body templates:** `templates/pr-body-feature.md`, `templates/pr-body-bugfix.md`

Covers: branch naming, commit conventions, PR creation (gh + curl), CI status checks and polling, auto-fix loop, merge methods (squash/rebase), auto-merge via GraphQL.

## 5. Code Review
**Trigger:** Reviewing local changes before push, or reviewing open PRs on GitHub.

- **Review output template:** `references/review-output-template.md`

Covers: local diff review (pure git), PR review via gh/curl, inline comments, formal review submission (approve/request changes/comment), review checklist (correctness, security, quality, testing, performance, documentation), pre-push review workflow.

## 6. CI/CD Troubleshooting
**Trigger:** CI failures, workflow issues, Actions debugging.

See `references/ci-troubleshooting.md` for common failure patterns, log retrieval, and auto-fix loop patterns.

## DOX Integration

When working in a project that uses the [DOX (Self-documenting AGENTS.md)](https://github.com/agent0ai/dox) framework:

- **Read Before Editing:** Walk the DOX tree from root to the target path. Read every AGENTS.md along the route before making any changes.
- **Update After Editing:** If the change affects purpose, scope, ownership, structure, workflows, or operating rules, update the closest owning AGENTS.md and refresh the Child DOX Index.
- **Reference:** [agent0ai/dox](https://github.com/agent0ai/dox) — copy `AGENTS.md` from the repo root into your project to initialize.

## Scripts

- `scripts/gh-env.sh` — Auth detection and environment setup helper

## Reference Files

| File | Content |
|------|---------|
| `references/github-environment.md` | Full auth setup (HTTPS, SSH, gh CLI, API) |
| `references/headless-auth.md` | Headless/server auth: why `--web` fails, GH_TOKEN, `--with-token` |
| `references/github-api-cheatsheet.md` | API quick reference for all GitHub operations |
| `references/hermes-backup-pattern.md` | Hermes-to-GitHub backup procedure |
| `references/ci-troubleshooting.md` | CI failure diagnosis and auto-fix patterns |
| `references/conventional-commits.md` | Commit message format guide |
| `references/review-output-template.md` | Code review output structure |

## Templates

| File | Use |
|------|-----|
| `templates/bug-report.md` | Bug report issue template |
| `templates/feature-request.md` | Feature request issue template |
| `templates/pr-body-feature.md` | PR body for new features |
| `templates/pr-body-bugfix.md` | PR body for bug fixes |
