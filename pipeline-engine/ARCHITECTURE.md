# MIFECO Pipeline Engine — Architecture

> **Brand:** MIFECO · **Background:** `#0f172a` · **Accent:** `#00ffcc` · **Theme:** Dark

---

## 1. System Overview

The MIFECO Pipeline Engine is a unified lead-to-revenue system that processes prospects across three product lines — **SaaS**, **Consulting**, and **Books** — through a single, orchestratable funnel. It combines automated discovery, multi-source enrichment, signal-based scoring, content generation, and outreach into one cohesive engine.

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                      MIFECO UNIFIED PIPELINE ENGINE                               │
│              Lead → Enrichment → Ranking → Content → Outreach                     │
└─────────────────────────────────────────────────────────────────────────────────┘

  LEAD SOURCES
  ┌─────────────────────────────────────────────────────────────────────────────┐
  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────┐ │
  │  │ Website  │  │ LinkedIn │  │ Referrals│  │Organic   │  │ BookExpo /   │ │
  │  │ Forms    │  │ Ads      │  │          │  │Search    │  │ Events       │ │
  │  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘  └──────┬───────┘ │
  │  ┌────┴─────┐  ┌────┴─────┐  ┌────┴─────┐  ┌────┴─────┐  ┌──────┴───────┐ │
  │  │ Chat     │  │ Social   │  │AgentMail │  │ Previous │  │ Exa          │ │
  │  │ Widget   │  │ Media    │  │ Inboxes  │  │ Customers│  │ Discovery    │ │
  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘  └──────────────┘ │
  └───────────────────────────────────┬─────────────────────────────────────────┘
                                      │
                                      ▼
  ┌─────────────────────────────────────────────────────────────────────────────┐
  │                    PIPELINE ENGINE ORCHESTRATOR                              │
  │  (Daily cron @ 8AM · Backlink weekly @ Sunday 8AM)                          │
  │                                                                              │
  │  1. Ingest leads from all sources → unified-pipeline.json                    │
  │  2. Classify by product_line → route to correct pipeline                     │
  │  3. Run enrichment — web research, signal detection                         │
  │  4. Score leads — 3 dimensions (Verification, Contact, Fit)                  │
  │  5. Queue nurture emails per product sequence                                │
  │  6. Update stages, advance stale leads                                       │
  │  7. Generate content for social media posting                                │
  └───────────────────────────────────┬──────────────────────────────────────────┘
                                      │
                                      ▼
  ┌─────────────────────────────────────────────────────────────────────────────┐
  │                     ENRICHMENT ENGINE (ChromaDB-backed)                       │
  │                                                                              │
  │  ┌──────────────────────┐  ┌──────────────────────────────────────────────┐ │
  │  │ Web Research Pipeline│  │ Signal Detection                              │ │
  │  │  · Company lookup    │  │  🔴 Personnel changes → key hire / departure │ │
  │  │  · Contact discovery │  │  🟡 Cyber breaches → security incident       │ │
  │  │  · Tech stack audit  │  │  🟢 Growth/downsizing → hiring / layoff      │ │
  │  │  · Social presence   │  │  💰 Funding rounds → Series A/B/C            │ │
  │  │  · News aggregration │  │  🚀 Product launches → new release           │ │
  │  └──────────────────────┘  └──────────────────────────────────────────────┘ │
  │  Vector memory: ChromaDB stores enriched profiles for recall                │
  └───────────────────────────────────┬──────────────────────────────────────────┘
                                      │
                                      ▼
  ┌─────────────────────────────────────────────────────────────────────────────┐
  │                     SCORING & RANKING ENGINE                                  │
  │                                                                              │
  │  ┌────────────────┐  ┌────────────────────┐  ┌────────────────────────────┐ │
  │  │ Verification   │  │ Contact            │  │ Product/Consulting         │ │
  │  │ (0–10 pts)     │  │ Availability       │  │ Fit (0–10 pts)             │ │
  │  │                │  │ (0–10 pts)         │  │                            │ │
  │  │ Company exists │  │ Email validated    │  │ SaaS ICP match (0–10)      │ │
  │  │ Domain valid   │  │ Phone available    │  │ Consulting need alignment  │ │
  │  │ Active entity  │  │ LinkedIn profile   │  │ Book interest relevancy    │ │
  │  └────────────────┘  └────────────────────┘  └────────────────────────────┘ │
  │                                                                              │
  │  MAX: 30 points · Thresholds: 25+ Hot · 15–24 Warm · 5–14 Cold · 0–4 Dead │
  └───────────────────────────────────┬──────────────────────────────────────────┘
                                      │
                                      ▼
  ┌─────────────────────────────────────────────────────────────────────────────┐
  │                     CONTENT GENERATION ENGINE                                │
  │                                                                              │
  │  Per Platform · Per Product Line                                             │
  │  ┌────────────┬────────────┬──────────────┬──────────────────────────────┐  │
  │  │ LinkedIn   │ Twitter/X  │ Instagram    │ Blog / Newsletter            │  │
  │  │ · SaaS     │ · SaaS     │ · Books      │ · Consulting thought         │  │
  │  │   product  │   product  │   cover art  │   leadership pieces          │  │
  │  │   demos    │   tips     │   quotes     │ · SaaS use-case studies      │  │
  │  │ · Consult  │ · Books    │ · Consult    │ · Book excerpt series        │  │
  │  │   insights │   series   │   infographics│                             │  │
  │  │ · Books    │   teasers  │              │                              │  │
  │  │   author   │            │              │                              │  │
  │  └────────────┴────────────┴──────────────┴──────────────────────────────┘  │
  └───────────────────────────────────┬──────────────────────────────────────────┘
                                      │
                                      ▼
  ┌─────────────────────────────────────────────────────────────────────────────┐
  │                     OUTREACH & NURTURE                                       │
  │                                                                              │
  │  ┌──────────────────────┐  ┌──────────────────────┐  ┌───────────────────┐  │
  │  │ AgentMail            │  │ Email Sequences      │  │ Backlink          │  │
  │  │ · SaaS inbox         │  │ · SaaS 7-email seq   │  │ Strategy (weekly) │  │
  │  │ · Consulting inbox   │  │ · Consulting 5-email  │  │ · Guest post      │  │
  │  │ · Books inbox        │  │ · Books 4-email seq   │  │   opportunities   │  │
  │  └──────────────────────┘  └──────────────────────┘  │ · Directory        │  │
  │                                                       │   submissions     │  │
  │                                                       │ · Resource page   │  │
  │                                                       │   link building   │  │
  │                                                       └───────────────────┘  │
  └───────────────────────────────────┬──────────────────────────────────────────┘
                                      │
                                      ▼
  ┌─────────────────────────────────────────────────────────────────────────────┐
  │                     REVENUE ENGINE                                           │
  │  ┌──────────────────┐  ┌────────────────────┐  ┌────────────────────────┐  │
  │  │ Stripe (SaaS)    │  │ Invoice (Consult)  │  │ Retail (Books)        │  │
  │  │ Subscriptions    │  │ Strategy Session   │  │ KDP · Kobo · B&N      │  │
  │  │ $29–$99/mo       │  │ $199/$1,499/$3,999 │  │ $9.99–$14.99 per book │  │
  │  └──────────────────┘  └────────────────────┘  └────────────────────────┘  │
  └─────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Pipeline Architecture — Three Product Lines

