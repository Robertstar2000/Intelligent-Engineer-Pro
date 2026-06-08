#!/bin/bash
"""
MemPalace Maintenance Wrapper Script
Runs consolidation, pruning, and reports system statistics
"""

# Configuration
MEMPALACE_DIR="$HOME/.hermes/mempalace"
LOG_DIR="$MEMPALACE_DIR/logs"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
LOG_FILE="$LOG_DIR/maintenance_$TIMESTAMP.log"

# Create log directory
mkdir -p "$LOG_DIR"

# Log function
log() {
    echo "[$(date +"%Y-%m-%d %H:%M:%S")] $1" | tee -a "$LOG_FILE"
}

log "Starting MemPalace maintenance"

# Change to MemPalace directory
cd "$MEMPALACE_DIR" || { log "ERROR: Cannot change to $MEMPALACE_DIR"; exit 1; }

# Run Python maintenance script
log "Running Python maintenance script..."
python3 "$MEMPALACE_DIR/scripts/cron_maintenance.py" 2>&1 | tee -a "$LOG_FILE"

# Get exit status
EXIT_STATUS=${PIPESTATUS[0]}

if [ $EXIT_STATUS -eq 0 ]; then
    log "MemPalace maintenance completed successfully"
else
    log "MemPalace maintenance failed with exit code $EXIT_STATUS"
fi

log "Maintenance finished. Log saved to: $LOG_FILE"

exit $EXIT_STATUS