# Memoir PDF Rebuild from Markdown (WeasyPrint Pipeline)

## When to Use
- A memoir manuscript exists as a single Markdown file (`MANUSCRIPT.md`) with chapter images in `chapter_images/`
- The existing PDF/EPUB is missing images, has wrong formatting, or was generated with different tools
- Proper 6×9" trade paperback formatting with B&W images is required

## Prerequisites
```bash
pip install markdown weasyprint PyPDF2 Pillow
```

## Full Pipeline

### 1. Pre-flight Checks
```bash
# Verify chapter images exist
ls chapter_images/ch*.png

# Check grep for image references in manuscript
grep -n "^!\[\]" MANUSCRIPT.md

# Verify chapter structure matches TOC
grep -n "^## Chapter\|^# Part" MANUSCRIPT.md
```

### 2. Convert Images to B&W (Grayscale)
All chapter images MUST be converted to grayscale before embedding:
```python
from PIL import Image
import os

IMGDIR = "chapter_images"
TMPDIR = "/tmp/memoir_pdf"
os.makedirs(TMPDIR, exist_ok=True)

for f in sorted(os.listdir(IMGDIR)):
    if f.lower().endswith(".png"):
        img = Image.open(os.path.join(IMGDIR, f)).convert("L")
        img.save(os.path.join(TMPDIR, f), "PNG")
```

### 3. Build HTML from Markdown
```python
import markdown, re

# Read and fix image paths to point to B&W versions
md_text = open("MANUSCRIPT.md").read()

def fix_img(m):
    alt, src = m.group(1), m.group(2)
    bw_path = os.path.join(TMPDIR, os.path.basename(src))
    if os.path.exists(bw_path):
        return f"![{alt}]({bw_path})"
    return m.group(0)

md_text = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", fix_img, md_text)

# Convert to HTML
html_body = markdown.markdown(md_text, extensions=["fenced_code", "smarty"])

# Add CSS class to images
html_body = re.sub(
    '<img ([^>]+)>',
    lambda m: f'<img {m.group(1)} class="chapter-image">',
    html_body
)
```

### 4. CSS for Memoir Formatting (6×9")
Key CSS rules:
- Page: 6×9" with 0.7-0.85in margins
- Body: Georgia 11.5pt, 1.7 line-height, justified, hyphenation
- H1 (part headings): 22pt centered, start on recto page
- H2 (chapter headings): 17pt centered italic, no page break after
- Paragraphs: 1.5em indent, no indent after headings
- Chapter images: full width, max 3.2in height, centered
- Scene breaks (hr): "• • •" centered
- Page numbers: 9pt in footer, suppressed on title page

### 5. Generate PDF
```python
from weasyprint import HTML, CSS

html_obj = HTML(filename=html_path, base_url=TMPDIR)
pdf_bytes = html_obj.write_pdf(stylesheets=[css])
open("Tomorrow_Remembered_final.pdf", "wb").write(pdf_bytes)
```

### 6. Verify PDF
```python
from PyPDF2 import PdfReader
import os

r = PdfReader("Tomorrow_Remembered_final.pdf")
size_mb = os.path.getsize("Tomorrow_Remembered_final.pdf") / 1024 / 1024
print(f"Pages: {len(r.pages)}, Size: {size_mb:.1f} MB")
print(f"Title: {r.metadata.get('/Title', '?')}")
# Spot-check key pages
for i in [1, 3, 5, 7, len(r.pages)]:
    t = r.pages[i-1].extract_text()[:80]
    print(f"  Page {i}: {t!r}")
```

## Expected Output
- **30-40K word memoir**: ~180-210 pages at 6×9" with 11.5pt Georgia
- **File size**: 3-8 MB depending on image count
- **Images**: All chapter images in grayscale, embedded once per chapter

## Common Pitfalls
1. **RGBA images**: WeasyPrint may fail with RGBA PNGs. Convert to RGB/L first.
2. **Image path resolution**: WeasyPrint needs absolute paths or correct `base_url`. Use `base_url=TMPDIR` with absolute image paths.
3. **TOC page numbers**: WeasyPrint doesn't support `target-counter()`. For print PDF with synchronized page numbers, use a 2-pass approach: render once → extract page numbers → hardcode → re-render. For memoirs without explicit page numbers in TOC, this isn't needed.
4. **Title page**: The first `<h1>` in the markdown becomes the title page. Center it with CSS and suppress page number via `@page :first`.
5. **WeasyPrint image duplication**: WeasyPrint may report many image objects per page in PyPDF2 inspection. This is normal — it embeds images in the page resource dictionary. Visual inspection confirms each chapter has exactly one opener image.

## EPUB Rebuild Note
If the EPUB is structurally broken (wrong chapter division, missing images, stale content):
1. Do NOT try to patch the existing EPUB
2. Rebuild from scratch using the current `MANUSCRIPT.md`
3. Create individual HTML files per chapter with images at the top
4. Build EPUB directory structure manually and zip it

## Cleanup
```bash
rm -rf /tmp/memoir_pdf /tmp/build_memoir_pdf.py
```
