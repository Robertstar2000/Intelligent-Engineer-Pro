# Pipeline File Map

When updating book status or catalog data, these are ALL the files that must be touched.

## Canonical Data Files (Source of Truth)

| File | Purpose | Format |
|------|---------|--------|
| `~/.hermes/pipeline-engine/data/pipeline-books.json` | Master book catalog with status, ASINs, prices, leads | JSON |
| `~/.hermes/pipeline-engine/data/social-content-books.json` | Social media post copy per book | JSON |
| `~/books/book_catalog.json` | Per-book metadata (chapters, words, epubs, status) | JSON |

## Dashboard Files (Served to Browser)

| File | Purpose | Sync Source |
|------|---------|-------------|
| `~/.hermes/pipeline-engine/dashboard/pipeline-books.json` | **Separate copy** — dashboard reads this | `cp` from data/pipeline-books.json |
| `~/.hermes/pipeline-engine/dashboard/pipeline-dashboard.html` | Main dashboard with `booksCatalog` JS array, static counts, badges | Edit directly |
| `~/.hermes/pipeline-engine/dashboard/pipeline-state.json` | Pipeline health/stage tracking (not per-book status) | Edit directly if needed |

## Email Sequence Files

| File | Purpose |
|------|---------|
| `~/.hermes/pipeline-engine/sequences/books-nurture.json` | 14-day email nurture sequence — Day 1 welcome email has full catalog listing |

## Sync Rule

After editing `data/pipeline-books.json`, ALWAYS run:
```bash
cp ~/.hermes/pipeline-engine/data/pipeline-books.json \
   ~/.hermes/pipeline-engine/dashboard/pipeline-books.json
```

The dashboard does NOT read from the data directory — it reads from its own copy.
