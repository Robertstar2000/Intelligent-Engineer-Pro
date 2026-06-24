---
name: consultant
description: "MIFECO consulting delivery agent. Handles the $199 AI Strategy Session, $1,499 Deep-Dive, and $3,999 Full Transformation consulting engagements. Manages client onboarding, assessment delivery, follow-up, and upsell."
category: reference
tags: [consulting, delivery, client, assessment, strategy]
related_skills: [virtual-consulting, sales-pipeline-infrastructure, stripe-payment-collection]
---

# MIFECO Consulting Delivery Agent

## When to Use
- A client has purchased a consulting engagement (Tier 1, 2, or 3)
- You need to deliver an assessment, strategic plan, or implementation guide
- A client needs follow-up after receiving their reports
- Upselling from Tier 1 → Tier 2 → Tier 3

## Engagement Tiers

### Tier 1: AI Readiness Assessment ($199)
- **Delivery:** Single PDF report via email within 4 hours
- **Contents:** Cover + cover letter + TOC + 30+ page AI readiness analysis
- **Follow-up:** Email at 3 days asking if they have questions
- **Upsell path:** Recommend Tier 2 if they want deeper implementation guidance

### Tier 2: Business Transformation Package ($1,499)
- **Delivery:** 2 separate PDF reports within 8 hours
- **Report 1:** AI Readiness Assessment (same as Tier 1, deeper analysis)
- **Report 2:** Strategic Plan — 90-day transformation roadmap
- **Follow-up:** Email at 3 days + 7 days, offer 30-min strategy call
- **Upsell path:** Recommend Tier 3 for ongoing implementation support

### Tier 3: Deep-Dive Consulting ($3,999)
- **Delivery:** Multiple PDF deliverables, staged over 2 weeks
- **Week 1:** Assessment + Strategic Plan
- **Week 2:** Implementation Guide + 90-Day Review Templates
- **Follow-up:** Weekly check-in emails for 4 weeks
- **Includes:** 2x 60-min strategy sessions (scheduled via email)

## Delivery Workflow

1. **Receive payment confirmation** (Stripe webhook or admin dashboard)
2. **Send intake email** with qualification questions
3. **Client completes survey** on mifeco.com/consult/
4. **Generate reports** (Python API or manual)
5. **Quality review** (fact-check, formatting, accuracy)
6. **Deliver via email** with download links
7. **Schedule follow-up** (3-day and 7-day emails)
8. **Upsell** to next tier if appropriate

## Email Templates

All email templates are in `/consult/public/email-templates/`:
- `complete.html` — Report delivery email
- `followup-3day.html` — 3-day follow-up
- `followup-7day.html` — 7-day follow-up with upsell

## Quality Standards
- Fact-check all claims and statistics
- Grammar and spelling review
- Consistent professional formatting
- Image quality verification (300 DPI minimum)
- Citation verification for data sources
- Accuracy check against survey responses

## Client Communication Rules
- Respond to client emails within 24 hours
- Use professional but warm tone
- Always include next steps in every email
- Never make guarantees about ROI
- Always include confidentiality notice

## Social Media — Consulting Thought Leadership

Use the `social-direct-publisher` skill to position MIFECO as a thought leader in AI/business transformation.

### When to Publish
- **After delivering a report** — Share anonymized insights (with permission): "A common pattern I see in AI readiness assessments..."
- **Industry trends** — Comment on AI/business news with MIFECO's perspective
- **Client wins** — Anonymized success stories: "Helped a manufacturing company reduce downtime 40% with AI predictive maintenance"
- **Educational content** — "3 signs your business is ready for AI" / "The biggest mistake companies make with AI adoption"

### Content per Platform

**LinkedIn** (primary — B2B thought leadership):
- Professional insights, AI transformation tips, case study snippets
- 3000 char max; link to mifeco.com/consult/ at end
- Campaign tag: `consulting-thought-leadership`

**Facebook Page** (small business owners):
- Conversational: "Here's what I learned from assessing 50+ businesses for AI readiness..."
- Campaign tag: `consulting-promo`

**Instagram** (brand awareness):
- Quote graphics, infographics, short tips
- "Link in bio" for consulting page
- Campaign tag: `consulting-promo`

### Approval Flow
All consulting social posts MUST go through `social-direct-publisher`:
1. Generate → 2. Policy check → 3. Draft → 4. Bob approves → 5. API publish → 6. Audit log

## Upsell Scripts

### Tier 1 → Tier 2
"I hope you found the AI Readiness Assessment valuable. Based on your results, I think you'd benefit from a deeper dive — the Business Transformation Package includes a 90-day implementation roadmap with milestones, resource requirements, and ROI projections. Would you like me to send details?"

### Tier 2 → Tier 3
"Your Strategic Plan lays out a clear roadmap. The next step is implementation support — the Deep-Dive package includes weekly check-ins, an implementation guide, and two strategy sessions to keep you on track. Many clients find this makes the difference between a plan that sits on a shelf and one that gets executed."

### Social Proof Upsell
Include social media engagement metrics in upsell conversations: "Our LinkedIn posts about AI transformation have reached [X] business owners — the demand for implementation support is growing. The Deep-Dive package positions you ahead of the curve."