Each product line has its own 8-stage pipeline that maps onto the 10-stage unified pipeline. Stages are managed through `data/unified-pipeline.json` with per-product routing via the `product_line` field.

### 2.1 Books Pipeline (8 stages)

| Stage | Name | Description | Unified Mapping |
|-------|------|-------------|-----------------|
| 1 | **Lead Inbox** | New inquiry received | Aware (1) |
| 2 | **Contacted** | Initial outreach sent | Interest (2) |
| 3 | **Discovery** | Needs assessment call | Consider (3) |
| 4 | **Quote Sent** | Bulk pricing proposal delivered | Proposal (6) |
| 5 | **Negotiation** | Terms, discount, shipping discussion | Negotiation (7) |
| 6 | **Order Placed** | Purchase order received | Closed Won (8) |
| 7 | **Fulfillment** | Printing, shipping, delivery | Onboarded (9) |
| 8 | **Follow-up** | Post-delivery check, referral ask | Advocate (10) |

**Products:** No Blue Sky series (5 vols, $9.99–$14.99), Tomorrow is Still Open ($19.99), AI That Works for Small Business ($19.99)  
**Bulk Tiers:** 5–49 (30% off), 50+ (40% off), Classroom Set 75 copies (40% off)  
**Email Inbox:** `bigtruck444@agentmail.to`  
**Nurture:** 4-email sequence over 14 days

### 2.2 SaaS Pipeline (8 stages)

| Stage | Name | Description | Unified Mapping |
|-------|------|-------------|-----------------|
| 1 | **Identified** | Lead captured from any source | Aware (1) |
| 2 | **Contacted** | Initial outreach sent | Interest (2) |
| 3 | **Qualified** | ICP validated, discovery complete | Consider (3) |
| 4 | **Demo Scheduled** | Product demo booked | Intent (4) |
| 5 | **Demo Completed** | Demo delivered, Q&A handled | Demo/Preview (5) |
| 6 | **Negotiation** | Pricing, terms, contract review | Negotiation (7) |
| 7 | **Closed Won** | Subscription activated | Closed Won (8) |
| 8 | **Closed Lost** | Deal lost or expired | — |

**Products:** Project Hypatia Pro ($99/mo), PM Accelerator ($69/mo), VibraEngineer ($29/mo)  
**Email Inbox:** `carefulvehicle192@agentmail.to`  
**Nurture:** 7-email sequence over 21 days  
**Auto-Advance:** Stage 1 → 2 after 7 days of no movement

