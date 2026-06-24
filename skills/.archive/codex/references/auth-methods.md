# Codex CLI Authentication Methods — Full Comparison

## Summary (v0.136.0, 2026-06)

| Method | Login Works? | `codex exec` Works? | Notes |
|--------|:---:|:---:|-------|
| OpenAI API Key (`--with-api-key`) | ✅ | ✅ | **Only working method for exec** |
| Device Auth (`--device-auth`) | ✅ | ❌ | All models rejected: "not supported with ChatGPT account" |
| Agent Identity JWT (`--with-access-token`) | ✅ | ❌ | 401 errors — wrong `aud` claim |

## Method A — OpenAI API Key (RECOMMENDED)

```bash
echo "sk-proj-..." | codex login --with-api-key
```

- Requires an OpenAI API key from https://platform.openai.com/api-keys
- NOT the same as an OpenRouter key
- Confirmed working model: `gpt-5.3-codex`
- Bypasses OAuth/device-auth entirely
- Store key securely: `chmod 600 ~/.codex/api_key.txt`

## Method B — Device Auth

```bash
codex login --device-auth
# Prints URL + one-time code (expires 15 min)
```

- **Login succeeds** but `codex exec` rejects ALL models
- Rate limited (429) if retried too fast — wait several minutes
- Only useful for `codex login status` verification
- Requires browser access to complete

## Method C — Agent Identity JWT

```bash
cat ~/.codex/agent-identity.token | codex login --with-access-token
```

- Token contains Ed25519 private key — treat as credential (chmod 600)
- Token `aud` claim is `codex-app-server`, but CLI needs `chatgpt.com/backend-api`
- Results in 401 errors on `codex exec`
- Token may be valid until ~2036 but is unusable with current CLI

## Config File (`~/.codex/config.toml`)

```toml
sandbox = "danger-full-access"
approvals = "never"
```

Even with these settings, the sandbox filesystem is read-only at the OS level. See SKILL.md for the workaround (run generated code on host).
