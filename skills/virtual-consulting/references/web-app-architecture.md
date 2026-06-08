# Web Application Architecture — Consulting Pipeline

## Pattern: PHP Frontend + Python AI Backend

**When to use:** Building web applications on DreamHost (PHP/MySQL) that need AI-heavy processing (question generation, PDF building, NLP) that PHP can't do well.

### Architecture

```
DreamHost (PHP/MySQL)          Local Machine (Python)
─────────────────────          ─────────────────────
index.php (landing)            api_server.py (HTTP API)
register.php (auth)            ├── /api/generate-questions
pay.php (Stripe)               └── /api/generate-reports
survey.php (questions)
download.php (PDFs)            WeasyPrint for PDF generation
stripe-webhook.php
```

### Why this split?
- **DreamHost** handles: user auth, sessions, Stripe payments, form rendering, file downloads
- **Python** handles: AI question generation, WeasyPrint PDF building, complex data processing
- **Communication:** PHP calls Python via HTTP POST with API key authentication

### Key implementation details

**PHP → Python API call:**
```php
function callPythonAPI(string $endpoint, array $data = []): array {
    $url = PYTHON_API_URL . $endpoint;
    $payload = json_encode(array_merge($data, ['api_key' => PYTHON_API_KEY]));
    $ch = curl_init($url);
    curl_setopt_array($ch, [
        CURLOPT_POST => true,
        CURLOPT_POSTFIELDS => $payload,
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_HTTPHEADER => ['Content-Type: application/json'],
        CURLOPT_TIMEOUT => 60,
    ]);
    $response = curl_exec($ch);
    curl_close($ch);
    return json_decode($response, true) ?: ['success' => false];
}
```

**Python API server:** Uses `http.server.HTTPServer` (no external deps). Listens on `0.0.0.0:8190`. Verify API key on every request.

**Keep-alive cron:**
```bash
*/5 * * * * /home/bob/.hermes/scripts/keep-consulting-api.sh
```

### Database schema pattern
- Use `JSON` columns for flexible data (questions, responses)
- Separate `survey_responses` table for individual answers (efficient partial saves)
- `survey_followups` table to track "I don't know, someone else knows" pending questions
- `documents` table to track generated PDFs with file paths

### PDF generation
- **WeasyPrint** (preferred): `pip install weasyprint`. Converts HTML → PDF with CSS support.
- **Fallback:** Write HTML file, try `wkhtmltopdf` subprocess, keep HTML if neither works.
- Build PDFs as complete HTML documents with `@page` CSS rules for print formatting.

### "I don't know" survey branching pattern

Every scale/choice question includes "I don't know / Not applicable" as the last option. When selected:

1. **Modal interstitial** with two paths:
   - **"Someone else knows"** → Pause screen. Save position in `survey_followups` table. Persistent banner on return.
   - **"Nobody knows / Not tracked"** → Show 2-3 diagnostic "why" questions, then continue.

2. **Database tracking:**
   - `survey_responses.answer = 'PENDING_FOLLOWUP'` for "someone else knows"
   - `survey_followups` table: pending → returned → resolved
   - Diagnostic answers stored as `{qid}_why{step}` question IDs

### Deployment
- Use **paramiko** (Python SFTP) to deploy PHP files to DreamHost
- Set permissions: 644 for PHP/HTML, 755 for download scripts, 777 for reports directory
- Test with `curl -s -o /dev/null -w "%{http_code}" https://domain/page.php`

### Common pitfalls
- **Port conflicts:** `pkill -f api_server.py` before restarting. Check with `lsof -ti:8190`.
- **Multiline Python editing:** Use line-by-line analysis, not regex — regex breaks on nested parens.
- **DreamHost redirects:** `mifeco.com` may redirect to `www.mifeco.com` — test both.

### Common pitfalls (updated)

**PHP operator precedence with null coalescing:**
```php
// WRONG — evaluates as: $_POST['action'] ?? ('' === 'register') which is always truthy
if ($_POST['action'] ?? '' === 'register') { ... }

// CORRECT — parentheses force the intended evaluation
if (($_POST['action'] ?? '') === 'register') { ... }
```
This applies to ALL `$_POST`/`$_GET` checks with `??` and comparison operators. Always wrap the null-coalesced value in parentheses before comparing.

**Port conflicts:**
```bash
pkill -f api_server.py  # Kill existing
lsof -ti:8190           # Check if port is free
```

**Multiline Python editing:** Use line-by-line analysis, not regex — regex breaks on nested parens in multiline function calls. When patching Python that spans multiple lines, read the full block and rewrite it cleanly.

**DreamHost panel is a React SPA:** Cannot be automated via simple curl POST. Database creation must be done via MySQL CLI (if user has CREATE privilege) or by manually logging into the panel. The panel login form uses fields: `username`, `password`, `Nscmd`.

**DreamHost redirects:** `mifeco.com` may redirect to `www.mifeco.com` — test both.

**Session cookies across curl requests:** When testing PHP forms that use CSRF tokens, you MUST use a cookie jar (`-c` and `-b` flags) and extract the CSRF token from the GET response before POSTing. The session ID is set in a cookie on the first request.

**Stripe webhook endpoint:** Returns 500 until Stripe PHP SDK is installed (`composer require stripe/stripe-php`). This is expected during setup.
