---
name: "mifeco-wordpress-management"
title: "MIFECO WordPress via DreamHost"
description: "Complete guide for managing the mifeco.com WordPress site through DreamHost hosting, including SSO login, form management, page creation, plugin management, navigation, and Ecwid store. For email/SMTP configuration, see references/gmail-shared-account.md."
---


## 🔍 MemPalace Query (MANDATORY FIRST STEP)
Before proceeding, query MemPalace for existing context:
```python
import sys, os; sys.path.insert(0, os.path.expanduser('~/.hermes/mempalace'))
import embed; embed.init_embedding(os.path.expanduser('~/.hermes/mempalace'))
results = embed.search_embeddings("MIFECO WordPress management DreamHost", k=5)
```
This retrieves previous decisions, domain-specific context, and lessons learned from the vector memory store.

# MIFECO WordPress Management via DreamHost

## Critical Architecture Notes

### nginx, NOT Apache
**DreamHost shared hosting runs nginx as the front-end web server.** There is NO Apache, no `mod_rewrite`, and `.htaccess` files are **completely ignored**.

- The web server is **nginx** (confirmed: `/etc/nginx/nginx.conf` active, no Apache processes)
- `.htaccess` rewrite rules have **NEVER worked** on this server
- DreamHost manages routing at the nginx vhost level, not via user-configurable configs
- Custom nginx configs cannot be added (`/etc/nginx/conf.d/` is not writable by users)

### SPA + WordPress Coexistence

mifeco.com serves both a Vite/React SPA and WordPress from the same web root. A **PHP-based router in the root `index.php`** handles the split:

```php
// /home/dh_mwpxuu/mifeco.com/index.php — Smart SPA + WP Router
// WordPress paths → load WordPress
// Everything else → readfile('index.html') (SPA)
```

WordPress paths routed to WP:
- `/wp-json/*`
- `/wp-admin/*`
- `/wp-login.php`
- `/wp-signup.php`
- `/xmlrpc.php`
- `/wp-content/*`
- `/wp-includes/*`
- `/index.php` itself

**REST API URL patterns that work:**
- `https://www.mifeco.com/index.php/wp-json/` — WP REST JSON discovery (HTTP 200)
- `https://www.mifeco.com/index.php?rest_route=/mifeco/v1/send-email` — MIFECO endpoints
- `/wp-json/` (without `index.php`) returns the SPA — nginx `try_files` serves it before PHP runs

### Landing Page (NOT WordPress)
- Vite/React SPA at site root
- Built via `npm run build` → `dist/` output uploaded
- See "Vite React SPA Lifecycle" section below for build/deploy

The WordPress backend handles:
- **Forms** (WPForms: Consulting ID:8, Books ID:9, SaaS ID:10)
- **Blog posts**
- **Ecwid store** (book products)
- **WP Mail SMTP** (email sending)
- **User management**

## Quick Reference
- **Site:** mifeco.com
- **WordPress Admin:** mifeco.com/wp-admin (SSO only — direct login fails)
- **DreamHost Panel:** panel.dreamhost.com
- **Theme:** Extendable (block theme / Full Site Editing)
- **WP Version:** 6.9.4
- **Credentials:** Stored in `~/.hermes/secrets/mifeco-dreamhost.env`
- **⚠️ Shared Email (CRITICAL):** MIFECOinc@gmail.com / Rm2214ri#### is the ONLY email account. Shared across ALL apps. DO NOT change password. See `references/gmail-shared-account.md` for full config.
- **SFTP User (mifeco.com):** `dh_mwpxuu` / `Rm2214ri####`
- **Panel login:** `rmills@mifeco.com` / `Rm2214ri####` (or `MIFECOinc@gmail.com`)
- **SFTP User (stage):** `robertstar`
- **Web Root:** `/home/dh_mwpxuu/mifeco.com/`
- **Ecwid Store ID:** `135660253`
- **Pipeline Engine:** `/home/dob/.hermes/.openclaw/workspace/pipeline-engine/`

## Login Procedure

### 1. DreamHost Panel
Navigate to panel.dreamhost.com → enter email + password from .env → handle privacy dialog → navigate to Websites → Manage Websites

### 2. SSO into WordPress (Two Methods)

**Method A — Direct (faster):**
After logging into DreamHost panel, navigate directly to `https://www.mifeco.com/wp-admin/`. The SSO session cookie is already set and auto-authenticates you.

**Method B — Through Panel:**
On the DreamHost WordPress tab for mifeco.com, click the **"Manage"** button → triggers SSO redirect.

### 3. Sessions Expire Frequently
- DreamHost SSO lasts ~15-30 min
- Re-authenticate: DreamHost panel login → click "Log in to WordPress" button
- Direct navigation to `wp-admin/` after panel login does NOT auto-authenticate — must click the SSO button
- Do NOT try `bob` password on wp-login — it always fails

