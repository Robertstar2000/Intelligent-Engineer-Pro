#!/usr/bin/env bash
#===============================================================================
# MIFECO Dashboard Sync — Regenerate + Deploy
#
# Reads pipeline data, regenerates dashboard HTML with fresh embedded JSON,
# then rsyncs to mifeco.com /admin/ directory.
#
# Usage:
#   ./dashboard-sync.sh                    # Full sync
#   ./dashboard-sync.sh --dry-run          # Preview only
#   ./dashboard-sync.sh --keep-local       # Regenerate without upload
#   ./dashboard-sync.sh --webhook          # Notify mifeco.com via webhook
#===============================================================================
set -e

BASE_DIR="$(cd "$(dirname "$0")/.." && pwd)"
DATA_DIR="$BASE_DIR/data"
DASHBOARD_DIR="$BASE_DIR/dashboard"
SSH_USER="dh_mwpxuu"
SSH_HOST="IAD1-SHARED-B8-42.DREAMHOST.COM"
SSH_TARGET="/home/dh_mwpxuu/mifeco.com/admin/"
SSH_PASS="Rm2214ri####"

DRY_RUN=false
KEEP_LOCAL=false
USE_WEBHOOK=false

for arg in "$@"; do
    case "$arg" in
        --dry-run) DRY_RUN=true ;;
        --keep-local) KEEP_LOCAL=true ;;
        --webhook) USE_WEBHOOK=true ;;
    esac
done

echo "╔══════════════════════════════════════════════════╗"
echo "║     MIFECO Dashboard Sync                       ║"
echo "╚══════════════════════════════════════════════════╝"
echo ""
echo "  Data dir:      $DATA_DIR"
echo "  Dashboard dir: $DASHBOARD_DIR"
echo "  Target:        ${SSH_USER}@${SSH_HOST}:${SSH_TARGET}"
echo ""

# Verify data files exist
for f in pipeline-saas.json pipeline-books.json pipeline-consulting.json leads-registry.json unified-pipeline.json; do
    if [ ! -f "$DATA_DIR/$f" ]; then
        echo "⚠ WARNING: $DATA_DIR/$f not found"
    else
        size=$(wc -c < "$DATA_DIR/$f")
        echo "  ✓ $f ($size bytes)"
    fi
done

# Check dashboard files
for f in index.php pipeline-dashboard.html content-command-center.html webhook.php .htaccess; do
    if [ -f "$DASHBOARD_DIR/$f" ]; then
        size=$(wc -c < "$DASHBOARD_DIR/$f")
        echo "  ✓ dashboard/$f ($size bytes)"
    else
        echo "⚠ WARNING: $DASHBOARD_DIR/$f not found"
    fi
done

echo ""

if [ "$DRY_RUN" = true ]; then
    echo "⏸ DRY RUN — No files will be transferred"
    echo ""
    echo "Files that would be synced:"
    for f in index.php pipeline-dashboard.html content-command-center.html webhook.php .htaccess; do
        if [ -f "$DASHBOARD_DIR/$f" ]; then
            echo "  → $SSH_TARGET$f"
        fi
    done
    echo "  → $SSH_TARGET data/ (if exists)"
    exit 0
fi

# Upload to server
if [ "$KEEP_LOCAL" = false ]; then
    echo "📤 Syncing to $SSH_HOST..."
    
    # Use rsync over SSH with password via sshpass (if available)
    UPLOAD_CMD="rsync -avz --rsh=\"ssh -o StrictHostKeyChecking=accept-new\" \
        $DASHBOARD_DIR/ ${SSH_USER}@${SSH_HOST}:${SSH_TARGET}"
    
    # Check if sshpass is available for non-interactive password
    if command -v sshpass &>/dev/null; then
        export SSHPASS="$SSH_PASS"
        sshpass -e rsync -avz --rsh="ssh -o StrictHostKeyChecking=accept-new" \
            "$DASHBOARD_DIR/" "${SSH_USER}@${SSH_HOST}:${SSH_TARGET}"
    else
        # Try with pexpect via Python
        python3 -c "
import pexpect, sys, os
child = pexpect.spawn('rsync', [
    '-avz',
    '--rsh=ssh -o StrictHostKeyChecking=accept-new',
    '${DASHBOARD_DIR}/',
    '${SSH_USER}@${SSH_HOST}:${SSH_TARGET}'
], timeout=60)
child.expect_exact('password:')
child.sendline('${SSH_PASS}')
child.expect(pexpect.EOF)
print(child.before.decode())
"
    fi
    
    echo "✅ Sync complete"
fi

# Trigger webhook
if [ "$USE_WEBHOOK" = true ]; then
    echo "📡 Triggering webhook..."
    WEBHOOK_URL="https://mifeco.com/admin/webhook.php"
    
    python3 -c "
import urllib.request, json
data = json.dumps({'secret': 'Rm2214ri####', 'action': 'refresh'}).encode()
req = urllib.request.Request('$WEBHOOK_URL', data=data, 
    headers={'Content-Type': 'application/json'})
resp = urllib.request.urlopen(req)
print('Webhook response:', resp.read().decode())
" 2>&1 || echo "⚠ Webhook failed (dashboard still synced)"
fi

echo ""
echo "✅ Done — https://mifeco.com/admin/"
