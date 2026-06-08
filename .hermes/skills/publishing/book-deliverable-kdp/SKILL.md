---
name: "book-deliverable-kdp"
title: "Book Deliverable — KDP Package"
description: "Build AND/OR deliver a complete KDP publishing package for any finished book. Fast path checks for an existing package before delivering. Build path creates everything from scratch. Covers: Kindle eBook (EPUB 3), print-ready PDF, wrap cover, marketing copy, AI disclosure, EPUB validation per KDP Kindle Publishing Guidelines 2025.1."
category: "publishing"
triggers: ["put this on kindle", "prepare for kdp", "kindle package", "book deliverable", "epub", "kindle ebook", "epub validation"]
---

## 🔍 MemPalace Query (MANDATORY FIRST STEP)
Before proceeding, query MemPalace for existing context:
```python
import sys, os; sys.path.insert(0, os.path.expanduser('~/.hermes/mempalace'))
import embed; embed.init_embedding(os.path.expanduser('~/.hermes/mempalace'))
results = embed.search_embeddings("KDP publishing package EPUB Kindle book deliverable", k=5)
```
This retrieves previous decisions, domain-specific context, and lessons learned from the vector memory store.

# Book Deliverable — KDP Publishing Package

> **MemPalace Query (MANDATORY):** Before starting, query MemPalace:
> `mempalace_integration.semantic_recall("KDP publishing [book title]")`
> Retrieves previous publishing history, known issues, and conventions.

> **MemPalace Query:** Before starting, query MemPalace for relevant context:
> ```python
> import sys, os
> sys.path.insert(0, os.path.expanduser('~/.hermes/mempalace'))
> from retrieve import search
> results = search("KDP publishing package mifeco books", k=5)
> ```
> This retrieves previous publishing history, known KDP issues, and book-specific details.

## MemPalace Query

Before using this skill, ALWAYS query MemPalace for relevant context:
- Previous KDP package issues for this book/series
- Known EPUB generation pitfalls that were fixed in past sessions
- User preferences for description style, keyword density, bio tone

Use `session_search` to find prior sessions for the same book title.

# Book Deliverable — KDP Publishing Package

> **MemPalace Query (MANDATORY):** Before starting, query MemPalace:
> `mempalace_integration.semantic_recall("KDP publishing [book title]")`
> Retrieves previous publishing history, known issues, and conventions.

## MemPalace Query

Before using this skill, ALWAYS query MemPalace for relevant context:
```
mempalace_integration.semantic_recall("KDP publishing package book deliverable")
```
This retrieves previous publishing history, known issues, and book-specific conventions.

Complete workflow for packaging a finished book manuscript for Amazon KDP submission.

## Fast Path vs Build Path

All book content must be organized with shortcuts for easy access:

**Directory Structure:**
- All books stored on USB drive at: `/mnt/usb_4tb/books/[Series_Name]/[Book_Name]/`
- Centralized KDP packages: `/home/bob/books/KDP_Packages/` — symlinks to each book directory
- Desktop shortcuts: Home, USB 4TB Drive, KDP Packages

**Shortcut Setup (one-time):**
```bash
# Create KDP_Packages directory
mkdir -p /home/bob/books/KDP_Packages

# Create symlinks for each book
ln -s /mnt/usb_4tb/books/[Series]/[Book] /home/bob/books/KDP_Packages/[Book_Name]

# Create desktop shortcuts
# Home.desktop, USB_4TB.desktop, KDP_Packages.desktop in ~/Desktop/
```

**Per-Book Directory Contents (MANDATORY):**
```
[Book_Name]/
├── manuscript_src/          # Individual chapter .md files (ch01.md-ch30.md)
├── generated_images/        # Cover + B&W chapter images (ch01.png-ch40.png)
├── output/                  # KEP-compliant EPUBs (digital, paperback, hardcover)
│   ├── [Book]_digital.epub
│   ├── [Book]_paperback.epub
│   └── [Book]_hardcover.epub
├── Marketing_and_Compliance/
│   ├── Title.txt
│   ├── Book_Description.txt
│   ├── Back_Cover.txt
│   ├── Author_Bio.txt
│   └── Keywords.txt
├── Marketing_Infographic.png
├── About_the_Author.txt
├── Author_Photo.jpg
├── cover.png / cover.jpg    # Full cover
├── qr_mifeco.png            # MIFECO QR code (300x300)
├── qr_amazon.png            # Amazon author page QR code (300x300)
└── [Book]_Print.pdf         # Print-ready PDF
```

**Existing Shortcuts:**
- `/home/bob/books/KDP_Packages/` → symlinks to all book directories
- `~/Desktop/Home.desktop` → Home folder
- `~/Desktop/USB_4TB.desktop` → USB 4TB drive
- `~/Desktop/KDP_Packages.desktop` → KDP Packages folder
- `~/Desktop/Hermes_Desktop.desktop` → http://localhost:3000
- `~/Desktop/MIFESCO_Dashboard.desktop` → https://www.mifeco.com/admin/
- `~/Desktop/MIFESCO_com.desktop` → https://www.mifeco.com
- `~/Desktop/Books.desktop` → /home/bob/books

**Desktop .desktop file format:**
```ini
[Desktop Entry]
Name=Label
Comment=Description
Type=Link
URL=file:///path/or/https://url
Icon=icon-name
```
Always `chmod +x` after creating .desktop files.

## Series Description (MANDATORY — every series)

When creating a new book series, a series description MUST be generated and saved as `SERIES_DESCRIPTION.txt` in the series root directory (e.g., `/mnt/usb_4tb/books/[Series_Name]/SERIES_DESCRIPTION.txt`).

**HARD LIMIT: 4,000 characters maximum.** Write the FIRST DRAFT to ~3,000-3,200 characters. Never start over 4,000. If the user asks for compaction, cut thematic expansions and middle-book blurbs first — never cut the opening hook or closing line.

**The series description MUST include:**

