---
name: manuscript-publishing-package
title: Manuscript Publishing Package — KDP-Ready ZIP
description: Build a complete .zip package with all KDP submission deliverables for a finished 6"×9" book. Covers Kindle description, cover art (400 DPI PNG), front matter, author bio, full manuscript PDF with front/back matter, TOC, back cover content, and EPUB 3 export with KDP-compliant validation.
category: publishing
triggers:
  - "publish this book"
  - "prepare for kdp"
  - "book deliverable"
  - "zip package"
  - "manuscript package"
  - "ready for review"
  - "review copy"
  - "review pdf"
  - "final publication"
  - "epub"
  - "kindle ebook"
  - "ebook format"
version: 1.0.0
author: MIFECO
tags: [publishing, kdp, manuscript, cover, kindle, pdf, zip, package, 6x9, 400dpi]
---

## 🔍 MemPalace Query (MANDATORY FIRST STEP)
Before proceeding, query MemPalace for existing context:
```python
import sys, os; sys.path.insert(0, os.path.expanduser('~/.hermes/mempalace'))
import embed; embed.init_embedding(os.path.expanduser('~/.hermes/mempalace'))
results = embed.search_embeddings("manuscript publishing package KDP ZIP EPUB PDF cover art", k=5)
```
This retrieves previous decisions, domain-specific context, and lessons learned from the vector memory store.

# Manuscript Publishing Package — KDP-Ready ZIP

## Book Format

All deliverables target **6" × 9"** (standard trade paperback).

---

## Package Contents (.zip)

The final ZIP archive must contain exactly these files in this structure:

```
{BOOK_TITLE_NO_SPACES}_Publishing_Package/
├── Kindle_Description/
│   ├── {Book_Title}.txt               ← Book title only
│   └── Description_{Book_Title}.pdf    ← 3,950 characters max
├── Book_Cover/
│   └── {Book_Title}_Cover.png          ← 6" × 9", 400 DPI, color, bold text, graphic + title + author
├── Front_Matter/
│   ├── Front_Matter_{Book_Title}.pdf   ← 3,950 characters max
│   └── Author_Bio_{Book_Title}.pdf     ← 1,500 characters max
├── Manuscript/
│   └── {Book_Title}_Manuscript.pdf     ← 150–200 pages, 50–60 chapters
└── Back_Cover/
    ├── Author_Bio.txt                  ← Author bio text
    ├── Back_Cover_Matter.txt           ← Back cover body text
    └── Author_Photo.png                ← Author photograph
```

---

## Step-by-Step Build Workflow

### Phase 1: Assess & Prepare

1. **Confirm the manuscript is finished.** Count chapters: target is **50–60 chapters** at roughly 150–200 pages when typeset at 6"×9".
2. **Confirm the source manuscript format.** Prefer HTML (with CSS for print) or Markdown that can be converted to HTML.
3. **Identify the book's title, author name, and any existing cover art.**
4. **Calculate page count estimate:**
   - Average ~2,500–3,500 characters per page at 6"×9" with standard 11–12pt type
   - 150–200 pages = roughly 375,000–700,000 characters of body text

### Phase 2: Build Kindle Description

1. **Write the book title** to `{Book_Title}.txt` — plain text, title only.
2. **Write the Kindle description** (max **3,950 characters**) as a compelling book description:
   - Hook the reader in the first line
   - Describe the story (fiction) or the problem/solution (non-fiction)
   - Include genre-appropriate keywords naturally
   - End with a call to action
   - Save as `Description_{Book_Title}.pdf`

### Phase 3: Build Cover Art

1. **Verify author name** against the user's current profile before generating — check memory for the correct form (e.g., "Bob J Mills").

2. **Confirm subtitle and author name** with the user before generating — these get baked into the artwork.

3. **Generate raw cover art** via OpenRouter API using `google/gemini-2.5-flash-image` (preferred) or `black-forest-labs/flux.2-max` (fallback). The prompt must specify the scene, atmosphere, "leave top 30-40% as clean negative space", "no text/logos/watermarks", "2:3 portrait aspect ratio". Never bake text into the AI generation prompt — apply typography in a separate step. See `openrouter-image-generation-workflow` skill for detailed API call patterns.

