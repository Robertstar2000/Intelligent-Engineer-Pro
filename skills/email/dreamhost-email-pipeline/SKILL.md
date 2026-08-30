---
name: dreamhost-email-pipeline
description: DreamHost email infrastructure for MIFECO — Gmail SMTP config (shared MIFECOinc@gmail.com account), subject tagging, WordPress REST endpoint, CAN-SPAM compliance, and reply routing
version: 2.0.0
author: MIFECO
tags: [email, dreamhost, smtp, wordpress, pipeline, routing]
---


## Memory context (Hindsight)

Long-term memory context is now provided automatically by Hindsight (bank
`mifeco-default`) on every turn — the retired MemPalace manual query step no
longer applies. Do NOT attempt to import `~/.hermes/mempalace` (it was removed
2026-08-19).This retrieves previous decisions, domain-specific context, and lessons learned from the vector memory store.

# DreamHost Email Pipeline — MIFECO Outbound Email System

## ⚠️ CRITICAL: nginx, NOT Apache

DreamHost shared hosting runs **nginx** as the front-end web server. There is NO Apache, no `mod_rewrite`, and `.htaccess` files are **completely ignored**.

- WordPress REST API is accessible via `/index.php?rest_route=` (NOT `/wp-json/` which returns the SPA)
- The root `index.php` contains a PHP router that routes WP paths to WordPress and everything else to the SPA
- Do NOT attempt to modify nginx config — `/etc/nginx/conf.d/` is not writable by users
- **Only the default nginx vhost** (`/etc/nginx/sites-enabled/default`) exists — DreamHost manages per-domain routing at a higher level
- **Test all API URLs from both internal (server curl) and external (public URL) contexts** — nginx routing differs
- **`mod_rewrite` may not even be loaded** — check `ls /etc/nginx/modules-enabled/` (not Apache mods-enabled)
- Use `curl` from the server to test both `http://127.0.0.1/path` (bypasses nginx vhost) and `https://www.mifeco.com/path` (full nginx routing) to diagnose routing issues

### PHP Smart Router Pattern

When WordPress coexists with a SPA on DreamHost, the root `index.php` must route requests:

```php
<?php
$request_uri = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);
$request_uri = rtrim($request_uri, '/');

$wp_paths = ['/wp-json', '/wp-admin', '/wp-login.php', '/wp-signup.php', '/xmlrpc.php'];
$is_wp = false;
foreach ($wp_paths as $wp_path) {
    if (strpos($request_uri, $wp_path) === 0) { $is_wp = true; break; }
}
if (preg_match('#^/(wp-content|wp-includes)/#', $request_uri)) $is_wp = true;
if ($request_uri === '' || $request_uri === '/index.php') $is_wp = true;

if ($is_wp) {
    define('WP_USE_THEMES', true);
    require __DIR__ . '/wp-blog-header.php';
    exit;
}
readfile(__DIR__ . '/index.html');
```

### nginx Troubleshooting Commands

```bash
# Check what's running
ps aux | grep -E 'nginx|apache|httpd' | grep -v grep

# Check nginx modules (not Apache!)
ls /etc/nginx/modules-enabled/

# Test external vs internal
curl -s -o /dev/null -w '%{http_code}' 'https://www.mifeco.com/wp-json/'
curl -s -o /dev/null -w '%{http_code}' 'https://www.mifeco.com/index.php/wp-json/'
curl -s -o /dev/null -w '%{http_code}' 'http://127.0.0.1/index.php/wp-json/'
```

## ⚠️ CRITICAL: Shared Email Account

**MIFECOinc@gmail.com** is the ONLY email account available on DreamHost. It is shared across ALL applications.

- **DO NOT change the password** without coordinating with all app owners
- All outbound email sends from `MIFECOinc@gmail.com`
- All outbound subjects are tagged with `[MIFECO]` for identification
- Abuse reports: recipients reply to `MIFECOinc@gmail.com` with `ABUSE` in the subject line
- Password: `Rm2214ri#` (stored in `~/.hermes/secrets/mifeco-dreamhost.env`)

## Architecture

