---
name: github
description: "Complete GitHub workflow: authentication, repositories, issues, pull requests, code review, and CI/CD. Unified class-level skill covering all GitHub operations via gh CLI or REST API fallbacks."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [GitHub, Authentication, Repositories, Issues, Pull-Requests, Code-Review, CI-CD, gh-cli, REST-API]
    related_skills: [github-auth, github-code-review, github-issues, github-pr-workflow, github-repo-management]
---

## 🔍 MemPalace Query (MANDATORY FIRST STEP)
Before proceeding, query MemPalace for existing context:
```python
import sys, os; sys.path.insert(0, os.path.expanduser('~/.hermes/mempalace'))
import embed; embed.init_embedding(os.path.expanduser('~/.hermes/mempalace'))
results = embed.search_embeddings("GitHub authentication repository management", k=5)
```
This retrieves previous decisions, domain-specific context, and lessons learned from the vector memory store.

# GitHub Complete Workflow

This is the class-level umbrella skill for all GitHub operations. It consolidates authentication, repository management, issues, pull requests, code review, and CI/CD into a single discoverable skill with labeled subsections.

## Architecture

Each subsection below corresponds to a former standalone skill that has been absorbed. The original narrow skills are archived and their unique content preserved here or in `references/`, `templates/`, `scripts/`.

### Subsections
1. [Authentication](#authentication) — HTTPS tokens, SSH keys, gh CLI login
2. [Repository Management](#repository-management) — Clone/create/fork, remotes, releases, secrets
3. [Issues](#issues) — Create, triage, label, assign via gh or REST
4. [Pull Request Workflow](#pull-request-workflow) — Branch, commit, open, CI, merge
5. [Code Review](#code-review) — Diffs, inline comments, formal reviews
6. [CI/CD Troubleshooting](#ci-cd-troubleshooting) — Common failure patterns and fixes

## Quick Start

```bash
# Load the auth helper (sets GH_AUTH_METHOD, GITHUB_TOKEN, GH_USER, GH_OWNER, GH_REPO)
source "${HERMES_HOME:-$HOME/.hermes}/skills/github/github/scripts/gh-env.sh"

# Then use gh or curl patterns from the relevant subsection
```