4. **Apply typography and resize** to exactly **6" x 9" at 400 DPI**:
   - **Pixel dimensions**: 2,400 x 3,600 pixels
   - **Color**: Full color (RGB) | **Format**: PNG
   - **Canvas from square source**: Gemini returns 1024x1024. Use full-bleed crop: scale 1.5x to 1536px height, center-crop width to 1024px. If art has critical edge content, use letterbox (60% top / 40% bottom black bars) instead.
   - **Dark gradient overlays** for text readability: alpha 0->130 over top 42% (title zone), alpha 0->120 over bottom 14% (author zone)
   - **Typography**: DejaVuSans-Bold.ttf or LiberationSans-Bold.ttf, shadow for legibility:
     - Title: 170pt, one word per line, centered in top 35%
     - Subtitle: 48pt, 1-2 lines below title, centered
     - Author: 90pt, centered ~160px from bottom
   - **Save at 400 DPI**: `cover.save(path, "PNG", dpi=(400, 400))`
   - **File**: `{Book_Title}_Cover.png`

5. **Post-generation verification**: 2400x3600 pixels, valid PNG, file size > 500KB

### Phase 4: Build Front Matter

1. **Write front matter text** (max **3,950 characters**) as a single document:
   - Copyright notice (© {year} {author}. All rights reserved.)
   - Disclaimer (this is a work of fiction / non-fiction as appropriate)
   - ISBN or edition notice (if applicable)
   - Introduction page thanking readers for choosing the book
   - **Request for help**: A personal note asking readers to leave a review on Amazon — explain how much it helps indie authors
   - Save as `Front_Matter_{Book_Title}.pdf`

2. **Write author bio** (max **1,500 characters**):
   - Who the author is
   - What they write / their expertise
   - Notable achievements
   - Where to find them online
   - Save as `Author_Bio_{Book_Title}.pdf`

### Phase 5: Build Manuscript PDF

1. **Convert manuscript to print-ready HTML** with CSS targeting 6"×9" output:
   - Page size: 6in × 9in
   - Margins: 0.75in all around
   - Font: 11–12pt serif for body (e.g., Garamond, Times New Roman), sans-serif for headings
   - Line height: 1.15–1.2
   - Paragraph spacing: 0pt after, first-line indent 0.2in

2. **Structure the manuscript in order:**
   - **Front matter page**: Copyright + disclaimer (from Phase 4)
   - **Introduction page**: Thank-you + review request (from Phase 4)
   - **Table of contents**: All chapter titles listed with page numbers (use PDF outlines or manual TOC)
   - **Book content**: Chapters 1 through N (50–60 chapters expected)
     - Each chapter starts on a new page
     - Chapter headings styled consistently
     - Tables, charts, and images **formatted to fit within 6"×9"** (max width 4.5in)
   - **Last page matter**: A closing essay about why this book matters — the author's personal reflection on why this book is important to readers

3. **Generate the PDF**:
   ```python
   # Using WeasyPrint
   import weasyprint
   html_content = """<!DOCTYPE html><html><head><style>
     @page { size: 6in 9in; margin: 0.75in; }
     body { font-family: 'DejaVu Serif', serif; font-size: 11pt; line-height: 1.2; }
     h1, h2, h3 { font-family: 'DejaVu Sans', sans-serif; }
     .toc { page-break-after: always; }
     .chapter { page-break-before: always; }
     img { max-width: 4.5in; height: auto; }
     table { font-size: 9pt; width: 100%; }
     .front-matter { page-break-after: always; }
     .last-page { page-break-before: always; }
   </style></head><body>
     ... all content sections ...
   </body></html>"""
   weasyprint.HTML(string=html_content).write_pdf('{Book_Title}_Manuscript.pdf')
   ```

4. **Verify the output:**
   - Page count: 150–200 pages ✅
   - Each chapter starts on a new page ✅
   - TOC lists all chapters with page numbers ✅
   - Images/charts fit within 4.5in width ✅

> **Automated TOC page numbers:** Use the `scripts/toc-page-numbers.py` script to inject WeasyPrint `target-counter()` links into any HTML manuscript — it adds heading IDs, converts TOC entries to `<a>` tags, and injects the required CSS in one pass.

### Phase 5.5: Generate Review PDF (pre-publication review copy)

Before building the full KDP package, generate a clean review PDF for the author to proofread. This is NOT the final submission PDF — it's a review copy with no cover artwork, just the front matter + TOC + full manuscript body.

**Review PDF rules:**
- **No cover pages** — skip the front cover illustration and back cover. Include only: title page (text), copyright, TOC, body content, closing reflection.
- **TOC MUST have page numbers** — use the `scripts/toc-page-numbers.py` script to inject table-based `target-counter()` links (avoids float artifacts on wrapped text). Run:
  ```bash
  python3 scripts/toc-page-numbers.py manuscript.html
  ```
