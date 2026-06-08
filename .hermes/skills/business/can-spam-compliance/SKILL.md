---
name: can-spam-compliance
description: "CAN-SPAM Act compliance audit and remediation for email-sending systems — physical address, unsubscribe mechanism, suppression list, List-Unsubscribe header, ad labeling, and abuse contact"
version: 1.0.0
author: Hermes
tags: [can-spam, compliance, email, legal, audit, marketing]
---

## 🔍 MemPalace Query (MANDATORY FIRST STEP)
Before proceeding, query MemPalace for existing context:
```python
import sys, os; sys.path.insert(0, os.path.expanduser('~/.hermes/mempalace'))
import embed; embed.init_embedding(os.path.expanduser('~/.hermes/mempalace'))
results = embed.search_embeddings("CAN-SPAM email compliance legal audit", k=5)
```
This retrieves previous decisions, domain-specific context, and lessons learned from the vector memory store.

# CAN-SPAM Compliance Remediation

## Trigger
Use this skill when:
- The user requests a CAN-SPAM audit of email functions
- You are building or modifying an email-sending system that sends commercial/bulk mail to US recipients
- A legal compliance review of email outreach is needed
- Marketing or sales sequences need unsubscribe + physical address added

## CAN-SPAM Act — The Seven Requirements

1. **No false or misleading header information** — From, To, Reply-To, routing must be accurate
2. **No deceptive subject lines** — Subject must reflect email content
3. **Identify as an advertisement** — Commercial emails should be identifiable (AD: prefix or similar)
4. **Valid physical postal address** — Your current street address, P.O. Box, or registered commercial address
5. **Opt-out mechanism** — Clear explanation of how to unsubscribe; must be easy and free
6. **Honor opt-out within 10 business days** — Suppression list must be checked before each send
7. **Beacon/pixel disclosure** — If tracking opens, disclose it (less common requirement)

## Remediation Checklist

### 1. Physical Postal Address
- Add to every email body (plain text and HTML)
- Format: `Business Name — Street/City/State/Zip`
- Location: End of email, separated by `---` line

### 2. Unsubscribe Mechanism
Pick one or both:
- **Reply-based**: "To unsubscribe, reply with 'UNSUBSCRIBE' in the subject line"
- **Link-based**: "To unsubscribe, click: https://yoursite.com/unsubscribe" — requires backend endpoint
- **Mailto-based**: "To unsubscribe, email: abuse@domain.com?subject=Unsubscribe"

For link-based, implement a REST endpoint that adds the email to a suppression file.

### 3. Suppression List
- Simple text file (`suppression-list.txt`), one email per line, lowercase
- Check before every send — return 403 if suppressed
- Log every unsubscribe with timestamp for audit trail
- Must suppress within 10 business days

### 4. List-Unsubscribe Header
Add to email headers:
```
List-Unsubscribe: <https://domain.com/unsubscribe>, <mailto:abuse@domain.com?subject=Unsubscribe>
List-Unsubscribe-Post: List-Unsubscribe=One-Click
```
Enables one-click unsubscribe in Gmail, Outlook, Yahoo, etc.

### 5. Ad Labeling
- Prepending `AD:` to commercial/sales email subjects is a common safe harbor approach
- Non-commercial (transactional/relationship) emails do NOT need it
- Common distinction: SaaS sales = commercial, Books nurture = relationship/newsletter

### 6. Abuse Contact
- Include `abuse@domain.com` in email footers
- Configure the mailbox to capture abuse/violation reports

## Common Code Patterns

### PHP — Suppression Check + Footer
```php
// Suppression check
private function is_suppressed($email) {
    $file = '/path/to/suppression-list.txt';
    if (!file_exists($file)) return false;
    $list = file($file, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES);
    return in_array(strtolower(trim($email)), array_map('strtolower', $list));
}

// Footer
private function build_footer($unsubscribe_url) {
    $footer = "\n\n---\nMIFECO — 147 Bathclub Cir, N. Redington Beach, FL 33708\n";
    if ($unsubscribe_url) $footer .= "To unsubscribe: $unsubscribe_url\n";
    $footer .= "Abuse reports: abuse@domain.com\n";
    return $footer;
}
```

