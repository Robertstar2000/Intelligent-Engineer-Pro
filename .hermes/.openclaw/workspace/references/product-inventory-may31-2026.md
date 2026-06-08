# MIFECO Product Line Inventory — May 31, 2026

> Snapshot of all MIFECO product lines. Last updated: 2026-05-31.
> **Always run a fresh `ls ~/books/` scan** — this file can be stale.

---

## 1. SaaS — Cloud Run Apps (ALL OPERATIONAL as of May 31)

| App | URL | Status | Key Issues |
|-----|-----|--------|------------|
| Project Hypatia Pro | project-hypatia-pro-1064319572465.us-west1.run.app | ✅ Operational | No security headers deployed (gcloud blocker), no onboarding flow |
| PM Accelerator | project-management-accelerator-845075991286.us-west1.run.app | ✅ Operational | No security headers; SQLite may crash (writes to ./db instead of /tmp) |
| VibraEngineer | vibraengineer-845075991286.us-west1.run.app | ✅ Operational | No security headers; CORS wildcard; SQLite crash risk; Tailwind CDN warning |
| mifeco.com | mifeco.com | ✅ Operational (HTTP 200) | All 6 security headers present |

**Known:** gcloud CLI NOT installed — all deployments blocked. Security headers fix coded May 7, never deployed (24 days).

---

## 2. Books Pipeline — 16 of 19 books have KDP packages

**Total: 19 books** across 5 series.

| Status | Count | Books |
|--------|-------|-------|
| ✅ KDP_PACKAGE + zip | 16 | All LF (4), All NBS (5), AL B1+ B4 + TR (2), AI That Works, Crisis Ready Co, Owners_Manual |
| 📦 Empty KDP dir (no EPUB inside) | 0 | None (all fixed May 31) |
| ❌ No KDP at all | 0 | None |

### Series:
- **No Blue Sky** (5 books) — ALL have KDP dir + zip ✅
- **Lunar Foundation** (4 books) — ALL have KDP dir + zip ✅
- **Age of Lightships** (4 books) — ALL 4 have KDP dir + zip ✅ (FIXED May 31)
- **Tomorrow** (incl. Tomorrow_Remembered + Still_Open) — Both have KDP zips ✅
- **Business Series** (3 books) — ALL 3 have KDP dir + zip ✅ (Owners_Manual fixed May 31)

### KDP May 31 Changes:
- AL B2 Mercury_Accord, B3 Ghosts_Beyond_Neptune, B4 Last_Photon_Fleet: Had full EPUBs (18-21MB) in output/ but EPUBs were NOT in KDP_PACKAGE dirs. Fixed by copying EPUBs in and creating ZIPs.
- Owners_Manual_AI_Agents: Same issue. Fixed.

---

## 3. Consulting Pipeline — STALLED

- 10 leads, 0 contacted (stuck at "identified" for 16+ days)
- Outreach packet ready (all DO NOT SEND — no email infra)
- 10 follow-up files exist but none sent
- 1 of 4 vertical one-pagers created (EdTech)
- consultant agent: OFFLINE (Cycle 2)

---

## 4. Agent Status (May 31)

| Agent | Status | Cycle | Notes |
|-------|--------|-------|-------|
| brand-advocate | 🔴 OFFLINE | 3+ | Not sending new tasks |
| consultant | 🔴 OFFLINE | 2 | CEO executes consulting tasks |
| sales | 🔴 OFFLINE | 1 | Not consolidated yet |
| engineer | 🔴 OFFLINE | 1 | Deadline-expired task cleaned up |
| security | 🔴 OFFLINE | 1 | Deadline-expired task cleaned up |
| researcher | 🟡 Watch | 2 | Deadline-expired task cleaned up; 1 newer task pending |
| publisher | ✅ CEO-executed | — | KDP packaging done inline by CEO |
| writer | 🟢 Active | — | No ghosting |

---

## 5. System Health

| Component | Status |
|-----------|--------|
| agent-communications.jsonl | ✅ 50 entries, 0 invalid JSON |
| All improvement scripts | ✅ 9/9 executable |
| SOUL.md tracking | ✅ 1 section (no duplicates) |
| gcloud CLI | ❌ Not installed (blocks all deployments) |
| Email infra | ❌ Not configured (blocks all outreach) |
| JSONL cleanup | ✅ 3 expired tasks failed on May 31 |

## 6. Deployment Runbook

📄 **Created May 30**: `/home/bob/.hermes/.openclaw/workspace/references/deployment-runbook-may2026.md`
- Complete gcloud setup instructions
- Per-app deploy commands + verification
- SQLite `/tmp` fix documented
- Rollback procedures included
- For Bob to execute manually
