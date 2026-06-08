#!/bin/bash
# Hermes Backup Verification Script
# Performs integrity check of latest Hermes backup

set -e

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

echo "=== Hermes Backup Verification ==="

# Find latest backup
LATEST=$(ls -t "${BACKUP_DIR}"/hermes-*.tar.gz 2>/dev/null | head -1)
if [ -z "$LATEST" ]; then
    echo "ERROR: No backups found in ${BACKUP_DIR}/"
    exit 1
fi

echo "Latest backup: $LATEST"
echo "Size: $(du -h "$LATEST" | cut -f1)"
echo ""

# gzip integrity check
echo "=== gzip integrity check ==="
if gzip -t "$LATEST"; then
    echo "PASS"
else
    echo "FAIL"
    exit 1
fi
echo ""

# Spot-check contents (first 15 entries)
echo "=== Contents (first 15 entries) ==="
tar tzf "$LATEST" | head -15
echo ""

# Total entries
TOTAL_ENTRIES=$(tar tzf "$LATEST" | wc -l)
echo "Total entries: $TOTAL_ENTRIES"
echo ""

# Check for unusually small backups that might indicate failures
echo "=== Checking for corrupt/dwarf backups ==="
SMALL_BACKUPS=$(find "${BACKUP_DIR}" -name "hermes-*.tar.gz" -size -100c 2>/dev/null)
if [ -n "$SMALL_BACKUPS" ]; then
    echo "WARNING: Unusually small backups found:"
    echo "$SMALL_BACKUPS" | while read small_backup; do
        echo "  $small_backup ($(du -h "$small_backup" | cut -f1))"
    done
else
    echo "No unusually small backups found."
fi
echo ""

echo "Verification completed successfully."
exit 0