# Standalone PHP Pages Alongside the React SPA

When you need to add a new page (blog, gallery, tools) to mifeco.com that the React SPA doesn't provide, create a standalone PHP page that coexists with the SPA at the domain root.

## Architecture

```
mifeco.com/
├── index.html                      # React/Vite SPA entry point
├── index.php                       # PHP router (if present)
├── wp-content/                     # WordPress core
├── blog.php                        # Standalone blog page (this pattern)
├── blog-api.php                    # Companion API endpoint
└── assets/                         # SPA compiled bundles
```

The key insight: **PHP pages at the root are NOT intercepted by the React SPA** because DreamHost serves `.php` files directly via the PHP handler. The SPA's `.htaccess` rewrite rules only catch non-file routes.

## Blog Page Pattern (from 2026-06-09 session)

### Step 1: Create the PHP Page

Create a standalone PHP page at `/tmp/blog.php` with:
- Full `<html>` document with inline CSS (the SPA uses Tailwind/CDN fonts, so the standalone page needs its own styles)
- Navigation bar that mirrors the SPA's header (logo, Home, Books, Consulting, Blog)
- A `<div id="blogList">` container for JavaScript-rendered content
- Client-side `fetch()` to the companion API endpoint

**Critical design choices:**
- **Inline CSS** — the standalone page can't import the SPA's compiled CSS. Write a self-contained stylesheet that matches the brand (colors, fonts, spacing).
- **Inter font** — match the SPA's `Inter` font via Google Fonts CDN link.
- **No React** — vanilla JS only. Keep it simple and durable.
- **Scrollable** — the page body naturally scrolls. No modal needed for the list itself.

### Step 2: Create the Companion API Endpoint

Create `blog-api.php` that queries WordPress directly via PDO:

```php
<?php
header('Content-Type: application/json');

$pdo = new PDO("mysql:host=mysql.mifeco.com;dbname=mifeco_com_1;charset=utf8", "ak48bme", "password");
$stmt = $pdo->query("SELECT ID, post_title, post_date, post_name, post_excerpt, guid
    FROM wp_gryu9c_posts
    WHERE post_type = 'post' AND post_status = 'publish'
    ORDER BY post_date DESC LIMIT 100");

$posts = [];
while ($row = $stmt->fetch(PDO::FETCH_ASSOC)) {
    $posts[] = [
        'id' => (int)$row['ID'],
        'title' => $row['post_title'],
        'date' => $row['post_date'],
        'slug' => $row['post_name'],
        'link' => 'https://mifeco.com/?p=' . $row['ID']
    ];
}
echo json_encode(['posts' => $posts, 'count' => count($posts)]);
```

**Table prefix:** WordPress uses `wp_gryu9c_` prefix — adjust if the site was rebuilt with a different prefix.

### Step 3: Add Navigation Link in SPA Bundle

Download the current SPA bundle, find the nav section, and add a `<a>` tag:

```python
# Desktop nav: insert after Virtual Consulting link
old_desktop = 'Virtual Consulting"}),l.jsxs("div",{className:"relative",children:[l.jsxs("button"'
new_desktop = 'Virtual Consulting"}),l.jsx("a",{href:"/blog.php",className:"text-gray-600 hover:text-blue-600 transition-colors",children:"Blog"}),l.jsxs("div",{className:"relative",children:[l.jsxs("button"'

js = js.replace(old_desktop, new_desktop)

# Mobile nav: same pattern but with "block" class
old_mobile = 'Virtual Consulting"}),l.jsx("a",{href:"#software"'
new_mobile = 'Virtual Consulting"}),l.jsx("a",{href:"/blog.php",className:"block text-gray-600 hover:text-blue-600 transition-colors",children:"Blog"}),l.jsx("a",{href:"#software"'
```

See `react-spa-bundle-modification.md` for the full modification workflow (download, brace/paren verification, upload).

### Step 4: Upload and Permissions

```bash
# Upload both files
scp /tmp/blog.php dh_mwpxuu@IAD1-SHARED-B8-42.DREAMHOST.COM:/home/dh_mwpxuu/mifeco.com/
scp /tmp/blog-api.php dh_mwpxuu@IAD1-SHARED-B8-42.DREAMHOST.COM:/home/dh_mwpxuu/mifeco.com/

# Set permissions (critical — 600 causes 403)
chmod 644 /home/dh_mwpxuu/mifeco.com/blog.php
chmod 644 /home/dh_mwpxuu/mifeco.com/blog-api.php
```

## Why This Pattern Works

1. **PHP is served directly** — DreamHost's PHP handler kicks in for `.php` files before the SPA's `.htaccess`
2. **No CORS issues** — the fetch from `blog.php` to `blog-api.php` is same-origin
3. **No build step needed** — unlike the SPA, PHP files are deployed as-is
4. **Durable against SPA rebuilds** — the standalone page survives even if the SPA is recompiled (the nav link will need re-adding though)

## Alternatives Considered (and why they didn't work)

| Approach | Problem |
|----------|---------|
| WP REST API | Returns 404 — `wp-json` endpoint is not available (blocked by SPA routing or WP config) |
| React modal in SPA | Requires source code access and rebuild of the Vite project |
| iframe embed | Styling conflicts, scroll issues, no native feel |

## Limitations

- **Navigation link is fragile** — the SPA bundle hash changes on rebuild, so the nav link addition must be re-applied. Keep the replacement script in a reference file.
- **No SPA routing** — the standalone page doesn't use React Router, so browser back/forward from the blog won't seamlessly return to the SPA state.
- **Styling maintenance** — the inline CSS CSS must be manually kept in sync with the SPA's appearance.