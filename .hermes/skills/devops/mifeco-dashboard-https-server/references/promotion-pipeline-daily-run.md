# Promotion Pipeline — Daily Run Procedure

Run the Promotion Generation (promo-gen) pipeline audit daily, autonomously.

## Data Sources

| File | Path | Content |
|------|------|---------|
| Pipeline state | `~/.hermes/pipeline-engine/data/pipeline-state.json` | Current pipeline status, content counts, timestamps |
| Generated social | `~/.hermes/pipeline-engine/data/generated-social-content.json` | LinkedIn + X posts from content-generator.py (per-qualified-lead) |
| Generated blogs | `~/.hermes/pipeline-engine/data/generated-blog-posts.json` | Blog posts from content-generator.py |
| Curated social | `~/.hermes/pipeline-engine/data/social-content-books.json` | Manually curated book- and space-themed posts |
| Outreach templates | `~/.hermes/pipeline-engine/data/linkedin-outreach-messages.json` | Per-product outreach message templates |
| Content generator script | `~/.hermes/pipeline-engine/data/content-generator.py` | Generates social + blog content from qualified leads |
| Unified pipeline | `~/.hermes/pipeline-engine/data/unified-pipeline.json` | All leads across books/consulting/SaaS pipelines |
| Dashboard copy | `~/.hermes/pipeline-engine/dashboard/pipeline-state.json` | Serve-side copy (must be synced after update) |

## Procedure

### 1. Read Current Pipeline State

```bash
# Read pipeline-state.json to see promo-gen section
```

Key fields on `promo-gen`:
- `items`, `active`, `queued`, `failed` — content pipeline counts
- `currentStage` — which stage the pipeline is at (0-indexed: Brief, Creative, Assets, Copy, Schedule, Launch)
- `lastRun` — timestamp of last run
- `dataSources` — which files to check

### 2. Check All Content Source Files

Read each data source file and count:

- **social-content-books.json**: Count items by `platform` (linkedin vs x). Note `generated_at` dates.
- **generated-social-content.json**: Count `linkedin_posts` and `x_posts` from `stats`. Check `qualified_leads` count. Note each item's `linked_lead_id` to see which leads were covered.
- **generated-blog-posts.json**: Count `total_posts` from `stats`. Note categories and `generated_at`.
- **linkedin-outreach-messages.json**: Count templates. Note each template's `target_type` (e.g., saas_hypatia, saas_pma, consulting_199, consulting_dive).

### 3. Count Qualified Leads

From `unified-pipeline.json`, count leads where `total_score >= 15`. The threshold is defined in content-generator.py as `QUALIFIED_SCORE_THRESHOLD = 15`.

Cross-reference: the generated-social-content stats should show the same number of qualified leads.

### 4. Reconcile & Calculate Counts

Compute:

| Metric | Calculation |
|--------|-------------|
| `linkedin-posts` | Curated LinkedIn (social-content-books) + Generated LinkedIn (generated-social-content) |
| `x-posts` | Curated X + Generated X |
| `blog-posts` | Count from generated-blog-posts.json |
| `linkedin-msgs` | Count from linkedin-outreach-messages.json |
| `totalItems` | Sum of all above + emails + enrichment (preserve existing) |
| `queuedItems` | = totalItems (all items are queued if none sent/approved) |

Promo-gen pipeline counts:
- `items` = total promotion items (28 social posts + 3 blog posts + 6 outreach = 37)
- `active` = generated content ready to post (count from generated-social-content stats)
- `queued` = items pending review/scheduling (curated social + blog posts + outreach templates)
- `failed` = 0 (unless detected)
- `lastRun` = current timestamp

### 5. Update pipeline-state.json

Three targeted patches:

1. **updatedAt** → current ISO timestamp
2. **promo-gen pipeline block** → new items/active/queued/lastRun values
3. **contentSummary** → new counts (x-posts, blog-posts, linkedin-posts, totalItems, queuedItems)

### 6. Copy to Dashboard

```bash
cp ~/.hermes/pipeline-engine/data/pipeline-state.json \
   ~/.hermes/pipeline-engine/dashboard/pipeline-state.json
```

### 7. Verify

Read the updated file back to confirm the patches applied correctly — check the promo-gen section and contentSummary block.

## Pitfalls

- **Counts must be additive across ALL content sources.** The contentSummary `linkedin-posts` and `x-posts` should count BOTH curated (social-content-books.json) AND generated (generated-social-content.json) posts. Each file alone gives only part of the picture.
- **sentItems and approvedItems** should remain 0 unless evidence exists that content was actually published. Do not assume anything was sent.
- **generated-social-content.json** has a header/stats object as its first element — skip it when counting individual post entries. Use `stats.total_posts` for the total count.
- **Pipeline `currentStage`** maps to the stages array index (0-5). If content is written but not scheduled, stage = 3 (Copy). Do not advance the stage unless content was actually dispatched.
- **content-generator.py** re-generates content from qualified leads — check `generated_at` timestamps before re-running. Stale output should be regenerated if leads are stale.
- **`contentSummary.enrichment`** must equal the count of qualified leads from `unified-pipeline.json` (score ≥ 15), NOT the total lead count. This field was historically stale (showing 10 when actual was 8). Always recompute from the source data.