- **Images via file:// paths, not base64** — WeasyPrint silently fails on large base64 data URIs (5MB+). Reference images as absolute `file://` URLs:
  ```html
  <img src="file:///home/user/project/images/part1.png" alt="...">
  ```
- **Interior image specs** — 1024×1024 pixels at ~293 DPI (when displayed at 3.5in width) is sufficient for pencil sketches / interior illustrations. Use JPEG quality 75, grayscale mode:
  ```python
  from PIL import Image
  img = Image.open('source.png').convert('L')
  img.save('output.jpg', 'JPEG', quality=75, optimize=True)
  # Result: ~240KB vs 750KB+ for PNG at same resolution
  ```
- **Page count:** Target 150–200 pages at 6"×9" (not 50–60 chapters — shorter memoir chapters also work; what matters is total character count ~375K–700K).
- **🪤 WeasyPrint pitfalls:** See `references/weasyprint-pitfalls.md` for a detailed reference on base64 image failures, wrapped-text TOC artifacts, heading ID truncation bugs, image optimization, and page-break nesting issues — all encountered during production.

### Phase 6: Build Back Cover

1. **Write author bio text** for the back cover (can differ from the front-matter bio — shorter, punchier):
   - 2–3 sentences
   - Save as `Author_Bio.txt`

2. **Write back cover matter**: A hook or teaser that makes someone pick up the book:
   - For fiction: A gripping short blurb
   - For non-fiction: The core promise in one paragraph
   - Save as `Back_Cover_Matter.txt`

3. **Add author photo**: A headshot or author image:
   - Source/ask the user for one, or use a placeholder
   - Save as `Author_Photo.png`

### Phase 7: Package & Deliver

1. **Create the ZIP archive**:
   ```bash
   cd {output_dir}
   zip -r {Book_Title}_Publishing_Package.zip {Book_Title}_Publishing_Package/
   ```

2. **Deliver to the user** via Telegram MEDIA: link:
   ```
   MEDIA:/path/to/{Book_Title}_Publishing_Package.zip
   ```

3. **Also deliver individual key files** that are useful standalone:
   - The cover PNG (for preview)
   - The manuscript PDF (for review)
   - The Kindle description TXT

---

## Character Count Reference

| Item | Max Chars | Typical Length |
|------|-----------|---------------|
| Kindle description | 3,950 | 2,500–3,500 |
| Front matter | 3,950 | 2,000–3,500 |
| Author bio (front) | 1,500 | 500–1,200 |
| Back cover bio | No limit | 300–500 |
| Back cover matter | No limit | 200–400 |

---

## Cover Art Specs (6" × 9" at 400 DPI)

| Property | Value |
|----------|-------|
| Width | 2,400 px |
| Height | 3,600 px |
| DPI | 400 |
| Aspect ratio | 2:3 (same as 6"×9") |
| Color mode | RGB |
| Format | PNG |
| Style | Bold white stacked typography, full-bleed artwork |
| Required elements | Artwork/graphic, book title, author name |

---

## Print-Ready Manuscript Specs (6" × 9")

| Property | Value |
|----------|-------|
| Page size | 6in × 9in |
| Margins | 0.75in all sides |
| Body font | 11–12pt serif |
| Heading font | Sans-serif (bold) |
| Line height | 1.15–1.2 |
| Paragraph indent | 0.2in first line |
| Chapter start | New page (page-break-before: always) |
| Max image width | 4.5in |
| Format | PDF |

---

## Page Count Estimation

The manuscript should be **150–200 pages** when typeset at 6"×9".

Rough guide:
- Average ~2,500–3,500 characters per page at 6"×9" with standard 11–12pt type
- 150–200 pages = roughly 375,000–700,000 characters of body text
- Chapter count varies by genre: novels 50–60 chapters, memoirs 10–20 chapters, non-fiction 8–15 chapters. What matters is total character count, not chapter count.

If the manuscript is too short, consider:
- Expanding chapters with more detail
- Adding supplementary material (appendix, glossary, further reading)
- Adding chapter-opening quotes or illustrations

If the manuscript is too long:
- Tighten prose
- Consolidate short chapters
- Reduce supplementary material

---

## Pitfalls