### 2.3 Consulting Pipeline (8 stages)

| Stage | Name | Description | Unified Mapping |
|-------|------|-------------|-----------------|
| 1 | **Lead** | Lead captured via intake form | Aware (1) |
| 2 | **Contacted** | Initial outreach sent | Interest (2) |
| 3 | **Qualified** | Needs assessment complete | Consider (3) |
| 4 | **Intent** | Pricing request received | Intent (4) |
| 5 | **Strategy Session** | Session booked & completed | Demo/Preview (5) |
| 6 | **Proposal Sent** | Engagement proposal delivered | Proposal (6) |
| 7 | **Negotiation** | Terms discussion | Negotiation (7) |
| 8 | **Closed Won** | Payment received | Closed Won (8) |

**Services:** Strategy Session ($199), Deep-Dive ($1,499), Full Transformation ($3,999)  
**Email Inbox:** `crowdedbutton536@agentmail.to`  
**Nurture:** 5-email sequence over 10 days

---

## 3. Data Flow

```
DISCOVERY ──► ENRICHMENT ──► SCORING ──► NURTURE ──► CONVERSION ──► ADVOCACY
   │              │              │             │              │             │
   ▼              ▼              ▼             ▼              ▼             ▼
┌────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐
│ Exa    │  │ Web      │  │ Score    │  │ AgentMail│  │ Stripe / │  │ Referral │
│ Search │  │ Research │  │ lead     │  │ send     │  │ Invoice  │  │ ask      │
│ Forms  │  │ ChromaDB │  │ 0–30 pts │  │ Day N    │  │ / Retail │  │ Review   │
│ Refer- │  │ Signal   │  │ Classify │  │ email    │  │ payment  │  │ request  │
│ rals   │  │ Detect   │  │ Hot/Warm │  │ sequence │  │ received │  │          │
│        │  │          │  │ Cold/Dead│  │          │  │          │  │          │
└────────┘  └──────────┘  └──────────┘  └──────────┘  └──────────┘  └──────────┘
```

### 3.1 Lead Discovery

Leads enter the pipeline through multiple channels:

- **Website forms** — SaaS, Consulting, and Books intake forms post to AgentMail inboxes
- **Exa Discovery** — Automated web searches for companies matching ICP profiles
- **Referrals** — Existing customers and partners submit referral cards
- **Events** — BookExpo, conferences, speaking engagements
- **Social Media** — Organic discovery via LinkedIn, Twitter/X
- **Previous Customers** — Repeat buyers, upsell opportunities

### 3.2 Ingestion & Classification

Each lead is ingested into `data/unified-pipeline.json` with a composite ID:

```
saas-NNN      → SaaS product line
consulting-NNN → Consulting service line
books-NNN     → Books product line
```

The `product_line` field determines routing, nurture sequence, and scoring criteria.

### 3.3 Enrichment Pipeline

Leads flow from raw capture to enriched profile via:

1. **Company lookup** — Verify company exists, get HQ, industry, size
2. **Contact discovery** — Find decision-maker emails, LinkedIn profiles
3. **Signal detection** — Scrape news for relevant signals (see §4)
4. **Tech stack analysis** — Identify tools, platforms, vendors in use
5. **Vector storage** — Store enriched profile in ChromaDB for future recall

### 3.4 Scoring & Triage

After enrichment, each lead receives a composite score (see §5). Based on score:

- **25+ (Hot)** — Immediate personal outreach, priority queue
- **15–24 (Warm)** — Enter nurture sequence, monitor for engagement
- **5–14 (Cold)** — Automated drip campaign, low-touch
- **0–4 (Dead)** — Archived, removed from active pipeline

### 3.5 Nurture Sequences

Each product line has a distinct email sequence defined in `sequences/`:

| Product Line | Emails | Duration | Frequency |
|-------------|--------|----------|-----------|
| SaaS | 7 | 21 days | Days 1, 3, 5, 7, 10, 14, 21 |
| Consulting | 5 | 10 days | Days 1, 3, 5, 7, 10 |
| Books | 4 | 14 days | Days 1, 4, 7, 14 |

Sequences pause on reply and resume after 7 days of silence.

### 3.6 Stage Advancement

Leads advance through stages via:

- **Manual action** — Agent updates stage after call/email
- **Auto-advance rules** — Stale leads move after N days
- **Trigger events** — Payment received → Closed Won
- **Engagement signals** — Reply/click → advance to Interest

### 3.7 Conversion & Advocacy

At conversion (payment received), the lead moves to **Closed Won**:

- **SaaS** → Account activation, onboarding sequence
- **Consulting** → Engagement kickoff, deliverable schedule
- **Books** → Fulfillment, shipping, delivery confirmation

Post-delivery, leads enter **Advocate** stage: referral requests, review solicitation, testimonial collection → feeds back to lead sources.

---

## 4. Enrichment Engine

