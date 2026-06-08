# MIFECO Product Line Inventory — June 3, 2026

> Snapshot of all MIFECO product lines. Last updated: 2026-06-03.
> **Always run a fresh `ls ~/books/` scan** — this file can be stale.

---

## 1. SaaS — Cloud Run Apps (ALL OPERATIONAL as of June 3)

| App | URL | Status | Key Issues |
|-----|-----|--------|------------|
| Project Hypatia Pro | project-hypatia-pro-1064319572465.us-west1.run.app | ✅ Operational | No security headers deployed; no onboarding flow |
| PM Accelerator | project-management-accelerator-845075991286.us-west1.run.app | ✅ Operational | No security headers; SQLite crash risk (writes to ./db) |
| VibraEngineer | vibraengineer-845075991286.us-west1.run.app | ✅ Operational | No security headers; CORS wildcard; SQLite crash risk |
| mifeco.com | mifeco.com | ✅ Operational | All 6 security headers present |

**Known:** gcloud CLI NOT installed — all deployments blocked. Security headers fix coded May 7, never deployed (27 days).
**CDN status:** Resolved as of May 26. All apps load with full styling.
**SQLite crash risk:** VibraEngineer + PM Accelerator write `./database.sqlite` — crashes on Cloud Run (read-only FS except `/tmp`). Must change to `/tmp/database.sqlite` before deploying.
**Pre-deploy checklist created:** `references/pre-deploy-checklist-june2026.md` (June 3, 2026).

---

## 2. Books Pipeline — ALL 19 main catalog books have KDP_PACKAGE + zip ✅

**Total: 19 books** (plus 4 Cindy Lou Legal Capers books).

### KDP_PACKAGE status (ALL 19 COMPLETE):
- ✅ **No Blue Sky Series (5):** Book I-V — all KDP ready
- ✅ **Lunar Foundation Series (4):** Book 1-4 — all KDP ready
- ✅ **Age of Lightships Series (4):** Book 1-4 — all KDP ready (B2-4 are full 40-chapter, 18-21MB EPUBs)
- ✅ **Tomorrow Series (2):** Tomorrow_Remembered, Tomorrow_is_Still_Open — all KDP ready
- ✅ **Business Series (3):** AI_That_Works, Owners_Manual_AI_Agents, The_Crisis_Ready_Company — all KDP ready

### Additional books not in main catalog:
- **Cindy Lou Legal Capers (4):** Book 1-3 + Reader Magnet — all have EPUBs, no KDP packages yet

### New EPUBs since June 2 inventory:
22 .epub files newer than June 2 snapshot — all within existing series (no new books created).

---

## 3. Consulting Pipeline — STALLED

- 10 leads, 0 contacted (stalled since May 15 — 19 days)
- Outreach packet + EdTech one-pager ready
- LinkedIn templates have grammar bugs (need fix)
- Lead profiles lack contact details (no names/emails)
- No email infrastructure
- consultant agent: OFFLINE (Cycle 2)
- sales agent: OFFLINE (Cycle 1)

---

## 4. Agent Status (June 3)

| Agent | Status | Cycle |
|-------|--------|-------|
| brand-advocate | 🔴 OFFLINE | 3+ |
| consultant | 🔴 OFFLINE | 2 |
| sales | 🔴 OFFLINE | 1 |
| engineer | 🔴 OFFLINE | 1 |
| security | 🔴 OFFLINE | 1 |
| researcher | 🟡 Watch | 3 pending tasks (within SLA) |
| publisher | 🔴 OFFLINE | 2 — all KDP work CEO-executed |
| writer | ✅ Active | — |

---

## 5. Key SaaS Fixes Needing Deployment (gcloud blocker)

1. **Security headers** (helmet.js) — coded May 7, 27+ days undeployed
2. **SQLite path fix** — change `./database.sqlite` to `/tmp/database.sqlite` in PM Accelerator + VibraEngineer
3. **Deployment runbook:** `references/deployment-runbook-may2026.md` (24,765 bytes)
4. **Pre-deploy checklist:** `references/pre-deploy-checklist-june2026.md` (3,854 bytes, created June 3)

---

## 6. Critical Market Intel (June 3)

- **MS Project Online retirement:** September 30, 2026 (120 days). No one-click full-fidelity migration path. Complex migrations take 3-6 months. Major opportunity for PM Accelerator.
- **AI PM tools market:** All major players (ClickUp, monday.com, Asana, Linear) now bundling AI as table stakes. Differentiator is the "action layer" between AI and work execution.
- **KDP AI enforcement:** Amazon escalated enforcement April 2026. Sci-fi/fiction = lower enforcement risk. "Human Authored" certification (Authors Guild) now open to all U.S. authors — 3,000 authors certified 5,000 titles.
- **AI consulting market:** $14-47B depending on scope, 25-44% CAGR. 91% of mid-market using AI but 70% need outside help. Boutique firms ($25K-150K engagements) winning mid-market.
- **Outcome-based contracting:** Only 25% of consulting fees linked to outcomes — largest unmet need.
