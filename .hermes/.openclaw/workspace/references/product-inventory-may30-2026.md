# MIFECO Product Line Inventory — May 30, 2026

> Snapshot of all MIFECO product lines. Last updated: 2026-05-30.
> **Always run a fresh `ls ~/books/` scan** — this file can be stale.

---

## 1. SaaS — Cloud Run Apps (ALL OPERATIONAL as of May 30)

| App | URL | Status | Key Issues |
|-----|-----|--------|------------|
| Project Hypatia Pro | project-hypatia-pro-1064319572465.us-west1.run.app | ✅ Operational | No security headers deployed (gcloud blocker), no onboarding flow |
| PM Accelerator | project-management-accelerator-845075991286.us-west1.run.app | ✅ Operational | No security headers; SQLite may crash (writes to ./db instead of /tmp) |
| VibraEngineer | vibraengineer-845075991286.us-west1.run.app | ✅ Operational | No security headers; CORS wildcard; SQLite crash risk; Tailwind CDN warning |

**Known:** gcloud CLI NOT installed — all deployments blocked. Security headers fix coded May 7, never deployed.
**Critical finding (May 30):** VibraEngineer + PM Accelerator write SQLite to `./database.sqlite` — Cloud Run FS is read-only except `/tmp`. Must change to `/tmp/database.sqlite` before deploying. Deployment runbook created at `references/deployment-runbook-may2026.md`.

---

## 2. Books Pipeline — 11 of 19 books have KDP_PACKAGE + zip

**Total: 19 books** across 5 series + 1 standalone.

| Status | Count | Books |
|--------|-------|-------|
| ✅ KDP_PACKAGE + zip | 11 | Moon_Rock, Mooncoming, Waters_End, Waters_Horizon, Red_Charter, First_Martian_Nation, Crisis_Ready_Company, Sunward_Exodus, AI_That_Works, Owners_Manual, Tomorrow_Remembered |
| 📁 Publishing_Package.zip only | 4 | NBS I Built_from_Dust, NBS II Oxygen_Gamble, NBS III Rivers_Under_Mars, Owners_Manual_AI_Agents |
| 📦 Empty KDP dir (no content) | 3 | AL B2 Mercury_Accord, AL B3 Ghosts_Beyond_Neptune, AL B4 Last_Photon_Fleet |
| ❌ No package at all | 1 | Tomorrow (book_source subdir) |

### Series:
- **No Blue Sky** (5 books) — B1-3 have old Pub zips; B4-5 have KDP+zip ✅; all 5 have complete manuscripts
- **Lunar Foundation** (4 books) — ALL 4 have KDP+zip ✅
- **Age of Lightships** (4 books) — B1 has KDP+zip ✅; B2-4 are EMPTY shells needing chapters
- **Tomorrow** (standalone) — ✅ published
- **Business Series** (3 books) — AI_That_Works ✅; Crisis_Ready_Company ✅; Owners_Manual has old Pub zip

---

## 3. Consulting Pipeline — STALLED

- 10 leads, 0 contacted (stuck at "identified" for 15+ days)
- Outreach packet ready (380 lines, all DO NOT SEND)
- LinkedIn templates have grammar bugs
- No contact details in lead profiles (only titles)
- Only 1 of 4 vertical one-pagers created (EdTech)
- No email infrastructure — all outreach manual

---

## 4. Agent Status (May 30)

| Agent | Status | Cycle | Notes |
|-------|--------|-------|-------|
| brand-advocate | 🔴 OFFLINE | 3+ | Not sending new tasks |
| consultant | 🔴 OFFLINE | 2 | CEO executes consulting tasks |
| sales | 🔴 OFFLINE | 1 | Not consolidated yet |
| engineer | ⚠️ Weak ghosting | 1 | CEO executes via delegate_task |
| security | ⚠️ Weak ghosting | 1 | CEO executes via delegate_task |
| researcher | 🟢 Watch | 1 | 2 pending tasks, within SLA |
| publisher | 🔴 OFFLINE | 2 | CEO executes KDP tasks |
| writer | 🟢 Active | — | No ghosting |

---

## 5. System Health

| Component | Status |
|-----------|--------|
| agent-communications.jsonl | ✅ 48 entries, 0 invalid JSON |
| All improvement scripts | ✅ 9/9 executable |
| SOUL.md tracking | ✅ 1 section (no duplicates) |
| Cron jobs | ✅ 2 active (mempalace-daily, daily-briefing) |
| gcloud CLI | ❌ Not installed (blocks all deployments) |
| Email infra | ❌ Not configured (blocks all outreach) |

## 6. Deployment Runbook

📄 **Created May 30**: `/home/bob/.hermes/.openclaw/workspace/references/deployment-runbook-may2026.md`
- Complete gcloud setup instructions
- Per-app deploy commands + verification
- SQLite `/tmp` fix documented
- Rollback procedures included
- For Bob to execute manually
