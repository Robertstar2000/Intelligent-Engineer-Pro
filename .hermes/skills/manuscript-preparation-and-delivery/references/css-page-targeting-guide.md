# CSS Page-Targeting Guide

For 6×9in books, use these CSS settings to hit specific page counts. Build-and-verify — calculations are approximate.

## Settings Table (Georgia serif, 6×9in, word counts are rough)

| Font | Line-Height | Margins | Words/Page | 40k words → | 50k words → | 62k words → |
|------|-------------|---------|:----------:|:-----------:|:-----------:|:-----------:|
| 11pt | 1.55        | 0.85in  | ~205       | 195+5=200   | 244+5=249   | 302+5=307   |
| 10.5pt| 1.45       | 0.75in  | ~240       | 167+5=172   | 208+5=213   | 258+5=263   |
| 10pt  | 1.4        | 0.75in  | ~270       | 148+5=153   | 185+5=190   | 230+5=235   |
| 9.5pt | 1.35       | 0.7in   | ~310       | 129+5=134   | 161+5=166   | 200+5=205   |

"+5" = roughly 5 pages for front matter (title, copyright, TOC).

## Quick Rules of Thumb

- **40k words**: use 11pt comfortable → ~200 pages ✓
- **50k words**: use 10.5pt moderate → ~213 pages (close)
- **62k words**: use 9.5pt tight → ~197 pages ✓
- **70k+ words**: won't fit in 200 pages at any readable size — split the book instead.

## Verification

After building the PDF, always check:
```bash
pdfinfo book.pdf | grep -E 'Pages|Page size'
```
Page size must be **432 × 648 pts** (= 6×9in). If you see 595×842 (A4), the `@page` CSS was stripped or invalid — check for special characters in the CSS value.

If page count is off by >10%, adjust line-height by ±0.05 and rebuild. Each ±0.05 of line-height changes page count by ~3-5%.