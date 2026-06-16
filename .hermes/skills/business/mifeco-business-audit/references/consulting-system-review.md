# MIFECO Business Audit — Consulting System Review

## Consulting System (mifeco.com/consult/)

### Architecture
- PHP frontend on DreamHost (shared hosting)
- Python API server on local machine (port 8190) for question generation + PDF building
- SSH reverse tunnel connects DreamHost → local MySQL + Python API
- Stripe for payment processing ($199 one-time)
- 8-stage pipeline: Lead → Contacted → Survey → Research → Generate Reports → Quality Review → Delivery → Complete

### Tech Stack
- PHP 8.x on DreamHost (mysql.mifeco.com)
- Python 3.x locally (WeasyPrint for PDF generation)
- Stripe Checkout (Express Checkout Element)
- MySQL (InnoDB)

### Key Files
- `config.php` — All credentials and API keys
- `setup.php` — Database table creation
- `survey.php` — Survey UI and state machine
- `pay.php` — Stripe payment page
- `register.php` — Authentication (register/login/backdoor)
- `download.php` — PDF report download
- `stripe-webhook.php` — Stripe event handler
- `api_server.py` — Python API (question gen + PDF build)
- `deploy.sh` — SFTP deployment script

### Critical Issues (as of 2026-06-15)
1. **Hardcoded secrets** in config.php, deploy.sh, register.php
2. **Fire-and-forget no-op** — reports never generated
3. **Table name mismatch** — setup.php vs application queries (fixed)
4. **Python API timeout** was 5s, needs 120s+ (fixed)
5. **Email template corrupted** (rebuilt)
6. **No email delivery** code
7. **Report files** generated on local machine, served from DreamHost (never sync)
8. **No admin dashboard**
9. **No forgot-password** implementation
10. **debug.php** exposes credentials

### Revenue Readiness Score: 70%
- UI/UX: 90% (polished, professional)
- Payment flow: 60% (Stripe keys needed, webhook needs SDK)
- Survey flow: 85% (works, needs timeout fix)
- Report generation: 20% (no-op, needs full implementation)
- Email delivery: 10% (template rebuilt, sending code needed)
- Security: 40% (hardcoded secrets, no rate limiting, debug.php exposed)

### Recommended Priority
1. Rotate all secrets → environment variables
2. Implement report generation (fix fire-and-forget)
3. Sync reports to DreamHost or generate there
4. Implement email delivery
5. Install Stripe SDK + configure real keys
6. Remove debug.php
7. Add admin dashboard
8. Add forgot-password flow
