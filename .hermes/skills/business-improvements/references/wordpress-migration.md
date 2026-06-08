# WordPress Migration Plan — mifeco.com

Source: /home/bob/.hermes/pipeline-engine/wordpress-integration-plan.md (May 5, 2026)

## Current State
- Static React site (Cloud Run) -> Target: WordPress on DreamHost
- Email: AgentMail (disposable) -> Target: DreamHost SMTP (hermes@mifeco.com)
- Lead forms: Static HTML -> Target: WordPress forms + webhook -> pipeline-engine

## Phase 1 — DreamHost WordPress Foundation

### Provision
- Point mifeco.com nameservers to DreamHost
- Enable WordPress via DreamHost One-Click Install
- Set up SSL (DreamHost provides free Let's Encrypt via AutoSSL)

### Essential Configuration
- Theme: GeneratePress or Astra (lightweight, fast, developer-friendly)
- PHP Version: 8.2+
- Permalinks: /%postname%/

### Must-Have Plugins
- ACF Pro: Custom fields for product pages, intake forms
- WP Mail SMTP: Route WordPress emails through DreamHost SMTP
- Fluent Forms Pro: Lead capture forms with webhook support
- Rank Math SEO: SEO metadata, sitemaps, schema
- UpdraftPlus: Automated backups
- Stripe Payments: SaaS subscription checkout
- LearnDash: Companion courses

## Phase 2 — Email Service Setup

### Email Accounts
- hermes@mifeco.com — Primary pipeline automation
- books@mifeco.com — Book inquiries
- saas@mifeco.com — SaaS inquiries
- consulting@mifeco.com — Consulting sessions
- bob@mifeco.com — Personal inbox

### DreamHost SMTP
- Host: smtp.dreamhost.com
- Port: 587 (STARTTLS)
- IMAP: imap.dreamhost.com:993

## Phase 3 — Lead Capture to Pipeline
- Consulting intake form -> leads-registry.json
- SaaS demo request -> pipeline-engine
- Book bulk order inquiry -> pipeline-engine
- Waitlist signup -> pipeline-saas.json
- Newsletter signup -> email sequence

## Phase 4 — Email Nurture Sequences
- SaaS Onboarding: 7 emails (free download trigger)
- Consulting Discovery: 5 emails (form submit trigger)
- Book Reader Nurture: 4 emails (purchase/email capture)
- Consulting Re-engagement: 3 emails (30 days inactive)

## Execution Order
1. Install WordPress on DreamHost
2. Install + configure plugins
3. Create email accounts in DreamHost panel
4. Configure EMAIL_* in .env with DreamHost SMTP
5. Migrate content from React site
6. Build lead capture forms
7. Set up webhook endpoint
8. Write email nurture sequences
9. Test: form -> pipeline -> email
10. Switch DNS from Cloud Run to DreamHost
11. Verify SSL + email deliverability
