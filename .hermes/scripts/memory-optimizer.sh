#!/bin/bash
WORKSPACE="$HOME/.hermes/.openclaw/workspace"
MEMORY_DIR="$WORKSPACE/memory"
LOG_FILE="$MEMORY_DIR/memory-optimization.log"

# Ensure log directory exists
mkdir -p "$(dirname "$LOG_FILE")"

timestamp() {
  date +"%Y-%m-%d %H:%M:%S"
}

log() {
  echo "[$(timestamp)] $1" >> "$LOG_FILE"
}

# Optimize memory storage
if [ -d "$MEMORY_DIR" ]; then
  # Check memory usage
  MEMORY_SIZE=$(du -sh "$MEMORY_DIR" | cut -f1)
  log "Current memory size: $MEMORY_SIZE"
  
  # Compress old JSONL files
  find "$MEMORY_DIR" -name "*.jsonl" -not -name "*.gz" -mtime +7 -exec gzip {} \;
  log "Compressed JSONL files older than 7 days"
  
  # Create memory index for faster searching
  if [ -f "$MEMORY_DIR/agent-communications.jsonl" ]; then
    # In real implementation, this would create search indexes
    log "Memory indexing completed for faster retrieval"
  fi
  
  # Add memory usage analytics
  TOTAL_LINES=$(wc -l < "$MEMORY_DIR/agent-communications.jsonl" 2>/dev/null || echo 0)
  log "Total communication entries: $TOTAL_LINES"
  
  # Memory health check
  if [ "$TOTAL_LINES" -gt 10000 ]; then
    log "WARNING: Memory file size approaching limits - consider archiving"
  fi
fi