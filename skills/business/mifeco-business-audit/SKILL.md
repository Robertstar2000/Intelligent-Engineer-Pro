---
name: mifeco-business-audit
description: "Comprehensive business operations audit for MIFECO -- analyzes website, pipeline engine, cron jobs, book catalog, SaaS products, consulting, and revenue opportunities across four promotion modes: Book Promotion, SaaS Marketing, Human Consulting, Virtual Consulting. Produces a prioritized improvement proposal with implementation roadmap. Use when the user asks for business analysis, revenue optimization, growth strategy, or 'what should I do next' for MIFECO."
triggers: ["analyze mifeco", "business audit", "revenue opportunities", "growth strategy", "what should I do next", "improve mifeco", "make more money", "business operations", "promotion audit", "marketing audit"]
---

## Memory context (Hindsight)

Long-term memory context is now provided automatically by Hindsight (bank
`mifeco-default`) on every turn — the retired MemPalace manual query step no
longer applies. Do NOT attempt to import `~/.hermes/mempalace` (it was removed
2026-08-19).This retrieves previous decisions, domain-specific context, and lessons learned from the vector memory store.

# MIFECO Business Audit

## Purpose

Produce a comprehensive, actionable analysis of MIFECO's business operations across all three product lines (Books, SaaS, Consulting) with prioritized revenue improvements and an implementation roadmap.

## Audit Workflow

### Phase 1: Data Collection (parallel)

Run these checks simultaneously:

1. **Website audit** -- `web_extract` mifeco.com, check React site components, identify gaps
2. **Pipeline engine** -- read ARCHITECTURE.md, pipeline-state.json, all pipeline data files
3. **Cron jobs** -- `cronjob list`, check last_status for errors, identify failed/stale jobs
4. **Book catalog** -- scan ~/books/ directories, check EPUB/PDF/KDP package completeness
5. **Business config** -- check .env for email/Stripe/API keys (note: .env is not directly readable; check config.yaml and skill files)
6. **Skills inventory** -- `skills_list` to see what automation already exists

### Phase 2: Gap Analysis (Four Promotion Modes)

For each promotion mode, identify:

**Book Promotion (Books Pipeline):**
- Published vs unpublished count
- KDP metadata completeness (description, keywords, cover, categories)
- Marketing automation (email sequences, ads, cross-promotion)
- Series page and "Also by" links
- Genre-specific marketing (sci-fi, cozy women's fiction, business/non-fiction)

**SaaS Marketing (SaaS Pipeline):**
- Product landing page quality
- Download/waitlist counts
- Payment integration (Stripe)
- Onboarding email sequence
- Open-source vs Pro feature split
- Free tool lead magnets

**Human Consulting Marketing (Human Consulting Pipeline):**
- Intake form to pipeline connection
- Email nurture sequences
- Pricing page clarity
- Testimonials and social proof
- Re-engagement of past clients
- Tech/AI assessment lead magnets

**Virtual Consulting Marketing (Virtual Consulting Pipeline):**
- Self-service web flow
- AI-driven consulting delivery
- Pricing page clarity
- Online booking/fulfillment
- AI-driven consulting on any subject

### Phase 3: Revenue Leakage

For each gap, estimate:
- Monthly revenue impact (conservative)
- Implementation complexity (Low/Medium/High)
- Dependencies (what must happen first)

### Phase 4: Proposal Output

Produce a structured proposal with:
1. **Executive summary** -- current state, projected revenue impact
2. **Top 5 immediate actions** -- highest ROI, lowest effort
3. **Priority matrix** -- P0 (revenue now), P1 (growth engine), P2 (scale), P3 (moats)
4. **Implementation roadmap** -- week-by-week for 90 days
5. **New skills needed** -- what to build
6. **New plugins/integrations** -- what to install
7. **Projected revenue table** -- month-by-month for 12 months
8. **Key metrics to track** -- weekly dashboard items
9. **Risks & mitigations** -- what could go wrong

## Key Files to Reference

- `~/.hermes/pipeline-engine/ARCHITECTURE.md` — full pipeline design
- `~/.hermes/pipeline-engine/data/pipeline-*.json` — current pipeline state
- `~/.hermes/skills/email/dreamhost-email-pipeline/SKILL.md` — email infrastructure
- `~/mifeco_web/mifeco-website/src/components/` — website components
- `~/books/` — all book directories and metadata
- `~/.hermes/skills/publishing/` — publishing workflow skills
- `~/.hermes/skills/business/` — business automation skills

## Common Findings (MIFECO-Specific)

These are recurring issues found in MIFECO audits:

1. **Email not connected** — .env EMAIL_* commented out. #1 blocker for all email-dependent revenue.
2. **Books pipeline stalled** — manuscripts exist but not uploaded to KDP. Passive income sitting on disk.
3. **No Stripe integration** — waitlist exists but no payment conversion path.
4. **Consulting leads go nowhere** — forms exist but don't connect to pipeline or email sequences.
5. **No content marketing** — no blog, no SEO content, no organic traffic driver.
6. **AgentMail inboxes are dead** — built around agentmail.to instead of real email.
7. **No CRM** — leads-registry.json has no web UI or email sync.

## Output Format

Save the proposal to `~/mifeco_web/MIFECO_Strategic_Proposal.md` and deliver a summary to the user via Telegram with the top 5 actions and projected revenue impact.
