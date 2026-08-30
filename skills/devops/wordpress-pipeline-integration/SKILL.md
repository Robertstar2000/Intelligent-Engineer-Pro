---
name: wordpress-pipeline-integration
description: >-
  Connect a hosted WordPress site to an agent-managed sales pipeline —
  hosting panel navigation, SMTP email setup (Gmail shared account),
  webhook form integration, and replacing third-party email services.
  For email configuration details, see references/gmail-shared-account.md.
version: 1.0.0
author: Hermes Agent
license: MIT
tags:
  - wordpress
  - dreamhost
  - hosting
  - email
  - smtp
  - webhook
  - pipeline
  - lead-capture
related_skills:
  - sales-pipeline-infrastructure
  - website-audit-and-product-launch
  - himalaya
# Note: wordpress-pipeline-integration (hosting/WordPress side) and
# sales-pipeline-infrastructure (pipeline data/CRM side) are complementary,
# not duplicative. This skill covers panel→SSO→forms→webhook→email.
# The pipeline skill covers lead registry, nurture sequences, and cron orchestration.
triggers:
  - "User says their WordPress is hosted on a provider (DreamHost, WP Engine, SiteGround, etc.) and wants to connect it to the sales pipeline"
  - "Replace third-party email service (AgentMail, SendGrid) with domain-hosted SMTP (hermes@domain.com)"
  - "Create DreamHost email accounts and configure SMTP for Hermes Agent"
  - "Set up lead capture forms on WordPress that POST to the pipeline webhook"
  - "Navigate a DreamHost panel to find/manage WordPress, email, and database"
  - "Install WordPress via One-Click Install on DreamHost"
  - "Configure WP Mail SMTP plugin to route WordPress email through hosting SMTP"
  - "Migrate from static HTML intake forms to WordPress forms with webhook submission"
  - "Set up DNS records (SPF, DKIM, DMARC) for email deliverability from a custom domain"
  - "User provides hosting credentials (panel login, SFTP user) and wants infrastructure help"
  - "WordPress is already installed via DreamHost One-Click Install and you need admin access and a site survey"
  - "Access a DreamHost-installed WordPress site where the admin password is unknown — use SSO from the panel instead"
  - "Survey what DreamHost's One-Click Install pre-configured — theme, plugins, content"
  - "Create a WordPress admin user when only DreamHost SSO access is available and the panel password doesn't work for wp-login.php"
  - "Create WordPress pages, posts, or forms programmatically via REST API during an SSO browser session — when the visual builder is slow, inaccessible, or you need to bulk-create content"
  - "Bulk-create product landing pages on WordPress using cookie-based REST API auth (no FTP/SSH/application passwords needed)"
  - "Use the WordPress REST API with browser session cookies and the wpApiSettings nonce to create/update/delete content"
  - "Store DreamHost/hosting credentials in an env file and reference from memory for cross-session use"
  - "Configure WPForms Lite fields with dropdowns, checkboxes, and custom labels — working around Pro-only field restrictions"
  - "Add webhook POST code to WordPress theme functions.php to forward form submissions to a local/remote pipeline server"
  - "Directly navigate to https://{domain}/wp-admin/ from an active DreamHost panel session — the SSO auto-authenticates without needing to find the 'Log in to WordPress' button on the manage dashboard"
---


## Memory context (Hindsight)

Long-term memory context is now provided automatically by Hindsight (bank
`mifeco-default`) on every turn — the retired MemPalace manual query step no
longer applies. Do NOT attempt to import `~/.hermes/mempalace` (it was removed
2026-08-19).This retrieves previous decisions, domain-specific context, and lessons learned from the vector memory store.

# WordPress Pipeline Integration

## Overview

Connect a hosted WordPress site to an agent-managed sales pipeline. This covers:
- Hosting panel navigation (DreamHost-specific, but generalizable)
- WordPress installation and configuration
- Domain email setup (SMTP/IMAP)
- Pipeline integration (webhooks, forms, lead capture)
- DNS configuration for email deliverability

## Prerequisites

- **Hosting panel credentials** — email + password (or Google OAuth)
- **Domain** already pointed to the hosting provider
- **Hermes pipeline engine** already set up (`pipeline-engine/`)
- **Agent knowledge** of products/services for forms and pages

## DOX Integration

