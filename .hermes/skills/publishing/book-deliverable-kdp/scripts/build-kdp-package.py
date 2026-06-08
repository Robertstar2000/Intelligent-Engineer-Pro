#!/usr/bin/env python3
"""
Build a complete KDP publishing package from existing output files.
Usage: python3 build-kdp-package.py <book_key> <title> <author> <output_dir> <cover_png>
"""
import sys, os, shutil, zipfile
from pathlib import Path
from PIL import Image

if len(sys.argv) < 6:
    print("Usage: build-kdp-package.py <book_key> <title> <author> <output_dir> <cover_png>")
    sys.exit(1)

BOOK_KEY = sys.argv[1]
TITLE = sys.argv[2]
AUTHOR = sys.argv[3]
OUTPUT = Path(sys.argv[4])
COVER = Path(sys.argv[5])

PKG_DIR = OUTPUT / f"{BOOK_KEY}_KDP_PACKAGE"
for d in ["Kindle", "Print", "Marketing_and_Compliance", "Source"]:
    (PKG_DIR / d).mkdir(parents=True, exist_ok=True)

# EPUB
epub_src = OUTPUT / f"{BOOK_KEY}.epub"
if epub_src.exists():
    shutil.copy2(epub_src, PKG_DIR / "Kindle" / f"{BOOK_KEY}.epub")

# Cover JPEG at 1600x2560
if COVER.exists():
    img = Image.open(COVER)
    jpg = img.resize((1600, 2560), Image.LANCZOS)
    jpg.convert("RGB").save(str(PKG_DIR / "Kindle" / f"{BOOK_KEY}_Cover.jpg"), "JPEG", quality=95)
    shutil.copy2(COVER, PKG_DIR / "Kindle" / f"{BOOK_KEY}_Cover.png")

# Print PDF
pdf_src = OUTPUT / f"{BOOK_KEY}_Print_Ready.pdf"
if pdf_src.exists():
    shutil.copy2(pdf_src, PKG_DIR / "Print" / f"{BOOK_KEY}_Print_Ready.pdf")

# Source manuscript
for candidate in ["manuscript.md", "manuscript.html", f"{BOOK_KEY}.md"]:
    src = OUTPUT.parent / candidate if candidate.endswith('.md') else OUTPUT / candidate
    if src.exists():
        shutil.copy2(src, PKG_DIR / "Source" / f"{BOOK_KEY}_{candidate}")
        break

# README
readme = f"""# {TITLE} — KDP Publishing Package

## Author
{AUTHOR}

## Contents
- Kindle/{BOOK_KEY}.epub — EPUB3 manuscript
- Kindle/{BOOK_KEY}_Cover.jpg — 1600x2560 cover JPEG
- Print/{BOOK_KEY}_Print_Ready.pdf — 6x9 print-ready PDF
- Source/ — manuscript source
- Marketing_and_Compliance/ — description, keywords, AI disclosure

## Upload to KDP
1. Go to kdp.amazon.com and create a new title
2. Upload the EPUB and cover JPEG for Kindle edition
3. Upload the print PDF for paperback edition
"""
(PKG_DIR / "README.md").write_text(readme)

# ZIP
zip_path = OUTPUT / f"{BOOK_KEY}_KDP_PACKAGE.zip"
with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
    for root, dirs, files in os.walk(PKG_DIR):
        for f in files:
            fp = os.path.join(root, f)
            rel = os.path.relpath(fp, PKG_DIR.parent)
            zf.write(fp, rel)

print(f"Package: {zip_path} ({zip_path.stat().st_size//1024} KB)")
