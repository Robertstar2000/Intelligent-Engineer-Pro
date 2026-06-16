# KDP Packaging Pitfalls & Patterns — CEO Agent

> Reference for KDP packaging tasks. Last updated: June 10, 2026.

## Orphan Book Enrichment Pattern

Some books have EPUBs, marketing text files, and cover images in the root book directory but **NO KDP_PACKAGE/ directory at all**. These are "orphans" — books with all assets but no formal KDP directory structure.

**Case study:** Tomorrow_Remembered — listed as KDP-ready in the product inventory, had zips in the central `KDP_Packages/` archive, but had NO per-book `KDP_PACKAGE/` directory. Reason: its EPUBs and marketing files were scattered in the root, never consolidated.

### Detection:
```bash
# Find books with EPUBs in root but no KDP_PACKAGE dir
for d in ~/books/*/; do
  book=$(basename "$d")
  if [ -d "$d" ] && [ "$(find "$d" -maxdepth 1 -name '*.epub' 2>/dev/null)" ] && [ ! -d "$d/KDP_PACKAGE" ]; then
    echo "ORPHAN: $book"
  fi
done
```

### Fix (CEO-executable inline, ~5s):
1. Create `KDP_PACKAGE/Kindle/`, `KDP_PACKAGE/Marketing_and_Compliance/`
2. Copy all `.epub` files from root into `Kindle/` (books may have multiple EPUB variants — copy all)
3. Copy all `.txt` marketing files from root into `Marketing_and_Compliance/`
4. Copy cover image (any file with 'Cover' in name) to `KDP_PACKAGE/`
5. Copy `Author_Photo.jpg` to `Marketing_and_Compliance/`
6. Zip the directory

## Thin Package Enrichment Pattern

Some KDP_PACKAGE directories have **only Kindle/ with an EPUB** (1 file total), missing all marketing materials. This is typical for newly created KDP packages where only the EPUB was copied in, or packages created by an automated process that skipped the marketing step.

### Detection:
```bash
# Find KDP_PACKAGE dirs with <4 files (likely missing marketing)
find ~/books/ -type d -name "KDP_PACKAGE" -exec sh -c 'c=$(find "$1" -type f | wc -l); [ "$c" -lt 4 ] && echo "THIN ($c files): $1"' _ {} \;
```

### Case study:
Cindy Lou Legal Capers 3 books had only 1 file each (EPUB in Kindle/). Marketing text files existed in the book root directory but were never copied into KDP_PACKAGE/.

### Fix (CEO-executable inline, ~5s per book):
Check the book root for existing marketing files. The standard set: `Author_Bio.txt`, `Book_Description.txt`, `Keywords.txt`, `Back_Cover.txt`, `Title.txt`, `Author_Photo.jpg`, `AI_Disclosure.txt`. Copy any that exist into `Marketing_and_Compliance/`, then re-zip. Do NOT fail if a file is missing — only copy files that exist.

## Upgrade Pattern: Publishing_Package.zip → KDP_PACKAGE/

### Directory structure to create:
```
KDP_PACKAGE/
├── README.md
├── Kindle/
│   └── {book_name}.epub
├── Print/
│   ├── {book_name}_Print.pdf
│   └── cover_wrap/
│       ├── {book_name}_Cover.jpg
│       └── {book_name}_Cover.png
└── Marketing_and_Compliance/
    ├── {book_name}_Author_Bio.txt
    ├── {book_name}_Back_Cover.txt
    ├── {book_name}_Description.txt
    ├── {book_name}_Keywords.txt
    ├── {book_name}_Title.txt
    ├── {book_name}_AI_Disclosure.md
    └── Author_Photo.jpg
```

## Key pitfalls:

1. **File naming inconsistency**: Marketing files use different prefixes than EPUB files (see below)
2. **PDF naming**: Some books use `_Print.pdf`, others `_Print_Ready.pdf`
3. **Cover format**: Some have `.jpg`, some `.png`, some both — copy both into cover_wrap/
4. **execute_code is fastest**: Inline `execute_code` with `shutil`/`zipfile` takes ~2-3s for 3 books

## NBS marketing file naming variants:

| Book | Marketing prefix | EPUB prefix |
|------|-----------------|-------------|
| NBS I | `Built_from_Dust_` | `No_Blue_Sky_1_Built_from_Dust_` |
| NBS II | `The_Oxygen_Gamble_` | `No_Blue_Sky_2_The_Oxygen_Gamble_` |
| NBS III | `Rivers_Under_Mars_` | `No_Blue_Sky_3_Rivers_Under_Mars_` |
| NBS IV-V | Consistent with EPUB prefix | Same |

**Fix logic:** Check both the short-name pattern AND the `{file_prefix}_` pattern. Copy whichever exists.

## KDP_PACKAGE checklist per book (minimum):
- [ ] Kindle/ has EPUB > 100KB
- [ ] Print/ has PDF + cover_wrap/ with JPG/PNG
- [ ] Marketing_and_Compliance/ has description, bio, keywords, AI disclosure
- [ ] README.md lists contents
- [ ] Zip file recreated after any changes
- [ ] Zip file size is reasonable (> 100KB, typically 1-100MB)

---

## Duplicate Zip Cleanup Pattern (June 13, 2026)

Over time, KDP zip files accumulate with inconsistent naming:
- **PascalCase canonical**: `Built_from_Dust_KDP_PACKAGE.zip` (keep)
- **kebab-case variants**: `built-from-dust_KDP_PACKAGE.zip` (remove)
- **book-N- prefix variants**: `book-1-retainer-to-trouble_KDP_PACKAGE.zip` (remove)
- **Central archive**: `KDP_Packages/` directory with 20+ duplicate zips (remove)
- **Build workspaces**: `cindy-lou-series/` nested dir with 3 duplicate KDP_PACKAGE dirs (remove)

