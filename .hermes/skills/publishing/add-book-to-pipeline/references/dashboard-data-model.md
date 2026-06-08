# Pipeline Dashboard Data Model Reference

## File: `~/.hermes/pipeline-engine/dashboard/pipeline-dashboard.html`

### Key JS Data Structures

**`booksCatalog` array** (~line 983):
```javascript
const booksCatalog = [
  { title:'Book Title', series:'Series Name', status:'published'|'draft', asin:'BXXXXXXXXXX', flags:'⚠ or ✅ message' },
];
```
- `status`: `"published"` shows "Buy on Kindle" button with ASIN link; `"draft"` shows "Coming Soon" badge
- `flags`: optional, displayed with warning (⚠) or success (✅) color
- `asin`: Amazon ASIN, only present for published books with known ASIN

**Static counters** (search for these strings to update):
- `id="totalBooks"` — hardcoded book count number (NOT dynamic). Update manually.
- Section badge format: `"N titles · N series · N published · N draft"` (in `<span class="section-badge">`)
- `latestProject` string: same format + "Active fixes needed"
- `tags` array: `['N titles', 'N published', 'draft info', 'N need fixes']`

### Complete File Sync List for Bulk Status Updates
1. `data/pipeline-books.json` — status, published_date per book
2. `dashboard/pipeline-books.json` — copy of #1
3. `dashboard/pipeline-dashboard.html` — booksCatalog, counters, badges, tags
4. `sequences/books-nurture.json` — Day 1 email catalog listing
5. `~/books/book_catalog.json` — status, asin, published_date per book