The enrichment engine is a **ChromaDB-backed** research pipeline that transforms raw leads into enriched, scored profiles.

### 4.1 Web Research Pipeline

```
Raw Lead
   │
   ▼
┌──────────────────────────────────────────────────────────────────────────┐
│  STEP 1: Company Verification                                            │
│  · Domain WHOIS lookup                                                   │
│  · Crunchbase / LinkedIn company page scrape                             │
│  · Business registration check (if available)                            │
│  · Output: company exists? Y/N, domain valid, HQ location, industry      │
└───────────────────────────────────┬──────────────────────────────────────┘
                                    │
                                    ▼
┌──────────────────────────────────────────────────────────────────────────┐
│  STEP 2: Contact Discovery                                              │
│  · Email pattern detection (first@company, first.last@company)           │
│  · LinkedIn profile search for decision-maker roles                      │
│  · Hunter.io / similar lookup for @company email addresses               │
│  · Output: contact_name, contact_email, LinkedIn URL, role, phone        │
└───────────────────────────────────┬──────────────────────────────────────┘
                                    │
                                    ▼
┌──────────────────────────────────────────────────────────────────────────┐
│  STEP 3: Signal Detection                                                │
│  · News aggregation (Google News, RSS, Crunchbase) for target company    │
│  · Classify signals into 5 categories (see §4.2)                         │
│  · Relevance scoring per signal type                                     │
│  · Output: signal_log[{type, date, summary, relevance_score}]            │
└───────────────────────────────────┬──────────────────────────────────────┘
                                    │
                                    ▼
┌──────────────────────────────────────────────────────────────────────────┐
│  STEP 4: Tech Stack & Social Analysis                                    │
│  · BuiltWith / Wappalyzer for tech stack fingerprinting                   │
│  · Social media presence audit (LinkedIn, Twitter, GitHub)               │
│  · Content analysis (blog quality, frequency, topics)                    │
│  · Output: tech_stack[], social_profiles{}, content_maturity_score       │
└───────────────────────────────────┬──────────────────────────────────────┘
                                    │
                                    ▼
┌──────────────────────────────────────────────────────────────────────────┐
│  STEP 5: Vector Embedding & Storage                                      │
│  · Generate embedding of entire enriched profile                         │
│  · Store in ChromaDB collection: lead_enrichments                        │
│  · Metadata: lead_id, enrichment_date, source, confidence_score          │
│  · Enables semantic search: "find companies with recent layoffs in AI"   │
└──────────────────────────────────────────────────────────────────────────┘
```

### 4.2 Signal Detection Categories

The engine monitors each target company for five signal categories:

#### 🔴 Personnel Changes (Priority: High)
- **C-suite hires/departures** — New CEO, CTO, CFO signals strategic shift
- **VP/Director movement** — Department leadership changes indicate reorganization
- **Team expansion** — Hiring spree in specific departments
- **Key departures** — Talent leaving may indicate instability or opportunity

#### 🟡 Cyber Breaches & Security (Priority: Critical)
- **Data breaches** — Recent breach = urgent need for consulting/SaaS solutions
- **Ransomware attacks** — Active incident = immediate pain point
- **Security vulnerabilities** — Publicly disclosed CVEs affecting their stack
- **Compliance failures** — GDPR/HIPAA/SOC2 violations

#### 🟢 Growth & Downsizing (Priority: High)
- **Funding rounds** — Series A/B/C/D = budget available, growth mode
- **Layoffs** — Downsizing indicates cost-cutting, potential need for efficiency tools
- **Office expansions/closures** — Physical footprint changes
- **Revenue milestones** — $1M, $10M, $100M ARR announcements

#### 💰 Funding Rounds (Priority: Medium)
- **Seed/Angel** — Early stage, building foundation
- **Series A/B** — Growth mode, budget for tools and consulting
- **Series C+** — Enterprise ready, larger deal sizes
- **Grant funding** — Nonprofit/government grants

#### 🚀 Product Launches (Priority: Medium)
- **New product releases** — Need for go-to-market strategy support
- **Feature announcements** — Indicates product maturity and innovation
- **Beta programs** — Early adopters, feedback-seeking mode
- **Partnership announcements** — Ecosystem growth

### 4.3 ChromaDB Vector Memory

ChromaDB serves as the persistent vector store for enrichment data:

- **Collection:** `lead_enrichments`
- **Embedding:** Each enriched lead profile is embedded into a 1536-dimension vector
- **Metadata:** `lead_id`, `product_line`, `enrichment_date`, `confidence`, `signal_count`
- **Query use cases:**
  - "Find companies with active CTO hires in EdTech"
  - "Show leads from companies that had a breach in the last 90 days"
  - "Match this lead's tech stack to similar scored leads"
- **Deduplication:** Before enriching, check ChromaDB for existing profile by domain

---

## 5. Scoring & Ranking Engine

Every lead is scored on **3 dimensions** — 10 points each for a **maximum of 30 points**.

### 5.1 Scoring Dimensions

