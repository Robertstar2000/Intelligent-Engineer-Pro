# DreamHost nginx Architecture Reference

## Key Facts

| Fact | Detail |
|------|--------|
| Web server | nginx (NOT Apache) |
| `.htaccess` | Completely ignored |
| `mod_rewrite` | Not loaded |
| Ports | 80 (HTTP), 443 (HTTPS) |
| Vhost config | `/etc/nginx/sites-enabled/default` only; per-domain routing managed at panel level |
| Conf.d writable? | No — `/etc/nginx/conf.d/` is root-only |
| PHP handler | PHP-FPM via nginx `fastcgi_pass` |

## nginx Default Config Locations

```bash
# Main config
/etc/nginx/nginx.conf

# Enabled sites
/etc/nginx/sites-enabled/default

# Modules (note: nginx modules, not Apache!)
/etc/nginx/modules-enabled/

# FastCGM pools
/etc/php/8.1/fpm/pool.d/www.conf
```

## PHP Smart Router Pattern

When WordPress coexists with a SPA at the web root, the root `index.php` must act as a router:

```php
<?php
$request_uri = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);
$request_uri = rtrim($request_uri, '/');

$wp_paths = ['/wp-json', '/wp-admin', '/wp-login.php', '/wp-signup.php', '/xmlrpc.php'];
$is_wp = false;
foreach ($wp_paths as $wp_path) {
    if (strpos($request_uri, $wp_path) === 0) { $is_wp = true; break; }
}
if (preg_match('#^/(wp-content|wp-includes)/#', $request_uri)) $is_wp = true;
if ($request_uri === '' || $request_uri === '/index.php') $is_wp = true;

if ($is_wp) {
    define('WP_USE_THEMES', true);
    require __DIR__ . '/wp-blog-header.php';
    exit;
}
readfile(__DIR__ . '/index.html');
```

## URL Routing Reference

| URL Pattern | What serves it |
|-------------|---------------|
| `/` | SPA `index.html` (via router) |
| `/about/` | SPA `index.html` (via router) |
| `/admin/` | Static files (nginx `try_files` finds directory) |
| `/admin/api.php` | PHP file directly (if not intercepted by WP plugin) |
| `/wp-admin/` | WordPress (via router → index.php → wp-blog-header.php) |
| `/wp-login.php` | WordPress (via router) |
| `/wp-json/` | WordPress (via router) — returns REST API |
| `/index.php/wp-json/` | WordPress — direct access, always works |
| `/index.php?rest_route=/` | WordPress — direct access, always works |

## Testing Commands

```bash
# Check what serves a URL
curl -s -o /dev/null -w '%{http_code}' 'https://www.mifeco.com/wp-json/'          # Should be 404 (SPA)
curl -s -o /dev/null -w '%{http_code}' 'https://www.mifeco.com/index.php/wp-json/' # Should be 200 (WP)
curl -s -o /dev/null -w '%{http_code}' 'https://www.mifeco.com/wp-admin/'          # Should be 302 (redirect)
curl -s -o /dev/null -w '%{http_code}' 'https://www.mifeco.com/admin/'             # Should be 200 (static)

# Check nginx processes
ps aux | grep nginx | grep -v grep

# Check listening ports
netstat -tlnp 2>/dev/null | grep -E ':80|:443'
# or
ss -tlnp | grep -E ':80|:443'
```

## Why `.htaccess` Was Never Working

The `.htaccess` file format is Apache-specific. DreamHost's nginx never reads it. The original `.htaccess` with "WordPress + SPA Rewrite Rules" was decorative — those rules never executed. The SPA's `index.html` was served for ALL non-file requests because nginx's `try_files $uri $uri/ =404` doesn't know about WordPress pretty permalinks.

The PHP router in `index.php` replaces `.htaccess` rewrite rules for nginx.
