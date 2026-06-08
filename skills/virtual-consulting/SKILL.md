---
name: virtual-consulting
description: "MIFECO Virtual Consulting — the $199 online business assessment product at mifeco.com/consult. Covers the full technical pipeline: PHP frontend on DreamHost, Python API for question generation and PDF reports, Stripe payment, interactive survey with IDK branching, and deployment. Also covers the consulting methodology (pre-research, assessment, deployment planning). NOT for human/expert consulting on the main mifeco.com site."
version: 2.0.0
author: OWL (ZOO)
license: MIT
metadata:
  hermes:
    tags: [mifeco, consulting, stripe, survey, pdf, dreamhost, php, python, business]
    related_skills: [saas-operations, stripe-payment-collection, mifeco-website-deployment]
---

## 🔍 MemPalace Query (MANDATORY FIRST STEP)
Before proceeding, query MemPalace for existing context:
```python
import sys, os; sys.path.insert(0, os.path.expanduser('~/.hermes/mempalace'))
import embed; embed.init_embedding(os.path.expanduser('~/.hermes/mempalace'))
results = embed.search_embeddings("virtual consulting MIFECO business assessment survey", k=5)
```
This retrieves previous decisions, domain-specific context, and lessons learned from the vector memory store.

## Skill Update Protocol

When updating skills after a session:
1. **Scope**: Only update MIFECO-relevant skills (business, consulting, SaaS, books, publishing, writing). Do not update unrelated skills.
2. **Method**: Use `skill_manage(action='patch')` first. If the tool can't resolve the skill path, fall back to direct file I/O:
   ```python
   import os, re
   path = '/home/bob/.hermes/skills/reference/openclaw-consultant/SKILL.md'
   with open(path) as f: content = f.read()
   # ... patch content ...
   with open(path, 'w') as f: f.write(content)
   ```
3. **Cache invalidation**: After updating files on DreamHost, force cache refresh:
   ```python
   sftp.utime("/path/to/file", None)  # Updates timestamp to now
   ```

## 1. OVERVIEW

### When to Use This Skill

Use this skill when a business owner or leader needs structured guidance to identify, evaluate, and implement AI solutions that solve real operational problems. This skill is appropriate when:

- A client reports being overwhelmed by administrative/repetitive tasks
- A client wants to "do AI" but doesn't know where to start
- A client has a specific pain point (customer service volume, lead management, data entry) and wants to explore automation
- A client has tried AI tools but abandoned them due to poor fit or lack of strategy
- A client is growing and needs to scale operations without proportional headcount increases
- A client needs an objective third-party assessment of their AI readiness and opportunities

### When NOT to Use This Skill

- The client has no digitized data at all (paper-only business) — recommend digitization first
- The client is not willing to invest time in learning or change management
- The client expects AI to replace human judgment entirely (unrealistic expectations)
- The client's business model has fundamental viability issues that technology cannot address

### Core Philosophy

The MIFECO framework is built on a single principle: **start with problems, not technology.** Every recommendation flows from identified business pain points, not from what's trendy or impressive. AI is a tool for solving business problems, not an end in itself.

---

## 2. THE MIFECO CONSULTING METHODOLOGY

The methodology follows a six-phase structure derived from the book's Assess → Choose → Implement → Optimize framework, enhanced with automated pre-engagement research and post-delivery sales enablement:

```
┌─────────────────────────────────────────────────────────┐
│              PHASE 0: PRE-ENGAGEMENT RESEARCH           │
│  ┌───────────┐ ┌────────────┐ ┌─────────────┐          │
│  │ Automated  │ │ Technology │ │ Pre-Fill    │          │
│  │ Web Search │ │ Footprint  │ │ Intake Temp │          │
│  └───────────┘ └────────────┘ └─────────────┘          │
│  ┌───────────┐ ┌────────────┐ ┌─────────────┐          │
│  │ Competitor│ │ Pain Point │ │ Client      │          │
│  │ Analysis  │ │ Signals    │ │ Dossier     │          │
│  └───────────┘ └────────────┘ └─────────────┘          │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│              PHASE 1: CONFIRMATION INTAKE                │
│  ┌─────────────┐ ┌──────────────┐ ┌──────────────────┐  │
│  │ Present      │ │ Pre-Filled   │ │ Client Confirms  │  │
│  │ Dossier     │ │ Sections     │ │ & Corrects       │  │
│  └─────────────┘ └──────────────┘ └──────────────────┘  │
│  ┌─────────────┐ ┌──────────────┐ ┌──────────────────┐  │
│  │ Dynamic     │ │ Gap Fill     │ │ Stakeholder      │  │
│  │ Follow-ups  │ │ Questions    │ │ Mapping          │  │
│  └─────────────┘ └──────────────┘ └──────────────────┘  │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│              PHASE 2: KNOWLEDGE ACQUISITION              │
│  ┌─────────────────────────────────────────────────┐   │
│  │ Industry Research → Tech Landscape → Stakeholder│   │
│  │ Interviews → Web Enrichment → Financial Analysis│   │
│  └─────────────────────────────────────────────────┘   │
│  ⚠ Assumptions made are tracked in Assumptions Log    │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│              PHASE 3: QUALITY ASSESSMENT                 │
│  ┌──────────┐ ┌────────────┐ ┌───────────┐ ┌────────┐  │
│  │ Readiness │ │ Pain Point │ │Opportunity│ │ Risk   │  │
│  │ Score     │ │ Prioritiz. │ │Assessment │ │Assess. │  │
│  └──────────┘ └────────────┘ └───────────┘ └────────┘  │
│  ┌────────────┐ ┌────────────────────────────────────┐  │
│  │Recommendat.│ │ Assumptions Log + Data Confidence  │  │
│  └────────────┘ └────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│              PHASE 4: DEPLOYMENT PLAN                    │
│  ┌──────────┐ ┌────────────┐ ┌───────────┐ ┌────────┐  │
│  │Phased    │ │ Tool       │ │ Change    │ │ Training│  │
│  │Timeline  │ │ Selection  │ │Management │ │ Plan   │  │
│  └──────────┘ └────────────┘ └───────────┘ └────────┘  │
│  ┌──────────┐ ┌────────────────────┐ ┌────────────────┐ │
│  │Success   │ │ Risk Mitigation    │ │ Assumptions    │ │
│  │Metrics   │ │ Plan               │ │ Log Updated    │ │
│  └──────────┘ └────────────────────┘ └────────────────┘ │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│              PHASE 5: SALES ENABLEMENT                   │
│    ┌──────────────┐ ┌──────────────┐ ┌───────────────┐  │
│    │ Enriched     │ │ Campaign     │ │ Vertical      │  │
│    │ Upgrade Email│ │ Dashboard    │ │ Social Posts  │  │
│    └──────────────┘ └──────────────┘ └───────────────┘  │
│    ┌──────────────┐ ┌────────────────────────────┐      │
│    │ Custom       │ │ Ready for Human Approval   │      │
│    │ Infographics │ │ (Email/Posts queued)       │      │
│    └──────────────┘ └────────────────────────────┘      │
└─────────────────────────────────────────────────────────┘
```

---

## 3. PHASE 0: PRE-ENGAGEMENT RESEARCH

### Purpose

Before any direct client interaction, conduct automated research to extract everything publicly available about the client's business. This transforms the intake from a blank-slate interview into a confirmation session, saving the client's time and demonstrating professionalism.

### 3.1 Automated Web Research

Upon receiving a client's basic signup information (business name, website, industry, contact name), immediately execute the following research:

**Research Pipeline:**

| Step | Target | What to Extract | Tool |
|------|--------|-----------------|------|
| 1 | Client website | Business description, products/services, team size, pricing, location | Browser navigation |
| 2 | LinkedIn company page | Employee count, recent hires, growth signals, tech stack | Web search |
| 3 | Google/Bing search | Recent news, press releases, reviews, community presence | Web search |
| 4 | Crunchbase/industry DBs | Funding, founding date, competitors, category | Web search |
| 5 | Review sites (Yelp, G2, etc.) | Customer sentiment, pain points mentioned in reviews | Web search |
| 6 | Job postings | Tech stack signals, growth areas, staffing challenges | Web search |
| 7 | Competitor identification | 3-5 direct competitors, their AI adoption level | Web search |
| 8 | Industry benchmarks | Average metrics for their sector (response times, CSAT, etc.) | Web search |
| 9 | Technology footprint | What tools they likely use (CMS, CRM, e-commerce platform) | BuiltWith/Wappalyzer or heuristic |
| 10 | Regulatory context | Industry-specific regulations, compliance requirements | Web search |

**Research Execution Rules:**

1. **Start with the website** — it's the richest public data source. Navigate to every page: About, Products/Services, Team, Careers, Blog, Pricing.
2. **Run searches in parallel** — use `delegate_task` with independent search goals to gather data faster.
3. **Extract structured data** — don't just collect URLs. Extract specific facts: employee count range, revenue indicators, technology keywords, customer complaints, competitor names.
4. **Look for pain point signals** — job postings for customer service roles (CS bottleneck), "we're growing" language (scaling pain), outdated technology mentions (tech debt).
5. **Document all sources** — for every pre-filled answer, note where the data came from so the client can verify.

### 3.2 Pre-Filling the Intake Template

Map every piece of researched data to the intake template sections:

