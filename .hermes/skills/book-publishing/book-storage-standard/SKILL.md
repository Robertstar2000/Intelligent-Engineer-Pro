---
name: book-storage-standard
description: Standardized book storage directory structure for all 6 series (20 books). Use when creating new books, migrating old ones, or validating file organization. All books must follow this exact layout. For the full book creation pipeline, see the book-creation skill.
---

# Book Storage Standard

## Directory Structure

```
Series_Folder/
  SERIES_PLOT_MAP.md          # Series-wide plot arcs
  SERIES_CHARACTERS_MAP.md    # Series-wide character list
  SERIES_DESCRIPTION.md       # Series description for marketing
  SERIES_INFOGRAPHIC.png      # Series marketing infographic
  Book_N_Name/                # N = book number, Name = title words
    BOOK_PLOT_MAP.md          # Book-specific plot map
    BOOK_CHARACTERS.md        # Book-specific character list
    manuscript/               # Manuscript source
      MANUSCRIPT.md           # Primary manuscript
      MANUSCRIPT_CONDENSED.md # Condensed version (if applicable)
      book-review.md          # Editorial review notes
    html/                     # HTML chapter source files
      ch01.md, ch02.md, ...
    images/                   # Chapter images
      ch01.png, ch02.png, ...
    output/                   # Working copies (_fixed, _updated, _print versions)
    KDP_Package/              # Publishing package
      cover.jpg/png           # KDP cover image
      Book_N_Name_final.pdf   # Print-ready PDF
      Book_N_Name_final.epub  # EPUB file
      Author_Bio.txt          # Author biography
      Author_Photo.jpg        # Author photo
      Back_Cover.txt          # Back cover text
      Book_Description.txt    # Amazon description
      Keywords.txt            # 7 keyword phrases
      Title.txt               # Full title + subtitle
    Promotion/                # Marketing materials
      infographic.png         # Book infographic
      sales_text.txt          # Sales copy
      target_audience.txt     # Target audience description
      qr_amazon.png           # Amazon QR code
      qr_mifeco.png           # MIFECO QR code
```

## Series Mapping

| Series | Directory | Books |
|--------|-----------|-------|
| Age of Lightships | `Age_of_Lightships_Series/` | Book_1_Sunward_Exodus, Book_2_Mercury_Accord, Book_3_Ghosts_Beyond_Neptune, Book_4_Last_Photon_Fleet |
| Lunar Foundation | `Lunar_Foundation_Series/` | Book_1_Moon_Rock, Book_2_Mooncoming, Book_3_Waters_End, Book_4_Waters_Horizon |
| No Blue Sky | `No_Blue_Sky_Series/` | Book_1_Built_from_Dust, Book_2_The_Oxygen_Gamble, Book_3_Rivers_Under_Mars, Book_4_The_Red_Charter, Book_5_The_First_Martian_Nation |
| Cindy Lou Legal Capers | `Cindy_Lou_Legal_Capers/` | Book_1_Retainer_to_Trouble, Book_2_Clause_for_Alarm, Book_3_Affidavits_and_Alibis |
| Business | `Business_Series/` | Book_1_AI_That_Works, Book_2_Owners_Manual_for_AI_Agents, Book_3_The_Crisis_Ready_Company |
| Tomorrow Remembered | `Tomorrow_Remembered/` | Tomorrow_Remembered (standalone) |

## Naming Conventions

- Series folders: `Series_Name_Series` (except Tomorrow_Remembered)
- Book folders: `Book_N_Title_Words` (Arabic numerals, underscores)
- No Roman numerals (Book_I → Book_1)
- No lowercase book dirs (book-1-name → Book_1_Name)
- No spaces in directory names (use underscores)

## Image Requirements

### B&W Conversion (ALL Books)
- **ALL books** (fiction, memoir, mystery, AND business) convert chapter images to B&W
- The hermes_publish pipeline handles this automatically via the `images-bw` step
- B&W versions are cached in `images_bw/` subdirectory
- ~~Business books keep color~~ **DEPRECATED**: business books now use B&W too (user correction 2026-06-18)

### Image Pipeline
1. Source images go in `images/` directory (ch01.png, ch02.png, etc.)
2. `images-bw` step converts to grayscale → `images_bw/` directory
3. `pdf` and `epub` steps use B&W images from `images_bw/` automatically
4. Business books skip conversion and use original color images

### Image specifications
- Format: PNG (preferred) or JPEG
- Resolution: 300 DPI for print
- Naming: `ch{NN}.png` matching chapter numbers
- Max height in PDF: 4" (all genres)

**Page sizes (ALL books):**
- ALL books: 6×9" (15.24 × 22.86 cm) — fiction, memoir, mystery, AND business
- **NEVER** use 8.5×11 for business books — KDP rejects non-standard trim sizes
- Never change page size to hit page targets — rewrite content instead

**Page count targets:**
- Standard books: 160–275 pages at 6×9"
- Exempt from minimum: Mooncoming (novella), Tomorrow Remembered (memoir)
- Business books at ~350 words/page for 6×9"

## 13-Point Quality Check

All books must pass:
1. No ISBN references anywhere
2. No YAML frontmatter in manuscripts
3. Has front matter (title, copyright, disclaimer)
4. Has back matter (Also by, About the Author)
5. Has PDF in KDP_Package or output/
6. Has EPUB in KDP_Package
7. Has cover image in KDP_Package
8. Has chapter images in images/
9. Has BOOK_PLOT_MAP.md
10. Has BOOK_CHARACTERS.md
11. Has Promotion/ directory with content
12. Has KDP_Package/ directory
13. Manuscript in manuscript/ directory

## Migration Notes

- Migration script: `/mnt/usb_4tb/books/scripts/migrate_to_standard_structure.py`
- Quality check script: `/mnt/usb_4tb/books/scripts/quality_check_13.py`
- hermes_publish config: `/mnt/usb_4tb/books/hermes_publish/config.py`
- All paths updated to use new structure as of 2026-06-17
