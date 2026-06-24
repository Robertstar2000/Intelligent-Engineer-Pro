# Image Compression & EPUB/PDF Rebuild Reference

## Session: 2026-06-22 — Lunar Foundation + Age of Lightships Image Update

### Problem
Book EPUBs and PDFs had old/small images. New high-res images (1024x1024 PNG, ~2MB each) needed to be inserted into all EPUBs and PDFs across 8 books. After insertion, file sizes were too large for KDP.

### Solution: Compress → Rebuild → Validate

#### Step 1: Compress Images
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
```

**Results**: 407 images, 512MB → 62MB (88% reduction)

#### Step 2: Rebuild EPUBs
Key insight: When replacing .png with .jpg, must update THREE things:
1. Image file bytes in EPUB ZIP
2. OPF manifest href (.png → .jpg) + add media-type="image/jpeg"
3. HTML img src references (.png → .jpg)

Also must add `cover-image` property to first image item in OPF manifest.

#### Step 3: Rebuild PDFs
Use PyMuPDF `page.replace_image(xref, stream=data)` — it's a **Page** method, not Document method.
Always save to a **different** output path.

#### Step 4: Validate
- cover-image property present
- spine element present with all chapters
- All image items have media-type attributes
- NCX has playOrder attributes
- nav.xhtml has epub:type="toc" and epub:type="landmarks"

### Books Processed
- Lunar Foundation: Book 1-4 (Moon Rock, Mooncoming, Waters End, Waters Horizon)
- Age of Lightships: Book 1-4 (Sunward Exodus, Mercury Accord, Ghosts Beyond Neptune, Last Photon Fleet)
- Book 4 Waters Horizon: chapter_images has ch31-60, EPUB has ch01-ch30 — no overlap, already correct

### File Counts
- 81 EPUBs rebuilt with compressed images
- 38 PDFs rebuilt with compressed images (_compressed.pdf)
- 72 EPUBs got cover-image property added
- All EPUBs pass KDP validation after fixes

### Tools Used
- **PyMuPDF (fitz)** v1.27.2 — PDF image replacement (`page.replace_image()`)
- **Pillow** — Image compression (JPEG, 200 DPI, q85, 800px max)
- **zipfile** — EPUB modification (read source, write to different path)

### Key Pitfalls Encountered
1. `doc.replace_image()` doesn't exist — it's `page.replace_image()`
2. `doc.update_image()` doesn't exist either
3. Cannot save PDF to same path with garbage collection — use different output path
4. EPUB OPF regex must handle items that already have media-type (use callback pattern)
5. PNG→JPEG conversion requires updating ALL references (OPF + HTML + file extension)
6. Some KDP_PACKAGE/Kindle files have 0-1 images (legacy files, skip them)
7. _fixed.epub files are content-only (no images), skip them
