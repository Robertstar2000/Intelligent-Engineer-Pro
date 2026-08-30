---
name: saas-security-audit
description: "Systematic security and compliance audit of deployed SaaS/web applications — uptime verification, security header inspection, credential exposure scanning, file permission review, SSH key check, cron job security review, and CAN-SPAM email compliance auditing."
version: 1.1.0
author: CEO Agent
tags: [security, audit, saas, web-apps, credential-scan, security-headers, compliance, can-spam, email]
related_skills: [ceo-agent-orchestrator, system-reliability-monitoring, dogfood]
---


## Memory context (Hindsight)

Long-term memory context is now provided automatically by Hindsight (bank
`mifeco-default`) on every turn — the retired MemPalace manual query step no
longer applies. Do NOT attempt to import `~/.hermes/mempalace` (it was removed
2026-08-19).This retrieves previous decisions, domain-specific context, and lessons learned from the vector memory store.

# SaaS Security Audit

## Trigger
Use this skill when performing a security audit of deployed web applications — whether as a weekly/monthly recurring check, a pre-launch security review, or a response to a security concern. Also use when any of these conditions are true:
- A new SaaS app is deployed to production
- A periodic (weekly/monthly) security review is due
- A security incident or concern has been raised
- A new cron job, script, or configuration file was added
- The user asks for a "security audit" or "security check" of their apps
- The user asks for a "CAN-SPAM audit", "CAN-SPAM compliance check", or "email compliance audit"
- The user asks to add unsubscribe links, opt-out mechanisms, or physical address footers to outbound email
- The user asks to add "List-Unsubscribe headers" or "email footer compliance"
- The user asks to "add security headers" or "fix missing security headers" on web apps
- The user asks to "harden" a web app or "add HSTS/CSP/X-Frame-Options"
- The user asks to "deploy helmet" to Express/Node.js apps

## What This Covers
This skill performs a 7-point security audit across all deployed SaaS/web applications and supporting infrastructure:

1. **Uptime & availability** — verify each app loads (200 OK)
2. **Security headers** — check for X-Frame-Options, CSP, HSTS, X-Content-Type-Options, X-XSS-Protection, Referrer-Policy
3. **Console errors** — browser JavaScript console scan
4. **Credential exposure** — scan agent-communications.jsonl, .env, config files, scripts for leaked API keys/passwords/tokens
5. **File permissions** — check config files for world-readability (should be 600), SSH keys (should be 600/644)
6. **Script security** — check shell/python scripts for hardcoded credentials, unsafe patterns
7. **Cron job security** — verify no exposed credentials in cron commands, no world-writable scripts, no missing script paths
8. **CAN-SPAM email compliance** — audit all outbound email functions against CAN-SPAM Act requirements (see Phase 8 below)

## Workflow

### Phase 1: Uptime & Console Check
For each SaaS app URL, use the browser tool to:
1. Navigate to the URL
2. Confirm 200 OK status
3. Check browser_console() for JavaScript errors
4. Optionally, capture a screenshot with browser_vision() for visual verification

### Phase 2: Security Headers
For each app URL, check HTTP response headers. Use curl (preferred) or the browser to verify these headers are set:

| Header | Recommended Value | Purpose |
|--------|-------------------|---------|
| X-Frame-Options | DENY | Clickjacking prevention |
| Content-Security-Policy | default-src 'self' (minimum) | XSS prevention |
| Strict-Transport-Security | max-age=31536000 | HSTS enforcement |
| X-Content-Type-Options | nosniff | MIME-sniffing prevention |
| X-XSS-Protection | 1; mode=block | Legacy XSS filter |
| Referrer-Policy | strict-origin-when-cross-origin | Referrer leakage prevention |

```bash
# Check headers with curl
curl -sI https://example.com | grep -iE "x-frame|x-content|x-xss|strict-transport|content-security|referrer"
```

### Phase 3: Credential Exposure Scan
Scan these locations for exposed credentials:

1. **`agent-communications.jsonl`** — search for patterns: `API_KEY`, `sk-`, `pk-`, `password`, `secret`, `token`, `key=`
2. **`~/.hermes/scripts/*.sh`** — search for hardcoded API keys, passwords, tokens
3. **`~/.hermes/.openclaw/` config files** — check that API keys are truncated/masked (e.g., `"sk-or-...fee5"`, `"AIzaSy...ntDY"`)
4. **`~/.hermes/.env`** — verify via `hermes doctor` or targeted grep
5. **SSH keys** at `~/.ssh/` — permissions should be 600 for private keys
6. **Check for `.env`, `.netrc`, `.aws` credential directories** that might contain exposed secrets

### Phase 4: File Permissions
```bash
# Check config file permissions
ls -la ~/.hermes/.openclaw/openclaw.json  # Should be 600
ls -la ~/.ssh/id_ed25519                   # Should be 600
ls -la ~/.ssh/id_ed25519.pub               # Should be 644
```

### Phase 5: Script & Cron Security
```bash
# Check cron jobs
crontab -l

# Check script permissions
find ~/.hermes/scripts/ -name "*.sh" -type f | xargs ls -la

# Verify no missing script paths in crontab
crontab -l | grep -v '^#' | while read line; do
  script=$(echo "$line" | grep -oP '/[^ ]+\.(py|sh)' || true)
  [ -n "$script" ] && [ ! -f "$script" ] && echo "MISSING: $script"
done
```

### Phase 8: CAN-SPAM Email Compliance Audit

Scan all email-sending code, templates, sequences, and infrastructure for CAN-SPAM Act (15 U.S.C. § 7701-7713) compliance. This is a regulatory compliance audit — treat missing items as HIGH severity.

**Map the email pipeline first:**

```bash
# Find all email-sending code
find /home/bob/.hermes -type f \( -name "*.py" -o -name "*.php" -o -name "*.js" -o -name "*.json" -o -name "*.html" \) | \
  xargs grep -l -iE "(send_email|wp_mail|smtp|unsubscribe|opt.out)" 2>/dev/null

# Check live email config (if loaded)
cat ~/.hermes/secrets/mifeco-dreamhost.env 2>/dev/null | grep -iE "smtp|from|secret"
```

**Audit checklist — every outbound email system must satisfy ALL of these:**

| # | CAN-SPAM Requirement | What to Check | Severity if Missing |
|---|---|---|---|
| 8.1 | **Accurate "From" identity** | Sender name + email truthful. Check `$from_email`, `$from_name`, `From:` header in PHP plugin, Python SMTP code, and all email templates | HIGH |
| 8.2 | **Non-deceptive subject line** | Subject reflects message content. Check nurture sequences, auto-generated subjects, and any subject-line-prepend logic | HIGH |
| 8.3 | **Message identified as ad** (if commercial) | Commercial emails must be identifiable as ads. Check for AD label or equivalent. B2B emails are lower risk but consumer emails (e.g., book sales) may need `AD:` prefix | MEDIUM |
| 8.4 | **Valid physical postal address** | Every email must include a valid physical postal address — P.O. Box is acceptable. Check every nurture sequence body, outreach HTML template email footer, the PHP plugin output body, and any hardcoded email footers. This is the most common CAN-SPAM violation | **CRITICAL** |
| 8.5 | **Clear opt-out mechanism** | Every email must include a clear way to unsubscribe. Check for: (a) unsubscribe link in email body, (b) `List-Unsubscribe` email header, (c) reply-to-unsubscribe with automated handler. A `settings.json` that says `"unsubscribe_behavior": "reply_to_unsubscribe"` is NOT sufficient unless an automated reply parser actually exists in code | **CRITICAL** |
| 8.6 | **Opt-out honored within 10 business days** | There must be code or a process that processes opt-out requests (suppression list, reply parser, webhook). Check for suppression list file/listener. If unsubscribe mechanism exists but nothing processes it → FAIL | **CRITICAL** |
| 8.7 | **Opt-out not required for transactional emails** | Order confirmations, account notices are exempt. But marketing/sales/nurture sequences are NEVER exempt. Distinguish by content | LOW |
| 8.8 | **No harvested addresses** | Verify email lists were opt-in or otherwise legally obtained. Check for purchased/scraped lists in pipeline data files | HIGH |