| Template Section | Researchable Data | Pre-Fill Source |
|-----------------|-------------------|-----------------|
| Business Profile | Name, industry, location, website, employee count, founding year, product/service description | Website, LinkedIn, Crunchbase |
| Pain Points & Time Audit | Customer service channels, product/service complexity (proxy for support volume), team structure | Website, job postings, review sites |
| Data Readiness | Tech footprint (CMS, CRM, e-commerce), digital presence indicators | Website tech analysis, job postings for data roles |
| Goals & Constraints | Business model, growth signals, recent funding/expansion | Press releases, news, LinkedIn |
| Risk Awareness | Industry regulations (healthcare, finance, legal), data handling signals | Industry research, website privacy policy |
| Stakeholders | Leadership team names and roles, org structure | LinkedIn, website Team page |

**Pre-Fill Format:**

For each question in the intake template, fill in the answer as:

```
[Pre-filled] Answer based on [source URL/description]
[Confidence: High/Medium/Low — based on data reliability]
```

**Pre-Fill Confidence Levels:**
- **High**: Directly stated on the client's website or verified across 2+ sources
- **Medium**: Inferred from available data (e.g., employee count from LinkedIn range)
- **Low**: Estimated based on industry averages or weak signals

### 3.3 Client Profile Dossier

Compile all researched data into a structured dossier that becomes the starting point for Phase 1:

```markdown
## Pre-Engagement Dossier

### Business Identity
- Name: [Researched]
- Website: [Researched]
- Industry: [Researched]
- Founded: [Researched or estimated]
- Employee Count: [Researched range]
- Location: [Researched]
- Revenue Range: [Estimated from industry + employee count]

### Digital Presence
- Website Platform: [Researched]
- Social Media: [List of platforms with follower counts]
- E-commerce: [Yes/No + platform if detectable]
- Review Profile: [Summary of review sentiment]

### Technology Footprint
- Known Tools: [List with confidence level]
- Likely Gaps: [Areas where no tools are evident]

### Competitive Context
- Direct Competitors: [3-5 names]
- Competitor AI Adoption: [Notes on what competitors are doing]

### Pain Point Signals
- From Reviews: [Quotes indicating frustrations]
- From Job Postings: [Hiring patterns indicating bottlenecks]
- From Website: [Language suggesting growth pains]

### Risk Signals
- Regulatory Exposure: [Identified regulations]
- Data Handling: [Privacy policy quality, data collection practices]

### Research Sources
- [URL 1] — [What was extracted]
- [URL 2] — [What was extracted]
- ...
```

### 3.4 Phase 0 Completion Criteria

- [ ] Client website fully navigated and data extracted
- [ ] LinkedIn company page reviewed
- [ ] Web searches completed for news, reviews, competitors
- [ ] Technology footprint assessed
- [ ] Competitor AI adoption researched
- [ ] Intake template pre-filled (every question has a researched answer or "No data found")
- [ ] Pre-engagement dossier compiled
- [ ] All sources documented
- [ ] Survey question set generated from pre-filled intake
- [ ] Custom email composed with survey link
- [ ] Email queued/sent to client

### 3.5 Survey Generation & Client Email

**Purpose:** After Phase 0 research completes, generate a comprehensive, adaptive survey that covers ALL data points needed to produce the two 30-page reports (Quality Assessment + Deployment Plan). The survey is interactive, supports save/resume, auto-adapts based on client responses, and varies in length depending on what Phase 0 research already uncovered.

#### Survey Architecture

The survey is a **conversational, state-tracked interview** delivered via the messaging platform. It is NOT a static form. It adapts in real-time based on responses.

```
┌──────────────────────────────────────────────────┐
│              SURVEY STATE MACHINE                 │
│                                                    │
│  Init → Section 1 → ... → Section N → Complete   │
│         ↕                   ↕                      │
│      Save/Resume         Save/Resume               │
│      (state.json)       (state.json)               │
└──────────────────────────────────────────────────┘
```

**State File:** `~/.hermes/skills/virtual-consulting/state/[client-name]-survey-state.json`

The state file tracks:
- Which sections are complete
- Each question's answer
- The current position (section + question number)
- Timestamps for save/resume
- Auto-generated follow-up questions from previous answers

#### Survey Coverage — Complete Data Acquisition

The survey covers every data point needed for BOTH reports. The question count is variable (typically 40-80 questions depending on pre-fill coverage):

| Section | Data Points Needed | Questions | Pre-fill Opportunity |
|---------|-------------------|-----------|---------------------|
| A. Business Identity & Context | Name, industry, size, revenue, locations, years, legal structure, ownership | 8-12 | High — website + LinkedIn |
| B. Current Technology Stack | All software tools, platforms, hosting, integrations, age of systems | 10-15 | Medium — detectable from web |
| C. Digital Presence | Website, social media, e-commerce, SEO, content strategy, review profile | 6-8 | High — directly observable |
| D. Customer Profile & Service | Customer segments, volume, channels, response times, CSAT, churn, ticket types | 8-12 | Medium — review sites, job posts |
| E. Sales & Marketing | Lead gen sources, conversion rates, sales process, marketing channels, spend | 8-10 | Low — mostly internal data |
| F. Operations & Admin | Key workflows, bottleneck areas, manual vs automated ratios, pain points | 10-15 | Low — internal knowledge |
| G. Financial Management | Bookkeeping method, tools, AR/AP process, forecasting, reporting cadence | 6-8 | Low — confidential |
| H. Data Readiness | Data types, storage, quality, access, security practices, backups | 8-12 | Medium — privacy policy, tech signals |
| I. Goals & Constraints | Primary objective, secondary goals, budget range, timeline, driving event, dealbreakers | 6-8 | Low — confidential |
| J. AI Attitudes & History | Past AI attempts (what, outcome), fears, hopes, team sentiment, openness to change | 6-10 | Medium — job posts, reviews |
| K. Risk & Compliance | Regulations (GDPR/HIPAA/CCPA), security concerns, vendor policies, insurance | 6-8 | Medium — industry research |
| L. Stakeholders & Change Readiness | Decision-makers, influencers, resisters, org structure, past change history | 6-8 | Low — internal dynamics |
| **TOTAL** | **Everything needed for 2x 30-page reports** | **80-120 questions** | **Variable by pre-fill** |

**Question Count Logic:**
- If Phase 0 research found 60% of data → ~40-50 survey questions needed
- If Phase 0 found 30% → ~70-80 survey questions needed
- If Phase 0 found 10% (thin web presence) → ~90-110 survey questions needed
- Each section automatically reduces questions based on pre-fill confidence (High confidence = just confirm)

#### Question Generation Rules

Each question is generated with these attributes:

```
{
  "id": "A3",
  "section": "Business Identity",
  "question": "How many full-time employees does [Company] have?",
  "type": "multiple_choice | open | likert | confirm | numeric | range",
  "prefill": {
    "value": "15-25 (estimated from LinkedIn)",
    "confidence": "B — Strong",
    "source": "LinkedIn company page"
  },
  "required_for": ["assessment.readiness.data", "deployment.training.scale"],
  "follow_ups": ["A3a", "A3b"],
  "skip_allowed": true
}
```

**Question Types:**
| Type | Format | Use Case |
|------|--------|----------|
| `confirm` | "We found X — is that correct?" | High-confidence pre-fills |
| `multiple_choice` | "Which best describes..." | Categorical data |
| `numeric` | "Approximately how many...?" | Quantities, counts |
| `range` | "Is your budget closer to...?" | Sensitive financial data |
| `likert` | "On a scale of 1-5..." | Attitudes, sentiment |
| `open` | "Tell me about..." | Qualitative context |
| `conditional` | Only shown if previous answer meets condition | Branching logic |

**Adaptive Branching:**
- If client answers "Yes, we use a CRM" → follow up: "Which CRM? How satisfied?"
- If client answers "No CRM" → follow up: "How do you track leads currently?"
- If client answers budget "<$100/mo" → narrow tool recommendations
- If client expresses fear about job displacement → add empathy + change management questions

#### Save/Resume Mechanism

The survey supports unlimited save/resume cycles via a persistent state file:

```
~/.hermes/skills/virtual-consulting/state/[client-slug]-survey-state.json
```

**State File Format:**
```json
{
  "client": "Client Name",
  "survey_id": "mifeco-survey-20260430-123456",
  "created_at": "2026-04-30T14:00:00Z",
  "last_saved_at": "2026-04-30T14:35:00Z",
  "total_questions": 87,
  "answered": 34,
  "current_section": "E",
  "current_question": 4,
  "sections": {
    "A": {
      "title": "Business Identity & Context",
      "status": "completed",
      "questions": {
        "A1": {"answer": "Confirmed", "saved_at": "..."},
        "A2": {"answer": "Corrected: 22 employees", "saved_at": "..."}
      }
    },
    "B": {
      "title": "Current Technology Stack",
      "status": "in_progress",
      "questions": {
        "B1": {"answer": "QuickBooks, Salesforce, Slack", "saved_at": "..."},
        "B2": {"answer": null, "notes": "Client hasn't answered yet"}
      }
    }
  },
  "generated_follow_ups": [
    {"from": "B1", "question": "You mentioned Salesforce — which edition?", "answered": false}
  ],
  "estimated_time_remaining": "35 min",
  "last_section_sent": "B — Current Technology Stack"
}
```

