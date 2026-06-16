# Registry Total Discrepancy — Dead Lead Purge — 2026-06-12

## Problem

The master lead registry (`leads-registry.json`) claims `total_leads_all: 18` (consulting: 10, books: 3, saas: 5), but the actual reachable leads in all pipeline JSON files sum to **16** (consulting: 8, books: 3, saas: 5). Every orchestrator run reports a **🔴 FAIL** on registry integrity.

## Root Cause

Two consulting leads — **C-005 "Summit Nonprofit Alliance"** and **C-008 "Golden Gate Tech Incubator"** — were described in the skill documentation as dead leads (`verification_status: "Dead"`). They were **deleted from the `leads[]` array** in `pipeline-consulting.json` but their counts were **never decremented** from the registry:

| Pipeline | Registry `total_leads` | Actual Lead IDs in `leads[]` |
|----------|----------------------|-----------------------------|
| Consulting | 10 | C-001, C-002, C-003, C-004, C-006, C-007, C-009, C-010 = **8** |

The removed leads (C-005, C-008) account for exactly the 2-lead gap.

## Impact

- **Every pipeline orchestrator run** since the leads were deleted (unknown date, but at or after 2026-05-07) reports registry integrity 🔴 FAIL
- **dashboard/pipeline-state.json** inherits the wrong count — shows 16 items/active, but sources from a registry claiming 18
- **Daily reports are permanently damaged** until the registry counters are corrected

## Resolution

Two options, listed in preference order:

### Option A: Decrement registry counters (recommended)

The dead leads have been intentionally purged from the pipeline file. Accept this as reality and fix the registry to match.

1. Edit `leads-registry.json`:
   - `pipelines.consulting.total_leads`: 10 → **8**
   - `total_leads_all`: 18 → **16**
   - `last_updated`: bump to current timestamp
2. Regenerate daily report — expect ✅ PASS

### Option B: Restore dead leads to pipeline JSON

Reverse the purge by re-adding C-005 and C-008 to `pipeline-consulting.json`'s `leads[]` array. Registry counts were correct all along; the pipeline JSON was wrong.

- C-005 Summit Nonprofit Alliance — Dead, value_estimate $199
- C-008 Golden Gate Tech Incubator — Dead, value_estimate $199

Would also restore $398 in pipeline value (inflating the total above what active leads produce).

## What NOT To Do

- Do NOT leave the mismatch unresolved — a permanent 🔴 FAIL on registry integrity cascade-causes dashboard panels to show wrong counts, human weekly reports to cite wrong numbers, and downstream enrichment decisions to operate on stale totals.
- Do NOT restore dead leads just to make the count match if the intent was to remove them permanently. Decrement the registry instead.