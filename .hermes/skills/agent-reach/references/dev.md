# 开发工具

GitHub CLI

## GitHub (gh CLI)

GitHub 官方命令行工具，用于仓库、Issue、PR、Actions、Release 以及 API 访问。

```bash
# 认证 — headless/server 环境
unset GITHUB_TOKEN  # 如果 .env 里有无效 token，先取消环境变量
echo "<token>" | gh auth login --with-token
gh auth status  # 验证

# 认证 — 交互式（有浏览器）
gh auth login

# 搜索
gh search repos "query" --sort stars --limit 10
gh search code "query" --language python

# 仓库
gh repo view owner/repo
gh repo clone owner/repo
gh repo create my-repo --private
gh repo fork owner/repo
gh repo fork owner/repo --clone
gh repo sync owner/repo

# Issues
gh issue list -R owner/repo --state open
gh issue view 123 -R owner/repo
gh issue create -R owner/repo --title "Title" --body "Body"

# Pull Requests
gh pr list -R owner/repo --state open
gh pr view 123 -R owner/repo
gh pr create -R owner/repo --title "Title" --body "Body"
gh pr checks 123 --repo owner/repo

# Actions / CI
gh run list --repo owner/repo --limit 10
gh run view <run-id> --repo owner/repo
gh run view <run-id> --repo owner/repo --log-failed
gh workflow list --repo owner/repo

# Releases
gh release list -R owner/repo
gh release create v1.0.0

# API
gh api /user
gh api repos/owner/repo

# JSON 输出
gh issue list --repo owner/repo --json number,title --jq '.[] | "\(.number): \(.title)"'
```

## Auth Pitfall — GITHUB_TOKEN overrides keyring

If `gh auth status` says "token is invalid" after you've logged in with `gh auth login --with-token`, the cause is almost always a stale `GITHUB_TOKEN` in `~/.hermes/.env` or the process environment. It takes precedence over the keyring-stored credential.

**Fix:** `unset GITHUB_TOKEN` before running gh commands, or remove the invalid entry from `.env`.

**Do NOT use `gh auth login --web`** in headless/server environments — it silently fails (opens browser, writes no token, exits 0).

## 选择指南

| 工具 | 来源 | 用途 |
|-----|------|------|
| gh CLI | agent-reach | Git 操作 |
| zread | my-mcp-tools | 读仓库内容 |
| context7 | my-mcp-tools | 查技术文档 |
