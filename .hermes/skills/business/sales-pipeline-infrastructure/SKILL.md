---
name: sales-pipeline-infrastructure
description: "Build a complete lead-to-revenue pipeline automation system for MIFECO's four product lines aligned with promotion modes: Books (Creation + Marketing) for Book Promotion, SaaS for SaaS Marketing, Human Consulting for Human Consulting Marketing, Virtual Consulting for Virtual Consulting Marketing. Each has intake forms, data trackers, email nurture sequences, LinkedIn discovery, social media content generation, content deployment dashboard with SEND/DELETE, unified cross-product pipeline, and cron-based orchestration."
version: 3.0.0
author: Hermes Agent
tags:
  - sales
  - pipeline
  - lead-generation
  - email-nurture
  - dashboard
  - automation
  - agentmail
  - book-promotion
  - saas-marketing
  - consulting-marketing
related_skills:
  - ceo-agent-orchestrator
  - virtual-consulting
  - complex-task-orchestration
  - book-marketing-launch
  - pipeline-dedup-discovery
  - openclaw-marketing
  - openclaw-brand-advocacy
---

## 🔍 MemPalace Query (MANDATORY FIRST STEP)
Before proceeding, query MemPalace for existing context:
```python
import sys, os; sys.path.insert(0, os.path.expanduser('~/.hermes/mempalace'))
import embed; embed.init_embedding(os.path.expanduser('~/.hermes/mempalace'))
results = embed.search_embeddings("sales pipeline infrastructure lead-to-revenue automation", k=5)
```
This retrieves previous decisions, domain-specific context, and lessons learned from the vector memory store.

# Multi-Product Sales Pipeline Infrastructure

## Trigger Conditions

Use this skill when building or modifying lead-to-revenue pipeline systems, dashboards, enrichment engines, cron orchestration, or content deployment views. Covers setup from scratch AND ongoing operations.

## Architecture (v2 — 5 Product Pipelines)

```
LEAD SOURCE → CAPTURE → SCORE → NURTURE → CONVERT → ONBOARD
AgentMail inboxes (1 per product line)
5 Product Pipelines: books-creation, books-marketing, saas, human-consulting, virtual-consulting
```

**2026-06-09 Migration: 9 → 5 pipelines.** The old architecture had separate creation/publishing/deployment pipelines per product line (9 total). The new architecture collapses to 5 product-aligned pipelines, each representing an end-to-end go-to-market flow. See `references/pipeline-migration-2026-06-09.md` for the full mapping of old→new pipeline IDs and stage remapping.

## The 5 Product Pipelines (8 Stages Each)

### 2.1a Books Creation Pipeline
**Stages:** Review Market → Build Book Bible → Build Framework → Write → Enrich → Edit → Prep for KDP → Finish
**Products:** No Blue Sky series (5 vols), The Lunar Foundation series (3 vols), Tomorrow Remembered, AI That Works for Small Business
**Email:** bigtruck444@agentmail.to | **Nurture:** 4-email sequence over 14 days

### 2.1b Books Marketing Pipeline
**Stages:** Marketing Content → Infographic → Discovery → Promote → Outreach → Nurture Sequence → Analyze Results → Optimize Campaigns
**Products:** Same as Books Creation
**Email:** bigtruck444@agentmail.to | **Nurture:** 4-email sequence over 14 days

### 2.2 SaaS Pipeline
**Stages:** Identified → Contacted → Qualified → Process → Demo/Free Trial → Complete Transaction → Followup → Upsell/Cross-sell
**Products:** Project Hypatia Pro ($99/mo), PM Accelerator ($69/mo), VibraEngineer ($29/mo)
**Email:** carefulvehicle192@agentmail.to | **Nurture:** 7-email sequence over 21 days

### 2.3a Human Consulting Pipeline
**Stages:** Lead → Contact → Qualified → Intent → Strategy Session → Proposal Sent → Negotiation → Closed Won
**Services:** Strategy Session ($199), Deep-Dive ($1,499), Full Transformation ($3,999)
**Email:** crowdedbutton536@agentmail.to | **Nurture:** 5-email sequence over 10 days

