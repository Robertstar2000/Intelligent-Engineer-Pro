---
name: mifeco-pipeline-management
description: Manage MIFECO product pipeline data — JSON definitions, SVG flow diagrams, kanban DB seeding, and dashboard rendering. Covers the full lifecycle from editing pipeline stages to syncing dashboards to DreamHost.
triggers: ["pipeline", "kanban", "pipeline dashboard", "pipeline data", "pipeline stages", "books pipeline", "saas pipeline", "consulting pipeline", "virtual consulting pipeline", "human consulting pipeline", "books creation", "books marketing", "kanban sync", "seed kanban", "pipeline sync", "rebuild pipeline", "update pipeline", "pipeline flow", "svg flow", "promotion pipeline", "promotion generation", "promo-gen", "daily pipeline run", "promotion run", "content generator", "content-generator", "social-content-books", "generated-social-content", "linkedin-outreach", "promotion inventory"]
---

# MIFECO Pipeline Management

Manages the 5 product pipelines that power the MIFECO admin dashboard and Hermes kanban board.

## Pipeline Architecture

5 product pipelines, each with 8 stages:

| Pipeline | ID | Color | Stages |
|---|---|---|---|
| Books Creation | `books-creation` | #3b82f6 blue | Review Market, Build Book Bible, Build Framework, Write, Enrich, Edit, Prep for KDP, Finish |
| Books Marketing | `books-marketing` | #8b5cf6 purple | Marketing Content, Infographic, Discovery, Promote, Outreach, Nurture Sequence, Analyze Results, Optimize Campaigns |
| SaaS | `saas` | #22c55e green | Identified, Contacted, Qualified, Process, Demo/Free Trial, Complete Transaction, Followup, Upsell/Cross-sell |
| Human Consulting | `human-consulting` | #f97316 orange | Lead, Contact, Qualified, Intent, Strategy Session, Proposal Sent, Negotiation, Closed Won |
| Virtual Consulting | `virtual-consulting` | #06b6d4 cyan | Lead, Contacted, Survey, Research, Generate Reports, Quality Review, Delivery, Complete |

### Virtual Consulting Deliverable Format

**Reports are SINGLE PDFs, NOT KDP packages.** This is a critical distinction — the old pipeline stages (Qualifier, Buy, Process, Deliverables, Edit) were book-purchase-oriented and wrong.

Each report is a standalone, professionally formatted PDF containing:
1. Integrated cover image (page 1)
2. Delivery cover letter (page 2)
3. Table of contents (page 3)
4. 30+ page detailed report

Content sources: initial qualification questions + full survey data + LLM domain knowledge + web search results when needed.

Engagement tiers:
- **AI Readiness Assessment** ($199) — Single PDF report
- **Business Transformation Package** ($1,499) — 2 separate PDFs (Assessment + Strategic Plan)
- **Deep-Dive Consulting** ($3,999) — Multiple PDF deliverables with ongoing support

### SaaS Product Line

The SaaS pipeline (`pipeline-saas.json` + `saas` section of `unified-pipeline.json`) lists 3 products:

| Product | Price | Description |
|---|---|---|
| Project Hypatia Pro | $99/mo | AI-powered project management for professionals |
| **HMAP Project Accelerator** | $69/mo | AI-powered project acceleration platform — proposals, plans, tracking & team coordination 20x faster. **NOT "PM Accelerator"** — the old name is deprecated. |
| VibraEngineer | $29/mo | Lightweight engineering task management |

**Important:** When replacing old product references, search ALL file types (`*.json`, `*.html`, `*.php`) for "PM Accelerator" — it appears in `pipeline-saas.json`, `index.html`, and `unified-pipeline.json`. Use `search_files` with `file_glob` to find all occurrences.

### Complete Book Catalog (20 titles)

Both Books Creation and Books Marketing pipelines in `unified-pipeline.json` must list ALL 20 books:

| Series / Category | Titles | Status |
|---|---|---|
| **No Blue Sky** (5) | Built from Dust, The Oxygen Gamble, Rivers Under Mars, The Red Charter, The First Martian Nation | published |
| **Lunar Foundation** (4) | Moon Rock, Mooncoming, Waters End, Waters Horizon | published |
| **Age of Lightships** (4) | Sunward Exodus, The Mercury Accord, Ghosts Beyond Neptune, The Last Photon Fleet | out_of_print |
| **Cindy Lou Legal Capers** (3) | Retainer to Trouble, Clause for Alarm, Affidavits and Alibis | draft |
| **Standalone** (4) | Tomorrow Remembered, AI That Works for Small Business, The Owner's Manual for AI Agents, The Crisis Ready Company | published |

**Common mistake:** Only listing the "active" published books and forgetting legacy/out-of-print series and standalone titles. Always include all 20.

