# DreamHost Subdirectory Deployment Pitfalls

## Absolute Path Trap

When deploying a PHP app to a subdirectory (e.g., `/consult/`), all internal links must include the subdirectory prefix.

**Wrong (links to root, causes 404):**
```html
<a href="/register.php">Sign Up</a>
```

**Correct:**
```html
<a href="/consult/register.php">Sign Up</a>
```

**Diagnosis:** If a page loads correctly directly but clicking a button/link gives a 404, inspect the link's `href` attribute. Absolute paths like `/page.php` resolve to the domain root, not the subdirectory.

**Fix pattern:** Search all HTML/PHP files for `href="/` and `action="/` that don't include the subdirectory prefix. Also check PHP `header('Location: ...')` calls — they should use `SITE_URL . $path` where `SITE_URL` includes the subdirectory (e.g., `https://mifeco.com/consult`).

**Verification command:**
```bash
curl -s "https://www.mifeco.com/consult/" | grep -o 'href="[^"]*"' | grep -v 'https://' | grep -v 'mailto:'
```
All results should include the `/consult/` prefix.

## .htaccess — Apache 2.2 Syntax

DreamHost may not support `Require all denied` (Apache 2.4+ syntax). Use `Order allow,deny` / `Deny from all`. A bad `.htaccess` causes 500 on every page.

**Working pattern:**
```apache
<FilesMatch "^(config\.php|setup\.php|composer\.json|composer\.lock)$">
    Order allow,deny
    Deny from all
</FilesMatch>
```

**Broken pattern (causes 500):**
```apache
<FilesMatch "^config\.php$">
    Require all denied
</FilesMatch>
```

## PHP Error Logging Disabled

`error_log()` does nothing on DreamHost. Use `file_put_contents('/tmp/debug.log', $msg, FILE_APPEND)` for debugging. Remove before production.

## cURL Timeout for External APIs

`CURLOPT_TIMEOUT_MS` + `CURLOPT_NOSIGNAL` may not work on shared hosting. Use `CURLOPT_TIMEOUT` (seconds, integer) instead.

## MySQL — Remote Only

DreamHost uses remote MySQL. `localhost` / unix socket won't work. Always use `-h mysql.mifeco.com` on CLI and in PHP config.
