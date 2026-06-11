# Dedup Data Alignment Discovery — 2026-06-10

## Problem

`dedup-check.py` builds its dedup index from `unified-pipeline.json` when the registry is in aggregate format. But the unified pipeline stores **enrichment/persona data** that doesn't match the actual pipeline lead records. This causes all dedup checks against actual pipeline leads to return false negatives.

## Concrete Mismatches Found

The following leads exist in both `unified-pipeline.json` and the actual pipeline JSONs, but with **completely different** name/org/email triples:

### Books Pipeline

| Field | Pipeline JSON (B-001) | Unified (lead-001) |
|-------|----------------------|---------------------|
| Name | Dr. Sarah Chen | Sarah Chen |
| Org | Northfield Academy | Galactic Reads Bookstore |
| Email | schen@northfieldacademy.edu | sarah@galacticreads.com |

### Consulting Pipeline

| Field | Pipeline JSON (C-001) | Unified (lead-002) |
|-------|----------------------|---------------------|
| Name | Phillip Berry | Dr. James Rodriguez |
| Org | Northwind Health Partners | MedTech Innovations Inc. |
| Email | pberry@northwindhealth.com | jrodriguez@medtechinnovations.com |

### SaaS Pipeline

| Field | Pipeline JSON (S-001) | Unified (lead-003) |
|-------|----------------------|---------------------|
| Name | Sarah Chen | Mike O'Brien |
| Org | TechFlow Labs | BuildRight Construction |
| Email | schen@techflowlabs.io | mike@buildrightconstruction.com |

## Impact

Running `dedup-check.py` against ANY actual pipeline lead always returns:

```json
{"is_duplicate": false}
```

Even for leads that have been in the registry for weeks. The dedup check is only useful for **truly new external leads** whose data hasn't been through any pipeline system.

## Root Cause

`unified-pipeline.json` is not a cross-reference of pipeline leads — it's a separate convenience view with different enrichment/persona data. It was never designed to mirror actual pipeline lead records. The names, orgs, and emails in it come from a different enrichment process than the one that populated the per-pipeline JSON files.

## Workaround

For registry integrity checks on existing leads:
1. Read `leads-registry.json` and cross-reference by *pipeline ID* (B-001, S-001, C-001), not by name/org/email
2. Verify counts manually: count actual leads in each `pipeline-{product}.json` and compare against `registry['pipelines'][p]['total_leads']`
3. Use `dedup-check.py` ONLY for new external leads that haven't been through pipeline processing

## Long-term Fix (if desired)

Either:
- A. Rebuild `unified-pipeline.json` to reflect actual pipeline lead data (extract contact fields per the field-name normalization table)
- B. Have `dedup-check.py` fall back to per-pipeline JSON files when the registry uses aggregate format, rather than relying solely on unified-pipeline.json
- C. Migrate the registry from aggregate format to individual format (flat list with `lead_key`/`name`/`email`/`organization` per entry)