# Stripe Webhook Events Reference

## Payment Link Events

| Event | Description | When to Use |
|-------|-------------|-------------|
| `checkout.session.completed` | Customer completed checkout | Trigger service delivery |
| `checkout.session.expired` | Checkout session expired | Follow up with customer |
| `payment_intent.created` | Payment intent created | Log for tracking |
| `payment_intent.succeeded` | Payment confirmed | Confirm order fulfillment |
| `payment_intent.payment_failed` | Payment failed | Retry or notify customer |
| `payment_intent.canceled` | Payment canceled | Clean up resources |

## Subscription Events

| Event | Description |
|-------|-------------|
| `customer.subscription.created` | New subscription started |
| `customer.subscription.updated` | Subscription modified |
| `customer.subscription.deleted` | Subscription canceled |
| `invoice.payment_succeeded` | Subscription payment received |
| `invoice.payment_failed` | Subscription payment failed |

## Customer Events

| Event | Description |
|-------|-------------|
| `customer.created` | New customer record |
| `customer.updated` | Customer info changed |
| `customer.deleted` | Customer removed |

## Dispute Events

| Event | Description |
|-------|-------------|
| `charge.dispute.created` | Chargeback initiated |
| `charge.dispute.closed` | Dispute resolved |

## Payout Events

| Event | Description |
|-------|-------------|
| `payout.created` | Payout initiated |
| `payout.paid` | Payout completed |
| `payout.failed` | Payout failed |
