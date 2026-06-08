# Vite SPA Component Patterns for mifeco.com

This file documents the component patterns used in the mifeco.com Vite React SPA for future modifications.

## BookstoreSection Component

Location: `mifeco-website/src/components/BookstoreSection.jsx`

### Structure (as of May 30, 2026)
The BookstoreSection defines books as a JS data structure grouped into series categories:
- `BOOKS.business` — 3 books (The Owner's Manual for AI Agents, AI That Works for Small Business, The Crisis Ready Company) — all published
- `BOOKS.noBlueSky` — 5 books (Built from Dust through The First Martian Nation) — all published
- `BOOKS.lunarFoundation` — 4 books (Moon Rock through Waters Horizon) — all published
- `BOOKS.lightships` — 4 books (Sunward Exodus through The Last Photon Fleet) — **published: false** (awaiting Amazon publication)
- `BOOKS.memoir` — 1 book (Tomorrow Remembered) — published

### Per-book fields
```js
{
  title: "Book Title",
  subtitle: "Series subtitle or tagline",
  published: true,         // or false
  kindleUrl: "https://...", // Amazon URL — search or direct ASIN
  description: "Short description for the card"
}
```

### Published vs. Available Soon
- `published: true` → Green "Published" badge + orange "Buy on Amazon Kindle" button linking to `kindleUrl`
- `published: false` → Amber "Available Soon" badge + disabled grey button

### Amazon URL Strategy (IMPORTANT)
**No confirmed ASIN:** Use Amazon search URL pattern:
```js
const amznSearch = (title) =>
  `https://www.amazon.com/s?k=%22Bob+J+Mills%22+%22${encodeURIComponent(title)}%22&i=digital-text`;
```
This searches Kindle Store for `"Bob J Mills" + "[title]"` — reliably surfaces the correct book.

**Confirmed ASIN:** Use direct link: `https://www.amazon.com/dp/B0XXXXXXXX`

**Author page link** (used in "View All Books" button and header):
```js
const AMAZON_AUTHOR = 'https://www.amazon.com/s?k=%22Bob+J+Mills%22&i=digital-text';
```

### Adding a New Series
1. Add a new key to the `BOOKS` object with `{ title, description, books: [...] }`
2. Add a `<BookSeriesSection series={BOOKS.newSeries} />` in the component JSX
3. Set `published: true/false` per book
4. For published books, provide `kindleUrl` (use `amznSearch()` helper if no ASIN)

### Import in App.jsx
```jsx
import BookstoreSection from './components/BookstoreSection';
// Insert in JSX: <BookstoreSection />
```

## Build & Deploy Quick Reference

```bash
cd ~/mifeco_web/mifeco-website

# Build (prefer npm if pnpm blocks builds)
rm -rf node_modules pnpm-lock.yaml
npm install --legacy-peer-deps
npx vite build
```

### Deploy via rsync (CRITICAL)
```
Use within execute_code() — NOT terminal()
⚠️ NEVER use --delete — WordPress co-located in web root
⚠️ Password is DreamHost panel password, NOT $SUDO_PASS
⚠️ First: ssh-keygen -R 'iad1-shared-b8-42.dreamhost.com'
```
Python pexpect pattern:
```python
import pexpect, time
host = "iad1-shared-b8-42.dreamhost.com"
user = "dh_mwpxuu"
dist = "~/mifeco_web/mifeco-website/dist/"
target = f"{user}@{host}:/home/dh_mwpxuu/mifeco.com/"
ts = time.strftime("%Y%m%d%H%M%S")

# Backup first, then rsync dist/ (no --delete)
```

### File Inventory
- `index.html`, `vite.svg`, `assets/index-XXX.js`, `assets/index-XXX.css`, `.htaccess`
- WordPress: `wp-admin/`, `wp-includes/`, `wp-content/` — NEVER DELETE
- 17 files typical transfer for a build

## SoftwareSection Component

Location: `mifeco-website/src/components/SoftwareSection.jsx`

### Structure
The SoftwareSection now shows 3 real MIFECO SaaS apps, not the generic Researcher/Hyperion/Engineering Assistant:

```js
const SAAS_APPS = [
  {
    id: 'hypatia',
    name: 'Project Hypatia Pro',
    subtitle: 'AI-Powered Engineering & Project Management',
    icon: <Rocket className="w-8 h-8" />,
    color: 'from-purple-600 to-pink-500',
    bgColor: 'bg-purple-50',
    appUrl: 'https://project-hypatia-pro-1064319572465.us-west1.run.app',
  },
  // ... PM Accelerator, VibraEngineer
];
```

Each app points to its Cloud Run URL. Original Stripe checkout / purchase flow was removed since these are browser-hosted apps (no download needed).

## Navigation Updates

When adding a new section:
1. Add a nav link in both desktop nav (`<nav className="hidden md:flex...">`) and mobile nav (`<div className="md:hidden...">`)
2. Use `href="#sectionname"` for scroll-to-section behavior
3. Desktop nav lists nav links as `<a>` tags inside `<nav>`. The "Industries" dropdown is a `<button>` inside a `<div className="relative">` — preserve this structure when inserting new links between Services and Industries.

## Key Imports

| Component | File | Import path |
|-----------|------|-------------|
| BookstoreSection | `src/components/BookstoreSection.jsx` | `./components/BookstoreSection` |
| SoftwareSection | `src/components/SoftwareSection.jsx` | `./components/SoftwareSection` |
| Card, Badge, Button | shadcn/ui | `./components/ui/card`, etc. |

## Build & Deploy Quick Reference

```bash
cd ~/mifeco_web/mifeco-website

# Build (prefer npm if pnpm blocks builds)
rm -rf node_modules pnpm-lock.yaml
npm install --legacy-peer-deps
npx vite build

# Deploy via rsync (within execute_code(), not terminal())
# rsync -avz --rsh="ssh -o StrictHostKeyChecking=accept-new" dist/ dh_mwpxuu@host:/home/dh_mwpxuu/mifeco.com/
# ⚠️ NEVER use --delete — WordPress co-located in web root
```
