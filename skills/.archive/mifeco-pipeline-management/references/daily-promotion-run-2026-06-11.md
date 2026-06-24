# Daily Promotion Pipeline Run — 2026-06-11

This is a concrete example of a successful daily promotion pipeline run.

## Initial State

From `pipeline-state.json` before the run:
- **promo-gen** pipeline: items=18, active=18, queued=0, currentStage=3 (Assets)
- **contentSummary**: linkedin-msgs=6, emails=7, enrichment=8, x-posts=14, blog-posts=5, linkedin-posts=14, totalItems=39

## Content Inventory (Before Generation)

| Source | LinkedIn | X | Other | Total |
|--------|----------|---|-------|-------|
| `social-content-books.json` | 6 | 6 | 0 | 12 |
| `generated-social-content.json` | 8 | 8 | 1 | 17 |
| `generated-blog-posts.json` | — | — | — | 8 (1 untitled stale) |
| `linkedin-outreach-messages.json` | — | — | — | 6 templates |

## Content Generator Report

```bash
python3 data/content-generator.py --report
```

Showed 8 qualified leads (score >= 15): 2 books, 3 consulting, 3 SaaS.
Would generate 16 social posts + 3 blog posts.

**Decision:** Regenerate. Existing content had stale entries (1 "unknown" platform post, 1 "untitled" blog post, and the last generation was ~1 month ago for social).

## Generation Result

```bash
python3 data/content-generator.py
```

Produced:
- 16 social posts (8 LinkedIn + 8 X) — 1 "unknown" platform entry remained from previous content
- 3 blog posts — 1 "untitled" stale entry remained (generator appends rather than truncates)

## Pipeline State After

**promo-gen** pipeline:
- `currentStage`: 3 → 4 (Copy) — content generated, advancing from Assets stage
- `items`: 18 → 38 (total promotion content available)
- `active`: 18 → 38 (all items ready to post)
- `queued`: 0 (no drafts pending)
- `lastRun`: "2026-06-11 12:31 PM"
- `health`: green

**contentSummary:**
- linkedin-msgs: 6, emails: 7, enrichment: 10
- x-posts: 14, blog-posts: 4, linkedin-posts: 14
- totalItems: 55, queuedItems: 55

## Dashboard Sync

```bash
cp ~/.hermes/pipeline-engine/data/pipeline-state.json ~/.hermes/pipeline-engine/dashboard/pipeline-state.json
```