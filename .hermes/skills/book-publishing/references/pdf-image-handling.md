# PDF/EPUB Image Handling — Pipeline Fix

> Bug discovered and fixed 2026-06-18 in `hermes_publish/step_pdf.py` and `hermes_publish/step_epub.py`.
> Affects all books with chapter images.

## The Double-Image Bug

**Symptom:** Every chapter image appeared twice in the output PDF/EPUB — once small and left-aligned, once full-width but overflowing the right margin.

**Root cause:** Two independent image insertion paths both fired for every chapter:

1. **Manual insertion** in `step_pdf.py` (line ~79-85) and `step_epub.py` (line ~184-194): inserts `<div class="chapter-image"><img src="...">` for each chapter via `get_bw_image_path()`
2. **Markdown conversion** in `md_to_html_simple()` (utils.py line ~98): converts `![alt](path)` syntax in the manuscript content to `<img src="...">` HTML tags

Both paths produced `<img>` tags pointing to the same file → duplicate images.

## The Fix

### Step 1: Strip markdown image syntax from chapter content

In both `step_pdf.py` and `step_epub.py`, strip markdown image references from the chapter content **before** passing it to `md_to_html_simple()`:

```python
# Strip markdown image syntax — images are inserted manually below
content = re.sub(r'!\[[^\]]*\]\([^)]+\)\s*\n?', '', content)
```

This ensures `md_to_html_simple()` never sees (and converts) markdown images. Only the manually-inserted `<div class="chapter-image">` remains.

### Step 2: Constrain image sizing in CSS (PDF)

The manual image insertion uses the `.chapter-image` CSS class. The original CSS used `width: 100%` which means 100% of the **page** width (6"), ignoring margins — causing overflow.

**Before:**
```css
.chapter-image img { width: 100%; height: auto; max-height: none; }
```

**After:**
```css
.chapter-image img { width: auto; max-width: 100%; height: auto; max-height: 400px; }
```

- `width: auto` — use the image's natural width
- `max-width: 100%` — but never exceed the content area width
- `max-height: 400px` — cap height to prevent tall images from consuming the whole page

### Step 3: Manuscript source files should NOT contain image references

When converting DOCX (or other sources) to MANUSCRIPT.md, strip all image references. The pipeline handles image insertion — the manuscript should only contain text content.

**Conversion rule:** After converting DOCX → markdown, run:
```python
import re
content = re.sub(r'!\[[^\]]*\]\([^)]+\)\s*\n?', '', content)
```

## Verification Checklist

After rebuilding, verify:
```bash
# PDF: count images (should be exactly 1 per chapter with an image)
pdfimages -list output/book.pdf | grep -c "image"

# EPUB: count <img> tags per chapter XHTML (should be exactly 1)
python3 -c "
import zipfile, re
z = zipfile.ZipFile('output/book.epub')
for n in sorted(z.namelist()):
    if n.startswith('OEBPS/ch') and n.endswith('.xhtml'):
        imgs = re.findall(r'<img[^>]+>', z.read(n).decode())
        print(f'{n}: {len(imgs)} images')
"

# Visual check: render a page with an image and verify it's centered and within margins
pdftoppm -png -f 4 -l 4 -r 150 output/book.pdf /tmp/check_page
```

## Affected Files

| File | Change |
|---|---|
| `hermes_publish/step_pdf.py` | Added `import re`, strip markdown images from content, fixed CSS |
| `hermes_publish/step_epub.py` | Strip markdown images from content before `md_to_html_simple()` |
| `hermes_publish/utils.py` | No change needed (the `![...] → <img>` conversion in `md_to_html_simple()` is correct for other use cases) |

## WeasyPrint Image Sizing — CRITICAL

`max-width: 100%` in WeasyPrint does NOT constrain images to the content area as expected. WeasyPrint interprets it relative to the image's intrinsic pixel width, not the CSS content box.

**Symptom:** 600×600px images render at 6.25" wide (600/96dpi) on a 5" content area, overflowing margins.

**Fix:** Use explicit pixel `max-width` in CSS:
```css
.chapter-image img { max-width: 480px; width: auto; height: auto; max-height: 400px; }
```

**Image sizing reference:**
| Image px | At 96dpi | Fits in 5" content? |
|---|---|---|
| 600px | 6.25" | ❌ Overflows |
| 480px | 5.00" | ✅ Exact fit |
| 460px | 4.79" | ✅ With 0.1" buffer |

**Recommendation:** Resize all chapter images to 460px wide before embedding. This provides a small buffer against sub-pixel rounding in WeasyPrint.

**Also required:** Replace relative image paths with absolute `file://` paths before calling WeasyPrint:
```python
html_content = re.sub(r'src="([^"]*)"', lambda m: f'src="file://{os.path.join(images_dir, os.path.basename(m.group(1)))}"', html_content)
```
