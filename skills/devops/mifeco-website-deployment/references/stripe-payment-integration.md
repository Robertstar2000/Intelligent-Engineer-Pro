# Stripe Payment Integration on DreamHost

## When to Use

Use this reference when building or maintaining Stripe payment flows on DreamHost shared hosting — specifically for the MIFECO consulting pipeline (`mifeco.com/consult/`) or any future PHP-based payment page.

---

## Stripe PHP SDK Installation on DreamHost

DreamHost shared hosting does **not** have composer pre-installed. Install it locally in the project directory:

```bash
# SSH into DreamHost, then:
cd /home/dh_mwpxuu/mifeco.com/consult
php -r "copy('https://getcomposer.org/installer', 'composer-setup.php');"
php composer-setup.php --install-dir=/home/dh_mwpxuu/mifeco.com/consult --filename=composer
php composer require stripe/stripe-php
```

This creates: `composer`, `vendor/autoload.php`, `composer.json`, `composer.lock`.

**PHP Version:** DreamHost runs PHP 8.2.x — compatible with stripe-php v20+.

---

## Webhook Handler: Required Autoloader

Every PHP file using the Stripe SDK **must** include the vendor autoloader **before** `config.php`:

```php
require_once __DIR__ . '/vendor/autoload.php';
require_once __DIR__ . '/config.php';
```

**Common pitfall:** Forgetting `vendor/autoload.php` causes `Class 'Stripe\Webhook' not found` → 500 error.

**Debugging webhook 500 errors:**
1. Is `vendor/autoload.php` included?
2. Is `vendor/` directory present? (`ls vendor/stripe/stripe-php/lib/Stripe.php`)
3. Is `STRIPE_WEBHOOK_SECRET` set correctly? (starts with `whsec_`)

GET to `stripe-webhook.php` should return **400** (no signature). If **500**, SDK not loaded.

---

## Express Checkout Element (Link, Apple Pay, Google Pay, PayPal, Klarna)

### Overview

One-click payment buttons embedded in your page — no redirect. Requires Link enabled in Stripe Dashboard → Settings → Payment Methods → Wallets.

### Frontend

```html
<div id="express-checkout-element"></div>
<div class="or-divider"><span>or pay with card</span></div>
<div id="card-element"></div>
<div id="card-errors"></div>
<button onclick="submitCardPayment()">Pay $199</button>

<script src="https://js.stripe.com/v3/"></script>
<script>
const stripe = Stripe('pk_live_...');
const appearance = {
    theme: 'night',
    variables: {
        colorPrimary: '#3b82f6', colorBackground: '#0d1117',
        colorText: '#f0f4ff', borderRadius: '12px',
    }
};
const elements = stripe.elements({
    mode: 'payment', amount: 19900, currency: 'usd', appearance,
    paymentMethodTypes: ['link', 'apple_pay', 'google_pay', 'paypal', 'klarna', 'card'],
});
const expressCheckout = elements.create('expressCheckout', { layout: { maxColumns: 2, maxRows: 3 } });
expressCheckout.mount('#express-checkout-element');

expressCheckout.on('confirm', async (event) => {
    const res = await fetch('/pay.php', { method: 'POST', body: formData });
    const data = await res.json();
    if (!data.success) { event.error({ message: data.error }); return; }
    const { error } = await stripe.confirmPayment({
        elements,
        confirmParams: { return_url: location.origin + '/pay.php?success=1&session_id=' + data.sessionId },
        redirect: 'if_required',
    });
    if (!error) window.location.href = '/survey.php';
    else event.error({ message: error.message });
});

const card = elements.create('card');
card.mount('#card-element');
</script>
```

### Server-Side (pay.php)

```php
$stripeData = [
    'line_items' => [['price' => STRIPE_PRICE_ID, 'quantity' => 1]],
    'mode' => 'payment',
    'success_url' => SITE_URL . '/pay.php?success=1&session_id={CHECKOUT_SESSION_ID}',
    'cancel_url' => SITE_URL . '/pay.php?canceled=1',
    'customer_email' => $userEmail,
    'payment_method_types' => ['card', 'link'],
    'metadata' => ['user_id' => $userId, 'full_name' => $userName],
];
// POST to https://api.stripe.com/v1/checkout/sessions with STRIPE_SECRET_KEY
```

### Express vs Redirect Comparison

| | Redirect | Express Checkout |
|--|----------|-----------------|
| User leaves site | Yes | No |
| Link | Yes | Yes (one-click) |
| Apple/Google Pay | No | Yes |
| PayPal/Klarna | No | Yes |
| Card entry | Stripe page | Your page |

---

## Backdoor Login Pattern (Testing Bypass)

Hardcoded test credentials that skip payment. Useful for QA without real charges.

### register.php

```php
$backdoorEmail = 'Robertstar@aol.com';
$backdoorPassword = 'Rm2214ri#';

if (strtolower($email) === strtolower($backdoorEmail) && $password === $backdoorPassword) {
    // Auto-create account if needed
    $stmt = $db->prepare('SELECT * FROM consulting_users WHERE email = ?');
    $stmt->execute([$email]);
    if (!$stmt->fetch()) {
        $hash = password_hash($backdoorPassword, PASSWORD_DEFAULT);
        $db->prepare('INSERT INTO consulting_users (email, password_hash, full_name, created_at) VALUES (?, ?, ?, NOW())')
           ->execute([$email, $hash, 'Test User']);
    }
    $_SESSION['user_id'] = /* fetch or lastInsertId */;
    $_SESSION['backdoor'] = true;
    redirect('/pay.php');
}
```

