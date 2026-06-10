---
name: hermes-backup
description: Create a timestamped compressed backup of Hermes configuration, data, memories, skills, sessions, and state database, excluding the cloned hermes-agent repo and caches.
---


## 🔍 MemPalace Query (MANDATORY FIRST STEP)
Before proceeding, query MemPalace for existing context:
```python
import sys, os; sys.path.insert(0, os.path.expanduser('~/.hermes/mempalace'))
import embed; embed.init_embedding(os.path.expanduser('~/.hermes/mempalace'))
results = embed.search_embeddings("Hermes backup configuration data memories", k=5)
```
This retrieves previous decisions, domain-specific context, and lessons learned from the vector memory store.

# Hermes Backup Skill

Creates an automated backup of critical Hermes user data.

## Trigger

- Cron: nightly at 1:00 AM (`0 1 * * *`)
- Manual: `hermes backup`

## Backup Contents

The backup includes:
- `config.yaml`, `.env`, `auth.json`, `channel_directory.json`
- `SOUL.md`, `.hermes_history`, `gateway_state.json`
- `skills/`, `memories/`, `cron/`, `crontab/`, `plugins/`
- `scripts/`, `plans/`, `hooks/`, `agent/`
- `mempalace/`, `sessions/`, `logs/`
- `state.db`, `state.db-shm`, `state.db-wal`
- Model caches, embedding scripts
- `~/books/` — all book manuscripts, covers, EPUBs, PDFs, publishing packages

**Excluded:** `hermes-agent/` (repo — can re-clone), `cache/`, `image_cache/`, `audio_cache/`, `node/`, `checkpoints/`, `sandboxes/`, `bin/`

See `references/hermes-backup-dir-behavior.md` for details on HERMES_BACKUP_DIR behavior.

See `references/hermes-backup-dir-behavior.md` for details on HERMES_BACKUP_DIR behavior.

## Procedure

