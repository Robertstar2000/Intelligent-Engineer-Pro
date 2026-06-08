# MIFECO Product Line Inventory — May 25, 2026

> Snapshot of all MIFECO product lines, their current state, known issues, and blockers.
> Last updated: 2026-05-26 (CEO Agent daily orchestrator — Tuesday Books & Content Marketing)

---

## 1. SaaS — Cloud Run Apps

### Project Hypatia Pro
- **URL:** `https://project-hypatia-pro-1064319572465.us-west1.run.app`
- **HTTP Status:** 200 ✅
- **Operational Status:** ⚠️ **DEGRADED** — CDN resource failures
- **Version:** V3.01
- **Features:** Landing page with 5 modules (Literature Synthesis, Hypothesis Simulation, Analytical Workspace, Peer-Review Protocol, Manuscript Architect), sign in/up, waitlist CTA
- **Root cause of degradation:** Uses esm.sh import maps for React/dependencies at runtime. CDN resources (esm.sh, cdn.jsdelivr.net) fail to load from Cloud Run us-west1. No dist/ directory found — build artifacts missing.
- **Source:** `/home/bob/saas/Project_Hypatia_Pro/` (Vite/React/TypeScript, Express/SQLite backend)
- **Known issues:** Missing all 6 security headers (helmet.js fix added May 7, never deployed), CDN runtime loading failures
- **Fix status:** Source code has helmet.js. CDN fix needs bundling or alternative CDN. Deployment requires gcloud (not available). Task ceo-engineer-20260525-001 assigned.

### PM Accelerator (HMAP Accelerator)
- **URL:** `https://project-management-accelerator-845075991286.us-west1.run.app`
- **HTTP Status:** 200 ✅
- **Operational Status:** ✅ **OPERATIONAL** — only minor Google Fonts failures
- **Version:** V2.5.0 (codebase updated with UX improvements May 11, not yet deployed)
- **Features:** Dashboard ("Welcome, A. User"), active projects, create new project, help drawer
- **Source:** `/home/bob/saas/Project_Management_Accelerator/` (React/TypeScript, Express/SQLite backend, Firestore sync, Google Gemini AI, 52 discipline templates)
- **UX improvements (coded, not deployed):** 3-step wizard, Cmd+K command palette, AI smart defaults, helpme.md fix
- **Architecture designed (not implemented):** HMAP Agent with 3 sub-agents (Task Triage, Sprint Risk Predictor, Assignment Optimizer)
- **Marketing opportunity:** MS Project Online retirement Sept 30, 2026 — massive migration wave. Planner lacks PMO features. PM Accelerator positioned to capture mid-market.
- **Known issues:** Missing security headers, Express x-powered-by leak

### VibraEngineer
- **URL:** `https://vibraengineer-845075991286.us-west1.run.app`
- **HTTP Status:** 200 ✅
- **Operational Status:** ⚠️ **DEGRADED** — CDN resource failures
- **Version:** V4.03
- **Features:** Landing page with 5 modules (HMAP Lifecycle, AI Generation, Risk Analysis, Team Sync, Insight Engine), sign in/up, waitlist CTA
- **Root cause of degradation:** Uses esm.sh import maps + Tailwind CSS classes without stylesheet. No dist/ directory. JSZip, Prism from cdnjs.cloudflare.com also fail.
- **Source:** `/home/bob/saas/VibraEngineer/` (Vite/React/TypeScript, Express/SQLite backend)
- **Known issues:** Missing security headers, CORS wildcard (access-control-allow-origin: *), CDN runtime loading failures, Tailwind classes without stylesheet
- **Fix status:** Source code has helmet.js. CDN fix needs Tailwind build + esm.sh replacement. Deployment requires gcloud. Task ceo-engineer-20260525-001 assigned.

### MIFECO.com
- **URL:** `https://mifeco.com`
- **Status:** ✅ Operational — full marketing site
- **Hosting:** DreamHost (WordPress)
- **Security headers:** ✅ All 6 headers present (only app properly configured)
- **Content:** Hero with CTA buttons, stats, storefront, client logos, awards, industry expertise, services, contact form