**Save Command:** At any point, the client can type:
- `save` — Saves all answers to state file, provides summary of what's done and remaining
- `resume` — Loads state file, shows current position, continues from where they left off
- `save and exit` — Save + close, with a "come back anytime" message
- `skip section` — Mark entire section as skipped, move to next (documented in assumptions log)

**Resume Flow:**
1. Agent checks for existing state file for this client
2. Loads state and identifies current position
3. Presents summary: "You completed 34 of 87 questions. Section E (Sales & Marketing) was in progress. Shall I continue?"
4. Agent re-displays the current question and proceeds

**Auto-Save:** After every 5 questions, save state automatically.

#### Survey Delivery Method

The survey is delivered conversationally through the messaging platform:

**Step 1: Opening Message**
```
Thank you for completing the purchase. I've already researched [Company] extensively.

I've prepared a comprehensive survey — it covers everything I need to build your two reports:
📋 Quality Assessment (30-page deep analysis)
📋 Deployment Plan (30-page implementation roadmap)

I'll walk you through it section by section. You can:
• Save your progress at any time by typing "save"
• Type "resume" to pick up where you left off
• Skip any question by typing "skip"
• Type "help" for options at any time

Ready to begin? Let's start with your business profile.
```

**Step 2: Section-by-Section Delivery**

For each section, the agent:
1. Announces the section heading and estimated question count
2. Presents one question at a time
3. Validates and stores each response
4. Generates adaptive follow-ups based on the answer
5. Auto-saves every 5 questions
6. Provides a section summary when completed

**Step 3: Progress Tracking**

After every section and on every save:
```
📊 Survey Progress — Section C Completed

Complete: 3 of 12 sections | 28 of 87 questions
⏱ Estimated remaining: 25 minutes

Remaining sections:
  D. Customer Profile & Service (8-12 questions)
  E. Sales & Marketing (8-10 questions)
  ...

Type "save" to stop here, "continue" to proceed, or "resume" anytime later.
```

**Step 4: Survey Complete**

When all sections are answered:
```
✅ Survey Complete!

You answered 87 of 87 questions across 12 sections.
Estimated time: 55 minutes total (across 3 sessions)

I'm now building your reports:
1️⃣ Quality Assessment — analyzing readiness, opportunities, risks...
2️⃣ Deployment Plan — phased roadmap, tool selection, ROI...

You'll receive both within 24 hours.
```

#### Phase 0 → Survey Handoff

The complete pipeline from sale to survey:

```
Sale Completed
    │
    ▼
Phase 0 Research (automated, ~5-10 minutes)
    │
    ▼
Survey State File Created
- [ ] Survey state file initialized with all sections and question IDs
- [ ] Pre-filled data mapped to survey questions with confidence levels
- [ ] Save/resume state file structure created
    │
    ▼
Agent Opens Survey: "Ready to begin your AI Readiness Survey?"
    │
    ▼
Client Responds
    ├─ "Yes, let's go" → Begin Section A
    ├─ "Not now, later" → Save state, set reminder
    └─ "Send me the questions" → Send full text as document
    │
    ▼
Survey proceeds section by section with save/resume
    │
    ▼
Survey Complete → Generate Reports

### 3.6 Assumptions & Inference Framework

**Purpose:** The AI will have incomplete data at every phase. This framework governs how to make reasonable assumptions, document them transparently, and use inference to fill gaps — ensuring the client always knows what's fact vs. what's assumed.

#### When to Make Assumptions

The AI is ENCOURAGED to make reasonable assumptions in these scenarios:

| Scenario | Assumption Approach | Documentation Required |
|----------|-------------------|----------------------|
| Missing data from pre-research | Use industry averages, company size proxies, or analogous business patterns | "Assumed based on [industry] average for companies of [size]" |
| Client declines to answer a question | Use the public data proxy + industry baseline | "Client declined to share; assumed industry baseline of [X]" |
| Inconsistent data between sources | Use the more authoritative/current source, flag discrepancy | "Source A says X, Source B says Y — using A because [reason]" |
| No data at all for a dimension | Cross-reference from known data points (e.g., revenue from employee count + industry multiples) | "Estimated by applying [methodology] to known data point [Z]" |
| Client says "I don't know" | Offer a range based on industry benchmarks | "Client uncertain; used conservative estimate of [low]-[high] range" |
| Future projections (ROI, timeline) | Use the book's standard models adjusted for company size/industry | "Projected using [book model] — see ROI Framework reference" |

#### Assumption Grading

Every assumption must be graded:

| Grade | Meaning | How It's Used |
|-------|---------|---------------|
| **A — Verified** | Confirmed by client or 2+ independent sources | Treated as fact in all outputs |
| **B — Strong** | Single reliable source + logical consistency | Used as primary data; flagged in assumptions log |
| **C — Reasonable** | Inferred from related data or industry average | Used with confidence range; sensitivity tested |
| **D — Educated Guess** | Weak signal, single indirect source, or generic average | Used only for ranges; explicitly noted as weak |
| **E — Placeholder** | No data available at all | Marked as "Needs Client Input" — drives follow-up questions |

#### The Assumptions Log

Maintain a running log throughout the engagement:

```markdown
## Assumptions Log — [Client Name]

| # | Data Point | Assumption | Grade | Source/Methodology | Impact If Wrong | Resolved? |
|---|-----------|------------|-------|-------------------|-----------------|-----------|
| 1 | Employee count | ~15-25 (LinkedIn range) | B | LinkedIn company page shows 11-50 | Revenue estimates off by 20% | ✅ Confirmed by client |
| 2 | Revenue | ~$2-5M (industry multiple) | C | Applied industry revenue/employee ratio to assumed employee count | Tool budget recommendations may be wrong | ⏳ Pending confirmation |
| 3 | Pain point priority | Customer service likely top (industry pattern) | C | Industry research: similar businesses cite CS as #1 time sink | Assessment section ordering may need revision | ⏳ |
```

#### Data Confidence Scoring

For each major section of the final assessment, calculate a confidence score:

```
Confidence = (Verified Data Points × 1.0 + Strong Inferences × 0.8 + Reasonable × 0.6 + Educated Guesses × 0.4 + Placeholders × 0.0) / Total Data Points
```

| Score Range | Meaning | Impact on Recommendations |
|-------------|---------|--------------------------|
| 90-100% | High confidence | Recommendations can be definitive |
| 70-89% | Moderate confidence | Add contingency language; recommend verification |
| 50-69% | Lower confidence | Frame as options; strong recommendation to gather more data |
| Below 50% | Low confidence | Recommend foundational data collection before committing |

#### Inference Methodology for Report Generation

When building the assessment and deployment plan, the AI MUST:

1. **Identify every data gap** — before writing a section, check what data points are missing
2. **Apply the best available inference** — from the Grades above, use the highest available
3. **Document the assumption** — include grade and methodology in the assumptions log
4. **Write with appropriate confidence language**:
   - Grade A-B: "The client reports..." or "Our research confirms..."
   - Grade C: "Industry patterns suggest..." or "Based on available data, we estimate..."
   - Grade D-E: "If this pattern holds..." or "We recommend confirming..."
5. **Sensitivity test critical assumptions** — for assumptions that significantly impact recommendations, run a "what if" scenario and note it
6. **Flag for client review** — in the final deliverable, include a "Data Confidence & Assumptions" appendix

#### What NOT to Assume

Some things should NEVER be assumed:
- Financial data (revenue, profit, budget) without client confirmation
- Internal politics or team dynamics
- Legal or compliance status without verification
- Customer satisfaction levels without data
- Employee sentiment about technology
- Specific tool pricing (always verify current pricing)

---

## 4. PHASE 1: CONFIRMATION INTAKE

### Purpose

Present the pre-filled intake template to the client for confirmation, correction, and elaboration. This is NOT a blank-slate interview — the goal is to validate and enrich what the research already found, then fill in gaps that public data couldn't cover.

### How This Differs from Traditional Intake

| Aspect | Traditional Consulting | MIFECO Pre-Fill Method |
|--------|----------------------|------------------------|
| First contact | "Tell me about your business" | "I researched your business and here's what I found — please correct anything wrong" |
| Client time required | 60-90 min interview | 15-20 min confirmation |
| Initial impression | Consultant knows nothing | Consultant came prepared |
| Value perception | Starting from zero | Immediate demonstration of competence |
| Data quality | Relies entirely on client recollection | Research + client correction (higher accuracy) |

### Confirmation Workflow

**Step 1: Present the Dossier (message to client)**

```
Thank you for signing up for the MIFECO AI Readiness Consultation.

Before we begin, I took the initiative to research [Client Name] based on publicly available information. I've pre-filled an initial assessment of your business below.

Please review each section and:
✅ Confirm — "That's correct"
✏️ Correct — Provide the accurate information
❓ Skip — "I'd rather not share that"

