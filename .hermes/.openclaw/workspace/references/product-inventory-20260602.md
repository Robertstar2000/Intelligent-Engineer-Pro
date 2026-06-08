# MIFECO Product Line Inventory — June 2, 2026

> Snapshot of all MIFECO product lines. Last updated: 2026-06-02.
> **Always run a fresh `ls ~/books/` scan** — this file can be stale.

---

## 1. SaaS — Cloud Run Apps (ALL OPERATIONAL as of June 2)

| App | URL | Status | Key Issues |
|-----|-----|--------|------------|
| Project Hypatia Pro | project-hypatia-pro-1064319572465.us-west1.run.app | ✅ Operational | No security headers deployed; no onboarding flow |
| PM Accelerator | project-management-accelerator-845075991286.us-west1.run.app | ✅ Operational | No security headers; SQLite crash risk (writes to ./db) |
| VibraEngineer | vibraengineer-845075991286.us-west1.run.app | ✅ Operational | No security headers; CORS wildcard; SQLite crash risk |
| mifeco.com | mifeco.com | ✅ Operational | All 6 security headers present |

**Known:** gcloud CLI NOT installed — all deployments blocked. Security headers fix coded May 7, never deployed.
**CDN status:** Resolved as of May 26. All apps load with full styling.
**SQLite crash risk:** VibraEngineer + PM Accelerator write `./database.sqlite` — crashes on Cloud Run (read-only FS except `/tmp`). Must change to `/tmp/database.sqlite` before deploying.

---

## 2. Books Pipeline — ALL 19 books have KDP_PACKAGE + zip ✅

**Total: 19 books** (including Cindy Lou Legal Capers series and Business Series with 3 books).

### KDP_PACKAGE status (ALL 19 COMPLETE):
- ✅ **No Blue Sky Series (5):** Book I Built_from_Dust, Book II Oxygen_Gamble, Book III Rivers_Under_Mars (all upgraded June 2), Book IV Red_Charter, Book V First_Martian_Nation
- ✅ **Lunar Foundation Series (4):** Book 1 Moon_Rock, Book 2 Mooncoming, Book 3 Waters_End, Book 4 Waters_Horizon
- ✅ **Age of Lightships Series (4):** Book 1 Sunward_Exodus, Book 2 Mercury_Accord, Book 3 Ghosts_Beyond_Neptune, Book 4 Last_Photon_Fleet
- ✅ **Tomorrow Series (2):** Tomorrow_Remembered, Tomorrow_is_Still_Open
- ✅ **Business Series (3):** AI_That_Works, Owners_Manual_AI_Agents, The_Crisis_Ready_Company

### Additional books not in main catalog:
- **Cindy Lou Legal Capers (4):** Book 1 Retainer_to_Trouble, Book 2 Clause_for_Alarm, Book 3 Affidavits_and_Alibis, Reader Magnet — all have EPUBs but no KDP packages yet

### Series:
- **No Blue Sky** (5 books) — Complete, all KDP ready
- **Lunar Foundation** (4 books) — Complete, all KDP ready
- **Age of Lightships** (4 books) — Complete, all KDP ready (B2-4 are full 40-chapter, 18-21MB EPUBs)
- **Tomorrow** (2 books) — Complete, all KDP ready
- **Business** (3 books) — Complete, all KDP ready
- **Cindy Lou Legal Capers** (3+ books) — Written, needs KDP packages

---

## 3. Consulting Pipeline — STALLED

- 10 leads, 0 contacted
- Outreach packet + EdTech one-pager ready
- No email infrastructure
- consultant agent: OFFLINE (Cycle 2)

---

## 4. Agent Status (June 2)

| Agent | Status | Cycle |
|-------|--------|-------|
| brand-advocate | 🔴 OFFLINE | 3+ |
| consultant | 🔴 OFFLINE | 2 |
| sales | 🔴 OFFLINE | 1 |
| engineer | 🔴 OFFLINE | 1 |
| security | 🔴 OFFLINE | 1 |
| researcher | 🟡 Watch | 1 (2 pending, within SLA) |
| publisher | 🔴 OFFLINE | 2 — all KDP work CEO-executed |
| writer | ✅ Active | — |

---

## 5. Key SaaS Fixes Needing Deployment (gcloud blocker)

1. **Security headers** (helmet.js) — coded May 7, 25+ days undeployed
2. **SQLite path fix** — change `./database.sqlite` to `/tmp/database.sqlite` in PM Accelerator + VibraEngineer
3. **Deployment runbook:** `references/deployment-runbook-may2026.md` (24,765 bytes)

## 6. Critical Market Intel (June 2)

- **MS Project Online retirement:** September 30, 2026 (121 days). Microsoft's successor (Planner) is a downscope. Migration wave opportunity for PM Accelerator.
- **KDP AI disclosure escalation:** Amazon escalated enforcement April 2026. Sci-fi/fiction = lower enforcement risk. Human-authored positioning = competitive advantage.
- **AI book flood:** 1,100+ AI titles/week on KDP. "Human Authored" certification gaining traction. Quality polarization favors proven human authors.
