#!/usr/bin/env bash
set -euo pipefail

# Run the Cisco skill-scanner from the vendored repo copy (no pip install).
#
# Usage:
#   ./scan_vendor_repo.sh /path/to/skill
#   ./scan_vendor_repo.sh /path/to/skills --all
#
# Notes:
# - This uses Python module execution with PYTHONPATH pointed at the vendored repo.
# - The repo still has dependencies; if missing, Python will error. In that case,
#   prefer installing the official package:
#     python3 -m pip install --user cisco-ai-skill-scanner

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_ROOT="${1:-}"
MODE="${2:-}"

if [[ -z "$SKILL_ROOT" ]]; then
  echo "Usage: $0 /path/to/skill [--all]" >&2
  exit 2
fi

REPO_DIR="/home/bob/.openclaw/workspace/vendor/skill-scanner-main"
if [[ ! -d "$REPO_DIR/skill_scanner" ]]; then
  echo "Vendored repo not found at: $REPO_DIR" >&2
  exit 2
fi

export PYTHONPATH="$REPO_DIR:${PYTHONPATH:-}"

if [[ "$MODE" == "--all" ]]; then
  python3 -m skill_scanner.cli.cli scan-all "$SKILL_ROOT" --recursive
else
  python3 -m skill_scanner.cli.cli scan "$SKILL_ROOT"
fi