[Pre-Filled Dossier Summary]
- Business: [Name] — [Industry] — [Size]
- We found you at [URL]
- Your team appears to use [tool list]
- We identified [N] potential areas where AI could help based on industry patterns
```

**Step 2: Present Key Sections for Confirmation**

Go section by section through the intake template. For each section:

1. **State what was found**: "Your website shows you offer [products/services] with a team of [size]."
2. **State what was assumed**: "Based on your industry, I've estimated your customer support volume at [X] inquiries per week. Is that in the right ballpark?"
3. **Ask the critical gaps**: For data that couldn't be researched (budget, internal pain points, specific goals), ask targeted questions.

**Step 3: Dynamic Follow-up Generation**

As the client confirms or corrects, generate follow-up questions based on their responses:

- **If they correct something substantial**: Probe deeper — "Interesting, our research suggested [X]. What changed?"
- **If they confirm a pain point**: "Tell me more about how that affects your daily operations."
- **If they mention a past AI attempt**: "What happened, and what would need to be different this time?"
- **If they express hesitation about sharing data**: "I understand. Here's how that data will be used and protected."

### Using the Intake Template

The intake template (at `templates/intake-template.md`) is divided into six sections:

| Section | Purpose | Pre-Fill Coverage | Confirmation Time |
|---------|---------|-------------------|-------------------|
| Business Profile | Baseline context | High (public data) | 2-3 min |
| Pain Points & Time Audit | Friction identification | Medium (signals only) | 5 min |
| Data Readiness | Data quality assessment | Low (internal data) | 3 min |
| Goals & Constraints | Scope & reality check | Low (private info) | 3 min |
| Risk Awareness | Compliance & security | Medium (regulatory research) | 2 min |
| Stakeholders & Change Readiness | People dynamics | Low (internal dynamics) | 3 min |

### Intake Completion Criteria

The intake phase is complete when you have:
- [ ] Client has confirmed or corrected all pre-filled Business Profile data
- [ ] Client has confirmed or corrected all pre-filled Pain Point signals
- [ ] Client has answered the critical data readiness questions
- [ ] Client has provided goals, budget, and timeline
- [ ] Client has confirmed risk assessment
- [ ] Client has identified key stakeholders
- [ ] All corrections and confirmations are documented
- [ ] Client has confirmed understanding of next steps and timeline

---

## 5. PHASE 2: KNOWLEDGE ACQUISITION

### Purpose

Go beyond the initial intake to acquire the specialized knowledge needed to produce a high-quality assessment. This phase transforms general understanding into actionable intelligence.

### 4.1 Industry-Specific Research

**Goal:** Understand the client's industry context — competitors, benchmarks, regulations, and AI adoption norms.

**Research Checklist:**
- [ ] Identify the client's primary industry classification (NAICS/SIC codes if helpful)
- [ ] Research 3-5 direct competitors and their technology/AI adoption level
- [ ] Identify industry-specific AI benchmarks (e.g., average chatbot containment rate for their sector)
- [ ] Research relevant regulations and compliance requirements
- [ ] Identify industry-specific AI tools and platforms
- [ ] Find 2-3 case studies of similar businesses that successfully implemented AI

**Sources:** Industry associations, Gartner/Forrester reports (public summaries), competitor websites, LinkedIn company pages, industry-specific publications, regulatory body websites.

### 4.2 Technology Landscape Assessment

**Goal:** Map available AI tools and platforms to the client's specific needs and constraints.

**Categories to Evaluate (from Chapters 3-5, 10):**

| Category | Example Tools | Use Case Fit |
|----------|--------------|--------------|
| Customer Service AI | Tidio, Intercom, Drift, ManyChat | FAQ automation, ticket triage, 24/7 response |
| Sales & Marketing AI | HubSpot, Apollo.io, Clay, Copy.ai | Lead gen, email personalization, content creation |
| Operations & Admin AI | Zapier, Make, Nanonets | Workflow automation, document processing |
| Financial AI | QuickBooks AI, Xero, Bill.com | Bookkeeping, expense categorization, forecasting |
| Strategy & Analytics | Tableau AI, Google Analytics 4 | Reporting, trend analysis, decision support |
| AI Agent Platforms | Hermes Agent, Claude Code, OpenAI Codex | Custom multi-agent workflows (for Growth Engine) |

**Evaluation Criteria (from Chapter 10):**
1. **Business Fit:** Does it solve the specific problem? Integrates with existing tools? Can scale?
2. **Technical Fit:** Easy to implement? Reliable? Secure? Good documentation?
3. **Vendor Fit:** Financially stable? Responsive support? Active development? Good reputation?

### 4.3 Stakeholder Interviews

**Goal:** Understand perspectives from key people who will be affected by changes.

**Who to Interview:**
- Key decision-makers (owner, partners, senior management)
- End users who will use the AI tools daily
- Those who expressed skepticism during intake
- Anyone who manages the processes being automated

**Stakeholder Interview Questions:**
1. "What's the most frustrating part of your daily work?"
2. "If you could wave a magic wand and automate one thing, what would it be?"
3. "What concerns do you have about AI changing how you work?"
4. "What would make you excited about using new technology?"
5. "How do you prefer to learn new tools and systems?"

### 4.4 Web Search Enrichment

**Goal:** Gather current, real-world data on AI adoption, tool pricing, and competitor strategies.

**Search Areas:**
- Competitor AI adoption signals (job postings, case studies, press releases)
- Industry-specific AI benchmarks and statistics
- Tool reviews and comparisons (G2, Capterra, TrustRadius)
- Pricing pages for shortlisted tools
- Recent news about AI regulation affecting the client's industry
- Community discussions (Reddit, LinkedIn groups) about specific tools

### 4.5 Financial Analysis

**Goal:** Build the ROI case that justifies the recommended AI investment.

**ROI Framework (from Chapter 9):**

**Cost Categories:**
| Cost Type | Examples |
|-----------|----------|
| Direct tool costs | Subscription fees, usage-based pricing |
| Implementation costs | Setup, configuration, integration |
| Training costs | Time spent learning, training materials, external courses |
| Opportunity cost | Time spent implementing vs. running the business |
| Ongoing costs | Maintenance, upgrades, support |

**Benefit Categories:**
| Benefit Type | How to Measure |
|-------------|----------------|
| Time savings | Hours saved × hourly value of time |
| Cost reduction | Direct expense reductions (materials, labor, errors) |
| Revenue increase | Additional sales, conversions, upsells |
| Quality improvement | Error rate reduction, consistency scores |
| Customer experience | Response time, satisfaction scores |
| Employee satisfaction | Retention, engagement, reduced burnout |

**ROI Calculation Formula:**
```
Total Benefits / Total Costs = ROI Ratio
Payback Period = Total Costs / Monthly Benefits
```

**Scenario Modeling:**
- Create conservative, moderate, and optimistic scenarios
- Factor in a 20-30% learning curve productivity dip in the first 4-6 weeks
- Calculate break-even point (weeks/months to recover investment)

### Phase 2 Completion Criteria

The knowledge acquisition phase is complete when:
- [ ] Industry research completed and documented
- [ ] Technology landscape assessed with 2-3 tool options per use case
- [ ] Stakeholder interviews conducted (at minimum: decision-maker + 2 end users)
- [ ] Web searches completed for competitive context
- [ ] Financial analysis with ROI projections drafted
- [ ] All findings organized for synthesis in Phase 3

---

## 6. PHASE 3: QUALITY ASSESSMENT

### Purpose

Synthesize everything from Phases 1 and 2 into a comprehensive assessment document that gives the client a clear picture of where they are, where they could go, and what stands in the way.

### 5.1 Readiness Score

Calculate readiness across four dimensions, each scored 1-5.

**Data Readiness:**
| Criterion | Score (1-5) |
|-----------|-------------|
| Data is digitized (not paper) | ___ |
| Data is organized and accessible | ___ |
| Data quality is acceptable (minimal duplicates/errors) | ___ |
| Data security practices in place | ___ |
| Compliance requirements identified | ___ |
| **Data Readiness Average:** | ___ |

**People Readiness:**
| Criterion | Score (1-5) |
|-----------|-------------|
| Leadership commitment to change | ___ |
| Team technology comfort level | ___ |
| Identified champions exist | ___ |
| Openness to learning new tools | ___ |
| History of successful change adoption | ___ |
| **People Readiness Average:** | ___ |

**Process Readiness:**
| Criterion | Score (1-5) |
|-----------|-------------|
| Key processes documented | ___ |
| Pain points clearly identified | ___ |
| Success criteria defined | ___ |
| Current workflows understood | ___ |
| Process automation potential exists | ___ |
| **Process Readiness Average:** | ___ |

**Technology Readiness:**
| Criterion | Score (1-5) |
|-----------|-------------|
| Reliable internet and hardware | ___ |
| Core systems digitized | ___ |
| Integration capability exists | ___ |
| Budget available for tools | ___ |
| Willingness to invest time in learning | ___ |
| **Technology Readiness Average:** | ___ |

**Overall Readiness Score:**
- **4.0-5.0:** High readiness — well-positioned for AI implementation
- **3.0-3.9:** Moderate readiness — address specific gaps before proceeding
- **2.0-2.9:** Foundation needed — significant preparation required
- **Below 2.0:** Not ready — recommend foundational improvements first

### 5.2 Pain Point Prioritization Matrix

Using the Impact/Effort Matrix from Chapter 2, plot each identified pain point:

| Pain Point | Impact (1-5) | Effort (1-5) | Priority | Category |
|------------|-------------|-------------|----------|----------|
| [Pain Point 1] | | | | Quick Win / Strategic / Fill-In / Avoid |
| [Pain Point 2] | | | | Quick Win / Strategic / Fill-In / Avoid |

**Scoring Methodology (from Chapter 2):**
- **Impact Score** = (Time Savings Potential + Cost Reduction Potential + Revenue Impact Potential) / 3
- **Effort Score** = (Implementation Difficulty + Employee Acceptance Challenge) / 2
- **Quadrant Assignment:**
  - High Impact, Low Effort → **Quick Wins** (start here)
  - High Impact, High Effort → **Strategic Initiatives** (plan for these)
  - Low Impact, Low Effort → **Fill-Ins** (do if easy)
  - Low Impact, High Effort → **Avoid** (generally not worth it)

### 5.3 Opportunity Assessment

For each prioritized pain point, map to specific AI opportunities:

| Opportunity | Pain Point Addressed | Business Objective | AI Approach | Data Needed | Est. Impact | Est. Effort |
|-------------|---------------------|-------------------|-------------|-------------|-------------|-------------|
| | | | | | | |

**Business Objectives Alignment (from Chapter 6):**
Connect each opportunity to one or more of:
- Increase revenue/profitability
- Improve customer satisfaction/retention
- Reduce operational costs
- Save time on routine tasks
- Improve decision-making with better data
- Scale operations without proportional hiring
- Improve work-life balance
- Stay competitive
- Build a sellable business

### 5.4 Risk Assessment

Evaluate risks across all categories from the book's risk framework:

| Risk Category | Specific Risk | Likelihood (1-5) | Impact (1-5) | Risk Level | Mitigation |
|---------------|--------------|------------------|--------------|------------|------------|
| **Data Security** | Breach, unauthorized access, data loss | | | | |
| **Privacy** | GDPR/CCPA/HIPAA violation, consent gaps | | | | |
| **AI-Specific: Hallucination** | AI generates false information | | | | |
| **AI-Specific: Bias** | AI produces biased outcomes | | | | |
| **AI-Specific: Drift** | Model performance degrades over time | | | | |
| **Vendor Risk** | Vendor shutdown, price change, support loss | | | | |
| **Operational Risk** | Integration failure, downtime, workflow disruption | | | | |
| **Reputational Risk** | Customer backlash, brand damage from automation | | | | |

**Risk Level = Likelihood × Impact**
- 1-6: Low — monitor
- 7-12: Medium — active management
- 13-25: High — must address before proceeding

### 5.5 Recommendations

Organize recommendations in a clear, actionable format:

**Immediate Quick Wins (Next 2-4 weeks):**
1. [Recommendation] — [Rationale] — [Expected outcome]

**Strategic Initiatives (Next 1-3 months):**
1. [Recommendation] — [Rationale] — [Expected outcome]

**Long-term Vision (3-12 months):**
1. [Recommendation] — [Rationale] — [Expected outcome]

**Foundational Prerequisites (Must Do First):**
1. [Prerequisite] — [Why it's needed] — [How to accomplish]

**Not Recommended (Don't Do):**
1. [Avoid] — [Rationale]

---

## 7. PHASE 4: DEPLOYMENT PLAN

### Purpose

Translate the assessment into a concrete, actionable deployment plan that the client can execute. This is the deliverable that drives results.

### 6.1 Phased Implementation Timeline

Using the 30-60-90 day framework from Chapter 8:

**Days 1-30: Foundation**
| Week | Focus Area | Key Actions | Success Metrics |
|------|-----------|-------------|-----------------|
| 1 | Assessment & Planning | Complete goals assessment, tech inventory, data audit | Assessment complete |
| 2 | Tool Selection | Problem mapping, research, evaluate, select tools | Tools selected |
| 3 | Preparation | Data cleaning, integration setup, team prep, announce change | Data ready, team informed |
| 4 | Pilot Launch | Training sessions, soft launch, parallel run, initial feedback | Team trained, pilot running |

**Days 31-60: Implementation**
| Week | Focus Area | Key Actions | Success Metrics |
|------|-----------|-------------|-----------------|
| 5-6 | Full Rollout | Transition from parallel to primary, confirm integrations, address gaps | All users active |
| 7-8 | Stabilization | Review adoption metrics, address issues, fine-tune, document SOPs | Issues resolved |
| 9-10 | Optimization | Analyze ROI data, identify improvements, expand features | Efficiency improving |
| 11-12 | Review & Plan | Complete review, document lessons, plan next phase, update strategy | ROI measured, roadmap updated |

**Ongoing: Optimization & Expansion**
- Monthly AI review meetings (60-90 min): metrics, issues, optimization, portfolio, planning
- Quarterly AI strategy reviews (half-day): ROI, strategy, portfolio, next quarter planning

### 6.2 Tool Selection Recommendations

For each recommended tool, provide:

**Tool Recommendation Template:**
```
Tool Name: [Name]
Category: [Customer Service / Sales & Marketing / Operations / Finance / Strategy]
Price: [Monthly cost range]
Best For: [Specific use case]
Integration: [Compatibility with existing tools]
Setup Complexity: [Low / Medium / High]
Training Required: [Hours/days]
Risk Level: [Low / Medium / High]
Alternative Options: [Tool 2], [Tool 3]
```

**Selection Rationale:**
- Why this tool over alternatives
- How it addresses the specific pain point
- What data/process changes are needed
- Estimated time to value

### 6.3 Change Management Approach

Based on Chapter 8 methodology:

**Communication Plan:**
| When | Message | Channel | Audience |
|------|---------|---------|----------|
| 2-4 weeks before launch | Announcement: why, what, timeline, benefits | All-hands meeting + email | All stakeholders |
| Implementation phase | Weekly progress updates, wins, issue transparency | Team standup + written update | All team members |
| Post-launch | Monthly check-ins, quarterly reviews | Scheduled reviews | Leadership + stakeholders |

**Resistance Management:**
- **Fear of job loss:** Address proactively: "AI eliminates tasks, not jobs. Our goal is to free you for higher-value work."
- **Fear of inadequacy:** Pair skeptics with champions. Provide hands-on, patient training.
- **Fear of complexity:** Start with simplest feature. Build confidence before adding sophistication.
- **Bad past experiences:** Acknowledge the failure, differentiate this approach, start with small guaranteed win.

**Implementation Team Structure:**
- **AI Implementation Lead:** Point person who owns the process (1 person)
  - Characteristics: Tech-comfortable, respected by peers, organized, patient
  - Responsibilities: Coordinate timeline, vendor contact, training lead, monitor adoption
- **AI Champions Network:** 1-2 per department/team
  - Characteristics: Curious, positive, influential
  - Responsibilities: First-line support, share tips, report issues, model adoption

### 6.4 Training Requirements

**Training Structure (based on Chapter 8):**

**Pre-Training:**
- Send agenda and pre-reading (5 min max)
- Set up equipment and test access
- Prepare real examples from the client's business

**Training Session Format (60-90 minutes):**
1. **Why (10 min):** Connect to business goals and individual benefits
2. **What (15 min):** Overview of what the tool does
3. **How (30 min):** Live demo of core features with real data
4. **Practice (20 min):** Hands-on exercises with business scenarios
5. **Questions (15 min):** Open Q&A, address concerns
6. **Next Steps (5 min):** Clear instructions on post-training actions

**Post-Training Support:**
- Summary email with key points and quick reference guides
- Scheduled follow-up check-ins (Day 3, Day 10, Day 30)
- Peer support channels (Slack/Teams group)
- Quick reference cards for common tasks
- Monthly office hours for questions and advanced training

**Training Levels:**
| Level | Audience | Content | Duration |
|-------|----------|---------|----------|
| Level 1: Basics | All users | Core features, daily use, common scenarios | 60 min |
| Level 2: Proficient | Regular users | Advanced features, customization, best practices | 90 min |
| Level 3: Champion | Champions + Lead | Admin, troubleshooting, training others | 120 min |

### 6.5 Success Metrics & KPIs

**For Each Implementation, Track:**

| KPI Category | Specific Metric | Baseline | Target | Measurement Method | Review Frequency |
|-------------|-----------------|----------|--------|--------------------|------------------|
| **Time Savings** | Hours saved per week | Current hours | Target hours | Time tracking | Weekly |
| **Cost Reduction** | Direct cost savings ($) | Current costs | Target costs | Financial reports | Monthly |
| **Revenue Impact** | Additional revenue ($) | Current revenue | Target revenue | Sales data | Monthly |
| **Quality** | Error rate reduction (%) | Current rate | Target rate | Quality audit | Weekly |
| **Customer Experience** | Response time, satisfaction | Current metrics | Target metrics | Survey, system data | Weekly |
| **Adoption** | Active user rate (%) | 0% | 80%+ | Usage analytics | Weekly |
| **Employee Satisfaction** | Tool satisfaction score | Survey needed | 4+/5 | Survey | Monthly |

### 6.6 Risk Mitigation Plan

For each identified risk in the assessment, provide:

| Risk | Trigger | Mitigation | Contingency | Owner |
|------|---------|------------|-------------|-------|
| Low adoption | <50% active users after 4 weeks | Additional training, champion intervention, simplify workflows | Re-evaluate tool fit | AI Lead |
| AI accuracy issues | Error rate >10% after tuning | Verify data quality, adjust settings, work with vendor | Add human review step | AI Lead |
| Integration failures | Data not syncing after 48 hours | Check API status, verify credentials, test in sandbox | Manual workaround temporarily | AI Lead + Vendor |
| ROI below projection | <50% of target at 90 days | Re-verify baselines, identify shortfalls, optimize | Adjust projections, learn for next phase | Owner + AI Lead |
| Team resistance escalation | Public pushback, refusal to use | One-on-one conversations, address root fears, pair with champions | Consider role adjustments | Owner |
| Vendor issues | Support unresponsive, tool unstable | Escalate, explore alternatives | Begin transition plan | AI Lead |

---

---

## 8. PHASE 5: SALES ENABLEMENT & FOLLOW-THROUGH

### Purpose

After delivering the Assessment and Deployment Plan (Phases 3-4), execute the post-delivery sales enablement workflow: creating enriched upgrade/sales emails from the assessment data, building a campaign dashboard, creating vertical-specific social media content from anonymized case studies, and generating custom infographics per target market.

**When to trigger this phase:** Immediately after delivering Phase 3 (Assessment) or Phase 4 (Deployment Plan). The window is 7-14 days — after that, the assessment ages and momentum is lost.

### Core Principle

The assessment is a goldmine of sales material. Every data point — ROI projections, stakeholder-specific benefits, pain point metrics, cost-of-delay framing — can be repurposed into multiple sales enablement assets. Do NOT let it sit idle in a deliverable file.

### 8.1 Enriched Upgrade Email Creation

**Purpose:** Transform the raw assessment data into a high-conversion upgrade email anchored by maximum sales performance techniques.

**Data points to extract from the assessment for enrichment:**

| Source (from Phase 3 Assessment) | Email Enrichment Use |
|:--------------------------------|:--------------------|
| Conservative/Realistic/Optimistic ROI projections | Three-scenario ROI table |
| Stakeholder-specific findings (by role) | Named stakeholder benefits |
| Pain point metrics (hours, dollars, response times) | "Before" baseline for contrast |
| Cost-of-delay calculation | Urgency framing |
| Budget range vs. projected costs | "Fits within your stated budget" |
| Specific tool recommendations with pricing | Path 1 vs Path 2 comparison |

**Enriched email structure:**

```
Subject: [Company]'s [Opportunity] — [Hero ROI] Is Waiting for Your Go-Ahead 🚀

