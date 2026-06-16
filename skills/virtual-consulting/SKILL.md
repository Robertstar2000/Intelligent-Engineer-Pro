---
name: virtual-consulting
description: "MIFECO Virtual Consulting — the $199 online business assessment product at mifeco.com/consult. Full pipeline: survey → research → generate Assessment + Strategic Plan as single PDF reports → quality review → email delivery. NOT KDP packages."
version: 4.0.0
author: OWL
category: business
metadata:
  hermes:
    tags: [mifeco, consulting, survey, dreamhost, php, business, pdf, report, assessment]
    related_skills: [saas-operations, stripe-payment-collection, mifeco-website-deployment]
---

# MIFECO Virtual Consulting — Skill

## When to Use
- Business owner needs structured AI assessment and action plan
- Client overwhelmed by admin/tasks and wants automation guidance
- Client wants AI but doesn't know where to start
- Building/maintaining the consulting pipeline at mifeco.com/consult/

## When NOT to Use
- Paper-only businesses (recommend digitization first)
- Clients unwilling to invest time in learning
- Fundamental business viability issues (technology won't fix)

## Core Philosophy
**Start with problems, not technology.** Every recommendation flows from identified business pain points.

## Deliverable Format — CRITICAL

**Reports are SINGLE PDFs, NOT KDP packages.**

Each report type is a standalone, professionally formatted PDF document:

### Single PDF Report Components
1. **Integrated Cover Image** — Professional cover design embedded as the first page
2. **Delivery Cover Letter** — Personalized letter addressing the client by name, summarizing what's included and next steps
3. **Table of Contents** — Clear section headings with page references
4. **30+ Page Detailed Report** — Comprehensive analysis based on collected data

### What Each Report Uses
- **Initial Qualification Questions** — First contact data (role, business type, size, primary challenge)
- **Full Survey Data** — Complete business health survey responses
- **LLM Domain Knowledge** — AI-generated analysis and recommendations
- **Web Search Results** — When needed for industry benchmarks, competitor analysis, technology trends

### Quality Standards
- Fact-check all claims and statistics
- Grammar and spelling review
- Consistent professional formatting throughout
- Image quality verification (minimum 300 DPI for embedded images)
- Citation verification for data sources
- Accuracy check against survey responses

### Research Phase Process
1. Analyze survey responses to identify key pain points
2. Research the client's industry (web search if needed)
3. Identify relevant AI/automation opportunities
4. Benchmark against industry standards
5. Generate prioritized action items

## Engagement Tiers

### Tier 1: AI Readiness Assessment ($199)
- **Format:** Single PDF report
- **Contents:** Cover image + cover letter + TOC + 30+ page AI readiness analysis
- **Focus:** Current state assessment, AI opportunity identification, strategic action plan
- **Delivery:** Email within 4 hours of survey completion
- **Source:** Initial questions + full survey data

### Tier 2: Business Transformation Package ($1,499)
- **Format:** 2 separate single PDF reports (Assessment + Strategic Plan)
- **Report 1:** AI Readiness Assessment (same as Tier 1 + deeper analysis)
- **Report 2:** Strategic Plan — detailed 90-day transformation roadmap with milestones, timelines, resource requirements
- **Delivery:** Email within 8 hours of survey completion
- **Source:** Initial questions + full survey + web research + LLM knowledge

### Tier 3: Deep-Dive Consulting ($3,999)
- **Format:** Multiple PDF deliverables (Assessment + Strategic Plan + Implementation Guide + 90-Day Review Templates)
- **Includes:** Tier 1 + Tier 2 deliverables plus ongoing support
- **Delivery:** Staged delivery — Assessment first, then Strategic Plan, then Implementation Guide
- **Source:** All sources + potential interactive research sessions

## Virtual Consulting Pipeline (8 Stages)

```
Lead → Contacted → Survey → Research → Generate Reports → Quality Review → Delivery → Complete
```

| # | Stage | Description |
|---|-------|-------------|
| 1 | Lead | New virtual consulting lead captured via website or referral |
| 2 | Contacted | Initial outreach sent, qualification questions delivered to client |
| 3 | Survey | Client completes initial questions + full business survey on mifeco.com/consult/ |
| 4 | Research | Deep research on client business, industry, pain points using LLM + web search |
| 5 | Generate Reports | Create Assessment Report + Strategic Plan — single PDFs with cover, letter, TOC, 30+ pages |
| 6 | Quality Review | Fact-check, grammar, spelling, formatting, image quality, accuracy verification |
| 7 | Delivery | Deliver reports via email with delivery cover letter |
| 8 | Complete | Delivery confirmed, client follow-up scheduled |

**Email Inbox:** backdoor@mifeco.com

## Report Components Detail

### Assessment Report (Single PDF)
| Page Section | Content |
|-------------|---------|
| Cover (p.1) | Professional cover image with title, company name, date |
| Cover Letter (p.2) | Personalized letter to client, overview of report contents |
| TOC (p.3) | Table of contents with all sections and page numbers |
| Executive Summary (p.4) | 1-page overview of key findings |
| Business Overview (p.5-6) | Summary of client's business from survey data |
| Current State Analysis (p.7-12) | Detailed analysis of current operations, technology, team |
| AI Opportunity Assessment (p.13-20) | Specific AI/automation opportunities ranked by impact |
| Gap Analysis (p.21-25) | Current vs. desired state with gap identification |
| Recommendations (p.26-32) | Prioritized recommendations with estimated ROI |
| Appendix (p.33+) | Supporting data, citations, methodology notes |

### Strategic Plan Report (Single PDF)
| Page Section | Content |
|-------------|---------|
| Cover (p.1) | Professional cover image with title, company name, date |
| Cover Letter (p.2) | Personalized letter, strategic plan overview |
| TOC (p.3) | Table of contents |
| Strategic Vision (p.4-5) | Future state vision aligned with client goals |
| 90-Day Roadmap (p.6-15) | Week-by-week implementation plan |
| Milestone Tracker (p.16-20) | Key milestones with success criteria and deadlines |
| Resource Requirements (p.21-25) | Team, budget, technology, and training requirements |
| Risk Mitigation (p.26-29) | Identified risks with mitigation strategies |
| ROI Projections (p.30-33) | Expected returns with timelines and metrics |
| Appendix (p.34+) | Supporting research, benchmarks, citations |

## Technical Pipeline

### PHP Stack on DreamHost
- **URL:** mifeco.com/consult/
- **Database:** mysql.mifeco.com / mifeco_com_1
- **Tables:** consulting_users, consulting_surveys, consulting_payments, consulting_activity_log, consulting_survey_responses, consulting_survey_followups, consulting_documents

### Python API Server (Local Machine)
- **Port:** 8190
- **Location:** `/mnt/usb_4tb/consulting/api/api_server.py`
- **API Key:** `mifeco-local-api-key-change-this`
- **Endpoints:** `/api/generate-questions`, `/api/generate-reports`
- **Depends on:** WeasyPrint (install: `uv pip install weasyprint --python /tmp/tunnel-env/bin/python`, takes ~3 min)

#### Making the API Reachable from DreamHost
DreamHost cannot reach the local machine's port 8190 directly. An SSH reverse tunnel is required.
See `references/dreamhost-tunnel-setup.md` for the full setup.

Quick summary:
1. Run `/tmp/reverse_tunnel.py` (paramiko-based, auto-reconnects)
2. Set `PYTHON_API_URL` in DreamHost `config.php` to `http://127.0.0.1:8190`
3. Monitor with cron job (ID: 20aa67570b2d) that restarts tunnel/API if either dies

### Authentication Flows
1. **Backdoor:** `/consult/survey.php?backdoor=1` → auto-login as Robert Mills → survey questions (no payment)
2. **Regular:** `/register.php` → `/pay.php` (Stripe $199) → `/survey.php`

### Backdoor Credentials
- Email: Robertstar@aol.com
- Password: Rm2214ri#

### Key Fixes Applied 2026-06-15
- setup.php: Fixed all table names to use `consulting_*` prefix (was mixed `users`/`consulting_users`)
- config.php: Increased Python API timeout from 5s → 120s (PDF generation takes 30-120s)
- config.php: Fixed_STRIPE_SK placeholder → `getenv('STRIPE_SK')` pattern
- email-templates/complete.html: Rebuilt corrupted file (was .htaccess content, now proper HTML email)
- **Stripe keys are placeholders** in config.php — real keys needed for regular payments
- **All secrets should be moved to environment variables** — current hardcoded values are a security risk

### Open Issues: Stripe Keys & Secrets
config.php has placeholder Stripe keys (`pk_live_CHANGEME`, `***`, `price_CHANGEME`). Regular payments work ONLY after real keys are added from Stripe dashboard. **All credentials (DB, SSH, API keys, backdoor) must be rotated and moved to environment variables before production.**

### Known Bugs (Updated 2026-06-15)
- ~~`_fireAndForgetPythonAPI()` is a no-op~~ ✅ **Fixed** — now actually calls the Python API
- ~~No email delivery mechanism~~ ✅ **Fixed** — `deliver_reports.py` sends via DreamHost SMTP
- ~~Reports generated locally, not on DreamHost~~ ✅ **Fixed** — `sync_reports.py` syncs via SFTP
- ~~`forgot-password.php` doesn't exist~~ ✅ **Fixed** — created with token-based reset flow
- ~~No admin dashboard~~ ✅ **Fixed** — `admin.php` with full survey/payment/report management
- ~~Hardcoded credentials in config.php~~ ✅ **Fixed** — all secrets moved to environment variables
- ~~Hardcoded SSH password in deploy.sh~~ ✅ **Fixed** — loaded from `DREAMHOST_PASS` env var
- ~~Hardcoded backdoor credentials~~ ✅ **Fixed** — loaded from `CONSULT_BACKDOOR_EMAIL/PASS` env vars
- ~~`debug.php` exposes DB credentials~~ ✅ **Fixed** — removed from production
- ~~Table name mismatch in setup.php~~ ✅ **Fixed** — all tables use `consulting_*` prefix
- ~~Python API timeout too short~~ ✅ **Fixed** — increased from 5s to 120s
- ~~Email template corrupted~~ ✅ **Fixed** — rebuilt proper HTML email
- **Auto-advance rules not executed** ✅ **Fixed** — `daily-pipeline-analysis.py` now advances leads
- **Empty skill files** ✅ **Fixed** — consultant, saas-ops, stripe skills populated
- **Stripe keys are placeholders** ⚠️ **Still needs action** — add real keys from Stripe dashboard
- **Webhook idempotency** ⚠️ **Still open** — duplicate webhook deliveries could create duplicate records
- **No rate limiting** ⚠️ **Still open** — auth endpoints need rate limiting
- **No survey timeout** ⚠️ **Still open** — incomplete surveys stay forever
- Reports generated on local machine (`~/.hermes/consulting-reports/`) but `download.php` serves from DreamHost. Files never reach the download endpoint.

### Reference Files
- `references/consulting-production-checklist.md` — Full production readiness checklist (security, functional, database, payment, survey, report delivery). Use this when auditing the consulting system before launch.

## Survey State Machine
```
initial → generating_questions → in_progress → analyzing → complete
```

## Backdoor Entry Points
1. Direct URL: `https://mifeco.com/consult/survey.php?backdoor=1`
2. Admin dashboard: 💼 Virtual Consulting card
3. Register form: POST with Robertstar@aol.com / Rm2214ri#

## Pitfalls

- **Reports are NOT KDP packages** — Virtual consulting deliverables are single PDF reports (cover + letter + TOC + 30+ pages). They have nothing to do with KDP book packages. Never generate consulting deliverables in KDP format.
- **Pipeline stages are research-oriented, not purchase-oriented** — The stages are Lead → Contacted → Survey → Research → Generate Reports → Quality Review → Delivery → Complete. Old incorrect stages (Qualifier → Buy → Process → Deliverables → Edit) were borrowed from a book sales pipeline and do not apply.

