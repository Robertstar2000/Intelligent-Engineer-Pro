# SPA + WordPress Router — Blank Page Fix

## The Bug

The root path `/` was routing to WordPress instead of the React SPA.

In `/home/dh_mwpxuu/mifeco.com/index.php`:

```php
// BUG: root path was routed to WordPress, serving a blank homepage
if ($request_uri === '' || $request_uri === '/index.php') {
    $is_wp = true;
}
```

When visiting `https://www.mifeco.com/`, Apache's `DirectoryIndex` served `index.php` (which exists alongside `index.html`). The router trimmed `/` to `''`, then sent the request to WordPress. WordPress had no content (its theme wasn't built for this SPA-first setup), producing a blank page.

Additionally, WordPress's WP Super Cache was active (`WP_CACHE=true` in wp-config.php with WPCACHEHOME pointing to wp-super-cache), which could cache the blank WordPress response and serve it to subsequent visitors.

## The Fix

```php
// Only /index.php directly routes to WordPress, NOT empty root path
if ($request_uri === '/index.php') {
    $is_wp = true;
}
```

The root path falls through to:
```php
// Serve the SPA
readfile(__DIR__ . '/index.html');
```

## Root Cause

There are **two index files** in the web root:
- `index.html` — the React SPA (520 bytes)
- `index.php` — the PHP router (1874 bytes)

Apache's `DirectoryIndex` default is `index.html index.php` — so `index.html` should be served first. However, the PHP router was explicitly catching the root path and routing to WordPress.

## Verification

- Root `https://www.mifeco.com/` → should return the SPA HTML (contains `<div id="root">`)
- `https://www.mifeco.com/wp-admin/` → should return 302 redirect to WordPress login
- `https://www.mifeco.com/wp-login.php` → should return 200 (WordPress login page)

## Backup

The original buggy `index.php` was renamed to `index.php.bak` on DreamHost at `/home/dh_mwpxuu/mifeco.com/index.php.bak`. The fixed version is at `index.php`.