Hi [Contact Name],

[Cold open — direct cost-of-delay statement]
"Every week that passes, [Company] loses roughly [$X] in recoverable [resource]."

[The hard numbers — extracted from assessment]
| Metric | Current | With [Phase N] | Timeline |
|--------|---------|----------------|----------|
| [Metric 1] | [Baseline] | [Target] | [Week] |

[Financial picture — three scenarios]
| Scenario | Annual Savings | Payback | First-Year ROI |
|----------|---------------|---------|----------------|
| Conservative | [$X] | [N months] | [N]% |
| Realistic | [$X] | [N months] | [N]% |
| Optimistic | [$X] | [N months] | [N]% |

[Stakeholder-specific benefits — 1-2 sentences per role]
- [Role 1] — [Specific benefit from assessment]
- [Role 2] — [Specific benefit from assessment]

[Two paths forward with side-by-side comparison]
Path 1: [Option Name] — [$X]
Path 2: [Option Name] — [$X] (Recommended)

[P.S. — specific human detail from assessment intake]
P.S. — [Name] told us during intake that [specific painful detail].
That's [N] [time periods] per year. We can give those back.
```

**Enriched email checklist:**
- [ ] Cost-of-delay framing in first paragraph ($X lost per week/month)
- [ ] Three-scenario ROI table (Conservative / Realistic / Optimistic)
- [ ] Named stakeholder benefits (real names from assessment)
- [ ] Before/after comparison table (current state vs. projected state)
- [ ] Two upgrade paths with side-by-side pricing comparison
- [ ] P.S. with specific human detail from intake
- [ ] Calendar link placeholder for scheduling
- [ ] File path: `DATA/followups/FU-XXX-email-enriched.md`

### 8.2 Campaign Dashboard Creation

**Purpose:** Build a single-page HTML dashboard that displays the upgrade email, media assets, pipeline status, and social content in one viewable location.

**Dashboard sections:**

```
┌────────────────────────────────────────────┐
│ Consulting Dashboard — [Campaign Name]     │
├────────────────────────────────────────────┤
│ Pipeline Stats | Upgrade Status (ROI)      │
├────────────────────────────────────────────┤
│ Enriched Email Preview (full text)          │
├────────────────────────────────────────────┤
│ Media Assets Grid (clickable infographics)  │
├────────────────────────────────────────────┤
│ Social Media Campaign (inline posts)        │
├────────────────────────────────────────────┤
│ Execution Checklist with status items       │
└────────────────────────────────────────────┘
```

**Dashboard creation rules:**
- Single self-contained HTML file with inline CSS (dark theme, brand colors)
- The enriched email preview should show the email body exactly as sent
- Each infographic should have a clickable preview card
- Social posts should be embedded inline showing platform (LinkedIn blue badge / X badge)
- Include a status checklist showing what's done vs. pending
- File path: `dashboard/consulting-dashboard.html` or `dashboard/[campaign]-dashboard.html`

### 8.3 Anonymous Social Media Content per Vertical

**Purpose:** Create LinkedIn and X/Twitter posts from the highest-scoring lead's case study data, anonymized (no company names, no contact names, no identifying details), adapted per vertical pipeline.

**Data source:** Use the highest-scoring (highest-priority) lead's case study data. Extract:
- The problem/metric (e.g., "55% fewer support tickets")
- The solution approach (e.g., "$199 AI Strategy Session identified 3 automation opportunities")
- The time frame (e.g., "90-day implementation")
- The ROI headline (e.g., "350%+ first-year ROI")
- The human impact (e.g., "team got Monday mornings back")

**Anonymization rules:**
- Replace all company names with "a [industry] company" / "we worked with a growing [industry] company"
- Remove contact names, locations, and any identifying details
- Keep industry-specific pain points generic but framed for the target vertical
- DO NOT fabricate specific metrics that weren't in the original data

**Output structure per pipeline run (per vertical):**

| Platform | Content | Length |
|----------|---------|--------|
| LinkedIn | Full case study narrative with stats, bullets, and 3-5 hashtags | ~200-300 words |
| X/Twitter | Condensed version with key stat in first line, 2-4 hashtags | ~200-280 chars |

**Pipeline runs (verticals to create):**
1. Education Technology
2. Healthcare IT
3. Manufacturing
4. Aerospace & Defense

Each vertical gets ONE LinkedIn post + ONE X/Twitter post = 8 posts total for 4 verticals. Each post must be adapted to the vertical audience's language and pain points.

**Social post structure (LinkedIn):**
```
**Headline:** How a[n] [Industry Ref] [Cut/Reduced/Automated] [Hero Stat] Without New Hires