| Pitfall | Why It Happens | How to Avoid |
|---------|---------------|--------------|
| **Cover wrong DPI** | 72 DPI source images scaled to 400 DPI | Always generate at 2,400×3,600 px from scratch — never upscale a low-res image |
| **Manuscript too short** | 20 chapters when 50–60 expected | Count chapters early; if below target, add content before building PDF |
| **Images overflow page** | Images wider than 4.5in get clipped | Set `img { max-width: 4.5in; height: auto; }` in the print CSS |
| **Images not rendering in WeasyPrint PDF** | Large base64 data URIs (5MB+) silently fail; WeasyPrint just skips them | Use `file://` absolute paths instead of data URIs. Keep individual images under 1MB. For interior illustrations, JPEG at quality 75 gives excellent quality at ~240KB (vs 750KB+ for PNG). See `references/weasyprint-pitfalls.md` |
| **Character count exceeded** | Description or front matter goes over 3,950 chars | Count characters with `wc -c` and trim ruthlessly — KDP truncates |
| **Font not embedded in PDF** | System font not available at render time | Use DejaVu fonts (Serif + Sans) — they're standard on Linux and embed reliably |
| **TOC `target-counter()` does NOT work in WeasyPrint** | `content: target-counter(attr(href), page)` silently produces wrong/missing page numbers. `string-set` on h1/h2 corrupts all TOC text (characters from first entry overlay onto every other). `<a>` tags in TOC cells also cause corruption. | Use the 2-pass approach: Pass 1 renders with empty page numbers, extract via `pdftotext`, Pass 2 hardcodes correct numbers. Use plain text in TOC cells (no `<a>` tags). See `book-deliverable-kdp` skill for the full TOC spec and CSS. |
| **No author bio at end of book** | Easy to overlook; a single line with just the author name is insufficient | Every book MUST have a full "About the Author" section (who they are, what they write, which series, personal closing line) after the final chapter, AND a standalone `About_the_Author.txt` file in the book root directory. |
| **Partial KDP package (marketing-only)** | A `KDP_PACKAGE/` directory with only `Marketing_and_Compliance/*.txt` but missing `Kindle/`, `Print/`, images, and zip is NOT publishable | Before calling a book "KDP-ready," verify the KDP_PACKAGE contains Kindle cover, print PDF, chapter images, and the final zip. Books 2-4 of the Age of Lightships series had complete marketing text but zero publishing assets inside KDP_PACKAGE. |
| **Title page low contrast** | Light text on light background, or no text shadow | Title and author must be bold, white, high contrast. Use dark background bars or text-shadow. Title fills ~80% of page width. See `book-deliverable-kdp` skill for the title-page CSS template. |

---

## Enrichment Gate: No Emails Without a to: Address

**CRITICAL RULE: Every email in the EMAILS viewer must have a VALID `to:` recipient email address.**

Template placeholders (`{{email}}`, `{{name}} <{{email}}>`) are NOT valid — they will be rejected by the viewer's enrichment gate.

### How it works

1. **Emails with real `to:` addresses** (e.g., `alice@testcorp.com`) appear in the Emails viewer tab with Send and Delete buttons.
2. **Emails without real `to:` addresses** (marked `NEEDS_ENRICHMENT`) are moved to the **🔍 Enrichment** tab. They cannot be sent until paired with a valid recipient.
3. **When sending**, the system validates that the `to:` field contains a real email address. If not, it blocks the send with an alert.

### Enrichment Workflow



## Verification Checklist

Before delivering, verify each item:

- [ ] ZIP archive created and can be extracted
- [ ] Kindle description .txt exists and is ≤ 3,950 chars
- [ ] Kindle description .pdf exists and matches .txt content
- [ ] Cover .png is 2,400 × 3,600 px (6" × 9" at 400 DPI)
- [ ] Cover shows title, author name, and graphic
- [ ] Front matter .pdf ≤ 3,950 chars
- [ ] Author bio (front) .pdf ≤ 1,500 chars
- [ ] Manuscript .pdf is 150–200 pages
- [ ] Manuscript has 50–60 chapters
- [ ] Manuscript has copyright/disclaimer page
- [ ] Manuscript has introduction/review-request page
- [ ] Manuscript has table of contents
- [ ] Manuscript has last-page reflection
- [ ] Author bio .txt exists
- [ ] Back cover matter .txt exists
- [ ] Author photo .png exists (or placeholder)
- [ ] All filenames match the {Book_Title} convention consistently

