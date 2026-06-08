# Page Count Targeting via Typography

When a book's word count doesn't naturally land at the target page range (e.g., 180-200 pages at 6×9in), the single most effective control is **CSS typography density** — adjusting `font-size`, `line-height`, and `@page margin` to spread or pack text per page.

## Density Reference Table (6×9in)

Target: **432 × 648 pts** with comfortable print readability.

| Words | Font | LnHt | Margin | ~Pages | Use Case |
|-------|------|:----:|:------:|:------:|----------|
| 40-45k | 11pt | 1.55 | 0.85in | 185-205 | **Standard novel** — most comfortable reading |
| 45-50k | 10.5pt | 1.45 | 0.75in | 190-210 | **Average novel** — slight density increase |
| 50-55k | 10pt | 1.40 | 0.75in | 195-215 | **Longer manuscript** — moderate density |
| 55-65k | 9.5pt | 1.35 | 0.70in | 195-210 | **Long manuscript** — tighter but still readable |
| 22-25k | 12pt | 1.70 | 1.00in | 180-185 | **Short manuscript** — generous spacing fills pages |
| 25-30k | 11.5pt | 1.65 | 0.95in | 180-195 | **Short-to-medium** — comfortable spread |

**For series with multiple volumes of different lengths**, use per-book CSS density so the one density setting that matches the shortest book also works for the longest. Alternatively, use per-book separate CSS.

## CSS Knobs (by strength)

| Knob | Effect | Range | Notes |
|------|--------|:-----:|-------|
| `font-size` | Strongest | 9pt → 12pt | Each 0.5pt shift ≈ 8-12 page change |
| `line-height` | Strong | 1.3 → 1.7 | Each 0.1 shift ≈ 5-8 page change |
| `@page margin` | Moderate | 0.6in → 1.0in | Each 0.1in ≈ 4-6 page change |
| `p margin` | Weak | 0em → 0.2em | Fine-tuning only |
| `p text-indent` | Negligible | 0.8em → 1.3em | Cosmetic at this scale |

## Implementation

When building review PDFs, pre-calculate density per book:

```python
import os, subprocess

def build_book(title, manuscript_path, output_dir, css_density):
    """css_density: 0.65=loose(short book), 1.0=standard, 1.3=tight(long book)"""
    
    if css_density < 0.8:
        fs, lh, mg = "12pt", 1.70, "1.00in"     # short books: generous
    elif css_density < 1.1:
        fs, lh, mg = "11pt", 1.55, "0.85in"      # standard novels
    else:
        fs, lh, mg = "9.5pt", 1.35, "0.70in"     # long books: tight
    
    # ... build HTML with these CSS values ...
```

## Quick Estimation

```bash
# After first PDF render, calculate words-per-page:
wc -w manuscript.md | awk '{print $1}'   # get word count
pdfinfo output.pdf | grep Pages           # get page count
# wpp = word_count / (page_count - front_matter_pages)
# To estimate: target_wpp = target_pages - front_matter_pages
# Then adjust font-size proportionally: new_fs = current_fs * (current_wpp / target_wpp)
```

## Pitfalls

- **Don't go below 9pt body text** — becomes unreadable in print
- **Don't go above 12pt body text** — looks like large-print edition
- **Line-height below 1.3** makes text look cramped; above 1.7 looks loose and amateur
- **Margins below 0.6in** risk text being cut off by printers (KDP minimum: 0.25in, but 0.5in+ recommended)
- **Always verify with pdfinfo** after rebuilding — the actual page count depends on WeasyPrint's rendering engine and can differ from estimates by 5-10 pages
- **Front matter** (title page, copyright, TOC, about author) adds ~5-8 fixed pages per book regardless of word count