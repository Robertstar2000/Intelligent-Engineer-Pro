#!/usr/bin/env bash
#===============================================================================
# MIFECO Social Media Publisher — Cron Runner
# ============================================
# Publishes approved social media posts via the social-direct-publisher API.
# Designed to run from cron at 9:00 AM daily (after pipeline sync).
#
# Usage:
#   ./run-social-publisher.sh                  # Publish all approved posts
#   ./run-social-publisher.sh --dry-run        # Show what would be published
#   ./run-social-publisher.sh --status         # Show queue status
#   ./run-social-publisher.sh --generate       # Generate drafts from pipeline events
#===============================================================================
set -e

BASE_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SCRIPTS_DIR="$BASE_DIR/scripts"
DATA_DIR="$BASE_DIR/data"
STATE_FILE="$DATA_DIR/pipeline-state.json"
SOCIAL_DRAFTS_FILE="$DATA_DIR/social-publisher-drafts.json"
SOCIAL_PUBLISHER_URL="${SOCIAL_PUBLISHER_URL:-http://localhost:8000}"

ACTION="${1:-publish}"

echo "╔══════════════════════════════════════════════╗"
echo "║   MIFECO Social Media Publisher              ║"
echo "╚══════════════════════════════════════════════╝"
echo "  API: $SOCIAL_PUBLISHER_URL"
echo "  Action: $ACTION"
echo ""

case "$ACTION" in
    publish)
        echo "▶ Publishing all approved posts..."
        python3 "$SCRIPTS_DIR/social_publisher_client.py" --action publish_approved
        ;;
    dry-run)
        echo "▶ Dry run — listing approved posts that would be published..."
        python3 "$SCRIPTS_DIR/social_publisher_client.py" --action list_drafts --status approved
        ;;
    status)
        echo "▶ Social publisher queue status..."
        echo ""
        echo "  Drafts (pending approval):"
        python3 "$SCRIPTS_DIR/social_publisher_client.py" --action list_drafts --status pending_approval
        echo ""
        echo "  Approved (ready to publish):"
        python3 "$SCRIPTS_DIR/social_publisher_client.py" --action list_drafts --status approved
        echo ""
        echo "  Published:"
        python3 "$SCRIPTS_DIR/social_publisher_client.py" --action list_drafts --status published
        ;;
    generate)
        echo "▶ Generating social post drafts from pipeline events..."
        # Check for recently published books (books with ASIN but no social posts yet)
        if [ -f "$DATA_DIR/pipeline-books.json" ]; then
            echo "  Checking pipeline-books.json for new publications..."
            # This would be expanded to auto-detect new ASINs and generate posts
            echo "  (Auto-detection of new publications — implement as needed)"
        fi
        echo "  Use social_publisher_client.py --action book_launch for specific books"
        ;;
    *)
        echo "Unknown action: $ACTION"
        echo "Usage: $0 [--publish|--dry-run|--status|--generate]"
        exit 1
        ;;
esac

echo ""
echo "✅ Done"
