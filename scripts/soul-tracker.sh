#!/bin/bash
SOUL_FILE="$HOME/.hermes/.openclaw/workspace/SOUL.md"
LOG_FILE="$HOME/.hermes/.openclaw/workspace/logs/soul-tracking.log"

# Ensure log directory exists
mkdir -p "$(dirname "$LOG_FILE")"

timestamp() {
  date +"%Y-%m-%d %H:%M:%S"
}

log() {
  echo "[$(timestamp)] $1" >> "$LOG_FILE"
}

# Track SOUL readiness indicators
if [ -f "$SOUL_FILE" ]; then
  # Extract key metrics from SOUL (use word-level matching)
  READINESS_SCORE=$(grep -i "ready\|prepared\|available\|operational" "$SOUL_FILE" | wc -l)
  BOUNDARIES_COUNT=$(grep -i "boundar\|limit\|restriction" "$SOUL_FILE" | wc -l)
  
  log "SOUL Readiness Check - Readiness indicators: $READINESS_SCORE, Boundaries defined: $BOUNDARIES_COUNT"
  
  # Update tracking entry in-place (replace existing section or append)
  TRACKING_LINE="## Last Tracking Update"
  TODAY_DATE="$(date)"
  TODAY_STATUS="Operational"
  
  if grep -q "$TRACKING_LINE" "$SOUL_FILE"; then
    # Update existing tracking section
    python3 -c "
import re
with open('$SOUL_FILE', 'r') as f:
    content = f.read()
# Replace the Last Tracking Update section
pattern = r'## Last Tracking Update\\n- Last checked: .*\\n- System status: .*'
replacement = '## Last Tracking Update\n- Last checked: $TODAY_DATE\n- System status: $TODAY_STATUS'
content = re.sub(pattern, replacement, content)
with open('$SOUL_FILE', 'w') as f:
    f.write(content)
" 2>/dev/null || {
    # Fallback: append
    echo "" >> "$SOUL_FILE"
    echo "$TRACKING_LINE" >> "$SOUL_FILE"
    echo "- Last checked: $TODAY_DATE" >> "$SOUL_FILE"
    echo "- System status: $TODAY_STATUS" >> "$SOUL_FILE"
  }
  else
    # First-time append
    echo "" >> "$SOUL_FILE"
    echo "$TRACKING_LINE" >> "$SOUL_FILE"
    echo "- Last checked: $TODAY_DATE" >> "$SOUL_FILE"
    echo "- System status: $TODAY_STATUS" >> "$SOUL_FILE"
  fi
  
  log "SOUL tracking updated for $(date)"
fi