## DreamHost Panel Navigation (React SPA Caveats)
The DreamHost panel is a React SPA. The browser accessibility snapshot often returns empty. Use the **browser console with JavaScript expressions** to read content and find interactive elements:

```js
// Find all buttons/links
Array.from(document.querySelectorAll('a, button')).map(el => ({tag: el.tagName, text: el.textContent.trim(), href: el.href, cls: el.className}))

// Read page text
document.body.innerText.substring(0, 2000)

// Get current URL
window.location.href
```

## SFTP Access (Works on Port 22)

**SFTP works on DreamHost shared hosting** with the correct password (`Rm2214ri####`). SSH shell access does NOT work (port 22 SSH is refused), but SFTP file transfers work fine.

```python
import paramiko

transport = paramiko.Transport(("iad1-shared-b8-42.dreamhost.com", 22))
transport.connect(username="dh_mwpxuu", password="Rm2214ri####")
sftp = paramiko.SFTPClient.from_transport(transport)

# Upload files
sftp.put("/local/path/file.html", "/remote/path/file.html")

# Create directories
try:
    sftp.mkdir("/remote/path/newdir")
except:
    pass

sftp.close()
transport.close()
```
The `paramiko` library handles SSH/SFTP reliably in this environment. Use it over `pexpect` which can have PTY output corruption issues:

```python
import paramiko

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('IAD1-SHARED-B8-42.DREAMHOST.COM', username='dh_mwpxuu', password=pw, timeout=15)

# Execute commands
stdin, stdout, stderr = client.exec_command("cd /home/dh_mwpxuu/mifeco.com && [command]", timeout=15)
out = stdout.read().decode('utf-8', errors='replace')

# SFTP file transfer
sftp = client.open_sftp()
sftp.get(remote_path, local_path)  # download
sftp.put(local_path, remote_path)  # upload
sftp.close()

client.close()
```

## Deployment

For SFTP deployment code and Panel File Manager instructions, see the `php-admin-dashboard-deployment` skill's `references/dreamhost-deployment.md`.

## Plugin Management

### Upload Plugin via ZIP + SCP (Most Reliable)
```python
import paramiko, os

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('IAD1-SHARED-B8-42.DREAMHOST.COM', username='dh_mwpxuu', password=pw, timeout=15)

# Upload ZIP to /tmp
sftp = client.open_sftp()
sftp.put('/tmp/plugin.zip', '/tmp/plugin.zip')
sftp.close()

# Extract to plugins directory
stdin, stdout, stderr = client.exec_command(
    "cd /tmp && unzip -o plugin.zip -d /home/dh_mwpxuu/mifeco.com/wp-content/plugins/ 2>&1",
    timeout=15
)
out = stdout.read().decode('utf-8', errors='replace')
print(out)

client.close()
```

Then activate via WP-CLI:
```bash
cd /home/dh_mwpxuu/mifeco.com
php -r "require 'wp-load.php'; activate_plugin('plugin-dir/plugin-file.php');"
```

Or via PHP script:
```php
<?php
require_once '/home/dh_mwpxuu/mifeco.com/wp-load.php';
$result = activate_plugin('plugin-dir/plugin-file.php');
echo is_wp_error($result) ? 'Error: ' . $result->get_error_message() : 'OK';
```

### Upload Plugin via WP Admin (Browser)
1. Navigate to `mifeco.com/wp-admin/plugin-install.php?tab=upload`
2. Click the **"Upload Plugin"** toggle button (`.upload-view-toggle`)
3. The form is inside `.upload-plugin-wrap > .upload-plugin > form.wp-upload-form`
4. Action URL: `/wp-admin/update.php?action=upload-plugin`
5. Set the file input (`#pluginzip`) then click "Install Now"
6. After installation, click "Activate Plugin"

### Programmatic Upload via Browser Fetch (No File Picker)
```js
// Read zip as base64 in terminal first: cat ~/plugin.zip | base64 -w0
const base64Zip = `...`;
const byteChars = atob(base64Zip);
const byteArrays = [];
for (let offset = 0; offset < byteChars.length; offset += 512) {
  const slice = byteChars.slice(offset, offset + 512);
  const byteNumbers = new Array(slice.length);
  for (let i = 0; i < slice.length; i++) byteNumbers[i] = slice.charCodeAt(i);
  byteArrays.push(new Uint8Array(byteNumbers));
}
const blob = new Blob(byteArrays, {type: 'application/zip'});
const file = new File([blob], 'plugin.zip', {type: 'application/zip'});
const formData = new FormData();
formData.append('pluginzip', file);
formData.append('_wpnonce', document.querySelector('.upload-plugin-wrap input[name="_wpnonce"]').value);
formData.append('_wp_http_referer', '/wp-admin/plugin-install.php');
fetch('https://www.mifeco.com/wp-admin/update.php?action=upload-plugin', {
  method: 'POST', body: formData, credentials: 'include'
});
```