```
Content Command Center  ──POST──→  WordPress REST API  ──wp_mail()──→  Gmail SMTP
  (Production mode)      /index.php  (mifeco-mailer     (WP Mail SMTP   smtp.gmail.com
                          ?rest_route  plugin)            configured)      :587 STARTTLS
                          =/mifeco/v1
                          /send-email
```

**⚠️ nginx routing:** DreamHost shared hosting uses nginx (not Apache). The `/wp-json/` path is intercepted by nginx's `try_files` and serves the SPA. The REST API is accessible via:
- `https://www.mifeco.com/index.php/wp-json/` — WP REST discovery
- `https://www.mifeco.com/index.php?rest_route=/mifeco/v1/send-email` — MIFECO endpoints

Do NOT use bare `/wp-json/` URLs — they return the SPA HTML, not JSON.

## Single Outbound Email

All product lines use ONE outbound email address. The product line is identified by the subject line identifier.

- **From:** MIFECOinc@gmail.com (the ONE shared email account)
- **From Name:** MIFECO
- **Reply-To:** MIFECOinc@gmail.com
- **Subject tag:** `[MIFECO]` prepended to all outbound subjects for shared-account identification

## Before You Start — Discover Your Actual Mailbox

DreamHost basic plans include **1 fully-hosted mailbox slot**. Before configuring anything:

1. Go to **DreamHost Panel → Mail → Manage Email** (or legacy page)
2. Look for the account marked **"Fully Hosted"** — that's your only SMTP-capable mailbox
3. Forward-only accounts (contact@, webmail@, etc.) **cannot send via SMTP**
4. Save the mailbox's full email address (e.g. `rmills@mifeco.com`) — use it everywhere below
5. If you don't know the password, click Manage → Edit and set a new one in the DreamHost panel

## Subject Line Identifier Rule

ALL outbound emails MUST include one of these identifiers in the subject:

| Identifier | Product Line | Example Subject |
|-----------|-------------|----------------|
| `[SaaS]` | Project Hypatia Pro, PM Accelerator, VibraEngineer | `[SaaS] Your PM Accelerator demo is ready` |
| `[Books]` | No Blue Sky series, standalone titles | `[Books] New release: Built from Dust` |
| `[Consulting]` | $199 Strategy Session, Custom Assessment | `[Consulting] Your AI Strategy Assessment` |

**The identifier MUST be in square brackets** at the start of the subject line for reliable parsing.

If no identifier is provided, the MIFECO Mailer plugin auto-prepends the pipeline identifier from the request data.

## Reply Routing

When a recipient replies to an email, the `Reply-To` header routes the response back to rmills@mifeco.com (the one fully-hosted mailbox, which also forwards to your Gmail). The pipeline orchestrator (or a mail filter) parses the original subject's identifier word to route the reply:

- Reply to email with `[SaaS]` in subject → routes to SaaS pipeline lead record
- Reply to email with `[Books]` in subject → routes to Books pipeline lead record
- Reply to email with `[Consulting]` in subject → routes to Consulting pipeline lead record

## MIFECO Mailer WordPress Plugin

### Installation

The plugin file is at: `~/.hermes/skills/email/dreamhost-email-pipeline/references/mifeco-mailer.php` (v1.0.1, from_email = `rmills@mifeco.com`)

1. Zip the plugin file:
   ```bash
   mkdir -p /tmp/mifeco-mailer && cp "$(skill_view --path dreamhost-email-pipeline --file references/mifeco-mailer.php)" /tmp/mifeco-mailer/mifeco-mailer.php
   cd /tmp/mifeco-mailer && zip /tmp/mifeco-mailer.zip mifeco-mailer.php
   ```
2. Go to WordPress Admin → Plugins → Add New → Upload Plugin → select the ZIP → Activate
3. The REST endpoint becomes available at: `https://www.mifeco.com/index.php?rest_route=/mifeco/v1/send-email`

> **Note:** There's also an existing **MIFECO Pipeline Setup** plugin (for forms/pipeline setup) already active. The MIFECO Mailer plugin is a separate plugin that provides only the REST email-sending endpoint. Both can coexist — but make sure the pipeline-setup plugin does NOT have a duplicate `send-email` endpoint. Check for `mifeco_handle_send_email` in `mifeco-pipeline-setup.php` and remove it if present.

