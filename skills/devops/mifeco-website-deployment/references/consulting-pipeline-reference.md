# Consulting Pipeline — Complete Flow Reference

## When to Use

Use this reference when debugging or extending the MIFECO Virtual Consulting pipeline at `mifeco.com/consult/`.

---

## Architecture

**Hybrid:** PHP on DreamHost (user-facing pages, auth, Stripe) + Python on local machine (AI question generation, PDF building via WeasyPrint).

| Component | Location | Language | Purpose |
|-----------|----------|----------|---------|
| Landing page | DreamHost `/consult/` | PHP | Marketing, CTA buttons |
| Register/Login | DreamHost `/consult/register.php` | PHP | Auth, backdoor login |
| Payment | DreamHost `/consult/pay.php` | PHP + Stripe.js | Express Checkout Element |
| Survey | DreamHost `/consult/survey.php` | PHP | Gateway + 42 assessment questions |
| Webhook | DreamHost `/consult/stripe-webhook.php` | PHP + Stripe SDK | Payment confirmation |
| API server | Local machine port 8190 | Python | Question gen, PDF building |
| Reports | Local `~/.hermes/consulting-reports/` | Python/WeasyPrint | Generated PDFs |

---

## Survey Flow

```
Landing → register.php → pay.php → survey.php → download.php
                ↑            ↑          ↑
           backdoor      skip for    gateway (4 questions)
           bypass        backdoor    → assessment (42 questions)
                                     → IDK modal (2 paths)
                                     → complete → PDF download
```

### Database Tables (all prefixed `consulting_`)

| Table | Purpose |
|-------|---------|
| `consulting_users` | Accounts |
| `consulting_payments` | Stripe payment records |
| `consulting_surveys` | One per user, tracks status |
| `consulting_survey_responses` | Individual answers |
| `consulting_survey_followups` | "Someone else knows" pending questions |
| `consulting_documents` | Generated PDF records |
| `consulting_activity_log` | Audit trail |

### Survey Status Lifecycle

```
initial → generating_questions → in_progress → analyzing → complete
   ↑              ↑                  ↑            ↑
 gateway       loading           questions     PDF build
 form          spinner           one at a time  (Python API)
```

---

## Key Files

| File | Path (local) | Path (DreamHost) |
|------|-------------|------------------|
| Landing | `/mnt/usb_4tb/consulting/public/index.php` | `/consult/` |
| Register | `/mnt/usb_4tb/consulting/public/register.php` | `/consult/register.php` |
| Payment | `/mnt/usb_4tb/consulting/public/pay.php` | `/consult/pay.php` |
| Survey | `/mnt/usb_4tb/consulting/public/survey.php` | `/consult/survey.php` |
| Config | `/mnt/usb_4tb/consulting/public/config.php` | `/consult/config.php` |
| Fallback Qs | `/mnt/usb_4tb/consulting/public/survey-questions.php` | `/consult/survey-questions.php` |
| Webhook | `/mnt/usb_4tb/consulting/public/stripe-webhook.php` | `/consult/stripe-webhook.php` |
| API server | `/mnt/usb_4tb/consulting/api/api_server.py` | N/A (local only) |

---

## Common Issues & Fixes

### 1. Gateway form loops (reappears after submission)
**Cause:** `$surveyId` is 0 because of `$_survey` vs `$survey` typo, or survey status not updating.
**Fix:** Ensure `$surveyId = (int)$survey['id']` (not `$_survey`). Check `consulting_surveys.status` in DB.
### 2. Backdoor user skips gateway, goes straight to questions

**Symptom:** User logs in with backdoor credentials (`Robertstar@aol.com` / `Rm2214ri#`) and lands on assessment questions instead of the 4 gateway questions (role, business type, employees, primary issue). The backdoor authentication itself works (redirects to survey.php, session cookie set), but the survey state is wrong.

**Cause:** Previous survey left in `in_progress` or `complete` state. The backdoor login code does NOT reset the survey — it only sets `$_SESSION['backdoor'] = true` and redirects.