[Opening hook — 1-2 sentences about the problem type]

[Body — case study summary with key stats]
✅ [Stat 1]
✅ [Stat 2]
✅ [Stat 3]
✅ [ROI stat]

[Lesson/takeaway — 1-2 sentences]

[Call to action — optional, soft]

#Hashtag1 #Hashtag2 #Hashtag3 #MIFECO
```

**Social post structure (X/Twitter):**
```
[Hero Emoji] [Industry] Case Study: [One-line summary]

[2-3 bullet stats]

Biggest win? [Human impact line].

#Hashtag1 #Hashtag2
```

### 8.4 Custom Infographics per Vertical

**Purpose:** Generate one branded infographic per vertical pipeline run, matching the social media campaign. Each infographic uses the same anonymous case study adapted for that vertical's audience.

**Infographic design specifications:**
- Dark theme background (#0f172a) with brand accent (#00ffcc)
- Dimensions: 800px × 1000px (social-friendly portrait ratio)
- Format: Self-contained SVG-embedded HTML file
- Font: JetBrains Mono for numbers, system sans-serif for body
- Grid background pattern with subtle radial glow

**Each infographic must include:**
1. Vertical name/identifier (e.g., "EdTech", "Healthcare IT")
2. Hero stat displayed prominently (the key metric for that vertical)
3. "Started with a $199 AI Strategy Session" brand line
4. "90-day implementation timeline"
5. "350%+ first-year ROI"
6. "No data science team required"
7. Vertical-adapted problem/solution flow
8. MIFECO branding footer

**Color themes per vertical:**

| Vertical | Color Gradient | Hero Stat | Tagline |
|----------|---------------|-----------|---------|
| Education Technology | Blues (#0a66c2 → #1e40af) | 55% fewer support tickets | "Start with problems, not technology" |
| Healthcare IT | Greens (#22c55e → #166534) | 50% compliance time cut | "Compliance-aware AI isn't a contradiction." |
| Manufacturing | Ambers (#f59e0b → #92400e) | 70% DFM feedback automated | "Manufacturing patterns are predictable. ROI is undeniable." |
| Aerospace & Defense | Reds (#ef4444 → #991b1b) | 55% evidence collection reduced | "Same compliance as Lockheed. Fraction of the budget." |

**File naming:** `DATA/dashboards/infographic-[vertical].html`

### 8.5 Phase 5 Completion Criteria

- [ ] Enriched upgrade email created from full assessment data
- [ ] Campaign dashboard built showing email + media + social posts
- [ ] 4 LinkedIn posts drafted (one per vertical, anonymous)
- [ ] 4 X/Twitter posts drafted (one per vertical, anonymous)
- [ ] 4 custom SVG infographics generated (one per vertical)
- [ ] FU-XXX.json updated with enriched email status
- [ ] All posts ready for human approval (not auto-posted)

### 8.6 Phase 5 Pitfalls

| Pitfall | Why It Happens | How to Avoid |
|---------|---------------|--------------|
| **Raw assessment dumped as email** | Takes the assessment verbatim instead of extracting key points | The email must be a REDUCTION, not a reprint. Extract 3-5 most compelling data points. |
| **Anonymized case study still identifiable** | Unique metric combinations (e.g., "a 4-person edtech company with 92% auto-rate") | Check that no combination of metrics could uniquely identify the source company. |
| **Identical social posts across verticals** | Copy-pasting with only the industry name changed | Each vertical needs a different angle, different pain point emphasis, and different language. |
| **Dashboard too complex** | Trying to build a full web app instead of a static page | Self-contained HTML only. No frameworks, no build tools, no server. |
| **Infographics too generic** | Using the same layout for all four verticals | Each layout should be unique (BEFORE→AFTER, timeline, process flow, shield/compliance). |

---


## 9. KNOWLEDGE CHECKLIST

The following data points MUST be acquired during the engagement. Track completion status for each.

### Phase 0: Pre-Engagement Research
- [ ] Client website fully navigated and data extracted
- [ ] LinkedIn company page reviewed
- [ ] Web searches completed for news, reviews, competitors
- [ ] Technology footprint assessed
- [ ] Competitor AI adoption researched
- [ ] Intake template pre-filled
- [ ] Pre-engagement dossier compiled
- [ ] Assumptions Log initialized
- [ ] Survey question set generated from pre-fill
- [ ] Custom email composed with survey link
- [ ] Email sent to client
- [ ] Survey responses received and mapped to intake template
- [ ] Survey save/resume state file maintained and accessible
- [ ] All survey data entered into Assumptions Log
- [ ] Adaptive follow-up questions generated and answered
- [ ] Complete data set assembled for 30-page reports

### Phase 1: Confirmation Intake
- [ ] Business name, industry, size (employees/revenue), years in operation
- [ ] Current technology stack (all software/tools used)
- [ ] Current digital presence (website, social media, e-commerce)
- [ ] Top 3 most time-consuming weekly tasks (with estimated hours)
- [ ] Biggest operational frustration (in client's own words)
- [ ] Customer service volume, channels, and handling method
- [ ] Sales/marketing process description (from lead gen to close)
- [ ] High-value vs. low-value time ratio estimate
- [ ] Data types collected and storage method
- [ ] Data quality assessment (duplicates, completeness, accuracy)
- [ ] Data security practices and access controls
- [ ] Primary business goal for 6-12 months (with urgency score)
- [ ] Budget range for AI investment
- [ ] Technical comfort level (owner + team average)
- [ ] Timeline urgency and driving event
- [ ] Regulatory/compliance requirements (GDPR, HIPAA, CCPA, etc.)
- [ ] Previous AI experience (positive or negative)
- [ ] Key decision-makers and their stance on AI
- [ ] Stakeholders affected by changes
- [ ] Change readiness assessment (past history, team attitude)

### Phase 2: Knowledge Acquisition
- [ ] Industry-specific research (competitors, benchmarks, regulations)
- [ ] 3-5 competitor AI adoption profiles
- [ ] Technology landscape mapped to client's use cases
- [ ] 2-3 tool options evaluated per opportunity
- [ ] Stakeholder interviews conducted (min: 3 people)
- [ ] Web search enrichment completed (reviews, pricing, comparisons)
- [ ] ROI projections (conservative, moderate, optimistic scenarios)
- [ ] Total cost of ownership calculated
- [ ] Payback period estimated
- [ ] Financial analysis document created
- [ ] Assumptions Log updated with all inferred data points
- [ ] Data confidence scores calculated for each assessment section

### Phase 3: Assessment
- [ ] Readiness score calculated (data, people, process, technology)
- [ ] Pain point prioritization matrix completed
- [ ] Opportunity assessment with business objective alignment
- [ ] Risk assessment across all 8 categories
- [ ] Recommendations organized (quick wins, strategic, long-term)
- [ ] Foundational prerequisites identified
- [ ] "Not recommended" items listed with rationale
- [ ] Assumptions Log reviewed and confidence levels updated
- [ ] Sensitivity analysis performed on critical assumptions

### Phase 4: Deployment
- [ ] Phased implementation timeline (30-60-90 day plan)
- [ ] Tool selection recommendations with pricing
- [ ] Change management communication plan
- [ ] Resistance management strategy
- [ ] Implementation team structure defined
- [ ] Training plan with levels and timelines
- [ ] Success metrics and KPIs with baselines and targets
- [ ] Risk mitigation plan (risks, triggers, mitigations, contingencies)
- [ ] KPI dashboard template
- [ ] Monthly review meeting agenda
- [ ] Quarterly review agenda
- [ ] Assumptions Log finalized with all resolved items
- [ ] Data Confidence appendix written for final deliverable

---

## 9. OUTPUT TEMPLATES

### 9.1 Assessment Output (assessment-output.md) — 30-Page Deep Analysis

The assessment document is a comprehensive 30-page analysis that synthesizes Phases 0-3. It must draw deeply from the book "AI That Works for Small Business" — using its frameworks, case studies, and methodologies. Every recommendation must cite specific book content.

**Page Budget (30 pages):**
1. **Executive Summary** (2 pages) — Key findings, readiness score, top 3 recommendations
2. **About This Assessment** (1 page) — Methodology (Assess→Choose→Implement→Optimize), data sources, confidence score
3. **Business Context** (3 pages) — Full profile, industry analysis, competitive landscape with competitor AI adoption profiles
4. **Current State Deep Dive** (5 pages) — Technology audit, pain point analysis using Chapter 2 Time Audit framework, process mapping
5. **Readiness Assessment** (4 pages) — Four-dimension scoring (Data × People × Process × Technology) from Chapter 2 methodology, with detailed gap analysis per dimension
6. **Opportunity Map** (5 pages) — Prioritized opportunities using Impact/Effort Matrix (Ch 2), mapped to business objectives (Ch 6), with industry benchmarks (Ch 10), ROI projections (Ch 9)
7. **Risk Assessment** (3 pages) — Risk matrix across all 8 categories (Ch 11), data security framework (Ch 1), compliance analysis, vendor risk evaluation
8. **Recommendations** (4 pages) — Quick wins, strategic initiatives, foundations, don't-do list. Each recommendation cites the relevant book chapter and framework
9. **Data Confidence & Assumptions** (2 pages) — Assumptions Log, confidence scoring per section, sensitivity analysis
10. **Next Steps** (1 page) — Immediate actions, transition to deployment phase

**Depth Requirements:**
- Every section must reference specific content from the book (chapter numbers, framework names, case studies)
- Analysis must be client-specific, not generic template content
- Readiness scores must include justification, not just numbers
- Risk assessment must include industry-specific regulations
- Recommendations must include estimated effort, expected impact, and sequencing logic
- All assumptions must be graded (A-E) and their potential impact assessed

### 9.2 Deployment Plan Output (deployment-plan.md) — 30-Page Implementation Roadmap

The deployment plan is a comprehensive 30-page phased implementation roadmap. It translates assessment into action using the book's 30-60-90 day framework (Ch 8), ROI methodology (Ch 9), tool evaluation criteria (Ch 10), and change management approach (Ch 8). It also incorporates the Growth Engine pipeline (Appendix) for advanced implementations.

| Page Budget (30 pages): |
|---|
1. **Executive Summary** (2 pages) — What we're doing, why, timeline to first value, expected ROI
2. **Phased Implementation Timeline** (5 pages) — 30-60-90 day breakdown with weekly actions per the book's Chapter 8 structure
3. **Tool Selection** (5 pages) — Recommended tools with pricing, alternatives, and detailed evaluation using Chapter 10's criteria:
   - Business Fit: problem match, integration, scalability
   - Technical Fit: implementation ease, reliability, security, documentation
   - Vendor Fit: stability, support, development, reputation
4. **Change Management Plan** (3 pages) — Communication plan, resistance management strategies (Ch 8), implementation team structure with AI Lead + Champions Network
5. **Training Plan** (3 pages) — Three-level training structure (Ch 8): Basic, Proficient, Champion. Pre-training, session format, post-training support
6. **Success Metrics & KPI Dashboard** (3 pages) — Baselines, targets, measurement methods for each KPI category (Ch 9):
   - Time Savings, Cost Reduction, Revenue Impact, Quality, Customer Experience, Adoption, Employee Satisfaction
7. **ROI Projections** (3 pages) — Conservative, moderate, optimistic scenarios (Ch 9). Payback period, 12-month TCO, break-even analysis
8. **Risk Mitigation Plan** (2 pages) — Risks, triggers, mitigations, contingencies per Ch 11
9. **Review Cadence** (1 page) — Monthly and quarterly review agendas per Ch 8
10. **Growth Engine Integration** (2 pages) — For advanced clients: Appendix-based agent pipeline setup with lead generation, engagement, and compliance agents
11. **Appendices** (1 page) — Tool evaluation details, vendor comparison, resource list

**Depth Requirements:**
- Every week in the 30-60-90 timeline must have specific, verifiable actions
- Tool recommendations must include actual pricing research, not estimates
- Training plan must specify who, what medium, duration, and success criteria
- KPI dashboard must include baseline measurement methodology
- Change management must address specific resistance types identified in assessment
- Risk mitigation must assign owners and trigger conditions

---

## 10. PITFALLS — Common Consulting Mistakes to Avoid

### Strategic Pitfalls

| Pitfall | Why It Happens | How to Avoid |
|---------|---------------|--------------|
| **Solution-first consulting** | Consultant wants to impress with AI knowledge | Always start with problems. Let the client's pain points drive the recommendations. |
| **One-size-fits-all recommendations** | Using a template without customization | Every recommendation must be tailored to the client's specific industry, size, stack, and culture. |
| **Overpromising results** | Consultant optimism bias | Use conservative ROI projections. Factor in learning curve dip (20-30% productivity loss first 4-6 weeks). |
| **Ignoring the human side** | Comfortable with technology, less comfortable with people | Dedicate equal attention to change management and technical implementation (Chapter 8). |
| **Scope creep** | Client keeps adding requests during assessment | Define clear scope boundaries. Document out-of-scope items for future phases. |

### Assessment Pitfalls

| Pitfall | Why It Happens | How to Avoid |
|---------|---------------|--------------|
| **Skipping the time audit** | Seems tedious, client pushes back | Time audit is non-negotiable. Without it, recommendations are guesses. Make it easy (3-day tracking). |
| **Not verifying data claims** | Taking the client's word on data quality | Ask to see actual spreadsheets, reports, or database exports. Verify data sample for quality. |
| **Missing stakeholder concerns** | Only talking to the owner | Interview at least 2-3 people who will be end users. Their concerns differ from the owner's. |
| **Underestimating compliance needs** | Client says "we're not regulated" | Verify this independently. Many businesses have compliance obligations they're unaware of. |

### Deployment Pitfalls

| Pitfall | Why It Happens | How to Avoid |
|---------|---------------|--------------|
| **Implementing too fast** | Client wants results immediately | Follow the 30-60-90 day plan. Rushing causes resistance and abandonment. |
| **Parallel run skipped** | "We'll just switch over" | Always run old and new systems in parallel for 1-4 weeks (Chapter 8). |
| **Training treated as one-time event** | "We did the training, they should know it" | Training is ongoing. Provide just-in-time resources, monthly refreshers, advanced sessions. |
| **No champion identified** | Owner wants to manage adoption themselves | Identify and empower champions in each department. Peer support is more effective than top-down mandates. |
| **Metrics not tracked** | "We'll know if it's working" | Define metrics and baselines before implementation. Measure continuously. Without data, you're guessing. |
| **Tool abandoned after launch** | No ongoing optimization | Establish monthly review cadence. AI tools need continuous tuning, just like any business system. |

### Communication Pitfalls

| Pitfall | Why It Happens | How to Avoid |
|---------|---------------|--------------|
| **Using jargon** | Consultant wants to sound expert | Speak in business terms, not tech terms. Explain everything in language the client understands. |
| **Not setting expectations** | Assuming client knows what's involved | Explicitly state: timeline, effort required from them, expected productivity dip, and when to expect results. |
| **Ignoring the skeptic** | Focusing only on enthusiastic stakeholders | Engage skeptics directly. Their concerns are often valid and can prevent implementation failures. |
| **Celebrating too early** | Announcing success before stabilization | Wait until 90-day mark and verified ROI before declaring success. Early wins are promising, not proven. |

---

## APPENDIX: TOOLS & REFERENCES

### Key Frameworks Referenced
| Framework | Source | Usage |
|-----------|--------|-------|
| Assess → Choose → Implement → Optimize | Book Core Framework | Phases 1-4 |
| Impact/Effort Matrix | Chapter 2 | Pain point prioritization |
| SMART Objectives | Chapter 2 | Goal setting |
| AI Readiness Profile | Chapter 2 | Readiness scoring |
| Four Pillars Strategy | Chapter 6 | Strategy alignment |
| 30-60-90 Day Plan | Chapter 8 | Implementation timeline |
| Change Management Framework | Chapter 8 | People adoption |
| ROI Framework | Chapter 9 | Financial analysis |
| Tool Evaluation Checklist | Chapter 10 | Tool selection |
| Risk Categories | Chapter 11 | Risk assessment |
| 16-Step Pipeline | Appendix | Growth Engine workflows |

### Quick Reference: Book Chapters by Consulting Phase

| Phase | Key Chapters | Key Concepts |
|-------|-------------|--------------|
| Pre-Engagement (0) | Ch 2, 10 | Industry research, tech detection, competitive analysis |
| Intake (1) | Ch 2 | Time audit, pain points, data readiness |
| Knowledge (2) | Ch 3-5, 7, 10 | Application areas, tool landscape |
| Assessment (3) | Ch 2, 6, 11 | Readiness scoring, strategy alignment, ethics |
| Deployment (4) | Ch 8, 9, 12, Appendix | Implementation, change mgmt, ROI, playbook |
| Sales Enablement (5) | Assessment Data, Phase 3-4 Outputs | Enriched upgrade email, dashboard display, social media from anonymized case studies, custom infographics per vertical |

---

*Skill Version: 2.0 — MIFECO Virtual Consulting Framework*
*Based on "AI That Works for Small Business" by Bob Mills*


---

## Web Implementation Reference

For the actual deployed consulting pipeline architecture (PHP + Python hybrid, Stripe integration, survey flow, database schema, backdoor login, deployment procedures), see:
`references/consulting-pipeline-architecture.md`

Live at: `https://mifeco.com/consult/`

