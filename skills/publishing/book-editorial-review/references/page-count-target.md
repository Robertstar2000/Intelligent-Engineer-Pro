# Page Count Target Reference

## 6x9" Trade Paperback — Fiction

**CORRECTED Formula (empirically verified 2026-06-19):**
`total_pages = (word_count / 320) + 4`

The old formula `(words / 275) + 6` overestimates by ~15-20%. Empirical data:
- 50,824 words → 158 pages (old formula estimated 190)
- 45,925 words → 162 pages (old formula estimated 173)
- 44,360 words → 151 pages (old formula estimated 166)

The corrected divisor of ~320 words/page accounts for WeasyPrint's actual rendering with 0.375" outside margins, 0.625" gutter, 0.5" top, 0.6" bottom, 10pt font, 1.45 line height.

## Target Ranges

| Pages | Words (corrected) | Status |
|-------|-------------------|--------|
| < 160 | < 50,500 | P0 — Too short, must expand |
| 160-190 | 50,500-60,200 | ✅ In range |
| 190-220 | 60,200-70,000 | ✅ In range |
| 220-275 | 70,000-87,400 | ✅ In range |
| > 275 | > 87,400 | P1 — Over target, trim |

## User Directive (Fiction)

The actual target is 160-190 pages at 6"×9" format = ~50,000-60,000 words. This is the universal target for all full-length fiction books.

## 6x9" Trade Paperback — Business / Non-Fiction

Business and non-fiction books have more structural formatting (headings, bullet lists, tables, callouts, case studies, sidebars) which reduces effective words per page. Use the formula:

`total_pages = (word_count / 325) + 10`

The +10 accounts for additional front/back matter typically required in business books (TOC, foreword, appendix, index, author bio with catalog).

## Target Ranges (Business at 6x9")

| Pages | Words | Status |
|-------|-------|--------|
| < 150 | < 45,500 | P1 — Thin, consider expanding |
| 150-200 | 45,500-61,750 | ✅ Good range for business |
| 200-275 | 61,750-86,125 | ✅ In range for comprehensive books |
| > 275 | > 86,125 | P1 — Over target, trim content |

## Verification Method

To verify page count at any trim and genre:
1. Count words: `wc -w MANUSCRIPT.md` (exclude back matter for accurate count)
2. Apply genre-appropriate formula:
   - Fiction 6×9": (words / 320) + 4
   - Business 6×9": (words / 325) + 10
   - Business 8.5×11": (words / 370) + 8
3. Compare result against 160-275 page target range
4. **Always verify with actual PDF build** — the formula is an estimate; the PDF is ground truth

## Critical Pitfall: Formula Overestimation

The old formula `(words / 275) + 6` consistently overestimates page counts by 15-20%. Always use the corrected formula `(words / 320) + 4` for fiction. When in doubt, build the PDF and check actual page count.

## Pitfall: Back Matter Inflation

When counting words with `wc -w`, the back matter ("Also by", "Thank You", author bio) can add 10,000+ words to the count. These sections don't contribute to page count proportionally. For accurate page estimation, count only the main content (from first chapter header to last chapter content, excluding back matter).

## Pitfall: write_file Token Limits

When expanding large manuscripts, write_file() has an ~8K token limit. For large expansions: (1) Write expansion content to an external .txt file first, (2) Use a Python script to read and apply, (3) Use cat >> for small appends, (4) Verify word count after each expansion.

## Multi-Round Expansion Workflow

When a book is below 160 pages and needs expansion:

1. **Identify shortest chapters** — Split manuscript by chapter headers, count words per chapter, sort ascending
2. **Target chapters below 2,500 words** — These have the most room for expansion
3. **Delegate expansion** — Use subagents to expand 3-5 chapters per round, targeting +800-1,500 words per chapter
4. **Rebuild PDF** — After each round, rebuild and check actual page count
5. **Repeat** — Continue until actual PDF page count ≥ 160
6. **Verify TOC sync** — After each rebuild, verify TOC page numbers match actual chapter locations

**Key insight:** It typically takes 2-3 rounds of expansion to reach 160+ pages. Don't try to do it all in one round — the subagents work better with focused, per-chapter tasks.
