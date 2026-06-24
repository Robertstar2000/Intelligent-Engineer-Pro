# Pipeline Image and TOC CSS Reference

## Chapter Image CSS (step_pdf.py)

```css
.chapter-image { text-align: center; margin: 1em 0; page-break-inside: avoid; }
.chapter-image img { width: auto; max-width: 100%; height: auto; max-height: 400px; }
```

**Why not `width: 100%`?** 100% of the page width (6") exceeds the content area (4.7" after margins). `max-width: 100%` constrains to the content box.

## TOC Page Number CSS (step_pdf.py)

```css
.toc-entry { margin: 0.3em 0; text-indent: 0; font-size: 9.5pt; overflow: hidden; }
.toc-entry .toc-title { border-bottom: 1px dotted #000; display: inline-block; width: 70%; vertical-align: bottom; }
.toc-entry .toc-page-num { float: right; text-decoration: none; color: inherit; }
.toc-entry .toc-page-num::after { content: target-counter(attr(href), page); }
```

**Why not `leader(dotted)`?** WeasyPrint does not support the CSS `leader()` function. Use `border-bottom: 1px dotted` on the title span instead.

**Why a separate `<a>` for the page number?** `target-counter(attr(href), page)` needs the `href` on the same element. The `<a>` holding the page number has `href="#chN"`, and the `::after` pseudo-element resolves the page number from it.

## Content Stripping (step_pdf.py + step_epub.py)

Before passing chapter content to `md_to_html_simple()`, strip:

```python
# 1. Markdown image syntax (pipeline inserts images manually)
content = re.sub(r'!\[[^\]]*\]\([^)]+\)\s*\n?', '', content)

# 2. Chapter heading line (template generates <h3>Chapter N: Title</h3>)
content = re.sub(r'^#{1,2}\s+Chapter\s+\d+\s*[:—\-–]?\s*.*?\n', '', content, count=1)
```

## B&W Image Conversion (utils.py)

All genres convert to B&W. `get_bw_image_path()` returns `images_bw/filename.png` for all books. The `images_bw/` directory is created on first access.

```python
from PIL import Image
img = Image.open(src_path)
bw = img.convert('L')  # 8-bit grayscale
bw.save(str(dst_path), dpi=(300, 300))
```

## Clean Rebuild Checklist

When rebuilding after code changes:
1. Delete old images from `output/` directory (stale color versions may persist)
2. Rebuild PDF: `python3 -c "from hermes_publish.step_pdf import run; ..."`
3. Rebuild EPUB: `python3 -c "from hermes_publish.step_epub import run; ..."`
4. Verify: check image count, B&W mode, no duplicates, TOC page numbers
