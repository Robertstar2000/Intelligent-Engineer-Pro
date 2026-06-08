#!/bin/bash
# Delivery Queue Processor
# NOTE: This is a legacy compatibility script from the OpenClaw multi-agent era.
# The current Hermes agent does NOT use file-based delivery queuing.
# Cron jobs deliver directly to Telegram via the cronjob `deliver` field.
# This script is kept for backward compatibility only — the queue stays empty by design.
# See: hermes-agent uses delegate_task() for sub-agents and cronjob() for scheduling.

WORKSPACE="$HOME/.hermes/.openclaw"
QUEUE_DIR="$WORKSPACE/delivery-queue"
LOG_FILE="$WORKSPACE/logs/delivery-queue.log"

mkdir -p "$QUEUE_DIR/archive" "$QUEUE_DIR/processed" "$QUEUE_DIR/failed" "$(dirname "$LOG_FILE")"

timestamp() {
  date +"%Y-%m-%d %H:%M:%S"
}

log() {
  echo "[$(timestamp)] $1" >> "$LOG_FILE"
}

# Count actual delivery items (not subdirectories) — use find for reliability
ITEMS=$(find "$QUEUE_DIR" -maxdepth 1 -type f 2>/dev/null | wc -l)

if [ "$ITEMS" -eq 0 ] 2>/dev/null; then
  log "No pending items — queue empty (expected: current Hermes uses direct Telegram delivery)"
  exit 0
fi

log "Found $ITEMS items in delivery queue — processing legacy items..."
echo "$ITEMS"
