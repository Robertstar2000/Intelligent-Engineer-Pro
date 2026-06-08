# GitHub Environment — Bob's Setup (2026-07-03)

## Authentication Status

| Method | Status | Details |
|--------|--------|---------|
| **SSH** | ✅ Working | Key: `~/.ssh/id_ed25519` → authenticated as `Robertstar2000` |
| **gh CLI** | ⚠️ Installed, not authenticated | `~/.local/bin/gh` v2.83.0 — needs `gh auth login` with PAT |
| **API (curl)** | ✅ Working | Public API accessible without auth via `curl https://api.github.com/...` |
| **Git HTTPS** | ⚠️ No credential helper | Would need PAT for HTTPS push |

## Access Patterns

### Read repos via API (no auth needed for public):
```bash
curl -s "https://api.github.com/users/Robertstar2000/repos?sort=updated&per_page=100"
```

### Clone/push via SSH:
```bash
GIT_SSH_COMMAND="ssh -i ~/.ssh/id_ed25519" git clone git@github.com:Robertstar2000/<repo>.git
```

### List GitHub user:
```bash
curl -s "https://api.github.com/users/Robertstar2000"
```

## Key Repos

| Repo | Lang | Description |
|------|------|-------------|
| `TallmanZero` | Python | Working clone of agent zero |
| `Tallman-LMS` | TypeScript | Learning Management System |
| `mifeco_web` | JavaScript | New website |
| `Hypatia` | TypeScript | Project Hypatia update |
| `MIFECO_Web_php` | PHP | MIFECO website |
| `BOBnet` | Python | Advanced self-improving agents |
| `OpenC` | — | Personal version of Open Claw |

## gh CLI Setup (when needed)

If full `gh` CLI auth is needed for PR/issue management:
```bash
# User provides PAT, then:
echo "<PAT>" | ~/.local/bin/gh auth login --with-token
~/.local/bin/gh auth setup-git
```

## Notes

- No `sudo` available — `gh` was downloaded directly from GitHub releases
- No `gh` in system PATH — use `~/.local/bin/gh` or add to PATH
- Firewall blocks some download methods but `wget` and `curl` work for GitHub domains
- Total repos: 29 (as of 2026-07-03)