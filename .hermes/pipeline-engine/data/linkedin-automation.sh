#!/usr/bin/env bash
# ===================================================================
# MIFECO — LinkedIn Discovery Automation
# Pipeline Engine · Lead Generation Helper
# ===================================================================
set -euo pipefail

VERSION="1.0.0"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DATA_DIR="${SCRIPT_DIR}"
LEADS_FILE="${DATA_DIR}/discovered-leads.json"
BROWSER=""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# ── Helpers ──────────────────────────────────────────────────────────

log()   { echo -e "${GREEN}[✓]${NC} $1"; }
warn()  { echo -e "${YELLOW}[!]${NC} $1"; }
err()   { echo -e "${RED}[✗]${NC} $1"; }
info()  { echo -e "${CYAN}[i]${NC} $1"; }
hr()    { echo -e "${CYAN}─────────────────────────────────────────────${NC}"; }

detect_browser() {
  if command -v google-chrome &>/dev/null; then
    BROWSER="google-chrome"
  elif command -v google-chrome-stable &>/dev/null; then
    BROWSER="google-chrome-stable"
  elif command -v chromium-browser &>/dev/null; then
    BROWSER="chromium-browser"
  elif command -v chromium &>/dev/null; then
    BROWSER="chromium"
  elif command -v firefox &>/dev/null; then
    BROWSER="firefox"
  elif command -v brave-browser &>/dev/null; then
    BROWSER="brave-browser"
  else
    return 1
  fi
}

save_lead() {
  # Append a lead to discovered-leads.json
  local name="$1"
  local title="$2"
  local company="$3"
  local linkedin_url="${4:-}"
  local has_email="${5:-false}"
  local notes="${6:-}"

  # Create file with empty array if it doesn't exist
  if [ ! -f "$LEADS_FILE" ]; then
    echo '[]' > "$LEADS_FILE"
  fi

  # Check for duplicates (by name+company)
  if jq -e --arg n "$name" --arg c "$company" \
    '.[] | select(.name == $n and .company == $c)' "$LEADS_FILE" &>/dev/null; then
    warn "Duplicate lead: $name @ $company — skipping."
    return 1
  fi

  jq \
    --arg name "$name" \
    --arg title "$title" \
    --arg company "$company" \
    --arg url "$linkedin_url" \
    --arg email "$has_email" \
    --arg notes "$notes" \
    --arg ts "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
    '. += [{
      name: $name,
      title: $title,
      company: $company,
      linkedin_url: $url,
      has_email: ($email == "true"),
      notes: $notes,
      created_at: $ts
    }]' "$LEADS_FILE" > "${LEADS_FILE}.tmp" && mv "${LEADS_FILE}.tmp" "$LEADS_FILE"

  log "Saved lead: $name — $title @ $company"
}

list_leads() {
  if [ ! -f "$LEADS_FILE" ]; then
    warn "No leads file found at $LEADS_FILE"
    return
  fi
  local count
  count=$(jq 'length' "$LEADS_FILE")
  if [ "$count" -eq 0 ]; then
    info "No leads recorded yet."
    return
  fi
  echo ""
  info "Discovered Leads ($count total):"
  hr
  jq -r '.[] | "  \(.name) | \(.title) | \(.company) \(if .has_email then "✉️" else "" end)"' "$LEADS_FILE"
  hr
  echo ""
}

# ── Header ───────────────────────────────────────────────────────────

