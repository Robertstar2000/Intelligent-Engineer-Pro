---
name: pipeline-dedup-discovery
description: Pipeline deduplication and discovery system — maintains a master lead registry, prevents duplicate leads from being added across pipeline runs, and provides a CLI dedup checker. Integrates with the daily pipeline orchestrator as Step 0.
version: 1.3.0
author: MIFECO
tags: [pipeline, dedup, discovery, leads, crm, enrichment]
related_skills:
  - sales-pipeline-infrastructure
---

## 🔍 MemPalace Query (MANDATORY FIRST STEP)
Before proceeding, query MemPalace for existing context:
```python
import sys, os; sys.path.insert(0, os.path.expanduser('~/.hermes/mempalace'))
import embed; embed.init_embedding(os.path.expanduser('~/.hermes/mempalace'))
results = embed.search_embeddings("pipeline deduplication discovery lead registry", k=5)
```
This retrieves previous decisions, domain-specific context, and lessons learned from the vector memory store.

# Pipeline Dedup & Discovery System

## Overview

This skill ensures every lead across all three MIFECO pipelines (Books, Consulting, SaaS) is unique. It maintains a **Master Lead Registry** (`leads-registry.json`) and provides a **dedup check tool** (`dedup-check.py`) that prevents duplicate leads from being processed across pipeline runs.

## When to Use

- **Before adding any new lead** to any pipeline — always run the dedup check
- **At the start of every pipeline orchestrator run** — Step 0: dedup discovery check
- **When enriching leads** — check registry to avoid registering duplicates
- **When cleaning up pipelines** — cross-reference leads against the registry

## Files & Locations

| File | Path | Purpose |
|------|------|---------|
| **Master Lead Registry** | `pipeline-engine/data/leads-registry.json` | Canonical index of all processed leads |
| **Dedup Check Script** | `pipeline-engine/data/dedup-check.py` | CLI tool for duplicate detection |
| **Pipeline SaaS** | `pipeline-engine/data/pipeline-saas.json` | SaaS pipeline (referenced by registry) |
| **Pipeline Consulting** | `pipeline-engine/data/pipeline-consulting.json` | Consulting pipeline |
| **Pipeline Books** | `pipeline-engine/data/pipeline-books.json` | Books pipeline |
| **Unified Pipeline** | `pipeline-engine/data/unified-pipeline.json` | Cross-pipeline unified view |

> **⚠️ Working Directory:** All relative paths resolve under the pipeline root at `/home/bob/.hermes/pipeline-engine/`. When running from cron or a non-standard directory, use this absolute path or set it as the workdir.

## Dedup Check — How to Use

### Single Lead Check
```bash
python3 pipeline-engine/data/dedup-check.py "<full name>" "<organization>" "<email>"
```

Returns:
```json
{"is_duplicate": true, "match": { "source_pipeline": "SaaS", "organization": "HealthBridge Tech", ... }}
```
or
```json
{"is_duplicate": false}
```

### Batch Check (for multiple new leads)
Pipe a JSON array of lead objects to stdin:
```bash
cat new-leads.json | python3 pipeline-engine/data/dedup-check.py
```

Input format:
```json
[
  {"name": "Jane Doe", "company": "Acme Corp", "contact_email": "jane@acme.com"},
  ...
]
```

Response:
```json
{"results": [...], "duplicates_found": 1}
```

## Dedup Logic (3-Layer)

1. **Exact key match** — `lead_key = "name|org|email"` (fully normalized, lowercased, trimmed)
2. **Email match** — Same email address = same person = duplicate regardless of org
3. **Email domain + name match** — Same domain AND same person name = duplicate (catches same person using different org names, e.g. "Hope Fellowship" vs "Hope Fellowship Community Center")
4. **Same domain, different person** — NOT a duplicate. **Multiple contacts from the same organization are allowed.** This is intentional — you can message a CEO, a VP, and a team lead from the same company without them being flagged as duplicates.

## Registering a New Lead

After the dedup check passes, register the new lead by appending to `leads-registry.json`:

```json
{
  "lead_key": "jane doe|acme corp|jane@acme.com",
  "source_pipeline": "SaaS",
  "original_id": "S-11",
  "name": "Jane Doe",
  "organization": "Acme Corp",
  "email": "jane@acme.com",
  "current_stage": 1,
  "value_estimate": null,
  "registered_at": "2026-05-02T14:00:00Z",
  "status": "active"
}
```

## Pipeline Orchestrator Integration

This skill provides **Step 0** of the daily pipeline orchestrator run. The full daily workflow (days-in-stage calculation, blocker detection, email queue generation, and report creation) is documented in the **[`sales-pipeline-infrastructure`](/home/bob/.hermes/skills/business/sales-pipeline-infrastructure/SKILL.md)** skill under **STEP 6 / STEP 6.1**.

