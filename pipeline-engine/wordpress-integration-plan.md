# MIFECO.com WordPress Integration Plan

**Date:** May 5, 2026
**Target:** MIFECO.com → WordPress (.php) on DreamHost
**Goal:** Unified website + email + pipeline infrastructure for Hermes Agent

---

## Current State

| Component | Current | Target |
|-----------|---------|--------|
| Website | Static / Cloud Run apps | WordPress on DreamHost |
| Email Sending | AgentMail (bigtruck444@agentmail.to) | DreamHost SMTP (hermes@mifeco.com) |
| Lead Forms | Static HTML → AgentMail API | WordPress forms + webhook |
| Product Pages | Separate Cloud Run URLs | WordPress subpages |
| Pipeline Automation | JSON-based, drafts only | Full send via SMTP |

---

## Phase 1 — DreamHost WordPress Foundation

### 1.1 Provision & Domain
- [ ] Point mifeco.com nameservers to DreamHost (or configure DNS)
- [ ] Enable WordPress via DreamHost's One-Click Install
- [ ] Set up SSL (DreamHost provides free Let's Encrypt via AutoSSL)
- [ ] Verify domain resolves correctly

### 1.2 Essential WordPress Configuration
- **Theme:** GeneratePress or Astra (lightweight, fast, developer-friendly)
- **PHP Version:** DreamHost supports 8.x — use 8.2+ for modern plugin compatibility
- **Permalinks:** `/`Post name`/` structure (`/%postname%/`)
- **Users:** Create admin account + separate editor account for content updates

### 1.3 Must-Have Plugins

| Plugin | Purpose | 
|--------|---------|
| **Advanced Custom Fields (ACF) Pro** | Custom fields for product pages, intake forms |
| **WP Mail SMTP** | Route WordPress emails through DreamHost SMTP |
| **Fluent Forms** or **WPForms** | Lead capture forms with webhook support |
| **Webhook URL Forwarder** or **Zapier** | Send form submissions to pipeline-engine |
| **Rank Math SEO** | SEO metadata, sitemaps, schema |
| **UpdraftPlus** | Automated backups to DreamHost storage |
| **WP Rocket** or **LiteSpeed Cache** | Caching/performance |

---

## Phase 2 — Email Service Setup

### 2.1 DreamHost Email Accounts
Create these email accounts in DreamHost's webmail panel:

| Email Address | Purpose | Forwarding |
|---------------|---------|------------|
| `hermes@mifeco.com` | **Primary — all pipeline automation** | SMTP config for Hermes |
| `books@mifeco.com` | Book inquiries & nurture sequences | → hermes@mifeco.com |
| `saas@mifeco.com` | SaaS inquiries & demo requests | → hermes@mifeco.com |
| `consulting@mifeco.com` | Consulting strategy sessions | → hermes@mifeco.com |
| `bob@mifeco.com` | Personal inbox (human reads) | → bob's personal email |

### 2.2 DreamHost SMTP Configuration
DreamHost SMTP credentials (to configure in Hermes):

```
SMTP Host: smtp.dreamhost.com (or sub5.dreamhost.com)
SMTP Port: 587 (STARTTLS) or 465 (SSL/TLS)
SMTP Auth: Full email address + password
IMAP Host: imap.dreamhost.com
IMAP Port: 993 (SSL)
```

### 2.3 Hermes Email Configuration
Update `~/.hermes/.env` with DreamHost SMTP:

```
EMAIL_ADDRESS=hermes@mifeco.com
EMAIL_PASSWORD=[generated password from DreamHost]
EMAIL_IMAP_HOST=imap.dreamhost.com
EMAIL_IMAP_PORT=993
EMAIL_SMTP_HOST=smtp.dreamhost.com
EMAIL_SMTP_PORT=587
EMAIL_POLL_INTERVAL=15
EMAIL_ALLOWED_USERS=bob@mifeco.com
EMAIL_HOME_ADDRESS=bob@mifeco.com
```

### 2.4 WP Mail SMTP Plugin
Configure the WP Mail SMTP plugin to use DreamHost SMTP — ensures all WordPress system emails (form notifications, password resets, etc.) use the same authenticated channel.

---

## Phase 3 — Website Content Pages

### 3.1 Product Pages

Each SaaS product gets a dedicated WordPress page:

| Page | URL | Content |
|------|-----|---------|
| Home | `/` | Hero, product overview, CTA |
| Project Hypatia Pro | `/hypatia` | Features, pricing, demo link, intake form |
| PM Accelerator | `/accelerator` | Features, pricing, get started form |
| VibraEngineer | `/vibraengineer` | Features, pricing, demo request |
| Consulting | `/consulting` | $199 Strategy Session, case studies |
| Books | `/books` | No Blue Sky series, standalone titles |
| AI That Works | `/ai-that-works` | Book info, bulk orders |
| Contact | `/contact` | General inquiry form |

Current Cloud Run URLs should redirect to WordPress pages:
- `hypatia.mifeco.com` → `/hypatia`
- `accelerator.mifeco.com` → `/accelerator`  
- `vibraengineer.mifeco.com` → `/vibraengineer`

### 3.2 Lead Intake Forms (Replace Static HTML)

Replace the current static HTML forms at `pipeline-engine/forms/` with WordPress forms that POST to a webhook endpoint (Phase 4):

| Pipeline | Form Location | Webhook Target |
|----------|---------------|----------------|
| SaaS | `/saas-demo` → Fluent Form | Hermes webhook → pipeline-saas.json |
| Consulting | `/consulting` → Fluent Form | Hermes webhook → pipeline-consulting.json |
| Books | `/books/order` → Fluent Form | Hermes webhook → pipeline-books.json |

Fluent Form fields map 1:1 to the current HTML forms (company, name, email, interest, pain points, etc.)

---

## Phase 4 — Pipeline Integration

### 4.1 Architecture

```
                      ┌─────────────────────────────┐
                      │   WordPress (mifeco.com)     │
                      │  ┌───────────────────────┐   │
                      │  │  Lead Intake Forms     │   │
                      │  │  Product Pages         │   │
                      │  │  Book Catalog          │   │
                      │  │  Blog / Content        │   │
                      │  └─────────┬─────────────┘   │
                      │            │ POST webhook    │
                      │            ▼                 │
                      │  ┌───────────────────────┐   │
                      │  │  WP Mail SMTP         │   │
                      │  │  (smtp.dreamhost.com) │   │
                      │  └───────────────────────┘   │
                      └─────────────────────────────┘
                               │                  ▲
                    Webhook POST                  │ SMTP
                               ▼                  │
┌────────────────────────────────────────────────────────────────┐
│                    Hermes Agent                              │
│  ┌────────────────────────────────────────────────────────┐   │
│  │  pipeline-engine/                                      │   │
│  │  ├─ webhook-server/ ← receives POST from WordPress    │   │
│  │  │   ├─ saas-intake.py     (appends to pipeline-saas) │   │
│  │  │   ├─ consulting-intake.py                           │   │
│  │  │   └─ books-intake.py                                │   │
│  │  ├─ data/pipeline-*.json   ← updated by webhooks      │   │
│  │  ├─ sequences/*-nurture.json  ← templates             │   │
│  │  └─ send-engine/           ← sends via SMTP           │   │
│  │      └─ daily-sender.py    ← cron: reads queue, sends │   │
│  └────────────────────────────────────────────────────────┘   │
│                                                              │
│  SMTP Config: smtp.dreamhost.com:587 → hermes@mifeco.com     │
│  IMAP Config: imap.dreamhost.com:993 → hermes@mifeco.com     │
└──────────────────────────────────────────────────────────────┘
```

### 4.2 Webhook Server

Create a lightweight Python webhook server at `pipeline-engine/webhook-server/`:

```
pipeline-engine/webhook-server/
├── server.py           ← Main HTTP server (Flask or FastAPI)
├── handlers/
│   ├── saas.py         ← Validate & append to pipeline-saas.json
│   ├── consulting.py   ← Validate & append to pipeline-consulting.json
│   └── books.py        ← Validate & append to pipeline-books.json
├── auth.py             ← Shared secret verification
└── requirements.txt
```

**Endpoints:**

| Endpoint | Method | Pipeline | Auth |
|----------|--------|----------|------|
| `/webhook/saas` | POST | JSON → pipeline-saas.json | Bearer token |
| `/webhook/consulting` | POST | JSON → pipeline-consulting.json | Bearer token |
| `/webhook/books` | POST | JSON → pipeline-books.json | Bearer token |
| `/webhook/health` | GET | Health check | None |

**Each webhook handler should:**
1. Verify shared secret (configured in WordPress + Hermes)
2. Validate JSON payload matches expected schema
3. Create lead ID, timestamp, initial stage
4. Run `dedup-check.py` against registry
5. Append to pipeline JSON + update registry
6. Return 201 + lead ID

**Deployment options:**
- Run as a background process on the Hermes machine
- Or deploy as a small Flask/FastAPI app to a lightweight service
- Or use DreamHost's own CGI/PHP endpoint to write to a shared file

### 4.3 Email Send Engine

Create a Python send engine that replaces the current AgentMail-only pipeline:

```
pipeline-engine/send-engine/
├── send.py             ← Core sender (SMTP via smtplib)
├── queue.py            ← Reads pipeline data, determines what to send
├── render.py           ← Renders templates with lead data
├── track.py            ← Simple open tracking (1x1 pixel)
└── cron-send.sh        ← Called by cron job
```

**Send flow:**
```
1. Cron triggers send-engine/cron-send.sh (daily at 09:00 UTC)
2. queue.py reads each pipeline JSON
3. For each lead in correct stage:
   a. Check email_sequence_day (0 = not sent anything yet)
   b. Load nurture JSON matching that day
   c. render.py: replace {{name}}, {{company}}, {{product}}, etc.
   d. send.py: deliver via smtplib→smtp.dreamhost.com:587
   e. Return-Path: hermes@mifeco.com
   f. Update lead: email_sequence_day++, last_contacted=now
4. Log all sends to send-engine/send-log.csv
5. Pipeline orchestrator report includes send results
```

### 4.4 Pipeline Cron Job Update

Update the daily pipeline orchestrator cron job to:

1. **Check email IMAP inbox** (`hermes@mifeco.com`) for replies — `pause_on_reply` logic
2. **Send nurture emails** via SMTP instead of just reporting what to send
3. **Process bounce notifications** — mark bounced emails as `status: bounced`

New cron schedule command concept:
```bash
cronjob action=create \
  schedule="0 9 * * *" \
  name="Pipeline — Daily Send + Report" \
  prompt="Run pipeline send-engine, then generate daily report" \
  workdir="/home/bob/.hermes/.openclaw/workspace/pipeline-engine"
```

---

## Phase 5 — WordPress Content Migration

### 5.1 From Cloud Run to WordPress

The current Cloud Run apps (React/Vite/Express) should remain live for their core functionality, but **marketing pages** move to WordPress:

| App | Core Function Stays | Marketing Moves to WP |
|-----|--------------------|---------------------|
| Project Hypatia Pro | Application UI | Landing page, features, pricing |
| PM Accelerator | Application UI | Landing page, features, pricing |
| VibraEngineer | Application UI | Landing page, features, pricing |

**Migration approach:**
1. Build WordPress landing pages first
2. Update Cloud Run apps to link to `/hypatia`, `/accelerator`, `/vibraengineer` instead of `*.run.app`
3. Decommission Cloud Run marketing pages once WordPress is live

### 5.2 Book Catalog

The `pipeline-engine/data/pipeline-books.json` `books_available` block should match what's on the WordPress book page. Keep them in sync — or better, have the pipeline READ from WordPress via API.

---

## Phase 6 — Security & Monitoring

### 6.1 Security
- **Webhook secret:** Shared HMAC key between WordPress and Hermes webhook
- **HTTPS only:** DreamHost auto-SSL covers all subdomains
- **Rate limiting:** DreamHost has default limits on SMTP (500/hour send)
- **SPF/DKIM/DMARC:** Configure DNS records for mifeco.com to ensure email deliverability:
  ```
  SPF: "v=spf1 mx include:dreamhost.com ~all"
  DKIM: Enable in DreamHost email panel
  DMARC: "v=DMARC1; p=none; rua=mailto:dmarc@mifeco.com"
  ```

### 6.2 Monitoring
- **Email delivery:** Cron job checks IMAP for bounce messages
- **Webhook uptime:** `/webhook/health` endpoint monitored
- **Pipeline report:** Daily orchestrator includes SMTP send status

---

## Implementation Order

| Phase | Tasks | Est. Time | Depends On |
|-------|-------|-----------|------------|
| **1** | WordPress + DreamHost provisioning | 1-2 hours | DreamHost account |
| **2** | Email accounts + SMTP config | 30 min | Phase 1 |
| **3.1-3.2** | Product pages + intake forms | 3-4 hours | Phase 1 |
| **4.1-4.3** | Webhook server + send engine | 2-3 hours | Phase 2 |
| **4.4** | Cron job update + pipeline rewrite | 1 hour | Phase 4.1-4.3 |
| **5** | Content migration (Cloud Run → WP) | 2-3 hours | Phase 3 |
| **6** | SPF/DKIM/DMARC + monitoring | 30 min | Phase 2 |

**Total estimated time:** ~10-14 hours

---

## Rollout Strategy

**Progressive cutover — no big-bang deployment:**

| Step | What Changes | Risk |
|------|-------------|------|
| 1 | WordPress goes live with home page only | None |
| 2 | DreamHost email accounts created, Hermes configured | None (AgentMail still active) |
| 3 | Test: send 1 nurture email via SMTP, verify delivery | Low |
| 4 | Product pages added to WordPress | Low |
| 5 | Intake forms published, webhook tested | Low (parallel to existing forms) |
| 6 | Send engine activated — 1 pipeline at a time (Books first) | Medium |
| 7 | AgentMail replaced entirely | Low (tested in step 6) |
| 8 | Cloud Run marketing redirects → WordPress | Low |

Ready to start whenever you provide the DreamHost credentials.
