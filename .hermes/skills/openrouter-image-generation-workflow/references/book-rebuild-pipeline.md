# Book Rebuild Pipeline — HTML → PDF → EPUB → KDP

After generating or regenerating chapter images, rebuild all three output formats (HTML, PDF, EPUB) and sync to KDP_Package.

## Pipeline Steps

### 1. Copy New Images to Output Folders

```bash
BASE="/mnt/usb_4tb/books/No_Blue_Sky_Series"
for book in Book_1_Built_from_Dust Book_2_The_Oxygen_Gamble ...; do
  cp -f "$BASE/$book/images"/*.png "$BASE/$book/output/"
done
```

### 2. Fix Duplicate Image References in HTML

Book HTML files contain **two** `<img>` tags per chapter — one in a `<div class="chapter-image">` (keep) and one in a `<p>` tag (duplicate — remove):

```python
with open(html_path, "r") as f:
    content = f.read()
content = re.sub(r'\s*<p><img src="chapter_images/[^"]*" alt=""\s*/>\s*', '\n', content)
content = re.sub(r'\s*<p><img src="[^"]*" alt=""\s*/>\s*', '\n', content)
with open(html_path, "w") as f:
    f.write(content)
```

### 3. Rebuild PDF via WeasyPrint

**⚠️ Data URIs (base64) do NOT work with WeasyPrint.** Use absolute file paths:

```python
from weasyprint import HTML
import re, os

with open(html_path, "r") as f:
    html_content = f.read()

def make_absolute(match):
    src = match.group(1)
    abs_path = os.path.join(images_dir, os.path.basename(src))
    return f'src="file://{abs_path}"'

html_content = re.sub(r'src="([^"]*)"', make_absolute, html_content)
tmp_html = html_path + ".tmp"
with open(tmp_html, "w") as f:
    f.write(html_content)

HTML(filename=tmp_html, base_url=images_dir).write_pdf(pdf_path)
os.remove(tmp_html)
```

### 4. Rebuild EPUB

**⚠️ OPF manifest requires UNIQUE `id` attributes** across ALL items. Use `id="ch01"` for chapter XHTML and `id="img-ch01"` for images.

**Spine must reference ALL chapters** — not just ch01.

**nav.xhtml must use actual chapter titles** (e.g., "Chapter 1: The Descent Window"), not generic "Chapter 1" labels. Extract titles from `<h3>` headings in the HTML.

**TOC page must be a standalone `toc.xhtml`** — not embedded in `front.xhtml`. The HTML has `<div class="toc-page">` which must be extracted into its own spine item between front matter and chapters. The nav.xhtml should include a link to this TOC page.

```
EPUB spine order: front.xhtml → toc.xhtml → ch01.xhtml → ch02.xhtml → ...
```

```python
# Correct OPF pattern:
manifest_items.append(f'    <item id="ch{ch_num:02d}" href="ch{ch_num:02d}.xhtml" media-type="application/xhtml+xml"/>')
manifest_items.append(f'    <item id="img-ch{ch_num:02d}" href="images/ch{ch_num:02d}.png" media-type="image/png"/>')
spine_items.append(f'    <itemref idref="ch{ch_num:02d}"/>')

# TOC extraction from HTML:
toc_start = html_content.find('<div class="toc-page">')
toc_end = html_content.find('</div>', toc_start) + len('</div>')
toc_content = html_content[toc_start:toc_end].strip()

# Chapter XHTML image refs must use images/ path, not bare filename:
sec_content_fixed = re.sub(r'src="ch(\d+\.png)"', r'src="images/ch\1"', sec_content)

# nav.xhtml — use actual chapter titles extracted from <h3> headings:
h3_match = re.search(r'<h3[^>]*>(.*?)</h3>', section, re.DOTALL)
title = re.sub(r'<[^>]+>', '', h3_match.group(1)).strip()
nav_items.append(f'    <li><a href="{sec_id}.xhtml">{title}</a></li>')
```

Chapter XHTML files must be proper XHTML documents (DOCTYPE + html wrapper), not raw body content.

**Image path fix in chapter XHTML:** The HTML has `src="ch01.png"` (bare filename) but EPUB chapters need `src="images/ch01.png"` (relative to OEBPS/). Always run this regex before writing chapter XHTML:
```python
sec_content = re.sub(r'src="ch(\d+\.png)"', r'src="images/ch\1"', sec_content)
```

**front.xhtml contains the full HTML document** (title page + copyright + TOC) because everything before the first `<div class="chapter">` is grouped together. This is valid EPUB but the TOC should be extracted into its own `toc.xhtml` for proper reader navigation.

### 5. Copy to KDP_Package

```python
kdp_dir = f"{base}/{book_dir}/KDP_Package"
shutil.copy2(pdf_path, f"{kdp_dir}/Print/{pdf_name}")
shutil.copy2(epub_path, f"{kdp_dir}/Kindle/{epub_name}")
```

## No Blue Sky Folder Structure

```
Book_N_Title/
├── images/chXX.png          ← source of truth (generate here)
├── images_bw/chXX.png       ← greyscale variant
├── output/
│   ├── chXX.png             ← copy from images/ for HTML/EPUB/PDF
│   ├── *_print.html         ← HTML with image references
│   ├── *_final.pdf          ← rebuilt PDF
│   └── No_Blue_Sky_N_*.epub ← rebuilt EPUB
├── manuscript/MANUSCRIPT.md  ← chapter headers
└── KDP_Package/
    ├── Print/*_final.pdf     ← copy of rebuilt PDF
    └── Kindle/*.epub         ← copy of rebuilt EPUB
```

## Chapter Header Formats by Book

| Book | Header Format |
|------|--------------|
| Book 1 (Built from Dust) | `## Chapter N — Title` (double hash) |
| Book 2 (The Oxygen Gamble) | `## Chapter N — Title` (double hash) |
| Book 3 (Rivers Under Mars) | `# Chapter N — Title` (single hash) |
| Book 4 (The Red Charter) | `# Chapter N — Title` (single hash) |
| Book 5 (The First Martian Nation) | `# Chapter N -- Title` (single hash, double dash) |

Some chapters have `.5` suffix (e.g., `Chapter 9.5`) — treat as separate chapters with their own image.
