#!/bin/bash
# DreamHost to USB backup script
# Backs up mifeco.com to /mnt/usb_4tb/Mifeco_Web_Backup/

set -e

BACKUP_DIR="/mnt/usb_4tb/Mifeco_Web_Backup"
REMOTE_USER="dh_mwpxuu"
REMOTE_HOST="iad1-shared-b8-42.dreamhost.com"
REMOTE_PATH="/home/dh_mwpxuu/mifeco.com/"
ENV_FILE="$HOME/.hermes/.env"

# Extract password from .env
DH_PASS=$(grep "^DREAMHOST_PASSWORD=" "$ENV_FILE" 2>/dev/null | head -1 | sed 's/^[^=]*=//')

if [ -z "$DH_PASS" ]; then
    echo "ERROR: No DREAMHOST_PASSWORD found in $ENV_FILE"
    exit 1
fi

echo "=== MIFECO DreamHost Backup ==="
echo "Source: ${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_PATH}"
echo "Dest:   ${BACKUP_DIR}/"
echo "Time:   $(date)"
echo ""

mkdir -p "$BACKUP_DIR"

# Use sshpass for rsync
if ! which sshpass >/dev/null 2>&1; then
    echo "Installing sshpass..."
    sudo apt-get install -y sshpass
fi

sshpass -p "$DH_PASS" rsync -avz --compress-level=6 \
    -e "ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null" \
    "${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_PATH}" \
    "${BACKUP_DIR}/"

echo ""
echo "=== Backup Complete ==="
echo "Time: $(date)"
du -sh "${BACKUP_DIR}/"
find "${BACKUP_DIR}/" -type f | wc -l | xargs -I{} echo "Total files: {}"
