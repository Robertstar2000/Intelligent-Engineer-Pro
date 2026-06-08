---
name: mifeco-website-deployment
title: MIFECO Website Deployment
description: Access instructions for DreamHost panel and deploying updates to mifeco.com and books.mifeco.com
category: devops
triggers: ["dreamhost", "mifeco deploy", "website update", "deploy books", "panel.dreamhost", "blank page", "white screen", "site not loading", "spa not rendering"]
---

# MemPalace Query

Before using this skill, ALWAYS query MemPalace for relevant context:
```
# In Python:
import sys, os
sys.path.insert(0, os.path.expanduser('~/.hermes/mempalace'))
from retrieve import search
results = search("mifeco deployment dreamhost website images", k=5)
```
This retrieves previous deployment history, known issues, file paths, and credentials.

---

# MIFECO Website Deployment

> **IMPORTANT: The books website is at `mifeco.com/books`, NOT `books.mifeco.com`.** The `books.mifeco.com` subdomain is not configured as a separate hosting entry on DreamHost. All book content lives under `mifeco.com/books/` as a subdirectory of the main WordPress site.

## DreamHost Access

**Dashboard URL:** https://panel.dreamhost.com
**Login:** mifecoinc@gmail.com / panel password

**Server details:**
- Host: IAD1-SHARED-B8-42.DREAMHOST.COM
- SSH Username: dh_mwpxuu
- SSH Password: same as panel password
- **Books web root:** `/home/dh_mwpxuu/mifeco.com/books/` (NOT `books.mifeco.com/`)
- Main web root: `/home/dh_mwpxuu/mifeco.com/`
- WordPress SSO: Visit DreamHost panel, click Manage on mifeco.com → Log in to WordPress

## Subdirectory Deployment Pitfalls

**CRITICAL:** When deploying a PHP app to a subdirectory (e.g., `/consult/`), all internal links must include the subdirectory prefix. Links like `/register.php` resolve to the domain root, causing 404s. Always use `/consult/register.php` or similar.

**CRITICAL:** The variable `$survey['id']` must NEVER be referenced as `$_survey['id']` in `survey.php`. The `$_survey` variable doesn't exist — it returns null, which casts to 0. This causes `$surveyId = 0`, which means all `WHERE id = ?` queries affect 0 rows. The survey status never changes from `initial`, causing the gateway form to reappear after submission. **This is the #1 debugging priority when the survey gateway loops.**

**CRITICAL — SPA Blank Page #1:** The PHP router at `index.php` must NOT route the root path `/` to WordPress. When `rtrim($request_uri, '/')` produces `''` (empty string from root URL), do NOT set `$is_wp = true`. The condition `$request_uri === ''` is the #1 cause of the blank white page (WordPress loads with no content). See `references/spa-wordpress-router-fix.md`.

**CRITICAL — SPA Blank Page #2:** After modifying the minified JS bundle (`assets/index-HASH.js`), always verify brace/paren balance. Unbalanced braces or parens prevent the bundle from parsing, producing a blank white page. See "React SPA Bundle Modification" below for the verification procedure.

See `references/dreamhost-subdirectory-pitfalls.md` for:
- Absolute path trap diagnosis and fix pattern
- `.htaccess` syntax (`Require all denied` causes 500; use `Order allow,deny`)
- PHP error logging disabled (use `file_put_contents('/tmp/debug.log', ...)`)
- cURL timeout differences (`CURLOPT_TIMEOUT` vs `CURLOPT_TIMEOUT_MS`)
- MySQL remote-only connection

See `references/dreamhost-subdirectory-pitfalls.md` for:
- Absolute path trap diagnosis and fix pattern
- `.htaccess` syntax (`Require all denied` causes 500; use `Order allow,deny`)
- PHP error logging disabled (use `file_put_contents('/tmp/debug.log', ...)`)
- cURL timeout differences (`CURLOPT_TIMEOUT` vs `CURLOPT_TIMEOUT_MS`)
- MySQL remote-only connection

## Local Website Source

All website files are at:
```
/mnt/usb_4tb/books/Cindy_Lou_Legal_Capers/books-mifeco-website/
```

### Server Structure (books.mifeco.com → actually mifeco.com/books/):
```
/home/dh_mwpxuu/mifeco.com/books/
├── index.html               # Main books landing page
├── router.php               # Smart router (serves static files)
├── privacy.html
├── age-of-lightships/index.html
├── cindy-lou/index.html
├── lunar-foundation/index.html
├── no-blue-sky/index.html
├── images/                  # All book covers, infographics, favicon (19 files)
│   ├── retainer-to-trouble-cover.jpg
│   ├── age-of-lightships-cover.jpg
│   ├── infographic-business.png
│   ├── author-photo.jpg     # Bob J Mills author photo
│   └── ... (19 total)
├── css/style.css
├── js/main.js
├── api/subscribe.php
├── magnets/                 # Free reader magnet downloads
└── data/subscribers.csv
```

