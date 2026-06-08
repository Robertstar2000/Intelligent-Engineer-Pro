#!/bin/bash
# Exa API Search Script with Credit Tracking
EXA_API_KEY="3d5b0159-71a9-4cf2-b7c2-326be971f2de"
LOG_FILE="$HOME/.hermes/logs/exa_usage.log"

# Default parameters
QUERY="${1:?Query required}"
TYPE="${2:-auto}"  # auto, fast, instant, deep-lite, deep, deep-reasoning
NUM_RESULTS="${3:-10}"
MAX_CHARS="${4:-20000}"

# Make the API call
response=$(curl -s -X POST 'https://api.exa.ai/search' \
  -H "x-api-key: $EXA_API_KEY" \
  -H 'Content-Type: application/json' \
  -d "{
    \"query\": \"$QUERY\",
    \"type\": \"$TYPE\",
    \"num_results\": $NUM_RESULTS,
    \"contents\": {
      \"text\": { \"max_characters\": $MAX_CHARS }
    }
  }")

# Log usage
echo "[$(date -u)] Query: $QUERY | Type: $TYPE | Results: $NUM_RESULTS | Response: $(echo $response | wc -c) bytes" >> "$LOG_FILE"

# Output response
echo "$response"
