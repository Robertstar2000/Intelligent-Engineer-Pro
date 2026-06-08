# DreamHost nginx Architecture Reference

## Key Discovery: nginx, NOT Apache

DreamHost shared hosting runs **nginx** as the front-end web server. There is NO Apache, no `mod_rewrite`, and `.htaccess` files are **completely ignored**.

### Evidence
- `ps aux | grep nginx` — nginx worker processes running
- `ps aux | grep apache` — no Apache processes
- `/etc/nginx/nginx.conf` — active nginx config
- `/etc/nginx/sites-enabled/default` — default vhost with `try_files $uri $uri/ =404`
- `ls /etc/apache2/mods-enabled/rewrite*` — mod_rewrite NOT loaded
- `cat /etc/apache2/apache2.conf | grep AllowOverride` — AllowOverride None (Apache not even running)

### Implications

1. **`.htaccess` is decorative** — Any rewrite rules, redirects, or access controls in `.htaccess` have no effect. The file can be replaced with a comment.

2. **WordPress routing requires PHP-level handling** — The root `index.php` must contain a router that detects WordPress paths and loads WP, while serving the SPA for everything else.

3. **REST API URLs must use `index.php?rest_route=`** — The `/wp-json/` path is intercepted by nginx's `try_files` and serves the SPA. Use:
   - `https://www.mifeco.com/index.php/wp-json/` for WP REST discovery
   - `https://www.mifeco.com/index.php?rest_route=/mifeco/v1/send-email` for MIFECO endpoints

4. **Real directories block WP plugin routing** — If a directory like `/admin/` exists on disk, nginx serves it directly. WordPress plugins cannot intercept requests to real directories.

### nginx Default Config (mifeco.com)
```nginx
server {
    listen 80 default_server;
    root /var/www/html;
    index index.html index.htm index.nginx-debian.html;
    server_name _;
    location / {
        try_files $uri $uri/ =404;
    }
}
```

### PHP Router in Root index.php
The root `/home/dh_mwpxuu/mifeco.com/index.php` contains:
```php
$wp_paths = ['/wp-json', '/wp-admin', '/wp-login.php', '/wp-signup.php', '/xmlrpc.php'];
// Also: wp-content/*, wp-includes/*, index.php itself

if (is_wp_request()) {
    define('WP_USE_THEMES', true);
    require __DIR__ . '/wp-blog-header.php';
} else {
    readfile(__DIR__ . '/index.html');  // SPA
}
```

### REST API URL Reference

| URL Pattern | Works? | Notes |
|-------------|--------|-------|
| `/wp-json/` | ❌ SPA HTML | nginx try_files |
| `/index.php/wp-json/` | ✅ JSON | PHP router → WP |
| `/index.php?rest_route=/` | ✅ JSON | PHP router → WP |
| `/wp-admin/` | ✅ WP Admin | PHP router → WP |
| `/wp-login.php` | ✅ WP Login | PHP router → WP |
| `/admin/` | ❌ Static dir | Real directory on disk |
| `/` | ✅ SPA | PHP router → index.html |