### Nonce Discovery
```js
Array.from(document.querySelectorAll('input[type="hidden"]'))
  .filter(i => i.name.includes('nonce'))
  .map(i => ({id: i.id, name: i.name, value: i.value}))
```

## Monsta FTP (DreamHost File Manager)

### Access
1. DreamHost Panel → SFTP Users & Files
2. Click **"File Manager"** button for `dh_mwpxuu`
3. Opens Monsta FTP web app at `us-east-files.dreamhost.com`

### URL Token
The File Manager URL contains a base64-encoded connection token:
```
https://us-east-files.dreamhost.com/#/c/SERVER_IP/USERNAME/BASE64_TOKEN
```
Decode to extract SFTP credentials:
```bash
echo 'BASE64_TOKEN' | base64 -d
# Returns: {"t":"sftp","c":{"v":0,"p":"PASSWORD","s":0,"m":"Password"}}
```

## Monsta FTP (DreamHost File Manager) — PRIMARY FALLBACK

When SSH/SFTP is unavailable (which is common on DreamHost shared hosting), use the DreamHost Panel's built-in file manager:

### Access
1. Log into `panel.dreamhost.com` (email + password from `.env`)
2. Navigate to **Users → SFTP Users & Files** (or **Websites → Manage → mifeco.com → File Manager**)
3. Click **"File Manager"** button for `dh_mwpxuu`
4. Opens Monsta FTP web app at `us-east-files.dreamhost.com`

### Deployment via File Manager
1. **Create deployment zip locally:**
   ```bash
   cd /path/to/source && zip -r /tmp/deploy.zip . --exclude "data/*" --exclude ".git/*"
   ```
2. **Upload via File Manager:**
   - Navigate to target directory (e.g., `/home/dh_mwpxuu/mifeco.com/`)
   - Click **Upload** → select the zip file
   - Wait for upload to complete
   - Select the zip → click **Extract**
   - Delete the zip after extraction

### For SPA Deployment (dist/ → web root)
1. Build: `cd mifeco-website && npm run build`
2. Zip: `cd dist && zip -r /tmp/spa-dist.zip .`
3. Upload to `/home/dh_mwpxuu/mifeco.com/` via File Manager
4. Extract in place (overwrites existing files)

### URL Token (Alternative Access)
The File Manager URL contains a base64-encoded connection token:
```
https://us-east-files.dreamhost.com/#/c/SERVER_IP/USERNAME/BASE64_TOKEN
```
Decode to extract SFTP credentials:
```bash
echo 'BASE64_TOKEN' | base64 -d
# Returns: {"t":"sftp","c":{"v":0,"p":"PASSWORD","s":0,"m":"Password"}}
```

## Common Tasks

### WPForms Form IDs
- **ID 8:** Consulting Inquiry (Name, Email, Message, Organization, Industry dropdown, Services checkboxes)
- **ID 9:** Books Inquiry (Name, Email, Organization, Books of Interest checkboxes, Quantity, Message)
- **ID 10:** SaaS Inquiry (Name, Email, Organization, Product Interest select, Message)

### Creating / Editing WPForms
- URL: `wp-admin/admin.php?page=wpforms-builder&form_id=N`
- **Phone is Pro-only** — use Single Line Text instead
- Save with Save button, verify by checking entries

### Navigation Menu (Header)
- Block theme: Appearance → Editor → Navigation
- Or: `wp-admin/site-editor.php?postType=wp_navigation`

