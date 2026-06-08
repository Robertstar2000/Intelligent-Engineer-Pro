# router.php — Smart Router for mifeco.com/books

The books website at `mifeco.com/books/` uses a PHP router to serve static files (HTML, CSS, JS, images, EPUBs, PDFs) from the `/home/dh_mwpxuu/mifeco.com/books/` directory.

## The router.php File

Located at: `/home/dh_mwpxuu/mifeco.com/books/router.php`

```php
<?php
$uri = $_SERVER['REQUEST_URI'];
$path = parse_url($uri, PHP_URL_PATH);

// Books section - serve from this directory
if (preg_match('#^/books(/.*)?#', $path)) {
    $relativePath = preg_replace('#^/books#', '', $path);
    if ($relativePath === '' || $relativePath === '/') {
        $relativePath = '/index.html';
    }
    
    $filePath = __DIR__ . $relativePath;
    
    if (is_file($filePath)) {
        $ext = pathinfo($filePath, PATHINFO_EXTENSION);
        $mimeTypes = [
            'html' => 'text/html', 'css' => 'text/css', 'js' => 'application/javascript',
            'png' => 'image/png', 'jpg' => 'image/jpeg', 'jpeg' => 'image/jpeg',
            'gif' => 'image/gif', 'svg' => 'image/svg+xml', 'ico' => 'image/x-icon',
            'json' => 'application/json', 'woff' => 'font/woff', 'woff2' => 'font/woff2',
            'eot' => 'application/vnd.ms-fontobject', 'ttf' => 'font/ttf', 'otf' => 'font/otf',
            'epub' => 'application/epub+zip', 'pdf' => 'application/pdf',
            'txt' => 'text/plain', 'md' => 'text/plain',
        ];
        if (isset($mimeTypes[$ext])) {
            header('Content-Type: ' . $mimeTypes[$ext]);
        }
        readfile($filePath);
        exit;
    }
}
readfile(__DIR__ . '/index.html');
```

## CRITICAL: $ Signs in PHP Variables

When writing router.php via SSH (bash heredoc or pexpect sendline), `$` characters in PHP variable names are interpreted by the shell. The file will be written with `$` stripped, producing broken PHP like `uri = _SERVER['REQUEST_URI']` instead of `$uri = $_SERVER['REQUEST_URI']`.

**Fixes:**
1. Write the file locally with a `'ENDOFPHP'` single-quoted heredoc (which prevents shell interpretation):
   ```bash
   cat > /tmp/router.php << 'ENDOFPHP'
   <?php
   $uri = $_SERVER['REQUEST_URI'];
   // ... rest of PHP
   ENDOFPHP
   ```
2. SCP the local file to the server
3. Verify with: `grep -c '\$' router.php` (should be 13+ for the router above)

## Pitfalls

- **books-section vs books**: An earlier version of the router referenced `books-section/` directory which doesn't exist. Always use `books/`
- **Missing $ signs**: Always verify PHP syntax with `php -l router.php` after deploying
- **File path logic**: The router strips `/books` prefix from the URL and prepends `__DIR__`, so URL `/books/images/cover.jpg` serves from `/home/dh_mwpxuu/mifeco.com/books/images/cover.jpg`