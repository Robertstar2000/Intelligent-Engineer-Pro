# Stripe Integration Reference

## Payment Link Setup

1. Go to Stripe Dashboard → Payment Links → Create
2. For each product × billing cycle combination:
   - MIFECO VibraEngineer Pro Monthly ($19)
   - MIFECO VibraEngineer Pro Annual ($190)
   - MIFECO PM Accelerator Pro Monthly ($29)
   - MIFECO PM Accelerator Pro Annual ($290)
   - MIFECO Hypatia Pro Pro Monthly ($29)
   - MIFECO Hypatia Pro Pro Annual ($290)
3. Copy the payment link ID (last segment of URL)
4. Replace placeholder URLs in each app's `src/lib/stripe.ts`

## Server-Side Webhook Scaffold

Each app's `server.ts` should have `POST /api/webhook/stripe`:

```typescript
app.post('/api/webhook/stripe', express.raw({type: 'application/json'}), async (req, res) => {
  const sig = req.headers['stripe-signature'];
  // Verify with stripe.webhooks.constructEvent(req.body, sig, webhookSecret)
  
  // Handle events:
  // - checkout.session.completed → upgrade user to pro
  // - customer.subscription.deleted → downgrade to free
  // - customer.subscription.updated → sync status
  // - invoice.payment_failed → mark past_due
  
  res.json({received: true});
});
```

## Environment Variables

```
STRIPE_WEBHOOK_SECRET=whsec_...
STRIPE_SECRET_KEY=sk_live_...
```

## Test Cards (Stripe test mode)
- Success: `4242 4242 4242 4242`
- Decline: `4000 0000 0000 0002`

## WordPress Integration

The MIFECO WordPress plugin (`mifeco-core.php`) has shortcodes:
```
[mifeco_pricing product="hypatia" tier="pro"]
[mifeco_pricing product="accelerator" tier="pro"]
[mifeco_pricing product="vibraengineer" tier="pro"]
```

These render Stripe checkout buttons on the product pages at:
- mifeco.com/hypatia
- mifeco.com/accelerator
- mifeco.com/vibraengineer
