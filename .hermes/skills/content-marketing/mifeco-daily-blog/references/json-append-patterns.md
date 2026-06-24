# JSON Append Patterns for Pipeline Data Files

## The Problem

The `patch` tool's fuzzy matcher fails on JSON files containing escaped quotes with an "Escape-drift detected" error. This is a serialization artifact.

## Preferred Solution: Python Heredoc via terminal()

```bash
python3 << 'PYEOF'
import json
path = '/home/bob/.hermes/pipeline-engine/data/generated-blog-posts.json'
with open(path, 'r') as f:
    data = json.load(f)
data.append({"title": "New Post", "slug": "new-slug", "type": "book"})
with open(path, 'w') as f:
    json.dump(data, f, indent=2)
print(f"OK - {len(data)} entries")
PYEOF
```

## Key Rules

1. Never retry `patch` on JSON -- switch to Python heredoc immediately
2. Always validate with `json.load()` after writing
3. Index [0] is metadata -- preserve it when appending
