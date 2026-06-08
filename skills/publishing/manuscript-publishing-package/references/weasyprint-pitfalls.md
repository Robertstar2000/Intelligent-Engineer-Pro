# WeasyPrint Pitfalls for Book Manuscripts

> This reference documents rendering issues encountered when generating 6"×9" book PDFs with WeasyPrint from HTML manuscripts. Add to this as new pitfalls emerge.

## 1. Images: Base64 Data URIs

**Pitfall:** WeasyPrint silently skips large base64-encoded images embedded via `<img src="data:image/png;base64,...">`. The PDF renders without error — the images just aren't there.

**Fix:** Use absolute `file://` paths instead:
```html
<img src="file:///home/user/project/images/part1.png" alt="...">
```

**Root cause:** WeasyPrint must keep the entire base64 string in memory. For 5+ images at ~750KB each (base64 makes them ~1MB), the cumulative memory pressure causes WeasyPrint to skip the images silently.

## 2. TOC Page Numbers: Float on Wrapped Text

**Pitfall:** `float: right` on a `::after` pseudo-element generates concatenated page numbers when the TOC entry text wraps to a second line. Example: "Chapter Two: The Echoes of Sputnik and a Family Legacy" shows **"3217"** instead of **"32"**. The right-floated number from the first wrapped line collides with the number from the next entry.

**Wrong approach:**
```css
.toc a::after { content: target-counter(attr(href url), page); float: right; }
```

Also problematic: `position: absolute; right: 0; top: 0` — places the number at the *first* line, not the *last* line of wrapped text.

**Fix:** Use a `<table>` with two columns. The label column takes available width; the page-number column has `width: 1%; white-space: nowrap;`. Each row is independent — wrapping in the label column never affects the page-number column:

```html
<table class="toc-table">
  <tr class="chapter">
    <td class="toc-label">Chapter Two: The Echoes of Sputnik and a Family Legacy</td>
    <td class="toc-page"><a href="#ch2"></a></td>
  </tr>
</table>
```

```css
.toc-table { width: 100%; border-collapse: collapse; }
.toc-table .toc-page {
    text-align: right; white-space: nowrap;
    width: 1%; padding-left: 12px;
}
.toc-table .toc-page a::after { content: target-counter(attr(href url), page); }
```

See `scripts/toc-page-numbers.py` for a full implementation.

## 3. Heading IDs: Truncation

**Pitfall:** Long chapter titles produce truncated auto-generated IDs (e.g., `chapter-fourteen-the-human-ho` instead of `chapter-fourteen-the-human-horizon`). If the `target-counter` href references one truncation but the heading `id` uses another, WeasyPrint logs "target points to undefined anchor" and page numbers silently fail.

**Causes:** Two different scripts or regexes truncated at different lengths, or a regex that captured only the first 30 characters of an ID.

**Fix:** Use a single `_make_id()` function everywhere, with a consistent max length (40 chars is safe). Verify that every `href="#..."` in the TOC has a matching `id="..."` in the document body before rendering:

```python
import re
all_hrefs = set(re.findall(r'href="#([^"]+)"', html))
all_ids = set(re.findall(r'id="([^"]+)"', html))
missing = all_hrefs - all_ids
if missing:
    raise ValueError(f"TOC links without matching headings: {missing}")
```

## 4. Image Resolution vs File Size for Interior Illustrations

**Pitfall:** Over-large image files bloat the PDF without improving quality. A 1024×1024 grayscale PNG at 750KB gives ~293 DPI when displayed at 3.5" width — adequate for print sketches.

**Optimization:**
- Convert grayscale images (`mode='L'`) to JPEG at quality 75 with `optimize=True`:
  ```python
  from PIL import Image
  img = Image.open('source.png').convert('L')
  img.save('output.jpg', 'JPEG', quality=75, optimize=True)
  ```
  Result: ~240KB vs 750KB+ for PNG — same visual quality, 1/3 the size.
- Never upscale below-native resolution expecting quality gain — upscaling doesn't add detail.
- For cover art (full-page, color): use 2,400×3,600 at 400 DPI as specified elsewhere.

## 5. Page-Break Nesting Issues

**Pitfall:** When part dividers and context boxes both use `page-break-before: always` and `page-break-after: always`, nesting them in the wrong HTML parent can push content far downstream. A Part One divider placed inside a Part Two `<div>` lands on page 35 instead of page 5.

**Fix:** Use a flat HTML structure for part dividers and context boxes — do not nest them inside each other:
```html
<div class="part-divider">...</div>    <!-- page break -->
<div class="context-box">...</div>      <!-- page break -->
<h2 class="chapter-title">...</h2>    <!-- page break -->
```

Verify the page order in the PDF by checking that Part One comes before Chapter One, which comes before Part Two. If a later part's heading appears on an unexpectedly high page number, check for nested/unclosed `<div>` tags.

## 6. PDF Verification: Page-by-Page

After rendering, validate chapter-to-page accuracy:

```python
import subprocess
for pg in range(1, 200):  # adjust range
    text = subprocess.run(['pdftotext', '-f', str(pg), '-l', str(pg),
                          'output.pdf', '-'], capture_output=True, text=True)
    first = [l.strip() for l in text.stdout.split('\n') if l.strip()]
    if first and any(first[0].startswith(p) for p in ['Chapter', 'Part ']):
        print(f'Page {pg}: {first[0]}')
```

Cross-reference this output against the TOC page numbers — they should match exactly.

## 7. PDF Page Count vs Chapter Count

WeasyPrint produces PDFs with `\f` (form feed) characters as page separators. Count pages with:
```bash
pdfinfo output.pdf | grep Pages
```

For memoirs, a typical 6"×9" page holds ~2,500–3,500 characters. With front matter + TOC + 16 chapters + back matter, expect:
- ~1,000–1,500 words per page
- 160–200 pages for a ~70K-word manuscript
