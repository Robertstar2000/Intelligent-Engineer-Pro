#!/bin/bash
# Weekly Home Backup Script
# Runs every Sunday at 2:00 AM
# All data and logs go directly to the 4TB USB drive

SOURCE="/home/bob"
DEST="/mnt/usb_4tb/backups/home-backup"
LOG_DIR="/mnt/usb_4tb/backups/logs"
TIMESTAMP=$(date +%Y-%m-%d_%H-%M-%S)
LOG="${LOG_DIR}/backup-${TIMESTAMP}.log"

# Verify USB is mounted
if ! mountpoint -q /mnt/usb_4tb; then
    echo "ERROR: /mnt/usb_4tb is not mounted. Aborting backup."
    exit 1
fi

mkdir -p "$LOG_DIR"

echo "===== Backup started at $(date) =====" >> "$LOG"

rsync -avh --delete \
  --exclude '.cache' \
  --exclude '.local/share/Trash' \
  --exclude 'node_modules' \
  --exclude '__pycache__' \
  --exclude '*.pyc' \
  --exclude '.npm' \
  --exclude '.yarn' \
  --exclude 'Downloads' \
  "$SOURCE/" "$DEST/" >> "$LOG" 2>&1

RC=$?
echo "===== Backup finished at $(date) with exit code $RC =====" >> "$LOG"

if [ $RC -eq 0 ]; then
  echo "✅ Home backup completed successfully on $(date). Log: $LOG"
else
  echo "❌ Home backup FAILED on $(date) with exit code $RC. Log: $LOG"
fi
