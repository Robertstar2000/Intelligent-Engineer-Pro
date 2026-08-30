---
name: saas-product-line
description: "Turn a working SaaS codebase into a sellable product. Use when preparing a SaaS for launch, creating launch assets, setting up pricing, or building GTM strategy. Starts from GitHub repository — reads markdown docs first, identifies gaps, then produces launch assets in order: product brief, environment plan, readiness assessment, packaging and pricing, distribution plan, promotion assets, outreach plan, and Stripe revenue ops."
---


## Memory context (Hindsight)

Long-term memory context is now provided automatically by Hindsight (bank
`mifeco-default`) on every turn — the retired MemPalace manual query step no
longer applies. Do NOT attempt to import `~/.hermes/mempalace` (it was removed
2026-08-19).This retrieves previous decisions, domain-specific context, and lessons learned from the vector memory store.

# SaaS Product Line — Commercialization Skill

## Overview

Turn a working SaaS codebase into a sellable product. Start from the GitHub repository, read the markdown documentation first, identify commercialization gaps, then produce launch assets in this order:

1. Product understanding and risk scan
2. Environment and operations requirements
3. Offer, pricing, and packaging
4. Distribution plan for GitHub and optional mobile channels
5. Promotion assets for LinkedIn, X, and email
6. Revenue operations using Stripe payment links

Stay commercial and execution-focused. Do not drift into generic startup advice. Ground decisions in the actual repository, docs, product surface area, and the board's constraints.

## Default operating rules

- Read the repository README and all relevant `.md` files before proposing packaging, pricing, or promotion.
- Treat the repository as the source of truth for current capabilities, dependencies, setup steps, and missing launch blockers.
- If required secrets or keys are missing, tell the user exactly what the board must provision and why.
- Do not claim a channel is ready if repo evidence is missing.
- Distinguish clearly between:
  - what exists now
  - what can be shipped with light packaging work
  - what requires engineering work before sale
- Prefer simple monetization and low-friction distribution first.
- Treat iOS and Android as optional release tracks unless the repo clearly includes mobile clients or wrappers.
- Draft promotional content, lists, and workflows by default. Only execute tool actions like sending email or posting when the user explicitly asks.

## Workflow

Follow this sequence.

### 1. Ingest the product

Collect and summarize:

- GitHub repo URL
- Primary product purpose
- Target buyer
- Current deployment model
- Evidence from markdown docs: setup, features, pricing hints, API notes, architecture, roadmap, compliance notes

Produce a short product brief:

- Product category
- Core problem solved
- Ideal customer profile
- Key features already working
- Known gaps and risks
- Commercialization readiness score: ready, near-ready, or not-ready

### 2. Define the environment and access plan

After reviewing the repo, produce a requirements plan and board action checklist.

Include only keys that are justified by repo evidence or necessary launch operations, such as:

- app runtime keys
- database credentials
- auth provider keys
- analytics keys
- email delivery keys
- app store credentials if mobile release is in scope
- social platform credentials only if automation is explicitly requested
- Stripe keys for payment links and webhook verification if checkout is in scope

For each item, state:

- variable name
- purpose
- who should provision it
- whether it is required for dev, staging, production, or launch ops

If secrets are not yet known, produce a list and a board action checklist instead of guessing values.

### 3. Assess sale readiness

Check these areas:

- onboarding friction
- authentication and account lifecycle
- billing entry point
- legal pages needed
- support path
- observability and error handling
- analytics and conversion tracking
- demoability
- installation clarity
- upgrade path and versioning

Use three buckets:

- **Ship now** — ready without changes
- **Ship after light packaging work** — needs minor effort
- **Blocked until engineering fixes** — significant work required

Consult `references/release-checklist.md` when building this assessment.

### 4. Package the offer for sale

Create a commercialization package that includes:

- product name and one-line positioning
- target customer and buying trigger
- pricing recommendation
- offer structure
- landing page outline
- GitHub distribution plan
- optional mobile release plan
- support and fulfillment notes

#### Pricing guidance

Prefer a simple first offer:

- one core plan
- one premium or team plan if justified
- annual option only if it simplifies sales
- no complex enterprise packaging unless repo evidence and user context support it

#### GitHub distribution guidance

For GitHub-first products, define:

- public vs private repo approach
- release artifacts or install paths
- README improvements needed for conversion
- screenshots, demo GIF, and changelog needs
- license and commercial terms that must be clarified

#### Mobile guidance

If iOS or Android is requested, classify the path:

- native app exists
- cross-platform app exists
- web app can be wrapped
- mobile release is not credible yet

Then produce the minimum viable release path, store asset requirements, and engineering blockers.

### 5. Create go-to-market assets

Create channel-specific assets rather than one generic launch note.

Required channels:

- LinkedIn founder or company post
- X launch thread
- email outreach
- podcast outreach shortlist criteria and email copy

Consult `references/outreach-templates.md`.

For each asset, anchor the copy in:

- customer pain
- proof from shipped features
- clear CTA
- Stripe payment link or demo CTA

Do not write hype-heavy copy. Keep it specific and credible.

### 6. Build outreach recommendations

For podcast and partner outreach, recommend targets based on the SaaS niche.

Produce:

- target profile definitions first
- search terms to find relevant podcasters and newsletters
- outreach angle per target type
- concise email draft
- follow-up sequence

If specific names are not available from the prompt or tools, provide a structured prospecting method instead of inventing people.

### 7. Set up revenue operations

Default payment rail: Stripe payment links.

Produce a revenue ops plan that covers:

- product-to-payment-link mapping
- checkout CTA placement
- webhook events needed
- access fulfillment path after payment
- refund and cancellation handling
- basic dashboard metrics

Minimum metrics:

- visits to checkout
- payment-link conversion
- trial-to-paid if trials exist
- monthly recurring revenue estimate
- churn signals
- refund count
- support burden notes

Keep the first version simple. Do not design a full finance stack unless the user asks.

## Required output structure

Use this structure unless the user asks for a different format.

```
# SaaS commercialization plan

## 1. Product brief
## 2. Repo evidence reviewed
## 3. Readiness assessment and board action list
## 4. Packaging and pricing plan
## 5. Distribution plan
## 6. GTM assets
## 7. Outreach plan
## 8. Stripe link revenue ops
## 9. Immediate next actions
```

## Quality bar

Before finishing, verify that the plan:

- cites repo evidence or explicitly marks assumptions
- separates ready work from blocked work
- gives the board a concrete requirements and setup request
- includes actual promotional drafts, not just advice
- includes a monetization path tied to Stripe payment links
- includes next actions in execution order

## Failure modes to avoid

Do not:

- assume the product is sale-ready because it runs locally
- recommend mobile app release without evidence
- invent integrations, customers, metrics, or security posture
- bury blockers inside long prose
- produce generic marketing language disconnected from the repo
- skip the board setup request for secrets and keys when needed

## Resource files

- `references/release-checklist.md` — launch-readiness review checklist
- `references/outreach-templates.md` — channel templates and messaging structure