**Review PDF checklist (Phase 5.5):**
- [ ] TOC page numbers match actual chapter/part start pages (verify with pdftotext)
- [ ] No concatenated page numbers ("3217" instead of "32" on wrapped entries — use table layout)
- [ ] Images render (check PDF file size: >400KB suggests images present)
- [ ] Front matter present (copyright, acknowledgments, etc.)
- [ ] Back matter present (author bio, closing note)
- [ ] No nested/unclosed div tags pushing content out of order

---

## EPUB Export Requirements (for KDP Kindle eBook)

When exporting the manuscript to EPUB for Kindle submission, follow the **Amazon Kindle Publishing Guidelines 2025.1**.

### EPUB File Format

- **Format**: EPUB 3 (preferred), EPUB 2 (acceptable)
- **Max file size**: 650 MB including all embedded images
- **Validate with**: `epubcheck` + **Kindle Previewer 3** before upload — fix all errors AND warnings

### EPUB Structure

```
{Book_Title}.epub/
├── mimetype                     ← application/epub+xml, uncompressed, first file
├── META-INF/
│   └── container.xml
└── OEBPS/
    ├── content.opf              ← Manifest, spine, metadata
    ├── nav.xhtml                ← Nav TOC (EPUB 3, required for books >20 pages)
    ├── toc.ncx                  ← NCX (EPUB 2 backward compat)
    ├── cover.xhtml              ← Cover page
    ├── ch01.xhtml               ← One XHTML per chapter
    ├── ...
    └── images/
        ├── cover.jpg
        └── ...
```

### Key Rules for EPUB from Manuscript Source

| Rule | Detail |
|------|--------|
| **One XHTML per chapter** | Split manuscript into individual chapter files |
| **Body text defaults** | No forced font-size/color on `<p>` — let Enhanced Typesetting apply reader preferences |
| **Font color** | Leave unspecified — forcing black breaks night/black-background mode |
| **Font size** | Use relative units (`em`, `%`) not absolute `pt`/`px` for body |
| **HTML TOC** | Linked/clickable, placed toward front, no page numbers |
| **Nav TOC** | 2 levels max, follows book order, required for books >20 pages |
| **Cover embedded** | Internal cover referenced in OPF manifest with `properties="cover-image"` |
| **Guide items** | Define `cover` and `toc` in OPF `<guide>` |
| **Metadata** | Must include: title, creator, language, identifier, dcterms:modified |
| **Alt text** | Required on all informative images |
| **No scripts** | `<script>` tags not supported in KF8 — remove entirely |
| **No counters** | `counter-increment` / `counter-reset` not supported in KF8 |
| **No pseudo-elements** | `::before`, `::after`, `::first-letter`, `::nth-child` not supported |
| **File paths** | Forward slashes only, no special characters in names |
| **Duplicate IDs** | Not allowed — every `id` must be unique across all files |

### EPUB QA Checklist

- [ ] EPUB passes epubcheck with 0 errors
- [ ] Kindle Previewer 3 shows 0 blocking errors
- [ ] Nav TOC lists all chapters at 1–2 levels
- [ ] HTML TOC links are all clickable
- [ ] Cover displays inside EPUB (Kindle Previewer)
- [ ] Body text has no forced font-size/color
- [ ] Images have alt text
- [ ] Metadata matches KDP listing
- [ ] No duplicate IDs across all XHTML
- [ ] Guide items defined for `cover` and `toc`
- [ ] File paths use `/` only, no special chars
- [ ] All custom fonts embedded with proper licensing
- [ ] File size under 650 MB

### No Embedded Cover in EPUB (KDP Rule)

When building an EPUB for Kindle, **do not embed the front or back cover artwork in the reading flow.** The cover image should:

1. **Be included in the EPUB's OEBPS/images/** directory for KDP to find it
2. **Be referenced in the OPF manifest** with `properties="cover-image"` so KDP auto-detects it
3. **Have a cover.xhtml page** placed in the spine with `linear="no"` — this hides it from the reading order while keeping it discoverable
4. **The user uploads the cover image separately** on the KDP website — the EPUB's internal cover is only for device previews

This avoids duplicate cover pages when the EPUB is viewed on Kindle devices (one from the internal file, one from the separately uploaded marketing image).

### Streamlined Package Structure (Alternative to Full Phase 1-7)

For rapid delivery of multiple books in a series, use this streamlined structure instead of the full production pipeline. Each package ZIP contains:

