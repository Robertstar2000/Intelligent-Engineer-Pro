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

## Common Issues
- **Content generator references Ghost CMS** — Must be adapted to WordPress REST API
- **Auto-advance rules not implemented** — Leads stuck at stage 1
- **No CRM** — leads-registry.json has no web UI
