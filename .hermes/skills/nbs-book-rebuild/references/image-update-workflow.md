# Image Update Workflow — EPUB & PDF

## When to Use
When `chapter_images/` directory has new/replaced images and EPUB/PDF files need to be updated.

## Date Comparison
```python
import os, re
from datetime import datetime

def needs_update(book_path):
    ch_dir = os.path.join(book_path, "chapter_images")
    if not os.path.isdir(ch_dir):
        return False, "No chapter_images"
    latest_img = max(
        (os.path.getmtime(os.path.join(ch_dir, f)), f)
        for f in os.listdir(ch_dir)
        if f.lower().endswith(('.png', '.jpg', '.jpeg'))
    )
    for root, dirs, files in os.walk(book_path):
        if '_archived' in root:
            continue
        for f in files:
            if f.endswith(('.epub', '.pdf')):
                fp = os.path.join(root, f)
                if latest_img[0] > os.path.getmtime(fp):
                    return True, f"Image {latest_img[1]} newer than {f}"
    return False, "All files current"
```

## EPUB Image Replacement
Use Python `zipfile` to read EPUB, replace images in `OEBPS/images/`, write to temp file, then move.

**CRITICAL**: Never write to the same path you're reading from.

## PDF Image Replacement
Use PyMuPDF `page.replace_image(xref, stream=data)`.

**CRITICAL**: `replace_image()` is a **Page** method, NOT `doc.replace_image()` or `doc.update_image()`.
**CRITICAL**: Always save to a **different** output path.

## Special Cases
- **_fixed.epub**: Content-only, no images — skip
- **KDP_PACKAGE/Kindle**: May have 0-1 images (cover only) — legacy, skip
- **Non-overlapping chapters**: If EPUB has ch01-30 but chapter_images has ch31-60, no update needed
