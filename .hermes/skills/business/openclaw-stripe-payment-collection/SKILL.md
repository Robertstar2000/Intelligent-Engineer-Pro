---
name: stripe-payment-collection
description: Use this skill whenever the user wants to collect payments for a SaaS or delivery service using Stripe payment links. Triggers when the user mentions Stripe, payment links, collecting payments, subscription billing, checkout, invoicing, or wants to automate payment collection for a service. Always use this skill when building payment workflows in OpenClaw or any automated pipeline that needs to accept money without manual intervention.
---


## 🔍 MemPalace Query (MANDATORY FIRST STEP)
Before proceeding, query MemPalace for existing context:
```python
import sys, os; sys.path.insert(0, os.path.expanduser('~/.hermes/mempalace'))
import embed; embed.init_embedding(os.path.expanduser('~/.hermes/mempalace'))
results = embed.search_embeddings("Stripe payment collection SaaS subscription billing", k=5)
```
This retrieves previous decisions, domain-specific context, and lessons learned from the vector memory store.

# Stripe Payment Collection Skill

This skill enables automated payment collection using Stripe Payment Links — no checkout page coding required. Payments are collected but funds stay in the Stripe account (not automatically paid out) until explicitly triggered.

---

## Overview

Stripe Payment Links let you:
- Generate a shareable URL that accepts payments
- Collect one-time or recurring payments
- Track payment status via webhooks or API polling
- Hold funds in your Stripe balance without auto-payout

---

## Prerequisites

- Stripe account (live or test mode)
- Stripe Secret Key (`sk_live_...` or `sk_test_...`)
- Optional: Stripe Webhook Secret for event verification

Store credentials as environment variables — never hardcode them:
```
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
```

---

## Step 1: Create a Price (Product)

Before creating a payment link, you need a Price object.

```python
import stripe
import os

stripe.api_key = os.environ["STRIPE_SECRET_KEY"]

# Create a product + price (one-time)
price = stripe.Price.create(
    unit_amount=2999,  # Amount in cents ($29.99)
    currency="usd",
    product_data={"name": "SaaS Delivery Service - Basic Plan"},
)

print(f"Price ID: {price.id}")  # Save this: price_xxxx
```

For recurring/subscription pricing:
```python
price = stripe.Price.create(
    unit_amount=2999,
    currency="usd",
    recurring={"interval": "month"},
    product_data={"name": "SaaS Delivery Service - Monthly"},
)
```

---

## Step 2: Create a Payment Link

```python
payment_link = stripe.PaymentLink.create(
    line_items=[{"price": price.id, "quantity": 1}],
    # Optional settings:
    after_completion={
        "type": "redirect",
        "redirect": {"url": "https://yourapp.com/success"}
    },
    metadata={
        "service": "saas_delivery",
        "customer_id": "cust_001",  # Tag for your records
    }
)

print(f"Payment URL: {payment_link.url}")
# Share this URL with customers → they pay → funds land in your Stripe balance
```

---

## Step 3: Track Payment Status (Without Auto-Payout)

### Option A — Webhook (Recommended for Automation)

Set up a webhook endpoint in your OpenClaw pipeline to receive events:

```python
from flask import Flask, request
import stripe, os

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    payload = request.data
    sig_header = request.headers.get("Stripe-Signature")
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, os.environ["STRIPE_WEBHOOK_SECRET"]
        )
    except stripe.error.SignatureVerificationError:
        return "Invalid signature", 400
    
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        payment_intent_id = session.get("payment_intent")
        customer_email = session.get("customer_details", {}).get("email")
        amount_paid = session.get("amount_total")  # in cents
        
        # Log or trigger next step in your pipeline
        print(f"Payment received: ${amount_paid/100:.2f} from {customer_email}")
        print(f"Payment Intent: {payment_intent_id}")
        # → Trigger service delivery here
    
    return "", 200
```

Key events to listen for:

| Event | Meaning |
|-------|---------|
| checkout.session.completed | Customer paid via payment link |
| payment_intent.succeeded | Payment confirmed & funds captured |
| payment_intent.payment_failed | Payment failed |
| customer.subscription.created | New subscription started |

### Option B — Poll the API

```python
def check_payment_link_payments(payment_link_id):
    sessions = stripe.checkout.Session.list(payment_link=payment_link_id)
    for session in sessions.data:
        if session.payment_status == "paid":
            print(f"Paid session: {session.id} | Amount: ${session.amount_total/100:.2f}")
    return sessions
```

---

## Step 4: Controlling Payouts (Keep Funds in Stripe)

By default, Stripe schedules automatic payouts. To hold funds:

### Disable Auto-Payout (Stripe Dashboard)
1. Go to Settings → Payouts
2. Set payout schedule to Manual
3. Funds accumulate in your Stripe balance until you trigger a payout

### Manual Payout via API (when ready to pay out)
```python
# Only call this when you WANT to release funds
payout = stripe.Payout.create(
    amount=10000,  # cents
    currency="usd",
)
print(f"Payout initiated: {payout.id}")
```

---

## Step 5: Full Automation Example (OpenClaw Pipeline)

