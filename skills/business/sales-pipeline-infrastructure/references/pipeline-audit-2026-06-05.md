# Pipeline Audit — June 5, 2026

## Scope
Reviewed all three pipelines: Virtual Consulting, SaaS, Lead Generation + supporting infrastructure.

## Consulting Pipeline

**Status:** Data layer solid. 10 leads, 9 stages. 2 leads are "Dead" (C-005 Summit Nonprofit Alliance, C-008 Golden Gate Tech Incubator) — should be marked closed_lost. Only 1 lead contacted (C-001). 4 of 10 leads have emails.

**Blockers:**
- Email sending is paused (books-welcome-emails cron disabled)
- No Stripe payment links integrated yet
- Enrichment engine bug: reads `data.get("leads")` but structure is `data["pipeline"]["leads"]`

**New web app built:** Complete self-service consulting web application at `/mnt/usb_4tb/consulting/`. See `virtual-consulting/references/web-app-architecture.md`.

## SaaS Pipeline

**Status:** 5 leads, 8 stages. All have emails. Only 1 contacted (S-001). Auto-advance rules defined in JSON but never executed by orchestrator.

**Blockers:**
- No Stripe links in nurture emails
- Products (Project Hypatia Pro, PM Accelerator, VibraEngineer) may not have working code yet
- Content generator references Ghost CMS, not WordPress

## Lead Generation Pipeline

**Status:** 9 operation pipelines. Lead registry is stale (13 IDs vs 18 actual leads). Unified pipeline is a subset (10 of 18).

**Blockers:**
- `content-generator.py` references Ghost API — won't work with WordPress
- `backlink-acquisition.py` same Ghost issue
- Outreach dashboard send button doesn't advance leads without server-side API

## Cron Jobs (19 total)
- Pipeline Orchestrator Daily (8:00 AM) — ✅ running
- Pipeline Ops Sync (8:15 AM) — ✅ running
- Dashboard Sync (8:30 AM) — ✅ running
- Promotion Generation (8:30 AM) — ✅ running
- books-welcome-emails — ❌ PAUSED (disabled at 12:15 PM on 2026-06-05)

## Critical Path
1. Get email working (WP Mail SMTP on DreamHost)
2. Install forms plugin on WordPress
3. Set up Stripe payment links
4. Clean dead leads from consulting pipeline
5. Fix content-generator for WordPress
6. Wire up send button with server-side API