**Where to check:**
1. WordPress REST email plugins (`mifeco-mailer.php` and similar) — check `wp_mail()` output for address/footer
2. Python SMTP/API senders (`pipeline_data_api.py`, `send_message_tool.py`) — check message construction
3. Nurture sequence JSON files (`*nurture*.json`, `*sequence*.json`) — check every `body:` field
4. Email HTML templates (`data/outreach/*.html`, `data/outreach/*.json`) — check rendered output
5. Email platform adapter (`gateway/platforms/email.py`) — check if `List-Unsubscribe` is ever set on outbound
6. Hermes `send_message_tool.py` `_send_email()` — check if it's used for transactional only or also marketing
7. Any "Approve & Send" or "content command center" flow — the last mile before SMTP matters most

**Common pitfalls found in this codebase (MIFECO-specific, updated 2026-05-31):**
- `settings.json` has `"unsubscribe_behavior": "reply_to_unsubscribe"` but no code parses replies → automated mechanism MUST be built into the PHP plugin
- Physical address is the most-commonly-missing item — check EVERY template, not just one
- Hardcoded secrets in PHP plugins that allow unauthenticated email sending → rotation needed (use `ssh` + `wp eval` to update via WP-CLI, or deactivate/reactivate the plugin after file replacement)
- Outbound email HTML templates with `compliance` or `footer` CSS classes that render in-browser but are stripped by email clients — physical address must be in the plaintext body, not just a styled div
- **Abuse contact format**: Use the shared email (e.g., `MIFECOinc@gmail.com`) with text instructing recipients to "reply with the word ABUSE in the subject line" — do NOT use a non-functional alias like `abuse@rmills.com` - **Subject tagging for shared accounts**: When multiple apps share one email account, tag all outbound subjects with a prefix like `[MIFECO]` so replies can be identified and routed
- **AD: prefix on commercial emails**: SaaS and Consulting pipeline subjects should be prepended with `AD:` per CAN-SPAM best practice for commercial identification
- **`List-Unsubscribe` header**: Must be set on every outbound email header, not just in the body footer. Format: `<https://domain.com/wp-json/mifeco/v1/unsubscribe>, <mailto:MIFECOinc@gmail.com?subject=Unsubscribe+recipient@example.com>`
- **AllowOverride None on DreamHost**: `.htaccess` files are ignored. Do NOT attempt `.htaccess`-based rewrite rules. WordPress REST API routing works through DreamHost's panel-level config, not `.htaccess`.
- **Gmail SMTP on DreamHost WP Mail SMTP**: Use `smtp.gmail.com:587` STARTTLS. If Gmail 2FA is enabled, an App Password must be generated and used instead of the regular password.

**Typical remediation for this codebase:**

See `references/can-spam-checklist.md` for the detailed remediation playbook — including exact code changes to `mifeco-mailer.php`, `pipeline_data_api.py`, and the nurture sequence templates.

### Phase 6: Report
Generate a structured findings report with:

```
## SECURITY AUDIT REPORT — <date>

### Summary
| Category | Finding | Severity |
|---|---|---|
| Uptime | All apps operational | None |
| Security Headers | <status> | HIGH/MEDIUM/LOW |
| Credential Exposure | <status> | HIGH/MEDIUM/LOW |
| File Permissions | <status> | HIGH/MEDIUM/LOW |
| Script Security | <status> | HIGH/MEDIUM/LOW |
| Cron Jobs | <status> | HIGH/MEDIUM/LOW |
| CAN-SPAM Compliance | <status> | CRITICAL/HIGH/MEDIUM/LOW |

### Findings by Severity

**CRITICAL:** <list of items that create legal liability — missing physical address, missing unsubscribe mechanism, no opt-out processing>

**HIGH:** <list of critical issues>

**MEDIUM:** <list of moderate issues>

**LOW:** <list of minor issues>

### Recommended Actions
1. <action> — <severity, effort>
2. <action> — <severity, effort>
```