When working in a project that uses the [DOX (Self-documenting AGENTS.md)](https://github.com/agent0ai/dox) framework:

- **Read Before Editing:** Walk the DOX tree from root to the target path. Read every AGENTS.md along the route before making any changes.
- **Update After Editing:** If the change affects purpose, scope, ownership, structure, workflows, or operating rules, update the closest owning AGENTS.md and refresh the Child DOX Index.
- **Reference:** [agent0ai/dox](https://github.com/agent0ai/dox) — copy `AGENTS.md` from the repo root into your project to initialize.

## Step-by-Step Workflow

### STEP 1: Access the Hosting Panel

Log into the hosting provider's control panel:

```
URL: https://panel.dreamhost.com (DreamHost)
     https://my.wpengine.com   (WP Engine)
     https://account.sgcloud.net (SiteGround)
```

**DreamHost specific notes:**
- Panel login requires the **email address** tied to the account, not the SFTP username
- Google OAuth is available but browser automation may be blocked ("This browser or app may not be secure")
- Use email+password login instead of Google Sign-In when using browser-based access
- After login, navigate to specific sections via URL patterns:
  - `tree=domain.dashboard#/site/{domain}/dashboard` — site dashboard
  - `tree=domain.dashboard#/site/{domain}/wordpress` — WordPress management
  - `tree=wordpress.installer#/site/{domain}/flow` — One-Click Install
  - `tree=mail.workspace#` — Google Workspace (not free DreamHost Email)
  - `tree=users.dashboard#` — SFTP users
  - `tree=advanced.mysql` — MySQL databases

**⚠️ Privacy cookie dialog:** After a fresh login, a "Privacy" dialog appears asking to accept cookies. Click the "Close" button (not the "Accept" link — the outlined "Close" button) to dismiss it before navigating.

**⚠️ Session management:** DreamHost panel sessions time out after ~15-30 minutes. If navigating to a different tab causes a redirect to the login page, you need to re-enter credentials. Bookmark the target URL and navigate directly after logging in. The `browser_console` tool's `document.body.innerText` works to read page content even when the accessibility snapshot returns `Empty page` (DreamHost is a React SPA). Use `browser_console` with JS expressions to click elements when `browser_click` can't find refs.

**🔐 Credential storage convention:**
Store DreamHost panel credentials in `~/.hermes/secrets/{domain}-dreamhost.env` and reference the path in memory so future sessions can load them:
```
# ~/.hermes/secrets/mifeco-dreamhost.env
DREAMHOST_EMAIL=user@gmail.com
DREAMHOST_PASS=password
WP_ADMIN_USER=bob
WP_ADMIN_EMAIL=user@domain.com
```
Load via `source ~/.hermes/secrets/mifeco-dreamhost.env` before browser sessions.

### STEP 2: Find or Install WordPress

**Check the Domain for an Existing WordPress Installation:**

```
https://{domain}/wp-admin/         → Login page = WordPress is at root
https://{domain}/wordpress/wp-admin/ → WordPress in subdirectory
https://{domain}/wp-json/          → REST API response = WordPress confirmed
```

If `wp-admin` returns the site's theme (NOT a login page), the `.htaccess` may be intercepting WordPress routes. Check the hosting panel's site dashboard for a **"WordPress" tab** or **"Log in to WordPress"** button.

**Hosting-specific paths to check:**

| Host | Check Path |
|------|-----------|
| DreamHost | Dashboard → site → **WordPress tab** or manage page |
| WP Engine | Sites → {site} → **WP Admin** |
| SiteGround | WordPress → Install → {domain} |

**DreamHost WordPress management page:**
```
https://panel.dreamhost.com/index.cgi?tree=domain.dashboard#/site/{domain}/wordpress
```
Shows: WordPress version, PHP version, database name, database credentials, and management options.

---

### STEP 2A.5: Discover SFTP Users & File Paths

When the DreamHost panel's File Manager needs to be used (e.g., for uploading plugin files when the WP admin upload fails), find the correct SFTP user and navigate the Monsta FTP interface:

**Finding the right SFTP user:**
1. Go to **SFTP Users & Files** (`tree=users.dashboard#`) in the DreamHost panel
2. Look at the **"Username / Domain name"** column — each SFTP user shows the domain it belongs to
3. Example mapping: `dh_mwpxuu` → `mifeco.com`, `robertstar` → `stage.mifeco.com`
4. Click the **"File Manager"** button next to the correct user
5. This opens Monsta FTP — an embedded web-based file manager (HTML-only UI)

**Monsta FTP navigation:**
- **Breadcrumb path** appears at the top: `/home/{sftp_user}/{domain}/`
- **Directory entries** can be opened by:
  - Double-clicking the directory name text
  - Clicking the expand icon () on the directory, then clicking " Open"
- **Going back to the previous directory**: Use the "" (back) button in the toolbar
- **Uploading files**: The toolbar button **** (upload icon) opens the file upload dialog
- **Limitations**: Restricted SFTP users cannot navigate "up" past their home directory

**WordPress file structure (DreamHost One-Click Install):**
```
/home/{sftp_user}/{domain}/
├── .htaccess
├── index.php
├── wp-config.php
├── wp-admin/
├── wp-content/
│   ├── plugins/          ← Upload plugin .zips here
│   ├── themes/           ← Theme files including functions.php
│   │   └── {theme-name}/
│   │       └── functions.php
│   ├── uploads/
│   └── index.php
├── wp-includes/
└── ... (other WP root files)
```

**Monsta FTP toolbar reference (Unicode icons):**
| Icon | Action |
|------|--------|
|  | Back to previous directory |
|  | Forward |
|  | Refresh |
|  | View options |
|  | History (directory listing) |
|  | **Upload** — open file upload dialog |
|  | Download selected |
|  | Terminal (when available) |
|  | Edit selected file |
|  | Properties |
|  | Copy/Move |
|  | New folder |
|  | Delete |
|  | CHMOD permissions |
|  | Help/Info |

⚠️ **Monsta FTP sessions are tied to the DreamHost panel session** — if the panel times out (~15-30 min), the File Manager stops working. Re-authenticate and open a fresh File Manager.

### STEP 2A: WordPress Already Installed via DreamHost One-Click Install

**Before attempting a fresh install, check if DreamHost already installed WordPress.** DreamHost's One-Click Install often runs automatically or by previous admin action. When it has, you get:

**How to detect:**
1. Log into the DreamHost panel at `https://panel.dreamhost.com` (use email+password, not Google SSO, for automation)
2. Go to `tree=domain.dashboard#/site/{domain}/dashboard` — site dashboard
3. Look for a **"WordPress"** tab in the left sidebar under the domain
4. Look for a **"Log in to WordPress"** button in the site dashboard overview
5. Check notifications — "Success installing WordPress on your site!" confirms it

**SSO login from DreamHost panel (no password needed):**
- The **"Log in to WordPress"** button is an SSO link — it logs you directly into WordPress admin **without needing a password**
- This bypasses the normal `wp-login.php` page entirely
- The link auto-authenticates via the DreamHost Panel Login plugin
- After clicking, you land in WordPress admin at `/wp-admin/admin.php?page=extendify-auto-launch`

**Admin username format:**
DreamHost auto-generates the admin username as `{domain}_{random6chars}` (e.g., `mifeco_6eexpm`). The password is random and not shown in the panel — use SSO instead.

**🟢 Direct SSO shortcut (skip finding the button):**  
Instead of hunting for the "Log in to WordPress" button in the DreamHost panel's React UI (which often doesn't render in the accessibility snapshot), **navigate directly to `https://{domain}/wp-admin/`** after your DreamHost panel session is active. The SSO session cookie auto-authenticates you — the DreamHost Panel Login plugin intercepts the request and logs you in automatically. This works even when the "Log in to WordPress" button is hidden or hard to locate in the panel's React SPA.

**🟢 Create a proper admin user:**
Since the DreamHost panel password does NOT work for WordPress login (they use different credential systems), and the auto-generated admin has a hard-to-remember username, create a real admin user from the SSO session:

1. After SSO login, go to **Users → Add New** (`/wp-admin/user-new.php`)
2. Fill in: Username (e.g. `bob`), Email (e.g. `user@domain.com`), First/Last Name
3. Set a password you'll remember (can match the DreamHost panel password)
4. **Uncheck "Send User Notification"** — prevents confusion
5. Set **Role** to **Administrator**
6. Save — now you can log in directly at `wp-login.php` with this username + password
7. Optionally delete the auto-generated user or keep it for SSO access as backup

**⚠️ Note:** The DreamHost panel password (e.g. `Rm2214ri####`) does NOT work for WordPress `wp-login.php` authentication, even though it's the same account. WordPress and DreamHost panel use separate authentication systems. Only SSO bridges them.

**What DreamHost's One-Click Install pre-configures:**

| Component | Details |
|-----------|---------|
| **Theme** | **Extendable** (by Extendify) — a block theme designed for the Extendify AI onboarding assistant |
| **Content** | May have auto-migrated content from the old static/PHP site |
| **Plugins (active)** | All in One SEO, Ecwid Ecommerce, EWWW Image Optimizer, Extendify, Site Assistant, **WP Mail SMTP**, **WP Super Cache**, **WPForms Lite** |
| **Plugins (inactive)** | Akismet, Hello Dolly |
| **Pages** | Privacy Policy (default), Sample Page (default), Store (Ecwid) |
| **Site Title** | "Just another WordPress site" (default — change it) |

**Extendify Assist dashboard:** After SSO login, visit `admin.php?page=extendify-assist#dashboard` for a site guide with quick-action links:
- **"Add new page"** — opens the block editor for a new page
- **"Edit your homepage"** — opens the site editor
- **"Set up WPForms"** — may open the WPForms builder
- **"Set up All in One SEO"** — opens SEO configuration
- **"Edit a page with AI"** — AI-assisted page editing
- **"Upload a logo"** / **"Upload a site icon"** — branding setup
These can be quicker than navigating through the admin menu.

**🟢 Key advantage:** The plugins you'd normally install manually (WP Mail SMTP, WPForms, All in One SEO) are **already there and active**. You can jump straight to:
- Configuring WP Mail SMTP with domain email credentials (Step 5)
- Creating intake forms with WPForms (Step 7)
- Setting up SEO metadata (via All in One SEO)
- Building product pages

**After SSO login, survey the install:**
```javascript
// In browser console:
// Check admin user
document.querySelector('#wp-admin-bar-my-account .ab-item .display-name[1]')?.textContent;

// List active plugins
Array.from(document.querySelectorAll('.plugin-title strong')).map((el, i) => {
  let row = el.closest('tr');
  return (row?.classList.contains('active') ? '✅' : '⏸️') + ' ' + el.textContent.trim();
});

// List existing pages
Array.from(document.querySelectorAll('.wp-list-table .row-title')).map(el => el.textContent.trim());

// Check active theme
document.querySelector('.theme.active .theme-name')?.textContent?.trim();
```

**To install WordPress via DreamHost One-Click Install (for a fresh install):**

1. From the site dashboard, look for the **WordPress** section with a **"Get Started"** button
2. Clicking opens: `tree=wordpress.installer#/site/{domain}/flow`
3. Choose experience: **Custom Installation** (for full plugin control) or **Liftoff Website Builder** (AI-assisted)
4. Set **Site Purpose** — choose from: Local Business, Portfolio, Blog, E-Commerce, Other, None
5. Select **Recommended Plugins** — key ones for pipeline integration:
   - **WP Mail SMTP** (required for email deliverability)
   - **wpForms Lite** (form builder with webhook support)
   - **All in One SEO** (SEO metadata and sitemaps)
   - WP Super Cache (performance)
   - EWWW Image Optimizer (image optimization)
   - DreamHost Panel Login (SSO from panel — pre-selected)
6. Confirm admin email (receives WordPress credentials)
7. Click **Confirm Install**

**⚠️ Note:** The DreamHost panel is a React SPA. Simple DOM queries (`querySelector`, `textContent`) may not find elements rendered inside shadow DOM or async-loaded components. If browser clicks don't register, try:
- Using `browser_console` with JS to click elements
- Navigating directly to installer URLs
- Using the panel's direct URL patterns above

## SSH Password-Auth Deployment Fallback

When the browser-based plugin upload fails (file input unreachable, session timeout, password with masked `#` chars) and SFTP credentials don't work, **SSH with password auth via pexpect** is a reliable escape hatch.

**Prerequisites:**
- SSH server is running on the target (DreamHost, WP Engine, etc.)
- You have a working SSH username + password (may differ from FTP/SFTP password)
- `pexpect` is installed in the agent's Python environment

**Step-by-step:**

### 1. Discover if SSH works

```python
import pexpect
child = pexpect.spawn('ssh -o StrictHostKeyChecking=no dh_mwpxuu@mifeco.com "ls /home/dh_mwpxuu/mifeco.com/wp-content/plugins/"', timeout=10)
child.expect('password:')
child.sendline('Rm2214ri####')
child.expect(pexpect.EOF, timeout=10)
print(child.before.decode())
```

**If it connects:** The password works for SSH even when it doesn't for FTP/SFTP. This is common on DreamHost — the SSH password may use a different authentication backend.

### 2. Deploy PHP code via SSH

The safest approach is **base64-encode the PHP and pipe it through echo + base64 -d** to avoid shell escaping issues with heredocs:

```python
import pexpect, base64

php_code = '''<?php
// Your plugin code here
'''

encoded = base64.b64encode(php_code.encode()).decode()
cmd = f'echo {encoded} | base64 -d >> /home/dh_mwpxuu/mifeco.com/wp-content/plugins/existing-plugin/existing-plugin.php'

child = pexpect.spawn(f'ssh -o StrictHostKeyChecking=no dh_mwpxuu@mifeco.com "{cmd}"', timeout=15)
child.expect('password:')
child.sendline('Rm2214ri####')
child.expect(pexpect.EOF, timeout=15)
```

**Why base64?** PHP code contains `$`, `{`, `}`, quotes, and other shell-sensitive chars. Base64 encoding avoids all escaping issues. The target file must already exist — use `>>` to append, or `>` to overwrite.

### 3. Append to an existing plugin (not create a new file)

WordPress requires plugins to have a proper directory structure. Rather than creating a new plugin directory via SSH (which requires `mkdir`), **append your code to an existing plugin** that's already installed and active:

```bash
# Append REST endpoint to existing MIFECO setup plugin
echo {base64_encoded_code} | base64 -d >> /home/dh_mwpxuu/wp-content/plugins/mifeco-pipeline-setup/mifeco-pipeline-setup.php
```

The appended code will be executed as part of the existing plugin on the next request. This works for adding REST API endpoints, webhooks, and custom post types.

### 4. Verify PHP syntax

Always verify the resulting file has no syntax errors:

```python
child = pexpect.spawn('ssh -o StrictHostKeyChecking=no dh_mwpxuu@mifeco.com "php -l /path/to/plugin.php"', timeout=10)
child.expect('password:')
child.sendline('Rm2214ri####')
child.expect(pexpect.EOF, timeout=10)
result = child.before.decode()
# Should contain: "No syntax errors detected"
```

### 5. Test the deployed endpoint

After deploying a REST API endpoint, verify it works from the agent:

```bash
curl -s -X POST "https://domain.com/wp-json/mifeco/v1/send-email" \
  -H "Content-Type: application/json" \
  -d '{"secret":"your-secret","email":{"to":"test@example.com","subject":"[SaaS] Test","body":"<p>test</p>","pipeline":"SaaS"}}'
```

### Pitfalls

| Pitfall | Why It Happens | How to Avoid |
|---------|---------------|--------------|
| **pexpect times out on long commands** | `cat >> file` with heredoc awaits stdin indefinitely | Use base64 encoding with `echo | base64 -d >>` — single command, no interactive input |
| **PHP syntax errors after append** | Escaped chars in the PHP code got mangled during transmission | Always run `php -l` on the remote file after deployment |
| **`#` in password breaks shell** | `#` starts a shell comment in bash | Passwords with `#` still work when passed via `sendline()` — pexpect sends it as literal text over the SSH channel |
| **Plugin not recognized by WordPress** | New plugin directory created via SSH but missing `index.php` | Append to an EXISTING active plugin instead of creating a new one. The existing plugin's header comments register it with WordPress; your code runs as part of it. |
| **WordPress REST endpoint returns 404** | Permalinks need a flush after adding a new route | Visit any WordPress admin page (or `wp-admin/options-permalink.php`) once to trigger permalink flush, or append `flush_rewrite_rules()` call |

Create email accounts at your domain using the hosting provider's email management:

**DreamHost DreamHost (free email):**
DreamHost's shared hosting plans include free email hosting, but it may need to be enabled. If "Mail" in the sidebar only shows Google Workspace, the free DreamHost Email may need to be activated:
- Navigate to **Mail** → look for **"Add Email"** or "Manage Email" options
- Or check: `https://panel.dreamhost.com/index.cgi?tree=mail.dreamhost`

**Standard email accounts to create:**

| Email | Purpose |
|-------|---------|
| `hermes@{domain}` | **Primary** — pipeline automation sending |
| `books@{domain}` | Book inquiries (forward to hermes@) |
| `saas@{domain}` | SaaS inquiries (forward to hermes@) |
| `{user}@{domain}` | Personal inbox |

**SMTP Configuration (standard):**

```
SMTP Host: smtp.{hosting-provider}.com
SMTP Port: 587 (STARTTLS) or 465 (SSL/TLS)
SMTP Auth: Full email address + password
IMAP Host: imap.{hosting-provider}.com
IMAP Port: 993 (SSL)
```

**DreamHost SMTP:** `smtp.dreamhost.com:587` — uses full email address as username.

### STEP 4: Configure Hermes Email

Update `~/.hermes/.env` with the SMTP credentials:

```
EMAIL_ADDRESS=hermes@{domain}
EMAIL_PASSWORD=[generated password]
EMAIL_IMAP_HOST=imap.{hosting-provider}.com
EMAIL_IMAP_PORT=993
EMAIL_SMTP_HOST=smtp.{hosting-provider}.com
EMAIL_SMTP_PORT=587
EMAIL_POLL_INTERVAL=15
EMAIL_ALLOWED_USERS={user}@{domain}
EMAIL_HOME_ADDRESS={user}@{domain}
```

**⚠️ CRITICAL:** Remember the no-auto-email rule — never send emails without explicit human approval for each individual email.

### STEP 5: Configure WP Mail SMTP Plugin

In the WordPress admin, configure the **WP Mail SMTP** plugin:

⚠️ **The ONLY email account is MIFECOinc@gmail.com (Gmail). This is shared across ALL applications. DO NOT change the password (`Rm2214ri#`) without coordinating all app owners.**

1. Go to **Settings → WP Mail SMTP**
2. Mailer: **Other SMTP**
3. SMTP Host: `smtp.gmail.com`
4. Encryption: **TLS** (port 587)
5. Authentication: **On**
6. Username: `MIFECOinc@gmail.com`
7. Password: `Rm2214ri#`
8. From Email: `MIFECOinc@gmail.com`
9. From Name: `MIFECO`
10. **Force From Email: ON** — critical, overrides any plugin-set From address

**If Gmail 2FA is enabled:** Create an App Password at https://myaccount.google.com/apppasswords and use that instead of `Rm2214ri#` for SMTP.

**Note:** The old DreamHost SMTP (`smtp.dreamhost.com` with `rmills@mifeco.com`) is no longer used. `rmills@mifeco.com` is a forward-only alias and cannot send email.

SPF record must include `_spf.google.com` (not `dreamhost.com`):

```txt
@ TXT "v=spf1 include:_spf.google.com ~all"
```

### STEP 6: DNS Hardening for Email Deliverability

Configure these DNS records at your domain registrar (or DreamHost's DNS panel):

**SPF Record** (authorizes DreamHost to send on your behalf):
```
TXT   @   "v=spf1 mx include:dreamhost.com ~all"
```

**DKIM Signing** (enable in hosting panel):
- DreamHost: Mail → Manage Email → DKIM → Enable
- Adds a TXT record automatically

**DMARC Policy** (receives reports on spoofing attempts):
```
TXT   _dmarc   "v=DMARC1; p=none; rua=mailto:dmarc@{domain}"
```
Start with `p=none` to monitor. Move to `p=quarantine` or `p=reject` after verifying all email sources are authenticated.

### STEP 7: Create Lead Intake Forms (WordPress → Pipeline)

Replace static HTML forms with WordPress-based forms that POST to the pipeline webhook.

**Option A — WPForms Lite (via the builder UI):**

**⚠️ WPForms Lite limitations:**
- **Phone field is Pro-only** — use Single Line Text labeled "Phone" instead
- **Address, Map, Date/Time, File Upload, Signature** — all Pro-only
- **Webhook integration** — not available in Lite; must add via `functions.php` or custom plugin
- **Available standard fields:** Single Line Text, Paragraph Text, Dropdown, Multiple Choice, Checkboxes, Numbers, Name, Email, Number Slider, CAPTCHA, Website/URL, Password, Hidden Field, Section Divider, HTML, Content, Rich Text

**Configuring dropdown/checkbox options efficiently:**  
The WPForms builder's visual field editor is a React SPA and can be slow to automate via browser clicks. For adding many options:

1. Click on the field in the form preview to select it  
2. In the field options panel, click **"Bulk Add"** (next to the Choices heading)  
3. Type all options — **one per line** — in the textarea  
4. Click **"Add New Choices"** to append them  
   ⚠️ **Bulk Add APPENDS, it does NOT replace** — existing placeholder defaults ("First Choice", "Second Choice", "Third Choice") remain  
5. Delete any placeholder defaults by clicking the **second link icon (trash)** next to each in the choices list  
6. ⚠️ **Label reset bug:** The field's Label textbox can get overridden by the first choice text after a Bulk Add operation. After adding choices, click back on the field and verify the label is still correct — re-type it if it was replaced

**Adding fields to an existing form via AJAX (faster than the builder UI):**
```javascript
// Requires being on the WPForms builder page (in the browser session)
let nonce = wpforms_builder?.nonce;

// Available field types: text, textarea, select, checkbox, number, name, email, url, password, hidden, html, divider, custom_captcha, rating, likert, net_promoter
fetch('/wp-admin/admin-ajax.php', {
  method: 'POST', credentials: 'same-origin',
  headers: {'Content-Type': 'application/x-www-form-urlencoded'},
  body: new URLSearchParams({
    action: 'wpforms_new_field_' + formId,
    field: JSON.stringify({type: 'name', label: 'Name', required: '1', format: 'first-last'}),
    _wpnonce: nonce
  })
}).then(r => r.json());
// But the WPForms AJAX API may not expose all field creation; the builder UI is more reliable for complex fields
```

**Adding webhook to WPForms Lite via custom PHP:**
Since WPForms Lite has no native webhook, add PHP to the active theme's `functions.php` or a custom plugin:

```php
add_action('wpforms_process_complete', 'mifeco_pipeline_webhook', 10, 4);
function mifeco_pipeline_webhook($fields, $entry, $form_data, $entry_id) {
    $form_name = $form_data['settings']['form_title'] ?? '';
    $pipeline = 'unknown';
    if (stripos($form_name, 'Consulting') !== false) $pipeline = 'consulting';
    elseif (stripos($form_name, 'Book') !== false) $pipeline = 'books';
    elseif (stripos($form_name, 'SaaS') !== false) $pipeline = 'saas';

    $data = [
        'pipeline' => $pipeline,
        'form_name' => $form_name,
        'entry_id' => $entry_id,
        'fields' => [],
        'timestamp' => current_time('mysql'),
    ];
    foreach ($fields as $field) {
        $data['fields'][] = ['name' => $field['name'] ?? '', 'value' => $field['value'] ?? ''];
    }

    $webhook_url = 'http://localhost:8080/api/webhook/wpforms';
    $response = wp_remote_post($webhook_url, [
        'headers' => ['Content-Type' => 'application/json'],
        'body' => json_encode($data),
        'timeout' => 15,
    ]);
    if (is_wp_error($response)) {
        error_log('MIFECO Webhook Error: ' . $response->get_error_message());
    }
}
```

**⚠️ Editing functions.php via the Theme File Editor in the browser:**  
The built-in theme editor (`/wp-admin/theme-editor.php?file=functions.php&theme={theme}`) can be used to add code, but saving via JavaScript textarea manipulation is unreliable (the `Update File` button click may not trigger the actual AJAX save, and the textarea's `value` set via console often reverts on save). Instead:  
1. Navigate to the theme editor page directly  
2. Click on `functions.php` in the file list sidebar (left panel)  
3. Scroll to the bottom of the textarea  
4. **Manually type** the PHP code at the end (before the closing `?>` if it exists)  
5. Click the **"Update File"** submit button — wait for the green success notice  
6. Verify by checking that a `document.querySelector('.notice-success')` appears, OR check `document.getElementById('newcontent')?.value?.length` increased  
7. **Saving via browser console:** If manually typing is impractical, set the textarea value AND use `document.querySelector('input[type="submit"]').click()` — a generic `input[type="submit"]` selector is more reliable than `[value="Update File"]`  
8. **Verify save persisted:** After clicking submit and the page reloads, check `document.getElementById('newcontent')?.value?.length`. If the length equals the original value, the save was lost — the page reloaded from server without persisting changes  
9. If it doesn't save, try selecting a different file and switching back, or use the custom plugin zip approach (below) instead — this is more reliable than the theme editor

**⚠️ Browser console limitation on WordPress admin pages:**  
The accessibility snapshot often shows only the admin sidebar nav, omitting the main content area entirely. Use `browser_console` with `document.getElementById('wpbody-content')?.innerText` to read page content, and `document.getElementById('newcontent')` for the theme editor textarea. Single-expression console queries work best — multi-line statements often return `null`. Simple checks like `document.getElementById('newcontent')?.value?.length` confirm whether textarea manipulation persisted.
1. Go to **WPForms → Add New**
2. Name the form and select a template (e.g., "Simple Contact Form")
3. Click **"Use Template"** — this creates the form and opens the builder
4. Add/remove fields from the left panel (drag or click)
5. Configure **Settings → Notifications** → send to `{user}@{domain}`
6. Configure **Settings → Confirmations** → thank-you message
7. Click **Save** then **Embed** to add to a page

**⚠️ WPForms builder automation caveat:** The builder is a JS-heavy React SPA. If browser clicks on template buttons time out or fail:
- Try clicking via JS: `document.querySelector('a.wpforms-template-use[data-template="simple-contact-form-template"]')?.click()`
- The button triggers `wpforms_builder.nonce` for the AJAX `wpforms_new_form` action — use it directly:
  ```javascript
  fetch(ajaxurl, { method: 'POST', credentials: 'same-origin',
    headers: {'Content-Type': 'application/x-www-form-urlencoded'},
    body: new URLSearchParams({
      action: 'wpforms_new_form',
      form_name: 'My Form Name',
      template: 'simple-contact-form-template',
      _wpnonce: wpforms_builder.nonce  // available in builder JS context
    })
  }).then(r => r.json()).then(d => console.log('Form ID:', d.data?.form_id));
  ```
- Once created, forms can be found at their ID: `admin.php?page=wpforms-builder&form_id={ID}`

**Option B — WPForms Lite (via custom plugin — recommended for automation):**  
When you need to create multiple forms (e.g., Consulting, Books, SaaS intake) or add webhook/REST API integration, a **standalone setup plugin** is the most reliable approach — it works when the theme editor save fails and doesn't require SFTP access.

**Creating the setup plugin locally (on the Hermes machine):**  
Use `execute_code` with Python's `zipfile` to create a plugin zip:

```python
import zipfile, tempfile, os, shutil

plugin_code = '''<?php
/**
 * Plugin Name: My Pipeline Setup
 * Description: One-time setup — creates forms, adds webhook.
 * Version: 1.0
 */

// Setup: triggered by visiting ?my_setup=1 as admin
add_action('init', function() {
    if (!isset($_GET['my_setup']) || !current_user_can('manage_options')) return;
    
    if (function_exists('wpforms')) {
        // Fix existing form — remove placeholder choices from dropdown/checkbox fields
        $form = wpforms()->form->get(8);  // change ID
        if ($form) {
            $data = wpforms_decode($form->post_content);
            if (isset($data['fields'][6]['choices'])) {  // field 6 = dropdown
                $keep = ['Healthcare', 'Technology / SaaS', 'Finance'];
                $cleaned = [];
                foreach ($data['fields'][6]['choices'] as $c) {
                    if (in_array($c['label'], $keep)) $cleaned[] = $c;
                }
                $data['fields'][6]['choices'] = $cleaned;
            }
            wpforms()->form->update(8, ['post_content' => wpforms_encode($data)]);
        }
        
        // Create new forms programmatically (auto-assigns IDs)
        wpforms()->form->add([
            'fields' => [
                1 => ['id' => '1', 'type' => 'name', 'label' => 'Name', 'format' => 'first-last', 'required' => '1'],
                2 => ['id' => '2', 'type' => 'email', 'label' => 'Email', 'required' => '1'],
                3 => ['id' => '3', 'type' => 'text', 'label' => 'Organization'],
                4 => ['id' => '4', 'type' => 'select', 'label' => 'Interest', 'choices' => [
                    ['label' => 'Option 1'], ['label' => 'Option 2'],
                ]],
            ],
            'settings' => ['form_title' => 'My New Form', 'submit_text' => 'Submit'],
        ]);
    }
    
    echo '<pre>Setup complete</pre>';
    exit;
});

// Webhook: POST WPForms entries to pipeline-engine
add_action('wpforms_process_complete', 'my_pipeline_webhook', 10, 4);
function my_pipeline_webhook($fields, $entry, $form_data, $entry_id) {
    $data = ['form_name' => $form_data['settings']['form_title'] ?? '', 'fields' => []];
    foreach ($fields as $f) $data['fields'][] = ['name' => $f['name'] ?? '', 'value' => $f['value'] ?? ''];
    wp_remote_post('http://localhost:8080/api/webhook/wpforms', [
        'headers' => ['Content-Type' => 'application/json'],
        'body' => json_encode($data), 'timeout' => 15,
    ]);
}
'''

tmpdir = tempfile.mkdtemp()
plugindir = os.path.join(tmpdir, 'my-setup')
os.makedirs(plugindir)
with open(os.path.join(plugindir, 'my-setup.php'), 'w') as f:
    f.write(plugin_code)
zip_path = os.path.expanduser('~/my-setup.zip')
with zipfile.ZipFile(zip_path, 'w') as z:
    z.write(os.path.join(plugindir, 'my-setup.php'), 'my-setup/my-setup.php')
shutil.rmtree(tmpdir)
print(f"Plugin zip: {zip_path}")
```

Then upload via **Plugins → Add New → Upload Plugin** in the WordPress admin. Activate the plugin, visit `https://mifeco.com/?my_setup=1` (as admin), then deactivate and delete the plugin.

**⚠️ Plugin upload via browser automation:**  
The file input (`<input type="file" id="pluginzip">`) on the upload page (`/wp-admin/plugin-install.php?tab=upload`) cannot be programmatically set from JavaScript due to browser security. You must either:
- Use `browser_type` on the file input ref found in the accessibility snapshot
- Navigate to the upload form, locate the file input, and manually select the zip through the native file picker — note that the `#pluginzip` input exists even when the upload form is hidden; the `.upload-view-toggle` link must be clicked first to show the form
- Or upload via SFTP/DreamHost File Manager as a fallback (see Step 2A.5 for Monsta FTP navigation)

**Plugin upload browser flow:**
1. Navigate to `/wp-admin/plugin-install.php?tab=upload`
2. Click the **"Upload Plugin"** toggle — this is the `.upload-view-toggle` link (a `page-title-action` class button that reads "Upload PluginBrowse Plugins")
3. This reveals the upload form with the file input (`#pluginzip`) and the "Install Now" button
4. The nonce for the upload is available at `document.getElementById('_wpnonce')?.value` on the page
5. After selecting the file and clicking "Install Now", you land on the plugin activation page — click **"Activate Plugin"**

After uploading and activating, visit the setup URL to trigger the one-time form creation/fix.

**Legacy approach (mu-plugin via SFTP):**

```php
<?php
/**
 * Plugin Name: MIFECO Forms & Pipeline
 * Description: Creates intake forms + REST API endpoint for pipeline polling
 */
if (!defined('ABSPATH')) exit;

// Create forms on activation
register_activation_hook(__FILE__, function() {
    if (!function_exists('wpforms')) return;
    wpforms()->form->add('Consulting Inquiry', [ /* form config */ ]);
});

// REST API endpoint for pipeline to poll new entries
add_action('rest_api_init', function() {
    register_rest_route('mifeco/v1', '/entries', [
        'methods' => 'GET',
        'callback' => function() {
            global $wpdb;
            $form_ids = array_filter([get_option('mifeco_form_consulting')]);
            if (empty($form_ids)) return ['entries' => []];
            $placeholders = implode(',', array_fill(0, count($form_ids), '%d'));
            $results = $wpdb->get_results($wpdb->prepare(
                "SELECT e.entry_id, e.form_id, e.fields, e.date, f.form_title
                 FROM {$wpdb->prefix}wpforms_entries e
                 JOIN {$wpdb->prefix}wpforms_forms f ON e.form_id = f.form_id
                 WHERE e.form_id IN ($placeholders) AND e.viewed = 0
                 ORDER BY e.date DESC", $form_ids));
            // ... parse and return entries
        },
        'permission_callback' => function() { /* API key check */ },
    ]);
});
```

Install via WP admin plugin upload (zip) or by placing the PHP file directly in `wp-content/mu-plugins/` via SFTP.

**Option C — Fluent Forms (if installed):**
1. Create form with Fluent Forms
2. Enable **Webhook Integration** under Marketing Integrations
3. Set webhook URL to: `https://{hermes-webhook-endpoint}/webhook/{pipeline}`
4. Map form fields to JSON payload

**Option D — Custom PHP snippet (in theme functions.php or custom plugin):**
```php
// Add to theme's functions.php or a custom plugin
add_action('wpcf7_mail_sent', function($contact_form) {
    $submission = WPCF7_Submission::get_instance();
    $data = $submission->get_posted_data();
    
    // POST to pipeline webhook
    wp_remote_post('https://{webhook-url}/webhook/{pipeline}', [
        'headers' => ['Content-Type' => 'application/json', 'X-Webhook-Secret' => '{secret}'],
        'body' => json_encode([
            'name' => $data['your-name'],
            'email' => $data['your-email'],
            'company' => $data['company'],
            'interest' => $data['interest'],
            'message' => $data['message'],
            'source' => 'wordpress-form',
            'timestamp' => current_time('c')
        ])
    ]);
});
```

### STEP 8: Set Up Pipeline Webhook Receiver

Create a lightweight webhook server in `pipeline-engine/webhook-server/`:

```
pipeline-engine/webhook-server/
├── server.py               ← Flask/FastAPI HTTP server
├── handlers/
│   ├── saas.py             ← Validates + appends to pipeline-saas.json
│   ├── consulting.py       ← Validates + appends to pipeline-consulting.json
│   └── books.py            ← Validates + appends to pipeline-books.json
├── auth.py                 ← Shared secret verification
└── requirements.txt
```

**Endpoints:**

| Endpoint | Method | Auth | Pipeline Target |
|----------|--------|------|-----------------|
| `/webhook/saas` | POST | Bearer token | `pipeline-saas.json` |
| `/webhook/consulting` | POST | Bearer token | `pipeline-consulting.json` |
| `/webhook/books` | POST | Bearer token | `pipeline-books.json` |
| `/webhook/health` | GET | None | Health check |

**Handler logic** (same for all pipelines):
1. Verify shared secret in `X-Webhook-Secret` header
2. Validate JSON payload against expected schema
3. Generate lead ID, timestamp, initial stage
4. Run `dedup-check.py` against the lead registry
5. Append lead to the appropriate pipeline JSON
6. Update the lead registry
7. Return 201 Created with lead ID

**Deployment:**
- Run as a background process: `python3 server.py &`
- Or deploy as a small service (Fly.io, Railway, etc.)
- Configure `cronjob action=create` to keep the webhook server alive

### STEP 9: Build WordPress Product Pages

Create product landing pages on WordPress for the pipeline products.

**For each product, create a WordPress page with:**
- Hero section (headline, subhead, CTA)
- Features overview (grid layout)
- Pricing table
- Embedded intake form
- FAQ section

Use the content from `website-audit-and-product-launch` skill for landing page copy and design patterns.

#### Option A — Visual Block Editor

1. Go to **Pages → Add New**
2. Add blocks using the block editor (heading, paragraph, buttons, columns)
3. Set featured image, slug, and SEO metadata
4. Publish

#### Option B — WordPress REST API (Recommended for automation / bulk creation)

When you're authenticated via DreamHost SSO (or any browser session), you can create pages programmatically using the WordPress REST API with cookie-based auth. This avoids the slow visual editor and is ideal for creating multiple product pages.

**Prerequisites:** You're already logged into `wp-admin` via the browser session.

**How it works:**

The browser session cookie authenticates REST API requests automatically. You also need the `X-WP-Nonce` header from the `wpApiSettings` JavaScript global (available on every admin page):

```javascript
// Available in the browser console of any WP admin page
let nonce = wpApiSettings.nonce;
```

**Create a page:**
```javascript
fetch('/wp-json/wp/v2/pages', {
  method: 'POST',
  credentials: 'same-origin',
  headers: {'Content-Type': 'application/json', 'X-WP-Nonce': wpApiSettings.nonce},
  body: JSON.stringify({
    title: 'Product Name',
    slug: 'product-name',
    content: '<!-- wp:heading --><h2>Headline</h2><!-- /wp:heading -->',
    status: 'publish'
  })
}).then(r => r.json()).then(d => console.log('Created:', d.id, d.link));
```

**Delete a page (e.g., duplicate):**
```javascript
fetch('/wp-json/wp/v2/pages/{ID}', {
  method: 'DELETE',
  credentials: 'same-origin',
  headers: {'X-WP-Nonce': wpApiSettings.nonce}
}).then(r => r.json()).then(d => console.log('Deleted:', d.deleted));
```

**Key notes:**
- `credentials: 'same-origin'` attaches the browser session cookies — no API key or application password needed
- The `X-WP-Nonce` header prevents CSRF — get it from `wpApiSettings.nonce` on any admin page
- Content uses **HTML block markup** (`<!-- wp:... -->`) — use standard WordPress blocks or raw HTML
- You can create multiple pages in parallel with `Promise.all()`
- Batch-create product pages for SaaS offerings, books, consulting tiers, etc.

**Verify created pages:**
Navigate to **Pages → All Pages** (`/wp-admin/edit.php?post_type=page`) and check the list:
```javascript
Array.from(document.querySelectorAll('.wp-list-table .row-title'))
  .map(el => el.textContent.trim());
```

**Alternative: Create via REST API with WPForms (for forms):**
If you need to create WPForms as well, use the WPForms AJAX endpoint with its own nonce:
```javascript
// Get nonce from the builder context
let nonce = wpforms_builder.nonce;  // available when on wpforms-builder page

fetch('/wp-admin/admin-ajax.php', {
  method: 'POST',
  credentials: 'same-origin',
  headers: {'Content-Type': 'application/x-www-form-urlencoded'},
  body: new URLSearchParams({
    action: 'wpforms_new_form',
    form_name: 'My Form Name',
    template: 'simple-contact-form-template',
    _wpnonce: nonce
  })
}).then(r => r.json()).then(d => console.log('Form created:', d.data?.form_id));
```

### STEP 10: Replace AgentMail with SMTP

Once SMTP is verified working, update the pipeline to use SMTP instead of AgentMail:

1. Update `pipeline-engine/data/pipeline-*.json` — replace `email_address` fields
2. Update `.env` — remove AgentMail API key references
3. Update intake forms — change POST targets from AgentMail API to WordPress forms
4. Test sending one nurture sequence email via SMTP

**Progressive cutover:**
1. Keep AgentMail active alongside new SMTP
2. Send 1 test email via SMTP, verify delivery
3. Move Books pipeline to SMTP first (lowest volume)
4. Move SaaS pipeline
5. Move Consulting pipeline
6. Decommission AgentMail

### STEP 11: Redirect Cloud Run Marketing Pages

Once WordPress product pages are live, add redirects from old Cloud Run URLs:

```htaccess
# .htaccess in web root
Redirect 301 /hypatia https://{domain}/hypatia
Redirect 301 /accelerator https://{domain}/accelerator
Redirect 301 /vibraengineer https://{domain}/vibraengineer
```

## Pitfalls

| Pitfall | Why It Happens | How to Avoid |
|---------|---------------|--------------|
| **DreamHost One-Click Install options don't respond to clicks** | The panel is a React SPA with async-loaded elements; simple DOM click events may not trigger | Try multiple approaches: (1) clicking child elements, (2) `browser_console` JS click, (3) navigating directly via URL patterns, (4) manual keyboard navigation (Tab + Enter) |
| **WordPress wp-login.php returns 404 instead of login form** | The root site's `.htaccess` or routing may intercept WordPress paths; or WordPress is installed at root but routing is misconfigured | Check `wp-admin/` (not `wp-login.php`), look for a "Log in to WordPress" button in the hosting panel, or check `wp-json/` for REST API response |
| **Session expires in hosting panel** | DreamHost panel sessions time out during complex navigation | Keep sessions short; log in, navigate directly to the target page, make the change, then log results. Don't idle. |
| **Google OAuth blocks browser automation** | Google flags automated browser sign-ins as "insecure" | Use email+password login for the hosting panel instead of Google Sign-In |
| **WordPress admin password unknown** | The One-Click Install creates a random password sent via email; or you're accessing an existing install with unknown credentials | **Primary: Use DreamHost SSO** — click "Log in to WordPress" on the site dashboard (panel.dreamhost.com). This bypasses passwords entirely. Only fall back to "Lost your password?" reset if SSO is unavailable. |
| **DreamHost panel password doesn't work for WordPress** | DreamHost Panel and WordPress use separate authentication systems — the same password string authenticates different credential stores | Use SSO only. Create a separate WordPress admin user via Users → Add New after SSO login. Do NOT try to brute-force or reset the WordPress password — it's tied to the auto-generated username, not your email. |
| **No MX records on DreamHost email** | DreamHost shared hosting includes email but may need activation | Check DreamHost panel under Mail → Manage Email. If only Google Workspace is shown, the free email tier may need to be enabled via the "Add Product" section |
| **SPF too strict** | Using `-all` (hard fail) before all email sources are authenticated | Start with `~all` (soft fail), move to `-all` only after verifying all legitimate email sources are in the SPF record |
| **AgentMail references still in pipeline** | The pipeline skill was built around AgentMail; SMTP migration requires updating multiple files | Search all files for `agentmail.to` references: `.env`, `pipeline-*.json`, intake forms, `sales-pipeline-infrastructure` skill |
| **Using smtp.dreamhost.com instead of smtp.gmail.com** | Old config used DreamHost SMTP with rmills@mifeco.com (forward-only alias). All sending must go through smtp.gmail.com with MIFECOinc@gmail.com | Update WP Mail SMTP to smtp.gmail.com:587 with MIFECOinc@gmail.com. Force From Email = ON. See references/gmail-shared-account.md |
| **Missing [MIFECO] subject tag** | All outbound email through the shared MIFECOinc@gmail.com account must be tagged so replies can be identified and routed | Pipeline send_via_wordpress() applies [MIFECO] prefix. WordPress mifeco-mailer.php also applies it. Do not remove. See references/gmail-shared-account.md |
| **Wrong abuse contact in footer** | Old footer referenced abuse@rmills.com (non-functional). Must use MIFECOinc@gmail.com with "ABUSE" subject instruction | Footer now reads: "For abuse/violation reports, reply to MIFECOinc@gmail.com with the word ABUSE in the subject line." See references/gmail-shared-account.md |
