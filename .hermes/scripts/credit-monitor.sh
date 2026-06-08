#!/bin/bash
# =============================================================================
# CREDIT MONITOR — Tracks all paid API keys and services
# Monitors: Exa Search, OpenRouter, Google AI Studio
# Run daily via cron job (`credit-monitor` at 18:00)
# =============================================================================
set -o pipefail

TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")
LOG_DIR="$HOME/.hermes/logs"
EXA_LOG="$LOG_DIR/exa_usage.log"
CREDIT_LOG="$LOG_DIR/credit-monitor.log"
GA_LOG="$LOG_DIR/google_ai_usage.log"
ENV_FILE="$HOME/.hermes/.env"
ENV_FILE2="$HOME/.bashrc"

mkdir -p "$LOG_DIR"

log() {
  echo "[$TIMESTAMP] $*" >> "$CREDIT_LOG"
}

# Source API keys from .env (primary) and .bashrc (for EXA_API_KEY)
if [ -f "$ENV_FILE" ]; then
  source <(grep -E '^(OPENROUTER_API_KEY|GOOGLE_AI_STUDIO_KEY|GEMINI_API_KEY)=' "$ENV_FILE" 2>/dev/null)
fi
if [ -f "$ENV_FILE2" ]; then
  source <(grep -E '^export EXA_API_KEY=' "$ENV_FILE2" 2>/dev/null || grep -E '^EXA_API_KEY=' "$ENV_FILE2" 2>/dev/null)
fi

# Normalize variable names — handle various casings from .env files
if [ -z "${OPENROUTER_API_KEY:-}" ] && [ -n "${openrouter_API_KEY:-}" ]; then
  export OPENROUTER_API_KEY="$openrouter_API_KEY"
fi

echo "=== CREDIT MONITOR — $(date '+%A, %B %d, %Y') ==="
echo ""

# ── 1. EXA ──────────────────────────────────────────────────────────────────
echo "╔═══════════════════════════════════════════╗"
echo "║  🔍 Exa Search API                        ║"
echo "╚═══════════════════════════════════════════╝"
if [ -f "$EXA_LOG" ]; then
    TODAY_EXA=$(grep "$(date +%F)" "$EXA_LOG" 2>/dev/null | wc -l)
    TOTAL_EXA=$(wc -l < "$EXA_LOG" 2>/dev/null || echo 0)
    printf "  Today's calls : %s\n" "$TODAY_EXA"
    printf "  Total calls   : %s\n" "$TOTAL_EXA"
    log "EXA: $TODAY_EXA calls today, $TOTAL_EXA total"
else
    echo "  No usage data yet"
    log "EXA: No usage data"
fi
echo ""