## Deploying Updates

### SFTP via pexpect (Recommended)

The `sshpass` utility is not available. Use pexpect for password-based SFTP:

```python
import pexpect, sys

password = "your-password"
local_file = "/path/to/local/file.php"
user_host = "dh_mwpxuu@mifeco.com"

child = pexpect.spawn(f'sftp -o StrictHostKeyChecking=no {user_host}', timeout=30, encoding='utf-8')
child.logfile_read = sys.stdout

idx = child.expect(['password:', pexpect.EOF, pexpect.TIMEOUT], timeout=15)
if idx != 0:
    raise Exception("Failed to get password prompt")

child.sendline(password)
idx = child.expect(['sftp>', 'Permission denied', pexpect.EOF, pexpect.TIMEOUT], timeout=15)
if idx != 0:
    raise Exception("Authentication failed")

child.sendline('cd /home/dh_mwpxuu/mifeco.com/consult')
child.expect('sftp>', timeout=10)

child.sendline(f'put {local_file} pay.php')
child.expect('sftp>', timeout=30)

# Verify upload
child.sendline('ls -la pay.php')
child.expect('sftp>', timeout=10)

child.sendline('bye')
child.close()
```

**Notes:**
- `pexpect` is pre-installed on this system (`python3-pexpect` package)
- `sshpass` is NOT available — use pexpect instead
- SFTP exit code 1 after `bye` is normal — verify with `ls -la` before closing
- For bulk uploads: put all files in a loop, or tar/extract over SSH

### PHP File Writing — $ Sign Stripping

**CRITICAL:** pexpect's `sendline()` strips `$` signs from PHP code. Variables like `$uri` become `uri`.

**Solutions (in order of reliability):**
1. **Write file locally, SCP it** — most reliable
2. **Use base64 encoding** — encode locally, decode on server
3. **Never use heredoc or triple-quoted strings** through pexpect for PHP files

## DreamHost Panel Login

- SSH username (`dh_mwpxuu`) is NOT the panel email — always ask user for panel email
- After entering credentials, re-snapshot to get fresh element refs before typing
- `browser_type` fails with "Unknown ref" if refs are stale — navigate → snapshot → then type/click
- **User prefers panel access over SFTP when possible** — the browser tool may not be available; when it isn't, use SFTP/SSH as fallback and note the limitation

## React SPA Bundle Modification

When the main mifeco.com site (React/Vite SPA) needs link changes and the source isn't available:

1. **Find the current bundle:**
   - Get hash from HTML: `curl -s "https://www.mifeco.com/" | grep -oP 'src="/assets/index-[^\\"]+\\.js"'`
   - Download: `curl -s "https://www.mifeco.com/assets/index-HASH.js" -o /tmp/bundle.js`

2. **ALWAYS back up the original on DreamHost before modifying:**
   `rename index-HASH.js index-HASH.js.original`

3. **Check existing old bundles** in `/home/dh_mwpxuu/mifeco.com/assets/` for a backup. Old bundles accumulate there (hashes change per rebuild) — keep the most recent pre-modification one as a fallback.

4. **Use Python string replacements** — more reliable than sed for large files. Write a script to `/tmp/` and execute it.

5. **CRITICAL: Verify brace/paren balance after EVERY modification.** Minified JS bundles are sensitive — one unbalanced brace or paren destroys the entire page (white screen / blank page).
   ```python
   with open('bundle.js') as f:
       c = f.read()
   print("Braces: {}/{}".format(c.count('{'), c.count('}')))
   print("Parens: {}/{}".format(c.count('('), c.count(')')))
   ```
   Braces MUST be balanced (equal count). Parens may be off by 1 (last statement implicit semicolon) — never more.

6. **Key patterns to search for in the current bundle:**
   - Desktop nav Books link: `l.jsx("a",{href:"#bookstore",className:"text-gray-600 hover:text-blue-600 transition-colors",children:"Books"})`
   - Mobile nav Books link: `l.jsx("a",{href:"#bookstore",className:"block text-gray-600 hover:text-blue-600 transition-colors",children:"Books"})`
   - Hero CTAs: `children:"Consult with an Expert"`
   - Product cards: `className:"grid md:grid-cols-3 gap-8`
   - Footer links: `href:"/consult"` or `href:"/books"`

7. **Upload back** to `/home/dh_mwpxuu/mifeco.com/assets/` via SFTP

8. **Verify immediately:**
   - Download the live bundle again and grep for your changes
   - Check HTTP 200 and correct Content-Type: `curl -sI "https://www.mifeco.com/assets/index-HASH.js"`
   - Verify brace/paren balance on the LIVE bundle (curl → check counts)