## File Map

All files live under `/home/bob/.hermes/pipeline-engine/dashboard/`:

| File | Purpose |
|---|---|
| `unified-pipeline.json` | Master pipeline definitions (stages, products, email, nurture) |
| `pipeline-state.json` | Admin-facing pipeline status (health, item counts, stage arrays) |
| `pipeline-books.json` | Book catalog (all 20 titles + box sets) + Books Marketing leads |
| `pipeline-saas.json` | SaaS products + leads |
| `pipeline-consulting.json` | Human + Virtual consulting leads |
| `pipeline-dashboard.html` | Main pipeline dashboard (tabbed view, kanban boards per pipeline) |
| `kanban-dashboard.html` | Agent task board (reads from kanban-data.php) |
| `kanban-data.php` | PHP proxy: tries SQLite DB (local + DreamHost paths), falls back to JSON pipeline files |
| `flows/*.svg` | 5 SVG flow diagrams (one per pipeline) |
| `.htaccess` | Apache rewrite rules — **must whitelist `kanban-data.php`** or it returns 403 |

A mirrored copy lives at `/home/bob/FL-Hermes/pipeline-engine/dashboard/`.

## Workflow: Full Pipeline Rebuild

When the user provides new pipeline stage definitions or wants to restructure pipelines:

### 1. Update JSON Data Files

Edit these files in order:
1. `unified-pipeline.json` — master definitions (include ALL books/products)
2. `pipeline-state.json` — admin status view
3. `pipeline-books.json` — book leads
4. `pipeline-saas.json` — SaaS leads
5. `pipeline-consulting.json` — consulting leads

Validate all JSON after editing:
```bash
cd /home/bob/.hermes/pipeline-engine/dashboard
for f in *.json; do python3 -c "import json; json.load(open('$f'))" && echo "OK $f" || echo "FAIL $f"; done
```

### 2. Regenerate SVG Flow Diagrams

Each pipeline needs an SVG in `flows/`. Use this exact pattern (8 stages, viewBox="0 0 1050 50"):

X positions for boxes: 25, 140, 255, 370, 485, 600, 715, 830
Text X positions: 75, 190, 305, 420, 535, 650, 765, 880
Arrow x1: 125, 240, 355, 470, 585, 700, 815
Arrow x2: 140, 255, 370, 485, 600, 715, 830

First stage box uses `class="stage-active"` (green highlight), rest use `class="stage-box"`.

### 3. Seed Kanban DB

The kanban SQLite DB is at `/home/bob/.hermes/kanban.db`. Key columns: `id`, `title`, `body`, `assignee`, `status`, `priority`, `tenant` (pipeline ID), `stage` (1-8).

Use `scripts/seed_kanban.py` as a template. Task ID prefixes:
- `BC-` = Books Creation
- `BM-` = Books Marketing
- `S-` = SaaS
- `C-` = Human Consulting
- `VC-` = Virtual Consulting

If the `stage` column doesn't exist, add it:
```sql
ALTER TABLE tasks ADD COLUMN stage INTEGER DEFAULT 1;
```

### 4. Rebuild Dashboards

- `pipeline-dashboard.html` — reads from JSON files via fetch(). Tabbed view with 8-column kanban boards per pipeline.
- `kanban-dashboard.html` — reads from `kanban-data.php` (which reads kanban.db). Tabbed view with 8-column boards grouped by stage.

### 5. Sync to DreamHost

Use the sync script:
```bash
python3 /home/bob/.hermes/pipeline-engine/scripts/sync_dashboard.py
```

**IMPORTANT:** rsync is ADDITIVE — it won't delete remote files that no longer exist locally. After removing files from local, run cleanup:
```bash
python3 /home/bob/.hermes/pipeline-engine/scripts/cleanup_dreamhost.py
```

**File permissions on DreamHost:** After sync, ensure `0644` on HTML and PHP files:
```bash
chmod 644 ~/mifeco.com/admin/kanban-dashboard.html ~/mifeco.com/admin/kanban-data.php ~/mifeco.com/admin/.htaccess
```

### 6. Sync to FL-Hermes Copy

```bash
SRC="/home/bob/.hermes/pipeline-engine/dashboard"
DST="/home/bob/FL-Hermes/pipeline-engine/dashboard"
cp "$SRC"/*.html "$SRC"/*.json "$SRC"/*.php "$DST/"
cp "$SRC/flows/"*.svg "$DST/flows/"
```

### 7. Deploy Kanban DB to DreamHost (if needed)

The `kanban-data.php` tries both local and DreamHost SQLite paths. For DreamHost to use SQLite (faster), copy the DB:
```bash
scp -o StrictHostKeyChecking=no ~/.hermes/kanban.db dh_mwpxuu@iad1-shared-b8-42.dreamhost.com:/home/dh_mwpxuu/mifeco.com/admin/kanban.db
```