### API Endpoint

**POST** `https://mifeco.com/index.php?rest_route=/mifeco/v1/send-email`

**Request body:**
```json
{
  "secret": "JY2pcWpfu1*JeubsVBpm",
  "email": {
    "to": "recipient@example.com",
    "subject": "AD: [SaaS] Your demo link inside",
    "body": "Hi there,\n\nHere is your demo link...",
    "pipeline": "SaaS"
  }
}
```

**Response:**
```json
{
  "success": true,
  "to": "recipient@example.com",
  "subject": "[SaaS] Your demo link inside",
  "pipeline": "SaaS",
  "message": "Email sent successfully"
}
```

### Authentication

The endpoint requires a `secret` parameter matching `JY2pcWpfu1*JeubsVBpm`. This prevents unauthorized use.

### Unsubscribe Endpoint

**POST** `https://mifeco.com/index.php?rest_route=/mifeco/v1/unsubscribe`

```json
{
  "email": "user@example.com"
}
```

```json
{
  "success": true,
  "message": "You have been unsubscribed. You will no longer receive emails from MIFECO."
}
```

This endpoint is public (no secret required) and adds the email to the suppression list at `wp-content/mifeco-suppression-list.txt`. **Note:** The actual unsubscribe URL must use the `index.php?rest_route=` format since nginx intercepts `/wp-json/`. The plugin code should generate: `https://mifeco.com/index.php?rest_route=/mifeco/v1/unsubscribe`

### Suppression Check Endpoint

**POST** `https://mifeco.com/index.php?rest_route=/mifeco/v1/suppress`

```json
{
  "secret": "JY2pcWpfu1*JeubsVBpm",
  "email": "user@example.com"
}
```

```json
{
  "success": true,
  "email": "user@example.com",
  "suppressed": true
}
```

## CAN-SPAM Compliance

All outbound emails sent through this pipeline include:

- **Physical postal address**: `147 Bathclub Cir, N. Redington Beach, FL 33708` — appended to every email body
- **Unsubscribe link**: `https://mifeco.com/index.php?rest_route=/mifeco/v1/unsubscribe` — included in every email footer
- **List-Unsubscribe header**: Set on all outbound emails for one-click unsubscribe in Gmail/Outlook
- **AD: prefix**: Prepended to all commercial/sales pipeline subjects (SaaS, Consulting)
- **[MIFECO] subject tag**: All outbound subjects prefixed for shared-account identification
- **Abuse contact**: `MIFECOinc@gmail.com` — recipients reply with "ABUSE" in the subject line
- **Suppression list**: The `send-email` endpoint checks `wp-content/mifeco-suppression-list.txt` before sending. Suppressed addresses receive a 403 response.

### Email Footer Format

Every outbound email body is appended with:

```
---
MIFECO — 147 Bathclub Cir, N. Redington Beach, FL 33708
To unsubscribe: https://mifeco.com/unsubscribe
For abuse/violation reports, reply to MIFECOinc@gmail.com with the word "ABUSE" in the subject line.
```

## Outreach Dashboard Integration

The outreach dashboard (`dashboard/outreach-dashboard.html`) integrates with the DreamHost SMTP pipeline:

1. **🧪 Test mode** (default): Calls `POST /api/advance-lead` → writes email to `data/mock-inbox.json` + advances lead stage 1→2 in the pipeline JSON
2. **🚀 Production mode**: Calls `POST /api/advance-lead` → POSTs to `https://mifeco.com/wp-json/mifeco/v1/send-email` + advances lead stage 1→2

The API at `scripts/pipeline_data_api.py` handles both modes. The mode toggle in the dashboard calls `setMode('test'|'production')` which persists to localStorage and switches between mock inbox writing and real SMTP sending.

### WordPress Admin Embed

The outreach dashboard is also embedded in the WordPress admin via the **MIFECO Outreach Dashboard** plugin. Once installed and activated, it registers a "📤 Outreach" menu item in the WP admin sidebar at `admin.php?page=mifeco-outreach`. The plugin file:

