---
name: nbs-book-rebuild
description: Rebuild book series — images, HTML, PDF, EPUB with KDP-compliant structure
version: 1.2.0
---

# Book Rebuild — KDP-Compliant EPUB/PDF

## Directory Structure
Each book lives at `/mnt/usb_4tb/books/<Series_Name>/Book_N_Title/` with:
- `images/` or `chapter_images/` — source PNG images (ch01.png, ch02.png, etc.)
- `output/` — HTML, PDF, EPUB output files
- `KDP_Package/Print/` — final PDF for KDP
- `KDP_Package/Kindle/` — final EPUB for KDP

## Image Generation (Sci-Fi Pencil Sketches)
- Use Gemini Flash Image API via Google AI Studio direct API
- Prompt: "Black and white pencil sketch illustration for a science fiction novel. [Scene]. Mars must look like real Mars: reddish-brown regolith, craters, thin pale pink sky. Astronauts must wear modern SpaceX-style suits: sleek form-fitting, angular helmets. Style: detailed pencil sketch, cross-hatching, no color."
- **CRITICAL**: After generation, convert all images to grayscale:
  ```python
  gray = img.convert('L')
  gray_rgb = gray.convert('RGB')
  gray_rgb.save(path, 'PNG', optimize=True)
  ```
  Gemini outputs warm-tinted images despite B&W prompts.
- Rate limit: 6 seconds between API calls
- Image size: 600x600 pixels

## HTML Fix (Before Rebuild)
The HTML has duplicate image references — each chapter has both:
```html
<div class="chapter-image"><img src="ch01.png" alt="Chapter 1" /></div>
<p><img src="chapter_images/ch01.png" alt="" /></p>
```
Remove the `<p><img .../></p>` duplicates, keeping only the `chapter-image` div.

## EPUB Build — KDP Compliance (CRITICAL)

See `references/kdp-epub-compliance.md` for the full authoritative checklist.

### Quick Summary
1. **`toc.ncx`** — must exist, be declared in OPF manifest, spine must have `toc="ncx"`
2. **`nav.xhtml`** — must have `epub:type="toc"` AND `epub:type="landmarks"` navs with `bodymatter` landmark
3. **Spine** — must include front matter (title page, TOC page) BEFORE chapters; must NOT contain image itemrefs
4. **Chapter titles** — extract from `<h1>`/`<h2>` in body, NOT from filename; clean duplicate prefixes
5. **Named entities** — XHTML files must use numeric entities only (`&#8212;` not `&mdash;`)
6. **XML validity** — all XHTML must parse cleanly with `xml.etree.ElementTree`

### Common Pitfalls
- **front.xhtml not in spine**: The title/TOC page must have an `<itemref>` in the spine or it's unreachable
- **Broken spine with image refs**: Source EPUBs (notably Age of Lightships) may have spines containing image itemrefs and only ch01–ch09. Rebuild spine from manifest. See `references/epub-spine-rebuild.md`
- **Duplicate "Chapter N:" prefix**: Source files may have `Chapter 1: Chapter 1 — Title`, `Chapter 1: Chapter 1: Title`, or `Chapter N: Chapter M: Title` (N≠M, from renumbering). Apply regex fix to ALL .xhtml, .ncx, .opf files. See `references/epub-spine-rebuild.md`
- **Missing bodymatter landmark**: AL books often lack `epub:type="landmarks"` with bodymatter. Auto-detect and add. See `references/epub-spine-rebuild.md`
- **Orphan `</div>` tags**: Chapter files from PDF extraction pipelines often have unbalanced divs; use tag-stacking logic to repair (see `references/epub-div-fix.md`)
- **Named entities in XHTML**: `&mdash;`, `&ldquo;`, `&rdquo;` etc. break XML parsing; replace with numeric equivalents (`&#8212;`, `&#8220;`, `&#8221;`)
- **Nested XML declarations**: `front.xhtml` extracted from PDF pipelines may contain nested `<?xml ...>` declarations; rewrite as a single clean XHTML document

## Image Compression for KDP

When images are too large for KDP (e.g., 1024x1024 PNG at ~2MB each), compress before inserting:

```python
from PIL import Image

def compress_image(input_path, output_path, target_dpi=200, quality=85, max_dim=800):
    img = Image.open(input_path)
    if img.mode in ('RGBA', 'P'):
        img = img.convert('RGB')
    w, h = img.size
    if w > max_dim or h > max_dim:
        ratio = max_dim / max(w, h)
        img = img.resize((int(w*ratio), int(h*ratio)), Image.LANCZOS)
    img.save(output_path, 'JPEG', dpi=(target_dpi, target_dpi), quality=quality, optimize=True)
    return os.path.getsize(output_path)
```

- **Target**: 200 DPI, JPEG quality 85, max 800px on longest side
- **Typical reduction**: 85-92%
- Save compressed images to `chapter_images_compressed/` directory
- When replacing .png with .jpg in EPUBs, update OPF manifest href, HTML img src, AND file extension

## Image Update Workflow (Date-Based)

When chapter_images have been regenerated and EPUB/PDF files need updating:

