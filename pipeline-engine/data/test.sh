#!/usr/bin/env bash
# Run all tests for content-generator.py
set -e
cd "$(dirname "$0")"

echo "=== Test Suite: content-generator.py ==="
echo ""

echo "1. Report mode (--report)..."
python3 content-generator.py --report 2>&1 | head -30
echo ""

echo "2. Social only mode..."
python3 content-generator.py --social only 2>&1
echo ""

echo "3. Blog only mode..."
python3 content-generator.py --blog only 2>&1
echo ""

echo "4. Pipeline filter: books..."
python3 content-generator.py --pipeline books --social only 2>&1
echo ""

echo "5. Full generation (all)..."
python3 content-generator.py 2>&1
echo ""

echo "=== Manual Verification ==="
echo "Checking generated files..."
for f in data/generated-social-content.json data/generated-blog-posts.json; do
    if [ -f "$f" ]; then
        size=$(wc -c < "$f")
        lines=$(wc -l < "$f")
        echo "  ✓ $f ($size bytes, $lines lines)"
    else
        echo "  ✗ $f not found!"
    fi
done

echo ""
echo "=== Content Sample ==="
echo ""
echo "--- Social Post Sample (first LinkedIn) ---"
python3 -c "
import json
with open('data/generated-social-content.json') as f:
    data = json.load(f)
for item in data[1:3]:
    if isinstance(item, dict) and 'platform' in item:
        print(f\"Platform: {item['platform']}\")
        print(f\"Lead ID: {item['linked_lead_id']}\")
        print(f\"Copy (first 200 chars): {item['copy'][:200]}...\")
        print(f\"Hashtags: {item['hashtags']}\")
        print()
"
echo ""
echo "--- Blog Post Sample ---"
python3 -c "
import json
with open('data/generated-blog-posts.json') as f:
    data = json.load(f)
for item in data[1:2]:
    if isinstance(item, dict) and 'title' in item:
        print(f\"Title: {item['title']}\")
        print(f\"Slug: {item['slug']}\")
        print(f\"Category: {item['category']}\")
        print(f\"Word count: {item['word_count']}\")
        print(f\"SEO Keywords: {item['seo_keywords']}\")
        print()
"