### Detection:
```bash
# Count total zips vs books
find ~/books/ -name "*KDP*PACKAGE*.zip" 2>/dev/null | wc -l
# If >> number of books (22), you have inflation
```

### Cleanup (CEO-executable inline, ~30s):
```python
import os, zipfile
# 1. Remove central KDP_Packages/ archive entirely
shutil.rmtree("~/books/KDP_Packages/", ignore_errors=True)
# 2. Remove cindy-lou-series/ nested build workspace
shutil.rmtree("~/books/Cindy_Lou_Legal_Capers/cindy-lou-series/", ignore_errors=True)
# 3. Per-book: keep only PascalCase *_KDP_PACKAGE.zip, remove kebab-case/book-N- variants
for book_dir in all_book_dirs:
    for zip_file in os.listdir(book_dir):
        if zip_file.endswith('.zip') and not zip_file.endswith('_KDP_PACKAGE.zip'):
            os.remove(os.path.join(book_dir, zip_file))
# 4. Recreate canonical zips from KDP_PACKAGE/ directories for all books
```

**Result today:** 63 zips → 22 canonical zips (2.9x inflation removed)

---

## Tomorrow_Remembered Flat Structure Fix (June 13, 2026)

More complex orphan case — book has:
- Multiple EPUB variants in root + subdirs (`output/`, `_resources/output/`, `_resources/Tomorrow_is_Still_Open_Publishing_Package/`)
- 15+ PDF variants scattered in root + `_resources/output/`
- Marketing files in root (`*_Author_Bio.txt`, `*_Description.txt`, `*_Keywords.txt`, `*_Title.txt`, `*_Back_Cover.txt`, `Author_Photo.jpg`)
- **NO KDP_PACKAGE/ directory** (but had zips in central KDP_Packages/ archive)

### Fix (CEO-executable inline, ~2 min):
1. Create `KDP_PACKAGE/Kindle/`, `KDP_PACKAGE/Print/`, `KDP_PACKAGE/Marketing_and_Compliance/`
2. Copy **ALL** `.epub` files from root and subdirs (recursive) into `Kindle/`
3. Copy **ALL** `.pdf` files from root and subdirs (recursive) into `Print/`
4. Copy marketing files (`*_Author_Bio.txt`, `*_Description.txt`, `*_Keywords.txt`, `*_Title.txt`, `*_Back_Cover.txt`, `Author_Photo.jpg`) into `Marketing_and_Compliance/`
5. Create `README.md` manifest
6. Create canonical zip: `Tomorrow_Remembered_KDP_PACKAGE.zip` (43MB)

**Pitfall:** Standardizing loop created `KDP_PACKAGE/` inside `KDP_PACKAGE/` — must remove nested `KDP_PACKAGE/KDP_PACKAGE/` after creation.

---

## Cindy Lou Legal Capers Thin Package Enrichment (June 13, 2026)

3 books (`book-1-retainer-to-trouble`, `book-2-clause-for-alarm`, `book-3-affidavits-and-alibis`) had KDP_PACKAGE dirs with **only 1 file each** (EPUB in Kindle/). Marketing files existed in book root: `Author_Bio.txt`, `Book_Description.txt`, `Keywords.txt`, `Title.txt`, `Back_Cover.txt`, `Author_Photo.jpg`.

### Fix (CEO-executable inline, ~5s per book):
Copy marketing files from book root → `KDP_PACKAGE/Marketing_and_Compliance/`, re-zip. Each went from 1 file → 7 files.

---

## EPUB Content Detection — Correct Method (June 2026)

**WRONG:** Filename filter `content|chapter|text` — misses `ch002.xhtml`, `ch025.xhtml`, `titlepage.xhtml`, etc.

**CORRECT:** Use `f.endswith('.xhtml')` or check total file count + EPUB size.

**Small EPUB ≠ stub:** EPUBs of 54-276KB can contain 12-34 XHTML files with full chapter content. Compression is very effective for text.

### Verification:
```bash
# Check EPUB internal structure
unzip -l book.epub | grep '\.xhtml$' | wc -l
# Or: check file count in extracted EPUB
```

---

## First Generation De-archiving Pattern (June 13, 2026)

Books previously archived under `~/books/_archived/` need restoration to active series directories with standard structure.

### Steps:
1. Locate manuscript in archive: `~/books/_archived/backup_2026-05-07_old/FG/First_Generation/working/First_Generation_Manuscript.md`
2. Copy to active series: `~/books/No_Blue_Sky_Series/Book_I_Built_from_Dust/manuscript/`
3. Create standard directories: `cover/`, `manuscript/`, `sources/`, `output/`, `KDP_PACKAGE/`
4. Move existing cover files to `cover/`
5. Move marketing files to `KDP_PACKAGE/Marketing_and_Compliance/`
6. Copy EPUBs to `KDP_PACKAGE/Kindle/`, PDFs to `KDP_PACKAGE/Print/`
7. Recreate canonical zip

---

## Directory Standardization Pattern (June 13, 2026)

All books should have consistent structure:
```
book_root/
├── cover/              # cover images (Cover.jpg, Cover.png, NBS_1_*.png, etc.)
├── manuscript/         # final MANUSCRIPT.md
├── sources/            # manuscript_src/ or chapters/ content
├── output/             # generated EPUB/PDF
└── KDP_PACKAGE/        # Kindle/, Print/, Marketing_and_Compliance/, README.md
```

### Migration (CEO-executable inline):
- Move `manuscript_src/` → `sources/`
- Move `chapters/` → `sources/`
- Move cover files → `cover/`
- Create missing directories

Applied to all 22 books across 6 series today.