```
/home/dh_mwpxuu/mifeco.com/wp-content/plugins/mifeco-outreach/mifeco-outreach-admin.php
```

It's an iframe embed pointing to `https://192.168.1.77:5543/outreach-dashboard.html`.

## Accessing WordPress Admin (via DreamHost SSO)

Direct login at `mifeco.com/wp-login.php` typically **fails** because the site uses DreamHost SSO. Use this path instead:

1. Log into **DreamHost Panel** at `https://panel.dreamhost.com` (email + password — NOT Google SSO)
2. Navigate to **Websites → Manage Websites** (sidebar)
3. Click on **mifeco.com** → **Dashboard**
4. Click the **"Log in to WordPress"** button — this SSO-authenticates you into the admin
5. You'll land at `mifeco.com/wp-admin/` already logged in as `mifeco_6eexpm`

**Troubleshooting:** If the DreamHost panel shows an empty page (React SPA), the page has loaded — check `document.body.innerText` for sidebar content. The new DreamHost panel is a React SPA and may not render fully in headless browser snapshots.

## WP Mail SMTP Configuration

The WP Mail SMTP plugin must be configured with DreamHost SMTP. Use the fully-hosted mailbox discovered above (NOT `info@mifeco.com` unless that IS your mailbox).

| Setting | Value |
|---------|-------|
| Mailer | Other SMTP |
| From Email | MIFECOinc@gmail.com (the shared Gmail account — DO NOT CHANGE) |
| From Name | MIFECO |
| **Force From Email** | **ON** — critical! Overrides any From header set by plugins/themes |
| SMTP Host | smtp.gmail.com |
| SMTP Port | 587 |
| Encryption | STARTTLS |
| Auto TLS | ON |
| Authentication | ON |
| SMTP Username | MIFECOinc@gmail.com |
| SMTP Password | Rm2214ri# (same for all apps — do NOT change) |

**To configure:**
1. Go to WordPress Admin → Settings → WP Mail SMTP
2. Select "Other SMTP" as the mailer
3. Fill in the Gmail SMTP settings above
4. **Enable "Force From Email"** so WP Mail SMTP overrides any plugin-set From address
5. Save Settings
6. Send a test email via the REST endpoint to verify

> **Note:** `MIFECOinc@gmail.com` is the ONLY email account — shared across all MIFECO applications. Password is `Rm2214ri#`. Do NOT change it without coordinating all app owners. All outbound subjects are tagged with `[MIFECO]`.

## Troubleshooting Failed Test Emails

If the REST endpoint returns `{"success":false,"message":"Failed to send email"}`, follow this **isolation ladder** — each step bypasses more layers to pinpoint the failure.

### Step 0 — Check for Password Propagation Delay

If you just changed the mailbox password on DreamHost, **it takes 2-15 minutes to propagate**. During this window:
- Neither the old nor new password may work
- The WP Mail SMTP test will return "SMTP Error: Could not authenticate"
- This does NOT mean the config is wrong — just wait and retry

Test from WP Mail SMTP → Tools → Email Test tab. If authentication fails but you're confident the password is correct, wait 5 minutes and try again before proceeding to deeper troubleshooting steps.

### Step 1 — Direct SMTP Auth Test (bypass WordPress entirely)

Before debugging WP Mail SMTP, verify credentials directly against the SMTP server. This tells you immediately if the password is valid.

**For Port 465 (SSL):**
```python
import smtplib
server = smtplib.SMTP_SSL('smtp.dreamhost.com', 465, timeout=15)
server.login('rmills@mifeco.com', 'your-password-here')
server.quit()
print('SUCCESS: credentials work!')
```

**For Port 587 (STARTTLS):**
```python
import smtplib
server = smtplib.SMTP('smtp.dreamhost.com', 587, timeout=15)
server.starttls()
server.login('rmills@mifeco.com', 'your-password-here')
server.quit()
print('SUCCESS: credentials work!')
```

**Interpreting results:**
- **SUCCESS** — credentials are valid; the problem is in WP Mail SMTP config (port, encryption, Auto TLS)
- **535 Error: authentication failed** — the password is wrong; go to Step 2
- **Connection unexpectedly closed / The read operation timed out** — DreamHost may be rate-limiting your IP after too many failed auth attempts. Wait 30-60 seconds, then try again with the correct credentials only.
- **Connection refused / timeout on first attempt** — port or firewall issue; try the other port (465 vs 587)