### Python — Footer Injection
```python
PHYSICAL_ADDRESS = "147 Bathclub Cir, N. Redington Beach, FL 33708"
ABUSE_EMAIL = "abuse@domain.com"

def build_can_spam_footer(unsubscribe_url=None):
    footer = f"\n\n---\nMIFECO — {PHYSICAL_ADDRESS}\n"
    if unsubscribe_url:
        footer += f"To unsubscribe: {unsubscribe_url}\n"
    else:
        footer += 'To unsubscribe, reply with "UNSUBSCRIBE" in the subject or body.\n'
    footer += f"Abuse reports: {ABUSE_EMAIL}\n"
    return footer
```

### REST Unsubscribe Endpoint
```python
# POST /unsubscribe
# Body: {"email": "user@example.com"}
def handle_unsubscribe(email):
    if is_suppressed(email):
        return {"success": True, "message": "Already unsubscribed"}
    with open("suppression-list.txt", "a") as f:
        f.write(email.lower() + "\n")
    log("UNSUBSCRIBE", email)
    return {"success": True, "message": "Unsubscribed"}
```

### Duplicate Endpoint Pitfall

When auditing WordPress plugins for CAN-SPAM compliance, check for **duplicate REST endpoints** across multiple plugins. A common pattern:

1. A "pipeline-setup" plugin registers `/mifeco/v1/send-email` with old credentials
2. A newer "mailer" plugin registers the same endpoint with updated credentials
3. WordPress uses the **first registered** endpoint — the old one wins

**Detection**: Search all plugin files for conflicting endpoint registrations:
```bash
grep -rn 'register_rest_route.*send-email' wp-content/plugins/
grep -rn 'mifeco_handle_send_email' wp-content/plugins/
grep -rn 'Rm2214ri%%%%' wp-content/plugins/
```

**Fix**: Remove the old endpoint registration from the pipeline-setup plugin entirely. Keep only the canonical mailer plugin.

### Secret Consistency Checklist

When updating authentication secrets across a WordPress deployment, check ALL of these locations:
- The mailer plugin PHP file (`$secret_key` variable)
- The content-command-center.html JS file (hardcoded in fetch calls)
- The webhook.php file (`$SECRET` variable)
- The api.php file (`$WEBHOOK_SECRET` variable)
- Any HTML templates with hardcoded secrets in URLs or JS
- **Search broadly**: `grep -rn 'old-secret-pattern' wp-content/ admin/`

### Unsubscribe URL Format (nginx hosting)

On nginx-hosted WordPress (DreamHost), `/wp-json/` paths return the SPA HTML. Unsubscribe URLs in email footers MUST use:
```
https://domain.com/index.php?rest_route=/mifeco/v1/unsubscribe
```
NOT:
```
https://domain.com/wp-json/mifeco/v1/unsubscribe  ← Returns SPA HTML on nginx
```

## MIFECO-Specific Configuration

| Constant | Value |
|----------|-------|
| FROM_EMAIL | MIFECOinc@gmail.com |
| FROM_NAME | MIFECO |
| ABUSE_EMAIL | MIFECOinc@gmail.com |
| ABUSE_KEYWORD | ABUSE |
| PHYSICAL_ADDRESS | 147 Bathclub Cir, N. Redington Beach, FL 33708 |
| SUBJECT_TAG | [MIFECO] |
| WP_SECRET | JY2pcWpfu1*JeubsVBpm |
| UNSUBSCRIBE_URL | https://mifeco.com/wp-json/mifeco/v1/unsubscribe |

⚠️ MIFECOinc@gmail.com is a shared Gmail account — DO NOT change password without coordinating all app owners.
- **AD: on transactional emails is wrong** — Order confirmations, password resets, and account notifications are NOT commercial. Only marketing/sales emails need the label.
- **Suppression file locking** — Use `LOCK_EX` on writes to prevent corruption from concurrent requests
- **Suppression list grew too large** — For high volume, move to database. Text file is fine for <10K entries
- **CAN-SPAM is US-only** — GDPR (Europe), CASL (Canada), and other regulations have stricter requirements. CAN-SPAM is the minimum standard.
- **"Unsubscribe" reply parsing is fragile** — Users may reply "please unsubscribe me" or "stop emailing me". A simple reply-based parser needs keyword detection, not exact match.
- **Audit trail** — Log every unsubscribe with timestamp, IP, and method (link/reply/abuse) for regulator inquiries.