9. Changes are lost if the React app is rebuilt — document what was changed in a reference file so it can be re-applied.

## Images Currently Deployed

All images are in `/mnt/usb_4tb/books/Cindy_Lou_Legal_Capers/books-mifeco-website/images/`:

### Book Covers (25 files):
- `retainer-to-trouble-cover.jpg`, `clause-for-alarm-cover.jpg`, `affidavits-and-alibis-cover.jpg`
- `age-of-lightships-cover.jpg`, `age-of-lightships-bookN-cover.jpg` (N=1-4)
- `lunar-foundation-cover.jpg`, `lunar-foundation-bookN-cover.jpg` (N=1-4)
- `no-blue-sky-cover.jpg`, `no-blue-sky-bookN-cover.jpg` (N=1-5)
- `ai-that-works-cover.jpg`, `crisis-ready-cover.jpg`, `ai-agents-cover.jpg`
- `tomorrow-remembered-cover.jpg`

### Infographics (10 files):
- `cindy-lou-infographic.png`, `age-of-lightships-infographic.png`
- `lunar-foundation-infographic.png`, `no-blue-sky-infographic.png`
- `business-infographic.png`, `ai-that-works-infographic.png`
- `crisis-ready-infographic.png`, `ai-agents-infographic.png`
- `tomorrow-remembered-infographic.png`

### Other:
- `favicon.png`

### Magnet Cover Images (3 files):
- `age-of-lightships-magnet-cover.jpg`
- `lunar-foundation-magnet-cover.jpg`
- `no-blue-sky-magnet-cover.jpg`

## Post-Deploy Checklist
- [ ] Verify https://books.mifeco.com loads
- [ ] Test all series pages
- [ ] Confirm all images render (check browser console for 404s)
- [ ] Test email signup form at /api/subscribe
- [ ] Verify SSL certificate is active
- [ ] Test magnet download links
- [ ] Check subscriber CSV is writable (data/subscribers.csv)

## New Books Pipeline

The unified pipeline at `/mnt/usb_4tb/books/hermes_publish.py` handles:
- Compiling manuscripts from chapter files
- Generating EPUB 3 files
- Assembling KDP packages
- File-watcher CI/CD mode (`--watch`)
- Incremental builds (only rebuilds changed books)

Usage:
```bash
cd /mnt/usb_4tb/books
python3 hermes_publish.py --book [book-name] --steps compile epub kdp
python3 hermes_publish.py --all --steps epub
```

## DreamHost File Manager (files.dreamhost.com)

The web-based SFTP file manager is at `https://files.dreamhost.com/`.

**Critical:** The file manager uses a **separate SFTP password**, NOT the DreamHost panel password. If authentication fails with "An unknown error occurred during authentication", the SFTP password is different from the panel password. Ask the user for the SFTP-specific password.

**Login flow (fragile — follow exactly):**
1. Navigate to `https://files.dreamhost.com/`
2. Fill Host, Username, Initial Directory fields
3. Click the Authentication Type dropdown → select "Password"
4. Two password fields appear — fill both with the SFTP password
5. Click Connect

**Workaround if file manager fails:** Use the DreamHost panel → Websites → SFTP Users & Files → click "File Manager" link next to the user.

## Disk Space Management

The root partition (`/`) is only 117GB and can fill up quickly.

**Before large operations, check space:**
```bash
df -h /
```

**Clean up if needed:**
```bash
rm -rf /home/bob/.cache/pip /home/bob/.cache/uv /home/bob/.cache/camoufox /home/bob/.cache/ms-playwright /home/bob/.cache/huggingface
rm -rf /tmp/*.zip /tmp/*.tar.gz /tmp/node-compile-cache
```

**Write large files directly to USB drive** (`/mnt/usb_4tb/`) instead of `/tmp` when possible.

## CRITICAL: Human vs Virtual Consulting Separation

The main mifeco.com site has **two distinct consulting offerings** that must never be confused:

| | Human Consulting | Virtual Consulting |
|---|---|---|
| **What** | Free 30-min expert session, industry-specific strategic consulting | $199 business assessment — 30-50 question survey, two PDF reports |
| **Price** | Free (form) or $500+/session | $199 one-time |
| **Buttons** | "Schedule Free Consultation", "Consult with an Expert", "Schedule Industry Consultation" | "Business Assessment — $199", "Start Your Assessment — $199" |
| **Links to** | Consultation form popup (`de(!0)`) | `/consult` (new tab) |
| **Form title** | "Consult with an Expert" / "Book your free 30-minute strategy session" | N/A (separate site) |

**Rules:**
- NEVER make a $199 button open the consultation form popup — this was a bug that was fixed
- The consultation form popup is for HUMAN consulting only
- Virtual consulting card titles and buttons must link to `/consult` with `target="_blank"`
- "AI-Powered" in the SaaS software section (Hypatia Pro, PM Accelerator, VibraEngineer) is CORRECT — do NOT change those
- The virtual consulting assessment is for ANY business issue, not just AI — all text should reflect this

