---
name: stripe-payment-collection
description: "Stripe payment integration for MIFECO products and services. Covers Checkout, Billing, webhooks, and refund processing for consulting, SaaS, and book sales."
category: business
tags: [stripe, payment, billing, checkout, webhook]
related_skills: [virtual-consulting, saas-operations, sales-pipeline-infrastructure]
---

# Stripe Payment Collection

## When to Use
- Setting up payment for a new MIFECO product or service
- Troubleshooting Stripe integration issues
- Processing refunds or handling disputes
- Configuring webhooks for payment events

## Stripe Configuration

All Stripe keys are loaded from environment variables:
- `STRIPE_PK` — Publishable key (pk_live_xxxxx)
- `STRIPE_SK` — Secret key (sk_live_xxxxx)
- `STRIPE_PRICE` — Price ID for the product (price_xxxxx)
- `STRIPE_WHSEC` — Webhook signing secret (whsec_xxxxx)

## Current Products

| Product | Price | Stripe Price ID | Status |
|---------|-------|----------------|--------|
| AI Readiness Assessment | $199 one-time | `price_CHANGEME` | Needs real key |
| Business Transformation | $1,499 one-time | Not configured | Pending |
| Deep-Dive Consulting | $3,999 one-time | Not configured | Pending |
| Project Hypatia Pro | $99/mo | Not configured | Pending |
| PM Accelerator | $69/mo | Not configured | Pending |
| VibraEngineer | $29/mo | Not configured | Pending |

## Checkout Flow
1. Client clicks "Get Started" on landing page
2. Client creates account / signs in
3. Client is redirected to Stripe Checkout
4. Client enters payment details
5. Stripe processes payment
6. Client is redirected back to mifeco.com/consult/pay.php?success=1
7. Webhook fires asynchronously to confirm payment
8. Survey record is created

## Webhook Events Handled
- `checkout.session.completed` — Payment successful, create survey
- `payment_intent.payment_failed` — Payment failed, mark as failed
- `charge.refunded` — Refund processed, mark as refunded

## Setup Checklist
1. Create Stripe account at stripe.com
2. Get API keys from Stripe Dashboard → Developers → API keys
3. Create products and prices in Stripe Dashboard
4. Set up webhook endpoint: `https://mifeco.com/consult/stripe-webhook.php`
5. Install Stripe PHP SDK: `composer require stripe/stripe-php`
6. Add keys to environment variables on DreamHost
7. Test in Stripe test mode first (use pk_test_ / sk_test_ keys)

## Security Notes
- Never hardcode Stripe keys in PHP files
- Always verify webhook signatures
- Use HTTPS for all payment pages
- Implement idempotency for webhook processing
- Log all payment events for audit trail