### pay.php

```php
if (!empty($_SESSION['backdoor'])) {
    redirect('/survey.php');  // Skip Stripe
}
```

### survey.php

```php
if (empty($_SESSION['backdoor'])) {
    requirePayment($db, $userId);  // Normal users must pay
}
```

### Backdoor Survey Reset Pattern

**Critical:** When the backdoor user logs in, always reset their survey to `initial` so they start fresh at the gateway form. Without this, a previous session's `in_progress` or `complete` survey causes the gateway to be skipped entirely — the user lands directly on assessment questions and can never reach the initial 4 gateway questions.

```php
// In register.php, after setting backdoor session:
// Reset any existing survey so backdoor always starts fresh
$db->prepare("DELETE FROM consulting_survey_responses WHERE survey_id IN (SELECT id FROM consulting_surveys WHERE user_id = ?)")->execute([$userId]);
$db->prepare("DELETE FROM consulting_survey_followups WHERE survey_id IN (SELECT id FROM consulting_surveys WHERE user_id = ?)")->execute([$userId]);
$db->prepare("DELETE FROM consulting_surveys WHERE user_id = ?")->execute([$userId]);
// Create a fresh survey
$db->prepare('INSERT INTO consulting_surveys (user_id, status) VALUES (?, "initial")')->execute([$userId]);
```

**Symptom of missing reset:** Backdoor login → survey.php shows assessment questions instead of gateway form. User clicks "Start Your Assessment" but never sees the 4 initial questions (role, business type, employees, primary issue).

**Debugging:** Check `consulting_surveys.status` for the backdoor user. If it's `in_progress` or `complete` instead of `initial`, the survey wasn't reset on login.

**Security:** Backdoor is hardcoded in PHP, session flag destroyed on logout. Remove or gate behind env check before production.

---

## Deployment Checklist

- [ ] `stripe/stripe-php` installed via composer on DreamHost
- [ ] `vendor/autoload.php` included in `stripe-webhook.php`
- [ ] `STRIPE_PUBLISHABLE_KEY` (pk_live_xxx) in config.php
- [ ] `STRIPE_SECRET_KEY` (sk_live_xxx) in config.php
- [ ] `STRIPE_PRICE_ID` (price_xxx) in config.php
- [ ] `STRIPE_WEBHOOK_SECRET` (whsec_xxx) in config.php
- [ ] Webhook endpoint in Stripe Dashboard → `/consult/stripe-webhook.php`
- [ ] Link enabled in Stripe Dashboard → Wallets
- [ ] Test webhook from Stripe Dashboard
- [ ] Test backdoor login end-to-end
- [ ] Test with Stripe test card: 4242 4242 4242 4242

---

## Multi-Step Survey Pattern (Gateway → Questions → IDK Branching)

### Flow
1. **Gateway** (`status = initial`): Collect role, issue, business type, industry, employees
2. **Questions** (`status = in_progress`): One question at a time, save progress
3. **IDK Modal**: When user picks "I don't know", show modal with two paths:
   - **Someone else knows**: Pause, save position, return later
   - **Nobody knows**: 3 diagnostic follow-up questions
4. **Complete** (`status = complete`): Generate PDF reports

### Critical Bug: `$_survey` vs `$survey`

```php
// WRONG — $_survey is not a superglobal, returns null → (int)null = 0
$surveyId = (int)$_survey['id'];

// CORRECT
$surveyId = (int)$survey['id'];
```

When `$surveyId` is 0, all `WHERE id = ?` queries affect 0 rows. The survey status never changes from `initial`, causing the gateway form to reappear after submission. **This is the #1 debugging priority when the survey gateway loops.**

### Database Table Prefix

All consulting tables use `consulting_` prefix: `consulting_users`, `consulting_payments`, `consulting_surveys`, `consulting_survey_responses`, `consulting_survey_followups`, `consulting_documents`, `consulting_activity_log`.

### MySQL Connection on DreamHost

DreamHost uses **remote** MySQL — `localhost` / unix socket won't work. Always use `-h mysql.mifeco.com` on CLI and in PHP config.

### Python API Integration

Use `callPythonAPI()` with a 5-second timeout and fall back to `generateFallbackQuestions()`:

```php
$api = callPythonAPI('/api/generate-questions', [
    'survey_id' => $surveyId, 'user_id' => $userId, 'initial_responses' => $ir
]);
$questions = (($api['success'] ?? false) && !empty($api['questions']))
    ? $api['questions']
    : generateFallbackQuestions($ir);
```

DreamHost may not reach the Python API (port 8190) due to outbound firewall restrictions. Fallback questions are comprehensive (42 questions, 8 categories).

---

## DreamHost-Specific PHP Pitfalls

### `.htaccess` — Apache 2.2 Syntax Required
DreamHost may not support `Require all denied`. Use `Order allow,deny` / `Deny from all`. A bad `.htaccess` causes 500 on every page.

### PHP Error Logging Disabled
`error_log()` does nothing on DreamHost. Use `file_put_contents('/tmp/debug.log', $msg, FILE_APPEND)` for debugging. Remove before production.

### cURL Timeout for External APIs
`CURLOPT_TIMEOUT_MS` + `CURLOPT_NOSIGNAL` may not work on shared hosting. Use `CURLOPT_TIMEOUT` (seconds, integer) instead.