# ── 2. OPENROUTER ───────────────────────────────────────────────────────────
echo "╔═══════════════════════════════════════════╗"
echo "║  🌐 OpenRouter API                        ║"
echo "╚═══════════════════════════════════════════╝"
OR_KEY="${OPENROUTER_API_KEY:-}"
if [ -n "$OR_KEY" ]; then
    OR_RESPONSE=$(curl -s --max-time 10 \
        -H "Authorization: Bearer $OR_KEY" \
        "https://openrouter.ai/api/v1/auth/key" 2>/dev/null)
    
    if [ -n "$OR_RESPONSE" ]; then
        OR_DATA=$(echo "$OR_RESPONSE" | python3 -c "
import sys, json
try:
    d = json.load(sys.stdin).get('data', {})
    label = d.get('label', 'unlabeled')
    limit = d.get('limit', 0)
    usage = d.get('usage', 0)
    credits = limit - usage
    print(f'{label}|{limit}|{usage}|{credits}')
except:
    print('parse_error|0|0|0')
" 2>/dev/null)
        
        OR_LABEL=$(echo "$OR_DATA" | cut -d'|' -f1)
        OR_LIMIT=$(echo "$OR_DATA" | cut -d'|' -f2)
        OR_USAGE=$(echo "$OR_DATA" | cut -d'|' -f3)
        OR_CREDITS=$(echo "$OR_DATA" | cut -d'|' -f4)
        
        if [ "$OR_LABEL" = "parse_error" ]; then
            echo "  ⚠️  API error — unexpected response"
            log "OpenRouter: parse error — response: $(echo "$OR_RESPONSE" | head -c 200)"
        else
            printf "  Key label    : %s\n" "$OR_LABEL"
            if [ "$OR_LIMIT" != "0" ]; then
                printf "  Total limit  : \$%.4f\n" "$OR_LIMIT"
                printf "  Used         : \$%.4f\n" "$OR_USAGE"
                printf "  Remaining    : \$%.4f\n" "$OR_CREDITS"
            else
                printf "  Total limit  : pay-as-you-go\n"
                printf "  Used         : \$%.4f\n" "$OR_USAGE"
            fi
            log "OpenRouter: label=$OR_LABEL limit=$OR_LIMIT usage=$OR_USAGE remaining=$OR_CREDITS"
        fi
    else
        echo "  ⚠️  Could not reach OpenRouter API"
        log "OpenRouter: query failed (no response)"
    fi
else
    echo "  ⚠️  OpenRouter key not available"
    log "OpenRouter: no API key configured"
fi
echo ""

# ── 3. GOOGLE AI STUDIO ─────────────────────────────────────────────────────
echo "╔═══════════════════════════════════════════╗"
echo "║  🤖 Google AI Studio (Gemini API)         ║"
echo "╚═══════════════════════════════════════════╝"
GA_KEY="${GOOGLE_AI_STUDIO_KEY:-${GEMINI_API_KEY:-}}"
if [ -n "$GA_KEY" ]; then
    if [ -f "$GA_LOG" ]; then
        GA_TODAY=$(grep "$(date +%F)" "$GA_LOG" 2>/dev/null | wc -l)
        GA_TOTAL=$(wc -l < "$GA_LOG" 2>/dev/null || echo 0)
    else
        GA_TODAY=0
        GA_TOTAL=0
    fi
    printf "  Today's calls : %s\n" "$GA_TODAY"
    printf "  Total tracked : %s\n" "$GA_TOTAL"
    printf "  Free tier     : 1,500 requests/day (60/min)\n"
    
    # Key validation via Gemini models list
    GA_CHECK=$(curl -s --max-time 5 \
        "https://generativelanguage.googleapis.com/v1beta/models?key=${GA_KEY}" 2>/dev/null)
    
    if echo "$GA_CHECK" | python3 -c "import sys,json; d=json.load(sys.stdin); sys.exit(0 if 'models' in d else 1)" 2>/dev/null; then
        echo "  ✅ Key valid"
        log "GoogleAI: today=$GA_TODAY total=$GA_TOTAL key_status=valid"
    else
        ERR_MSG=$(echo "$GA_CHECK" | python3 -c "import sys,json; print(json.load(sys.stdin).get('error',{}).get('message','unknown'))" 2>/dev/null || echo "connection failed")
        printf "  ❌ Key issue : %s\n" "$ERR_MSG"
        log "GoogleAI: today=$GA_TODAY total=$GA_TOTAL key_status=invalid error=$ERR_MSG"
    fi
else
    echo "  ⚠️  Google AI Studio key not found"
    log "GoogleAI: no API key configured"
fi
echo ""

# ── 4. SUMMARY & ALERTS ─────────────────────────────────────────────────────
echo "╔═══════════════════════════════════════════╗"
echo "║  📊 Credit Status Summary                 ║"
echo "╚═══════════════════════════════════════════╝"
WARNINGS=""

if [ -n "$OR_CREDITS" ] && [ "$OR_CREDITS" != "0" ] && [ "$(echo "$OR_CREDITS < 10" | bc 2>/dev/null)" = "1" ]; then
    WARNINGS="${WARNINGS}⚠️  OpenRouter credits running low: \$${OR_CREDITS} remaining\n"
fi

if [ "${TODAY_EXA:-0}" -gt 100 ] 2>/dev/null; then
    WARNINGS="${WARNINGS}⚠️  Exa usage high: $TODAY_EXA calls today (limit: 100/day)\n"
fi

if [ -n "$WARNINGS" ]; then
    echo -e "$WARNINGS"
    log "ALERTS: $(echo "$WARNINGS" | tr '\n' ';')"
else
    printf "  %s\n" "✅ All services within normal limits"
    log "All services normal"
fi

echo ""
echo "────────────────────────────────────────────"
echo "Next check: Tomorrow at 18:00"
echo "Logged to: $CREDIT_LOG"

# Append monitoring result to credit log
echo "[$TIMESTAMP] MONITOR: Exa=$TODAY_EXA OpenRouter='${OR_LABEL:-unknown}' GoogleAI=$GA_TODAY Status=OK" >> "$CREDIT_LOG" 2>/dev/null || true
