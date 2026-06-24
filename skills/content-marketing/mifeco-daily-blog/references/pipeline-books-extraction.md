# Pipeline Books JSON Extraction

The file `~/.hermes/pipeline-engine/data/pipeline-books.json` has a deeply nested structure. Books are scattered across multiple JSON paths under `products`:

## JSON Paths to Published Books

| Path | Series | Count | Status |
|------|--------|-------|--------|
| `products.titles[]` | No Blue Sky | 5 | All published |
| `products.moon_books.titles[]` | Lunar Foundation | 4 | All published |
| `products.age_of_lightships.titles[]` | Age of Lightships | 4 | All published |
| `products.cindy_lou.titles[]` | Cindy Lou Legal Capers | 3 | All **draft** — skip |
| `products.standalone[]` | (Standalone) | 1 | Published |
| `products.business_books.titles[]` | Business | 3 | All published |

**Total published**: 17 (5 + 4 + 4 + 1 + 3)

## Python Extraction Snippet

Use this in a `python3 << 'PYEOF'` heredoc to extract all published books:

```python
import json

with open('/home/bob/.hermes/pipeline-engine/data/pipeline-books.json') as f:
    data = json.load(f)

p = data['pipeline']['products']
published = []

# No Blue Sky
for book in p.get('titles', []):
    if book.get('status') == 'published':
        published.append({**book, 'series': 'No Blue Sky'})

# Lunar Foundation
for book in p.get('moon_books', {}).get('titles', []):
    if book.get('status') == 'published':
        published.append({**book, 'series': 'Lunar Foundation'})

# Age of Lightships
for book in p.get('age_of_lightships', {}).get('titles', []):
    if book.get('status') == 'published':
        published.append({**book, 'series': 'Age of Lightships'})

# Standalone (array, not nested under titles)
for book in p.get('standalone', []):
    if book.get('status') == 'published':
        published.append({**book, 'series': 'Standalone'})

# Business books
for book in p.get('business_books', {}).get('titles', []):
    if book.get('status') == 'published':
        published.append({**book, 'series': 'Business'})

# Cindy Lou Legal Capers — all draft, skip

print(f"Found {len(published)} published books")
for b in published:
    print(f"  {b['title']} ({b['series']}) — ASIN: {b.get('asin', 'N/A')}")
```

## Book B Selection (mifeco.com/books)

Book B must be from a **different series/genre** than Book A. The series/genre mapping:

| Series | Genre |
|--------|-------|
| No Blue Sky | Sci-Fi (Mars colonization) |
| Lunar Foundation | Sci-Fi (Moon settlement) |
| Age of Lightships | Sci-Fi (Space opera) |
| Cindy Lou Legal Capers | Cozy mystery |
| Business | Business / Non-fiction |
| Standalone (Tomorrow Remembered) | Memoir |

**Note**: No Blue Sky, Lunar Foundation, and Age of Lightships are all sci-fi but are different *series* — the skill requires a different series/genre, so cross-sci-fi comparisons (e.g., No Blue Sky vs Age of Lightships) are valid as long as the series differ.

## Cindy Lou Edge Case

Cindy Lou Legal Capers titles are `status: "draft"` in pipeline data (no ASIN) but ARE listed on mifeco.com/books. When using them as Book B:
- Use MIFECO books page links as CTAs instead of Amazon links
- They are valid Book B targets (different genre from all sci-fi books)