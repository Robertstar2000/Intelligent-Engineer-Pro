# MIFECO Product Line Inventory — June 1, 2026

> Snapshot of all MIFECO product lines. Last updated: 2026-06-01.
> **Always run a fresh `ls ~/books/` scan** — this file can be stale.

---

## 1. SaaS — Cloud Run Apps (ALL OPERATIONAL as of June 1)

| App | URL | Status | Key Issues |
|-----|-----|--------|------------|
| Project Hypatia Pro | project-hypatia-pro-1064319572465.us-west1.run.app | ✅ Operational | No security headers deployed (gcloud blocker); no onboarding flow; waitlist has no conversion flow |
| PM Accelerator | project-management-accelerator-845075991286.us-west1.run.app | ✅ Operational | No security headers; SQLite crash risk (writes to ./db instead of /tmp) |
| VibraEngineer | vibraengineer-845075991286.us-west1.run.app | ✅ Operational | No security headers; CORS wildcard; SQLite crash risk; Tailwind CDN warning |
| mifeco.com | mifeco.com | ✅ Operational | All 6 security headers present |

**Known:** gcloud CLI NOT installed — all deployments blocked. Security headers fix coded May 7, never deployed (25 days overdue as of June 1).

**Header verification (June 1):**
- All 3 apps return `server: Google Frontend`, `x-powered-by: Express`
- Missing: X-Frame-Options, Content-Security-Policy, Strict-Transport-Security, X-Content-Type-Options, X-XSS-Protection, Referrer-Policy
- VibraEngineer still has `access-control-allow-origin: *` (CORS wildcard)

---

## 2. Books Pipeline — 16 of 19 books have KDP_PACKAGE + zip

**Total: 19 books** across 5 series.

| Status | Count | Books |
|--------|-------|-------|
| ✅ KDP_PACKAGE + zip | 16 | All LF (4), All NBS (5), All AL (4), Both Tomorrow (2), AI That Works |
| 📦 Need KDP standardization | 3 | Owners_Manual_AI_Agents, The_Crisis_Ready_Company (have zips but may need EPUB copy) |

### Series:
- **No Blue Sky** (5 books) — ALL have KDP dir + zip ✅
- **Lunar Foundation** (4 books) — ALL have KDP dir + zip ✅
- **Age of Lightships** (4 books) — ALL 4 have KDP dir + zip ✅. B2-4 confirmed to have FULL manuscripts (40 chapters each, 18-21MB EPUBs)
- **Tomorrow** (2 books) — Both have KDP zips ✅
- **Business Series** (3 books) — ALL 3 have KDP dir + zip ✅

### Key Finding (June 1):
AL B2-4 (Mercury Accord, Ghosts Beyond Neptune, Last Photon Fleet) were previously misidentified as "empty shells." They have complete 40-chapter manuscripts and full EPUBs. The books pipeline is **16/19 complete** with KDP packages.

---

## 3. Consulting Pipeline — STALLED

- 10 leads, 0 contacted (stuck at "identified" for 17+ days)
- Outreach packet ready at `~/book-business/consulting/DATA/OUTREACH/ready-to-send-may2026.md`
- 10 follow-up files exist but none sent (all marked DO NOT SEND)
- 1 of 4 vertical one-pagers created (EdTech)
- consultant agent: OFFLINE (Cycle 2)
- **Blocker**: No email sending service configured

---

## 4. Agent Status (June 1)

| Agent | Status | Cycle | Notes |
|-------|--------|-------|-------|
| brand-advocate | 🔴 OFFLINE | 3+ | Not sending new tasks |
| consultant | 🔴 OFFLINE | 2 | CEO executes consulting tasks |
| sales | 🔴 OFFLINE | 1 | Not consolidated yet |
| engineer | 🔴 OFFLINE | 1 | CEO documents deploy steps instead |
| security | 🔴 OFFLINE | 1 | CEO assesses SaaS health inline |
| researcher | 🟡 Watch | 2 | Fresh task assigned (MS Project campaign) |
| publisher | ✅ CEO-executed | — | All KDP packaging done inline by CEO |
| writer | ✅ Active | — | AL B2-4 fully written, no action needed |
| saas-ops | 🟡 New task | — | Critical task assigned (deploy documentation) |

---

## 5. System Health

| Component | Status |
|-----------|--------|
| agent-communications.jsonl | ✅ 56 entries, 0 invalid JSON |
| All improvement scripts | ✅ 9/9 executable (from May 31 check) |
| SOUL.md tracking | ✅ 1 section (no duplicates) |
| gcloud CLI | ❌ Not installed (blocks all deployments) |
| Email infra | ❌ Not configured (blocks all outreach) |
| JSONL cleanup | ✅ 2 superseded tasks failed June 1 |

---

## 6. Deployment Runbook

📄 **Created May 30**: `/home/bob/.hermes/.openclaw/workspace/references/deployment-runbook-may2026.md`
- Complete gcloud setup instructions
- Per-app deploy commands + verification
- SQLite `/tmp` fix documented
- Rollback procedures included
- For Bob to execute manually

---

## 7. Market Intelligence (June 1 Update)

- **MS Project Online**: Hard retirement Sept 30, 2026 (121 days). No read-only extension. Microsoft's successor (Planner Premium) is a downscope.
- **AI PM Competitors**: ClickUp Brain² leads on agentic features. Monday.com has meeting AI. Asana has AI Teammates. All shipping fast.
- **KDP/Amazon**: AI disclosure mandatory (3 dropdown menus: text, images, translations). No public-facing AI badge yet. Authors Guild offers voluntary "Human Author" certification. Silent shadow-banning of AI content is real.
- **MIFECO web presence**: mifeco.com is a minimal landing page. No product pages, no pricing, no signup flow. Not a visible SaaS competitor yet.