clear
cat << "EOF"
  __  __ ___ _____ _____ ___   ___   ___   ___   ___
 |  \/  |_ _|  ___|  ___/ _ \ / __| / _ \ / _ \ / __|
 | |\/| || || |_  | |_ | | | | (__ | (_) | (_) | (__
 |_|  |_|___|_|   |_|   \___/ \___| \___/ \___/ \___|

  LinkedIn Discovery Automation — Pipeline Engine v1.0
EOF
echo ""

# ── Step 1: Check Browser ────────────────────────────────────────────

echo -e "${CYAN}═══ Step 1: Browser Check ═══════════════════════════════${NC}"

if detect_browser; then
  log "Browser detected: $BROWSER"
else
  warn "No supported browser found. You can still use the search URLs manually."
  BROWSER=""
fi

# ── Step 2: Open LinkedIn Connections ────────────────────────────────

echo ""
echo -e "${CYAN}═══ Step 2: Open LinkedIn ═══════════════════════════════${NC}"

if [ -n "$BROWSER" ]; then
  log "Opening LinkedIn connections page..."
  "$BROWSER" "https://www.linkedin.com/mynetwork/invite-connect/connections/" 2>/dev/null &
  log "LinkedIn connections page opened in $BROWSER."
else
  warn "No browser available. Open this URL manually:"
  echo "  https://www.linkedin.com/mynetwork/invite-connect/connections/"
fi

# ── Step 3: Search Instructions ──────────────────────────────────────

echo ""
echo -e "${CYAN}═══ Step 3: Search & Filter Instructions ════════════════${NC}"
echo ""
cat << "EOF"
  📋 HOW TO FIND & CONNECT WITH TARGET LEADS:

  1. Go to LinkedIn search bar (top of page)

  2. Enter one of these role keywords:
     • CTO / Chief Technology Officer
     • VP Engineering / Vice President Engineering
     • CEO / Chief Executive Officer
     • Head of Product / VP Product
     • Founder / Co-Founder
     • Operations Director / Director of Operations

  3. ADD FILTERS (click "All filters"):
     • Location:  [your target city/region/country]
     • Industry:  SaaS, Technology, Information Technology, Consulting
     • Company:   [target companies if applicable]
     • Connections: 2nd (warmer outreach)

  4. BROWSE profiles and look for:
     • Mutual connections
     • Shared interests or groups
     • Recent posts or activity
     • Company size and growth signals

  5. CLICK "Connect" and select "Add a note"
     → Use the note templates from the HTML guide

  6. SAVE each lead using:
     save-lead "Full Name" "Job Title" "Company" "LinkedIn URL" "has_email" "notes"

     Example:
     save-lead "Jane Smith" "CTO" "Acme Corp" "https://linkedin.com/in/janesmith" false "Mutual connection: John D."

EOF

# ── Step 4: Quick Search URLs ────────────────────────────────────────

echo -e "${CYAN}═══ Step 4: Quick Search Links ═══════════════════════════${NC}"
echo ""
echo "  Pre-built LinkedIn search URLs for each target role:"
echo ""

SEARCH_URLS=(
  "CTO SaaS:https://www.linkedin.com/search/results/people/?keywords=CTO%20SaaS%20technology&origin=GLOBAL_SEARCH_HEADER"
  "VP Engineering:https://www.linkedin.com/search/results/people/?keywords=VP%20Engineering%20SaaS&origin=GLOBAL_SEARCH_HEADER"
  "CEO SaaS/Consulting:https://www.linkedin.com/search/results/people/?keywords=CEO%20SaaS%20consulting&origin=GLOBAL_SEARCH_HEADER"
  "Head of Product:https://www.linkedin.com/search/results/people/?keywords=Head%20of%20Product%20SaaS&origin=GLOBAL_SEARCH_HEADER"
  "Founder Startup:https://www.linkedin.com/search/results/people/?keywords=Founder%20startup%20technology&origin=GLOBAL_SEARCH_HEADER"
  "Operations Director:https://www.linkedin.com/search/results/people/?keywords=Operations%20Director%20consulting&origin=GLOBAL_SEARCH_HEADER"
)

i=1
for entry in "${SEARCH_URLS[@]}"; do
  label="${entry%%:*}"
  url="${entry#*:}"
  echo "  [$i] $label"
  echo "      $url"
  echo ""
  i=$((i + 1))
done

echo "  To open a search in your browser, use:"
echo "    open_search <number>"
echo ""

# ── Step 5: Open a search URL ────────────────────────────────────────

open_search() {
  local idx="$1"
  if [ -z "$idx" ] || [ "$idx" -lt 1 ] || [ "$idx" -gt "${#SEARCH_URLS[@]}" ]; then
    err "Invalid search number. Use 1-6."
    return 1
  fi
  local entry="${SEARCH_URLS[$((idx - 1))]}"
  local label="${entry%%:*}"
  local url="${entry#*:}"

  if [ -n "$BROWSER" ]; then
    "$BROWSER" "$url" 2>/dev/null &
    log "Opened search [$idx]: $label"
  else
    warn "No browser available. Copy the URL manually:"
    echo "  $url"
  fi
}

# ── Step 6: Manual lead save function ────────────────────────────────

save-lead() {
  if [ $# -lt 3 ]; then
    err "Usage: save-lead \"Name\" \"Title\" \"Company\" [LinkedInURL] [hasEmail] [Notes]"
    err "Minimum: name, title, company"
    return 1
  fi
  save_lead "$1" "$2" "$3" "${4:-}" "${5:-false}" "${6:-}"
}

# ── Interactive Help ─────────────────────────────────────────────────

show_help() {
  echo ""
  echo -e "${CYAN}╔══════════════════════════════════════════════════════════╗${NC}"
  echo -e "${CYAN}║           MIFECO LinkedIn Discovery — Commands           ║${NC}"
  echo -e "${CYAN}╚══════════════════════════════════════════════════════════╝${NC}"
  echo ""
  echo "  open_search <1-6>   Open a pre-built LinkedIn search URL"
  echo "  save-lead <args>    Save a discovered lead to JSON"
  echo "  list-leads          Show all saved leads"
  echo "  show-guide          Open the HTML discovery guide"
  echo "  help                Show this help"
  echo "  exit                Exit the automation tool"
  echo ""
}

show_guide() {
  local guide_file="${SCRIPT_DIR}/../forms/linkedin-discovery-guide.html"
  if [ -f "$guide_file" ]; then
    if [ -n "$BROWSER" ]; then
      "$BROWSER" "$guide_file" 2>/dev/null &
      log "Opened LinkedIn Discovery Guide."
    else
      warn "Open this file in your browser:"
      echo "  $guide_file"
    fi
  else
    err "Guide file not found at $guide_file"
  fi
}

# ── Main Interactive Loop ────────────────────────────────────────────

list-leads
show_help
echo -e "${GREEN}Ready to work. Type a command (or 'help' for list).${NC}"
echo ""

while true; do
  read -r -p "mifeco> " cmd args
  case "$cmd" in
    open_search)
      open_search $args
      ;;
    save-lead|save_lead)
      # We need to parse the remaining args carefully
      # Use eval-style parsing for quoted strings
      eval "save_lead $args" 2>/dev/null || err "Invalid arguments. Use: save-lead \"Name\" \"Title\" \"Company\" [URL] [email_bool] [notes]"
      ;;
    list-leads|list)
      list_leads
      ;;
    show-guide|guide)
      show_guide
      ;;
    help|--help|-h)
      show_help
      ;;
    exit|quit|q)
      log "Exiting. Happy prospecting!"
      exit 0
      ;;
    "")
      continue
      ;;
    *)
      err "Unknown command: $cmd  (type 'help' for available commands)"
      ;;
  esac
done