```
{Key}_Publishing_Package.zip/
├── {Key}.epub              ← KDP-compliant EPUB3 (no embedded cover in reading order)
├── {Key}_Cover.png         ← Front cover image (for KDP upload)
├── {Key}_Cover.jpg         ← Cover at 1600×2560 (KDP-recommended dimensions)
├── {Key}_Back_Cover.txt    ← Back cover blurb text
├── {Key}_Author_Bio.txt    ← Short author bio
└── {Key}_README.md         ← Upload instructions
```

**Use this when:** The user asks for "publishing packages" for a batch of books, the cover art is already generated, the manuscript HTML is ready, and the priority is getting all books into KDP-uploadable shape quickly.

**Script:** `scripts/build-epub-package.py` — one-shot EPUB3 + package builder from HTML manuscript + cover PNG. Run once per book:

```bash
python3 scripts/build-epub-package.py \
  /path/to/manuscript.html \
  /path/to/cover.png \
  "Book Title" \
  "Author Name" \
  "Series Name" \
  "1" \
  /path/to/output_dir
```

The script generates the EPUB from raw HTML (no external dependencies beyond Python stdlib), creates the text files, and zips the package — all in one pass.

### Critical Cover Rule: Author and Subtitle Verification

Before applying typography to any cover artwork, verify these two things — they are the most common source of user corrections:

1. **Author name must match the BOOK's author, NOT the inspiration/reference.** If the artwork was inspired by a best-selling book, double-check that you're using the current book's author name (e.g., "Bob J Mills"), not the name from the reference.

2. **No subtitle unless explicitly requested.** Never add a secondary text line under the main title. "Inspired by" does not mean copying the tagline or subtitle from another book.

3. **"Completely original" constraint in prompts.** When artwork is inspired by existing styles, add this exact text to the generation prompt: `This must be completely original — do not reference or copy elements from any existing book covers.`

### Build with Pandoc

```bash
pandoc manuscript.md -o "{Book_Title}.epub" \
  --epub-cover-image="Cover.png" \
  --toc \
  --toc-depth=2 \
  --metadata title="{Book_Title}" \
  --metadata author="{AUTHOR_NAME}" \
  --metadata language="en" \
  --css=epub-style.css
```

Add an `epub-style.css` that follows KDP CSS constraints (no `::before`/`::after`, no `counter-*`, no `img` selector — use classes instead). See the `book-deliverable-kdp` skill's template `templates/kdp-epub-style.css` for a ready-to-use KDP-safe stylesheet.

---

## Appendix: Quick Script for Character Counting

```python
#!/usr/bin/env python3
import sys
with open(sys.argv[1]) as f:
    text = f.read()
print(f"Characters: {len(text)}")
if len(text) > int(sys.argv[2] if len(sys.argv) > 2 else 3950):
    print(f"⚠️ OVER LIMIT by {len(text) - int(sys.argv[2] if len(sys.argv) > 2 else 3950)} chars")
else:
    print(f"✅ Within limit ({int(sys.argv[2] if len(sys.argv) > 2 else 3950)} max)")
```

Usage: `python3 count_chars.py myfile.txt 3950`

---

## Support Files

This skill ships with the following support files. Load them via `skill_view(name='manuscript-publishing-package', file_path='<path>')`:

| Path | Purpose |
|------|---------|
| `scripts/toc-page-numbers.py` | Injects table-based TOC page numbers into any HTML manuscript — adds heading IDs, converts TOC to table rows with `target-counter` CSS. Run before WeasyPrint. |
| `scripts/build-epub-kdp.py` | Builds a complete KDP-compliant EPUB3 + publishing package (.zip) from an HTML manuscript + cover PNG. Handles all 4 known HTML heading formats. No external dependencies beyond PIL. |
| `scripts/check-epub-kdp.py` | Comprehensive EPUB QA checker — validates structure, metadata, nav TOC, KDP compliance. Run against any EPUB before delivery. |
| `references/weasyprint-pitfalls.md` | Detailed reference on WeasyPrint rendering issues: base64 image failures, wrapped-text TOC artifacts, heading ID truncation, image optimization, page-break nesting. Add to as new pitfalls emerge. |
| `references/html-heading-formats.md` | Catalog of 4 HTML heading patterns found across manuscripts + universal detection regex + pitfall guide. Essential for EPUB builders. |
| `references/book-rebranding.md` | Title/subtitle change workflow after manuscript is complete — updating manuscript, build script, cover, and package. Reuse raw artwork if possible; only redo typography. |
| `references/business-book-writing.md` | End-to-end pipeline for non-fiction business books: ideation → market research → voice guide → parallel batch writing → humanize QA → compile → publish. Always load before delegating chapter writing to subagents. |