#### Dimension 1: Verification (0–10 pts)

| Criteria | Points | Condition |
|----------|--------|-----------|
| Company verified | 3 | Domain resolves, business registration confirmed |
| Domain is valid | 2 | MX records, website loads, not a disposable domain |
| Company is active | 2 | Recent activity (social, news, hiring) in last 90 days |
| Industry confirmed | 2 | Industry matches form input or enrichment data |
| No fraud indicators | 1 | Not on blacklists, no bounced email patterns |

#### Dimension 2: Contact Availability (0–10 pts)

| Criteria | Points | Condition |
|----------|--------|-----------|
| Email validated | 3 | Email format valid, domain accepts mail, no hard bounce |
| Phone available | 2 | Phone number provided or discovered |
| LinkedIn profile | 2 | LinkedIn URL found, profile active |
| Decision-maker role | 2 | Title indicates purchasing authority (C-suite, VP, Director) |
| Multiple contacts | 1 | >1 contact discovered at the company |

#### Dimension 3: Product/Consulting Fit (0–10 pts)

| Criteria | Points | Condition |
|----------|--------|-----------|
| ICP match | 4 | Company size, industry, role align with ideal customer profile |
| Pain point clarity | 2 | Clear description of problem in intake or discovered via research |
| Budget indication | 2 | Budget range provided or inferred from company size/funding |
| Timeline | 1 | Decision timeline mentioned or inferred (e.g., "next quarter") |
| Engagement history | 1 | Previous interaction, downloaded resource, attended event |

### 5.2 Score Thresholds

| Score Range | Classification | Action |
|-------------|---------------|--------|
| **25–30** | 🔥 **Hot** | Immediate personal outreach within 24h. Priority queue. C-suite attention. |
| **15–24** | 🔶 **Warm** | Enter nurture sequence. Monthly check-in. Monitor for engagement signals. |
| **5–14** | 🔵 **Cold** | Automated drip campaign. Low-touch. Quarterly re-scoring. |
| **0–4** | ⚫ **Dead** | Archived. Removed from active pipeline. May re-enter if new signal detected. |

### 5.3 Scoring Flow

```
Raw Lead
   │
   ├──► Verification Score (0–10) ────────────┐
   │                                           │
   ├──► Contact Availability (0–10) ───────────┼──► TOTAL SCORE (0–30)
   │                                           │
   └──► Product/Consulting Fit (0–10) ────────┘
                    │
                    ▼
         ┌─────────────────────┐
         │  Classification     │
         │  25+  → Hot        │
         │  15–24 → Warm      │
         │  5–14 → Cold       │
         │  0–4  → Dead       │
         └─────────────────────┘
                    │
                    ▼
         Route to appropriate pipeline action
```

---

## 6. Content Generation Engine

The content engine generates platform-specific social media posts for each product line. Content is queued in structured JSON and deployed via the orchestrator.

### 6.1 Per-Platform Matrix

```
                    │  LinkedIn    │  Twitter/X   │  Instagram   │  Blog
────────────────────┼──────────────┼──────────────┼──────────────┼──────────────
📘 Books            │ Author posts │ Series       │ Cover art    │ Chapter
                    │ Reader       │ quotes       │ Author       │ excerpts
                    │ testimonials │ "Did you     │ photos       │ Writing
                    │ Bulk order   │ know" Mars  │ Infographics │ process
                    │ case studies │ facts        │              │ behind-the-
                    │              │              │              │ scenes
────────────────────┼──────────────┼──────────────┼──────────────┼──────────────
☁️ SaaS             │ Product     │ Feature      │ Product      │ Use-case
                    │ demos        │ tips         │ screenshots  │ deep dives
                    │ Case studies │ CLI tricks   │ Team photos  │ Technical
                    │ Customer     │ Threads:     │ Charts &     │ tutorials
                    │ success      │ "How we     │ dashboards   │ Comparison
                    │ stories      │ built X"    │              │ guides
────────────────────┼──────────────┼──────────────┼──────────────┼──────────────
💼 Consulting       │ Thought     │ Quick tips   │ Client       │ Methodology
                    │ leadership   │ Threads:     │ journey      │ pieces
                    │ Industry     │ "3 things   │ timelines    │ Research
                    │ analysis     │ every CEO   │ Workshop     │ reports
                    │ Methodology  │ should know │ photos       │ Whitepapers
                    │ breakdowns   │ about AI"   │              │
```

### 6.2 Content Cadence

| Platform | Frequency | Per Product | Total Posts/Month |
|----------|-----------|-------------|-------------------|
| LinkedIn | 3x/week | 1 per product line | ~36 |
| Twitter/X | Daily | Rotating across lines | ~30 |
| Instagram | 2x/week | Books focus + visuals | ~24 |
| Blog | 1x/week | Rotating by priority | ~4 |

### 6.3 Content Templates

Each post is generated from a template with product-specific variables:

