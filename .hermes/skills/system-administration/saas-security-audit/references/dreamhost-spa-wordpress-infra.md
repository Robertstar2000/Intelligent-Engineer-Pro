# DreamHost-WordPress SPA Coexistence — Infrastructure Notes
**Created**: 2026-05-31

## Critical: AllowOverride None

DreamHost shared hosting has `AllowOverride None` in `/etc/apache2/apache2.conf`. `.htaccess` files are COMPLETELY IGNORED for rewrite purposes.

**Implications:**
- Do NOT add mod_rewrite rules to `.htaccess` — they silently fail
- The SPA index.html is served by DreamHost's built-in static file priority
- WordPress paths (/wp-admin/, /wp-json/, /wp-content/) are routed through DreamHost's panel-level WordPress config, NOT .htaccess
- If /wp-json/ returns SPA HTML, the issue is NOT .htaccess — check: (1) plugin active, (2) permalinks flushed, (3) DreamHost panel WordPress settings

## Email Infrastructure (MIFECO)

- Shared account: MIFECOinc@gmail.com / Rm2214ri#### (ONLY account on DreamHost, shared across ALL apps)
- SMTP: smtp.gmail.com:587 STARTTLS (NOT smtp.dreamhost.com)
- REST endpoint: POST /wp-json/mifeco/v1/send-email (requires secret param)
- Unsubscribe: POST /wp-json/mifeco/v1/unsubscribe (public, adds to suppression-list.txt)
- Subject tag: [MIFECO] prepended to all outbound subjects
- Abuse contact: MIFECOinc@gmail.com — "reply with ABUSE in subject line"
- Physical address: 147 Bathclub Cir, N. Redington Beach, FL 33708 in every footer

## Deployment Reliability (Best → Worst)

1. SCP + SSH with pexpect — Most reliable
2. rsync with pexpect — Reliable for bulk (NEVER --delete)
3. WP admin browser upload — Works but fetch() can navigate to about:blank
4. Monsta FTP in headless — Unreliable, clicks don't navigate

## Session Expiry

- DreamHost panel SSO: ~15-30 min — same for WP admin
- Re-auth path: panel login → click "Log in to WordPress" button
- Direct /wp-admin/ navigation does NOT auto-authenticate from panel cookies