### 2.3b Virtual Consulting Pipeline
**Stages:** Lead → Contacted → Qualifier → Buy → Process → Deliverables → Edit → Complete Delivery
**Products:** Strategy Session ($199), Deep-Dive ($1,499), Full Transformation ($3,999)
**Email:** backdoor@mifeco.com | **Nurture:** None (self-service via web)

## Pipeline Operations Data Layer (Shared State JSON)

When syncing Pipeline Ops numbers with Content CC, build a **pipeline-state.json** at `pipeline-engine/data/pipeline-state.json` as the single source of truth. Copy into `dashboard/` for HTTP serving (server blocks directory traversal). This is a display-oriented summary with `monthlyTarget` (not daily), `cronJob`/`cronSchedule` references, `skills` arrays, `contentCCViewer` field, and `contentSummary` object.

**Key differences from per-pipeline JSON files:** pipeline-state.json uses monthlyTarget (not daily), includes cron job mapping, skills references, and contentCCViewer cross-reference. Both dashboards load it via `fetch('pipeline-state.json')` on page load.

Create a master sync runner at `pipeline-engine/scripts/run-all-pipelines.sh` that runs data sync and copies state to dashboard. Add a cron job at 8:15 AM daily (15 min after main orchestrator).

**Monthly vs Daily conversion:** When user requests monthly targets, convert daily × 30, rename key `dailyTarget`→`monthlyTarget`, relabel "Daily Target"→"Monthly Target".

**Cron job mapping:** Each pipeline object has `cronJob` (name) and `cronSchedule` (cron expression). Display in card footer.

**Pipeline skills reference:** Each pipeline has a `skills` array. Display as ⚡ tag chips in card and flow modal for task delegation context.

## Key Files

```
pipeline-engine/
├── data/
│   ├── pipeline-state.json       ← Shared source of truth (ALL pipelines)
│   ├── pipeline-{product}.json   ← Per-product pipeline trackers (Books/SaaS/Consulting)
│   ├── unified-pipeline.json     ← Optional cross-product view
│   ├── leads-registry.json       ← Canonical lead list for dedup
│   ├── dedup-check.py            ← CLI dedup tool
│   ├── enrichment-engine.py      ← Stale detection
│   ├── content-generator.py      ← Social/blog post generation
│   ├── social-content-*.json     ← Generated posts per product
│   ├── linkedin-outreach-messages.json
│   ├── linkedin-automation.sh
│   ├── daily-pipeline-report.md  ← Orchestrator output
│   └── outreach/                 ← Generated emails/SVGs
├── scripts/
│   ├── pipeline-sync.py          ← Reads real data, updates pipeline-state.json
│   ├── pipeline_data_api.py      ← POST API: advance-lead, mock-inbox, clear-mock-inbox
│   ├── daily-pipeline-analysis.py ← Full 7-step orchestrator analysis (reusable)
│   └── run-all-pipelines.sh      ← Master cron runner
├── sequences/{product}-nurture.json
├── forms/{product}-intake.html
├── data/
│   ├── mock-inbox.json           ← Test-mode sent emails (created by pipeline_data_api.py)
│   └── ...
└── dashboard/
    ├── pipeline-dashboard.html   ← Pipeline Command Center
    ├── outreach-dashboard.html   ← Send interface (API-powered, mode toggle, mock inbox viewer)
    ├── pipeline-state.json        ← Copy of state for HTTP serving
    └── flows/*.svg               ← Pipeline flow diagrams
```

## 4-Panel MIFECO Dashboard Template

