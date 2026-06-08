---
name: exa-web-search
description: High-quality web search using Exa API for real-time web content, RAG workflows, and agent research
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [search, web, exa, rag, agent]
    related_skills: [hermes-agent, research-paper-writing]
---

## 🔍 MemPalace Query (MANDATORY FIRST STEP)
Before proceeding, query MemPalace for existing context:
```python
import sys, os; sys.path.insert(0, os.path.expanduser('~/.hermes/mempalace'))
import embed; embed.init_embedding(os.path.expanduser('~/.hermes/mempalace'))
results = embed.search_embeddings("web search Exa API RAG research", k=5)
```
This retrieves previous decisions, domain-specific context, and lessons learned from the vector memory store.

# Exa Web Search Integration

## API Configuration
- **Endpoint:** https://api.exa.ai/search
- **API Key:** 3d5b0159-71a9-4cf2-b7c2-326be971f2de (stored in ~/.bashrc as EXA_API_KEY)
- **Dashboard:** https://dashboard.exa.ai

## Search Types
| Type | Best For | Latency |
|------|----------|---------|
| auto | Most queries (default) | ~1s |
| fast | Latency-sensitive | ~450ms |
| instant | Chat/voice/autocomplete | ~250ms |
| deep-lite | Cheaper synthesis | 4s |
| deep | Research, thorough results | 4-15s |
| deep-reasoning | Complex multi-step reasoning | 12-40s |

## Content Configuration
```bash
# Full text extraction
"contents": { "text": { "max_characters": 20000 } }

# Token-efficient highlights
"contents": { "highlights": { "max_characters": 4000 } }

# Per-result summary
"contents": { "summary": { "query": "your specific question" } }
```

## Common cURL Pattern
```bash
curl -s -X POST 'https://api.exa.ai/search' \
  -H "x-api-key: $EXA_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{
    "query": "your query here",
    "type": "auto",
    "num_results": 10,
    "contents": {
      "text": { "max_characters": 20000 }
    }
  }'
```

## Structured Outputs
```bash
curl -s -X POST 'https://api.exa.ai/search' \
  -H "x-api-key: $EXA_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{
    "query": "companies in renewable energy",
    "type": "auto",
    "outputSchema": {
      "type": "object",
      "required": ["companies"],
      "properties": {
        "companies": {
          "type": "array",
          "items": {
            "type": "object",
            "required": ["name"],
            "properties": {
              "name": { "type": "string" },
              "focus": { "type": "string" }
            }
          }
        }
      }
    }
  }'
```

## Domain Filtering
```json
{
  "includeDomains": ["arxiv.org", "github.com"],
  "excludeDomains": ["pinterest.com"]
}
```

## Credit Monitoring
Run `~/.hermes/scripts/exa_credit_monitor.sh` to check usage. Credits tracked via Telegram.

## Best Practices
1. Use `type: "auto"` for most queries
2. Always set `maxCharacters` to control token cost
3. Use `type: "deep"` for research requiring thorough synthesis
4. Use `outputSchema` when structured data is needed
5. Prefer `highlights` over `text: true` for token efficiency
6. Combine search with domain filters for authoritative sources

## Troubleshooting
- No results? Remove filters, simplify query, try `type: "auto"`
- Irrelevant results? Try `type: "deep"` or refine query
- Slow responses? Use `type: "fast"` or reduce `numResults`
- Token cost blowup? Use `highlights` with `maxCharacters`