### Step 0: Dedup Discovery Check

Run before all other orchestrator operations:

```
STEP 0: DEDUP DISCOVERY CHECK
  1. Read leads-registry.json
  2. For any new lead being considered: run dedup-check.py
  3. If duplicate → skip + log to report
  4. If new → append to leads-registry.json
  5. Verify registry lead count matches total across all pipeline files
```

### Full Orchestrator Steps (for reference)

The daily orchestrator (cron at 8am Monday–Friday, workdir=`/home/bob/.hermes/pipeline-engine/`) performs these steps in order:

| Step | What It Does | Skill |
|------|-------------|-------|
| **Step 0** | Dedup discovery check + registry integrity | This skill |
| **Step 1** | Read all pipeline JSON files and nurture sequences | `sales-pipeline-infrastructure` |
| **Step 2** | Calculate days-in-stage for each lead | `sales-pipeline-infrastructure` |
| **Step 3** | Apply pipeline-specific blocker thresholds | `sales-pipeline-infrastructure` |
| **Step 4** | Detect nurture sequence content discrepancies | `sales-pipeline-infrastructure` |
| **Step 5** | Generate today's email queue + 7-day projection | `sales-pipeline-infrastructure` |
| **Step 6** | Save structured health report to `data/daily-pipeline-report.md` | `sales-pipeline-infrastructure` |
| **Step 7** | Verify lead registry integrity (cross-reference counts) | This skill + `sales-pipeline-infrastructure` |

### Cron Schedule Pattern

```bash
# Create the daily pipeline orchestrator cron job:
cronjob action=create \
  schedule="0 8 * * 1-5" \
  name="Pipeline Orchestrator — Daily" \
  workdir=/home/bob/.hermes/pipeline-engine \\
  skills='["business/pipeline-dedup-discovery", "business/sales-pipeline-infrastructure"]' \
  prompt="Run the daily pipeline orchestrator: read all data/pipeline-*.json, sequences/*.json, and leads-registry.json; calculate days-in-stage; apply blocker thresholds; generate email queue; and save report to data/daily-pipeline-report.md"
```

> **Important:** The `workdir` parameter ensures all relative paths (`pipeline-engine/data/`, `sequences/`) resolve correctly. Without it, cron sessions running from an arbitrary directory will fail to find the pipeline files.

## Registry Format Compatibility

The registry uses an **aggregate format** (pipeline-level IDs only, no lead detail fields):

```json
{
  "pipelines": {
    "books": { "leads": ["lead-001", "lead-004", ...] },
    "saas": { "leads": ["lead-003", ...] }
  },
  "total_leads_all": 18
}
```

The dedup script automatically detects this format and sources actual lead data (name, org, email) from `unified-pipeline.json` (or individual pipeline JSONs as fallback). It also supports the legacy **individual format** (flat list of dicts with `lead_key`/`name`/`email`/`organization` fields).

Field name normalization across pipelines:

| Pipeline | Name Field | Org Field | Email Field |
|----------|-----------|-----------|-------------|
| **SaaS** | `name` | `company` | `email` |
| **Books** | `contact.name` | `contact.organization` | `contact.email` |
| **Consulting** | `contact_name` | `company_name` | `contact_email` |
| **Unified** | `enrichment.contact_name` | `enrichment.company_name` | `enrichment.email` |

## Pitfalls

