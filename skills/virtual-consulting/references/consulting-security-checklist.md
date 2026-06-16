# Consulting System — Security Audit Checklist

**Purpose:** Run this checklist before every production deployment of the consulting system.
**Last updated:** 2026-06-15

## P0 — Secrets & Credentials

- [ ] No hardcoded DB credentials in any PHP file (use `getenv()`)
- [ ] No hardcoded SSH passwords in any shell script (use env vars)
- [ ] No hardcoded backdoor credentials in any PHP file (use `getenv()`)
- [ ] Stripe keys loaded from environment variables, not hardcoded
- [ ] API keys loaded from environment variables, not hardcoded
- [ ] `debug.php` removed from production (or IP-restricted)
- [ ] All exposed credentials rotated after any commit to version control
- [ ] `.env` file exists outside web root and is in `.gitignore`

## P1 — Input Validation & Injection

- [ ] All user inputs sanitized before DB insertion (use prepared statements)
- [ ] CSRF tokens verified on all POST handlers
- [ ] CSRF tokens regenerated after use (not single token per session)
- [ ] File download paths validated (no path traversal via `file_path` parameter)
- [ ] Email headers sanitized (no header injection)

## P2 — Authentication & Session

- [ ] Passwords hashed with `PASSWORD_ARGON2ID`
- [ ] Session cookies: `httponly`, `secure`, `samesite=Lax`
- [ ] Session GC max lifetime set (86400 = 24hr)
- [ ] Rate limiting on auth endpoints (register, login, forgot-password)
- [ ] Forgot-password tokens expire (24hr max)
- [ ] Account enumeration prevented (same message whether email exists or not)

## P3 — Infrastructure

- [ ] HTTPS enforced (not just in .htaccess — also in PHP redirect)
- [ ] Error display disabled in production (`display_errors = 0`)
- [ ] Error logging enabled (`log_errors = 1`)
- [ ] File permissions correct (644 for static files, 755 for directories)
- [ ] Reports directory writable by web server

## P4 — Payment & Webhook

- [ ] Stripe webhook signature verified on every request
- [ ] Webhook idempotency (check for duplicate event IDs)
- [ ] Payment status verified server-side (not just client redirect)
- [ ] Stripe PHP SDK installed and autoloaded
- [ ] Test mode used for development (pk_test_ / sk_test_)

## P5 — Report Generation & Delivery

- [ ] Python API timeout >= 120s (PDF generation takes 30-120s)
- [ ] Report files synced to DreamHost after generation
- [ ] Download.php validates file ownership before serving
- [ ] Email delivery uses authenticated SMTP (not bare `mail()`)
- [ ] Email template exists and is valid HTML

## P6 — Database

- [ ] All table names use consistent prefix (`consulting_*`)
- [ ] Foreign keys reference correct table names
- [ ] `consulting_activity_log` table exists for audit trail
- [ ] Survey timeout/cleanup for stale in-progress surveys
