#!/bin/bash
# MIFECO Consulting API — Keep-alive script
# Add to cron: */5 * * * * /home/bob/.hermes/scripts/keep-consulting-api.sh

API_PORT=8190
API_DIR="/mnt/usb_4tb/consulting/api"
LOG="/tmp/consulting-api.log"

# Check if already running
if pgrep -f "api_server.py" > /dev/null 2>&1; then
    # Verify it's responding
    if curl -s -o /dev/null --max-time 3 http://localhost:${API_PORT}/ 2>/dev/null; then
        exit 0  # Running and healthy
    fi
fi

# Start it
cd "$API_DIR"
nohup python3 api_server.py >> "$LOG" 2>&1 &
echo "$(date): API server restarted (PID $!)" >> "$LOG"