If SQLite isn't available on DreamHost, `kanban-data.php` automatically falls back to reading JSON pipeline files.

## Promotion Pipeline Daily Run

A recurring cron workflow that inventories all promotion content, validates the content generator, and syncs updated counts to the dashboard. Trigger: the `promotion-orchestrator` cron job or any request to "run the promotion pipeline."

### Workflow Steps

#### 1. Load & Inspect Pipeline State

Read `pipeline-state.json` to capture:
- `promo-gen` pipeline: `items`, `active`, `queued`, `currentStage`, `lastRun`, `contentSummary`
- Note stale vs actual counts (contentSummary is often out of sync with real file inventory)

#### 2. Inventory All Content Sources

The promotion pipeline draws from 4 independent JSON files. Count each:

| Source | What It Contains | How to Count |
|--------|-----------------|--------------|
| `social-content-books.json` | Pre-written book promotion drafts (LinkedIn + X) | Read the array length; cross-check `post_type`/`platform` fields |
| `generated-social-content.json` | Pipeline-generated social posts from qualified leads | Read the `stats` header object for `linkedin_posts`, `x_posts`, `total_posts` (skip the header entry itself) |
| `generated-blog-posts.json` | Blog articles + comparison posts | Read the `stats` header for generated count; then count any extra entries (comparison posts) manually |
| `linkedin-outreach-messages.json` | Outreach message templates (not sent counts) | Array length — these are templates, not sent messages |

**Compute totals:**
- LinkedIn posts = social-content-books LinkedIn count + generated-social-content LinkedIn count
- X posts = social-content-books X count + generated-social-content X count
- Blog posts = total entries in generated-blog-posts (excluding header)
- Outreach = total entries in linkedin-outreach-messages
- Total items = sum of all above

#### 3. Check Content Generator Status

Run the content generator in report mode to see if new content is needed:

```bash
cd ~/.hermes/pipeline-engine
python3 data/content-generator.py --report
```

This reports:
- Total leads in pipeline
- Qualified leads (score >= 15) by pipeline (books/consulting/saas)
- How many social posts and blog posts would be generated

**Decision rule:** Compare qualified leads vs existing content. If they differ materially (different lead IDs, scores changed, or the last generation was more than 7 days old), regenerate by running the full generator without `--report`. Also regenerate if existing content has stale/unknown entries (e.g. `platform: "unknown"` or `title: "untitled"`) — these are artifacts from prior runs that should be replaced. Always run the full generator at least weekly to keep content fresh.

**Running the generator:**
```bash
cd ~/.hermes/pipeline-engine
python3 data/content-generator.py
```
**Note:** The generator OVERWRITES the output files. If stale entries remain (like an `"untitled"` blog post or an `"unknown"` platform post), the generator may be appending/extending rather than truncating — verify by reading the output files after generation and correcting if needed.

After generation, check the actual file counts:
```bash
python3 -c "
import json
sc = json.load(open('data/generated-social-content.json'))
li = sum(1 for p in sc if p.get('platform') in ('linkedin',) or p.get('post_type') == 'linkedin')
x = sum(1 for p in sc if p.get('platform') in ('x',) or p.get('post_type') == 'x')
other = len(sc) - li - x
print(f'LinkedIn: {li}, X: {x}, Other: {other}')
bp = json.load(open('data/generated-blog-posts.json'))
print(f'Blog posts: {len(bp)}')
"
```

**Stage advancement:** If content was successfully generated, advance `currentStage` from 3 (Assets) to 4 (Copy) since the copy/assets stage is now complete.

#### 4. Update pipeline-state.json

Update these fields in the `promo-gen` pipeline:
- `lastRun` — timestamp
- `currentStage` — advance to 4 (Copy) after content generation if currently at 3 (Assets)
- `items` — total promotion content items available (computed inventory — see step 2)
- `active` — ready-to-post items (same as items when nothing has been sent)
- `queued` — drafts pending generation (0 if all content has been generated)

Update `contentSummary`:
- `x-posts`, `linkedin-posts`, `blog-posts`, `linkedin-msgs` — computed inventory
- `enrichment` — count enriched/qualified leads in pipeline
- `totalItems` — sum of all content
- `queuedItems` — same as totalItems if nothing has been sent/approved
- `sentItems`, `approvedItems` — leave at 0 unless confirmed otherwise

#### 5. Sync to Dashboard

```bash
cp ~/.hermes/pipeline-engine/data/pipeline-state.json ~/.hermes/pipeline-engine/dashboard/pipeline-state.json
```

### Content Generator (`content-generator.py`)