### Step 1: Compare file dates
```python
import os
from datetime import datetime

# Get latest image date
latest_img = max(os.path.getmtime(os.path.join(chapter_images_dir, f))
                 for f in os.listdir(chapter_images_dir)
                 if f.endswith(('.png', '.jpg')))

# Check if EPUB/PDF is older
epub_mtime = os.path.getmtime(epub_path)
if latest_img > epub_mtime:
    needs_update = True
```

### Step 2: Update EPUB images (zipfile method)
```python
import zipfile, os, re, shutil

def update_epub_images(epub_path, chapter_images_dir):
    """Replace images in EPUB with latest from chapter_images"""
    # Build sorted chapter image list
    ch_files = sorted([(int(re.match(r'ch(\d+)', f, re.IGNORECASE).group(1)), f)
                       for f in os.listdir(chapter_images_dir)
                       if re.match(r'ch(\d+)', f, re.IGNORECASE)])
    
    temp_path = epub_path + ".tmp"
    with zipfile.ZipFile(epub_path, 'r') as zin:
        with zipfile.ZipFile(temp_path, 'w', zipfile.ZIP_DEFLATED) as zout:
            for item in zin.infolist():
                data = zin.read(item.filename)
                # Replace images in OEBPS/images/
                if item.filename.startswith('OEBPS/images/'):
                    basename = os.path.basename(item.filename)
                    match = re.match(r'ch(\d+)', basename, re.IGNORECASE)
                    if match:
                        ch_num = int(match.group(1))
                        if ch_num in [c[0] for c in ch_files]:
                            idx = [c[0] for c in ch_files].index(ch_num)
                            _, ch_filename = ch_files[idx]
                            with open(os.path.join(chapter_images_dir, ch_filename), 'rb') as f:
                                data = f.read()
                zout.writestr(item, data)
    shutil.move(temp_path, epub_path)
```

### Step 3: Update PDF images (PyMuPDF method)
```python
import fitz, os, re

def update_pdf_images(pdf_path, chapter_images_dir):
    """Replace images in PDF with latest from chapter_images"""
    ch_files = sorted([(int(re.match(r'ch(\d+)', f, re.IGNORECASE).group(1)), f)
                       for f in os.listdir(chapter_images_dir)
                       if re.match(r'ch(\d+)', f, re.IGNORECASE)])
    
    output_path = pdf_path.replace('.pdf', '_updated.pdf')
    doc = fitz.open(pdf_path)
    img_index = 0
    
    for page in doc:
        imgs = page.get_images(full=True)
        for img in imgs:
            if img_index < len(ch_files):
                ch_num, ch_filename = ch_files[img_index]
                ch_path = os.path.join(chapter_images_dir, ch_filename)
                with open(ch_path, 'rb') as f:
                    page.replace_image(img[0], stream=f.read())
                img_index += 1
    
    doc.save(output_path)
    doc.close()
    return output_path
```

**CRITICAL**: `replace_image()` is a **Page** method, not a Document method. Use `page.replace_image(xref, stream=data)`.

**CRITICAL**: Always save PDF to a **different** output path. PyMuPDF cannot save to the original file with garbage collection.

### Step 4: Update all target directories
After rebuilding, copy updated files to all required locations:
- `output/` — working copies
- `KDP_Package/` — KDP upload targets
- `KDP_Package/Kindle/` — Kindle-specific EPUBs
- `KDP_Package/Print/` — Print PDFs
- `KDP_PACKAGE/` — Alternate naming (some books use this)

## EPUB Modification — Use zipfile, NOT unzip+rezip

**CRITICAL**: When modifying existing EPUBs, NEVER use shell `unzip` + file manipulation + `zip` — this silently loses files (ch10+ disappeared in AL book repair). Always use Python `zipfile.ZipFile` to read source and write destination in a single pass. See `references/epub-spine-rebuild.md` for the safe pattern.

**NEVER open a zipfile for reading AND writing to the same path** — `zipfile.ZipFile(path, 'r')` then `ZipFile(path, 'w')` in the same block corrupts the file. Always write to a *different* output path.

## Complete Rebuild Script

See `scripts/epub-rebuild.py` for the production-ready single-pass rebuild script that combines:
- Image replacement from external directory
- Spine rebuild from manifest (fixes broken AL-style spines)
- Duplicate prefix fix (handles both N===M and N!==M patterns)
- Bodymatter landmark auto-add

## PDF Build
- Use WeasyPrint with absolute file:// paths for images
- `HTML(filename=tmp_html, base_url=images_dir).write_pdf(pdf_path)`

## Workflow
1. Generate/convert images → `images/` folder
2. Copy images from `images/` → `output/` folder
3. Fix HTML duplicates
4. Rebuild PDF (WeasyPrint)
5. Rebuild EPUB (correct OPF, nav, image refs)
6. Copy PDF to `KDP_Package/Print/`, EPUB to `KDP_Package/Kindle/`

## EPUB Repair (When Source EPUB Exists but Is Broken)
See `references/epub-repair-patterns.md` for the full repair script and patterns used to fix the Lunar Foundation series.
See `references/epub-spine-rebuild.md` for spine rebuild, zipfile-safe modification, duplicate prefix regex, and bodymatter auto-add patterns.