```json
{
  "platform": "linkedin",
  "product_line": "SaaS",
  "template": "product_demo",
  "variables": {
    "product_name": "Project Hypatia Pro",
    "feature": "AI Risk Detection",
    "benefit": "catch schedule conflicts before they happen",
    "cta": "Book a demo at mifeco.com/demo",
    "tone": "professional, solution-oriented"
  }
}
```

---

## 7. Backlink Strategy

The backlink engine runs **weekly on Sundays** to discover and pursue link-building opportunities.

### 7.1 Weekly Discovery Process

```
Sunday 8:00 AM ─► Backlink Scan
                      │
                      ▼
┌──────────────────────────────────────────────────────────────────────────┐
│  DISCOVERY SOURCES                                                       │
│                                                                          │
│  1. "Write for us" pages in SaaS/AI/engineering niche                    │
│     · Search: "write for us" + "AI" + "project management"              │
│     · Search: "guest post" + "engineering" + "technology"               │
│                                                                          │
│  2. Broken link opportunities on relevant resource pages                 │
│     · Search: "resources" + "AI tools" + "project management"           │
│     · Check for 404s, suggest MIFECO content as replacement             │
│                                                                          │
│  3. Unlinked brand mentions                                              │
│     · Search: "MIFECO" + "AI consulting" (unlinked mentions)            │
│     · Reach out to site owner: "thanks for the mention, please link"     │
│                                                                          │
│  4. Competitor backlink gaps                                             │
│     · Analyze top 5 competitor domains                                   │
│     · Identify sites linking to them but not to MIFECO                  │
│     · Prioritize by domain authority (DA 30+)                            │
│                                                                          │
│  5. Directory & listing submissions                                      │
│     · SaaS directories (G2, Capterra, GetApp)                            │
│     · Consulting directories (Clutch, Consultancy.org)                   │
│     · Author/book directories (Goodreads, LibraryThing)                  │
└───────────────────────────────────┬──────────────────────────────────────┘
                                    │
                                    ▼
┌──────────────────────────────────────────────────────────────────────────┐
│  PRIORITY QUEUE                                                          │
│                                                                          │
│  Score each opportunity by:                                              │
│  · Domain Authority (DA)                                                │
│  · Relevance to product line                                             │
│  · Effort to acquire (low/medium/high)                                   │
│  · Likelihood of success                                                 │
│                                                                          │
│  Top 5 opportunities → outreach emails generated → queued for review    │
└──────────────────────────────────────────────────────────────────────────┘
```

### 7.2 Outreach Templates

- **Guest post pitch:** Personalized email with 3 article ideas, mentioning their audience
- **Broken link replacement:** "Found a broken link on your resources page — here's a replacement"
- **Brand mention thank you:** Polite request to add a link
- **Directory submission:** Fill in listing forms with optimized descriptions

---

## 8. File Structure Reference

```
pipeline-engine/
│
├── ARCHITECTURE.md                          ← This file
│
├── data/
│   ├── unified-pipeline.json                ← ★ PRIMARY: Single unified pipeline tracker
│   ├── pipeline-saas.json                   ← Legacy SaaS pipeline (reference)
│   ├── pipeline-consulting.json             ← Legacy Consulting pipeline (reference)
│   └── pipeline-books.json                  ← Legacy Books pipeline (reference)
│
├── sequences/
│   ├── saas-nurture.json                    ← SaaS 7-email sequence (21 days)
│   ├── consulting-nurture.json              ← Consulting 5-email sequence (10 days)
│   └── books-nurture.json                   ← Books 4-email sequence (14 days)
│
├── forms/
│   ├── saas-intake.html                     ← SaaS lead capture form (dark theme, #00ffcc)
│   ├── consulting-intake.html               ← Consulting lead capture form
│   └── books-intake.html                    ← Books inquiry form
│
├── dashboard/
│   ├── pipeline-dashboard.html              ← ★ PRIMARY: Combined pipeline dashboard
│   ├── consulting-dashboard.html            ← Consulting-specific view
│   └── index.html                           ← Command center / hub page
│
├── enrichment/                              ← Enrichment engine modules
│   ├── engine.py                            ← Orchestrator: runs full enrichment pipeline
│   ├── company_verify.py                    ← Step 1: Company verification
│   ├── contact_discovery.py                 ← Step 2: Contact discovery & validation
│   ├── signal_detector.py                   ← Step 3: Signal detection (5 categories)
│   ├── tech_stack.py                        ← Step 4: Tech stack & social analysis
│   ├── vector_store.py                      ← Step 5: ChromaDB embedding & storage
│   └── config.json                          ← API keys, endpoints, thresholds
│
├── scoring/
│   ├── scorer.py                            ← Scoring engine (3 dimensions → 30 pts)
│   ├── verification_score.py                ← Dimension 1: Verification
│   ├── contact_score.py                     ← Dimension 2: Contact availability
│   ├── fit_score.py                         ← Dimension 3: Product/Consulting fit
│   └── rules.json                           ← Scoring rules, weights, thresholds
│
├── content/
│   ├── generator.py                         ← Content generation orchestrator
│   ├── templates/
│   │   ├── linkedin.json                    ← LinkedIn post templates per product
│   │   ├── twitter.json                     ← Twitter/X post templates
│   │   ├── instagram.json                   ← Instagram post templates
│   │   └── blog.json                        ← Blog post templates
│   └── queue.json                           ← Scheduled content queue
│
├── backlinks/
│   ├── scanner.py                           ← Weekly backlink opportunity scanner
│   ├── outreach.py                          ← Outreach email generator
│   ├── priority_queue.json                  ← Scored opportunities (top 5)
│   └── history.json                         ← Past outreach tracking
│
├── outreach/
│   ├── mailer.py                            ← AgentMail integration for email sending
│   ├── sequence_manager.py                  ← Nurture sequence scheduler
│   └── reply_processor.py                   ← Inbound reply handler
│
├── orchestrator/
│   ├── daily.sh                             ← Daily 8AM orchestration script
│   ├── weekly.sh                            ← Sunday 8AM backlink script
│   └── config.sh                            ← Shared config (paths, API keys)
│
├── chromadb/
│   ├── data/                                ← ChromaDB persistent storage directory
│   └── collections.json                     ← Collection registry
│
├── logs/
│   ├── orchestrator.log                     ← Daily orchestration logs
│   ├── enrichment.log                       ← Enrichment run logs
│   ├── scoring.log                          ← Scoring engine logs
│   └── backlinks.log                        ← Weekly backlink scan logs
│
├── scripts/
│   ├── dedup-check.py                       ← Dedup tool for lead registry
│   ├── reset-stage.py                       ← Manual stage reset utility
│   └── report.py                            ← Pipeline health report generator
│
└── leads-registry.json                      ← Canonical lead registry (dedup master)
```