---

## OpenClaw Migration: books-product-line

# Books Product Line - Operational Support Skill

Use this skill to run the MIFECO Books workflow from board handoff through manuscript completion, publishing, organic promotion, and income tracking.

## The Three-Book Stack

| Title | Type | Launch Order | Audience | Mars Niche? |
|---|---|---|---|---|
| **The Unwritten Future** | Personal memoir — Bob's life story | 1st | Business leaders, memoir readers, engineering professionals | **NO** |
| **First Generation** | Mars-based narrative fiction | 2nd | Mars Society, Mars Technology Institute, space community | **YES** |
| **Second Generation** | Mars-based narrative fiction | 3rd | Mars Society, Mars Technology Institute, space community | **YES** |

**Critical distinction:** The Unwritten Future is a standalone memoir — it is NOT about Mars. It establishes Bob's authority and credibility as an author and leader. Marketing should target leadership/memoir readers, not Mars communities.

**First Generation** and **Second Generation** are the Mars fiction titles. Both serve the Mars Society and Mars Technology Institute communities. Each reinforces the authority of the other as a series.

All three books are authority assets, not revenue products. The goal is thought leadership positioning, not direct book sales profit.

## Core operating rules
- Treat the Board as the originator of every project. Do not qualify leads or sell services. Start from the assumption that the Board has already approved the project and supplied the source materials.
- Use the Board-provided materials as the primary source of truth. Identify missing information, contradictions, weak evidence, or voice gaps early.
- Produce a bestseller-quality commercial book package, not only a draft manuscript. The minimum deliverable set is manuscript, preface, table of contents, front matter, back matter suggestions, metadata, and cover brief or cover asset package.
- Default to no paid promotion. Promotion must rely on virtual posting and repurposed content across LinkedIn, Facebook, and X unless the Board explicitly authorizes spend.
- Protect quality. If source material is thin, repetitive, legally risky, defamatory, plagiarized, or insufficient for a credible manuscript, escalate before drafting final copy.
- Keep financial management simple and auditable. Track list prices, launch pricing, retailer status, royalties, and payouts in one ledger.

## Standard inputs
Expect some or all of the following:
- Board memo or kickoff brief
- Interview transcripts
- Prior articles, speeches, decks, white papers, or notes
- Source folders in Drive
- Brand or author voice guidance
- Target audience, positioning, and publishing goals
- Required publishing accounts or access credentials

If critical inputs are missing, create a gap list and escalate to the Board with the exact missing items.

## Required outputs
Produce the following unless the Board narrows scope:
- Bestseller quality manuscript draft
- Preface
- Table of contents
- Front matter and recommended back matter
- Book subtitle options and retailer metadata
- Cover concept brief and final cover production checklist
- Ebook and print-ready formatted files
- Retail upload checklist
- Organic launch and promotion calendar for LinkedIn, Facebook, and X
- Pricing ladder with escalation logic
- Royalty and income tracking report

## Workflow

### 1. Intake from the Board
- Confirm the project objective, target reader, genre, tone, target length, and deadline.
- Inventory all supplied source materials.
- Create a project control sheet with status, owners, deliverables, risks, and access needs.
- Identify whether the job is ghostwriting, developmental edit, manuscript rescue, or full publishing support.

Escalate to the Board immediately if:
- the source materials are missing or unusable
- there is legal or reputational risk
- authorship rights are unclear
- the target publication timeline is not feasible

### 2. Manuscript architecture
- Extract the central thesis, reader promise, and transformation.
- Build a commercial outline designed for clarity, momentum, and authority.
- Draft the table of contents early.
- Define chapter purpose, evidence, stories, and calls to reflection or action.
- Decide what belongs in preface, introduction, chapters, appendices, acknowledgments, and back matter.

Use concise, market-aware chapter titles. Remove overlaps. Ensure each chapter earns its place.

### 3. Ghostwriting and chapter production
- Convert board materials into clean narrative prose with a consistent voice.
- Fill structural gaps by synthesizing existing materials, not inventing unsupported facts.
- Write at a professional trade-book standard: strong opening, clean transitions, useful examples, and concrete takeaways.
- Where material quality is weak, improve structure and readability without distorting meaning.
- Keep a fact-check list and unresolved question log.

Do not fabricate case studies, quotes, data, endorsements, or achievements. Flag unsupported claims for review.

