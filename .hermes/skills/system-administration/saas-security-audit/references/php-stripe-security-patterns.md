# PHP/Stripe Application — Security Audit Patterns

## Hardcoded Credentials Pattern

**What to grep for:**
```bash
grep -rn "password\|secret\|key\|token" --include="*.php" --include="*.sh" | grep -v "getenv\|$_ENV\|$_SERVER\|config->\|define.*getenv"
```

**Common locations:**
- `config.php` — DB credentials, Stripe keys, API keys
- `deploy.sh` — SSH passwords
- `register.php` — backdoor credentials

**Fix pattern:**
```php
// BEFORE (insecure):
define('DB_PASS', '7jpetxEL');

// AFTER (secure):
define('DB_PASS', getenv('DB_PASS') ?: '');
```

## Fire-and-Forget No-Op Pattern

**What to look for:**
```bash
grep -rn "function.*fire\|function.*forget\|function.*async" --include="*.php"
```

**Symptom:** Function is defined but body is empty or contains only a comment. Status is set to "complete" before the async work finishes.

**Fix:** Either make it synchronous (wait for result) or implement proper queue/cron-based processing with status polling.

## Table Name Mismatch Pattern

**What to check:**
```bash
# Compare table names in setup.php vs application queries
grep -oP 'CREATE TABLE IF NOT EXISTS \K\w+' setup.php
grep -oP 'FROM \K\w+' *.php | sort -u
```

**Root cause:** Setup script and application code are maintained independently. Prefix changes in one aren't reflected in the other.

**Prevention:** Use a single `TABLES` constant array that both setup and queries reference.

## Email Template Corruption Pattern

**What to check:**
```bash
head -5 email-templates/*.html
```

**Symptom:** Template file contains non-HTML content (Apache rules, binary data, etc.).

**Prevention:** Add HTML comment header to templates. Validate templates in deployment script.

## Report File Location Mismatch

**What to check:**
```bash
grep -rn "REPORTS_DIR\|reports_dir\|consulting-reports" --include="*.py" --include="*.php"
```

**Symptom:** Python API saves to local path, PHP download serves from different filesystem.

**Fix:** Either sync files post-generation or generate on the serving machine.
