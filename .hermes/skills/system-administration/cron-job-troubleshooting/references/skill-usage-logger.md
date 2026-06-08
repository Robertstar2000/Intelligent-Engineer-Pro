# Skill Usage Logger — Known Issues

## `NEW_ENTRIES` Always Shows 0

The auto-scan script increments `NEW_ENTRIES` inside piped `while` loops (Methods 1 and 2), which run in a subshell. The parent shell never sees the increments, so `New: $NEW_ENTRIES` in the summary line is always 0 — even when entries ARE successfully written to the log.

The fix is to replace pipe-to-while with process substitution:
```bash
# Before (broken — subshell, counter lost):
python3 -c "..." 2>/dev/null | while IFS= read -r line; do
  NEW_ENTRIES=$((NEW_ENTRIES + 1))  # Lost
done

# After (fixed — current shell, counter works):
while IFS= read -r line; do
  NEW_ENTRIES=$((NEW_ENTRIES + 1))  # Propagates
done < <(python3 -c "..." 2>/dev/null)
```

Same fix applies to the `find ... | while read -r outfile` block in Method 2.

## Running the Scan Manually

```bash
bash ~/.hermes/scripts/skill-usage-logger.sh auto-scan
bash ~/.hermes/scripts/skill-usage-logger.sh --stats   # Analytics
```

## Auto-Nap Interaction

The cron ticker now uses `auto_nap()` which extends the tick interval to 30 minutes during idle periods (10+ minutes without user activity). This means cron jobs fire less frequently when the system is idle. Jobs are NOT skipped — they just run on a longer interval. When user input arrives, the ticker immediately resumes 60-second ticks.

If a cron job seems to have "missed" a run, check whether the system was in idle mode. The job will fire on the next tick after the idle period ends or after user activity resets the timer.