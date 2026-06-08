# Troubleshooting Log — Updated 2026-07-03

## MEMORY.md Drift Fix
**Symptom:** `memory(action='add')` fails with "Refusing to write MEMORY.md"
**Root cause:** `write_file` was used on MEMORY.md, bypassing memory tool's format tracking.
**Fix:** `cp MEMORY.md MEMORY.md.bak; rm -f MEMORY.md MEMORY.md.bak.* MEMORY.md.lock;` then re-add via `memory(action='add')`
**Lesson:** NEVER use `write_file`/`patch` on MEMORY.md or USER.md. Only the `memory` tool.

## `hermes config set` Mangles JSON-in-YAML
**Symptom:** List values become 1,500+ single-character fragments.
**Root cause:** YAML parser splits JSON string by commas.
**Fix:** Use `yaml.safe_load`/`yaml.dump` directly via Python.
**Lesson:** NEVER use `hermes config set` for list values.

## Patch Tool Leaves Orphaned Code
**Symptom:** `IndentationError: unexpected indent` after patching `gateway/run.py`.
**Root cause:** Patch replaced function signature but not body. Left duplicate lines.
**Fix:** Always verify syntax after patching: `python3 -m ast <file>`
**Lesson:** Always read the full affected region after patching to confirm clean replacement.

## Skills Disabled — Gateway Restart Required
**Symptom:** Token counts don't change after updating `skills.disabled`.
**Root cause:** Skills prompt cached in `.skills_prompt_snapshot.json`.
**Fix:** `rm -f ~/.hermes/.skills_prompt_snapshot.json` then `hermes gateway restart` from shell.

## Skill Name Mismatch
**Symptom:** Disabled skill still appears in system prompt.
**Root cause:** Name in disabled list didn't match frontmatter name exactly.
**Lesson:** Verify via `grep "^name:" ~/.hermes/skills/<skill>/SKILL.md`.

## auto_nap() Adaptive Cron Ticker
**What:** Cron ticker that extends interval from 60s → 30min after 10min idle.
**Where:** `gateway/run.py` → `auto_nap()` function (replaces `_start_cron_ticker`).
**Trigger:** Any inbound user message calls `_record_cron_activity()` → resets to 60s.
**Config:** `idle_after=600`, `idle_interval=1800`, `normal_interval=60` in `auto_nap()` call.
**House-keeping:** Uses wall-clock time (not tick counts) so cadences stay correct in idle mode.