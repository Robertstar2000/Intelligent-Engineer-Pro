#!/usr/bin/env bash
set -euo pipefail

# Convenience wrapper: scan the OpenClaw workspace skills directory.
#
# Usage:
#   ./scan_workspace_skills.sh
#   ./scan_workspace_skills.sh --use-behavioral
#   ./scan_workspace_skills.sh --format sarif --output results.sarif

ROOT="/home/bob/.openclaw/workspace/skills"

if ! command -v skill-scanner >/dev/null 2>&1; then
  echo "skill-scanner not found on PATH. Install first:" >&2
  echo "  python3 -m pip install --user cisco-ai-skill-scanner" >&2
  exit 2
fi

exec skill-scanner scan-all "$ROOT" --recursive "$@"