### Step 2 — Verify & Reset the Mailbox Password on DreamHost Panel

If direct auth fails, the password stored in WP Mail SMTP doesn't match what DreamHost has. Common causes:

- **"Pick a new password" generated a new one** — DreamHost's password generator overwrites whatever you typed; the old password stops working immediately
- **Password was changed manually but propagation hasn't happened** — DreamHost says *"a few minutes for this change to take effect"*
- **The password was set by someone else** (previous session, another admin, DreamHost auto-generated)

**To find the current working password on DreamHost Panel:**

1. Log into DreamHost Panel at `https://panel.dreamhost.com` (email+password, NOT Google SSO)
2. Navigate to **Mail → Manage Email**
3. Find your Fully Hosted mailbox (e.g. `rmills@mifeco.com`)
4. Click **Manage** — this opens the mailbox settings page at `#/manage/{mailbox}/{domain}/settings`

⚠️ **DreamHost Panel is a React SPA — direct `input.value` changes are silently ignored!** Setting `pwField.value = 'newpass'` in the console won't persist because React manages its own state. You must trigger native events:

```javascript
// THIS WORKS (triggers React's onChange):
var nativeSetter = Object.getOwnPropertyDescriptor(
  window.HTMLInputElement.prototype, 'value'
).set;
nativeSetter.call(pwField, 'newpassword');
pwField.dispatchEvent(new Event('input', { bubbles: true }));
```

**Or better: use the LEGACY Manage Email form (recommended):**
1. Click the **"Use legacy Manage Email page"** link at the top of the Manage Email page
2. Find your mailbox and click **Edit** (not Manage — Edit leads to the legacy form)
3. In the legacy form (URL: `?tree=mail.addresses&next_step=Edit`):
   - Uncheck **"Pick a new password for me"** (if auto-checked)
   - Type the password in both **New Password** (`#password1`) and **New Password Again** (`#password2`) fields
   - Click the submit button
4. The legacy form confirms: *"Successfully edited {mailbox}!"*
5. Wait **a few minutes** for propagation before testing

**🚨 Password change propagation behavior:**
- The old password stops working almost immediately after save
- The new password takes **"a few minutes"** (2-15 min) to propagate across DreamHost's SMTP auth servers
- During propagation, **neither password may work** — this is normal
- "Pick a new password for me" generates a new password immediately; there is NO overlap period — the old password is invalidated right away
- If you're testing with Python's smtplib and get a **timeout** after a failed auth attempt, DreamHost may be rate-limiting. Wait 10-15 seconds between retries. Don't blast multiple passwords in rapid sequence.

⚠️ **Important:** If you're running a credential test with Python's smtplib and it **times out** after a failed attempt, DreamHost may be rate-limiting. Wait 10-15 seconds between retries. Don't blast multiple passwords in rapid sequence.

### Step 3 — Check WP Mail SMTP Config

If Step 1 passes (credentials work directly) but WordPress still fails, the issue is in WP Mail SMTP:

1. **Auto TLS conflict** — When using **Port 465 with SSL**, Auto TLS must be **OFF**. When using **Port 587 with STARTTLS**, Auto TLS must be **ON**. Having the wrong combination causes silent failures.
2. **Wait, isn't Port 465 with SSL right?** — DreamHost's own help page (in the panel under Mail → Manage Email) recommends **Port 587 with STARTTLS/TLS**. Both work, but Port 587+STARTTLS is the documented/default configuration.
3. **Password field disabled** — WP Mail SMTP's password field (`#wp-mail-smtp-setting-smtp-pass`) is **disabled** when a password is stored. You must enable it via JS before setting a new value:
   ```javascript
   document.querySelector('#wp-mail-smtp-setting-smtp-pass').disabled = false;
   document.querySelector('#wp-mail-smtp-setting-smtp-pass').value = 'new-password';
   ```
