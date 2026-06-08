#!/bin/bash
# Agent Heartbeat Enhancer
# NOTE: This is a legacy compatibility script from the OpenClaw multi-agent era.
# The current Hermes agent does NOT use file-based inter-agent communication.
# It uses delegate_task() for live sub-agents and cronjob() with built-in delivery.
# This script is kept for backward compatibility only.
#
# The agent-communications.jsonl file is a historical record, not an active queue.
# Delivery-queue is intentionally always empty — cron jobs deliver directly via Telegram.

WORKSPACE="$HOME/.hermes/.openclaw"
COMM_FILE="$WORKSPACE/memory/agent-communications.jsonl"
HEARTBEAT_LOG="$WORKSPACE/logs/agent-heartbeat.log"

mkdir -p "$(dirname "$HEARTBEAT_LOG")"

timestamp() {
  date +"%Y-%m-%d %H:%M:%S"
}

log() {
  echo "[$(timestamp)] $1" >> "$HEARTBEAT_LOG"
}

# Only write heartbeat if communications file exists (legacy compatibility)
if [ -f "$COMM_FILE" ]; then
  QUEUE_COUNT=$(find "$WORKSPACE/delivery-queue/" -maxdepth 1 -type f 2>/dev/null | wc -l)
  
  cat >> "$COMM_FILE" << HEARTBEAT_ENHANCE
{
  "timestamp": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "task_id": "heartbeat-enhanced-$(date +%s)",
  "from": "system",
  "to": "all",
  "type": "status",
  "task": "System heartbeat — legacy compatibility ping",
  "payload": {
    "agents_active": 1,
    "communication_channels": ["telegram"],
    "file_based_queue_depth": $QUEUE_COUNT,
    "note": "File-based inter-agent communication is legacy. Active agent uses direct Telegram delivery.",
    "system_health": "optimal"
  },
  "status": "completed"
}
HEARTBEAT_ENHANCE
  log "Heartbeat logged to legacy agent-communications.jsonl (queue: $QUEUE_COUNT)"
else
  log "Legacy communications file not found — heartbeat skipped"
fi
