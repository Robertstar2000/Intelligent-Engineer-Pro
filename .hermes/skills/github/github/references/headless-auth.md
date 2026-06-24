# GitHub Headless/Server Authentication

## Problem

`gh auth login --web` opens a browser for OAuth flow. In headless environments (SSH, containers, CI, agents), there is no browser — the command **exits 0 but writes no token**. Silent failure.

## Detection

```bash
gh auth status 2>&1
# Bad: "Failed to log in to github.com using token (GITHUB_TOKEN)"
# Bad: "You are not logged into any GitHub hosts"
# Good: "Logged in to github.com as <username>"
```

## Solutions (headless-safe)

### Option A: GH_TOKEN environment variable (preferred for automation)

```bash
export GH_TOKEN=<your-fine-grained-pat>
# gh CLI uses GH_TOKEN automatically — no gh auth login needed
gh auth status  # verify
```

- `GH_TOKEN` takes precedence over `GITHUB_TOKEN` for `gh` CLI
- Fine-grained PATs are recommended (scope to specific repos)
- Classic PAT with `repo`, `read:org`, `gist` scopes also works

### Option B: PAT via stdin

```bash
echo "<token>" | gh auth login --with-token
```

### Option C: Check before acting

```bash
if ! gh auth status 2>&1 | grep -q "Logged in"; then
    echo "ERROR: gh not authenticated. Set GH_TOKEN or use gh auth login --with-token"
    exit 1
fi
```

## Token Scopes Required

| Operation | Minimum scope |
|-----------|--------------|
| Read repos, issues, PRs | `repo` (full) or `public_repo` (public only) |
| Read org membership | `read:org` |
| Create gists | `gist` |
| Trigger workflows | `workflow` |

## Pitfalls

- `GITHUB_TOKEN` ≠ `GH_TOKEN`: `gh` CLI uses `GH_TOKEN`; GitHub Actions uses `GITHUB_TOKEN`
- Fine-grained PATs may have resource-specific restrictions that cause confusing 404s
- Tokens expire — check `gh auth status` before long-running operations
- `gh auth login --web` in PTY mode still requires a browser; it won't work over plain SSH
