# Troubleshooting Notes from Session 2026-05-26

## Memory Limit Issues
- Memory reached 2,065/2,200 chars limit causing tool failures
- Specific error: "Memory at 2,065/2,200 chars. Adding this entry (272 chars) would exceed the limit"
- Another error: "Replacement would put memory at 2,305/2,200 chars"
- Solution: Clear outdated memory entries or increase limit in config.yaml

## Gateway Service Conflicts
- Both user and system gateway services installed causing confusion
- Message: "⚠ Both user and system gateway services are installed (user + system). This is confusing and can make start/stop/status behavior ambiguous."
- Solution: Keep only one service (user service preferred)
- Commands used:
  - `systemctl show hermes-gateway -p MainPID --value` to get PID
  - `kill -USR1 "$mainpid"` to restart gateway without sudo
  - `sudo hermes gateway uninstall --system` to remove system service

## Tool-Specific Errors
### browser_click Unknown Ref
- Error: "Tool browser_click returned error (0.47s): {\"success\": false, \"error\": \"Unknown ref: e5\"}"
- Likely cause: Attempting to click element without fresh snapshot after page changes
- Fix: Always call browser_snapshot after navigation/actions before clicking

### Execute Code Failures
- Multiple execute_code errors including:
  - Traceback about missing memory_path in MemPalace offload procedure
  - Various script execution failures
- Context: These occurred during automated memory maintenance procedures

### Skill Management Errors
- "Could not find a match for old_string in the file"
- "Found 2 matches for old_string. Provide more context to make it unique"
- "old_string and new_string are identical"
- Solutions: Increase specificity of old_string, use replace_all=True when appropriate, verify content before replacement

## Cron Job Status
- All cron jobs active as of session time
- One error: "Promotion Generation — Daily" job had "error: RuntimeError: Connection error."
- Most recent runs showed "ok" status for maintenance jobs

## Book Project Status
- "Tomorrow Remembered" appears published with artifacts:
  - EPUB, PDF, KDP package files
  - Cover images, description, keywords
  - No active source chapters in book_source/ directory
  - Likely in promotion/marketing phase

## Recommended Maintenance Actions
1. Run memory cleanup to free up space
2. Verify only one gateway service is active
3. Monitor the promotion generation cron job for recurring connection errors
4. Consider increasing memory limit if cleanup doesn't resolve issues