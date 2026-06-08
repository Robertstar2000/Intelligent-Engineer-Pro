# CAN-SPAM Remediation Checklist — MIFECO Email Pipeline

*From audit conducted 2026-05-31. This is the remediation playbook referenced by Phase 8 of the saas-security-audit skill.*

## How to Use This File

When a CAN-SPAM audit finds violations (Phase 8 of the saas-security-audit skill),
use this file as the step-by-step remediation guide. Each section maps to a Phase 8 checklist item.

---

## 8.4 — Add Physical Postal Address (CRITICAL)

**Every outbound email must include a valid physical postal address.** P.O. Box is acceptable under CAN-SPAM Act.

### Where to add it

**1. WordPress PHP mailer plugin** (`mifeco-mailer.php`):
```php
// In handle_send_email(), append to body before sending:
$address_footer = "\n\n---\nMIFECO\nP.O. Box XXX\nCity, State ZIP";
$body_with_footer = nl2br($body) . $address_footer;
$sent = wp_mail($to, $subject, $body_with_footer, $headers);
```

**2. Nurture sequence JSON files** — add to every email `body:` field:
```
\n\n---\nMIFECO\nP.O. Box XXX\nCity, State ZIP

To unsubscribe, reply with "UNSUBSCRIBE"
```

**3. Outreach HTML templates** (`data/outreach/*.html`):
```html
<div style="margin-top:20px; padding-top:10px; border-top:1px solid #eee; font-size:11px; color:#999;">
  <p>MIFECO | P.O. Box XXX, City, ST ZIP</p>
  <p><a href="mailto:rmills@mifeco.com?subject=UNSUBSCRIBE">Unsubscribe</a></p>
</div>
```

**4. Pipeline Data API** (`pipeline_data_api.py` `send_via_wordpress()`):
```python
# Append physical address to body before sending
body = message_body + "\n\n---\nMIFECO\nP.O. Box XXX, City, State ZIP"
payload["email"]["body"] = body
```

**5. Hermes send_message_tool.py** — if used for marketing, append address footer in `_send_email()`:
```python
address_footer = "\n\n---\nMIFECO | P.O. Box XXX, City, State ZIP"
message = message + address_footer
```

---

## 8.5 / 8.6 — Implement Unsubscribe Mechanism + Processing (CRITICAL)

### Option A: Reply-to-Unsubscribe with automated processing (recommended for this stack)

**Step 1: Add reply footer to all email bodies:**
```php
// In mifeco-mailer.php, append after body:
$unsubscribe_footer = "\n\nTo stop receiving these emails, reply with \"UNSUBSCRIBE\"";
```

**Step 2: Build a reply parser** — add to the Hermes email adapter or a cron script:
```python
# In the email adapter's _fetch_new_messages(), after extracting body:
import re
from pathlib import Path

SUPPRESSION_LIST = Path.home() / ".hermes" / "secrets" / "email-suppression-list.txt"

if re.search(r'\b(unsubscribe|opt\s*out|remove\s*me)\b', body, re.IGNORECASE):
    with open(SUPPRESSION_LIST, 'a') as f:
        f.write(sender_addr + '\n')
```

**Step 3: Check suppression list before sending (in `mifeco-mailer.php`):**
```php
// In handle_send_email(), after $to is determined:
$suppression_file = '/home/bob/.hermes/secrets/email-suppression-list.txt';
if (file_exists($suppression_file)) {
    $suppression = file_get_contents($suppression_file);
    if (stripos($suppression, $to) !== false) {
        return new WP_REST_Response(['success' => false, 'error' => 'Recipient has opted out'], 403);
    }
}
```

**Step 4: Add `List-Unsubscribe` email header in PHP mailer:**
```php
$headers[] = 'List-Unsubscribe: <mailto:rmills@mifeco.com?subject=UNSUBSCRIBE>';
$headers[] = 'List-Unsubscribe-Post: List-Unsubscribe=One-Click'; // RFC 8058
```

### Option B: Simple suppression list + manual management (minimum viable)

1. Create the suppression list file:
```bash
touch ~/.hermes/secrets/email-suppression-list.txt
chmod 600 ~/.hermes/secrets/email-suppression-list.txt
```

2. Manually add addresses when requested. The check in Step 3 above still applies.

---

## 8.2 — Subject Line Compliance

**Already implemented:** The pipeline auto-prepends `[SaaS]`, `[Books]`, or `[Consulting]` identifiers.

**Consider adding for consumer-facing book sales emails:**
```python
if is_promotional:
    subject = "[AD] " + subject
```

---

## Credential Rotation (from audit findings)

The old REST secret was hardcoded in 3+ locations. When rotating:

1. Generate new secret: `openssl rand -hex 32`
2. Update `mifeco-mailer.php` → `$secret_key`
3. Update `pipeline_data_api.py` → `WP_SECRET`
4. Update any SKILL.md or documentation
5. Do NOT store in `.env` — belongs only in plugin source and calling code

---

## Quick Verification After Remediation

```bash
# 1. Test the PHP mailer returns address footer
curl -X POST https://mifeco.com/wp-json/mifeco/v1/send-email \
  -H "Content-Type: application/json" \
  -d '{"secret":"NEW_SECRET","email":{"to":"test@example.com","subject":"[SaaS] Test","body":"<p>Test</p>","pipeline":"SaaS"}}'

# 2. Check suppression list works
echo "test@example.com" >> ~/.hermes/secrets/email-suppression-list.txt
# Re-run the curl — should return opt-out error

# 3. Verify List-Unsubscribe header on sent email
# Send a test, then inspect headers in received email
```
