---
name: publishing-workflow
version: 2.7.0
description: Comprehensive approach for transforming raw manuscripts into professionally formatted books with enhanced transitions, proper publishing details, and AI integration.
tags: [publishing, formatting, PDF, HTML, WeasyPrint, OpenRouter, image-creation]
depends: [manuscript-conversion-pipeline, manuscript-restructuring]
---

## Memory context (Hindsight)

Long-term memory context is now provided automatically by Hindsight (bank
`mifeco-default`) on every turn — the retired MemPalace manual query step no
longer applies. Do NOT attempt to import `~/.hermes/mempalace` (it was removed
2026-08-19).This retrieves previous decisions, domain-specific context, and lessons learned from the vector memory store.

# Book Publishing Pipeline

## MemPalace Query

Before using this skill, query MemPalace for:
- Previous book formatting issues for this book/series
- Known WeasyPrint or EPUB rendering fixes from past sessions
- Chapter title extraction patterns that caused issues before

---

## Quick Start — Use hermes-publish (Recommended)

For all production builds, use the unified pipeline runner. Full details in `references/hermes-publish-pipeline.md`.

```bash
# Build a book: compile → cover → pdf → epub → kdp
cd /mnt/usb_4tb/books
python3 hermes_publish.py --book moon-rock

# Build everything
python3 hermes_publish.py --all

# File-watcher CI/CD (auto-rebuild on changes)
python3 hermes_publish.py --watch
```

The unified pipeline handles all 20 books across 6 series, supports incremental builds (file-hash change detection), and includes MemPalace auto-offload and Codex OAuth image generation.

## Overview
A high-production pipeline for book series and manuscripts, integrating cinematic AI-generated cover art, systematic front/back matter assembly, and professional PDF generation using WeasyPrint or ReportLab.

## When to Use
- Building professional-quality books or series for digital delivery.
- When Pandoc or complex LaTeX environments are unavailable and a Python-native solution is needed.
- Requiring consistent visual branding across a series (covers, typography).
- **Making structural revisions to an existing non-fiction/guide/playbook manuscript** — adding new chapters, updating subtitles, renaming/reorganizing content, and rebuilding all output formats.
- **Converting data-entry/assessment sections** (markdown tables with blank cells, fill-in-the-blank lines, checklists with `[ ]`) into printable forms with bordered tables, checkable boxes, and fillable fields — then rebuilding HTML/PDF/EPUB.

## Workflow Steps

### 1. Visual Branding (Covers)

> **Full KDP specs in `book-deliverable-kdp/references/kdp-specs.md`** — this section summarizes the key values. Refer to the authoritative file for complete details.
- **Tooling:** Use `requests` with endpoints like `pollinations.ai` for reliable, no-key fallback image generation.
- **Prompts:** Use cinematic descriptors ("hyper-realistic", "high contrast", "light band for title space") to ensure professional quality.
- **KDP Cover Requirements (authoritative — verified 2025-05-27):**

| Cover Type | Format | Dimensions | DPI | Color | Max Size |
|---|---|---|---|---|---|
| **Kindle eBook (marketing)** | JPEG (.jpg) or TIFF | **2560×1600 px** ideal; min 1000×625 px | 72 (pixel count matters) | **RGB only** | 50 MB |
| **Kindle eBook (internal/EPUB)** | JPEG in OPF | Large, ≥50% of first page | — | RGB | — |
| **Paperback wrap** | **PDF** single page | Calc: 0.125+Tw+spine+Tw+0.125 wide × 0.125+Th+0.125 tall | **300 min** | CMYK preferred, RGB accepted | 650 MB |
| **Hardcover case laminate** | **PDF** single page | 7-section: wrap+bleed+back+hinge+spine+hinge+front+bleed+wrap | **300 min** | CMYK preferred, RGB accepted | 650 MB |