---

## Admin Dashboard Integration

The MIFECO admin dashboard (`mifeco.com/admin/`) has sidebar tabs linking to:
- 📚 Books, ☁️ SaaS, 💼 Consulting, 📊 Lead & Promotion (internal sections)
- 🎨 Content Command Center (external page)
- 🤖 Jarvis (`/jarvis`, new tab)
- ⚙️ Admin (`/admin`, new tab)
- 💬 Consult (`/consult`, new tab)
- 📖 Books Site (`/books`, new tab)

**Jarvis Page** (`mifeco.com/jarvis/`):
- Standalone HTML page (not part of React SPA)
- Dark-themed AI assistant interface with chat UI
- Files: `/home/dh_mwpxuu/mifeco.com/jarvis.html` and `/home/dh_mwpxuu/mifeco.com/jarvis/index.html`

See `references/admin-dashboard-integration.md` for full details.

## OpenClaw Migration: virtual-consulting-orchestrator

# Virtual Consulting Orchestrator

## Overview

Run MIFECO's virtual consulting workflow as a structured revenue and delivery system.

**Entry tier:** $199 AI Strategy Session (Q&A format, entirely AI-driven virtual consultation)
**Core tier:** Custom monthly retainer ($2K-$10K/month)
**Implementation tier:** Agent Systems Implementation ($25K-$100K+)

