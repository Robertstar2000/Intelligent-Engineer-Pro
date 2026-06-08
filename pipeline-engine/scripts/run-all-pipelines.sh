#!/usr/bin/env bash
#===============================================================================
# MIFECO run-all-pipelines.sh
# ============================
# Master runner — refreshes pipeline state and outputs a structured report
# for each pipeline. Designed to run from cron safely (idempotent).
#
# Usage:
#   ./run-all-pipelines.sh                  # Full run
#   ./run-all-pipelines.sh --quiet          # Suppress banner
#   ./run-all-pipelines.sh --json-only      # Output JSON state at the end
#===============================================================================
set -e

BASE_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SCRIPTS_DIR="$BASE_DIR/scripts"
DATA_DIR="$BASE_DIR/data"
STATE_FILE="$DATA_DIR/pipeline-state.json"
DASHBOARD_DIR="$BASE_DIR/dashboard"
SYNC_SCRIPT="$SCRIPTS_DIR/pipeline-sync.py"

QUIET=false
JSON_ONLY=false

for arg in "$@"; do
    case "$arg" in
        --quiet) QUIET=true ;;
        --json-only) JSON_ONLY=true ;;
    esac
done

if [ "$QUIET" = false ]; then
    echo "╔══════════════════════════════════════════════╗"
    echo "║   MIFECO Pipeline Runner                     ║"
    echo "╚══════════════════════════════════════════════╝"
    echo ""
fi

# ── Step 1: Run pipeline-sync.py ─────────────────────────────────────────
echo "▶ Step 1/2: Refreshing pipeline data..."
python3 "$SYNC_SCRIPT"
SYNC_EXIT=$?

if [ $SYNC_EXIT -ne 0 ]; then
    echo ""
    echo "⚠ ERROR: pipeline-sync.py exited with code $SYNC_EXIT"
    exit $SYNC_EXIT
fi

# ── Step 2: Sync state to dashboard ─────────────────────────────────────
echo "▶ Step 2/3: Syncing to dashboard..."
cp "$STATE_FILE" "$DASHBOARD_DIR/pipeline-state.json"
echo "  ✓ pipeline-state.json → dashboard/"
echo ""

# ── Step 3: Read state and report ────────────────────────────────────────
echo ""
echo "▶ Step 3/3: Pipeline Status Report"

if [ ! -f "$STATE_FILE" ]; then
    echo "⚠ ERROR: $STATE_FILE not found after sync"
    exit 1
fi

# Extract and report using python3 for proper JSON parsing
python3 -c "
import json, sys

with open('$STATE_FILE') as f:
    state = json.load(f)

pipelines = state.get('pipelines', [])
cs = state.get('contentSummary', {})

print()
print('=' * 56)
print('  ALL PIPELINES STATUS REPORT')
print('=' * 56)
print()

for p in pipelines:
    health_icon = {'green': '🟢', 'yellow': '🟡', 'red': '🔴'}.get(p['health'], '⚪')
    status_icon = '▶' if p['status'] == 'running' else '⏸'
    bar_chars = int(p['pct'] / 10)
    bar = '█' * bar_chars + '░' * (10 - bar_chars)

    print(f'  {p[\"icon\"]} {p[\"name\"]}')
    print(f'     ID:        {p[\"id\"]}')
    print(f'     Status:    {status_icon} {p[\"status\"]}   Health: {health_icon} {p[\"health\"]}')
    print(f'     Progress:  [{bar}] {p[\"pct\"]}%')
    print(f'     Stage:     {p[\"currentStage\"]}/{len(p[\"stages\"])} ({p[\"stages\"][p[\"currentStage\"]-1]})')
    print(f'     Items:     {p[\"items\"]} total | {p[\"active\"]} active | {p[\"queued\"]} queued | {p[\"failed\"]} failed')
    print(f'     Threshold: {p[\"thresholds\"][\"monthlyTarget\"]}/mo target')
    print(f'     Cron:      {p[\"cronSchedule\"]} ({p[\"cronJob\"]})')
    print()

print('─' * 56)
print('  CONTENT COMMAND CENTER SUMMARY')
print('─' * 56)
print(f'  LinkedIn Messages: {cs.get(\"linkedin-msgs\", 0)}')
print(f'  Emails:            {cs.get(\"emails\", 0)}')
print(f'  Enrichment:        {cs.get(\"enrichment\", 0)}')
print(f'  X/Twitter Posts:   {cs.get(\"x-posts\", 0)}')
print(f'  Blog Posts:        {cs.get(\"blog-posts\", 0)}')
print(f'  LinkedIn Posts:    {cs.get(\"linkedin-posts\", 0)}')
print(f'  ─────────────────────────')
print(f'  Total:             {cs.get(\"totalItems\", 0)}')
print(f'  Sent:              {cs.get(\"sentItems\", 0)}')
print(f'  Approved:          {cs.get(\"approvedItems\", 0)}')
print(f'  Queued:            {cs.get(\"queuedItems\", 0)}')
print()

# Overall summary
running = sum(1 for p in pipelines if p['status'] == 'running')
paused = sum(1 for p in pipelines if p['status'] == 'paused')
green = sum(1 for p in pipelines if p['health'] == 'green')
yellow = sum(1 for p in pipelines if p['health'] == 'yellow')
red = sum(1 for p in pipelines if p['health'] == 'red')
total_items = sum(p['items'] for p in pipelines)
total_active = sum(p['active'] for p in pipelines)
total_queued = sum(p['queued'] for p in pipelines)
total_failed = sum(p['failed'] for p in pipelines)

print('=' * 56)
print('  OVERALL')
print('=' * 56)
print(f'  Pipelines: {len(pipelines)} ({running} running, {paused} paused)')
print(f'  Health:    {green} 🟢, {yellow} 🟡, {red} 🔴')
print(f'  Items:     {total_items} total | {total_active} active | {total_queued} queued | {total_failed} failed')
print(f'  Updated:   {state.get(\"updatedAt\", \"?\")}')
print()
" 2>&1 || echo "⚠ Report generation failed"

# ── JSON-only output ─────────────────────────────────────────────────────
if [ "$JSON_ONLY" = true ]; then
    echo ""
    echo "── JSON STATE ──"
    cat "$STATE_FILE"
fi

echo "✅ Done"