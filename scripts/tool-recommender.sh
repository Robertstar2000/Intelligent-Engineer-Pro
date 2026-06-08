#!/bin/bash
TASK_REQUIREMENTS="$1"

echo "Tool recommendations for: $TASK_REQUIREMENTS"
echo "=========================================="

# Simple keyword-based tool recommendations
case "$TASK_REQUIREMENTS" in
  *web*|*browser*|*scrape*|*download*)
    echo "1. browser_tool (High relevance)"
    echo "2. web_tools (High relevance)"
    echo "3. delegate_tool (Medium relevance for complex workflows)"
    ;;
  *file*|*read*|*write*|*edit*|*search*)
    echo "1. file_tools (High relevance)"
    echo "2. patch (High relevance for targeted edits)"
    echo "3. search_files (High relevance for content search)"
    ;;
  *terminal*|*command*|*shell*|*execute*)
    echo "1. terminal (High relevance)"
    echo "2. execute_code (Medium relevance for Python execution)"
    echo "3. process (Medium relevance for background processes)"
    ;;
  *skill*|*learn*|*teach*|*train*)
    echo "1. skill_manage (High relevance)"
    echo "2. skill_view (High relevance)"
    echo "3. skills_list (Medium relevance for discovery)"
    ;;
  *memory*|*recall*|*remember*)
    echo "1. memory (High relevance)"
    echo "2. session_search (High relevance for past conversations)"
    echo "3. mempalace-integration (Medium relevance for long-term storage)"
    ;;
  *)
    echo "General purpose recommendations:"
    echo "1. file_tools (Universal need)"
    echo "2. terminal (Universal need)"
    echo "3. memory (Context preservation)"
    ;;
esac