#!/bin/bash
MEMORY_DIR="$HOME/.hermes/.openclaw/workspace/monthly_archive"
ARCHIVE_DIR="$HOME/.hermes/.openclaw/workspace/memory/archive"

# Create directories if they don't exist
mkdir -p "$MEMORY_DIR"
mkdir -p "$ARCHIVE_DIR"

# Compress monthly memory files
TIMESTAMP=$(date +%Y%m)
SOURCE_FILE="$HOME/.hermes/.openclaw/workspace/memory/agent-communications.jsonl"

if [ -f "$SOURCE_FILE" ]; then
  # Create monthly archive
  ARCHIVE_FILE="$ARCHIVE_DIR/agent-communications-$TIMESTAMP.jsonl.gz"
  
  # Compress and store
  gzip -c "$SOURCE_FILE" > "$ARCHIVE_FILE"
  
  # Clear current file (keeping header if needed)
  echo "" > "$SOURCE_FILE"
  
  echo "Memory compressed and archived: $ARCHIVE_FILE"
  echo "Current memory file cleared for new entries"
fi