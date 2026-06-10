# Consulting Pipeline — Web Implementation Reference

**Live URL:** `https://mifeco.com/consult/`
**Admin backdoor:** `https://mifeco.com/consult/survey.php?backdoor=1`

## Database Tables

| Table | Notes |
|-------|-------|
| `consulting_users` | Users |
| `consulting_surveys` | Survey state machine |
| `consulting_survey_responses` | Individual responses |
| `consulting_payments` | **NOT `payments`** — this was a bug |
| `consulting_activity_log` | Created 2026-06-09 |

## Fixes Applied 2026-06-09

1. **pay.php table names:** `payments` → `consulting_payments`, `surveys` → `consulting_surveys`
2. **consulting_activity_log table:** Created (was missing, causing silent failures)
3. **survey.php backdoor:** Added `?backdoor=1` GET handler — auto-creates session, skips payment, goes straight to questions
4. **Admin Dashboard:** Added 💼 Virtual Consulting card → `/consult/survey.php?backdoor=1`

## Virtual Consulting Deliverable Format

**Reports are SINGLE PDFs, NOT KDP packages.**

Each report is a standalone PDF with:
- Integrated cover image (page 1)
- Delivery cover letter (page 2)
- Table of contents (page 3)
- 30+ page detailed report with research-backed analysis

Content sources: initial questions + survey data + LLM knowledge + web search when needed

## Open Issues
- **Stripe keys are placeholders** in config.php (`pk_live_CHANGEME`, `price_CHANGEME`) — real Stripe keys needed for regular (non-backdoor) payments to work

## Flows

### Backdoor (admin → survey directly)
Admin dashboard → 💼 Virtual Consulting → `/consult/survey.php?backdoor=1` → auto-login as Robert Mills → survey questions immediately

### Regular User
`/consult/` → `/register.php` → `/pay.php` (Stripe $199) → `/survey.php`

Backdoor credentials: `Robertstar@aol.com` / `Rm2214ri#`