Located at `data/content-generator.py`. Key modes:
- `--report` — dry-run showing what would be generated, no file writes
- `--pipeline books` — filter to books pipeline only
- `--social only` — social posts only
- `--blog only` — blog posts only

Requires these data files:
- `unified-pipeline.json` — lead pipeline data
- `leads-registry.json` — lead registry
- `social-content-books.json` — existing book social posts (used to avoid duplicates)
- `nurture-sequences.json` — nurture sequence templates

Output files:
- `generated-social-content.json` — LinkedIn + X posts, one per qualified lead per platform
- `generated-blog-posts.json` — blog articles covering AI/Tech, PM/SaaS, and Books/Space themes

### Content Inventory Reference

Current known post types and their typical pipelines:
- **LinkedIn book promos**: templates for No Blue Sky series, Tomorrow Is Still Open memoir
- **LinkedIn consulting promos**: AI adoption frameworks, compliance AI use cases
- **LinkedIn SaaS promos**: tool sprawl, transparency, project management
- **X book promos**: concise book quotes, space exploration hooks
- **X consulting promos**: AI adoption stats, quick tips
- **X SaaS promos**: productivity stats, tool insights
- **Blog posts**: long-form articles (AI transformation, project management, space/science fiction)
- **Outreach templates**: personalized email drafts for SaaS (Hypatia/PMA/Vibra) and Consulting ($199/Dive/Transform) targets

### Inventory-Only Pass (When Generator is Skipped)

When the content generator ran within the last 7 days and lead scores haven't changed meaningfully, skip regeneration and do a pure inventory pass:

1. Count all posts from each source file individually (don't trust cached contentSummary — it can drift)
2. Compute new totals from scratch
3. Update `contentSummary` with fresh counts
4. **Keep `currentStage` at its current value** — only advance to stage 4 (Copy) on actual generation runs
5. Sync to dashboard

**Decision rule for regeneration vs. inventory-only:**
- Last run < 7 days AND same qualified leads: → **inventory-only** (this session's pattern)
- Last run ≥ 7 days OR different lead IDs/scores OR stale entries in output: → **regenerate**
- If uncertain, regenerate — running the generator is inexpensive

### contentSummary Drift Warning

The `contentSummary` in `pipeline-state.json` is **not automatically updated** by the content generator script. After a generation run, the summary still shows old counts until manually recomputed. Always count actual files after every run — generation or inventory-only — and update `contentSummary` from those real numbers, never from the previous cached values.

### Reference Files

| File | Pattern | Description |
|------|---------|-------------|
| `references/daily-promotion-run-2026-06-11.md` | Regeneration | Full content generation run (advancing Assets→Copy stage) |
| `references/daily-promotion-run-2026-06-12.md` | Inventory-only | Quick count-and-sync when content is fresh |

## Pitfalls

- **Always sync JSON + HTML + SVGs together** — the HTML fetches JSON at runtime, so mismatched versions cause display errors
- **rsync is additive** — old files on DreamHost persist unless explicitly deleted
- **kanban-data.php syntax** — PHP is picky about `.` vs `->` and missing semicolons. Test with `php -l kanban-data.php` after editing.
- **SVG viewBox** — use `viewBox="0 0 1050 50"` for 8 stages (not the old 6-stage `650`)
- **JSON validation** — always validate JSON files after editing; a single trailing comma breaks the dashboard
- **Pipeline ID consistency** — the `tenant` field in kanban.db must exactly match the `id` in unified-pipeline.json
- **`.htaccess` PHP whitelist** — any new PHP data proxy files must be added to BOTH the `RewriteCond` allow list AND the `RewriteCond` exclusion list in `.htaccess`, or they'll be blocked with 403
- **File permissions** — DreamHost shared hosting requires `0644` for web-accessible files; `0600` or `0664` can cause 403 errors
- **Book catalog completeness** — when updating `unified-pipeline.json`, always include ALL books from `pipeline-books.json` (20 titles), not just the currently active/published ones
- **Virtual Consulting deliverable format** — reports are SINGLE PDFs (not KDP packages). Each PDF: integrated cover + cover letter + TOC + 30+ pages. Old pipeline stages (Qualifier/Buy/Process/Deliverables/Edit) were book-oriented and wrong. Current stages: Lead → Contacted → Survey → Research → Generate Reports → Quality Review → Delivery → Complete.
- **`memory replace` action** — the `content` parameter is the NEW replacement text, `old_text` is the substring identifying the entry to replace. Both are required for the `replace` action. Use `content` for new text and `old_text` for the match string.
- **`read_file` caching** — `read_file` may return cached content with a `dedup: true` flag when called again for the same file. After editing a file with `patch` or `write_file`, re-read the full file (without offset/limit) to get fresh content before making further edits.