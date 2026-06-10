---
name: mifeco-pipeline-management
description: Manage MIFECO product pipeline data — JSON definitions, SVG flow diagrams, kanban DB seeding, and dashboard rendering. Covers the full lifecycle from editing pipeline stages to syncing dashboards to DreamHost.
triggers: ["pipeline", "kanban", "pipeline dashboard", "pipeline data", "pipeline stages", "books pipeline", "saas pipeline", "consulting pipeline", "virtual consulting pipeline", "human consulting pipeline", "books creation", "books marketing", "kanban sync", "seed kanban", "pipeline sync", "rebuild pipeline", "update pipeline", "pipeline flow", "svg flow"]
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