---

## 9. Cron Schedule

The pipeline engine is driven by two cron jobs on the orchestrator:

### 9.1 Daily Orchestrator — 8:00 AM Daily

```cron
0 8 * * * /home/bob/.hermes/.openclaw/workspace/pipeline-engine/orchestrator/daily.sh
```

**Daily workflow:**

| Time | Step | Action |
|------|------|--------|
| 08:00 | 1 | Check all 3 AgentMail inboxes for new leads |
| 08:05 | 2 | Classify new leads by `product_line` → route to unified pipeline |
| 08:10 | 3 | Run enrichment on unenriched leads (<3 days old) |
| 08:30 | 4 | Score all new and updated leads (3 dimensions) |
| 08:45 | 5 | Triage by score: route Hot leads to priority queue |
| 09:00 | 6 | Send Day-N follow-up emails per product sequence schedule |
| 09:15 | 7 | Process replies received since last run → update stages |
| 09:30 | 8 | Advance stale leads (auto-advance rules) |
| 09:45 | 9 | Update pipeline metrics in unified-pipeline.json |
| 10:00 | 10 | Generate daily report → log |

### 9.2 Weekly Backlink Scan — Sunday 8:00 AM

```cron
0 8 * * 0 /home/bob/.hermes/.openclaw/workspace/pipeline-engine/orchestrator/weekly.sh
```

**Weekly workflow:**

| Time | Step | Action |
|------|------|--------|
| 08:00 | 1 | Scan "write for us" pages in SaaS/AI/engineering niches |
| 08:15 | 2 | Identify broken link opportunities on resource pages |
| 08:30 | 3 | Find unlinked brand mentions of MIFECO |
| 08:45 | 4 | Analyze top 5 competitor backlink gaps |
| 09:00 | 5 | Score and prioritize opportunities (DA × relevance × effort) |
| 09:15 | 6 | Generate outreach emails for top 5 opportunities |
| 09:30 | 7 | Queue outreach for manual review |
| 09:45 | 8 | Submit to 3 directory listings |
| 10:00 | 9 | Log results to `logs/backlinks.log` |

### 9.3 Implementation: Crontab Entry

```bash
# MIFECO Pipeline Engine — Daily Orchestrator
0 8 * * * /home/bob/.hermes/.openclaw/workspace/pipeline-engine/orchestrator/daily.sh > /home/bob/.hermes/.openclaw/workspace/pipeline-engine/logs/orchestrator.log 2>&1

# MIFECO Pipeline Engine — Weekly Backlink Scan
0 8 * * 0 /home/bob/.hermes/.openclaw/workspace/pipeline-engine/orchestrator/weekly.sh > /home/bob/.hermes/.openclaw/workspace/pipeline-engine/logs/backlinks.log 2>&1
```

---

## 10. Technology Stack

### 10.1 Core Stack