## CRITICAL: Website URL Structure

**The books site is at `mifeco.com/books/` — NOT `books.mifeco.com`.**

- `books.mifeco.com` is a separate (possibly unconfigured) domain
- The actual books website lives at `/home/dh_mwpxuu/mifeco.com/books/` as a subdirectory of the main WordPress site
- The main site at `/home/dh_mwpxuu/mifeco.com/` is a **React/Vite SPA** (not WordPress)
- The books subdirectory uses `router.php` to serve static files
- Images are at `/home/dh_mwpxuu/mifeco.com/books/images/`
- HTML references use relative paths like `images/cover.jpg` (not `/books/images/cover.jpg`)

**Always verify the actual web path before uploading files.** Check `router.php` to understand the routing.

## Adding Links to the React SPA (mifeco.com)

The main mifeco.com site is a React/Vite SPA. To add external links (e.g., to `/consult/` or `/books/`), you must either modify the minified JS bundle or inject an external script. See `references/react-spa-link-injection.md` for both approaches.

**Quick summary:**
- The SPA has its own `#bookstore` anchor section — this is NOT the same as `/books/`
- The SPA has service pages at `/strategic-planning`, `/digital-transformation`, etc.
- External links need `target="_blank"` and `rel="noopener"` since they leave the SPA
- Bundle hash changes on rebuild — prefer script injection for persistence

## Jarvis Page

The Jarvis AI assistant page lives at `mifeco.com/jarvis/` as a standalone HTML page (not part of the React SPA). See `references/jarvis-page-creation.md` for the creation pattern, file locations, and deployment steps.

**Key files:**
- `/home/dh_mwpxuu/mifeco.com/jarvis.html` (primary)
- `/home/dh_mwpxuu/mifeco.com/jarvis/index.html` (directory index, must be identical)

## Skill Patching via File I/O

When `skill_manage` cannot resolve a skill by name (common for `reference/openclaw-*` skills), use direct file I/O:

```python
import os, re

# Read the skill file
with open('/home/bob/.hermes/skills/reference/openclaw-consultant/SKILL.md') as f:
    content = f.read()

# Check if already patched
if 'MemPalace Query' in content:
    print("Already has preamble")
else:
    # Insert after frontmatter
    match = re.search(r'^---\s*\n.*?\n---\s*\n\n(#+|##+)', content, re.MULTILINE | re.DOTALL)
    if match:
        insert_pos = match.end(1) - len(match.group(1))
        new_content = content[:insert_pos] + preamble + '\n' + content[insert_pos:]
        with open('/home/bob/.hermes/skills/reference/openclaw-consultant/SKILL.md', 'w') as f:
            f.write(new_content)
```

**Note:** Always use `skill_manage` first. Fall back to file I/O only when the tool cannot resolve the skill path.

## Consulting Pipeline

For the full consulting pipeline architecture, survey flow, database schema, common issues, and credentials, see:
`references/consulting-pipeline-reference.md`

## Stripe Payment Integration

For Stripe payment flows (Express Checkout Element, webhooks, SDK installation, backdoor login pattern), see:
`references/stripe-payment-integration.md`

Key points:
- Composer is NOT pre-installed on DreamHost — install locally in project dir
- `vendor/autoload.php` must be required before `config.php` in every PHP file using Stripe SDK
- Express Checkout Element provides Link, Apple Pay, Google Pay, PayPal, Klarna without redirect
- Webhook endpoint returns 400 on GET (no signature), 500 means SDK not loaded

## Image Replacement Workflow

When replacing images on the website:

1. **First identify what HTML actually references** — grep all HTML files for image paths before touching anything
2. **Remove ALL old/unreferenced files** — don't just upload new ones on top
3. **Resize images for web** before uploading:
   - Covers: resize to 400x600 (2:3 ratio for 6x9" book covers)
   - Infographics: resize to 600-800px wide
   - Use PIL: `img.resize((400, 600), Image.LANCZOS)`
   - Convert RGBA→RGB before saving as JPEG
4. **Upload via SCP** (not the web file manager which is fragile)
5. **Verify every HTML reference resolves** after upload
6. **Create symlinks** if HTML references old naming conventions (e.g., `infographic-series.png` → `series-infographic.png`)

## Image Pipeline Pattern

See `references/image-pipeline-pattern.md` for the full image discovery → naming → CSS → deploy → cleanup workflow. Key rules:
- Always `object-fit: contain` (no cropping)
- Author photo is rectangle only (no border-radius)
- Clean up stale files on server AND local after every deploy
- Map images by book/series, not by arbitrary glob