1. **Series tagline** — One sentence capturing the core premise
2. **Series hook** — 2-3 paragraphs describing the overarching story, stakes, and themes (this is marketing prose, not a dry summary)
3. **Book-by-book breakdown** — 2-3 sentences per book showing the arc across the series (how each book advances the overall story, what changes, what's at stake)
4. **Themes** — 3-5 bullet points on the series' core themes
5. **Market position** — "Fans of [author/series] will love this" comparisons
6. **Series stats** — Number of books, total chapters, word count
7. **Call to action** — "Available on Amazon Kindle and Paperback" + website

**Format: Marketing prose.** Not a dry synopsis. Write it like the back cover of an omnibus edition or a series page on Amazon. Hook the reader. Make them need to read book one. Use short paragraphs. Vary sentence length. End with a punch.

**Pitfall — Over-writing:** The most common user correction on series descriptions is LENGTH. If the user says "compact" or "too long" or "just need a single overview":
- Cut thematic expansions first (lose 30-50% of "what this series explores" paragraphs)
- Condense middle-book blurbs to 1-2 sentences each
- Cut genre comps to 2 max
- Remove redundant structural phrases ("A story of...", "A novel of..." used repeatedly)
- Remove 2 out of every 3 adjectives
- NEVER cut the opening hook or closing line — these sell the series

**Example structure:**
```
[Series Title]
[Tagline — one line]

[Hook paragraph — what's the series about, what's at stake]

[Book 1 description — 2-3 sentences]
[Book 2 description — 2-3 sentences]
[Book 3 description — 2-3 sentences]
[Book 4 description — 2-3 sentences]

THEMES:
• [Theme 1]
• [Theme 2]
• [Theme 3]

Perfect for fans of [comparison] and [comparison].

[N books. N chapters. One journey.]

Available on Amazon Kindle and Paperback.
www.mifeco.com
```

**Each individual book's `Book_Description.txt` MUST reference the series:**
- First line: "THE AGE OF LIGHTSHIPS — Book N of 4" (or appropriate series name and position)
- Include "Also in series: Book 1... Book 2... Book 3..." at the end
- The book description should work standalone but also sell the series

### Sci-fi / Fiction Covers
- Background: High-quality LLM-generated space/sci-fi imagery (stars, planets, ships, landscapes). Must be visually striking and genre-appropriate.
- Title text: Bold white, high contrast against background. If title is MORE THAN 2 WORDS, word-wrap onto 2 lines, stacked. Each line must be VERY BOLD, filling most of the cover width. Use text shadow/glow for readability.
- Author name: Bold, approximately 50% of the page width, near the bottom of the cover. Very bold font, clearly readable.
- Subtitle (if applicable): Smaller than title but still bold, in a contrasting color (amber/gold for sci-fi).
- All text must pass thumbnail test (legible at 80px wide).
- 2-pass generation: raw background image first, typography second. Can use PIL for text compositing.
- KDP export: 2560x1600 px JPEG (1.6:1 ratio), RGB, max 50MB.
- Cover background image: The central illustration/photo must fill at least 60% of the cover height and 90% of the cover width. Images must be directly relevant to the book content (key scenes, settings, or imagery from the story). Small decorative borders/frames are fine but the dominant visual content must be the scene itself, not a small centered image with large empty borders.

### Business Covers
- Use bold line illustrations with bright vivid colors (image appropriate to the book content, an example for a book on disasters: might be tornado, fire, storm imagery). Title text white, subtitle bright yellow, both on semi-transparent dark background bars for high contrast.
- Title: If more than 2 words, word-wrap stacked. Very bold, white, filling most of cover width.
- Author name: Bold, 50% page width, very bold font.

### Cover Text Rules (ALL GENRES)
- Title: VERY BOLD. If >2 words, word-wrap onto multiple stacked lines. Each line fills most of cover width. White text with dark shadow/glow for high contrast.
- Author name: Bold, 50% of page width, positioned near bottom. Very bold font. Must be clearly readable at thumbnail size.
- All text must have high contrast against background (dark shadow, glow, or contrasting bar behind text).
- Never use light text on light background.
- Cover background image must fill at least 60% of cover height and 90% of cover width. Image must be directly relevant to book content.

### Technical Specs
- Font baseline positioning: PIL's `text((x, y), ...)` uses y as ascender line, NOT text top. Use `baseline_y = desired_top - bbox[1]` to correct. See `references/cover-text-positioning.md`.
- Alpha composite method: Use fully opaque overlay + alpha mask for vibrant text colors. Mask threshold p>30 captures both bars and text. See `references/cover-text-positioning.md`.
- KDP export: 2560x1600 px JPEG (1.6:1 ratio), RGB, max 50MB

## Infographics Color Spec (Added 2026-05-28)
- ALL infographics for business books MUST use grayscale ONLY (black, white, shades of gray)
- Remove all color from infographics while keeping content, text, and data unchanged
- After grayscale conversion, enhance contrast 1.5x to ensure text and linework readability
- Verify contrast is sufficient before finalizing — text must be clearly readable against background
- Detailed conversion recipe: `references/infographics-grayscale.md`
- Applies to: The Crisis Ready Company (40 infographics converted to B&W) and all future business book infographics

> **Single authoritative reference**: `references/kdp-specs.md` in this skill. All other book skills should point here — do not duplicate specs across skills.

> **Source**: [KDP Cover Image Guidelines](https://kdp.amazon.com/en_US/help/topic/G200645690) | [Paperback Guidelines](https://kdp.amazon.com/en_US/help/topic/G201857950) | [Hardcover Guide](https://kdp.amazon.com/en_US/help/topic/GDTKFJPNQCBTMRV6) | [Cover Calculator](https://kdp.amazon.com/cover-calculator) (all verified 2025-05-27)

### Quick Reference

| Cover Type | File Format | Dimensions | DPI | Color | Max Size |
|---|---|---|---|---|---|
| **Kindle eBook (marketing)** | JPEG (.jpg) or TIFF | **2560×1600 px** ideal; min 1000×625 px | 72 (pixel count matters) | **RGB only** | 50 MB |
| **Kindle eBook (internal/EPUB)** | JPEG inside OPF | Large, ≥50% of first page | — | RGB | — |
| **Paperback wrap** | **PDF** single page | Calc: 0.125+Tw+spine+Tw+0.125 wide, 0.125+Th+0.125 tall | **300 min** | CMYK preferred, RGB accepted | 650 MB |
| **Hardcover case laminate** | **PDF** single page | Calc: see hardcover section below | **300 min** | CMYK preferred, RGB accepted | 650 MB |

**Spine formulas (Paperback):**
- White paper (B&W): `page_count × 0.002252"`
- Cream paper (B&W): `page_count × 0.0025"`
- Color interior: `page_count × 0.002347"`

**Paperback example — 200 pages, 6×9", white, B&W:**
Spine = 200×0.002252 = 0.4504"; Width = 12.7004"; Height = 9.25"; At 300 DPI = **3810×2775 px**

**Hardcover — NEVER use paperback formulas.** Hardcover adds 0.625" wrap per side + 0.375" hinge per side + 0.189" board in spine. Total width = 2×trim + spine + 1.812". Spine includes board: `(page_count × 0.0025) + 0.189"`. Supported trim sizes: 5.5×8.5, 6×9, 6.14×9.21, 6.69×9.61, 7×10, 7.44×9.69, 7.5×9.25, 8.5×11. Max 550 pages.

**Content rules (all types):**
- Front cover must have title + author. No pricing/promotional text
- White/light backgrounds → add 3–4px medium gray border
- Background images must extend 0.125" beyond trim on all sides (bleed)
- All critical text ≥0.25" inside trim edge (safe zone)
- Spine text only on books **80+ pages**
- **Paperback/Hardcover covers: submit as single-page PDF** (KDP requires PDF for print)
- **eBook cover: submit as JPEG** (not PDF)

**MIFECO cover design standard:**
- Title: Large, white, bold sans-serif (DejaVuSans-Bold), with 2px black drop-shadow for readability on any background
- Author: Smaller than title, bottom of front cover
- Background: Highly relevant to content (Mars landscapes for sci-fi, professional imagery for business)
- Must pass thumbnail test (legible at 80px wide) and grayscale test
- **Manuscript files should NOT have embedded front/back cover art** — KDP's Cover Creator handles the cover display. Only the separate cover file is uploaded to KDP.

## KDP Print & eBook Interior Specs (Authoritative)

> Source: [Paperback Submission Guidelines](https://kdp.amazon.com/en_US/help/topic/G201857950) | [Formatting Your Book](https://kdp.amazon.com/en_US/help/topic/G200634400) (verified 2025-05-27)

### Print (Paperback/Hardcover) Interior

| Requirement | Spec |
|---|---|
| **Trim size** | 6" × 9" standard for MIFECO (trade paperback) |
| **Bleed** | 0.125" (3.2mm) on all sides. PDF manuscript only if bleed is needed. |
| **No-bleed page size** | Set to exact trim size (e.g. 6" × 9") |
| **Bleed page size** | Trim + 0.125" each side = 6.125" × 9.25" for 6×9 |
| **Minimum page count** | **24 pages** (KDP will not accept fewer) |
| **Maximum page count** | **828 pages** for B&W+white paper; 600 for color; 550 for hardcover |
| **Page count rounding** | Always **even** (KDP rounds up if odd — add blank page if needed) |
| **Inside (gutter) margins** | 24–150 pgs: 0.375" / 151–300: 0.5" / 301–500: 0.625" / 501–700: 0.75" / 701–828: 0.875" |
| **Outside margins** | ≥0.25" (no bleed) or ≥0.375" (with bleed) |
| **Image resolution** | **300 DPI minimum** for all interior images (600 DPI max to keep file <650MB) |
| **Fonts** | All fonts **embedded** in PDF |
| **File format** | **PDF** for print (required if bleed; recommended for all print) |
| **Color space** | CMYK preferred for print interior; RGB accepted |

### eBook (Kindle) Interior

| Requirement | Spec |
|---|---|
| **Preferred format** | **EPUB 3** (also accepts EPUB 2, DOCX, HTML, RTF, TXT) |
| **MOBI** | No longer accepted for new uploads (as of March 2025) |
| **Max file size** | 650 MB (including all embedded images) |
| **TOC** | Required for books >20 pages. Use nav.xhtml (EPUB3) + linked HTML TOC |
| **Chapter breaks** | Use `page-break-before: always` in CSS or separate XHTML files |
| **Images** | 150–300 DPI recommended; max-width: 100% |
| **Body text** | No forced font-family/size/color on `<p>` (let reader preferences apply) |
| **Font color** | Leave unspecified (forced black breaks dark mode) |
| **Validation** | **epubcheck** (0 errors) + **Kindle Previewer 3** (0 blocking errors) |
| **Duplicate IDs** | All `id=""` attributes must be unique across all XHTML files |
| **File paths** | Forward slashes `/` only; no special characters in filenames |

### Front Matter Order (Print & eBook)

1. **Title page** — Book title (bold, white, high contrast, fills ~80% of page width), subtitle, author name (bold, white, high contrast). Use a dark/black background bar or the cover image background. Title text must be clearly readable at thumbnail size.
2. **Copyright page** — Copyright notice, rights reserved, AI disclosure if applicable
3. **Table of Contents** — **MANDATORY.** Must start on a new page (use `page-break-before: always` on a wrapper div with `page-break-after: always`). See TOC Layout spec below.
4. **Dedication/Preface** (optional)
5. **Chapter 1** — Begin body matter. **Must start on a new page** (`page-break-before: always` on the heading)

### Title Page CSS (MANDATORY)

```css
.title-page {
    text-align: center;
    padding-top: 30%;
    page-break-after: always;
}
.title-page h1 {
    font-size: 2.5em;
    color: #ffffff;
    font-weight: bold;
    text-shadow: 2px 2px 4px #000000;
    width: 80%;
    margin: 0 auto 0.3em auto;
}
.title-page h2 {
    font-size: 1.3em;
    color: #ffffff;
    font-weight: bold;
    text-shadow: 1px 1px 3px #000000;
    margin-bottom: 0.5em;
}
.title-page .author {
    font-size: 1.1em;
    color: #ffffff;
    font-weight: bold;
    text-shadow: 1px 1px 2px #000000;
}
```

### TOC — MANDATORY Rules (Print PDF)

**Page placement:**
- TOC **must start on a new page**: wrap in `<div class="toc" style="page-break-before: always;">` and CSS `.toc { page-break-before: always; page-break-after: always; }`
- The section **after** the TOC (Part I, Chapter 1, etc.) **must also start on a new page**: ensure `page-break-after: always` on the TOC div, and `page-break-before: always` on the next heading
- Title page div must also have `page-break-after: always`

**Page numbers:**
- TOC **must include page numbers** synced to the actual manuscript pages
- Use the 2-pass rendering approach: Pass 1 renders with empty page numbers, extract page numbers with `pdftotext`, Pass 2 hardcodes the correct numbers
- Do NOT use CSS `target-counter()` — it does not work in WeasyPrint
- See `references/toc-page-number-sync.md` for the full 2-pass workflow

**Layout — no word wrapping:**
- Each TOC entry (chapter title + page number) **must fit on exactly ONE LINE** — no wrapping
- Use `white-space: nowrap` on the title cell
- Use `table-layout: auto` (NOT `fixed`) for the TOC table
- Do NOT use `<a>` tags in TOC cells for print PDFs — use plain text only (`<a>` tags cause WeasyPrint text corruption)
- Do NOT use `string-set` on h1/h2 — it corrupts all TOC text in WeasyPrint
- Use dotted leader cells (`border-bottom: 1px dotted #888`) between title and page number
- Part header rows use `colspan="3"` to match the 3-column layout

**TOC CSS:**
```css
.toc { page-break-before: always; page-break-after: always; }
.toc-table {
    width: 100%;
    table-layout: auto;
    border-collapse: collapse;
    margin: 0.5em 0;
    font-size: 10pt;
}
.toc-table td { padding: 0.2em 0; vertical-align: baseline; border: none; }
.toc-ch {
    width: auto;
    white-space: nowrap;
    padding-right: 0.5em;
    font-size: 9pt;
}
.toc-dots {
    width: 100%;
    border-bottom: 1px dotted #888;
    padding: 0 0.3em;
    font-size: 8pt;
    line-height: 1;
}
.toc-pge {
    width: 2em;
    white-space: nowrap;
    text-align: right;
    padding-left: 0.3em;
    font-size: 9pt;
}
.toc-part {
    font-weight: bold;
    font-size: 1.1em;
    padding-top: 0.8em;
    padding-bottom: 0.3em;
    border-bottom: 1px solid #333;
}
```

### Back Matter — MANDATORY Last Page (Added 2026-05-31, updated 2026-06-02)

Every book MUST include an expanded last page after the final chapter with these elements in order:

1. **Thank You Blurb** (4-5 sentences, expanded, in Bob J Mills' direct/sincere voice) — reference the specific journey in THIS book. For sci-fi: reference the fleet, the Moon, Mars, etc. For business: reference the practical tools the reader now has. For memoir: personal reflection.

2. **Series Sales Pitch** (MANDATORY for every book in a series) — After the thank-you, add a section that sells the SERIES:
   - **Series Hook** (3-5 sentences): Remind the reader what this series is about, the overarching story arc, what makes it special. Tailor to the specific series.
   - **Next Book Teaser** (2-3 sentences): Tease the NEXT book in the series by name, hint at stakes, create urgency. "Continue the journey in [Book Title] where..."
   - **Series Reading Order**: Numbered list of ALL books in the series with 1-line descriptions
   - **Complete Bibliography**: ALL Bob J Mills books across ALL series (organized by series/genre)
   - **Call to Action**: "Available on Amazon Kindle and Paperback" + QR codes

   **Series-specific hooks:**
   - *Age of Lightships*: Reference the 58-ship fleet, Proxima Centauri, the 120-year journey, what comes next
   - *Lunar Foundation*: Reference the Moon colony, survival, expanding civilization
   - *No Blue Sky*: Reference Mars, independence, the Red Planet's brutal beauty
   - *Cindy Lou Legal Capers*: Reference the cases, the humor, the quirky characters

3. **More From Bob Statement** (2-3 sentences, expanded) — mention Bob writes across hard sci-fi (space colonization, lunar settlements, Martian independence), business (AI, crisis management), and memoir. This single book is part of a larger body of work.

4. **Two QR Codes** — MIFECO (https://www.mifeco.com) + Amazon (https://www.amazon.com/s?k=bob+j+mills). Generated with `qrcode` library, ERROR_CORRECT_H, 300x300px. Saved as `qr_mifeco.png` and `qr_amazon.png` in book directory.

5. **Complete "Also by Bob J Mills" Bibliography** — ALL books published to-date, organized by series. Update with each new publication. Check `/mnt/usb_4tb/books/` for current inventory.

6. **Fan Club Blurb** — After the AI disclosure:

```
---

### Join My Fan Club!

**Join my Fan Club's Mailing List** to get access to free, exclusive content and to receive periodic updates on my various works in progress!

🌐 www.mifeco.com
```

#### PDF Generation (MANDATORY)
Every book MUST have a highly formatted PDF for KDP print:
- Generated via WeasyPrint from HTML or ReportLab
- Professional interior: title page, copyright, TOC with page numbers, all chapters, back matter
- Times New Roman 12pt body, 18pt headings
- 6"x9" trim, proper gutter margins, all fonts embedded
- Even page count (add blank page if needed)
- Page numbers start after front matter
- Save as `[BookName]_Print.pdf` in output directory

This blurb MUST appear at the very end of every book manuscript, after the AI disclosure line. It is the final thing the reader sees. Apply to ALL books in ALL series — fiction, business, and memoir.

See `publishing-workflow` skill section 2C and its `references/last-page-back-matter.md` for full HTML template and markdown template.

#### Dual Output Locations (MANDATORY for Cindy Lou books)

Cindy Lou books exist in TWO directory structures:
- **Pipeline source:** `.../Cindy_Lou_Legal_Capers/cindy-lou-series/book-N-name/` (where hermes_publish.py reads from)
- **Legacy/KDP:** `.../Cindy_Lou_Legal_Capers/book-N-name/` (where KDP packages are assembled)

When generating marketing files (Book_Description.txt, Author_Bio.txt, etc.), write to BOTH locations. The legacy directory is where the user and KDP pipeline expect to find files. Never write only to the `cindy-lou-series/` subdirectory.

#### Directory Structure Note for chapters_md Type

The `chapters_md` manuscript type looks for chapter files in `book_dir/chapters/` (preferred) or `book_dir/manuscript_src/` (fallback). When setting up a book for condensation:

1. Place condensed chapter files in `book_dir/chapters/` as `ch01.md` through `ch30.md`
2. Update BOOK_REGISTRY to point `dir` to the directory containing the `chapters/` subdirectory
3. Set `manuscript_type: "chapters_md"` in BOOK_REGISTRY
4. Delete old output files (PDF, EPUB, KDP ZIP) before regenerating to avoid confusion between old and new versions

#### Dual Output Locations (MANDATORY)

Cindy Lou books exist in TWO directory structures:
- **Pipeline source:** `.../Cindy_Lou_Legal_Capers/cindy-lou-series/book-N-name/` (where hermes_publish.py reads from)
- **Legacy/KDP:** `.../Cindy_Lou_Legal_Capers/book-N-name/` (where KDP packages are assembled)

When generating marketing files (Book_Description.txt, Author_Bio.txt, etc.), write to BOTH locations:
```python
for src_dir, dst_dir in [(series_dir, legacy_dir), (series_dir, series_dir)]:
    copy_marketing_files(src_dir, dst_dir)
```

The legacy directory at `.../Cindy_Lou_Legal_Capers/book-N-name/` is where the user and KDP pipeline expect to find files. Never write only to the `cindy-lou-series/` subdirectory.

#### Cleanup Before Rebuild

Always remove stale output files before generating new ones:
```bash
# In the book's output directory
rm -f *.pdf *.epub *.zip
# Or specifically
rm -f Retainer_to_Trouble_Print.pdf Retainer_to_Trouble.epub Sunward_Exodus_KDP_PACKAGE.zip
```

This prevents users from accidentally opening the old 474-page PDF when the new EPUB is only 182 pages.

Every book MUST include a marketing infographic image in the book root directory AND copied to `KDP_PACKAGE/`.

**File:** `Marketing_Infographic.png`

**Design requirements:**
- Bright colors and bold visual design
- Eye-catching composition suitable for social media posting (Instagram, Facebook, Twitter/X)
- Square 1024x1024 recommended (1:1) or vertical 1080x1350 (4:5)
- Generated using Flux.2 Max via OpenRouter (Pass 1), composited with PIL (Pass 2)
- No watermarks from image generation services

**Content requirements (ALL must be visually present):**
1. Book title prominently displayed
2. Author name credited visibly
3. Key sales hook, stat, or call-to-action (the "why you need this book" message)
4. Two QR codes: MIFECO (https://www.mifeco.com) + Amazon author page
5. "Available on Amazon and Kindle" callout
6. MIFECO branding or URL visible

**Generation workflow (two-pass):**
1. Pass 1: Generate base image with Flux.2 Max via OpenRouter — detailed prompt with brand colors, 1024x1024, include large text headers in prompt. Save raw as `Marketing_Infographic_raw.png`.
2. Pass 2: Composite with PIL — **resize art to 80% height** using LANCZOS (preserves all content including bottom text), add whitespace band below with QR codes, separator, heading, labels. **Never crop or overlay the art.** Track band positions sequentially and verify `avail_y + 20 < new_h`.
3. Save final as `Marketing_Infographic.png`
4. Copy final to `KDP_PACKAGE/Marketing_Infographic.png`

**QR sizing**: 220x220px (75% of 300px source), in 248x248px white cards (14px padding), 50px gap between cards.

See `image-generation-workflow` skill's `references/infographic-composition.md` for full code pattern and common pitfalls (band height math, content cut-off).

### Marketing & Compliance Content (MANDATORY — every book)

Every book MUST have a `Marketing_and_Compliance/` directory in the KDP package with the following files. All files MUST be plain `.txt` format — NOT `.md`. NO markdown symbols (`*`, `#`, `>`, etc.) in the marketing copy files.

**File requirements:**

| File | Required | Format | Spec |
|------|----------|--------|------|
| `Book_Description.txt` | YES | .txt | 80% of KDP max (3,200 chars of 4,000). No markdown. Plain text only. Hook in first 2 sentences. End with call to action. |
| `Back_Cover.txt` | YES | .txt | 150-250 words. No markdown. Compelling blurb that makes reader want to buy. |
| `Author_Bio.txt` | YES | .txt | 100-200 words. No markdown. Who the author is, what they write, series info. |
| `Keywords.txt` | YES | .txt | 5-7 keywords/phrases, one per line. No markdown. |
| `Title.txt` | YES | .txt | Full title + subtitle on separate lines. No markdown. |

### Pre-Upload Checklist (Checklist items continue...)
- [ ] All chapters present (count them in the PDF)
- [ ] Page count within target range (150-190 pages for 6x9" condensed novel; verify via word count: 36,000-45,000 words at 200-270 wpp)
- [ ] No front/back cover artwork (just text title page for V2.0+ rebuilds)
- [ ] No back cover content
- [ ] TOC lists everything with correct page numbers (hardcoded, NOT target-counter)
- [ ] Page count is reasonable (175-225 for a trade book at 6×9in)
- [ ] Final paragraph / closing reflection is present
- [ ] TOC entries each fit on ONE LINE (no wrapping — verified in pdftotext output)
- [ ] About the Author section present after final chapter (full bio, not just name)
- [ ] About_the_Author.txt standalone file exists in book root directory
- [ ] Author_Photo.jpg exists in book root directory
- [ ] Marketing_and_Compliance directory exists with all required .txt files
- [ ] All marketing files are .txt format (NOT .md)
- [ ] No markdown symbols (*, #, >, - bullets) in any marketing file
- [ ] Book_Description.txt is 80% of 4,000 char KDP limit (3,200 chars max)
- [ ] Back_Cover.txt is 150-250 words, compelling blurb, no spoilers
- [ ] Marketing_Infographic.png exists in book root directory AND KDP_PACKAGE/
- [ ] Infographic includes QR code linking to MIFECO.com
- [ ] Infographic includes QR code linking to Amazon author page
- [ ] Infographic states book is available on Amazon and Kindle
- [ ] Infographic includes book title, author name, and compelling hook/stat
- [ ] Infographic is generated using Flux.2 Max via OpenRouter (NOT Python/PIL for visual design)
- [ ] Infographic uses bright colors and bold design suitable for social media
- [ ] qr_mifeco.png and qr_amazon.png exist in book directory (300x300, ERROR_CORRECT_H)
- [ ] Last page includes expanded thank-you blurb (unique per book, in Bob's voice)
- [ ] Last page includes expanded "more from Bob" cross-genre statement
- [ ] Last page includes complete "Also by Bob J Mills" book list (all books, updated)
- [ ] **Fan Club blurb** present at the very end (after AI disclosure): "Join my Fan Club's Mailing List to get access to free, exclusive content and to receive periodic updates on my various works in progress!" with mifeco.com link
- [ ] Cover image fills at least 60% of cover height and 90% of cover width with content-relevant imagery
- [ ] Cover title is VERY BOLD and fills most of cover width (word-wrap if >2 words)
- [ ] Cover author name is bold, ~50% page width, near bottom
- [ ] Cover text has high contrast (shadow/glow) against background
- [ ] Cover generated using LLM image generation (not Python/PIL for visual design)

**Condensation target for 6x9" trade paperback (150-190 pages):**
- ~270 words/page → 40,500-51,300 total words
- 30 chapters → ~1,350-1,700 words per chapter
- Keep all plot beats, dialogue, and humor — cut atmospheric description and redundant internal monologue
- Target ~1,200-1,500 words per chapter for a tight read

### Chapter Spelling & Grammar Check (MANDATORY)

After writing or importing chapter manuscripts, run automated spell-check and grammar scan on EVERY chapter before generating EPUBs or PDFs.

**Run:** `python3 scripts/spell_check_chapters.py <manuscript_src_directory>`

**What the script checks:**
1. **Common misspellings** — 100+ known errors (teh→the, thier→their, recieve→receive, occured→occurred, seperate→separate, definately→definitely, goverment→government, enviroment→environment, realy→really, completly→completely, etc.)
2. **AI-isms** — Flags overused AI writing patterns: "delve", "leverage", "tapestry", "intricate", "fostering", "vibrant", "pivotal", "robust", "utilize", "facilitate", "furthermore", "moreover", "nonetheless", "consequently", "subsequently"
3. **Repeated words** — Catches accidentally doubled words via regex `\b(\w+)\s+\1\b`
4. **Double spaces** — Double spaces after periods or within sentences
5. **Em-dash consistency** — Normalize `&mdash;` to unicode `—`, use ` — ` (spaced) for narrative

**Fix all issues found before publishing.** Do not ship manuscripts with known spelling errors.

### Chapter Image Embed (MANDATORY)

Every chapter MUST have a B&W illustration image embedded in the EPUB. Images are stored in `generated_images/` as `ch01.png` through `ch40.png` (or in `generated_images/illustrations/ch01_sketch.png` for older books).

**Image location priority:**
1. `generated_images/illustrations/chNN_sketch.png` (older books)
2. `generated_images/chNN.png` (newer books)
3. If no image exists, generate one using Gemini with a prompt describing the chapter content

**Embed pattern in EPUB chapter HTML:**
```html
<div class="chapter-image">
  <img src="images/ch01.png" alt="Chapter 1 illustration"/>
</div>
<div>
  <h2>Chapter 1</h2>
  <h3>Chapter Title</h3>
  [chapter content]
</div>
```

**Image requirements:**
- Grayscale (black and white), high contrast
- Minimum 1024x1024 pixels
- Relevant to chapter content (space scenes, ships, technology, etc.)
- No text or watermarks in the image
- Stored as PNG format
- Embedded as `epub.EpubItem` with `media_type='image/png'` and `uid='chNN-img'`

## EPUB Generation — Use hermes-publish

**For all new EPUB builds, use the unified `hermes-publish` pipeline** which provides a single ZIP-based EPUB 3 builder (`step_epub.py`) that works for all book types. This resolves the previous ebooklib vs manual ZIP inconsistency.

```bash
cd /mnt/usb_4tb/books
python3 hermes_publish.py --book moon-rock --steps epub
```

The unified builder:
- Uses manual ZIP-based EPUB 3 (no external dependencies like ebooklib)
- Handles all 4 manuscript types: chapters_md, chapters_xhtml, manuscript_md, single_md
- Produces proper EPUB 3 structure: mimetype, container.xml, content.opf, nav.xhtml, per-chapter XHTML
- Includes cover image with `properties="cover-image"` in OPF manifest

### EPUB Pitfalls (preserved for reference)

- **EPUB `&nbsp;` entity invalid in XHTML**: `&nbsp;` is an HTML entity that is NOT valid in XHTML (which EPUB uses). All `&nbsp;` entities in chapter content MUST be replaced with `&#160;` before embedding in XHTML. This includes indentation entities from markdown source files. The `md_to_html_simple()` function should do this replacement. If post-processing EPUB files, use `content.replace('&nbsp;', '&#160;')` on all XHTML files.
  - **Symptom**: Every chapter shows "Entity 'nbsp' not defined" error in EPUB readers. The page renders blank or shows raw error text instead of chapter content.
  - **Fix**: In `md_to_html_simple()`, add `line = line.replace('&nbsp;', '&#160;')` as the first line of the loop. Also apply to any content passed to EPUB XHTML generation.
  - **Verification**: After regenerating EPUB, extract a chapter XHTML from the ZIP and search for `&nbsp;` — there should be zero occurrences. All indentation should use `&#160;` or CSS padding instead.

- **Chapter title extraction — plain text titles**: Chapter files may have titles as plain text on the first line (e.g., "The Letterhead Lies") OR as markdown headers (e.g., "# Chapter 1: The Letterhead Lies"). The extraction logic must handle BOTH formats. Additionally, strip "Chapter N:" prefixes from extracted titles to avoid duplication when the EPUB generates `<h2>Chapter N: {title}</h2>` headers. Pattern: `re.sub(r'^Chapter\\s+\\d+:\\s*', '', title)`.

- **Chapter title appears as first paragraph body text**: If the chapter title appears both in the `<h2>` header AND as the first paragraph of body content, the title line from the chapter file is being passed through as body text. In the EPUB generation loop, strip the title line before converting to HTML: check if first line starts with `#` OR is a short plain text line (< 60 chars, not starting with `---`), and if so, remove it before `md_to_html_simple()`.

- **Python bytecode cache after pipeline changes**: After modifying any `hermes_publish/` Python module, ALWAYS clear the bytecode cache: `find /mnt/usb_4tb/books/hermes_publish/ -name "__pycache__" -type d -exec rm -rf {} +`. Failure to do this causes the pipeline to run stale code, producing EPUBs with old bugs that appear to be "not fixed" even after source changes.
```python
if book["manuscript_type"] == "chapters_md":
    cl = content.split('\n')
    if cl and (cl[0].strip().startswith('#') or 
               (len(cl[0].strip()) < 60 and not cl[0].strip().startswith('---') and not cl[0].strip().startswith('*'))):
        content = '\n'.join(cl[1:]).strip()
```

- **Python bytecode cache after pipeline changes**: After modifying any `hermes_publish/` Python module, ALWAYS clear the bytecode cache: `find /mnt/usb_4tb/books/hermes_publish/ -name "__pycache__" -type d -exec rm -rf {} +`. Failure to do this causes the pipeline to run stale code, producing EPUBs with old bugs that appear to be "not fixed" even after source changes.

### Stale output files**: Delete old PDF/EPUB/ZIP outputs before regenerating to avoid user confusion between old (e.g., 474-page) and new (e.g., 180-page) versions.
- Also delete old mixed-case manuscript variants (`Clause_for_Alarm_MANUSCRIPT.md`) when the lowercase variant (`clause-for-alarm_MANUSCRIPT.md`) replaces them.

### File Placement Discipline — Dual Directory Requirement

KDP build output files (EPUB, PDF, KDP ZIP) and condensed chapter files must exist in BOTH directory locations:

1. **Primary series path:** `cindy-lou-series/[book]/output/` and `cindy-lou-series/[book]/chapters/`
2. **Legacy path:** `Cindy_Lou_Legal_Capers/[book]/output/` and `Cindy_Lou_Legal_Capers/[book]/chapters/`

The user checks both locations. Never assume one is sufficient.

### Page Count Targeting for 6x9" Condensed Books

Target: 150-190 pages at 6x9" format:
- Total words (with front/back matter): ~37,500-55,000
- Chapter-only words (without ~5K front/back matter): ~32,500-50,000
- Per-chapter for 30 chapters: ~1,080-1,670 words each
- At 230-270 words per page for a 6x9" formatted book

### Chrome Browser Installation (for DreamHost deployment)

When the browser tool needs Chrome and it's not installed:
1. Download Chrome separately: `wget "https://storage.googleapis.com/chrome-for-testing-public/149.0.7827.54/linux64/chrome-linux64.zip" -O /tmp/chrome-linux64.zip`
2. Extract: `python3 -c "import zipfile; zipfile.ZipFile('/tmp/chrome-linux64.zip').extractall('/tmp/chrome-install')"`
3. The browser tool should detect it automatically. If not, the path is `/tmp/chrome-install/chrome-linux64/chrome-linux64/chrome`

### Marketing Files — Dual Location Requirement

KDP marketing files must exist in BOTH locations:
1. Book root directory: `Book_Description.txt`, `Back_Cover.txt`, `Author_Bio.txt`, `Author_Photo.jpg`, `Keywords.txt`, `Title.txt`
2. `Marketing_and_Compliance/` subdirectory: same files (plus `KDP_AI_Disclosure.md`)

### EPUB Pitfalls (preserved for reference)

- **EPUB `&nbsp;` entity invalid in XHTML**: `&nbsp;` is an HTML entity that is NOT valid in XHTML (which EPUB uses). All `&nbsp;` entities in chapter content MUST be replaced with `&#160;` before embedding in XHTML. This includes indentation entities from markdown source files. The `md_to_html_simple()` function should do this replacement. If post-processing EPUB files, use `content.replace('&nbsp;', '&#160;')` on all XHTML files.
  - **Symptom**: Every chapter shows "Entity 'nbsp' not defined" error in EPUB readers. The page renders blank or shows raw error text instead of chapter content.
  - **Fix**: In `md_to_html_simple()`, add `line = line.replace('&nbsp;', '&#160;')` as the first line of the loop. Also apply to any content passed to EPUB XHTML generation.
  - **Verification**: After regenerating EPUB, extract a chapter XHTML from the ZIP and search for `&nbsp;` — there should be zero occurrences. All indentation should use `&#160;` or CSS padding instead.

- **Chapter title extraction — plain text titles**: Chapter files may have titles as plain text on the first line (e.g., "The Letterhead Lies") OR as markdown headers (e.g., "# Chapter 1: The Letterhead Lies"). The extraction logic must handle BOTH formats. Additionally, strip "Chapter N:" prefixes from extracted titles to avoid duplication when the EPUB generates `<h2>Chapter N: {title}</h2>` headers. Pattern: `re.sub(r'^Chapter\\s+\\d+:\\s*', '', title)`.

- **Chapter title appears as first paragraph body text**: If the chapter title appears both in the `<h2>` header AND as the first paragraph of body content, the title line from the chapter file is being passed through as body text. In the EPUB generation loop, strip the title line before converting to HTML: check if first line starts with `#` OR is a short plain text line (< 60 chars, not starting with `---`), and if so, remove it before `md_to_html_simple()`.

- **Python bytecode cache after pipeline changes**: After modifying any `hermes_publish/` Python module, ALWAYS clear the bytecode cache: `find /mnt/usb_4tb/books/hermes_publish/ -name "__pycache__" -type d -exec rm -rf {} +`. Failure to do this causes the pipeline to run stale code, producing EPUBs with old bugs that appear to be "not fixed" even after source changes.

- **EPUB EpubHtml.content is body-only**: `epub.EpubHtml.content` should contain ONLY body HTML (e.g., `<div class="cover"><img src="..."/></div>`), NOT a full HTML document with DOCTYPE/head. Full documents cause `get_body_content()` → NULL → "Document is empty" crash.
- **EPUB set_cover() creates duplicate empty cover.xhtml**: Calling `book.set_cover()` auto-creates a cover.xhtml with EMPTY body. If you also manually create a cover xhtml page, you get a duplicate zip warning AND the empty-body cover.xhtml causes "Document is empty" parse errors. Solution: either (a) DON'T call `set_cover()` and just add the cover image as a regular EpubItem + create your own cover xhtml page with proper body content, or (b) call `set_cover()` but DON'T create a separate cover xhtml page.
- **EPUB RGBA Image Pitfall**: LLM-generated PNG images are often RGBA (with alpha channel). The EPUB builder will fail when trying to convert these to JPEG for the EPUB interior. Fix: batch-convert all images to RGB before building EPUB.
- **Gemini image model**: Use `google/gemini-2.5-flash-image` (NOT `...-preview` which 404s). Gemini returns 1024x1024 by default — for KDP covers (2560x1600), request 1.6:1 aspect ratio in prompt and upscale/crop with PIL LANCZOS after.
- **KDP sign-in requires OTP**: Amazon KDP sign-in always triggers two-step verification (OTP sent to phone). The agent CANNOT complete KDP sign-in autonomously — it must stop and ask the user for the OTP code after entering password.

- **Page count estimation for condensed books**: 150-190 pages at 6x9" = ~37,500-51,300 words at 250 words/page. Chapter words alone (~30K-43K) plus front/back matter (~5K) give the total. Always check the PDF page count (via pypdf PdfReader) not just word count.

- **Two MANUSCRIPT.md files causing wrong selections**: Having both lowercase (`retainer-to-trouble_MANUSCRIPT.md`) and mixed-case (`Retainer_to_Trouble_MANUSCRIPT.md`) manuscript files causes PDF generators to pick the wrong (old/long) version. When condensing books, delete the old mixed-case manuscript after the pipeline generates the new one. The pipeline always writes lowercase filenames; old build scripts wrote mixed-case.

- **Book condensation approach — manual rewriting required**: Mechanical paragraph-filtering (keeping every other paragraph, keeping only dialogue) does NOT produce readable condensed chapters. The novels are already tightly written with short dialogue-heavy paragraphs. Condensation requires reading each chapter and rewriting it at ~65-75% of the original word count while preserving all plot beats, humor, and voice. Target ~900-1,100 words per chapter for a 30-chapter book at 150 pages.

### Pitfalls (continued)
- **TOC — all rules consolidated**: See **TOC — MANDATORY Rules** in the Front Matter section. Key pitfalls: `string-set` corrupts text, `<a>` tags corrupt text, `table-layout: fixed` causes wrapping, `<a>` tags must not be used in TOC cells for print PDFs, page numbers must be hardcoded (not `target-counter`).
- **Forms also need grayscale**: When converting infographics to B&W, also check and convert ALL images in `generated_images/forms/` — these are often missed because they are separate from the `infographics/` directory. Apply the same grayscale + 1.5x contrast pipeline.
- **Chapter title extraction Entity handling**: Check both `<h1>` and `<h2>`. Handle `&mdash;` HTML entity in the regex (not just literal dash characters). Only fall back to filename if neither h1, h2, nor `<title>` tag has content. Using filenames (ch001, ch002) as TOC titles is wrong.
- **"Chapter N Chapter N" doubled titles**: The title extraction regex did not strip the prefix. Check that `&mdash;` is handled. When rewriting chapters, ensure the `<h1>` content is "Chapter N — Title" not "Chapter N — Chapter N — Title".
- **TOC table colspan**: `colspan` on part header rows must match total column count (e.g. `colspan="3"` for a 3-column TOC). Mismatched colspan causes weasyprint cell-ignore warnings.
- **Subagent chapter delegation — single chapter only**: When using `delegate_task` to write chapters, delegate ONE chapter per subagent, not batches. Batching 3+ chapters per subagent causes 600s timeouts. Each subagent should read the previous chapter(s) for voice continuity, receive explicit style rules and character names, and save to a specific file path. Running 3 concurrent subagents (one per book) creates an efficient pipeline: ~3 chapters every 5-8 minutes. See `references/bulk-manuscript-writing.md` for the full pattern.
- **Subagent "Window too small" failures**: Do NOT delegate full-book rewrites to subagents. Write small Python scripts that read/write chapter files sequentially.
- **Triple-quoted Python strings with apostrophes**: NEVER use triple-quoted strings containing apostrophes in HTML generation scripts. Use helper functions like `p(text)` and `fp(text)`.
- **WeasyPrint base64 images slow rendering**: Use `sed '/data:image/d'` to strip when cover art isn't needed.
- **weasyPrint binary location**: On this system, weasyprint is installed in the hermes-agent venv at `/home/bob/.hermes/hermes-agent/venv/bin/python3`. The `pip3` binary may not be on the system PATH — use `/home/bob/.hermes/hermes-agent/venv/bin/pip3` or `python3 -m pip` from that venv.
- **PDF page verification**: Use `pypdf` (import as `from pypdf import PdfReader`) to verify page count and inspect text content per page. Install with `/home/bob/.hermes/hermes-agent/venv/bin/pip3 install pypdf`. This is the most reliable way to check PDF structure after weasyprint renders.
- **Missing author bio**: Every book MUST have a full "About the Author" section (not just the author's name) after the final chapter, AND a standalone `About_the_Author.txt` file in the book root directory. A single line with just the author name is insufficient. Include: who they are, what they write, which series this book belongs to, and a personal closing line. Also include `Author_Photo.jpg` in the book directory.
- **Page-break-after on title-page and toc divs**: Both `.title-page` and `.toc` divs MUST have `page-break-after: always` (not `none`). Without it, the next section starts on the same page.
- **Title page contrast**: Title and author text MUST be bold, white, with high contrast (dark background or text shadow). Title must fill ~80% of page width. Never use light text on a light background.
- **Marketing file format**: All Marketing_and_Compliance files MUST be .txt (never .md). NO markdown symbols (*, #, >, - bullets, []() links) in marketing files. Book description must be 80% of KDP 4,000 char limit (3,200 chars max). Count ALL characters including spaces.
- **Chapter cleanup — duplicate paragraphs**: AI-generated or multi-draft chapters often contain duplicated entire paragraphs. Use a regex-based dedup: extract all `<p...>...</p>` blocks, compare cleaned text content, remove second occurrences of any block >30 chars. Then verify p-tag balance (open count must equal close count).
- **Chapter cleanup — double scene breaks**: `<p class="scene">* * *</p><p class="scene">* * *</p>` appearing consecutively is always wrong — collapse to a single scene break. Fix with simple string replace first before other edits.
- **Chapter cleanup — mixed em-dash formats**: `&mdash;` HTML entities and unicode `—` should be normalized to unicode `—` for consistency. Also fix spaced vs unspaced em-dashes: use ` — ` (spaced) for narrative prose, no spaces for compound words.
- **Chapter cleanup — p-tag mismatch after dedup**: Removing duplicate paragraphs can strip a `</p>` tag, leaving open/close counts mismatched. After any paragraph removal, always verify `<p` count equals `</p>` count per file. Add missing `</p>` at end of the affected line.
- **Chapter cleanup — automated script**: For bulk cleanup of multiple chapter files, use `scripts/cleanup-chapters.py` which handles all four issues above in one pass. Run: `python3 scripts/cleanup-chapters.py <manuscript_src_directory>`. See `references/chapter-cleanup-and-cover-techniques.md` for the full regex patterns and techniques.
- **Long-running background tasks**: Use `terminal(background=True)` with output redirected to log file. Check progress via `tail` not `process(action="poll")` which buffers all output.
- **Bulk manuscript writing**: For 40+ chapters, write each chapter to disk immediately after LLM generation. Run as background process. ~10-15s per chapter including API latency.
- **Partial KDP_PACKAGE anti-pattern**: A book directory with `KDP_PACKAGE/Marketing_and_Compliance/` (all text files present) but missing `KDP_PACKAGE/Kindle/`, `KDP_PACKAGE/Print/`, and `KDP_PACKAGE/*.zip` is NOT a complete KDP package. It's marketing-only. During audits, check the *contents* of KDP_PACKAGE, not just the directory existence.

### Website & Reader Magnet Deployment (Added 2026-06-01)

**Subagent delegation**: Single-file tasks only per subagent. Multi-file batch tasks (4+ pages, 3+ novellas) timeout at 600s. Delegate one chapter/page/novella per subagent.

**File writes**: Content >15KB can truncate silently. Use `execute_code` with Python for large files.

**DreamHost deployment**: Password auth required. PHP 7.4+ available. Use paramiko SFTP or rsync. Weekly cron job auto-deploys (Mondays 9 AM, job ID tracked in memory).

**Reader magnets**: 2,500-3,500 words, complete story with hook into Book 1. EPUB + PDF. 4-email welcome sequence: deliver → thank → showcase → cross-promote. Place in back matter, series pages, and author website.

**add-book-to-pipeline skill**: Now includes Steps 6 (reader magnet) and 7 (website deployment) — always update both when adding a new book.
