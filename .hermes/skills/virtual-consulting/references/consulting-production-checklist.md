# Consulting System — Production Readiness Checklist

## Security Audit Points

### Credentials & Secrets
- [ ] No hardcoded DB credentials in config.php (use `getenv()` or `.env`)
- [ ] No hardcoded SSH passwords in deploy scripts
- [ ] No hardcoded backdoor credentials in PHP files
- [ ] API keys are not default/placeholder values
- [ ] Stripe keys are real (not `pk_live_CHANGEME`)
- [ ] `debug.php` removed from production or IP-restricted

### Input Validation
- [ ] All form inputs sanitized before DB insert
- [ ] CSRF tokens verified on all POST handlers
- [ ] Rate limiting on auth endpoints

### Infrastructure
- [ ] HTTPS enforced in PHP (not just .htaccess)
- [ ] File download endpoint validates ownership + checks path traversal

## Functional Checklist

### Database
- [ ] Table names consistent between setup.php and all queries (`consulting_*` prefix)
- [ ] Foreign keys reference correct table names
- [ ] All 7 tables created: `consulting_users`, `consulting_payments`, `consulting_surveys`, `consulting_survey_responses`, `consulting_documents`, `consulting_survey_followups`, `activity_log`

### Payment Flow
- [ ] Stripe keys configured in environment
- [ ] Stripe PHP SDK installed on DreamHost
- [ ] Webhook endpoint accessible and idempotent
- [ ] Backdoor bypass works for testing

### Survey Flow
- [ ] Python API timeout is >=120s (not 5s)
- [ ] Fallback question generation works if API is down
- [ ] "I don't know" flow works end-to-end

### Report Generation & Delivery
- [ ] Report generation actually works (not fire-and-forget no-op)
- [ ] PDFs stored in accessible location (synced to DreamHost or generated there)
- [ ] Email template is valid HTML
- [ ] Email sent to client with download links
- [ ] `forgot-password.php` exists

## Known Bug Patterns

### Setup/Query Table Name Mismatch
`setup.php` creates `users` but code queries `consulting_users`. Always use `consulting_*` prefix in BOTH.

### Fire-and-Forget No-Op
`_fireAndForgetPythonAPI()` is empty. Survey marks "complete" without generating reports.

### Email Template Corruption
`email-templates/complete.html` was overwritten with .htaccess content. Rebuild and add protective comment header.

### Report File Location Mismatch
Python API generates locally, download.php serves from DreamHost. Sync via SFTP or generate on DreamHost.