**Fix:** Backdoor login now resets survey to `initial` on every login (see `register.php` lines 99-104):
```php
$db->prepare("DELETE FROM consulting_survey_responses WHERE survey_id IN (SELECT id FROM consulting_surveys WHERE user_id = ?)")->execute([$userId]);
$db->prepare("DELETE FROM consulting_survey_followups WHERE survey_id IN (SELECT id FROM consulting_surveys WHERE user_id = ?)")->execute([$userId]);
$db->prepare("DELETE FROM consulting_surveys WHERE user_id = ?")->execute([$userId]);
$db->prepare('INSERT INTO consulting_surveys (user_id, status) VALUES (?, "initial")')->execute([$userId]);
```

**Debugging:** Check `consulting_surveys.status` for the backdoor user. If it's not `initial`, the survey wasn't reset on login.

**Important distinction:** This is NOT an authentication failure — the backdoor credentials authenticate correctly. It's a survey state issue. The user sees questions instead of the gateway form.

### 3. 404 on button click from landing page
**Cause:** Links use `/register.php` (root) instead of `/consult/register.php`.
**Fix:** All internal links must include `/consult/` prefix.

### 4. 500 on all pages
**Cause:** `.htaccess` uses `Require all denied` (Apache 2.4+ syntax).
**Fix:** Use `Order allow,deny` / `Deny from all` instead.

### 5. Questions not rendering after gateway submit
**Cause:** `$surveyId` is 0 → UPDATE affects 0 rows → status stays `initial`.
**Fix:** Same as #1. Verify `$surveyId` matches the actual `consulting_surveys.id`.

### 6. Python API unreachable from DreamHost
**Cause:** Outbound firewall on shared hosting blocks non-standard ports.
**Fix:** Fallback questions are used automatically when API times out (5s).

---

## Deployment

Use `pexpect` for password-based SFTP (sshpass is NOT available):

```python
import pexpect, sys
password = "DreamHost-SSH-password"
child = pexpect.spawn('sftp -o StrictHostKeyChecking=no dh_mwpxuu@mifeco.com', timeout=30, encoding='utf-8')
child.expect('password:', timeout=15)
child.sendline(password)
child.expect('sftp>', timeout=15)
child.sendline('cd /home/dh_mwpxuu/mifeco.com/consult')
child.expect('sftp>', timeout=10)
child.sendline('put /mnt/usb_4tb/consulting/public/survey.php survey.php')
child.expect('sftp>', timeout=30)
child.sendline('bye')
child.close()
```

---

## Credentials

| Item | Value |
|------|-------|
| DreamHost SSH user | `dh_mwpxuu` |
| DreamHost MySQL host | `mysql.mifeco.com` |
| DreamHost MySQL db | `mifeco_com_1` |
| DreamHost MySQL user | `ak48bme` |
| Backdoor email | `Robertstar@aol.com` |
| Backdoor password | `Rm2214ri#` |
| Python API URL | `http://97.91.18.250:8190` |
| Python API key | `mifeco-local-api-key-change-this` |

## Landing Page Text (Current)

The consulting landing page (`/consult/index.php`) uses the following key text:
- **Title**: "MIFECO Virtual Consulting — Business Assessment for Any Issue"
- **Hero badge**: "Comprehensive Business Assessment — Any Issue"
- **Hero headline**: "Find Out Exactly Where Your Business Stands — On Any Issue"
- **Hero subtitle**: "Get a comprehensive business assessment and strategic action plan, tailored to your specific business. Delivered in 4 hours."
- **Pain point**: "Technology Confusion" (not "AI Confusion")
- **Process step**: "Expert Analysis" (not "AI Analysis")
- **CTA**: "Join the businesses using MIFECO to cut through the noise and get clarity on any challenge."

**Important**: The virtual consulting assessment is for ANY business issue, not just AI. All text should reflect this broad scope. Do NOT use "AI Readiness" or "AI strategy" anywhere in the consulting pipeline text.