| Pitfall | Why It Happens | How to Avoid |
|---------|---------------|--------------|
| **Registry uses aggregate format** | `leads-registry.json` only stores pipeline-level IDs | Fix already applied: `dedup-check.py` auto-detects and builds dedup index from `unified-pipeline.json` |
| **Per-pipeline `leads` arrays are POC SAMPLES, not exhaustive** | Registry shows books: 5 IDs, consulting: 4, saas: 4 — but actual lead counts are 3, 10, 5. These arrays appear to be proof-of-concept examples, not comprehensive lists. | NEVER use `len(registry['pipelines'][p]['leads'])` for count verification. Use `registry['pipelines'][p]['total_leads']` and `registry['total_leads_all']` as the authoritative counts. |
| **Unified pipeline has DIFFERENT data, not just fewer leads** | `unified-pipeline.json` stores enrichment/persona data with names, orgs, and emails that often DON'T MATCH the actual pipeline JSON records. Example: actual books B-001 is "Dr. Sarah Chen, Northfield Academy, schen@northfieldacademy.edu" but unified lead-001 is "Sarah Chen, Galactic Reads Bookstore, sarah@galacticreads.com". Because `dedup-check.py` builds its dedup index from unified-pipeline.json (when registry uses aggregate format), the name/org/email triples never match — so it returns `{"is_duplicate": false}` for EVERY actual pipeline lead. | Do NOT rely on `dedup-check.py` for verifying existing leads are in the registry — it will always return false for actual pipeline leads due to the unified data mismatch. For that, cross-reference pipeline IDs directly against the registry's `pipelines[].leads[]` arrays. The dedup check is only reliable for catching true duplicates of truly NEW leads that haven't been through the pipeline system before. After running dedup-check against any lead, verify by testing against a known-registered lead first to confirm the index reflects your actual data. |
| **Enrichment engine `--report` misreads pipeline structure** | `enrichment-engine.py --report` calls `data.get(\"leads\", ...)` on each pipeline JSON file, but the actual data lives at `data[\"pipeline\"][\"leads\"]`. This means the report only finds 1 lead total (the first unrelated key) instead of all leads. | Use the enrichment engine for stale-detection heuristics only. For accurate per-lead enrichment status, read each pipeline JSON directly and check individual `enriched_at`, `verification_status`, and `contact_email` fields. The reusable `scripts/daily-pipeline-analysis.py` handles this correctly. |
| **Case sensitivity** | "Acme Corp" vs "acme corp" | Lead_key normalizes to lowercase |
| **Whitespace** | " John " vs "John" | Script trims all values |
| **Same org, different person** | Both at HealthBridge Tech | Fixed: only blocks same email OR same name+domain |
| **Empty contact fields** | Consulting leads have no names/emails yet | Registry stores what exists — flagged for enrichment |
| **Old leads not in registry** | Leads added before registry existed | Pipeline orchestrator re-indexes them on first run |
| **Date format variance** | Consulting pipeline uses date-only (`2026-05-07`) while Books/SaaS use full ISO timestamps (`2026-05-07T14:00:39Z`). Registry entries store `registered_at` as ISO. | Any cross-reference script must handle both date formats. Use `datetime.fromisoformat()` for ISO and `datetime.strptime(..., '%Y-%m-%d')` for date-only strings.

## Enrichment Flow

When enriching leads:
1. Run dedup check against any newly discovered contact info
2. If contact name/email found for a lead that had none → update the registry entry
3. Update `enriched_at` timestamp in both pipeline JSON and registry

## Step 7: Registry Integrity — Resolving Count Mismatches

When Step 7 flags a registry count mismatch (e.g., registry claims 10 consulting leads but only 8 exist in the pipeline file), follow this diagnostic flow:

1. **Compare registry `total_leads` counts vs actual lead IDs in each pipeline JSON**
2. **Identify missing leads** — cross-reference lead IDs (C-001, C-002, etc.) against the registry's `pipelines[p].leads[]` arrays
3. **Two resolution paths:**

   | Scenario | Resolution |
   |----------|-----------|
   | **Lead was moved to closed_lost** (exists in pipeline JSON at stage 9 but missing from registry) | Add it back to the pipeline JSON's `leads` array as-is; registry count is correct |
   | **Lead was deleted from pipeline JSON entirely** (dead lead purged from file) | Decrement the registry's `pipelines[p].total_leads` and `total_leads_all` to match actual counts. Do NOT restore deleted dead leads just to satisfy the count — the count should reflect reality |

4. After fixing, update `last_updated` in the registry and regenerate the daily report to confirm ✅ PASS

> **Key principle:** The registry's `total_leads_all` must equal the sum of all actual lead entries in all pipeline JSON files. When leads are deliberately removed from pipeline files (e.g., dead leads purged from `pipeline-consulting.json`), decrement the registry counters in lockstep. Never leave a gap — a permanent 🔴 FAIL means downstream dashboards, reports, and daily briefings all inherit a broken number.

## Maintenance

- Registry is append-only — never delete entries (set `status: "inactive"` instead). However, when leads are **removed from pipeline JSON files** (e.g., dead leads C-005, C-008 deleted from `pipeline-consulting.json`'s `leads` array), you MUST decrement the registry's `pipelines[p].total_leads` and `total_leads_all` counters to match. Otherwise every orchestrator run reports a permanent 🔴 FAIL.
- Pipeline orchestrator detects registry mismatches and flags them in the daily report
- **Dead leads still count toward pipeline value** — Leads with `verification_status: "Dead"` (e.g., C-005 "Summit Nonprofit Alliance", C-008 "Golden Gate Tech Incubator") that are still present in the pipeline JSON retain their original `value_estimate`. This inflates total pipeline value. Either mark dead leads as `closed_lost` (move to final stage) or set `value_estimate: 0` so they don't skew pipeline totals. If you delete dead leads from the JSON file instead, also decrement the registry counters (see above).
