# EPUB Cover Embedding Pattern

When a cover image changes, all EPUBs for that book must be updated with the new cover.
EPUBs are ZIP files; the cover image is typically at `EPUB/images/cover.jpg` (or `.png`)
and referenced by `EPUB/cover.xhtml`.

## Workflow

```python
import os, shutil, zipfile, tempfile, glob

def update_epub_cover(epub_path, cover_jpg_path):
    """Replace the embedded cover image in an EPUB file."""
    tmp_dir = tempfile.mkdtemp()
    try:
        # Extract EPUB
        with zipfile.ZipFile(epub_path, 'r') as z:
            z.extractall(tmp_dir)

        # Copy new cover image (always as JPEG for KDP compliance)
        os.makedirs(f"{tmp_dir}/EPUB/images", exist_ok=True)
        shutil.copy2(cover_jpg_path, f"{tmp_dir}/EPUB/images/cover.jpg")

        # Ensure cover.xhtml exists
        if not os.path.exists(f"{tmp_dir}/EPUB/cover.xhtml"):
            with open(f"{tmp_dir}/EPUB/cover.xhtml", "w") as f:
                f.write('''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">
<head><title>Cover</title>
<style type="text/css">body{margin:0;padding:0;text-align:center;}img{max-width:100%;max-height:100%;}</style>
</head><body><div id="cover-image"><img src="images/cover.jpg" alt="Cover"/></div></body>
</html>''')

        # Repack EPUB (mimetype must be first, uncompressed)
        all_files = []
        for root, dirs, files in os.walk(tmp_dir):
            for fn in files:
                fp = os.path.join(root, fn)
                rp = os.path.relpath(fp, tmp_dir)
                all_files.append((rp, fp))
        all_files.sort(key=lambda x: (0 if x[0] == "mimetype" else 1, x[0]))

        with zipfile.ZipFile(epub_path, 'w', zipfile.ZIP_DEFLATED) as zout:
            for rel_path, full_path in all_files:
                if rel_path == "mimetype":
                    info = zipfile.ZipInfo(rel_path)
                    info.compress_type = zipfile.ZIP_STORED
                    with open(full_path, 'rb') as f:
                        zout.writestr(info, f.read())
                else:
                    zout.write(full_path, rel_path)
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)
```

## Batch Update Pattern

For a book with multiple EPUB formats (digital, hardcover, paperback):

```python
book_dir = "/home/bob/books/Series_Name/Book_X_Title"
cover_kdp = f"{book_dir}/generated_images/cover_KDP.jpg"
for epub in sorted(glob.glob(f"{book_dir}/output/*.epub")):
    update_epub_cover(epub, cover_kdp)
    print(f"Updated: {os.path.basename(epub)}")
```

## Key Rules

- KDP cover must be JPEG (`cover.jpg`), not PNG — always convert to JPEG when embedding
- `mimetype` file must be written first and uncompressed in the ZIP
- Preserve existing `cover.xhtml` if it exists; create one if missing
- The cover image in `EPUB/images/` replaces whatever format was there before
- After updating, also copy `cover_KDP.jpg` to `KDP_PACKAGE/images/cover.jpg` for KDP submission

## Two-Pass Cover Generation Pattern (Age of Lightships, May 2026)

For high-quality covers that follow the skill's typography standards, use a two-pass approach:

**Pass 1 — Generate base art (NO text in prompt):**
- Craft prompt with scene description, genre palette, "TOP 40% EMPTY" instruction
- Include "NO TEXT NO WORDS NO LETTERS" at end of prompt
- Save as `cover_base_bN.png` (1024×1024 from Gemini)

**Pass 2 — Apply typography overlay (PIL):**
- Crop/resize to working canvas (1024×1536 for 3:4 or 1200×1800 for 2:3)
- Apply gradient overlay (top 35% dark fade + bottom 55px author bar)
- Series label at y=15, title at y=54, author at bottom
- Save as `cover_final.png` + export `cover_KDP.jpg` (1600×2560)

**Pass 3 — Embed in EPUBs:**
- Use batch update pattern above for all 3 EPUB formats
- Also copy to `KDP_PACKAGE/images/cover.jpg`

This separates art quality from typography quality and gives clean, professional results.
