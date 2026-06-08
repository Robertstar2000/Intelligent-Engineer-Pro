# Jarvis Page — Creation & Deployment

## Overview
Jarvis is a standalone HTML page at `mifeco.com/jarvis/` — NOT part of the React SPA. It serves as the MIFECO AI assistant interface.

## File Locations
- **Primary**: `/home/dh_mwpxuu/mifeco.com/jarvis.html`
- **Directory index**: `/home/dh_mwpxuu/mifeco.com/jarvis/index.html` (copy of jarvis.html)
- Both must be kept in sync.

## Page Structure
- Dark theme (`#0f172a` background) matching admin dashboard
- Header with nav links: Dashboard, Content, Consult, Books
- Sidebar with quick action categories: Quick Actions, Content, Research, System
- Chat-style message area with user/assistant bubbles
- Quick action pills below the input
- Status bar showing connection status

## Creation Pattern
When creating a new standalone page for mifeco.com:

1. Use the admin dashboard's CSS variables for consistency:
   ```css
   :root {
     --bg-primary: #0f172a;
     --bg-secondary: #1e293b;
     --bg-card: #1a2332;
     --border: #334155;
     --text-primary: #e2e8f0;
     --text-secondary: #94a3b8;
     --accent: #00ffcc;
   }
   ```

2. Include Inter font from Google Fonts (same as admin):
   ```html
   <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;80&display=swap" rel="stylesheet">
   ```

3. For pages that should be accessible from the admin dashboard sidebar:
   - Add to `<nav class="sidebar-nav">` in `admin/index.html`
   - Use `target="_blank"` for external links
   - Use `onclick="closeSidebar()"` for mobile support

4. Deploy both files:
   ```python
   sftp.put("/tmp/jarvis.html", "/home/dh_mwpxuu/mifeco.com/jarvis.html")
   sftp.put("/tmp/jarvis.html", "/home/dh_mwpxuu/mifeco.com/jarvis/index.html")
   ```

## Cache Invalidation
After updating any file on DreamHost, force cache invalidation:
```python
sftp.utime("/path/to/file", None)  # Updates timestamp to now
```
This forces browsers and any CDN to fetch fresh content.