---

## 2. Books Pipeline

### Status: ✅ FULLY COMPLETE — All 13 books have published output

| # | Title | Series | KDP Package | Location |
|---|-------|--------|-------------|----------|
| 1 | Built from Dust | No Blue Sky | ✅ CEO-created May 12 | `~/books/No_Blue_Sky_Series/Book_I_Built_from_Dust/` |
| 2 | The Oxygen Gamble | No Blue Sky | ✅ | `~/books/No_Blue_Sky_Series/` |
| 3 | Rivers Under Mars | No Blue Sky | ✅ | `~/books/No_Blue_Sky_Series/` |
| 4 | The Red Charter | No Blue Sky | ✅ | `~/books/No_Blue_Sky_Series/` |
| 5 | The First Martian Nation | No Blue Sky | ✅ | `~/books/No_Blue_Sky_Series/` |
| 6-9 | Moon Rock through Waters Horizon | Lunar Foundation (4 books) | ✅ Book 4 has KDP ZIP; Books 1-3 have EPUBs | `~/books/Lunar_Foundation_Series/` |
| 10 | Tomorrow Remembered | Tomorrow Remembered | ✅ Rebuilt May 24 | `~/books/Tomorrow_Remembered/` |
| 11 | Tomorrow is Still Open | Tomorrow Remembered | ✅ | `~/books/Tomorrow_Remembered/` |
| 12 | AI That Works (AI Playbook) | Business | ✅ | `~/books/Business_Series/` |
| 13 | Owner's Manual AI Agents | Business | ✅ | `~/books/Business_Series/` |

**Recent activity:** Tomorrow Remembered had a major rebuild on May 24 (rebuild scripts, enhanced EPUB/PDF/DOCX output). All KDP packages now complete.

### Remaining Items
- No new writing tasks needed
- Lunar Foundation Books 1-3 could use KDP ZIP packages (currently only EPUBs)
- AI disclosure compliance verified for all books

---

## 3. Consulting Pipeline

### Status: 🟡 STALLED — Infrastructure built, zero outreach

**Pipeline location:** `~/book-business/consulting/` (NOT `~/consulting-pipeline/`)

### Lead Status
| # | Company | Vertical | Stage | Outreach |
|---|---------|----------|-------|----------|
| 1 | Outschool | EdTech | Identified | ❌ Not sent |
| 2 | Newsela | EdTech | Identified | ❌ Not sent |
| 3 | Edmentum | EdTech | Identified | ❌ Not sent |
| 4 | Redox | Healthcare IT | Identified | ❌ Not sent |
| 5 | Collective Health | Healthcare IT | Identified | ❌ Not sent |
| 6 | HealthSherpa | Healthcare IT | Identified | ❌ Not sent |
| 7 | Firefly Aerospace | Aerospace | Identified | ❌ Not sent |
| 8 | BlackSky | Aerospace | Identified | ❌ Not sent |
| 9 | Fictiv | Manufacturing | Identified | ❌ Not sent |
| 10 | Plethora | Manufacturing | Identified | ❌ Not sent |

### Key Files
- Pipeline tracker: `consulting-pipeline/DATA/conversions/pipeline-tracker-2026-05.json`
- Lead profiles: `~/book-business/consulting/DATA/leads/` (10 files, created May 15)
- Outreach drafts: `~/book-business/consulting/DATA/followups/` (all marked DO NOT SEND)
- Consulting DATA infrastructure: 22 files, created by CEO May 15

### #1 Blocker: Email Infrastructure
No email sending service configured (SendGrid, Postmark, Amazon SES, etc.). All outreach drafts must be DO NOT SEND. Bob must either:
1. Configure an email service, OR
2. Send outreach manually using the prepared drafts