```bash
# 0. Determine backup destination
# If HERMES_BACKUP_DIR is explicitly set, use it directly (skipping auto-detection)
# Otherwise, auto-detect USB drive preference
# See references/hermes-backup-dir-behavior.md for detailed behavior
if [ -z "$HERMES_BACKUP_DIR" ]; then
    if mountpoint -q /mnt/usb_4tb 2>/dev/null; then
        HERMES_BACKUP_DIR="/mnt/usb_4tb/backups"
        echo "USB drive detected — backing up to $HERMES_BACKUP_DIR"
    else
        HERMES_BACKUP_DIR="$HOME/backups"
        echo "USB drive not found — backing up to $HERMES_BACKUP_DIR"
    fi
else
    echo "Using explicitly set backup directory: $HERMES_BACKUP_DIR"
fi

# 1. Create backup directory
BACKUP_DIR="$HERMES_BACKUP_DIR/hermes-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$BACKUP_DIR"

# 2. Backup .hermes directory with exclusions
# Exclude: hermes-agent (re-clonable), cache directories, node, checkpoints, sandboxes, bin, state-snapshots
DATA_DIR="$HOME/.hermes"
BACKUP_HERMES_DIR="$BACKUP_DIR/.hermes"
mkdir -p "$BACKUP_HERMES_DIR"
rsync -av \
  --exclude='hermes-agent' \
  --exclude='cache' \
  --exclude='image_cache' \
  --exclude='audio_cache' \
  --exclude='node' \
  --exclude='checkpoints' \
  --exclude='sandboxes' \
  --exclude='bin' \
  --exclude='state-snapshots' \
  "$DATA_DIR/" "$BACKUP_HERMES_DIR/"

# 3. Also back up book files (manuscripts, covers, EPUBs, PDFs)
# Note: ~/books may be a symlink to /mnt/usb_4tb/books — resolve it
BOOKS_SRC="$HOME/books"
if [ -L "$BOOKS_SRC" ]; then
    BOOKS_SRC=$(readlink -f "$BOOKS_SRC")
fi
if [ -d "$BOOKS_SRC" ]; then
    mkdir -p "$BACKUP_DIR/books"
    rsync -a "$BOOKS_SRC/" "$BACKUP_DIR/books/" --exclude="_archived_*" --exclude="__pycache__" --exclude="generated" --exclude="*.pyc"
fi

# 4. Compress
# Note: tar compression can take several minutes for large backups.
# If running in a timed context (e.g., cron), ensure timeout is sufficient (e.g., 600 seconds).
# Consider using background mode for automated backups to avoid timeout issues.
# Use the -C flag to change to the backups directory to avoid "Removing leading '/' from member names" warnings.
tar czf "${BACKUP_DIR}.tar.gz" -C "$HERMES_BACKUP_DIR" "$(basename "$BACKUP_DIR")" --remove-files

# Verify the archive was created successfully
if [ ! -f "${BACKUP_DIR}.tar.gz" ]; then
    echo "ERROR: Backup archive was not created"
    exit 1
fi
# Verify gzip integrity
echo "Verifying backup integrity..."
gzip -t "${BACKUP_DIR}.tar.gz" && echo "Backup integrity check passed." || { echo "ERROR: Backup integrity check failed."; exit 1; }

# 5. Prune backups older than 30 days
THIRTY_DAYS_AGO=$(date -d "30 days ago" +%Y%m%d)
for backup in "$HERMES_BACKUP_DIR"/hermes-*.tar.gz; do
  basename=$(basename "$backup")
  backup_date=$(echo "$basename" | sed -n 's/hermes-\\([0-9]\\{8\\}\\)-[0-9]\\{6\\}\\.tar\\.gz/\\1/p')
  if [ -n "$backup_date" ] && [ "$backup_date" -lt "$THIRTY_DAYS_AGO" ]; then
    rm "$backup"
  fi
done

echo "Backup complete: ${BACKUP_DIR}.tar.gz ($(du -h "${BACKUP_DIR}.tar.gz" | cut -f1))"

# 6. Optional: GitHub sync — push to FL-Hermes repo
# Only runs if FL-Hermes repo exists at ~/FL-Hermes
FL_HERMES_DIR="$HOME/FL-Hermes"
if [ -d "$FL_HERMES_DIR/.git" ]; then
  echo "Syncing to FL-Hermes GitHub repo..."
  cd "$FL_HERMES_DIR"

  # Sync all hermes files (excluding secrets)
  rsync -av --delete \
    --exclude='.env' --exclude='auth.json' \
    --exclude='hermes-agent' --exclude='cache' \
    --exclude='image_cache' --exclude='audio_cache' \
    --exclude='node' --exclude='checkpoints' \
    --exclude='sandboxes' --exclude='bin' \
    --exclude='state-snapshots' --exclude='.git' \
    "$DATA_DIR/" .hermes/

  rsync -av --delete --exclude='.git' "$DATA_DIR/skills/" skills/
  rsync -av --delete "$DATA_DIR/scripts/" scripts/
  rsync -av --delete "$DATA_DIR/cron/" cron/
  rsync -av --delete "$DATA_DIR/memories/" memories/
  rsync -av --delete "$DATA_DIR/mempalace/" mempalace/
  rsync -av --delete "$DATA_DIR/pipeline-engine/" pipeline-engine/
  rsync -av --delete "$DATA_DIR/consulting-reports/" consulting-reports/

  # Sync SaaS products if they exist
  if [ -d "$HOME/saas" ]; then
    rsync -av --delete --exclude='node_modules' --exclude='.git' \
      --exclude='dist' --exclude='database.sqlite' \
      "$HOME/saas/" saas/
  fi

  git add -A
  git diff --cached --quiet || git commit -m "Nightly backup: $(date +%Y-%m-%d)"
  git push origin main 2>&1 || echo "WARNING: GitHub push failed"
fi
```
- Must verify USB is mounted before running (`mountpoint /mnt/usb_4tb`)
- Excludes caches, trash, `node_modules`, `.cache`, etc.

## Pitfalls