```python
import stripe, os

stripe.api_key = os.environ["STRIPE_SECRET_KEY"]

def create_payment_link_for_customer(customer_name: str, amount_cents: int, description: str) -> str:
    """
    Creates a Stripe payment link for a customer.
    Returns the payment URL to send to them.
    """
    # 1. Create price
    price = stripe.Price.create(
        unit_amount=amount_cents,
        currency="usd",
        product_data={"name": description},
    )
    
    # 2. Create payment link
    link = stripe.PaymentLink.create(
        line_items=[{"price": price.id, "quantity": 1}],
        metadata={
            "customer_name": customer_name,
            "service": "saas_delivery",
        }
    )
    
    return link.url

def get_balance() -> dict:
    """Check current Stripe balance (collected but not paid out)."""
    balance = stripe.Balance.retrieve()
    available = balance.available[0].amount / 100
    pending = balance.pending[0].amount / 100
    return {"available": available, "pending": pending}

# Example usage
url = create_payment_link_for_customer(
    customer_name="Acme Corp",
    amount_cents=4999,
    description="SaaS Delivery - One-Time Setup"
)
print(f"Send this to customer: {url}")

balance = get_balance()
print(f"Balance → Available: ${balance['available']} | Pending: ${balance['pending']}")
```

---

## Testing

Use Stripe test mode keys (`sk_test_...`) and test card numbers:

- ✅ **Success:** 4242 4242 4242 4242
- ❌ **Decline:** 4000 0000 0000 0002
- 🔐 **3D Secure:** 4000 0025 0000 3155

Use any future expiry date and any 3-digit CVC.

---

## Error Handling

```python
try:
    link = stripe.PaymentLink.create(...)
except stripe.error.AuthenticationError:
    print("Invalid API key")
except stripe.error.InvalidRequestError as e:
    print(f"Bad request: {e.user_message}")
except stripe.error.StripeError as e:
    print(f"Stripe error: {str(e)}")
```

---

## Reference Files

- `references/webhook-events.md` — Full list of relevant Stripe events
- `references/test-cards.md` — Stripe test card numbers and scenarios

See [Stripe Payment Links docs](https://stripe.com/docs/payment-links) for full API reference.

---

# AGENT DIRECTIVE: Execution Protocol

> **CRITICAL INSTRUCTION FOR ALL MIFECO AGENTS**

## The Golden Rule

**DO NOT SUGGEST ACTIONS. EXECUTE THEM.**

### What This Means

| ❌ DON'T | ✅ DO |
|---------|-------|
| "You could create a file..." | Create the file. |
| "I recommend running this command..." | Run the command. |
| "Here's a script you might use..." | Execute the script. |
| "Would you like me to...?" | Just do it and report results. |

### Execution Standard

When assigned a task:

1. **Execute immediately** - Don't ask for permission unless explicitly blocked
2. **Report what you did** - Not what you "would" do
3. **Show results** - Output, files created, changes made
4. **Escalate on failure** - Don't stall, notify immediately

## Failure Protocol

If you **CANNOT** perform an action:

**STEP 1:** Try alternative approaches (max 2 attempts)

**STEP 2:** If still blocked, send immediate notification:

```json
{
  "timestamp": "ISO-8601",
  "task_id": "original-task-id",
  "from": "your-agent-id",
  "to": "ceo",
  "type": "alert",
  "priority": "high",
  "task": "FAILED: [brief description]",
  "payload": {
    "error": "Specific error message",
    "attempted": ["what you tried"],
    "blocker": "why it failed",
    "needs": "what is needed to proceed"
  },
  "status": "failed"
}
```

**STEP 3:** Send Telegram notification:

```
🚨 AGENT FAILURE ALERT

Agent: [your-agent-id]
Task: [task_id]
Error: [specific error]

Needs: [what is required]
Timestamp: [ISO-8601]
```

## Telegram Notification Template

Use this exact format for Telegram alerts:

```
🚨 [AGENT] FAILED: [Brief Task Description]

Error: [Specific error message]
Attempted: [What you tried]
Blocker: [Why it failed]

Needs CEO/Board attention to proceed.
Task ID: [task_id]
```

## When to Notify

Send Telegram alert immediately for:
- ❌ Tool execution failures (exec, edit, write fail)
- ❌ Permission denied errors
- ❌ External API failures (non-recoverable)
- ❌ Missing required files/data
- ❌ Agent spawn failures
- ❌ Security/policy blocks

**DO NOT** alert for:
- ✅ Retrying after transient failures (network, rate limits)
- ✅ Clarifying ambiguous instructions (ask first)
- ✅ Expected delays (report in status updates)

## Examples

### Good Execution

User: "Create a backup script"

Agent:
```
Created backup.sh in /home/bob/scripts/

Contents:
#!/bin/bash
# Backup script
tar -czf backup-$(date +%Y%m%d).tar.gz ~/workspace

Tested: ✅ Executes successfully
Next backup: Tonight at 2 AM via cron
```

### Good Failure Handling

Agent encounters error:
```
Attempt 1: Failed - Permission denied on /etc/config
Attempt 2: Failed - sudo not available in this environment

🚨 Sending alert to CEO...

Telegram notification sent.
Waiting for escalation.
```

## Mandatory Footer

All agent responses must follow this structure:

```
[EXECUTION RESULT]

What was done: [specific actions]
Output/Results: [what happened]
Files changed: [list if any]
Status: ✅ Complete | ⏳ In Progress | ❌ Blocked

If Blocked:
🚨 Telegram alert sent: [yes/no]
Next action: [what happens next]
```

## Agent Self-Check

Before responding, verify:

- [ ] Did I actually DO the thing, or just describe it?
- [ ] Did I run the command, or just paste it?
- [ ] Did I create the file, or just show the content?
- [ ] If blocked, did I send the Telegram alert?

**Remember: Actions speak louder than suggestions.**
---

## AUTO-CONTINUE SYSTEM

This agent is monitored by the auto-continue system. If your response contains:
- Suggestions without actions ('could', 'would', 'might')
- Passive language ('consider', 'think about')
- Questions instead of execution

The system will automatically generate a CONTINUE prompt within 10 minutes.
To prevent this: ALWAYS execute immediately and show concrete results.

See AGENT_DIRECTIVE.md for complete protocol.
