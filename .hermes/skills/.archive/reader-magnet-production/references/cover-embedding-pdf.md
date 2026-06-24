# Cover Image Embedding into Reader Magnet PDFs

## When to Use

- A reader magnet novella PDF is already built (from fpdf2 or HTML conversion) but has **no graphical cover** as the first page
- The PDF is served directly as a download (mifeco.com/books/magnets/) — readers see a blank/plain first page when opening
- The full-sized original PDF from the novella subdirectory already has a title page (text-only) and you want to prepend the cover image

## Why This Exists

The original PDF generation pipeline (fpdf2 or HTML→PDF) produces a book-style interior PDF with chapter content starting on page 1. The cover is only used for the Amazon KDP package, not embedded in the reader-facing PDF. Since novella magnets are direct downloads (not through KDP), they need the cover embedded so readers see it when they open the file.

## Prerequisites

- `PIL` (Pillow) for image manipulation
- `PyPDF2` for PDF merging (`pip3 install PyPDF2`)
- Cover image in portrait orientation (1024×1536 or similar 2:3 ratio)
- Content PDF already generated

## Workflow

### Step 1: Convert Cover Image to PDF Page

The cover images are stored in two places:
- `/mnt/usb_4tb/books/books-section/images/magnet-{series}.png` — website marketing graphics (preferred)
- `/mnt/usb_4tb/books/books-section/magnets/{Series Name}/CoverImage.png` — larger originals

Resize the cover to fit a 6×9" page (900×1350px at 150 DPI), centered on a white canvas:

```python
from PIL import Image

img = Image.open(cover_img_path)

# 6x9" at 150 DPI
target_w, target_h = 900, 1350
img_w, img_h = img.size
scale = min(target_w/img_w, target_h/img_h)
new_w, new_h = int(img_w*scale), int(img_h*scale)
img = img.resize((new_w, new_h), Image.LANCZOS)

canvas = Image.new("RGB", (target_w, target_h), (255, 255, 255))
x = (target_w - new_w) // 2
y = (target_h - new_h) // 2
canvas.paste(img, (x, y))

cover_pdf = "/tmp/cover_temp.pdf"
canvas.save(cover_pdf, "PDF", resolution=150)
```

**Note:** `resolution=150` in the save call is critical — it ensures the DPI metadata matches the pixel dimensions so PDF readers render it at the right size.

### Step 2: Merge Cover + Content

```python
from PyPDF2 import PdfReader, PdfWriter

content_reader = PdfReader(content_pdf_path)
writer = PdfWriter()
writer.append(cover_pdf)
for page in content_reader.pages:
    writer.add_page(page)

output_path = "magnet_with_cover.pdf"
with open(output_path, "wb") as f:
    writer.write(f)

os.remove(cover_pdf)
```

### Step 3: Replace the Live PDF

```python
os.replace(output_path, "original_magnet.pdf")
```

## Cover Image Sources

| Series | Web Image | Subdirectory Image |
|--------|-----------|-------------------|
| Age of Lightships | `images/magnet-age-of-lightships.png` | `magnets/Age of Lightships Novella/Lightships.png` |
| Lunar Foundation | `images/magnet-lunar-foundation.png` | `magnets/lunar foundation Novella/Moon.png` |
| No Blue Sky | `images/magnet-no-blue-sky.png` | `magnets/No Blue Sky Novella/Dust.png` |
| Cindy Lou | `images/magnet-cindy-lou.png` | `magnets/Cindy Lou Novella/CindyLou.png` |
| Business | `images/magnet-business.png` | `magnets/Business Series Magnet/Business.png` |

All images are 1024×1536 or 992×1586 (≈2:3 portrait — standard book cover ratio).

## File Sizes After Embedding

| Novella | Before | After |
|---------|--------|-------|
| Last Transmission | ~76KB | ~1.5MB |
| First Light | ~97KB | ~1.8MB |
| Before the Dust | ~83KB | ~2.1MB |
| Cindy Lou Magnet | ~98KB | ~2.7MB |
| AI for Small Business | ~1.8MB | ~1.9MB |

The increase is expected — the cover PNG (~1-2MB) is now part of the PDF.

## Verification

After replacing the file, verify it's being served correctly:

```bash
curl -sI "https://www.mifeco.com/books/magnets/{filename}.pdf" | grep -i "content-length"
# Should show the new, larger file size
```