4. **Force From Email must be ON** — WP Mail SMTP must override any `From` header set by plugins (the MIFECO Mailer plugin hardcodes an address). Enable this in the General settings.

**⚠️ WP Mail SMTP React Save Pitfall:** The Save Settings button uses a React-powered handler that reads values from React state, not the DOM. If you change the password field via `element.value = '...'` and click Save, the React state may not pick up the change — it silently saves the old password. Workarounds:
- **Option A (most reliable):** Use `wp-cli` (see Step 3.5 below) to write the option directly to the database
- **Option B:** Use the `wp_mail_smtp` option filter in a must-use plugin: `add_filter('option_wp_mail_smtp', function($v) { $v['smtp']['pass'] = 'newpass'; return $v; });`
- **Option C:** After setting the field value, use `React` devtools or dispatch an `input` event: `pw.dispatchEvent(new Event('input', {bubbles:true}))` before clicking Save

### Step 3.5 — Diagnose & Fix via wp-cli (Reliable Fallback)

If the browser-based save (Step 3) appears to work but the endpoint still fails, the password may not have persisted. The React/AJAX save can silently drop changes. Use wp-cli for a reliable fix.

**A) Get the actual SMTP error message:**

Write a debug script and run it on the DreamHost server via SSH:

```php
<?php
require_once '/home/dh_mwpxuu/mifeco.com/wp-load.php';
add_action('wp_mail_failed', function($error) {
    file_put_contents('/tmp/wp-mail-error.log', print_r($error, true));
});
global $phpmailer;
$r = wp_mail('test@example.com', '[SaaS] Debug', '<p>Test</p>', ['Content-Type: text/html; charset=UTF-8']);
echo 'RESULT: ' . ($r ? 'TRUE' : 'FALSE') . "\n";
if (isset($phpmailer) && is_object($phpmailer)) {
    echo 'ErrorInfo: ' . $phpmailer->ErrorInfo . "\n";
}
```

Upload via SCP and run with wp-cli:
```bash
scp /tmp/test-debug.php dh_mwpxuu@IAD1-SHARED-B8-42.DREAMHOST.COM:/tmp/
ssh dh_mwpxuu@IAD1-SHARED-B8-42.DREAMHOST.COM
cd /home/dh_mwpxuu/mifeco.com
/usr/bin/wp eval-file /tmp/test-debug.php
```

Key error messages to look for:
- `"SMTP Error: Could not authenticate"` → wrong password stored in WP Mail SMTP option
- `"SMTP Error: Data not accepted"` → message content issue
- `"Connection timed out"` → port/firewall issue (check 587 vs 465)

**B) Fix the password directly via wp-cli (most reliable method):**

```bash
ssh dh_mwpxuu@IAD1-SHARED-B8-42.DREAMHOST.COM
cd /home/dh_mwpxuu/mifeco.com
/usr/bin/wp eval '
$opts = get_option("wp_mail_smtp");
$opts["smtp"]["pass"] = "actual-password-here";
update_option("wp_mail_smtp", $opts);
echo "Password updated\n";
'
```

This bypasses the WP Mail SMTP React form entirely and writes directly to the `wp_options` table. WP Mail SMTP's encryption wrapper will encrypt the password on next save, but plaintext works immediately.

**C) Verify the fix:**

```bash
/usr/bin/wp eval '
$r = wp_mail("you@gmail.com", "[SaaS] wp-cli Test", "<p>Working now.</p>", ["Content-Type: text/html; charset=UTF-8"]);
echo $r ? "OK" : "FAIL";
'
```

If OK, the REST endpoint will now work too:
```bash
curl -X POST https://www.mifeco.com/index.php?rest_route=/mifeco/v1/send-email \
  -H "Content-Type: application/json" \
  -d '{"secret":"JY2pcWpfu1*JeubsVBpm","email":{"to":"you@gmail.com","subject":"AD: [SaaS] Final Confirmation","body":"<p>Pipeline works.</p>","pipeline":"SaaS"}}'
```

## SSH/SFTP Deployment

### ✅ SSH Available (Verified 2026-06-05)

SSH **is** working on DreamHost shared hosting (`IAD1-SHARED-B8-42.DREAMHOST.COM`) as of June 2026. Earlier reports of "connection refused" appear to have been temporary or resolved. Use paramiko for reliable scripted deployment.