The dashboard at `pipeline-engine/dashboard/pipeline-dashboard.html` follows a dark-themed (#0f172a bg, #00ffcc accent) multi-panel layout with fixed sidebar:

1. **📚 Books Catalog** — Auto-adapting grid of book cards with status badges (ideation/written/edited/packaged/published)
2. **☁️ SaaS Applications** — Cards with GitHub/prod/local links, online/offline status dots
3. **💼 Virtual Consulting** — Tier pricing grid, pipeline flow modal
4. **📊 Lead & Promotion** — Cross-pipeline stats, outreach engine status, nurture sequence status
5. **⚙️ Pipeline Operations Center** — 5 pipeline cards (books-creation, books-marketing, saas, human-consulting, virtual-consulting) with run/pause/stop controls, progress bars, monthly thresholds, cron job mapping, skills display, and flow diagram modal
6. **🩺 Pipeline Health** — Per-pipeline operational status cards

### Outreach Dashboard (Send Interface)

At `dashboard/outreach-dashboard.html`: Enriched lead cards organized by pipeline (Books/SaaS/Consulting) with:

- **Mode toggle** — 🧪 Test mode (emails go to mock inbox, viewable inline) / 🚀 Production mode (emails sent via WordPress REST → DreamHost SMTP)
- **API-powered sends** — Clicking "Send" calls `POST /api/advance-lead`, advancing the lead's stage in the pipeline JSON from "Lead Inbox" → "Contacted"
- **Mock inbox panel** — Visible in test mode, shows all sent emails with body previews
- **Email enrichment gate** — Only leads with valid emails get Send buttons
- **Filter bar** — By pipeline (Books/SaaS/Consulting) or readiness (Ready / Needs Enrichment)

**Note:** The spec-described `dashboard/content-command-center.html` (6 viewer tabs) is NOT deployed. The outreach dashboard serves as the primary send interface.

### Dashboard Data Loading

Both dashboards load `pipeline-state.json` dynamically on page load. Pipeline Ops overlays data on static defaults. Content CC updates sidebar stats from `contentSummary`. The JSON file must be in the dashboard directory.

## First-Run Setup

Before the cron orchestrator can run, deploy the bundled scripts from the skill bundle to the project directory:

```bash
# Copy the reusable analysis script (bundled with this skill)
cp /home/bob/.hermes/skills/business/sales-pipeline-infrastructure/scripts/daily-pipeline-analysis.py \
   /home/bob/.hermes/pipeline-engine/scripts/daily-pipeline-analysis.py

# Ensure scripts/ directory exists in pipeline-engine
mkdir -p /home/bob/.hermes/pipeline-engine/scripts
```

The analysis script lives in the skill bundle and must be deployed to `pipeline-engine/scripts/` before first use. Without this copy, `python3 scripts/daily-pipeline-analysis.py` will fail with "No such file".

## Cron Orchestration

- **8:00 AM** — Pipeline Orchestrator (dedup + data reading + stage calc + report)
- **8:00 AM** — CEO Agent (business assessment + task assignment)
- **8:15 AM** — Pipeline Ops Sync (runs sync script, copies state to dashboard)
- **8:30 AM** — Promotion Generation (content check + state update)
- **8:30 AM** — Dashboard Sync (deploy to mifeco.com)
- **Sunday 8:00 AM** — Backlink Acquisition (weekly)

All cron jobs are read-only. They report what needs doing; humans/CEO agent make changes.

## Process Overview

1. **Define architecture** (ARCHITECTURE.md with stages, inboxes, products)
2. **Create per-product pipeline trackers** (JSON with stages/leads/ICP scores)
3. **Set up lead registry & dedup** (leads-registry.json + dedup-check.py)
4. **Build intake forms** (POST to AgentMail)
5. **Create nurture sequences** (SaaS 7, Consulting 5, Books 4)
6. **Build dashboards** (Pipeline CC + Content CC)
7. **Set up cron orchestration** (report → state → cycle)
8. **LinkedIn discovery** (browser guide + automated messages)
9. **Social media content** (per-platform per-product posts)
10. **Enrichment operations** (lead verification, scoring, outreach generation)
11. **Pipeline date resets** (fresh start when needed)
12. **Product changes** (multi-file update pattern: JSON → Sequence → Dashboard → Content CC)
13. **Unify pipelines** (optional cross-product view)
14. **Pipeline audit** — Full audit checklist and current-state snapshot at `references/pipeline-audit-2026-06-05.md`

## Pitfalls

- **Shared state file must be in dashboard/ directory** — HTTP server blocks directory traversal above serving root
- **Both dashboards must load pipeline-state.json** — Pipeline Ops for pipeline counts, Content CC for sidebar stats
- **Monthly targets not daily** — Users prefer monthly ×30 scaling
- **No automated email sending** — Every email needs individual human approval via the Send button
- **Leads don't advance when "sent" via dashboard alone** — The outreach dashboard's localStorage-only send doesn't update the pipeline JSON files. You MUST wire up a server-side API (`pipeline_data_api.py`) that:
  1. Receives `POST /api/advance-lead` with pipeline, lead_name, mode
  2. Updates the lead's `current_stage` from 1→2 in the appropriate `pipeline-{product}.json` file
  3. In test mode: writes to `mock-inbox.json` for review
  4. In production mode: calls the WordPress REST endpoint for real sending
  Without this, leads stay at "Lead Inbox" forever regardless of how many Send buttons are clicked
- **9 pipelines → 5 product pipelines migrated 2026-06-09** — Pipeline data files now use `books-creation`, `books-marketing`, `saas`, `human-consulting`, `virtual-consulting` IDs. Stage arrays, lead mappings, and dashboard state JSON all updated in lockstep.
- **JSON patch escape issues** — Write files fresh when body contains escaped newlines
- **Pipeline data and dashboard arrays must stay in sync** — Always update both
- **Content Command Center may not be deployed** — The spec-defined `content-command-center.html` may not exist. Check first: if absent, use/update `outreach-dashboard.html` which has the mode toggle and mock inbox viewer built-in
- **Date format variance between pipelines** — Books/SaaS use full ISO timestamps (`2026-05-07T14:00:39Z`) while Consulting uses date-only strings (`2026-05-07`). Any script that calculates days-in-stage must handle both formats. Use `datetime.fromisoformat()` for ISO and `datetime.strptime(..., '%Y-%m-%d')` for date-only. The reusable `scripts/daily-pipeline-analysis.py` handles this automatically.
- **Enrichment engine ignores nested `pipeline.leads` structure** — `enrichment-engine.py --report` calls `data.get("leads", ...)` on each pipeline JSON file, but the actual nesting is `data["pipeline"]["leads"]`. This means `--report` only examines 1 lead total — not all leads. For accurate per-lead enrichment status, read the pipeline JSON directly and check each lead's `enriched_at` / `verification_status` / `contact_email` fields. The `--report` mode is only useful for its stale-detection heuristic on the first matched lead.
- **Orchestrator script available as reusable tool** — The full 7-step analysis (days-in-stage, blockers, nurture health, email queue, projection, registry integrity) is available as `scripts/daily-pipeline-analysis.py`. Run it from the pipeline-engine/ directory with `python3 scripts/daily-pipeline-analysis.py` to get the full report on stdout. Redirect to `data/daily-pipeline-report.md` to save.
- **Content generator references Ghost CMS, but site runs WordPress** — `pipeline-engine/data/content-generator.py` contains Ghost API constants and calls. It will fail against the WordPress REST API. Either adapt the generator to use WordPress endpoints (`/wp-json/wp/v2/posts`) or use generic HTTP posting. Same issue affects `backlink-acquisition.py`.
- **Auto-advance rules in JSON aren't executed** — `pipeline-saas.json` defines `auto_advance_rules` (e.g., stage 1→2 after 7 days), but `daily-pipeline-analysis.py` has no code path to read or execute these rules. Leads with `stage: 1` and `created_at` older than 7 days will NOT auto-advance. Either implement auto-advance in the orchestrator or advance leads manually via the outreach dashboard.
- **Pipeline summary counts don't match actual lead stages** — `pipeline-consulting.json` summary shows `"lead": 10` but only 1 lead is actually at stage 2 (`"contacted"`). The summary object is not recalculated when individual lead stages change. Always count actual lead stages from the `leads` array, never trust summary counts.

## DreamHost Pipeline Dashboard Deployment

The pipeline dashboard lives at `pipeline-engine/dashboard/` and is deployed to `mifeco.com/admin/` via rsync over SSH. Use the `sync_dashboard.py` script:

```bash
cd /home/bob/.hermes/pipeline-engine && python3 scripts/sync_dashboard.py
```

This uses pexpect to handle the SSH password from `~/.hermes/.env` (DREAMHOST_PASSWORD var). The password is for `dh_mwpxuu@iad1-shared-b8-42.dreamhost.com`.

**Key:** Always sync both data JSON files AND the HTML dashboard AND the SVG flows in one rsync run. The dashboard HTML fetches JSON via `fetch()` at runtime, so stale JSON = stale display.

**Cleanup old files:** Use `scripts/cleanup_dreamhost.py` to remove obsolete SVG/HTML files that rsync alone won't delete (rsync additive by default, not --delete).