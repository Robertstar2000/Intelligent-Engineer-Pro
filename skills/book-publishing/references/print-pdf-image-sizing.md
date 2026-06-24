# Print PDF Image & Table Sizing for 6"×9" Books

WeasyPrint renders images at CSS reference **96 DPI**, NOT at the image's embedded DPI metadata:

```
width_in_inches = width_in_px / 96
```

## KDP Margin Rules (2026-07-20)

KDP requires minimum margins based on page count. The gutter is the binding-side margin (left for odd pages, right for even pages).

| Page Count | Gutter (inside) | Outside | Top | Bottom |
|---|---|---|---|---|
| < 200 pages | **0.5"** | 0.25" | 0.25" | 0.25" |
| 200–299 pages | 0.5" | 0.25" | 0.25" | 0.25" |
| 300+ pages | 0.625" | 0.25" | 0.25" | 0.25" |

> ⚠️ **KDP rejection:** "Insufficient gutter" — books with 158+ pages require at least 0.5" gutter AND at least 0.25" for outside/top/bottom. Books under 200 pages also need 0.5" gutter (NOT 0.375").

### Recommended: 0.5" all around

For simplicity and safety, use `margin: 0.5in 0.5in 0.5in 0.5in` (top right bottom left) for all books. This meets KDP minimums and gives a 5" content area on a 6" page.

### Content Area Math (6"×9" book, 0.5" margins)

```
page_width           = 6.00"
- left margin        = 0.50"
- right margin       = 0.50"
content_width        = 5.00" = 480px at 96dpi
```

## Image Sizing

### Critical: WeasyPrint max-width:100% Pitfall

`max-width: 100%` in WeasyPrint is **relative to the image's intrinsic size**, NOT the container. A 600px image with `max-width: 100%` still renders at 600px = 6.25" wide, which overflows the 5" content area.

**Fix:** Use explicit `max-width` in pixels, not percent:

```css
.chapter-image img { max-width: 480px; width: auto; height: auto; max-height: 400px; }
```

### Target Image Size

Resize all chapter images to **460px wide** (aspect ratio preserved):

```
460px ÷ 96 = 4.79"  → fits with 0.1" buffer on each side
```

### One-Liner (PIL)

```python
from PIL import Image
img = Image.open(path)
ratio = 460 / img.width
new_w, new_h = 460, int(img.height * ratio)
img.resize((new_w, new_h), Image.LANCZOS).save(path, dpi=(150, 150))
```

### Directory Checklist

Resize images in BOTH:
- `images/` (source for future rebuilds)
- `output/` (copies used by the PDF build)

## Paragraph and Element Margins

**Critical:** The `<p>` tag margin adds to page margins. If `@page` has 0.5" margins and `p { margin: 0.5in }`, the effective content offset is 1.0" from page edge, causing images to overflow.

```css
/* CORRECT: no extra margin on p */
p { text-indent: 1.5em; margin: 0; orphans: 2; widows: 2; }

/* WRONG: doubles the margin */
p { text-indent: 1.5em; margin: 0.5in; orphans: 2; widows: 2; }
```

Same applies to `.chapter-image` — use `margin: 0; padding: 0;` (NOT 0.5in margins).

## Table Sizing

```css
table { max-width: 100%; width: 100%; border-collapse: collapse;
    margin: 1em 0; font-size: 8.5pt; page-break-inside: avoid; }
th, td { border: 1px solid #999; padding: 4px 6px;
    text-align: left; vertical-align: top; word-wrap: break-word;
    overflow-wrap: break-word; }
```

## Verification

After rebuilding, verify images are within margins:

```python
import fitz
doc = fitz.open('output/book.pdf')
margins = {'left': 36, 'right': 396, 'top': 36, 'bottom': 612}  # 0.5in in points
for page_num in range(1, len(doc)+1):
    page = doc[page_num - 1]
    for img in page.get_images(full=True):
        for rect in page.get_image_rects(img[0]):
            assert rect.x0 >= margins['left'] - 1
            assert rect.x1 <= margins['right'] + 1
```
