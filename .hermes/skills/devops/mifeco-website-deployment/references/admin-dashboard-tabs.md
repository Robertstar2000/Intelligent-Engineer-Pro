# MIFECO Admin Dashboard — Tab Management

## Overview
The MIFECO admin dashboard is a standalone HTML application at `/admin/` (not part of the React SPA). It has a sidebar navigation with tabs linking to different sections.

## File Location
- **Admin dashboard**: `/home/dh_mwpxuu/mifeco.com/admin/index.html`
- **Jarvis page**: `/home/dh_mwpxuu/mifeco.com/jarvis.html` and `/home/dh_mwpxuu/mifeco.com/jarvis/index.html`

## Current Sidebar Tabs

### Internal Sections (hash links, same page)
- 📚 Books → `#books`
- ☁️ SaaS → `#saas`
- 💼 Consulting → `#consulting`
- 📊 Lead & Promotion → `#lead-promotion`

### External Pages
- 🎨 Content Command Center → `content-command-center.html`
- 🤖 Jarvis → `/jarvis` (new tab)
- ⚙️ Admin → `/admin` (new tab)
- 💬 Consult → `/consult` (new tab)
- 📖 Books Site → `/books` (new tab)

## Adding/Modifying Tabs

The sidebar nav is in `index.html` as `<nav class="sidebar-nav">`. To add a new tab:

1. Edit `/home/dh_mwpxuu/mifeco.com/admin/index.html`
2. Find `<nav class="sidebar-nav">...</nav>`
3. Add a new `<a>` element with:
   - `href` — the URL (use absolute paths like `/jarvis` for cross-site links)
   - `target="_blank"` — for external links that should open in new tabs
   - `onclick="closeSidebar()"` — for mobile sidebar auto-close
   - Icon emoji in `<span class="icon">`

Example:
```html
<a href="/new-page" target="_blank" onclick="closeSidebar()"><span class="icon">🆕</span> New Page</a>
```

## Sidebar Footer Links

The footer section at the bottom of the sidebar also has quick links. Update `<div class="sidebar-footer">` to add footer shortcuts.

## Deployment

Since this is a plain HTML file (not part of the React SPA), changes are deployed via SFTP:
```python
sftp.put("/tmp/admin_index.html", "/home/dh_mwpxuu/mifeco.com/admin/index.html")
```

No bundle hash changes or cache invalidation needed — changes are immediate.

## Jarvis Page

The Jarvis page (`/jarvis`) is a standalone HTML page with:
- Dark theme matching the admin dashboard
- Chat-style UI (placeholder for Hermes Agent API integration)
- Sidebar with quick actions for Books, SaaS, Consulting, Content, Research, System
- Header navigation to Dashboard, Content, Consult, Books

To update Jarvis, edit `/home/dh_mwpxuu/mifeco.com/jarvis.html` and copy to `/home/dh_mwpxuu/mifeco.com/jarvis/index.html`.