| Component | Technology | Role |
|-----------|-----------|------|
| **Runtime** | Python 3.10+ | All engine modules, enrichment, scoring, content generation |
| **Data Storage** | JSON flat files | Pipeline state, sequences, forms, config (`data/`, `sequences/`) |
| **Vector Memory** | ChromaDB | Enrichment profiles, semantic search, lead deduplication |
| **Email** | AgentMail API | Outbound nurture sequences, inbound reply processing |
| **Orchestration** | Bash scripts + cron | Daily/weekly scheduling, log management |
| **Frontend** | Vanilla HTML/CSS/JS | Pipeline dashboard, intake forms (dark theme) |

### 10.2 Python Dependencies

```
chromadb>=0.4.0          # Vector storage for enrichment profiles
requests>=2.28.0         # HTTP client for AgentMail, web research
beautifulsoup4>=4.11.0   # HTML parsing for signal detection
lxml>=4.9.0              # XML/HTML parser
python-dotenv>=1.0.0     # Environment variable management
email-validator>=2.0.0   # Email validation for contact scoring
```

### 10.3 Infrastructure

| Aspect | Implementation |
|--------|---------------|
| **Scheduling** | Linux cron (system crontab) |
| **Logging** | Plain text log files in `logs/` |
| **Backup** | Entire `pipeline-engine/` directory snapshotted weekly |
| **Monitoring** | Dashboard serves as real-time pipeline health view |
| **Configuration** | `orchestrator/config.sh` for shared paths, API keys |

### 10.4 Design System

- **Background:** `#0f172a` (slate-900) — primary dark background
- **Card background:** `#1e293b` (slate-800) — secondary surfaces
- **Accent:** `#00ffcc` (teal) — primary interactive color, highlights, CTAs
- **Text primary:** `#e2e8f0` (slate-200) — body text
- **Text secondary:** `#94a3b8` (slate-400) — labels, metadata
- **Borders:** `#334155` (slate-700) — card and table borders
- **Success:** `#22c55e` — closed won, verified
- **Warning:** `#f59e0b` — negotiation, pending verification
- **Danger:** `#ef4444` — dead leads, flags, errors
- **Gradient accent:** `linear-gradient(135deg, #00ffcc, #667eea)` — form buttons

---

## Appendix A: Data Model — Lead Record

Every lead in the unified pipeline follows this schema:

```json
{
  "id": "saas-001 | consulting-001 | books-001",
  "source_pipeline": "SaaS | Consulting | Books",
  "product_line": "SaaS | Consulting | Books",
  "unified_stage": 1,
  "per_product_stage": 1,
  "company": "Company Name",
  "contact_name": "Contact Person",
  "contact_email": "person@company.com",
  "icp_score": 0,
  "value_estimate": 0.00,
  "source": "form | referral | exa_discovery | event",
  "last_action": "Description of most recent activity",
  "next_action": "Description of next step to take",
  "last_action_date": "ISO-8601",
  "next_action_date": "ISO-8601",
  "product_interest": "Product or service name",
  "industry": "Industry classification",
  "created_date": "ISO-8601",
  "notes": "Free-text notes from enrichment and interactions"
}
```

## Appendix B: Pipeline Metrics Model

```json
{
  "total_leads": 0,
  "active_leads": 0,
  "leads_by_pipeline": {
    "SaaS": 0,
    "Consulting": 0,
    "Books": 0
  },
  "leads_by_unified_stage": {
    "1_Aware": 0,
    "2_Interest": 0,
    "3_Consider": 0,
    "4_Intent": 0,
    "5_Demo/Preview": 0,
    "6_Proposal": 0,
    "7_Negotiation": 0,
    "8_Closed_Won": 0,
    "9_Onboarded": 0,
    "10_Advocate": 0
  },
  "total_pipeline_value": 0.00,
  "last_updated": "ISO-8601"
}
```

## Appendix C: Enrichment Signal Record

```json
{
  "lead_id": "saas-001",
  "enrichment_date": "ISO-8601",
  "signals": [
    {
      "type": "personnel_change | cyber_breach | growth_downsizing | funding_round | product_launch",
      "priority": "critical | high | medium | low",
      "date": "ISO-8601",
      "source": "news_url or source name",
      "summary": "Brief description of signal",
      "relevance_score": 0.0
    }
  ],
  "company_profile": {
    "domain": "company.com",
    "industry": "Industry",
    "size": "1-10 | 11-50 | 51-200 | 201-1000 | 1001+",
    "headquarters": "City, State",
    "founded": "YYYY",
    "tech_stack": ["technology1", "technology2"],
    "social_links": {
      "linkedin": "url",
      "twitter": "url",
      "github": "url"
    }
  },
  "contact_profile": {
    "emails": ["email1", "email2"],
    "phones": ["phone1"],
    "linkedin_url": "url",
    "role": "Job Title",
    "seniority": "c-suite | vp | director | manager | ic"
  },
  "vector_id": "chromadb_document_id",
  "confidence": 0.0
}
```

---

> **MIFECO Pipeline Engine v2.0** · One Pipeline · Three Product Lines · Full Funnel from Aware → Advocate
>
> Dark theme · `#00ffcc` accent · Built for scale