### 4. Editing and quality pass
Run editing in this order:
1. developmental edit for structure and argument
2. line edit for tone, rhythm, clarity, and repetition
3. copy edit for grammar, punctuation, consistency, and usage
4. proof pass for final defects

During editing:
- tighten slow sections
- remove clichés and filler
- standardize terminology and capitalization
- verify chapter sequencing and TOC alignment
- confirm preface and front matter fit the final structure

### 5. Packaging the book product
Create a complete production package:
- preface
- title page and copyright page draft
- table of contents
- dedication, acknowledgments, introduction, appendices, resources, about the author, and call-to-action as applicable
- retailer description
- author bio
- keyword and category suggestions
- cover concept brief

For cover work:
- create a clear brief with title hierarchy, subtitle treatment, tone, trim size, spine needs, and back cover copy
- if a design tool is available, prepare production-ready cover assets or handoff notes
- confirm final files meet retailer specs for ebook and print

### 6. Publishing operations
Primary channels:
- Amazon KDP / Kindle Direct Publishing
- IngramSpark
- other online channels only if already authorized by the Board

Publishing steps:
- prepare ebook and print interiors
- prepare final metadata
- upload assets
- set territories, categories, and keywords
- configure contributor fields and descriptions
- submit for review
- log all platform statuses and issues

Escalate if accounts are blocked, tax or banking details fail, ISBN ownership is unclear, or a platform rejects the book.

### 7. Pricing ladder
Use escalating pricing tied to launch maturity and organic reach. Since promotion is virtual-only, optimize for discoverability first and margin later.

Default launch ladder:
- ebook launch window: $0.99 to $2.99
- ebook growth window: $3.99 to $5.99
- ebook mature window: $6.99 to $9.99
- paperback launch window: $12.99 to $16.99
- paperback mature window: $16.99 to $24.99
- hardcover, if used: set premium relative to paperback and market norms

Pricing logic:
- start low enough to reduce purchase friction at launch
- raise prices only after reviews, audience traction, or sustained content output improves conversion confidence
- document each price change, reason, and date
- do not discount below platform or royalty constraints without Board approval

### 8. Virtual promotion only
No paid ads unless the Board changes policy.

Promotion channels:
- LinkedIn
- Facebook
- X

Build a promotion set that includes:
- launch announcement posts
- excerpt posts
- quote cards or text snippets
- credibility or insight threads
- reader problem / solution posts
- milestone posts tied to rankings, reviews, or media mentions
- evergreen repost schedule

Promotion rules:
- repurpose the manuscript into short-form social content
- adapt the same message to platform norms instead of reposting identical copy everywhere
- track posting cadence, engagement, and links used
- recommend organic collaborations, podcast outreach, newsletter mentions, and community posting only if no spend is required

### 9. Income and royalty management
Maintain a simple monthly operating report with:
- title
- format
- retailer
- list price
- active promotions
- units sold
- gross revenue
- estimated royalty
- payout date
- notes on anomalies or returns

Also maintain:
- a change log for price updates
- platform payment status
- account issues and resolutions
- Board-ready summary of title performance and next actions

### 10. Escalation rules
Escalate to the CEO for:
- contract or rights disputes
- platform access failures
- major quality concerns close to launch
- pricing exceptions outside standard ladder
- material scope growth or major deliverable changes

Escalate to the Board for:
- strategic repositioning of the book
- publication delays that affect public commitments
- legal or reputational concerns
- missing source material that blocks completion
- requests to add paid marketing or external spend

## Agent assignments
| Task | Primary Agent | Support |
|---|---|---|
| board intake and coordination | writer | ceo |
| manuscript architecture | writer | main |
| ghostwriting | writer | main |
| editing and QA | writer | editor |
| cover brief and asset coordination | designer | writer |
| metadata and publishing setup | writer | designer |
| virtual promotion content | writer | linkedin-writer |
| price ladder management | writer | ceo |
| royalties and income reporting | writer | finance |

## Key metrics
Track at minimum:
- manuscript completion on schedule
- revision cycle count
- publication readiness by deadline
- launch post cadence by platform
- review count and average rating
- unit sales by format and retailer
- royalty and payout totals
- revenue per title over time

## Operating notes
- Prefer concrete, high-conviction copy over generic inspirational business writing.
- Maintain a board-facing status summary at each major phase: intake, outline, draft, edit, publish, launch, report.
- When asked for deliverables, provide the book package and the management layer around it: price plan, promotion plan, and income report.
- Keep all recommendations practical for a no-spend launch environment.