### Market Context (May 2026)
- AI consulting market: $14.1B in 2026, growing 26.5% CAGR
- 73% of SMBs cite integration barriers as primary obstacle
- 78% of mid-market companies adopted AI (up from 55% in 2024)
- Project-based pricing: $2,000-$15,000 most common for SMBs
- ROI expectation: 30-90 days

---

## 4. Known Infrastructure Issues

### Security (CRITICAL)
1. **Cloud Run apps missing all 6 security headers** — helmet.js fix added May 7 but never deployed (18+ days overdue)
2. **Hardcoded credentials in 5 files:**
   - `~/.hermes/scripts/exa_search.sh` — Exa API key (world-readable, 755)
   - `~/.hermes/scripts/dashboard-sync.sh` — DreamHost SSH password (plaintext)
   - `~/.hermes/.openclaw/workspace/pipeline-engine/mifeco-dreamhost.env` — SMTP password (644)
   - PHP files (webhook secret, admin password, reused across 4+ services)
3. **Secrets directory permissions:** `~/.hermes/secrets/` is 755 (should be 700)
4. **VibraEngineer:** CORS wildcard (`access-control-allow-origin: *`)
5. **All 3 Cloud Run apps:** Express `x-powered-by` header leaks framework version

### CDN Issues (NEW May 25)
- **Project Hypatia Pro:** esm.sh + cdn.jsdelivr.net resources fail → app unstyled
- **VibraEngineer:** esm.sh + cdnjs.cloudflare.com + tailwindcss.com resources fail → app unstyled
- **PM Accelerator:** Uses bundled assets → no CDN issues
- **Root cause:** Apps use esm.sh import maps in production mode instead of bundling

### Deployment Blockers
- **gcloud CLI not installed** on the cron/deployment machine
- `gcloud auth list` returns empty
- All deployment tasks blocked — Bob must run manually

---

## 5. Agent Status

| Agent | Status | Since | Notes |
|-------|--------|-------|-------|
| `brand-advocate` | 🔴 OFFLINE | Apr 30 | Multiple consolidations. No further assignments. |
| `consultant` | 🔴 OFFLINE | May 14 | Cycle 2 escalation. CEO executes directly. |
| `sales` | 🔴 OFFLINE | May 15 | Cycle 1 consolidation. No further assignments. |
| `engineer` | ⚠️ Weak ghosting | May 1 | Tasks executed by CEO via delegate_task |
| `security` | ⚠️ Weak ghosting | May 4 | Tasks executed by CEO via delegate_task |
| `researcher` | 🟡 Watch | May 25 | 2 stale tasks cleared (Cycle 1). New task assigned. |
| `publisher` | 🟡 Watch | May 14 | Cycle 1 consolidation. Books pipeline complete. |
| `writer` | ✅ N/A | — | Books pipeline fully complete |
| `researcher` | ✅ Active | — | Previously active, now under watch |

---

## 6. Market Intelligence (May 25, 2026)

### AI PM Market
- **$4.1B** in 2026 (15.7% CAGR toward $13.29B by 2034)
- 70% of project professionals say their organization uses AI
- **MS Project Online retires Sept 30, 2026** — hard shutdown, no read-only extension
- **ClickUp Brain²** launched May 2026: agentic AI, auto-routes tasks across LLMs, MCP support, $300M+ ARR
- **Linear Agent** public beta March 2026, Code Intelligence May 2026: "Issue tracking is dead"
- **Key feature gaps (none filled):** Autonomous schedule rescheduling, stakeholder-intelligent communication, cross-portfolio resource optimization

### Book Publishing
- **AI disclosure mandatory** on KDP — compliance verified for MIFECO books
- **GEO (Generative Engine Optimization)** emerging as successor to SEO
- **AI audiobooks** going mainstream in 2026
- **"AI slop"** creating trust premium for human-authored books
- **Direct-to-reader** growing (Shopify, Kickstarter)

### Consulting
- **$14.1B** AI consulting market in 2026
- **73% integration failure rate** = MIFECO's sweet spot
- **Anthropic Claude for Small Business** launched May 13, 2026
- SMB pricing: $2,000-$15,000 project-based most common