**Use paramiko** (not pexpect) for reliable SSH/SFTP:

```python
import paramiko

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('IAD1-SHARED-B8-42.DREAMHOST.COM', username='dh_mwpxuu', password=pw, timeout=15)

# Execute commands
stdin, stdout, stderr = client.exec_command("cd /home/dh_mwpxuu/mifeco.com && wp plugin list --allow-root", timeout=15)
out = stdout.read().decode('utf-8', errors='replace')

# File transfer
sftp = client.open_sftp()
sftp.put(local_path, remote_path)   # upload
sftp.get(remote_path, local_path)   # download
sftp.close()
client.close()
```

**Why paramiko over pexpect**: More reliable for complex multi-step SSH sessions. No PTY issues. Works in headless execution.

**Avoid**: `sshpass` (not installed on agent), `pexpect` (buffer/timeout issues with DreamHost shell), browser-based file upload (unreliable for non-trivial files).

**NEVER use `--delete`** with rsync to the web root — the SPA and WordPress coexist. Target subdirectories only.

**Admin password**: `Rm2214ri####` (same as SSH password). Web root: `/home/dh_mwpxuu/mifeco.com/`.

1. **SMTP Username wrong** — The username must be the FULL email address of the actual fully-hosted mailbox (e.g. `rmills@mifeco.com`). Forward-only accounts cannot authenticate.

2. **Plugin code uses wrong From** — The MIFECO Mailer plugin may hardcode `info@mifeco.com`. Fix by:
   - **Option A:** Enable WP Mail SMTP's **Force From Email** (no code change needed — WP Mail SMTP overrides any From header set by plugins)
   - **Option B (more robust):** Patch the plugin file directly via SSH:
     ```bash
     ssh dh_mwpxuu@IAD1-SHARED-B8-42.DREAMHOST.COM
     sed -i 's/info@mifeco.com/MIFECOinc@gmail.com/g' \
       /home/dh_mwpxuu/mifeco.com/wp-content/plugins/PLUGIN_DIR/PLUGIN_FILE.php
     ```
     This replaces all hardcoded `info@mifeco.com` references with the actual fully-hosted mailbox. Run the REST endpoint test afterward to confirm.

3. **Plugin editor fails** — WordPress may revert changes with "Unable to communicate back with site to check for fatal errors". This is a loopback check. Either:
   - Disable the check temporarily (add `define('WP_DISABLE_FATAL_ERROR_HANDLER', true);` to wp-config.php)
   - Upload the file via SFTP/DreamHost file manager instead
   - Use a standalone mailer plugin (upload via Plugins → Add New → Upload Plugin)

4. **DNS/SPF issues** — If authentication passes but delivery fails, check SPF records include `include:_spf.google.com` (for Gmail SMTP). Also verify DKIM is set up in Google Workspace.

## Cron Email Queueing

The pipeline orchestrator reports what *needs* sending in the daily report. No emails are sent automatically — each requires explicit human approval via the content command center Approve & Send button.

## Email Headers for Reply Parsing and CAN-SPAM

Every outbound email includes custom headers for automated reply routing and compliance:

```
X-MIFECO-Pipeline: SaaS|Books|Consulting
X-MIFECO-Identifier: [SaaS]|[Books]|[Consulting]
List-Unsubscribe: <https://mifeco.com/wp-json/mifeco/v1/unsubscribe>, <mailto:MIFECOinc@gmail.com?subject=Unsubscribe+recipient@example.com>
List-Unsubscribe-Post: List-Unsubscribe=One-Click
```

The `List-Unsubscribe` header enables one-click unsubscribe in Gmail, Outlook, and other major providers. The `List-Unsubscribe-Post` header enables RFC 8058 one-click unsubscribe.

---

> **See also:** `references/books-mifeco-welcome-email-pipeline.md` — the standalone Python welcome email system for books.mifeco.com, a separate pipeline from this WordPress-based one. Uses Himalaya CLI with a 4-email sequenced series (immediate / day 2 / day 5 / day 8), JSON state file, and CSV subscriber storage.
