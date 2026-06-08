# KDP Packaging Pitfalls & Patterns — CEO Agent

> Reference for KDP packaging tasks. Last updated: June 2, 2026.

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