- **Spine (paperback):** White B&W: `pages×0.002252"` | Cream B&W: `pages×0.0025"` | Color: `pages×0.002347"`
- **Spine (hardcover):** `(pages×0.0025") + 0.189"` board | Total width adds 1.812" for wrap+hinge
- **Paperback example (200pg, 6×9", white B&W):** 12.7004" × 9.25" = **3810×2775 px at 300 DPI**
- **MIFECO design standard:** Large white bold title with 2px black drop-shadow, highly relevant background imagery, author name smaller at bottom, 3-4px gray border if light background
- **Manuscript files should NOT have embedded front/back cover** — KDP's Cover Creator adds those. Only the separate cover file is uploaded.
- **Chapter illustrations by genre:** Sci-fi books get one black-and-white pencil sketch per chapter (generated via OpenRouter image generation, pencil sketch style). Business books get one infographic per chapter (generated via matplotlib). These are embedded in the manuscript as images.

### 1B. KDP Interior Specs (Print & eBook — all output must comply)

> **Single authoritative source**: `book-deliverable-kdp/references/kdp-specs.md`. This section summarizes key values; refer to the source for complete details including margin tables, page counts, and spine formulas.

#### Print (Paperback/Hardcover)
| Requirement | Spec |
|---|---|
| Trim size | 6" × 9" standard |
| Bleed | 0.125" all sides (PDF only if bleed needed) |
| Min pages | **24** |
| Max pages | **828** (B&W/white), 600 (color), 550 (hardcover) |
| Page count | Must be **even** |
| Gutter margins | 24–150pg: 0.375" / 151–300: 0.5" / 301–500: 0.625" / 501–700: 0.75" / 701–828: 0.875" |
| Outside margins | ≥0.25" (no bleed) or ≥0.375" (bleed) |
| Image DPI | **300 min** (600 max) |
| Fonts | All **embedded** in PDF |
| File format | **PDF** for print |

#### eBook (Kindle)
| Requirement | Spec |
|---|---|
| Format | **EPUB 3** preferred (no more MOBI after Mar 2025) |
| Max size | 650 MB |
| TOC | Required (nav.xhtml for EPUB3) |
| Body text | No forced font/size/color on `<p>` |
| Font color | Leave unspecified (dark mode compatibility) |
| Validation | epubcheck (0 errors) + Kindle Previewer (0 blocking errors) |
| Images | 150–300 DPI, max-width: 100% |
| Duplicate IDs | Must be unique across ALL XHTML files |
| File paths | Forward slashes `/` only, no special chars in filenames |

#### Front Matter Order
1. Title page → 2. Copyright page → 3. Table of Contents → 4. (Dedication/Preface) → 5. Chapter 1

### 2. Front & Back Matter
- **Title Page:** Enshrine title, subtitle, author, and specific taglines.
- **Copyright:** Include Standard placeholders: Year, Publisher, Rights Reserved note.
- **Author Note:** Include a specific "Note on composition" or "AI Disclaimer" if assisted by agents.
- **Back Cover:** Include praise placeholders, author bio, and standard identifiers (ISBN/Logo placeholders).

### 2C. Last Page — MANDATORY for Every Book (Added 2026-05-31)

The last page of EVERY manuscript MUST include these elements, in order:
(A) Expanded thank-you blurb (4-5 sentences, in Bob's direct/sincere voice, unique per book referencing that specific story)
(B) **Series Sales Pitch** (MANDATORY for every book in a series) — Series hook (3-5 sentences), next book teaser (2-3 sentences), series reading order, complete bibliography, call to action + QR codes. MUST be unique per book.
(C) Expanded "more from Bob" cross-genre statement (2-3 sentences)
(D) Two QR codes (MIFESCO qr_mifeco.png + Amazon qr_amazon.png, 300x300px, ERROR_CORRECT_H)
(E) Complete "Also by Bob J Mills" book list (all books to-date, organized by series, updated per publication)
(F) Fan Club blurb (www.mifeco.com)
(G) AI Disclosure

See `references/last-page-back-matter.md` for full templates.

### 2E. Reader Magnet PDF Assembly (Added 2026-06-05)

Reader magnets are free novellas/prequels used as lead magnets to drive newsletter signups. They follow a different assembly pattern from KDP print-ready books.

#### Content Assembly Order (from Contents instructions)
1. **Cover Image** — Full-page, no text overlay needed (existing scene/cover art)
2. **Note from Author** — 1-page letter thanking the reader, explaining the series, inviting further reading
3. **Table of Contents** — Linked chapter/part list with page numbers
4. **Full Manuscript** — Complete novella content with chapter headings, scene breaks
5. **Series Sales Pitch** — Series hook, next book teaser, reading order
6. **Complete Book List** — ALL Bob J Mills books organized by series (updated per publication)
7. **Available from Amazon/Kindle** — CTA with links to Amazon author page and mifeco.com/books

#### PDF Spec (for Web Distribution)
- Generated via **WeasyPrint** from a single HTML document (self-contained, base64-embedded cover)
- Trim size: **6×9 inches** (standard for compatibility)
- Font: DejaVu Serif/Georgia 12pt body, 18-20pt chapter headings
- Margins: 0.75in top/bottom, 0.8in left/right
- Page numbers centered at bottom (starting after front matter)
- Images: object-fit:contain (no cropping) with dark background
- **No bleed** needed (web distribution, not print)
- **No ISBN** needed
- **No gutter margin** needed (screen reading)

#### Cover Page
- Full-bleed cover image fills the entire first page
- `@page cover { margin: 0; @bottom-center { content: none; } }`
- Embed cover as base64 data URI for self-contained HTML

#### Note from Author Template
```html
<div class="note-page">
  <h2>Note from the Author</h2>
  <p>Thank you for downloading this reader magnet novella. I write stories about people
  who face impossible odds and choose to move forward anyway...</p>
  <p>This novella is a gateway into a larger world...</p>
  <p class="signature">— Bob J Mills</p>
</div>
```

#### Bibliography Section
Must list ALL published books to-date, organized by series with 1-line descriptions. Check `/mnt/usb_4tb/books/` for current inventory. Current series (2026-06):

| Series | Books |
|--------|-------|
| Age of Lightships | Sunward Exodus, Mercury Accord, Ghosts Beyond Neptune, Last Photon Fleet |
| Lunar Foundation | Moon Rock, Mooncoming, Waters End, Waters Horizon |
| No Blue Sky | Built from Dust, Oxygen Gamble, Rivers Under Mars, Red Charter, First Martian Nation (5) |
| Cindy Lou Legal Capers | Retainer to Trouble, Clause for Alarm, Affidavits and Alibis |
| Business | AI That Works, Crisis Ready Company, Owner's Manual for AI Agents |
| Memoir | Tomorrow Remembered |

#### Filename Convention
`[Book_Title]_Magnet.pdf` — placed in the book's series directory under magnets/.

#### Key Differences from KDP Print PDF
| Feature | Reader Magnet | KDP Print |
|---------|--------------|-----------|
| Cover | Full-page image | Separate wrap cover |
| Bleed | None | 0.125in |
| Page count | Any (no even restriction) | Must be even |
| Note from Author | ✅ Required | ❌ |
| Series pitch | ✅ Required | ❌ |
| Complete book list | ✅ Required | ❌ |
| Amazon/Kindle CTA | ✅ Required | ❌ |
| ISBN | ❌ | ✅ Required for print |
| Gutter margins | ❌ | ✅ Required |

Full HTML template, markdown template, and QR code generation code: see `references/last-page-back-matter.md`.
Multi-block infographic composition (layout, typography, platform formats, pitfalls): see `references/infographic-pitfalls.md`.

### 2F. Novella Requirements — MANDATORY for Every Individual Book in a Series

Every individual book/novella in a series MUST have:

#### A. Cover Image
- Professional cover in series style (consistent typography, color scheme across series)
- Same design language as the parent series but unique per book
- Save as `cover.png` and `cover_KDP.jpg` (2560x1600px, RGB, JPEG for KDP upload)
- Use Gemini 2.5 Flash Image or Flux.2 Max via OpenRouter for generation
- Cover must include: title, subtitle, author name, series name, series number
- MUST pass thumbnail test (legible at 80px wide)

#### B. Highly Formatted PDF
- Professional interior PDF for KDP print submission
- Generated via WeasyPrint from HTML or ReportLab
- Must include: cover page, title page, copyright, TOC, chapters, back matter
- Fonts: Times New Roman 12pt body, 18pt chapter headings
- Page size: 6"x9" trim, proper gutter margins
- All fonts embedded in PDF
- Even page count (add blank page if needed)
- Page numbers starting after front matter
- Save to output directory as `[BookName]_Print.pdf`

#### C. Sales Pitch (End of Book)
After the story ends and "About the Author" section, add a **series sales pitch**:

1. **Series hook** (3-5 sentences): Remind the reader what this series is about, the overarching story arc, and what makes it special. Tailor to the specific series.
2. **Next book teaser** (2-3 sentences): Tease the next book in the series by name, hint at the stakes, create urgency to continue.
3. **Series reading order** (numbered list): All books in the series with titles and brief 1-line descriptions.
4. **Complete bibliography**: ALL Bob J Mills books across all series (organized by series/genre)
5. **Call to action**: "Available on Amazon Kindle and Paperback" + QR codes

**Series-specific sales pitch examples:**
- *Lightships*: Reference the fleet, Proxima Centauri, the 120-year journey, what comes next
- *Lunar Foundation*: Reference the Moon colony, survival, the expanding settlement
- *No Blue Sky*: Reference Mars, independence, the Red Planet's brutal beauty
- *Business books*: Reference practical ROI, real-world application, what readers will gain

The pitch MUST be unique per book — don't copy-paste. Reference the specific book the reader just finished and connect it to the next book and the broader body of work.

KDP has specific TOC requirements for both eBook and print:

#### eBook TOC Requirements
- **Required** for all books >20 pages (KDP will reject without it)
- **Two types needed**: (1) HTML TOC (visible, clickable list at start of book) and (2) nav.xhtml (logical navigation for Kindle)
- **HTML TOC rules**:
  - Linked/clickable entries that resolve to chapter anchors
  - **No page numbers** (eBook pages are reflowable — page numbers are meaningless)
  - Placed in front matter before Chapter 1
- **nav.xhtml rules** (EPUB3):
  - Uses `<nav epub:type="toc">` with `<ol>` nesting
  - Max **2 levels of nesting** (parts → chapters)
  - Listed in reading order
  - Referenced in OPF spine
- **Heading consistency**: All chapter titles must use the SAME heading level (e.g. `## Chapter N` or `h2`). Inconsistent heading levels break auto-TOC generation.

#### Print TOC Requirements
- **Manual creation required** (KDP does NOT auto-generate print TOC)
- Must include accurate **page numbers**
- Page numbers must be updated after final pagination (use `pdftotext` to extract actual pages)
- Render TOC as HTML list with hardcoded page numbers, then convert to PDF

#### Directory Structure Note for chapters_md Type

The `chapters_md` manuscript type looks for chapter files in `book_dir/chapters/` (preferred) or `book_dir/manuscript_src/` (fallback). When setting up a book for condensation:

1. Place condensed chapter files in `book_dir/chapters/` as `ch01.md` through `ch30.md`
2. Update BOOK_REGISTRY to point `dir` to the directory containing the `chapters/` subdirectory
3. Set `manuscript_type: "chapters_md"` in BOOK_REGISTRY
4. Delete old output files (PDF, EPUB, KDP ZIP) before regenerating to avoid confusion between old and new versions

#### Cleanup Before Rebuild

Always remove stale output files before generating new ones:
```bash
# In the book's output directory
rm -f *.pdf *.epub *.zip
# Or specifically
rm -f Retainer_to_Trouble_Print.pdf Retainer_to_Trouble.epub Sunward_Exodus_KDP_PACKAGE.zip
```

Also remove old mixed-case manuscript variants (e.g., `Clause_for_Alarm_MANUSCRIPT.md`) when the lowercase variant (`clause-for-alarm_MANUSCRIPT.md`) replaces them.

**Pitfall — Dual directory placement:** After writing any file (condensed chapters, EPUBs, PDFs, KDP packages), copy to BOTH directory locations:
1. `cindy-lou-series/[book]/` — primary pipeline path
2. `Cindy_Lou_Legal_Capers/[book]/` — legacy path
The user checks both. Never assume one is sufficient. Use `cp` with explicit destination paths, not wildcards.

This prevents users from accidentally opening the old 474-page PDF when the new EPUB is only 182 pages.
- **Blank pages**: Ensure `@page :blank` CSS is set or blank pages in PDF get page numbers/correct headers
- **TOC entries not linked**: Every TOC entry must be a clickable anchor (`<a href="#ch1">`)

#### TOC Code Pattern (eBook)
```python
# Generate both HTML TOC and nav.xhtml from the same heading list
def generate_toc(chapter_list, max_depth=2):
    """chapter_list = [(level, title, anchor_id), ...]"""
    html_items = []
    nav_items = []
    
    for level, title, anchor in chapter_list:
        html_items.append(f'<p class="toc-{level}"><a href="#{anchor}">{title}</a></p>')
        nav_items.append(f'<li><a href="{anchor}.xhtml">{title}</a></li>')
    
    html_toc = '<div class="toc">\n' + '\n'.join(html_items) + '\n</div>'
    nav_toc = '<nav epub:type="toc">\n<ol>\n' + '\n'.join(nav_items) + '\n</ol>\n</nav>'
    
    return html_toc, nav_toc

# For print: extract actual page numbers after PDF build
def extract_page_numbers(pdf_path, chapter_headings):
    """Use pdftotext to find actual page for each chapter heading"""
    import subprocess
    result = subprocess.run(['pdftotext', pdf_path, '-layout', '-'],
                          capture_output=True, text=True)
    pages = result.stdout.split('\f')  # form-feed = page break
    
    page_map = {}
    for i, page_text in enumerate(pages, 1):
        for heading in chapter_headings:
            if heading in page_text and heading not in page_map:
                page_map[heading] = i
    return page_map
```

### 3A. **Numbered Sub-Section Generation in HTML Build** (For Non-Fiction Books)

Non-fiction/guide books require numbered sub-sections within chapters (e.g., `1.1 Why This Matters`, `1.2.1 Implementation Steps`). The HTML build script must convert markdown `##` and `###` headers inside chapter content into numbered section labels.

#### Strategy
During HTML generation, for each chapter `N`, track counters as you encounter headings:

```python
def chapter_md_to_html(text, ch_num):
    """Convert markdown within a chapter to HTML with numbered sub-sections."""
    sec = [0, 0]  # [major_section, minor_section]
    in_ul = False
    result = []
    
    for line in text.split('\n'):
        stripped = line.strip()
        
        # ## → major section: 1.1, 1.2, 1.3
        if stripped.startswith('## '):
            sec[0] += 1
            sec[1] = 0
            title = stripped[3:]
            result.append(f'<h3>{ch_num}.{sec[0]} {esc_html(title)}</h3>')
        
        # ### → minor section: 1.1.1, 1.2.1
        elif stripped.startswith('### '):
            sec[1] += 1
            title = stripped[4:]
            result.append(f'<h4>{ch_num}.{sec[0]}.{sec[1]} {esc_html(title)}</h4>')
        
        # #### → sub-sub-section (numbered or parenthesized)
        elif stripped.startswith('#### '):
            title = stripped[5:]
            result.append(f'<h5>{esc_html(title)}</h5>')
        
        # Regular paragraph with NO text-indent for non-fiction
        elif stripped:
            result.append(f'<p>{process_inline(stripped)}</p>')
        else:
            result.append('')
    
    return '\n'.join(result)
```

#### Important: Exclude Chapter Title Headers
Only apply numbering to `##` headers INSIDE chapter content — NOT the chapter title itself (`## Chapter N: Title`). The chapter title gets its own `<h2>` outside this function.

#### CSS for Numbered Sections
```css
h3.section-heading { font-size: 14pt; font-weight: bold; margin: 22px 0 10px; }
h4.sub-section-heading { font-size: 12pt; font-weight: bold; font-style: italic; margin: 16px 0 8px; }
h5.sub-sub-section-heading { font-size: 11pt; font-weight: bold; margin: 12px 0 6px; }
p { text-indent: 0; }  /* no indent — business books use block paragraphs */
```

#### Pitfall: &nbsp; Not Valid in XHTML/EPUB

`&nbsp;` is an HTML entity that is NOT valid in XHTML (which EPUB uses). If your markdown chapter files contain `&nbsp;&nbsp;&nbsp;&nbsp;` for paragraph indentation, they will break EPUB rendering with:

```
Entity 'nbsp' not defined
```

**Fix:** In your `md_to_html_simple()` function, add `&nbsp;` → `&#160;` replacement BEFORE processing:

```python
def md_to_html_simple(text):
    lines = text.split('\n')
    out = []
    in_p = False
    for line in lines:
        # Replace &nbsp; with &#160; for valid XHTML
        line = line.replace('&nbsp;', '&#160;')
        s = line.strip()
        # ... rest of processing
```

**Also applies to**: Any content passed to EPUB XHTML generation, including compiled manuscripts and marketing text. When post-processing EPUB files, use `content.replace('&nbsp;', '&#160;')` on all XHTML files inside the EPUB ZIP.

**Verification**: After regenerating EPUB, extract a chapter XHTML from the ZIP and search for `&nbsp;` — there should be zero occurrences.

**Website deployment**: This same issue affects HTML files served on websites. If `&nbsp;` entities appear in markdown that gets converted to HTML for web serving, they will cause rendering errors in strict XHTML/XML parsers. Always replace before serving.
The regex that splits `# Chapter N: Title` from content may leave `## Chapter N: Title` inside chapter content as a secondary heading. Filter it out during section numbering: `if line.startswith('## Chapter'): continue`.

### CSS Distinction: Fiction vs Non-Fiction Paragraph Formatting

**Fiction / Memoir / Novels:**
```css
p { text-indent: 1.5em; margin: 0; }  /* classic book look */
```

**Non-Fiction / Guide / Business Books:**
```css
p { text-indent: 0; margin: 6px 0; }  /* block paragraphs, no indent */
```

### EPUB Rendering: `&nbsp;` Entity Fix (MANDATORY)

`&nbsp;` is an HTML entity that is NOT valid in XHTML (which EPUB requires). If chapter files contain `&nbsp;&nbsp;&nbsp;&nbsp;` for paragraph indentation, they will break EPUB rendering with:

```
error on line 6 at column 10: Entity 'nbsp' not defined
```

**Fix:** In `md_to_html_simple()`, add `line = line.replace('&nbsp;', '&#160;')` as the FIRST line of the paragraph processing loop, before any other processing. This replaces the invalid HTML entity with the valid XHTML numeric entity.

### Chapter Title Extraction (chapters_md type)

Chapter files may have titles as plain text on the first line (e.g., "The Letterhead Lies") OR as markdown headers (e.g., "# Chapter 1: The Letterhead Lies"). The `collect_chapters()` function MUST handle both:

```python
first = content.split('\n')[0] if content else ""
if first.startswith('#'):
    title = first.lstrip('#').strip()
elif first.strip():
    title = first.strip()  # Plain text title
else:
    title = f"Chapter {num}"
# Strip "Chapter N:" prefix to avoid duplication
title = re.sub(r'^Chapter\s+\d+:\s*', '', title)
```

The prefix-stripping regex prevents "Chapter 4: Chapter 4: The Sister's Plea" duplication in EPUB `<h2>` headers.

### Python Bytecode Cache After Pipeline Changes

After modifying ANY `hermes_publish/` Python module, ALWAYS clear the bytecode cache:
```bash
find /mnt/usb_4tb/books/hermes_publish/ -name "__pycache__" -type d -exec rm -rf {} +
```
Failure to do this causes the pipeline to run stale code, producing EPUBs with old bugs that appear to be "not fixed" even after source changes.

### Stale Output File Cleanup

Before regenerating EPUBs/PDFs after condensation or edits, delete old output files to prevent user confusion:
```bash
rm -f /path/to/book/output/*.pdf *.epub
rm -f /path/to/book/*_KDP_PACKAGE.zip
```
Remove old mixed-case manuscript variants (e.g., `Clause_for_Alarm_MANUSCRIPT.md`) when the lowercase variant (`clause-for-alarm_MANUSCRIPT.md`) replaces them.

The difference is both aesthetic and functional:
- Fiction uses indent to mark paragraph breaks naturally, saving vertical space.
- Non-fiction uses block paragraphs (space between paragraphs) because many sections contain lists, tables, callout boxes, and forms where indent looks wrong.

When building from the same manuscript, toggle the CSS based on genre using a variable:
```python
css_paragraph = 'p { text-indent: 1.5em; margin: 0; }' if genre == 'fiction' else 'p { text-indent: 0; margin: 6px 0; }'
```

### 3B. **ReportLab PDF Generation** (Alternative to WeasyPrint)

Use ReportLab when WeasyPrint is unavailable or when you need pixel-perfect layout control (tables with grid borders, data entry fields, page numbers, TOC).

#### Key Styles Pattern
```python
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Image, KeepTogether
from reportlab.lib.colors import black, white, HexColor
from reportlab.pdfgen import canvas

MARGIN = 1 * inch
PAGE_W, PAGE_H = letter
CONTENT_W = PAGE_W - 2 * MARGIN  # 6.5in

sBody = ParagraphStyle('Body', parent=styles['Normal'],
    fontSize=12, leading=18, alignment=TA_JUSTIFY, spaceAfter=6, firstLineIndent=24)
```

#### Table Formatting with Grid Borders (Spreadsheet Style)
```python
def make_table(rows):
    if not rows or len(rows) < 2: return None
    max_cols = max(len(r) for r in rows)
    padded = [r + [''] * (max_cols - len(r)) for r in rows]
    
    cell_data = []
    for i, row in enumerate(padded):
        cell_row = []
        for cell in row:
            style = sTableHeader if i == 0 else sTableCell
            clean = cell.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
            clean = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', clean)
            clean = re.sub(r'\*(.+?)\*', r'<i>\1</i>', clean)
            cell_row.append(Paragraph(clean, style))
        cell_data.append(cell_row)
    
    if max_cols >= 2:
        col_widths = [CONTENT_W/max_cols * 1.3] + [CONTENT_W/max_cols * 0.85] * (max_cols - 1)
    else:
        col_widths = [CONTENT_W]
    
    t = Table(cell_data, colWidths=col_widths, repeatRows=1)
    t.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.8, black),
        ('BOX', (0,0), (-1,-1), 1.2, black),
        ('BACKGROUND', (0,0), (-1,0), HexColor('#eeeeee')),
        ('LINEBELOW', (0,0), (-1,0), 1.5, black),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [white, HexColor('#f8f8f8')]),
    ]))
    return KeepTogether([Spacer(1, 0.1*inch), t, Spacer(1, 0.1*inch)])
```

### 3C. **B&W Infographic Chart Generation**

Generate B&W charts for books using matplotlib (Agg backend, no display needed):

```python
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

plt.rcParams.update({
    'font.family': 'sans-serif', 'font.size': 8,
    'axes.edgecolor': 'black', 'axes.linewidth': 0.8,
    'grid.color': '#cccccc', 'grid.linestyle': '--', 'grid.alpha': 0.5,
    'figure.dpi': 200,
})

fig, ax = plt.subplots(figsize=(4.5, 3.0))  # standard chart size
bars = ax.bar(categories, values, color='white', edgecolor='black', linewidth=1.2)
for bar, v in zip(bars, values):
    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.3, f'{v}', ha='center', fontsize=7)
ax.set_title('Chart Title', fontsize=9, fontweight='bold')

OUT = "/path/to/charts"
os.makedirs(OUT, exist_ok=True)
fig.savefig(f"{OUT}/01-chart-name.png", bbox_inches='tight', dpi=200, facecolor='white')
plt.close(fig)
```

**20 B&W chart types** useful for business books:
1. Bar charts (time distribution, savings, costs, revenue)
2. Before/after comparison (grouped bars)
3. Impact/effort matrices (quadrant scatter)
4. Funnel diagrams (adoption, conversion)
5. Line charts (growth trajectories, trends)
6. Pie/ring charts (data sources, budget allocation)
7. Gantt-like timelines (implementation roadmaps)
8. Lead scoring curves
9. Radar/network diagrams (readiness scores, risk assessment)
10. Decision matrix bar charts

**Integration into build script:** Create a caption dict, save charts as PNG, then insert via:
```python
def insert_chart(name):
    captions = {'01-chart-name': 'Figure 1: Description'}
    img = Image(chart_path, width=CONTENT_W * 0.75, height=CONTENT_W * 0.5)
    story.append(img)
    story.append(Paragraph(caption, sChartCaption))
```

### 3D. **Programmatic Cover Regeneration (PIL)**

When updating a book title/author, regenerate the cover using an existing raw artwork image plus text overlay:

```python
from PIL import Image, ImageDraw, ImageFont

# Find font
for fp in ['/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
           '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf']:
    if os.path.exists(fp): font_path = fp; break

img = Image.open("raw_cover.png").convert("RGB")
# Scale to target: 1024x1536 for 2:3 aspect ratio
target_w, target_h = 1024, 1536
scale_h = target_h / img.height
new_w = int(img.width * scale_h)
img = img.resize((new_w, target_h), Image.LANCZOS)
# Center crop to width
x_offset = (new_w - target_w) // 2
canvas = img.crop((x_offset, 0, x_offset + target_w, target_h))

# Add dark gradient overlays for text readability
overlay = Image.new("RGBA", (target_w, target_h), (0,0,0,0))
draw = ImageDraw.Draw(overlay)
# Top gradient (18% height, 50 alpha)
for y in range(int(target_h * 0.18)):
    alpha = int(50 * (1 - y / (target_h * 0.18)))
    draw.rectangle([0, y, target_w, y+1], fill=(0,0,0,alpha))

# Title (stacked words)
title_font = ImageFont.truetype(font_path, 62)
for i, word in enumerate(["AI", "THAT", "WORKS"]):  # etc.
    bbox = draw.textbbox((0,0), word, font=title_font)
    tx = (target_w - (bbox[2]-bbox[0])) // 2
    ty = 50 + i * int(62 * 1.15)
    draw.text((tx+2, ty+2), word, fill=(0,0,0,200), font=title_font)
    draw.text((tx, ty), word, fill=(255,255,255), font=title_font)

# Subtitle (multi-line, smaller)
sub_font = ImageFont.truetype(font_path, 18)
for i, line in enumerate(["A Practical Guide to", "Save Time, Cut Costs,"]):
    bbox = draw.textbbox((0,0), line, font=sub_font)
    sx = (target_w - (bbox[2]-bbox[0])) // 2
    sy = title_end_y + i * 22
    draw.text((sx+1, sy+1), line, fill=(0,0,0,180), font=sub_font)
    draw.text((sx, sy), line, fill=(200,200,200), font=sub_font)

# Author at bottom
author_font = ImageFont.truetype(font_path, 28)
bbox = draw.textbbox((0,0), "Author Name", font=author_font)
ax = (target_w - (bbox[2]-bbox[0])) // 2
draw.text((ax+2, target_h-100+2), "Author Name", fill=(0,0,0,200), font=author_font)
draw.text((ax, target_h-100), "Author Name", fill=(255,255,255), font=author_font)

final = Image.alpha_composite(canvas.convert("RGBA"), overlay).convert("RGB")
final.save("Cover.png", "PNG", optimize=True)
```
First choice: WeasyPrint for direct HTML-to-PDF conversion with CSS support.
Fallback: ReportLab for total layout control when WeasyPrint is unavailable.
- **Margins:** 2.5cm standard for A4.
- **Typography:** Use `Times-Roman` (12pt Body) and `Times-Bold` (18pt Headings) for the "bestseller" look.
- **Justification:** Set `alignment=4` in `ParagraphStyle` for professional blocks.
- **Dynamic TOC:** 
  - Scan the manuscript for `## Chapter` headers.
  - Build a list of entries for the TOC.
- **Media Delivery:** Always provide an absolute path for the final PDF to ensure `MEDIA:/path` works on Telegram.

### 3E. **Chapter Insertion and Renumbering** (for Non-Fiction Revisions)

When adding a new chapter to an existing non-fiction manuscript (e.g., a risk management chapter between ethics and implementation playbook):

#### Step 1: Find the Insertion Point
The manuscript has `# Chapter N: Title` headers. Locate the chapter boundary:
```python
pattern = r"^# Chapter (\d+): (.+)$"
headers = re.findall(pattern, manuscript, re.MULTILINE)
```

#### Step 2: Insert the New Chapter
Use `re.sub` with `re.MULTILINE`, inserting the new chapter BEFORE the target:
```python
content = re.sub(
    rf"^# Chapter {OLD_NUM}: {re.escape(OLD_TITLE)}\n",
    new_chapter_content + "\n# Chapter " + str(OLD_NUM) + ": " + OLD_TITLE,
    content, count=1, flags=re.MULTILINE
)
```

#### Step 3: Renumber Subsequent Chapters
After insertion, increment all following chapter numbers:
```python
for old_num in range(NEW_NUM, MAX_NUM + 1):
    content = re.sub(
        rf"^# Chapter {old_num}: ",
        f"# Chapter {old_num + 1}: ",
        content, count=1, flags=re.MULTILINE
    )
```
**Iterate from highest to lowest** to avoid re-scanning already-renumbered headers.

#### Step 4: Update Cross-References & TOC
Update "In the next chapter..." or "In the final chapter..." text in preceding chapters. Update any hardcoded TOC in the manuscript front matter (e.g. `12. **Your AI Implementation Playbook**`).

#### Step 5: Verify
```python
headers = re.findall(r"^# Chapter (\d+):", content, re.MULTILINE)
# Verify sequential 1, 2, 3, ... N
assert [int(h) for h in headers] == list(range(1, int(headers[-1]) + 1))
```

### 3F. **Markdown Data-Entry Form Conversion** (For Business Books)

Business/guide books contain assessment tables, checklists, rating scales, and fill-in-the-blank exercises. These need printable forms with visible borders and checkboxes — NOT regular tables.

#### What to Detect
- **Tables with blank cells**: cells containing `___`, empty, or "Your turn:" text
- **Checklists:** `[ ]` or `[x]` markers
- **Fill-in-the-blank lines:** numbered blanks or `___` answer fields
- **Rating scales:** `(Rate 1-5): ___`

#### Conversion Strategy (Markdown → HTML Forms)

Scan the manuscript line by line with a state machine:

```python
def reformat_data_entry_sections(text):
    lines = text.split('\n')
    result = []
    i = 0
    in_table = False
    table_lines = []
    
    while i < len(lines):
        line = lines[i]
        # Detect table start
        if not in_table and line.strip().startswith('|') and '|' in line[1:]:
            if i + 1 < len(lines) and re.match(r'^\|[\s\-:]+\|', lines[i+1]):
                in_table = True; table_lines = [line, lines[i+1]]; i += 2; continue
        if in_table:
            if line.strip().startswith('|') and '|' in line[1:]:
                table_lines.append(line); i += 1; continue
            else:
                result.append(format_table_with_blanks(table_lines))
                table_lines = []; in_table = False; continue
        # Single-line checks
        if re.match(r'^[\-\*]\s+\[[\s\]*\s+', line):
            label = re.sub(r'^[\-\*]\s+\[[\s\]*\s+', '', line)
            result.append(f'<div class="form-checkbox-line"><span class="checkbox-box">☐</span><span class="checkbox-label">{label}</span></div>')
        elif re.match(r'^[\-\*]\s+\[[xX]\\]\s+', line):
            label = re.sub(r'^[\-\*]\s+\[[xX]\\]\s+', '', line)
            result.append(f'<div class="form-checkbox-line"><span class="checkbox-box">☑</span><span class="checkbox-label">{label}</span></div>')
        elif re.match(r'^[\-\*]\\s+(.+?)\\s*\(Rate 1-5\\):\\s*_{0,5}$', line):
            label = re.match(r'^[\-\*]\\s+(.+?)\\s*\(Rate 1-5\\):\\s*_{0,5}$', line).group(1)
            result.append(f'<div class="form-line"><span class="form-bullet">•</span><span class="form-label">{label} (Rate 1-5):</span><span class="form-blank">&nbsp;</span></div>')
        elif re.match(r'^(.+?)\\s+_{5,}\\s*$', line.strip()) and len(line.strip()) > 10:
            label = re.match(r'^(.+?)\\s+_{5,}\\s*$', line.strip()).group(1).strip()
            result.append(f'<div class="form-fill-line"><span class="form-fill-label">{label}</span><span class="form-fill-field">&nbsp;</span></div>')
        elif re.match(r'^.{0,3}_{5,}\\s*$', line.strip()):
            result.append('<div class="form-text-block">&nbsp;</div>')
        else:
            result.append(line)
        i += 1
    return '\n'.join(result)
```

#### HTML Table-to-Form Conversion
For tables with blank cells, output as bordered form tables:
```html
<div class="data-entry-form">
<table class="form-table">
<thead><tr><th>Header</th><th>Header</th></tr></thead>
<tbody>
<tr><td>Data</td><td class="entry-cell"><span class="entry-line">&nbsp;</span></td></tr>
</tbody>
</table>
</div>
```

#### Required CSS
```css
.form-table { width: 100%; border-collapse: collapse; border: 1.5px solid #000; font-size: 10pt; }
.form-table th { background: #e8e8e8; border: 1px solid #000; padding: 6px 8px; text-align: left; font-weight: bold; }
.form-table td { border: 1px solid #000; padding: 5px 8px; }
.form-table .entry-cell { background: #fafafa; height: 24px; }
.form-table .entry-line { display: block; border-bottom: 1px solid #666; width: 100%; min-height: 18px; }
.form-line { margin: 8px 0; padding: 6px 10px; border: 1px solid #999; background: #fafafa; page-break-inside: avoid; }
.form-line .form-blank { display: inline-block; border-bottom: 1px solid #666; min-width: 120px; min-height: 18px; }
.form-text-block { border: 1px solid #999; min-height: 60px; margin: 8px 0; background: #fafafa; }
.form-checkbox-line { margin: 4px 0; padding: 3px 8px; page-break-inside: avoid; }
.form-checkbox-line .checkbox-box { font-size: 14pt; margin-right: 8px; }
.form-fill-line { margin: 8px 0; padding: 6px 10px; border: 1px solid #999; background: #fafafa; page-break-inside: avoid; }
.form-fill-field { display: inline-block; border-bottom: 1px solid #666; min-width: 200px; min-height: 18px; }
.form-instruction { font-style: italic; color: #666; margin: 6px 0; }
```

#### Pitfalls
- **Only convert tables WITH blanks** — leave regular data tables alone. Check for `___`, empty cells, or "Your turn" text.
- **Drop `<ul>` containers** when converting checklists — form checkboxes use their own CSS layout.
- **Page-break avoidance** on form containers so forms don't split across pages in print.
- **EPUB compatibility**: form borders work well in PDF but may render differently in EPUB readers — this is acceptable since forms are primarily for print use.

### 3G. **Disclaimer on Copyright Page**

For non-fiction, business, or advice books, add a disclaimer at the bottom of the copyright page:

```html
<p style="margin-top:30px;font-size:9pt;border-top:1px solid #ccc;padding-top:12px;">
<strong>Disclaimer:</strong> This book is intended for informational and advisory purposes only. 
The author and publisher make no representations or warranties regarding the accuracy, 
completeness, or applicability of its content. The reader assumes full responsibility 
for the use of any information, strategies, or tools described herein. The author shall 
not be held liable for any damages, losses, or legal issues arising from the use or 
misuse of this content. Always consult qualified professionals for business, legal, 
and technical decisions specific to your situation.
</p>
```

Include this in both the HTML/PDF copyright page AND the EPUB `copyright.xhtml`.

### 3H. **Cover Image in EPUB**

EPUB requires three things for a proper cover:

1. **Copy the cover PNG into OEBPS:**
```python
import shutil
COVER_PATH = Path("/path/to/Cover.png")
shutil.copy2(COVER_PATH, epub_dir / "OEBPS" / "cover.png")
manifest.append('<item id="cover-img" href="cover.png" media-type="image/png" properties="cover-image"/>')
```

2. **Create a cover XHTML page:**
```python
cover_xhtml = f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html><html xmlns="http://www.w3.org/1999/xhtml"><head><title>Cover</title></head>
<body style="text-align:center;padding-top:20px;">
<img src="cover.png" alt="Cover" style="max-width:100%;height:auto;"/>
</body></html>'''
with open(epub_dir / "OEBPS" / "cover.xhtml", "w") as f: f.write(cover_xhtml)
manifest.append('<item id="cover-page" href="cover.xhtml" media-type="application/xhtml+xml"/>')
```

3. **Add to spine with `linear="no"`:**
```python
spine.append('<itemref idref="cover-page" linear="no"/>')
```

The `linear="no"` tells e-readers the cover is a dedicated page (shown as the opening image) rather than part of the page-flow. Without this, some readers skip the cover.

### 3I. **Pre-Delivery Verification**

Before sending generated files to the user, run a quick content check on the HTML output:

```python
checks = {
    'Cover image': 'data:image/png;base64,' in html,
    'Disclaimer': 'Disclaimer:' in html,
    'TOC': 'Table of Contents' in html,
    'Back cover': 'back-cover' in html,
    'Form tables': 'form-table' in html,
    'Checkboxes': 'checkbox-box' in html,
}
# For each chapter
for ch in chapters:
    checks[f'Chapter {ch}'] in html

all_pass = all(checks.values())
for name, status in checks.items():
    print(f'  {"✅" if status else "❌"} {name}')
```

This catches regressions from build script changes before the user sees them. Focus on structural markers: cover, disclaimer, TOC, all chapters, forms/checklists if expected.

#### Page Numbering (Custom DocTemplate)
```python
class PageNumberDoc(SimpleDocTemplate):
    def afterPage(self):
        c = self.canv
        c.saveState()
        c.setFont('Times-Roman', 9)
        c.setFillColor(HexColor('#666666'))
        page = c.getPageNumber()
        if page > 3:  # Skip cover, title, copyright
            c.drawCentredString(PAGE_W / 2, 0.5 * inch, f"{page}")
        c.restoreState()

doc = PageNumberDoc(PDF_PATH, pagesize=letter,
    leftMargin=MARGIN, rightMargin=MARGIN,
    topMargin=MARGIN, bottomMargin=MARGIN)
```

#### TOC with Page Number Estimation
Since SimpleDocTemplate builds sequentially, exact page numbers aren't known during assembly. Use content-based estimation:
```python
lines_per_page = 38  # body lines on 8.5x11 letter
current_page = 3  # after cover(1), title(2), copyright(3)
toc_items = []

for ch in chapters:  # each chapter with 'title' and 'lines' count
    start_page = current_page + 1
    toc_items.append({'type': 'chapter', 'title': ch['title'], 'page': start_page})
    ch_pages = max(1, min(ch['lines'] // lines_per_page, 25))
    current_page += ch_pages

# Render TOC as paragraphs with dot leaders
for item in toc_items:
    if item['type'] == 'chapter':
        line = f"<b>{item['title']}</b> {'·'*40} {item['page']}"
        story.append(Paragraph(line, sTOCChapter))
    else:  # subsection
        line = f"&nbsp;&nbsp;&nbsp;&nbsp;{item['title']} {'·'*40} {item['page']}"
        story.append(Paragraph(line, sTOCSub))
```

#### Data Entry Fields (Surveys/Exercises)
For exercises where users fill in data, render as bordered single-cell tables or use underlined spaces:
```python
# Option 1: Bordered table cell
entry_data = [[Paragraph("___", sTableCell)]]
entry_table = Table(entry_data, colWidths=[CONTENT_W])
entry_table.setStyle(TableStyle([
    ('BOX', (0,0), (-1,-1), 0.8, black),
    ('LEFTPADDING', (0,0), (-1,-1), 8),
    ('TOPPADDING', (0,0), (-1,-1), 6),
    ('BOTTOMPADDING', (0,0), (-1,-1), 6),
]))

# Option 2: Underline-only (lighter)
# In markdown, use `___` with consistent spacing. In the build script,
# render as a left-indented paragraph with underline spaces.
```

### 3J. **Appending a New Final Section to a Fiction/Memoir Manuscript** (For Prose Books)

When a user provides a new prose section (in markdown) to append to the end of an existing memoir or fiction manuscript, the existing structure and content must be fully preserved. The workflow differs from non-fiction chapter insertion because memoirs use organic transitions rather than numbered headers.

#### When to Use
- User says "add this new section to the end of the book"
- A markdown file containing a final section (e.g., "The Future After Bob") needs to be appended after the existing ending
- The manuscript uses narrative headers like `# Part One:`, `## Chapter One:`, or `### Transition:` markers rather than `# Chapter N:` numbered headers
- The existing ending (epilogue, final chapter) must be preserved, not removed

#### Step 1: Identify the Endpoint
The manuscript's final substantive line is the natural anchor. Find it by searching for the last narrative paragraph, not the last line of the file (which may contain AI artifacts or old epilogues). In a memoir, the ending is often a reflective closing image — e.g., "the willingness to touch the outlet anyway" or "That is enough."

```python
# Find the last meaningful line in the manuscript
last_line_marker = "willingness to touch the outlet anyway"
if last_line_marker in manuscript:
    idx = manuscript.rfind(last_line_marker)
    end_idx = manuscript.find('\\n', idx)
    if end_idx == -1: end_idx = len(manuscript)
    main_body = manuscript[:end_idx].strip()
```

#### Step 2: Write a Transitional Bridge
Write 1-3 paragraphs in the author's established voice that bridge the existing ending into the new section. The transition should:
- Return to a concrete present-moment scene (dinner, workshop, family)
- Expand outward thematically to the larger question the new section addresses
- Explicitly frame the new section (e.g., "One more story. Not a look backward — a look forward.")
- Use the same tone, rhythm, and narrative style as the main manuscript

```markdown
---

## The Threshold

Bob closes the document. Cindy is calling from downstairs. Dinner is on the table. The evening stretches ahead — ordinary, precious, irreplaceable.

But a story this size does not end at a dinner table...

What follows is not Bob's memory. It is Bob's imagination — offered to the generations who will inherit what he could only dream of building.

---
```

#### Step 3: Append Without Removing Anything
Combine the three parts:
```python
manuscript = main_body + "\\n\\n" + transition + "\\n\\n" + new_section
```

Do NOT remove the epilogue, AI artifacts, author's notes, or any other content. The existing ending is the user's work. Only insert the transition after it.

#### Step 4: Build the TOC from Organic Headers
Memoirs often use varied header styles. Parse multiple patterns:
```python
toc_entries = []
for line in manuscript.split('\\n'):
    s = line.strip()
    m1 = re.match(r'^# (Part \w+: .+)$', s)       # Part headers
    if m1: toc_entries.append(('part', m1.group(1))); continue
    m2 = re.match(r'^## (Chapter \w+: .+)$', s)    # Chapter headers (Roman numerals)
    if m2: toc_entries.append(('chapter', m2.group(1))); continue
    if s == '# Epilogue: The Unwritten Future':
        toc_entries.append(('epilogue', s[2:].strip())); continue

# Add the new final section
toc_entries.append(('final', 'Final Section: The Future After Bob'))

# Add ## subsections from the new section as sub-entries
for line in new_section.split('\\n'):
    s = line.strip()
    m = re.match(r'^## (.+)$', s)
    if m and m.group(1) in known_subsections:
        toc_entries.append(('sub', m.group(1)))
```

#### Step 5: CSS for Memoir vs Non-Fiction
Fiction/memoir uses indented paragraphs; non-fiction uses block paragraphs:
```css
/* Memoir */
.chapter-content p { text-indent: 1.5em; }

/* Non-fiction override for final section if it uses block style */
.final-section-content p { text-indent: 0; margin: 8px 0; }
```

#### Pitfalls
- **Splitting on the wrong marker** — The manuscript may have `# Chapter` lines in its TOC that look like section headers. Always anchor your search to the last narrative paragraph, not regex-based chapter detection.
- **Removing content accidentally** — The user explicitly said "do not remove content." Append only. Do not strip the epilogue, old transitions, or author notes even if they look like AI artifacts.
- **Header style mismatch** — Memoirs may use `## Chapter One:` (Roman) while the user's build script expects `## Chapter 1:` (Arabic). Parse both patterns.
- **New section headers conflicting with existing** — The new section's `##` sub-headings (e.g., "The Empty Chair") should appear in the TOC but NOT be treated as top-level chapters. Use a "sub" CSS class with indentation.
- **Transition voice mismatch** — The bridge paragraph must match the manuscript's voice. For memoirs, this means first-person reflective, with concrete sensory details (smells, sounds, gestures).

### 4. Quality Assurance

#### Content Verification Checklist
- [ ] **Fabricated-claim integrity pass**: For non-fiction books, scan for fabricated first-person claims ("I spent $43k," "my company built X," "my agent handles Y"). Rewrite as anonymized case studies, second-person framing, or illustrative examples. See `references/fabricated-claim-detection.md` for pattern catalog and batch-rewrite technique.
- [ ] **Humanization mandate**: ALL book prose — transitions, part divider pages, context boxes, front matter narrative, back matter, bridge sections, expanded content — MUST pass the `humanizer` skill's 29 pattern checks. No AI-isms, no filler, real voice, variable rhythm. This is mandatory for every piece of book text.
- [ ] **Reader engagement mandate**: ALL added material — transitions, part divider pages, context boxes, front matter narrative, back matter, bridge sections, expanded content — MUST be interesting, exciting, and engaging to readers. Every added element must serve the reader's experience, not just fill structural gaps.
- [ ] All chapters present and in correct order
- [ ] Transitions are meaningful and well-placed
- [ ] Images match chapter content and are properly positioned
- [ ] Table of contents matches chapter pages
- [ ] Front matter properly formatted and in correct order
- [ ] Copyright and ISBN information included
- [ ] Back matter complete (epilogue, author bio, etc.)

#### Technical Checks
- [ ] PDF renders correctly on multiple devices and PDF readers
- [ ] Fonts display properly
- [ ] Images are high resolution (300 DPI) and clear
- [ ] Margins are correct for chosen printer specifications
- [ ] No text is cut off or obscured by images
- [ ] File size appropriate for distribution method

## Delivery

### File Preparation
- **Print PDF**: High-resolution, CMYK color profile, proper bleeds
- **Ebook PDF**: Optimized for screen reading, smaller file size
- **Source Files**: HTML, CSS, and Markdown originals

### Distribution Methods
1. **Telegram Delivery**: Use `MEDIA:/path` for file delivery
2. **Print Service**: Upload directly to print-on-demand service
3. **Website**: Host on author website for download

### No-AI Login Handoff for KDP Upload

Amazon KDP (and all publishing platforms) block automated/AI logins. After all files are prepared, the final publishing step requires a shared-browser handoff:

1. **AI opens KDP**: Navigate to `https://kdp.amazon.com` via browser
2. **Bob logs in**: Bob enters credentials + 2FA manually in the shared browser
3. **AI guides entry**: Once on the KDP bookshelf, AI:
   - Clicks "+ Create" → "Create a new title"
   - Fills metadata: title, author, description, categories, keywords
   - Tells Bob to upload the manuscript EPUB file when an upload button is visible
   - Tells Bob to upload the cover **JPEG** file (2560×1600 px, RGB)
   - Guides pricing/royalty selection
   - Marks AI disclosure checkbox
4. **Bob submits**: Bob clicks "Publish Your Kindle eBook" button
5. **AI confirms**: Captures ASIN and product page URL from the confirmation screen

**Pre-upload checklist to have ready:**
- [ ] Manuscript file (EPUB for KDP, or clean PDF) saved locally
- [ ] **Manuscript has NO embedded front/back cover** — KDP Cover Creator handles cover display
- [ ] Cover image as **JPEG** (KDP requires `.jpg`, not `.png`; **2560×1600 px** ideal, min 1000×625 px, RGB, ≤50MB, quality 95)
- [ ] Paperback wrap cover as **PDF** (KDP requires PDF for print; calculated per trim+pages, 300 DPI min, CMYK preferred)
- [ ] AI Disclosure record (markdown file for reference)
- [ ] Marketing copy with description, categories, and keywords ready to paste
- [ ] ISBN for print version (if applicable)
- [ ] Pricing strategy (royalty path, list price, territorial rights)

### 3K. **Non-Fiction Business Book Writing (Parallel Subagent Pattern)**

Writing a non-fiction business book for a practitioner-author (someone who built what they're writing about) follows a different process from fiction. Chapters are modular, voice is first-person opinionated, and there's no character consistency to maintain across batches.

#### When to Use
- User asks to write a business/leadership/non-fiction book based on their real-world expertise
- The author has actual production experience with the topic (not theory — built it themselves)
- Target: 40 chapters at ~1,000-1,200 words each (~44,000-50,000 words for 180-200 pages at 6×9")
- Book needs front/back matter plus publishing package

#### Phase 1: Book Concept & Market Research

Before writing a word, research the competitive landscape:

1. **Search for existing books** on the topic — check Amazon, O'Reilly, Wiley for direct competitors
2. **Identify the gap** — what unique angle does this author bring that no existing book has?
   - Practitioner-owner who built it themselves > consultant/researcher > platform vendor
3. **Position the subtitle** — the subtitle is your competitive thesis in one line
4. **Target KDP categories** — pick 3 specific BISAC categories where the book can rank

Example from this session: *The Autonomous Enterprise* positioned against 6 competing books, winning on the "built and operates it daily" angle.

#### Phase 2: Chapter Outline & Voice Guide

Create a master planning document with:

**Voice Rules (for subagents):**
- First person, real experience — "I built this. I broke this. I fixed this."
- Honest about failures — share what went wrong, not just wins
- Short sentences mixed with longer explanations — varied rhythm
- No AI-isms — run all output through the humanizer checklist (29 patterns)
- No hype — no "revolutionary", "game-changing", "groundbreaking"
- Specific > vague — real numbers, real names, real costs
- Opinionated — say what you actually think, not what sounds balanced
- No em dashes every sentence — mix in periods, commas, colons

**Chapter Structure (each chapter):**
1. **Opening hook** — a specific moment, problem, or question. Start in the middle of something.
2. **The framework** — what this chapter is actually about. Brief context.
3. **Real example** — how this works in practice. Either the author's system or a realistic composite.
4. **The lesson** — what the reader should take away. Direct and actionable.
5. **Bridge to next** — one line that sets up what comes next (optional, don't force it).

**4-Part Narrative Arc (40 chapters):**
| Part | Theme | Chapters | Narrative Function |
|------|-------|:--------:|--------------------|
| I | The Problem | 1-10 | Establish the gap between promise and reality. Why existing approaches fail. |
| II | The Solution | 11-20 | Build the first working prototype. Step-by-step, hands-on. |
| III | Scale | 21-30 | Move from one to many. Architecture, operations, production realities. |
| IV | The Vision | 31-40 | What comes next. Philosophy, roadmap, call to action. |

#### Phase 3: Parallel Batch Writing

Non-fiction books benefit from parallel writing because chapters are self-contained:

1. **Create the planning doc** — concept, outline, voice guide, chapter summaries (saved to book directory)
2. **Delegate 4 batches of 10 chapters** via `delegate_task`:
   - Each task receives: voice guide + humanizer rules + their 10 chapter outlines with detailed summaries
   - Each task writes ~1,000-1,200 words per chapter, saves as `chXX.md`
   - Max 3 concurrent children — batch 3+1 if 4 batches
3. **Each subagent also receives**: a sample chapter from an already-written batch or the book plan for voice calibration
4. **No character consistency needed** — business books don't track characters across chapters, so batches are fully independent

#### Phase 4: Compile & QA

After all batches return:

1. **Normalize heading levels** — different subagents may use `# Chapter N:` or `## Chapter N — Title`. Normalize all to consistent format (recommended: `## Chapter N — Title`)
2. **Verify all 40 chapters present** — `grep -c "^## Chapter" manuscript.md`
3. **Run humanizer word-frequency scan** on the compiled manuscript:
   ```python
   patterns = ['delve', 'revolutionize', 'game-changing', 'groundbreaking', 
               'cutting-edge', 'synergy', 'paradigm', 'leverage', 'unlock',
               'empower', 'pivotal', 'testament', 'showcase', 'additionally',
               'tapestry', 'intricate', 'fostering', 'vibrant']
   for p in patterns:
       if re.search(r'\b' + p + r'\b', text):
           print(f'FOUND: {p}')
   ```
4. **Check em dash count** — aim for < 3 per 1,000 words. Use `text.replace('—', '. ')` for bulk reduction if over target.
5. **Verify total word count** — target 44,000-50,000 words (~250 words/page = 180-200 pages at 6×9")
6. **Count chapter word counts** — ensure each is ~1,000-1,200. Expand or trim outliers.

#### Phase 5: Generate EPUB & Publishing Package

Use the same EPUB builder as fiction books (see `book-deliverable-kdp` skill), but with non-fiction front matter:
- **Copyright** includes disclaimer (see section 3G)
- **TOC** includes part divider labels
- **Body CSS** uses block paragraphs (`p { text-indent: 0; margin: 6px 0; }`) instead of indented paragraphs
- **Back cover blurb** positions the book against the competitive gap identified in Phase 1

#### Pitfalls
- **Inconsistent heading levels**: Subagents naturally use different `#` / `##` / `###` levels. Always normalize after compilation.
- **Missing part dividers**: The compiled manuscript may have 40 consecutive chapters with no section breaks. Inject `# PART N — Title` dividers at chapters 1, 11, 21, 31.
- **Em dash creep**: Each subagent writes ~10 chapters with 10-15 em dashes = 100-150 total across all batches. Do a bulk reduction pass.
- **Author voice drift**: Subagents may drift into neutral/expository voice. The voice guide must explicitly say "first person, I statements, honest about failures." A sample chapter from batch 1 helps calibrate later batches.
- **Tool loop warning**: If `delegate_task` returns duplicate subagent content, verify each subagent wrote independently by spot-checking chapter opening sentences for unique phrasing.
- **Humanizer is mandatory, not optional**: Every piece of book prose must pass the 29-pattern humanizer check. This is a permanent requirement (see memory/user profile).

## Best Practices

### Content Creation
- Write transitions that connect emotionally with readers
- Balance action with introspection in fiction works
- Show, don't tell - use sensory details and specific examples
- Maintain consistent voice throughout the book

### Technical Implementation
- Test PDF conversion early and often with sample chapters
- Keep original AI prompts for future image regeneration
- Maintain version control for all manuscript iterations
- Create backup copies of all generated files

## Example Project Structure

```
book-project/
├── manuscript/
│   ├── edited/                 # Edited manuscript
│   └── final.md                # Final Markdown
├── formatting/
│   ├── html/                   # HTML files
│   └── css/                    # CSS stylesheets
├── images/
│   ├── generated/              # AI-generated images
│   └── final/                  # Optimized images
├── pdf/
│   ├── drafts/                 # Test PDFs
│   └── final/                  # Production PDFs
└── scripts/                    # Automation scripts
```

## Integrated Single-Script Pipeline

**For all new builds, use `hermes-publish`** (see Quick Start above). The patterns below are preserved for reference and custom scripts.

For production efficiency, build a single `generate_all.py` script that does all format generation in one pass, rather than running separate tools for HTML, EPUB, and PDF. The pattern:

1. **Load manuscript** → parse `## Chapter N — Title` headers into chapter list
2. **Build rich HTML** with cover (base64-embedded), copyright, TOC with chapter titles, all chapters, back cover
3. **Derive EPUB from the same HTML** — extract cover, copyright, TOC, chapter sections, and back matter from the HTML body using regex, then assemble EPUB3 structure (mimetype, container.xml, content.opf, nav.xhtml, per-chapter XHTML)
4. **Derive PDF from the same HTML** — pass directly to WeasyPrint: `HTML(string=html_content).write_pdf(output_path)`

This approach ensures three formats are always in sync — no drift between HTML and EPUB/PDF content.

### Cover Embedding Technique

Embed cover art as a base64 data URI so the HTML is fully self-contained (no external image files):

```python
cover_file = os.path.join(cover_dir, f"{book_key}_Cover.png")
if os.path.exists(cover_file):
    with open(cover_file, "rb") as f:
        cover_b64 = base64.b64encode(f.read()).decode("utf-8")
    cover_img_html = f'<img src="data:image/png;base64,{cover_b64}" alt="Cover" ... />'
```

For EPUB, include the cover image in the manifest with `properties="cover-image"` AND a separate cover XHTML in the spine. Both are required for KDP/Apple Books.

### CSS Pitfall: Blank Pages Before Every Chapter

A common mistake: setting `page-break-before: always` on the general `h2` rule. Because chapter headings use `<h2>`, this inserts a blank page before every single chapter. **Fix:** Scope page breaks:

```css
h2 { page-break-before: always; }           /* structural h2 (copyright, TOC) */
.chapter-body h2 { page-break-before: avoid; margin-top: 1cm; }  /* chapter titles */
```

This keeps page breaks on structural elements (cover → copyright → TOC → chapters) while letting chapters flow naturally without leading blank pages.

### Text-Only Margins with Full-Bleed Art Breakout

When a book contains chapter art that should extend to the page edges while body text sits at a defined margin, use `@page` margins for text and a CSS breakout class for images.

#### Pattern

```css
/* Text sits at 0.75in top/bottom, images can bleed past */
@page {
  size: 6in 9in;
  margin: 0.75in 0.8in;   /* top/bottom, left/right — text margins */
  @bottom-center { content: counter(page); }
}

/* Full-bleed art — negative margins extend past text margins to page edges */
.art, .full-bleed {
  margin: 0 -0.8in;                /* cancel left/right margins horizontally */
  width: calc(100% + 1.6in);       /* extend past left+right margins combined */
  max-width: none;
  display: block;
}
.art img, .full-bleed img {
  width: 100%;
  height: auto;
  display: block;
}
```

#### How It Works

- `@page margin: 0.75in 0.8in` sets the text content area 0.75" from top/bottom edges
- The `.full-bleed` class uses negative left/right margins to break out of the content area
- `calc(100% + 1.6in)` adds back the width consumed by the 0.8in left + 0.8in right margins, making the element span the full page width
- Images set to `width: 100%; display: block` fill the breakout container edge-to-edge

#### Usage in Manuscript HTML

```html
<!-- Regular text sits at 0.75in margin -->
<p>Margaret stared at the holodisplay...</p>

<!-- Chapter art wraps in .full-bleed, extends to page edge -->
<div class="full-bleed">
  <img src="chapter1.png" alt="The moon base at dawn">
</div>

<!-- Text resumes at normal margin -->
<p>The numbers didn't lie...</p>
```

#### Pitfalls

- **Margin values must match.** The `-0.8in` and `+1.6in` values in `.full-bleed` must exactly cancel the `@page` left/right margins. If you change page margins, recalculate both values.
- **No `max-width: 100%`** — the breakout element is intentionally wider than its parent container. If a parent element has `max-width` or `overflow: hidden`, the breakout will be clipped.
- **EPUB compatibility**: E-readers handle breakout differently. This technique works best in WeasyPrint PDFs. For EPUB, full-bleed art is less critical since e-readers typically scale images to screen width anyway.
- **Page-edge art only left/right**: The `.full-bleed` class only breaks out horizontally (left/right). To have art break out of top/bottom margins too, add `margin-top: -0.75in` and `height: calc(...)` adjustments. Typically chapter art only needs horizontal bleed.
- **Inline elements**: The `.full-bleed` class sets `display: block`. Do not apply it to inline elements or text spans.

### Duplicate Content Detection Across Series

When restructuring a multi-series library, books from different series that share identical chapter titles are likely duplicates (same content, different character names). This happened with the No Blue Sky / Lunar Foundation series where Books 4/6 and 5/7 were identical.

**Detection technique:**

```python
# Compare chapter titles across books
for book_a in series_a_books:
    for book_b in series_b_books:
        ch_titles_a = extract_chapter_titles(book_a)
        ch_titles_b = extract_chapter_titles(book_b)
        overlap = set(ch_titles_a) & set(ch_titles_b)
        if len(overlap) > len(ch_titles_a) * 0.8:
            print(f"DUPLICATE: {book_a} == {book_b}")
```

**Verification:** Even if chapter titles are identical, check body text for a shared unique string (e.g., a typo or Mission AI line) to confirm duplication. In one real case, a copy-paste error ("Chapter 36" instead of "Chapter 16") appeared in BOTH books across different series, conclusively proving they derived from the same source.

**Remediation:** Rewrite one copy as a completely distinct story with different plot, characters, and genre (e.g., political thriller vs survival story vs mystery). The rewritten book must have a unique title, unique chapter sequence, and no shared narrative content.

### Page Count Compression (Content Trimming)

After quality improvements add content, books may exceed the 180-200 page target. To compress without changing font size or margins:

1. **Extract full content** from the last clean PDF or HTML source
2. **Rebuild HTML from extracted text** using the original chapter structure
3. **Trim proportionally** — keep first ~85% of sentences per chapter, dropping redundant expansions
4. **Verify** by regenerating PDF and checking page count

For aggressive compression, split scene-break sections and keep only the first 1-2 scenes per chapter. The opening + one development scene preserves the narrative arc while cutting filler.

When splitting a single manuscript into multiple books at a chapter boundary (e.g., chapter 20/21, or splitting an already-split volume further):

#### Finding the Split Point
Analyze cumulative word counts per chapter to locate the target page boundary (250 words/page):

```python
import re
with open("manuscript.md") as f:
    content = f.read()
chunks = re.split(r'^## Chapter (\d+)', content, flags=re.MULTILINE)
chapters, current_num = {}, None
for chunk in chunks:
    chunk = chunk.strip()
    if not chunk: continue
    if chunk.isdigit(): current_num = int(chunk)
    elif current_num is not None: chapters[current_num] = len(chunk.split())

cumulative, target_words = 0, 100 * 250  # target_pages * 250
for num in sorted(chapters):
    cumulative += chapters[num]
    if cumulative >= target_words:
        print(f"Split after Chapter {num}")
        break
```

#### The Split (with renumbering)
Use `re.split()` on `## Chapter N — Title` headers, reconstruct the chapter list, then split at the boundary. For the **second book**, renumber chapters sequentially (Chapter 19 → Chapter 1, etc.) by targeting only header lines with `re.sub(r'Chapter \d+', f'Chapter {new_num}', ...)` — do NOT replace chapter numbers in body text or dialogue.

#### Sequential/Recursive Splitting
An already-split volume (e.g., "Part 2" that was itself the result of a previous split) can be split again into updated Part 2 + Part 3. Key considerations:
- **Part 2 keeps its existing cover** (subtitle "PART 2" stays the same) — no need to regenerate unless the cover file naming changed
- **Cover filename consistency check**: The cover generation script and publishing script must use the same filename prefix (e.g., both `Book_Part_2_Cover.png`, not `Book_Pt2_Cover.png` vs `Book_Part_2_Cover.png`)
- **Part 3 needs a new cover** that visually advances the series aesthetic (different scene/subject, same typography style)

#### Rewriting Boundary Chapters

The split point needs two targeted rewrites:

**Book 1's last chapter** — rewrite as a series-ending chapter:
- A closing arc that resolves the book's central tension
- Characters reflecting on how far they've come (viewport/observation scene optional but effective)
- A thematic callback to the series title
- A bridge paragraph (italic, marked as "Bridge" or "End of Book N") that sets up what's coming in the next book
- The closing should feel like a chapter end AND a book end

**Book 2's first chapter** — rewrite the opening to include:
- A **book-level Mission AI ping** using the convention: `Mission AI: "Book N — Chapter 1: [thematic summary]"` — this distinguishes it from regular chapter-level Mission AI lines
- A **summary transition paragraph** (the "bridge" from Book 1's cliffhanger or resolution) that re-establishes setting and stakes
- The original chapter's content — keep it intact, only replace the opening lines
- A character quote that reflects the new book's theme

**Common pitfall — duplicate Mission AI lines:** When inserting new book-opening content before the original Chapter 1's `*Mission AI: ...*` line, the old opening lines survive and create duplicates. After inserting the new opening, **always check for and remove** the old duplicate Mission AI + character quote pair that immediately follows.

#### Chapter Header Parser Pitfall
Some manuscripts have two `##` lines per chapter (bare `## Chapter N` followed by `## Chapter N — Title`). Match only `## Chapter N — Title` (with dash/title after the number) to avoid double-splitting.

#### Regenerate
After splitting and rewriting, regenerate all three formats (HTML, EPUB, PDF) for both books from their respective manuscripts using the Integrated Single-Script Pipeline above.

### Historical Transition Sections (Memoir/Non-Fiction)

Long-form memoirs need 2-4 page historical context sections placed between chapters/parts. These contextualize the author's personal events against the broader world events of the era.

**When to Use:** Memoirs spanning decades where the reader needs world context (wars, cultural shifts, technological changes) between personal chapters.

**Technique:**
1. Map all existing transitions first. Extract every year/event mentioned in transitions to understand what's already covered.
2. For each new transition, identify the gap's time period and key events that the author lived through but aren't mentioned elsewhere.
3. Write 4-6 paragraphs in the author's established voice — connecting world events to the author's personal experience. The transition should frame what happened OUTSIDE the author's door while their life unfolded inside.
4. Insert at the appropriate chapter boundary (typically after a chapter ends, before a part/chapter begins).
5. Rebuild all formats (PDF/EPUB/DOCX) — page numbers shift, so TOC must be regenerated with correct page numbers.

**Critical Pitfalls:**
- **Duplicate events:** Track every event mentioned across ALL transitions (Sputnik, Vietnam, 9/11, COVID, etc.). A new transition MUST NOT repeat events already covered in an existing one. Use a shared event registry.
- **Historical accuracy:** The transition must be factually accurate for the dates mentioned. If a chapter spans 2005-2015 and mentions the Great Recession, the transition should not attribute it to the wrong year.
- **Tone consistency:** Transition sections must match the author's narrative voice — not shift into textbook prose. They should read like the author reflecting on the times, not a history lecture.
- **Stream stall awareness:** Large write operations on manuscript files (>10KB) may cause stream stalls. Break file writes into small sequential steps when this occurs.
- **Multiple formats, one source:** Always rebuild from a single canonical markdown file. Never let PDF/EPUB/DOCX drift from the source — they must all be derived from the same manuscript.

## Troubleshooting

**Issue**: Images not generating properly
**Solution**: Refine prompts with more specific details, try different AI models

**Issue**: PDF formatting breaks or looks wrong
**Solution**: Check CSS for print-specific rules, ensure proper page breaks, validate HTML structure. Most common fix: scope `page-break-before` to structural elements only, not generic h2.

**Issue**: WeasyPrint not available or not working
**Solution**: Use browser print method or install wkhtmltopdf as alternative

**Issue**: Images not displaying in PDF
**Solution**: Check file paths, ensure images are accessible, use absolute paths if needed. For self-contained HTML, use base64 data URIs — they always resolve regardless of filesystem context.

**Issue**: EPUB shows duplicate chapters or wrong number of chapters
**Solution**: The EPUB generator extracts chapters from the final HTML using regex. If the manuscript has two `##` lines per chapter (e.g., `## Chapter N` plus `## Chapter N — Title`), the regex may split on both. Fix the parser to only split on lines matching `## Chapter N — Title` (with dash after the number).

**Issue**: Telegram PDF delivery times out for large files (>2MB)
**Solution**: Send large PDFs individually rather than bundled with other files in one message. The HTML and EPUB will send fine together; send the PDF in its own follow-up message.

### EPUB Rendering Errors: "Entity 'nbsp' not defined"

If every chapter in the EPUB shows:
```
error on line 6 at column 10: Entity 'nbsp' not defined
```
The markdown chapter files contain `&nbsp;&nbsp;&nbsp;&nbsp;` for paragraph indentation. `&nbsp;` is an HTML entity that is NOT valid in XHTML (which EPUB requires).

**Fix:** In `md_to_html_simple()`, add `line = line.replace('&nbsp;', '&#160;')` as the first line of the loop, before any other processing.

### Chapter Titles Show "Chapter N" Instead of Actual Title

If EPUB TOC and chapter headers show "Chapter 4: Chapter 4" instead of "Chapter 4: The Sister's Plea", the title extraction in `collect_chapters()` only handles `# Title` markdown headers, not plain text titles.

**Fix:** Update the extraction to handle both formats:
```python
if first.startswith('#'):
    title = first.lstrip('#').strip()
elif first.strip():
    title = first.strip()  # Plain text title like "The Sister's Plea"
else:
    title = f"Chapter {num}"
```

### Chapter Title Appears as First Paragraph Body Text

If the chapter title appears both in the `<h2>` header AND as the first paragraph of body content, the title line from the chapter file is being passed through as body text.

**Fix:** In the EPUB generation loop, strip the title line before converting to HTML:
```python
if book["manuscript_type"] == "chapters_md":
    cl = content.split('\n')
    if cl and (cl[0].strip().startswith('#') or 
               (len(cl[0].strip()) < 60 and not cl[0].strip().startswith('---'))):
        content = '\n'.join(cl[1:]).strip()
```

### Page Count 2-3x Expected Length

If the user reports 474 pages when expecting ~180, they are looking at a stale PDF/EPUB from BEFORE condensation. Delete old output files before regenerating:
```bash
cd /path/to/book/output && rm -f *.pdf *.epub *.zip
```

### Condensation Too Aggressive — Below 150 Pages

For a 150-190 page 6x9" book, you need ~36,000-51,000 words. If condensation falls below 36K words, reduce aggressiveness (keep 55-60% instead of 45%). Target ~1,200-1,700 words per chapter for 30 chapters.

### EPUB Rendering Errors: "Entity 'nbsp' not defined"

If every chapter in the EPUB shows "Entity 'nbsp' not defined", the markdown chapter files contain `&nbsp;&nbsp;&nbsp;&nbsp;` for paragraph indentation. `&nbsp;` is NOT valid in XHTML/EPUB. Fix: in `md_to_html_simple()`, add `line = line.replace('&nbsp;', '&#160;')` as the first line of the loop.

### Chapter Title Duplication

If EPUB shows "Chapter 4: Chapter 4" or title appears in both `<h2>` and body text: (1) strip `Chapter N:` prefix from extracted titles with `re.sub(r'^Chapter\s+\d+:\s*', '', title)`, (2) strip title line from content before EPUB generation, (3) clear Python `__pycache__` after editing pipeline code.

### Stale Output Files

Delete old PDF/EPUB/ZIP outputs before regenerating to avoid user confusion between old (474-page) and new (180-page) versions.

## Appending External Content as an Appendix

When a user provides an external PDF (case study, research paper, article) to include as an appendix in an existing book, use this workflow:

### When to Use
- A PDF document (case study, whitepaper, interview transcript) needs to be appended to the end of a completed manuscript
- The user wants to expand a book with new material without modifying the original chapters
- Back cover needs updating with review blurbs from partner companies or endorsers

### Step 1: Extract PDF to Markdown
Use `pdftotext` (from poppler-utils) to extract the text, then clean up PDF artifacts:

```bash
pdftotext "/path/to/document.pdf" - > /tmp/extracted.txt
```

**Common PDF artifacts to clean:**
- Spaced-out capital letters: `A C A S E S T U D Y` → replace with the properly spaced form
- Page numbers on their own lines: skip lines that are just a number < 5 digits
- Table of Contents sections: skip entries that list chapters with page numbers
- Part/chapter header formatting: normalize to markdown heading levels (`##`, `###`)
- Repeated title/author blocks at chapter starts

### Step 2: Build the Combined HTML

Write (or extend an existing) build script that:

1. **Reads the original manuscript** (markdown with `## Chapter N` headers)
2. **Extracts the appendix content** from the cleaned markdown
3. **Builds HTML structured as:** Cover → Title → Copyright → TOC → Chapters → Appendix → Back Cover

**CSS sections to add:**
```css
.appendix { page-break-before: always; }
.appendix h2 { font-size: 20pt; text-align: center; }
.appendix h3 { font-size: 16pt; margin-top: 25px; }
.back-cover { page-break-before: always; background-color: #000000; color: #ffffff; text-align: center; padding: 60px 40px; min-height: 600px; }
.back-cover .review { font-style: italic; font-size: 13pt; margin: 30px 0; color: #e0e0e0; }
.back-cover .review-author { font-style: normal; font-size: 11pt; color: #aaaaaa; }
.back-cover hr { border: none; border-top: 1px solid #444; margin: 30px 60px; }
```

### Step 3: Build the Back Cover

The back cover typically includes:
- Book title (white, large)
- Subtitle (white, smaller, italic)
- 2-3 review blurbs from endorsers (italic white on black, 13pt)
- Reviewer attribution (smaller, gray)
- Publisher/imprint branding at bottom

### Step 4: Avoid Duplicate TOCs

If the original markdown has a TOC section AND the build script generates one programmatically, you'll get two TOCs in the output. **Remove the programmatic TOC generation** in the build script and rely on the markdown's own TOC. Update the markdown TOC to include the appendix entry.

### Step 5: Generate the Combined Package

```python
# Key structure for the build script:
html_parts = [
    # Front matter (cover, title, copyright) — hardcoded
    # TOC — from markdown or single programmatic version
    # Chapters — from original manuscript, unchanged
    # Appendix — from extracted PDF markdown, with .appendix CSS class
    # Back cover — hardcoded black background with reviews
]
```

Save to the manuscript's final print HTML path. Also save a combined markdown version with `## Appendix:` header added at the end.

### Pitfalls

- **PDF extraction quality**: `pdftotext` may mangle columns, tables, or complex layouts. Always review the extracted text for artifact lines (page numbers, TOC lists, header/footer repeats).
- **Second TOC**: When adding an appendix, update the TOC to include it. If there are TWO TOCs (one in markdown, one programmatic), remove the programmatic one to avoid duplicates.
- **Back cover CSS isolation**: The `.back-cover` styles must NOT inherit from the body styles. Use explicit `color: #ffffff` and `background-color: #000000` to guarantee visual independence from the book's interior CSS.
- **File size**: Appending a large external document can double the manuscript size. Verify the generated HTML still renders within reasonable load times.

## KDP Print-Ready PDF Generation

When a user needs a print-ready PDF for KDP paperback, generate a version with **bleeds** — the print area extends 0.125" beyond the trim on each edge.

### Technique: WeasyPrint with Bleed CSS

Start from the same HTML used for the ebook, but modify the CSS:

```css
/* KDP Print-Ready: 6x9in + 0.125in bleed */
@page {
    size: 6.25in 9.25in;  /* 6x9 + 0.125in bleed on each side */
    margin: 0.75in;  /* safe margin inside bleed */
    @top-center { content: "BOOK TITLE"; font-family: 'Times New Roman', Times, serif; font-size: 8pt; color: #999; }
    @bottom-center { content: counter(page); font-family: 'Times New Roman', Times, serif; font-size: 9pt; color: #666; }
}
@page:first { @top-center { content: none; } @bottom-center { content: none; } }
```

**Important:** Remove the front cover page from the interior PDF (KDP uses the wrap cover as the cover, so the interior starts with the title page). Strip the cover div before generating the print PDF:

```python
# Remove front cover from interior (KDP uses wrap cover)
html = re.sub(r'<!-- COVER -->.*?<!-- TITLE PAGE -->', '<!-- TITLE PAGE -->', html, flags=re.DOTALL)
```

### Full KDP Package Bundling

When asked for a "KDP package" or "everything to publish," build a structured ZIP with both Kindle and Print subdirectories:

```python
PKG_DIR = Path("BookName_KDP_PACKAGE")
for d in ["Kindle", "Print", "Marketing_and_Compliance", "Source"]:
    (PKG_DIR / d).mkdir(parents=True)
```

**Package structure:**

```
BookName_KDP_PACKAGE/
├── README.md                          # Upload instructions
├── Kindle/
│   ├── BookName.epub                  # Kindle manuscript (upload to KDP)
│   └── BookName_Cover.jpg             # Cover as JPEG (KDP requires .jpg; 2560×1600px, RGB, ≤50MB)
│   └── BookName_Cover.png             # Source cover PNG (for regeneration)
├── Print/
│   ├── BookName_Print_Ready.pdf       # 6x9in + bleeds
│   ├── BookName_Wrap_Cover.pdf        # Full wrap — PDF (KDP requires PDF for print covers)
│   └── BookName_Cover.png             # Front cover source
├── Marketing_and_Compliance/
│   ├── Marketing_Copy.md              # Description, categories, keywords
│   └── KDP_AI_Disclosure.md           # AI use record
└── Source/
    └── BookName_Manuscript.md         # Full source
```

### Marketing Copy Template

When generating Marketing_Copy.md, include these specific KDP fields:

```markdown
# BOOK TITLE: MARKETING COPY

## Book Title
**[Title]: [Subtitle]**

## Author
[Name]

## Description (Short - 200 characters)
One compelling hook sentence...

## Description (Long - Amazon Style)
**Bold hook sentence.**

[1-2 paragraphs establishing stakes and value proposition]

**Inside you'll discover:**
- Bullet 1
- Bullet 2
...

**This book is for you if:**
- You run a small business with limited time and budget
- ...

**What readers are saying:**
"Review quote..."

## Categories
- BUSINESS & ECONOMICS / Small Business
- COMPUTERS / Artificial Intelligence / General
- BUSINESS & ECONOMICS / Entrepreneurship
(3-5 BISAC categories)

## Keywords (comma-separated)
15-20 relevant keywords...

## Pricing
- Kindle eBook: $9.99
- Paperback: $14.99
- Hardcover: $24.99

## Book Details
- Title, Subtitle, Author, Edition, Language, Trim Size, Pages, Publication Date
```

### Full Wrap Cover Creation (Back + Spine + Front)

When preparing a book for print-on-demand (KDP paperback, IngramSpark, etc.), a full wrap cover image is needed — a single wide canvas containing the back cover, spine, and front cover in one piece.

### When to Use
- The user requests a "full wrap cover" or "cover with spine and back" for print-on-demand
- A paperback/hardcover edition needs retail-ready cover art
- The book already has a front cover image and needs matching back + spine panels

### CRITICAL: KDP requires wrap cover as PDF, not PNG/JPEG
Paperback and hardcovers covers must be submitted to KDP as a **single-page PDF file**. PNG/JPEG wrap covers are NOT accepted for print. See full specs in `book-deliverable-kdp` skill.

### Key Dimensions (for 6×9" trade paperback)

| Panel | Width (inches) | Height (inches) |
|-------|---------------|-----------------|
| Front | 6.0 | 9.0 |
| Spine | Varies with page count | 9.0 |
| Back | 6.0 | 9.0 |
| **Full wrap width** | 0.125 + 6.0 + spine + 6.0 + 0.125 | 9.25 |
| (at 300 DPI) | Width × 300 | Height × 300 |

**Spine width (for B&W books on white paper):** `pages × 0.002252"`
- 200 pages: 200 × 0.002252 = 0.4504"
- 214 pages: 214 × 0.002252 = 0.4819"

**Total wrap width:** `0.125" (bleed) + 6.0" (back) + spine + 6.0" (front) + 0.125" (bleed) = 12.25" + spine`
**Total wrap height:** `0.125" (bleed) + 9.0" (trim) + 0.125" (bleed) = 9.25"`

**At 300 DPI (pixels):** `wrap_width_inches × 300`, `wrap_height_inches × 300`

### Implementation (PIL/Pillow → PDF conversion via img2pdf)

```python
from PIL import Image, ImageDraw, ImageFont
import img2pdf  # or use reportlab to embed in PDF
from io import BytesIO

# --- Configuration ---
TRIM_W = 6.0       # inches
TRIM_H = 9.0       # inches
PAGE_COUNT = 200   # actual page count
PAPER_TYPE = 'white'  # 'white' or 'cream'

BLEED = 0.125
SPINE = PAGE_COUNT * 0.002252 if PAPER_TYPE == 'white' else PAGE_COUNT * 0.0025
WRAP_W_IN = BLEED + TRIM_W + SPINE + TRIM_W + BLEED
WRAP_H_IN = BLEED + TRIM_H + BLEED

DPI = 300
WRAP_W_PX = int(WRAP_W_IN * DPI)
WRAP_H_PX = int(WRAP_H_IN * DPI)
FRONT_W_PX = int(TRIM_W * DPI)
SPINE_W_PX = int(SPINE * DPI)
BACK_W_PX = int(TRIM_W * DPI)

# Safe zone: keep text 0.25" inside trim = 0.125" bleed + 0.125" = 0.25" from cover edge
SAFE = int(0.25 * DPI)

# --- Build the wrap ---
front = Image.open("front_cover.png").convert("RGBA")
front = front.resize((FRONT_W_PX, WRAP_H_PX), Image.LANCZOS)

wrap = Image.new("RGBA", (WRAP_W_PX, WRAP_H_PX), (0, 0, 0, 255))

# 1. Back cover (left panel)
back = Image.new("RGBA", (BACK_W_PX, WRAP_H_PX), (0, 0, 0, 255))
draw = ImageDraw.Draw(back)

# Find available font
for fp in ['/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
            '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf']:
    if os.path.exists(fp): font_path = fp; break

title_font = ImageFont.truetype(font_path, int(DPI * 0.25))  # ~0.25" height
draw.text((SAFE, SAFE), "BOOK TITLE", fill=(255,255,255), font=title_font)
blurb_y = int(DPI * 1.5)
draw.text((SAFE, blurb_y), "\"Compelling review quote\"", fill=(200,200,200),
          font=ImageFont.truetype(font_path, int(DPI * 0.15)))
wrap.paste(back, (0, 0), back)

# 2. Spine (center panel)
spine = Image.new("RGBA", (SPINE_W_PX, WRAP_H_PX), (10, 10, 25, 255))
draw_spine = ImageDraw.Draw(spine)
if SPINE > 0.5:  # Only add text if spine is wide enough
    spine_font = ImageFont.truetype(font_path, int(DPI * 0.18))
    draw_spine.text((SPINE_W_PX//2, WRAP_H_PX//2), "TITLE • Author",
                    fill=(200,200,200), font=spine_font, anchor="mm")
wrap.paste(spine, (BACK_W_PX, 0), spine)

# 3. Front cover (right panel)
wrap.paste(front, (BACK_W_PX + SPINE_W_PX, 0), front)

# --- Save as PNG first, then convert to PDF ---
# Save high-res PNG
wrap_png_path = "Wrap_Cover.png"
wrap.save(wrap_png_path, "PNG", optimize=True, dpi=(DPI, DPI))

# Convert to PDF (KDP requirement)
with open(wrap_png_path, "rb") as f:
    pdf_bytes = img2pdf.convert(f.read())

with open("Wrap_Cover.pdf", "wb") as f:
    f.write(pdf_bytes)

print(f"Wrap cover: {WRAP_W_PX}x{WRAP_H_PX} px ({WRAP_W_IN:.3f}x{WRAP_H_IN:.3f} in at {DPI} DPI)")
print(f"Spine: {SPINE:.4f} in ({SPINE_W_PX} px)")
print(f"Front cover width: {FRONT_W_PX} px")
print(f"Back cover width: {BACK_W_PX} px")
print(f"Saved: Wrap_Cover.png (source) and Wrap_Cover.pdf (KDP submission)")
```

### Files to Deliver
Save the wrap cover alongside the front cover in the publishing package:
```
BookName_KDP_PACKAGE/
├── Kindle/
│   ├── BookName.epub               # Kindle manuscript
│   └── BookName_Cover.jpg           # JPEG, 2560×1600 px, RGB
├── Print/
│   ├── BookName_Print_Ready.pdf    # Interior PDF with bleeds
│   ├── BookName_Wrap_Cover.pdf     # Full wrap — PDF (KDP requirement)
│   └── BookName_Cover.png          # Front cover source PNG
```

### Back Cover Content Layout

The back cover typically includes (top to bottom):
- **Book title** (white, large, centered)
- **Subtitle** (light gray, smaller)
- **Divider line** (thin, dark gray)
- **Review blurbs** (italic, light gray/white, ~16pt) — 2-3 quotes from endorsers
- **Reviewer attributions** (smaller, gray)
- **Divider line**
- **Publisher/imprint branding** (small, bottom)
- **ISBN / price** (small, bottom — placeholder or actual)

### Review Blurb Formatting
```python
reviews = [
    ('"Quote from endorser one. Keep it to 1-2 sentences."', '— Endorser Name, Company'),
    ('"Quote from endorser two."', '— Endorser Name, Organization'),
]
y_start = 150
for quote, author in reviews:
    draw.text((60, y_start), quote, fill=(220,220,220), font=review_font)
    draw.text((80, y_start + 100), author, fill=(160,160,160), font=author_font)
    y_start += 200  # spacing between reviews
```

### Spine Text
For a readable spine on a trade paperback (1"+ spine width), use horizontal text centered on the spine panel. For narrow spines (<1"), text is typically rotated 90 degrees (bottom-to-top). Decision rule: if `spine_w > 180px` at 300 DPI, use horizontal; otherwise use vertical rotated text.

### Font Discovery
Always check these common font paths in order, falling through until one exists:
```python
for fp in [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
]:
    if os.path.exists(fp):
        font_path = fp
        break
```

### Files to Deliver (old — replaced by KDP package structure above)

---
category: creative
related_skills:
  - openrouter-image-generation
  - manuscript-preparation-and-delivery
requirements:
  - Python 3.8+
  - WeasyPrint (for PDF conversion)
  - OpenRouter API access (for image generation)
  - Basic HTML/CSS knowledge
  - Text editor