### WordPress REST API Endpoints
Test endpoints using the `index.php?rest_route=` pattern (since `/wp-json/` doesn't work through nginx):
```bash
# Check WP REST API
curl -s 'https://www.mifeco.com/index.php/wp-json/' | python3 -m json.tool

# MIFECO send-email
curl -s -X POST 'https://www.mifeco.com/index.php?rest_route=/mifeco/v1/send-email' \
  -d 'secret=JY2pcWpfu1*JeubsVBpm&email[to]=test@example.com&email[subject]=[SaaS] Test&email[body]=Hello'

# MIFECO suppress check
curl -s -X POST 'https://www.mifeco.com/index.php?rest_route=/mifeco/v1/suppress' \
  -d 'secret=JY2pcWpfu1*JeubsVBpm&email=test@example.com'

# MIFECO unsubscribe
curl -s -X POST 'https://www.mifeco.com/index.php?rest_route=/mifeco/v1/unsubscribe' \
  -d 'email=test@example.com'
```

## Vite React SPA Lifecycle (Build & Deploy)

### Overview
The mifeco.com landing page is a standalone Vite React SPA hosted at the site root. Source on GitHub.

### 1. Clone
```bash
git clone https://github.com/Robertstar2000/mifeco_web.git
cd mifeco_web/mifeco-website/
```

Key source files:
```
mifeco-website/
├── src/
│   ├── App.jsx                          ← Main layout
│   ├── main.jsx
│   └── components/
│       ├── BookstoreSection.jsx
│       ├── SoftwareSection.jsx
│       ├── PricingSection.jsx
│       ├── IndustriesSection.jsx
│       ├── ConsultationBookingModal.jsx
│       └── ui/                          ← shadcn/ui components
├── public/
├── package.json
└── vite.config.js
```

### 2. Build
```bash
# Preferred: use npm to avoid pnpm approve-builds prompt
rm -rf node_modules pnpm-lock.yaml
npm install --legacy-peer-deps
npx vite build
```

### 3. Deploy
Build output goes to `dist/`. Upload to web root `/home/dh_mwpxuu/mifeco.com/` via rsync or SCP.

### 4. Troubleshooting
- **`npx vite build` hangs/returns empty in `terminal()`**: The terminal tool flags vite as a server process. Use `background=true` + `process(action='wait')`, or run inside `execute_code()` instead.
- **Site shows old version**: Hard refresh (Ctrl+Shift+R). Vite content-hashes filenames automatically.

## Ecwid Store Management

### Limits
- **Free plan: max 5 products.** 7 MIFECO books exceed this limit.

### Add Products via REST API
Store ID: `135660253`. Get SSO token from WP admin Ecwid iframe:
```js
const token = document.querySelector('iframe').src.match(/token=([^&]+)/)[1];
```

### Product Pages Created
- `/hypatia` — Project Hypatia Pro
- `/accelerator` — Project Management Accelerator
- `/vibraengineer` — VibraEngineer
- `/books` — Books Catalog

## Common Pitfalls

1. **nginx, not Apache** — `.htaccess` is completely ignored. Do NOT attempt to add rewrite rules to `.htaccess`. WordPress routing is handled by the PHP router in the root `index.php`.

2. **`/wp-json/` returns SPA** — This is expected on nginx. Use `/index.php?rest_route=` or `/index.php/wp-json/` as the REST API base URL.

3. **`/admin/` directory blocks WordPress admin proxy** — A real `admin/` directory exists on disk. nginx's `try_files` serves it directly, preventing WordPress plugins from intercepting `/admin` requests. The admin proxy plugin cannot work while this directory exists.

4. **Session timeout** — DreamHost SSO expires every 15-30 min. Check `window.location.href` to confirm WP admin.

5. **WPForms Lite limits** — no Phone field type, no Webhook, no REST API for forms

6. **Block theme** — navigation in Site Editor, not old Menu editor

7. **React SPA in DreamHost panel** — accessibility snapshot often returns empty; use browser console JS

8. **Ecwid shipping** — Omitting shipping field entirely works; `shipping: {type: 'SINGLE_ADDRESS'}` causes validation error

9. **Plugin editor fails** — WordPress may revert changes with "Unable to communicate back with site to check for fatal errors". Fix: add `define('WP_DISABLE_FATAL_ERROR_HANDLER', true);` to wp-config.php temporarily, or upload via SCP instead.

10. **No email sending** without human approval per individual email

11. **WPForms email notification** — Set under Settings → Notifications → "Send To Email Address". Free version supports one notification.

12. **WordPress SSO session validity** — Direct navigation to `wp-admin/` after panel login does NOT auto-authenticate. You must click the "Log in to WordPress" button.

14. **SSH shell unavailable, SFTP works** — DreamHost shared hosting refuses SSH shell connections (port 22 SSH = connection refused). But SFTP file transfers on port 22 work reliably with password `Rm2214ri####`. Use `paramiko.Transport` + `SFTPClient` for automated deployment. When all else fails, use the DreamHost Panel File Manager as fallback.

15. **Password format in saved files** — The actual SFTP/panel password is `Rm2214ri####` (with literal `####` suffix). This was confirmed by decoding the DreamHost file manager token. Always use this exact password for SFTP and panel login.

16. **Remove old/duplicate endpoints** — Always check `mifeco-pipeline-setup.php` for duplicate send-email endpoints that may conflict with the CAN-SPAM-compliant `mifeco-mailer.php` plugin. Look for hardcoded `rmills@mifeco.com` references and old secrets.

## Deployment Reference

For detailed step-by-step Panel File Manager deployment instructions, see:
`references/panel-file-manager-deployment.md`
