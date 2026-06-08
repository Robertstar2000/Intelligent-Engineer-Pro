# Stripe Express Checkout Element — Reference

## Overview

The Express Checkout Element provides one-click payment buttons (Link, Apple Pay, Google Pay, PayPal, Klarna) embedded directly in the page — no redirect to Stripe Checkout.

## Server-Side (PHP)

### Creating a Checkout Session

```php
$stripeData = [
    'line_items' => [[
        'price' => STRIPE_PRICE_ID,  // e.g., 'price_1ABC...'
        'quantity' => 1,
    ]],
    'mode' => 'payment',
    'success_url' => SITE_URL . '/pay.php?success=1&session_id={CHECKOUT_SESSION_ID}',
    'cancel_url' => SITE_URL . '/pay.php?canceled=1',
    'customer_email' => $userEmail,
    'payment_method_types' => ['card', 'link'],  // 'link' enables Link
    'metadata' => [
        'user_id' => $userId,
        'full_name' => $userName,
    ],
];

$ch = curl_init('https://api.stripe.com/v1/checkout/sessions');
curl_setopt_array($ch, [
    CURLOPT_POST => true,
    CURLOPT_POSTFIELDS => http_build_query($stripeData),
    CURLOPT_RETURNTRANSFER => true,
    CURLOPT_USERPWD => STRIPE_SECRET_KEY . ':',
]);
$response = curl_exec($ch);
$session = json_decode($response, true);
```

### Verifying Payment on Return

```php
$ch = curl_init("https://api.stripe.com/v1/checkout/sessions/" . urlencode($sessionId));
curl_setopt_array($ch, [
    CURLOPT_RETURNTRANSFER => true,
    CURLOPT_USERPWD => STRIPE_SECRET_KEY . ':',
]);
$response = curl_exec($ch);
$session = json_decode($response, true);

if ($session && ($session['payment_status'] ?? '') === 'paid') {
    // Mark payment complete in DB
}
```

## Client-Side (Stripe.js)

### Initialize Elements

```javascript
const stripe = Stripe('pk_live_...');

const appearance = {
    theme: 'night',
    variables: {
        colorPrimary: '#3b82f6',
        colorBackground: '#0d1117',
        colorText: '#f0f4ff',
        colorTextSecondary: '#94a3b8',
        colorTextPlaceholder: '#64748b',
        colorDanger: '#ef4444',
        fontFamily: 'Inter, sans-serif',
        borderRadius: '12px',
    }
};

const elements = stripe.elements({
    mode: 'payment',
    amount: 19900,       // $199.00 in cents
    currency: 'usd',
    appearance,
    paymentMethodTypes: ['link', 'apple_pay', 'google_pay', 'paypal', 'klarna', 'card'],
});
```

### Express Checkout Element

```javascript
const expressCheckout = elements.create('expressCheckout', {
    layout: { maxColumns: 2, maxRows: 3 }
});
expressCheckout.mount('#express-checkout-element');

expressCheckout.on('confirm', async (event) => {
    // Create server-side session
    const res = await fetch('/pay.php', {
        method: 'POST',
        body: formData  // action=create_session + csrf_token
    });
    const data = await res.json();
    
    if (!data.success) {
        event.error({ message: data.error });
        return;
    }
    
    // For redirect-based flows
    const result = await stripe.redirectToCheckout({ sessionId: data.sessionId });
    if (result.error) {
        event.error({ message: result.error.message });
    }
});
```

### Card Element Fallback

```javascript
const card = elements.create('card', {
    style: {
        base: {
            color: '#f0f4ff',
            fontFamily: 'Inter, sans-serif',
            fontSize: '16px',
            '::placeholder': { color: '#64748b' },
        },
        invalid: { color: '#ef4444' },
    },
});
card.mount('#card-element');
```

## HTML Structure

```html
<!-- Express Checkout buttons -->
<div id="express-checkout-element"></div>

<!-- Divider -->
<div class="or-divider"><span>or pay with card</span></div>

<!-- Card input -->
<div id="card-element"></div>
<div id="card-errors"></div>

<!-- Submit button (for card payments) -->
<button class="btn-pay" onclick="submitCardPayment()">
    Pay $199 & Begin Assessment
</button>
```

## Checklist

- [ ] Replace `pk_live_CHANGEME` with real Stripe publishable key
- [ ] Replace `price_CHANGEME` with real Stripe price ID ($199 one-time)
- [ ] Replace `sk_live_CHANGEME` with real Stripe secret key
- [ ] Enable Link in Stripe Dashboard → Settings → Payment Methods → Wallets
- [ ] Set up Stripe webhook endpoint for `checkout.session.completed`
- [ ] Install Stripe PHP SDK: `composer require stripe/stripe-php`
- [ ] Test with Stripe test keys before going live
- [ ] Verify `success_url` and `cancel_url` are absolute URLs

## Common Issues

| Issue | Cause | Fix |
|-------|-------|-----|
| Link button not showing | `link` not in `payment_method_types` | Add `'link'` to array |
| Apple Pay not showing | Domain not verified | Register domain in Stripe Dashboard → Apple Pay |
| `redirectToCheckout` deprecated | Using old Stripe.js API | Use `stripe.elements()` + Express Checkout Element |
| Session creation fails | Invalid `price_id` | Verify price exists in Stripe Dashboard |
| Webhook returns 500 | Stripe SDK not installed | `composer require stripe/stripe-php` |
