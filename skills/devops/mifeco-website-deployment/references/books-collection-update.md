# Updating the Book Collection (BookstoreSection.jsx)

The Browse Our Book Collection section on mifeco.com is rendered by `BookstoreSection.jsx` in the React SPA source at `/mnt/usb_4tb/project-dirs/mifeco_web/mifeco-website/src/components/BookstoreSection.jsx`.

## BOOKS Object Structure

All books are defined in a single `BOOKS` constant object, organized by series:

```js
const BOOKS = {
  business: { title, description, books: [{ title, subtitle, published, kindleUrl, description }] },
  noBlueSky: { ... },
  lunarFoundation: { ... },
  lightships: { ... },
  cindyLou: { ... },    // <-- Cindy Lou Legal Capers
  memoir: { ... },
};
```

Each series object has:
- `title: string` — displayed as section header (e.g., "Cindy Lou Legal Capers Series")
- `description: string` — subtitle text below header
- `books: array` — list of book objects

Each book object has:
- `title: string` — displayed as card title
- `subtitle: string` — displayed below title (e.g., "Cindy Lou Legal Capers, Book 1")
- `published: true` or `false` — controls badge (Published vs Available Soon) and button (Buy on Amazon vs disabled)
- `kindleUrl: amznSearch('Title')` — Amazon search URL for the book. **REQUIRED when `published: true`** — if omitted, the Buy button has no URL.
- `description: string` — 1-2 sentence summary shown on card

## Amazon URL Helper

```js
const amznSearch = (title) =>
  `https://www.amazon.com/s?k=%22Bob+J+Mills%22+%22${encodeURIComponent(title)}%22&i=digital-text`;
```

The `kindleUrl` field should always use this helper: `kindleUrl: amznSearch('Book Title')`. The `encodeURIComponent` is handled by the helper — pass the bare title.

## Count Text

Update the "Search all X books" text near the bottom of the section when the count changes:

```js
<p className="text-gray-500 text-sm">
  Can't find a title? Search all 20 books by Bob J Mills on Amazon:
</p>
```

Count = sum of all books with `published: true` across all series.

## Rendering

Each series must be rendered in `BookSeriesSection` calls inside the component return:

```jsx
<BookSeriesSection series={BOOKS.business} />
<BookSeriesSection series={BOOKS.noBlueSky} />
<BookSeriesSection series={BOOKS.lunarFoundation} />
<BookSeriesSection series={BOOKS.lightships} />
<BookSeriesSection series={BOOKS.cindyLou} />
<BookSeriesSection series={BOOKS.memoir} />
```

New series must be added here AND to the BOOKS object. Order in the rendering list = display order on the page.

## Build and Deploy

After editing `BookstoreSection.jsx`:

```bash
cd /mnt/usb_4tb/project-dirs/mifeco_web/mifeco-website
npm run build
```

Deploy only the `dist/assets/` directory (JS + CSS + images) to DreamHost:

```python
import pexpect
child = pexpect.spawn(
    'rsync -avz --delete /mnt/usb_4tb/project-dirs/mifeco_web/mifeco-website/dist/assets/ dh_mwpxuu@mifeco.com:/home/dh_mwpxuu/mifeco.com/assets/',
    timeout=60, encoding='utf-8')
child.expect('password:', timeout=30)
child.sendline('Rm2214ri####')
child.expect(pexpect.EOF, timeout=60)
```

Notes:
- Use `--delete` to clean up old hash-named bundles (they accumulate on every rebuild)
- **CRITICAL: MUST also sync `dist/index.html`** every time you deploy assets. The index.html references hashed bundle filenames that change on every build. If you only sync assets/, the HTML on the server still points to the old (now-deleted) filenames → blank page.
- Correct two-file deploy:
  ```python
  child = pexpect.spawn(
      'rsync -avz --delete /mnt/usb_4tb/project-dirs/mifeco_web/mifeco-website/dist/assets/ dh_mwpxuu@mifeco.com:/home/dh_mwpxuu/mifeco.com/assets/ && rsync -avz /mnt/usb_4tb/project-dirs/mifeco_web/mifeco-website/dist/index.html dh_mwpxuu@mifeco.com:/home/dh_mwpxuu/mifeco.com/index.html',
      timeout=60, encoding='utf-8')

## Verification

SSH to DreamHost and grep the live JS for your changes:

```python
import pexpect
child = pexpect.spawn(
    'ssh dh_mwpxuu@mifeco.com "grep -o \'Book Title\\|Series Name\\|20 books\' /home/dh_mwpxuu/mifeco.com/assets/index-*.js"',
    timeout=30, encoding='utf-8')
child.expect('password:', timeout=15)
child.sendline('Rm2214ri####')
child.expect(pexpect.EOF, timeout=30)
print(child.before)  # Should show all the new/changed text
```

## Common Pitfalls

- **Old bundles persist** — `--delete` in rsync handles this, but verify old hashes are gone
- **Published status mismatch** — the admin pipeline (`unified-pipeline.json`) lists 20 books across 6 series. The SPA must match. Check both when adding new books.
- **Amazon URLs** — always use `amznSearch()`. Do NOT hardcode URLs or use a different format.
- **JSX escaping** — single quotes in titles/descriptions (e.g., "Owner's Manual") need backslash-escaping in JSX source: `Owner\\'s Manual`
- **Published vs Available Soon** — `published: true` shows green "Published" badge + orange "Buy on Amazon Kindle" button. `published: false` shows amber "Available Soon" badge + disabled button. When a book goes from unpublished to published, you must: (1) change `published: false` → `true`, (2) ADD `kindleUrl: amznSearch('...')`, (3) update the "X books" count.

## Current Book Inventory (as of 2026-06-09)

| Series | Books | Published |
|--------|:-----:|:---------:|
| Business Books | 3 | ✅ All |
| No Blue Sky | 5 | ✅ All |
| Lunar Foundation | 4 | ✅ All |
| Age of Lightships | 4 | ✅ All |
| Cindy Lou Legal Capers | 3 | ✅ All |
| Memoir | 1 | ✅ All |
| **Total** | **20** | **20/20** |