**Primary channels:** LinkedIn + cold email (per board Decision 5)
**Delivery model:** Sub-agents + CEO agent, hybrid (per board Decision 11)
**Lead search runs concurrent with book launch** (per board Decision 7)

---

## Engagement Tiers

### Entry Tier: $199 Strategy Session — LAUNCH FIRST
- Q&A survey of key business leaders (1-2 hours total)
- Written summary + action items as deliverable
- Use case: initial consultation, specific question answers, strategy kickoff
- Stripe payment required before delivery

### Core Tier: Advisory Retainer — LAUNCH AFTER ENTRY VALIDATION
- Virtual advisory with monthly touchpoints
- Deliverables: Monthly strategy review, ongoing advisory, email support
- 3-month minimum commitment
- Use case: Fractional CTO services, ongoing AI leadership

### Agent Systems Implementation — LAUNCH THIRD
- Design, build, deploy custom AI agent systems
- Integrates with existing systems (CRM, ERP, databases)
- Training, documentation, ongoing optimization
- Use case: Companies ready to deploy AI agents in production

---

## Lead Generation (Channels Only)

**Channel 1: LinkedIn organic promotion**
- Targeted at Mars Society and Mars Technology Institute audiences
- Case studies, AI Myth Busters, tool comparisons
- Personal outreach to members of these communities

**Channel 2: Cold email outreach**
- Researched targets in the Mars/space sector
- Personalized sequences (not mass email language)
- CTA: book strategy session via Stripe link

---

## Sales Funnel Metrics

- Lead-to-order conversion rate
- Lead clicks vs. email
- Lead clicks vs. social media ads

---

## Delivery Workflow

1. Lead generated (LinkedIn or email)
2. Qualify and send Stripe payment link
3. Payment confirmed → book session
4. Conduct Q&A session
5. Deliver written summary + action items
6. Identify upsell path (retainer or implementation project)

---

## Delivery Model

**Sub-agents + CEO agent, hybrid model.**

Bob provides oversight and strategic direction. Sub-agents execute:
- Research tasks
- Analysis generation
- Deliverable drafting
- Survey creation
- Report compilation

CEO agent coordinates handoffs between sub-agents.

---

## Channel Routing

Route operational updates to:
- Topic 12 (Virtual consulting product line) in Ai Topics forum
- Chat ID: -1003883088282

---

## Escalation

Escalate to CEO immediately if:
- Client disputes or dissatisfaction signals
- Payment failures
- Scope creep requests
- Technical blockers

## Sign-post

Ready for Phase 1 execution: $199 session, LinkedIn + email, sub-agent delivery model.
