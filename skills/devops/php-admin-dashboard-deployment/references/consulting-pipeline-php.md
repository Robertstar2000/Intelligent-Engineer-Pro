# Consulting Pipeline — PHP Patterns & Pitfalls

## When to Use

Use this reference when building or maintaining the MIFECO consulting pipeline (`mifeco.com/consult/`) or any similar PHP-based gated survey/payment flow on DreamHost shared hosting.

---

## Architecture Overview

```
User → register.php (signup/login) → pay.php (Stripe $199) → survey.php (30-50 questions) → download.php (PDF reports)
                ↑                         ↑                      ↑
           Backdoor bypass          Express Checkout        "I don't know" branching
           (testing only)           (Link, Apple Pay,       (modal with 2 paths +
                                    Google Pay, etc.)         3 diagnostic follow-ups)
```

**Hybrid architecture**: PHP on DreamHost (auth, payment, survey UI) + Python on local machine (AI question generation, PDF building via WeasyPrint).

---

## Database Schema

Tables use `consulting_` prefix in the shared `mifeco_com_1` database:

| Table | Purpose |
|-------|---------|
| `consulting_users` | User accounts (email, password_hash, full_name, business_name, etc.) |
| `consulting_payments` | Stripe payment records (stripe_session_id, stripe_payment_intent, status, amount) |
| `consulting_surveys` | Survey state (status, questions JSON, current_question, initial_responses) |
| `consulting_survey_responses` | Individual answers (survey_id, question_id, answer) |
| `consulting_survey_followups` | "I don't know" pending follow-ups (survey_id, question_id, status) |
| `consulting_documents` | Generated PDF reports (survey_id, type, filename, status) |
| `consulting_activity_log` | Audit trail (user_id, action, details) |

**MySQL connection**: `mysql -h mysql.mifeco.com -u ak48bme -p[password] mifeco_com_1`

---

## Survey State Machine

```
initial → in_progress → analyzing → complete
  │            │             │          │
  │       One question   PDF reports   Download
  │       at a time      generated    links
  │
  └── 4 gateway questions (role, issue, business_type, employee_count)
```

---

## "I don't know" Branching Flow

When a user selects "I don't know / Not applicable" on any scale/choice question:

1. **Modal appears** with two options:
   - **"Someone else knows"** → Pause screen. Saves question index. User can return later.
   - **"Nobody knows"** → 3 diagnostic follow-up questions about why they don't know.
2. After 3 diagnostics → original question marked as "I don't know" → move to next.

---

## Backdoor Login Pattern

The MIFECO admin dashboard (`index.php`) uses a single email + password gate (not multi-user).

**Credentials:**
- Email: `Robertstar@aol.com`
- Password: `Rm2214ri#`

**In `index.php`:**
```php
$ADMIN_EMAIL    = 'Robertstar@aol.com';
$ADMIN_PASSWORD = 'Rm2214ri#';

// In the POST handler:
if ($_POST['email'] === $ADMIN_EMAIL && $_POST['password'] === $ADMIN_PASSWORD) {
    $_SESSION['logged_in'] = true;
    $_SESSION['login_time'] = time();
    header('Location: ' . $redirect);
    exit;
}
```

**For the consulting pipeline specifically** (`register.php`), the backdoor skips Stripe payment:

```php
// In register.php — BEFORE normal auth
$backdoorEmail = 'Robertstar@aol.com';
$backdoorPw    = 'Rm2214ri#';
if (strcasecmp($email, $backdoorEmail) === 0 && $password === $backdoorPw) {
    // Auto-create account if needed, then:
    $_SESSION['user_id'] = $userId;
    $_SESSION['backdoor'] = true;
    redirect('/survey.php');  // Skip pay.php entirely
}
```

**In pay.php**: `if (!empty($_SESSION['backdoor'])) redirect('/survey.php');`

> **Note**: There are two copies of `index.php` — one in `~/.hermes/pipeline-engine/dashboard/` and one in `~/FL-Hermes/pipeline-engine/dashboard/`. Always update both.

---

## Critical PHP Pitfalls (DreamHost)

### 1. `$_survey` vs `$survey` — Silent Zero Bug

`$_survey` is undefined → null → (int)0. All `WHERE id = 0` queries affect 0 rows silently.

### 2. `.htaccess` — Use Apache 2.2 Syntax

`Require all denied` causes 500 on DreamHost. Use `Order allow,deny` / `Deny from all`.

### 3. PHP Error Logging Disabled

`error_log()` does nothing on DreamHost. Use `file_put_contents('/tmp/debug.log', ...)`.

### 4. `CURLOPT_TIMEOUT_MS` Unreliable on Shared Hosting

Fire-and-forget curl may hang. Use fallback data instead.

### 5. `strcasecmp` for Email Comparison

Safer than `strtolower` for Unicode: `strcasecmp($email, $backdoorEmail) === 0`.

---

## Testing Checklist

- [ ] Backdoor login → skips Stripe → survey gateway
- [ ] Gateway submission → questions with "I don't know"
- [ ] "I don't know" modal → pause screen / diagnostic questions
- [ ] Normal user → pay.php (Stripe)
- [ ] `config.php` returns 403
- [ ] `stripe-webhook.php` returns 400 (SDK loaded)
