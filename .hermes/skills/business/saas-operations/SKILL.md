---
name: saas-operations
description: "Manage MIFECO SaaS products — Project Hypatia Pro ($99/mo), PM Accelerator ($69/mo), VibraEngineer ($29/mo). Handles product lifecycle, landing pages, onboarding, billing, and feature development."
category: business
tags: [saas, product, billing, onboarding, stripe]
related_skills: [sales-pipeline-infrastructure, stripe-payment-collection, virtual-consulting]
---

# MIFECO SaaS Operations

## When to Use
- Managing SaaS product lifecycle (launch, update, sunset)
- Building or updating SaaS landing pages
- Handling onboarding email sequences
- Managing Stripe billing and subscriptions
- Planning feature development

## Product Lineup

| Product | Price | Status | Description |
|---------|-------|--------|-------------|
| Project Hypatia Pro | $99/mo | Planned | AI-powered project management for engineering teams |
| PM Accelerator | $69/mo | Planned | Project management templates + AI coaching |
| VibraEngineer | $29/mo | Planned | Vibration analysis tool for mechanical engineers |

## SaaS Pipeline Stages
1. **Identified** — Lead captured via website or referral
2. **Contacted** — Initial outreach sent
3. **Qualified** — Lead confirmed as potential customer
4. **Process** — Demo or free trial offered
5. **Demo/Free Trial** — Lead is evaluating
6. **Complete Transaction** — Payment received
7. **Followup** — Onboarding + check-in
8. **Upsell/Cross-sell** — Upgrade or additional products

## Landing Page Requirements
- Clear value proposition above the fold
- Pricing table with feature comparison
- Social proof (testimonials, case studies)
- CTA button linking to Stripe payment
- FAQ section addressing common objections
- 30-day money-back guarantee badge

## Onboarding Sequence
1. **Immediate:** Welcome email with login credentials
2. **Day 1:** Getting started guide + video tutorial
3. **Day 3:** Feature highlight email
4. **Day 7:** Check-in email + support offer
5. **Day 14:** Advanced tips + upsell to higher tier
6. **Day 30:** Renewal reminder + satisfaction survey

## Stripe Integration
- Use Stripe Checkout for one-time payments
- Use Stripe Billing for subscriptions
- Webhook endpoint: `/stripe-webhook.php`
- Handle: `checkout.session.completed`, `invoice.paid`, `customer.subscription.deleted`

## Metrics to Track
- **MRR:** Monthly recurring revenue
- **Churn rate:** % of customers canceling per month
- **LTV:** Lifetime value per customer
- **CAC:** Customer acquisition cost
- **Conversion rate:** Trial → Paid
- **Activation rate:** Signup → First value moment
## Social Media — SaaS Product Marketing

Use the `social-direct-publisher` skill to promote MIFECO SaaS products on social media.

### When to Publish
- **Product launch** — New SaaS product goes live on Cloud Run
- **Feature release** — Major feature update or improvement
- **Social proof** — User testimonials, case studies, usage milestones
- **Educational content** — AI/project management tips that position MIFECO as an expert
- **Promotional campaigns** — Free trial offers, discount codes, webinar announcements

### Content per Platform

**LinkedIn** (B2B/professional audience):
- Product announcements: "[Product] is now live — [key benefit] for [target audience]"
- Thought leadership: AI in engineering, project management best practices
- Feature highlights: "New in [Product]: [feature] helps you [benefit]"
- CTA: Link to product landing page
- Campaign tag: `saas-promo` or `saas-[product-key]`

**Facebook Page** (small business owners, makers):
- Conversational: "Tired of [problem]? [Product] can help."
- Demo videos, screenshots, user testimonials
- Campaign tag: `saas-promo`

**Instagram** (visual/brand):
- Product screenshots, UI demos, infographics
- Caption: Brief value prop + "Link in bio"
- Campaign tag: `saas-promo`

### Approval Flow
All SaaS social posts MUST go through `social-direct-publisher`:
1. Generate → 2. Policy check → 3. Draft → 4. Bob approves → 5. API publish → 6. Audit log

### Integration with SaaS Pipeline
When a SaaS product reaches "Deploy" stage in the pipeline:
1. Auto-generate launch social posts for all 3 platforms
2. Store as drafts in social publisher
3. Report in deployment summary
4. Bob approves → publish on launch day

## Common Issues

- **Content generator references Ghost CMS** — Must be adapted to WordPress REST API
- **Auto-advance rules not implemented** — Leads stuck at stage 1
- **No CRM** — leads-registry.json has no web UI
- **Social posts require approval** — Never publish SaaS social media directly from LLM output. Always route through `social-direct-publisher`.