## Common Remediation Steps

### Missing Security Headers (Cloud Run apps)
For Cloud Run/Express/Node.js apps, add `helmet` middleware (the standard Express security headers library):

```bash
# Install helmet
cd /path/to/app && npm install helmet
```

```typescript
// server.ts — add import and middleware
import helmet from 'helmet';
// ...after other middleware but BEFORE routes:
app.use(helmet());
```

`helmet()` automatically sets all standard security headers with safe defaults:
- `X-Frame-Options: DENY`
- `X-Content-Type-Options: nosniff`
- `Strict-Transport-Security: max-age=15552000; includeSubDomains` (HSTS, 180 days)
- `X-XSS-Protection: 1; mode=block`
- `Referrer-Policy: strict-origin-when-cross-origin`
- `Content-Security-Policy: default-src 'self'` (and other CSP directives)

For apps that need inline scripts or external CDN resources (common in SPAs), configure CSP explicitly:

```typescript
app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      scriptSrc: ["'self'", "'unsafe-inline'", "'unsafe-eval'", "https://*.stripe.com"],
      styleSrc: ["'self'", "'unsafe-inline'"],
      imgSrc: ["'self'", "data:", "https:"],
      connectSrc: ["'self'", "https://*.stripe.com"],
      fontSrc: ["'self'", "data:"],
      frameSrc: ["https://*.stripe.com"],
    },
  },
}));
```

**Always place `app.use(helmet())` BEFORE route definitions** for headers to apply to all responses.

### Missing Security Headers (Static SPAs on Apache/Shared Hosting)

For static SPA sites deployed on Apache (e.g., DreamHost, WP Engine, SiteGround), deploy an `.htaccess` file at the web root:

```apache
# Security Headers
<IfModule mod_headers.c>
    Header always set X-Frame-Options "DENY"
    Header always set X-XSS-Protection "1; mode=block"
    Header always set X-Content-Type-Options "nosniff"
    Header always set Referrer-Policy "strict-origin-when-cross-origin"
    Header always set Permissions-Policy "geolocation=(), microphone=(), camera=()"
    Header always set Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval' https://*.stripe.com; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self' data:; connect-src 'self' https://*.stripe.com https://api.stripe.com; frame-src https://*.stripe.com"
    Header always set Strict-Transport-Security "max-age=31536000; includeSubDomains; preload"
</IfModule>

# Block access to sensitive files
<FilesMatch "^\\.">
    Require all denied
</FilesMatch>
<FilesMatch "(wp-config\\.php|\\.env|\\.sql|\\.git)">
    Require all denied
</FilesMatch>

# Enable compression
<IfModule mod_deflate.c>
    AddOutputFilterByType DEFLATE text/html text/plain text/xml text/css text/javascript application/javascript application/json
</IfModule>
```

**Deployment via SSH/SCP:**
```bash
scp /tmp/.htaccess_security user@host:/path/to/webroot/.htaccess
```

**Verify deployment:**
```bash
curl -sI https://domain.com | grep -iE "x-frame|x-content|x-xss|strict-transport|content-security"
```

### Config File Permissions
```bash
chmod 600 ~/.hermes/.openclaw/openclaw.json
```

## Pitfalls

- **browser_console() may error** on pages with no console output — that's expected and OK (it means no JS errors were logged)
- **API keys in config files may show as truncated (e.g., `"sk-or-...fee5"`)** — this is intentional masking by the config system, not credential exposure
- **Missing cron script paths** — crontab may reference scripts that were moved/renamed; flag but don't alarm unless it's a critical job
- **Empty scripts directory** — if `~/.hermes/scripts/` is empty, the agents aren't using script-based workflows and there are no scripts to audit; that's a clean finding, not an issue
- **Some browsers block mixed content** — if checking CSP headers, be aware that HTTP→HTTPS redirects may affect header visibility

## Verification
After completing the audit:
1. Confirm all findings are severity-graded correctly
2. If HIGH findings exist, create a remediation task for the engineer (do not fix yourself)
3. Log the audit completion to the communications file
4. Include the findings summary in the report
