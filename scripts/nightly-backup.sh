#!/bin/bash
# Nightly Hermes Backup Script
# Backs up ~/.hermes config + ~/books to /mnt/usb_4tb/backups/
# Then syncs to GitHub repo at ~/FL-Hermes

set -euo pipefail

# 0. Determine backup destination
if mountpoint -q /mnt/usb_4tb 2>/dev/null; then
    HERMES_BACKUP_DIR="/mnt/usb_4tb/backups"
    echo "USB drive detected — backing up to $HERMES_BACKUP_DIR"
else
    echo "ERROR: USB drive not mounted at /mnt/usb_4tb"
    echo "SKIPPED: USB drive not found — fallback not implemented for safety"
    exit 1
fi

TIMESTAMP=$(date +%Y%m%d-%H%M%S)
BACKUP_DIR="$HERMES_BACKUP_DIR/hermes-$TIMESTAMP"
LOGFILE="$HERMES_BACKUP_DIR/logs/backup-${TIMESTAMP}.log"
mkdir -p "$HERMES_BACKUP_DIR/logs"

echo "===== Backup started at $(date) =====" >> "$LOGFILE"

# 1. Create backup directory
mkdir -p "$BACKUP_DIR/.hermes" "$BACKUP_DIR/books"

# 2. Backup .hermes directory (exclude re-clonable repo and caches)
echo "Backing up .hermes..." | tee -a "$LOGFILE"
rsync -a --whole-file --timeout=60 \
  --exclude='hermes-agent' \
  --exclude='cache' \
  --exclude='image_cache' \
  --exclude='audio_cache' \
  --exclude='node' \
  --exclude='checkpoints' \
  --exclude='sandboxes' \
  --exclude='bin' \
  --exclude='state-snapshots' \
  /home/bob/.hermes/ "$BACKUP_DIR/.hermes/" >> "$LOGFILE" 2>&1
echo ".hermes backup completed" | tee -a "$LOGFILE"

# 3. Backup books directory
echo "Backing up books..." | tee -a "$LOGFILE"
BOOKS_SRC="/home/bob/books"
if [ -L "$BOOKS_SRC" ]; then
    BOOKS_SRC=$(readlink -f "$BOOKS_SRC")
fi
if [ -d "$BOOKS_SRC" ]; then
    rsync -a --whole-file --timeout=60 \
      --exclude="_archived_*" \
      --exclude="__pycache__" \
      --exclude="generated" \
      --exclude="*.pyc" \
      "$BOOKS_SRC/" "$BACKUP_DIR/books/" >> "$LOGFILE" 2>&1
    echo "Books backup completed" | tee -a "$LOGFILE"
else
    echo "No books directory found at $BOOKS_SRC — skipping" | tee -a "$LOGFILE"
fi

# 4. Compress with integrity check
echo "Compressing backup..." | tee -a "$LOGFILE"
tar czf "${BACKUP_DIR}.tar.gz" -C "$HERMES_BACKUP_DIR" "hermes-$TIMESTAMP" --remove-files >> "$LOGFILE" 2>&1

if [ ! -f "${BACKUP_DIR}.tar.gz" ]; then
    echo "ERROR: Backup archive was not created" | tee -a "$LOGFILE"
    exit 1
fi

echo "Verifying backup integrity..." | tee -a "$LOGFILE"
if gzip -t "${BACKUP_DIR}.tar.gz"; then
    echo "Backup integrity check passed." | tee -a "$LOGFILE"
else
    echo "ERROR: Backup integrity check FAILED" | tee -a "$LOGFILE"
    exit 1
fi

BACKUP_SIZE=$(du -h "${BACKUP_DIR}.tar.gz" | cut -f1)
echo "Backup archive: ${BACKUP_DIR}.tar.gz ($BACKUP_SIZE)" | tee -a "$LOGFILE"

# 5. Prune backups older than 30 days
THIRTY_DAYS_AGO=$(date -d "30 days ago" +%Y%m%d)
for backup in "$HERMES_BACKUP_DIR"/hermes-*.tar.gz; do
    [ -f "$backup" ] || continue
    bname=$(basename "$backup")
    bdate=$(echo "$bname" | sed -n 's/hermes-\([0-9]\{8\}\)-[0-9]\{6\}\.tar\.gz/\1/p')
    if [ -n "$bdate" ] && [ "$bdate" -lt "$THIRTY_DAYS_AGO" ]; then
        echo "Pruning old backup: $backup" | tee -a "$LOGFILE"
        rm -f "$backup"
    fi
done

# 6. GitHub sync (only if FL-Hermes repo exists)
FL_HERMES_DIR="/home/bob/FL-Hermes"
if [ -d "$FL_HERMES_DIR/.git" ]; then
    echo "Syncing to FL-Hermes GitHub repo..." | tee -a "$LOGFILE"
    cd "$FL_HERMES_DIR"

    rsync -av --delete --whole-file --timeout=60 \
      --exclude='.env' --exclude='auth.json' \
      --exclude='hermes-agent' --exclude='cache' \
      --exclude='image_cache' --exclude='audio_cache' \
      --exclude='node' --exclude='checkpoints' \
      --exclude='sandboxes' --exclude='bin' \
      --exclude='state-snapshots' \
      /home/bob/.hermes/ .hermes/ >> "$LOGFILE" 2>&1

    rsync -av --delete --whole-file --timeout=60 \
      --exclude='.git' \
      /home/bob/.hermes/skills/ skills/ >> "$LOGFILE" 2>&1

    rsync -av --delete --whole-file --timeout=60 \
      /home/bob/.hermes/scripts/ scripts/ >> "$LOGFILE" 2>&1

    rsync -av --delete --whole-file --timeout=60 \
      /home/bob/.hermes/cron/ cron/ >> "$LOGFILE" 2>&1

    rsync -av --delete --whole-file --timeout=60 \
      /home/bob/.hermes/memories/ memories/ >> "$LOGFILE" 2>&1

    rsync -av --delete --whole-file --timeout=60 \
      /home/bob/.hermes/mempalace/ mempalace/ >> "$LOGFILE" 2>&1

    rsync -av --delete --whole-file --timeout=60 \
      /home/bob/.hermes/pipeline-engine/ pipeline-engine/ >> "$LOGFILE" 2>&1

    rsync -av --delete --whole-file --timeout=60 \
      /home/bob/.hermes/consulting-reports/ consulting-reports/ >> "$LOGFILE" 2>&1

    git add -A
    if git diff --cached --quiet; then
        echo "No changes to commit" | tee -a "$LOGFILE"
    else
        COMMIT_MSG="Nightly backup: $(date +%Y-%m-%d)"
        git commit -m "$COMMIT_MSG" >> "$LOGFILE" 2>&1
        git push origin main >> "$LOGFILE" 2>&1 && \
            echo "GitHub push successful" | tee -a "$LOGFILE" || \
            echo "WARNING: GitHub push failed" | tee -a "$LOGFILE"
    fi
else
    echo "FL-Hermes repo not found — skipping GitHub sync" | tee -a "$LOGFILE"
fi

echo "===== Backup finished at $(date) =====" | tee -a "$LOGFILE"
echo "✅ Backup complete: ${BACKUP_DIR}.tar.gz ($BACKUP_SIZE)"