- `rsync -a --relative` with absolute source paths (e.g., `/home/bob/.hermes/config.yaml`) creates the full path hierarchy inside the backup directory, making it hard to verify or restore. Use `cp -a` for files and plain `rsync -a` for directories instead — this keeps a simple flat `.hermes/` structure in the archive.
- The `tar` compression of a multi-GB backup directory can take 60–120 seconds. Use background mode or `-C` flag with relative paths to avoid the "Removing leading `/' from member names" warning.
- If the tar step times out (e.g., when using a timeout in automation), increase the timeout value or run the compression in the background and monitor completion.
- `.env` and `auth.json` contain API keys/secrets — backup is encrypted only by filesystem permissions. Keep the archive secure.
- The backup size varies significantly depending on the size of your ~/books directory (manuscripts, covers, EPUBs, PDFs). The .hermes directory (including state.db ~60MB) typically adds ~70MB compressed, but total backup size can range from ~100MB to several GB based on book collection size.
- **Default destination is now `/mnt/usb_4tb/backups/` when the USB drive is mounted.** The procedure auto-detects the USB drive via `mountpoint`. If the USB is not mounted, it falls back to `$HOME/backups/`. To override manually, set `HERMES_BACKUP_DIR` before running.
- **Always verify the USB is mounted** before running (`mountpoint /mnt/usb_4tb`). If the drive is not mounted, backups will silently land on the SSD — defeating the purpose.
- Do NOT back up the hermes-agent/ directory — it's 8.2GB and can be re-cloned from GitHub.
- Ensure sufficient free disk space on the destination before running (at least 2x expected backup size).
+ - The GitHub sync step (rsync) can take a long time for large .hermes directories and may time out in automated contexts. Consider increasing the timeout or running the sync in the background if using automation.
## Verification
- Unusually small backup files (e.g., 4K) may indicate a failed backup. Regularly check for these using the verification script or by scanning the backup directory for files significantly smaller than expected.
- **If `~/books` is a symlink** (e.g., to `/mnt/usb_4tb/books`), resolve it with `readlink -f` before rsync to avoid backing up the symlink itself.
- **When HERMES_BACKUP_DIR is explicitly set**, the skill uses that value directly without auto-detection. This ensures predictable behavior for cron jobs and automated backups. See `references/hermes-backup-dir-behavior.md` for details.

## Verification

You can run the verification script to check backup integrity:
```bash
hermes skills run hermes-backup:scripts/verify_backup.sh
```

Or manually:

```bash
## Verification

You can run the verification script to check backup integrity:
```bash
hermes skills run hermes-backup:scripts/verify_backup.sh
```

Or manually:

```bash
# Determine the active backup directory
# If HERMES_BACKUP_DIR is explicitly set, use it directly (skipping auto-detection)
# Otherwise, auto-detect USB drive preference
# See references/hermes-backup-dir-behavior.md for detailed behavior
if [ -z "$HERMES_BACKUP_DIR" ]; then
    if mountpoint -q /mnt/usb_4tb 2>/dev/null; then
        HERMES_BACKUP_DIR="/mnt/usb_4tb/backups"
    else
        HERMES_BACKUP_DIR="$HOME/backups"
    fi
fi

# Full integrity check of latest backup
LATEST=$(ls -t "$HERMES_BACKUP_DIR"/hermes-*.tar.gz 2>/dev/null | head -1)
if [ -n "$LATEST" ]; then
    echo "Checking: $LATEST"
    echo "Size: $(du -h "$LATEST" | cut -f1)"
    
    # gzip integrity check
    echo ""
    echo "=== gzip integrity ==="
    gzip -t "$LATEST" && echo "PASS" || echo "FAIL"
    
    # Spot-check contents
    echo ""
    echo "=== Contents (first 15 entries) ==="
    tar tzf "$LATEST" | head -15
    
    echo ""
    echo "Total entries: $(tar tzf "$LATEST" | wc -l)"
    
    # Check for any unusually small backups that might indicate failures
    echo ""
    echo "=== Checking for corrupt/dwarf backups ==="
    find "$HERMES_BACKUP_DIR" -name "hermes-*.tar.gz" -size -100c 2>/dev/null | while read small_backup; do
        echo "WARNING: Unusually small backup found: $small_backup ($(du -h "$small_backup" | cut -f1))"
    done
    echo "Done."
else
    echo "No backups found in $HERMES_BACKUP_DIR/"
fi
```