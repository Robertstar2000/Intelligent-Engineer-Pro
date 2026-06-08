# Skill scanning rules of thumb

Treat findings as signals, not verdicts.

Prioritize review when you see:
- Unnecessary network access (fetching remote prompts, webhooks, arbitrary URLs)
- Reading environment variables (API keys) without a clear reason
- File reads outside the workspace
- Shell execution (`exec`, `subprocess`, `os.system`) without strict allowlists
- “Prompt includes tool instructions” patterns (classic injection)

Good hygiene patterns:
- Explicit allowlists for hosts / commands
- Clear separation of data vs instructions
- Minimal permissions / least privilege
- No hidden telemetry
