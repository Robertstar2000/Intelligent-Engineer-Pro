#!/usr/bin/env bash
"""
Cron job script for MemPalace maintenance tasks.
Run scoring and consolidation periodically.
"""
set -euo pipefail

LOGS_DIR="$HOME/.hermes/mempalace/logs"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
LOG_FILE="$LOGS_DIR/mempalace_${TIMESTAMP}.log"

# Create logs directory
mkdir -p "$LOGS_DIR"

{
    echo "=== MemPalace Maintenance Started: $(date) ==="
    echo
    
    # Run scoring on new raw memories
    echo "Step 1: Scoring new memory events..."
    python3 "$HOME/.hermes/mempalace/bin/score.py"
    echo "Scoring complete."
    echo
    
    # Run consolidation for memories scoring above threshold
    echo "Step 2: Consolidating high-value memories..."
    python3 "$HOME/.hermes/mempalace/bin/consolidate.py" 0.7
    echo "Consolidation complete."
    echo
    
    # Optional: Run reinforcement based on recent usage (would need tracking)
    # echo "Step 3: Applying reinforcement decay..."
    # python3 "$HOME/.hermes/mempalace/bin/reinforce.py" --decay
    # echo "Reinforcement complete."
    # echo
    
    # Light pruning (remove very old, low-value memories)
    echo "Step 4: Light pruning of old low-value memories..."
    python3 "$HOME/.hermes/mempalace/bin/prune.py" --max-age 730 --min-value 0.1  # 2 years, very low threshold
    echo "Pruning complete."
    echo
    
    echo "=== MemPalace Maintenance Finished: $(date) ==="
} 2>&1 | tee "$LOG_FILE"

# Keep only recent logs (last 30 days)
find "$LOGS_DIR" -name "mempalace_*.log" -mtime +30 -delete 2>/dev/null || true

exit 0