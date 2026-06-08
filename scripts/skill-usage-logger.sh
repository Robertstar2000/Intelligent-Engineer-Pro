#!/bin/bash
# Skill Usage Logger — manual log + auto-scan + analytics
# Usage:
#   skill-usage-logger.sh log <skill-name> [context]   # Manual log entry
#   skill-usage-logger.sh auto-scan                     # Auto-detect skills from cron jobs + session history
#   skill-usage-logger.sh (no args)                     # Show analytics

LOG_FILE="$HOME/.hermes/logs/skill-usage.log"
SKILL_DIR="$HOME/.hermes/skills"
CRON_JOBS="$HOME/.hermes/cron/jobs.json"
CRON_OUTPUT="$HOME/.hermes/cron/output"
TODAY=$(date +%Y-%m-%d)

mkdir -p "$(dirname "$LOG_FILE")"

timestamp() {
  date +"%Y-%m-%d %H:%M:%S"
}

log_skill_usage() {
  local SKILL_NAME="$1"
  local CONTEXT="${2:-auto-detected}"
  echo "[$(timestamp)] SKILL_USED: $SKILL_NAME | CONTEXT: $CONTEXT" >> "$LOG_FILE"
}

# Manual log mode
if [ "$1" = "log" ] && [ -n "$2" ]; then
  log_skill_usage "$2" "$3"
  exit 0
fi

# Auto-scan mode — detect skills from cron jobs and session activity
if [ "$1" = "auto-scan" ]; then
  echo "[$(timestamp)] SKILL_AUTO_SCAN: Starting daily skill usage scan" >> "$LOG_FILE"
  NEW_ENTRIES=0

  # Method 1: Scan cron jobs for skills attached to jobs that ran today
  if [ -f "$CRON_JOBS" ]; then
    python3 -c "
import json, datetime

today = datetime.date.today().isoformat()
with open('$CRON_JOBS') as f:
    data = json.load(f)

for job in data.get('jobs', []):
    last_run = job.get('last_run_at', '')
    # Check if job ran today
    if last_run and last_run.startswith(today):
        skills = job.get('skills', []) or []
        if job.get('skill'):
            skills.append(job['skill']) if job['skill'] not in skills else None
        for skill in skills:
            print(f'SKILL_USED: {skill} | CONTEXT: Cron job \"{job.get(\"name\", \"unknown\")}\"')
    " 2>/dev/null | while IFS= read -r line; do
      # Check if already logged today
      SKILL_NAME=$(echo "$line" | sed 's/.*SKILL_USED: //;s/ | CONTEXT:.*//')
      if ! grep -q "$TODAY.*SKILL_USED: $SKILL_NAME" "$LOG_FILE" 2>/dev/null; then
        echo "[$(timestamp)] $line" >> "$LOG_FILE"
        echo "  → Logged: $SKILL_NAME"
        NEW_ENTRIES=$((NEW_ENTRIES + 1))
      fi
    done
  fi

  # Method 2: Scan cron output directory for recent runs mentioning skill_view
  if [ -d "$CRON_OUTPUT" ]; then
    find "$CRON_OUTPUT" -name "*.txt" -newer "$LOG_FILE" 2>/dev/null | while read -r outfile; do
      while IFS= read -r line; do
        if echo "$line" | grep -q "skill_view\|skill_manage\|SKILL_USED\|loaded skill"; then
          SKILL=$(echo "$line" | grep -oP '(?:skill_view\(|skill_manage\(|SKILL_USED: |loaded skill )"?([a-zA-Z0-9_-]+)' | head -1)
          [ -n "$SKILL" ] && {
            if ! grep -q "$TODAY.*SKILL_USED: $SKILL" "$LOG_FILE" 2>/dev/null; then
              echo "[$(timestamp)] SKILL_USED: $SKILL | CONTEXT: auto-scan from cron output" >> "$LOG_FILE"
              echo "  → Logged: $SKILL (from cron output)"
              NEW_ENTRIES=$((NEW_ENTRIES + 1))
            fi
          }
        fi
      done < "$outfile"
    done
  fi

  # Method 3: List all known skills (just count them for analytics)
  SKILL_COUNT=0
  if [ -d "$SKILL_DIR" ]; then
    SKILL_COUNT=$(find "$SKILL_DIR" -name "SKILL.md" -type f | wc -l)
  fi

  TOTAL=$(wc -l < "$LOG_FILE" 2>/dev/null || echo 0)
  TODAY_COUNT=$(grep -c "$TODAY" "$LOG_FILE" 2>/dev/null || echo 0)

  echo "[$(timestamp)] SKILL_AUTO_SCAN: Complete. Total skills tracked: $TOTAL | Today: $TODAY_COUNT | New: $NEW_ENTRIES | Available skills: $SKILL_COUNT" >> "$LOG_FILE"
  exit 0
fi

# Analytics mode (no args or --stats)
if [ $# -eq 0 ] || [ "$1" = "--stats" ] || [ "$1" = "stats" ]; then
  if [ -f "$LOG_FILE" ]; then
    echo "=== Skill Usage Analytics ==="
    echo "Total skill usages: $(wc -l < "$LOG_FILE")"
    echo ""
    echo "Top most used skills:"
    awk -F'SKILL_USED: ' '{print $2}' "$LOG_FILE" | cut -d'|' -f1 | sort | uniq -c | sort -nr | head -10
    echo ""
    echo "Usage by hour (last 24h):"
    awk -F'[ \\[\\]]' '{print $2}' "$LOG_FILE" | cut -d: -f1 | sort | uniq -c | sort -n
    echo ""
    echo "Today's entries ($TODAY):"
    grep "$TODAY" "$LOG_FILE" || echo "  (none)"
    echo ""
    echo "Available skills:"
    if [ -d "$SKILL_DIR" ]; then
      find "$SKILL_DIR" -name "SKILL.md" -type f | sed 's|.*/skills/||;s|/SKILL.md||' | sort
    fi
  else
    echo "No skill usage log found"
  fi
  exit 0
fi

echo "Usage: $0 {log <skill> [context]|auto-scan|--stats}"
exit 1
