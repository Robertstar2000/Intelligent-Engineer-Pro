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
