# MIFECO Product Line Inventory — June 5, 2026

> Snapshot of all MIFECO product lines. Last updated: 2026-06-05.
> **Always run a fresh `ls ~/books/` scan** — this file can be stale.

---

## 1. SaaS — Cloud Run Apps (ALL OPERATIONAL as of June 5)

| App | URL | Status | Key Issues |
|-----|-----|--------|------------|
| Project Hypatia Pro | project-hypatia-pro-1064319572465.us-west1.run.app | ✅ Operational | No security headers deployed; no onboarding flow |
| PM Accelerator | project-management-accelerator-845075991286.us-west1.run.app | ✅ Operational | No security headers; SQLite crash risk (writes to ./db) |
| VibraEngineer | vibraengineer-845075991286.us-west1.run.app | ✅ Operational | No security headers; CORS wildcard; SQLite crash risk |
| mifeco.com | mifeco.com | ✅ Operational | All 6 security headers present |

**Known:** gcloud CLI NOT installed — all deployments blocked. Security headers fix coded May 7, never deployed (29 days).

---

## 2. Books Pipeline — 22/22 books complete with KDP_PACKAGE + EPUB

**Total: 22 books** (19 main catalog + 3 Cindy Lou Legal Capers)

### KDP_PACKAGE status (ALL COMPLETE as of June 5):
- ✅ **All 22 books** have KDP_PACKAGE/ directory with EPUB in Kindle/
- ✅ **All main 19** have KDP_PACKAGE.zip files
- ✅ **Cindy Lou B1-3** have KDP_PACKAGE dirs + zips (created June 5)

### Series:
- **No Blue Sky** (5 books) — All KDP ready ✅ (B1-5 have EPUBs in KDP_PACKAGE/Kindle/)
- **Lunar Foundation** (4 books) — All KDP ready ✅
- **Age of Lightships** (4 books) — All KDP ready ✅ (B2-4 have 18-21MB EPUBs with 40 ch each)
- **Tomorrow** (1 book) — KDP ready ✅ (flat structure, zips in root)
- **Business** (3 books) — All KDP ready ✅
- **Cindy Lou Legal Capers** (3 books) — All KDP ready ✅ (created June 5)

### EPUB Status:
- All 22 KDP_PACKAGE dirs now have EPUBs in Kindle/
- Duplicate zip files exist across camelCase and kebab-case naming (cleanup needed)

---

## 3. Consulting Pipeline — STALLED

- 10 leads, 0 contacted
- Only 1 deliverable (EdTech pitch onepager)
- No email infrastructure
- consultant agent: OFFLINE (Cycle 2)
- **OPPORTUNITY**: MS Project Online retirement Sept 30, 2026 = consulting angle

---

## 4. Agent Status (June 5)

| Agent | Status | Cycle |
|-------|--------|-------|
| brand-advocate | 🔴 OFFLINE | 3+ |
| consultant | 🔴 OFFLINE | 2 |
| sales | 🔴 OFFLINE | 1 |
| engineer | 🔴 OFFLINE | 1 |
| security | 🔴 OFFLINE | 1 |
| publisher | 🔴 OFFLINE | 2 |
| researcher | 🟡 Watch | 2 pending tasks (within SLA) |
| writer | ✅ Active | — |

---

## 5. Market Intelligence (June 5)

- **MS Project Online**: Hard retirement Sept 30, 2026. Organizations MUST migrate. Major consulting opportunity.
- **KDP Quality Crackdown**: Amazon AI content detection improving. Human-authored quality premium increasing.
- **KDP A10**: Series perform better than standalone. Subcategories <5K titles offer better ranking.
- **AI PM Tools**: 78% of PM tools now have AI features. 41% of PMs say AI adoption is a challenge.

---

## 6. Critical Blockers

1. **gcloud CLI not installed** — 29 days, all SaaS deployments blocked
2. **No email infrastructure** — consulting outreach impossible
3. **Agent ghosting** — 7 of 9 agent types OFFLINE
