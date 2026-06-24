# B&W Image Conversion — Pipeline Reference

## Overview

The hermes_publish pipeline automatically converts chapter images to grayscale (B&W) for all fiction, memoir, and mystery books. Business books retain color images.

## Pipeline Step: `images-bw`

**Location:** `hermes_publish/utils.py` → `convert_images_to_bw(book_key, book)`

**Behavior:**
- Fiction/memoir/mystery: converts all images in `images/` to `images_bw/` (8-bit grayscale, 300 DPI)
- Business: skips conversion entirely (color charts/infographics preserved)
- Cached: only converts images that don't already exist in `images_bw/`

## Key Functions

```python
from hermes_publish.utils import (
    convert_image_to_bw,      # Single image: src to dst grayscale
    collect_images_for_book,  # List all (chapter_num, path) for a book
    get_bw_image_path,        # Get B&W path (auto-converts if needed)
)
```

### `convert_image_to_bw(src_path, dst_path, dpi=300)`
Converts a single image to 8-bit grayscale using PIL. Sets DPI metadata. PNG uses compress_level=6, JPEG uses quality=95.

### `get_bw_image_path(book, chapter_num)`
Returns the path to use for a chapter image in PDF/EPUB builds:
- Fiction/memoir/mystery: returns `images_bw/chNN.png` (converts if needed)
- Business: returns `images/chNN.png` (original color)
- Returns None if no image exists for that chapter

## PDF/EPUB Integration

Both `step_pdf.py` and `step_epub.py` call `get_bw_image_path(book, chapter_num)` for each chapter. The B&W image is embedded at the top of the chapter content.

## Image Specifications

- Format: PNG (preferred) or JPEG
- Resolution: 300 DPI for print
- Naming: `chNN.png` matching chapter numbers
- Max height in PDF: 4in (fiction 6x9) or 5in (business 8.5x11)
- Color mode: 8-bit grayscale ('L' mode in PIL)

## Directory Layout

```
Book_N_Name/
  images/           <- Source images (color)
  images_bw/        <- Auto-generated B&W conversions (fiction only)
  output/           <- Built PDF/EPUB files
```

The `images_bw/` directory is auto-created and cached. Delete it to force re-conversion.
