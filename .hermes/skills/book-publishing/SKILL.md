---
name: book-publishing
description: "Amazon KDP book publishing workflow: smart skip/publish pipeline, ASIN lookup, editorial audit, derivable generation, Kindle link generation, KDP package building"
---

# Book Publishing Workflow

## 🔍 MemPalace Query (MANDATORY FIRST STEP)
Before proceeding, query MemPalace for existing context:
```python
import sys, os; sys.path.insert(0, os.path.expanduser('~/.hermes/mempalace'))
import embed; embed.init_embedding(os.path.expanduser('~/.hermes/mempalace'))
results = embed.search_embeddings("book publishing [your specific topic]", k=5)
```

## Amazon ASIN Lookup
To find ASINs for published books, search Amazon for author "Bob J Mills":
1. Go to `https://www.amazon.com/s?k=%22Bob+J+Mills%22&i=digital-text`
2. Extract ASINs from the `data-asin` attributes on each result card
3. Use the DevTools console query:
   `Array.from(document.querySelectorAll('[data-asin]')).map(e => e.getAttribute('data-asin')).filter(a => a.length > 5)`

## Known ASINs (as of 2026-05-25)
| Book | ASIN | Kindle Price |
|------|------|-------------|
| Tomorrow Remembered | B0GX2XC5YF | $3.99 |
| AI That Works for Small Business | B0H15NLBW8 | $2.99 |
| Built from Dust (NBS 1) | B0GX2YJ92K | $2.99 |
| The Owner's Manual for AI Agents | B0H1KSCRYC | $3.99 |

## Amazon Link Format for Books
- Use ASIN-based: `https://www.amazon.com/dp/[ASIN]`
- Always use the ASIN (not the author page) for direct book links in the dashboard
- In JavaScript: `<a href=\"https://www.amazon.com/dp/${asin}\">Buy on Kindle</a>`

## KDP Package Structure
Each book's publishing package zip contains:
- `[BookKey].epub` — Kindle-compatible EPUB3
- `[BookKey]_Cover.jpg` — Kindle eBook cover (**2560×1600 px**, JPEG, RGB, ≤50MB)
- `[BookKey]_Cover.png` — Source cover PNG (for regeneration/editing)
- `[BookKey]_Wrap_Cover.pdf` — Paperback wrap cover (**PDF**, calculated dimensions, 300 DPI min, CMYK preferred)
- `[BookKey]_Back_Cover.txt` — Back cover text/blurb
- `[BookKey]_Author_Bio.txt` — Author biography
- `[BookKey]_README.md` — Upload instructions

## KDP Cover Specs (Quick Reference)
> Full specs in `book-deliverable-kdp` skill. Summary:
>
> **KDP archive maintenance** — see `references/kdp-packaging-patterns-june2026.md` for the canonical naming convention and deduplication procedure.

| Cover Type | Format | Key Spec |
|---|---|---|
| **Kindle eBook** | JPEG | **2560×1600 px**, RGB, ≤50MB |
| **Paperback wrap** | **PDF** | Calculated: trim×2 + spine + 0.25" bleed, **300 DPI**, spine = pages×0.002252" (white B&W) |
| **Hardcover wrap** | **PDF** | 7-section layout, spine includes 0.189" board, **300 DPI** |

**Manuscript files should NOT include front/back cover** — KDP's Cover Creator handles that. Only the separate cover file is uploaded.

## Pipeline Dashboard Updates
When adding/updating books:
1. Add `asin` field to the book entry in `pipeline-books.json` (under `products.titles` or `products.standalone`)
2. Add `asin` field to the `booksCatalog` array in `pipeline-dashboard.html`
3. The render function generates the Amazon link using `b.asin`
4. Run `bash scripts/dashboard-sync.sh` to deploy

## Weekly Amazon Book Monitor Cron Job
A cron job runs every Monday at 9 AM to search Amazon for new books under "Bob J Mills":
- Job ID: `b111a8678866`
- Script: `~/.hermes/scripts/amazon-book-monitor.py`
- Schedule: `0 9 * * 1` (once a week on Monday)
- Toolsets: terminal, browser, file
- When new ASINs are found, delivers a report via the cron output

To run manually: `python3 ~/.hermes/scripts/amazon-book-monitor.py`
To check status: `hermes cron list`

## Lunar Foundation Series (4 books, not yet on Amazon)
- Book 1: Moon Rock (ASIN TBD)
- Book 2: Mooncoming (ASIN TBD)
- Book 3: Waters End (ASIN TBD)
- Book 4: Waters Horizon (ASIN TBD)

Series page: "Available on Amazon Kindle and Paperback" — search "Bob J Mills" "Lunar Foundation"

## Books NOT on Amazon Yet
- No Blue Sky 2-5 (The Oxygen Gamble, Rivers Under Mars, The Red Charter, The First Martian Nation)
- Lunar Foundation 1-4 (Moon Rock, Mooncoming, Waters End, Waters Horizon)
- These should show "Coming Soon" in the dashboard

## Publisher Task — Smart Skip, Audit & Publish Pipeline

> **This is the authoritative workflow for publishing books. All publisher task runs MUST follow this logic.**

### Overview

When the publisher task runs, it processes each book in the pipeline through a decision tree:

```
For each book in pipeline:
  ├─ Has ASIN (published on KDP)?
  │   └─ YES → SKIP (already published, do nothing)
  ├─ Has manuscript AND cover in book directory?
  │   ├─ NO  → SKIP (incomplete — log warning, move on)
  │   └─ YES → Run editorial pass + package audit
  │       ├─ All required derivables present?
  │       │   ├─ YES → Package is ready for KDP upload
  │       │   └─ NO  → Create missing derivables, then re-audit
  │       └─ Upload to KDP (or prepare KDP package zip)
```

### Step 1: Check KDP Publication Status

A book is considered "published" if it has a non-empty `asin` field in `pipeline-books.json`.

**How to check:**
```bash
# Check if book has ASIN
jq '.products.titles[] | select(.key=="BOOK_KEY") | .asin' pipeline-books.json
jq '.products.standalone[] | select(.key=="BOOK_KEY") | .asin' pipeline-books.json
```

- If ASIN exists and is not empty → **SKIP this book entirely**. Do not rebuild covers, regenerate images, re-audit, or re-upload. Published books are immutable.
- If ASIN is empty or missing → continue to Step 2.

### Step 2: Check Manuscript + Cover Existence

**Required minimum for publishing:**
| File | Location | Notes |
|------|----------|-------|
| Manuscript source | `<book_dir>/manuscript/` or `<book_dir>/manuscript_src/` | HTML chapter files OR a complete manuscript HTML file |
| Cover | `<book_dir>/cover.png` or `<book_dir>/generated_images/cover.png` | LLM-generated, NOT Python |
| Author photo | `<book_dir>/Author_Photo.jpg` | Must exist |

**If either manuscript or cover is missing:**
- Log a warning: `"SKIP: [BookTitle] — missing [manuscript/cover]"`
- Do NOT attempt to generate covers or manuscripts in a publisher task
- Move to next book

### Step 3: Editorial Pass + Package Audit

If manuscript and cover exist, run a full editorial audit:

**3a. Editorial Pass — Check Manuscript Quality:**
1. Verify every chapter file exists and has actual content (>100 words)
2. Check chapter numbering is sequential (no gaps, no duplicates)
3. Verify TOC exists in the manuscript HTML
4. Check all images referenced in manuscript exist on disk
5. Verify no placeholder text remains (`TODO`, `FIXME`, `XXX`, `lorem ipsum`)
6. Check chapter titles match between manuscript content and TOC

**3b. Package Audit — Check All Required Derivables:**

| Derivable | Required? | Location | Check |
|-----------|-----------|----------|-------|
| EPUB | ✅ Yes | `<book_dir>/output/<BookKey>.epub` | Valid EPUB, passes EPUBCheck |
| Print PDF | ✅ Yes | `<book_dir>/output/<BookKey>.pdf` | 6×9" or 5.5×8.5", TOC with page numbers |
| KDP Cover JPEG | ✅ Yes | `<book_dir>/output/<BookKey>_Cover.jpg` | 2560×1600, RGB, JPEG |
| KDP Cover PNG | Optional | `<book_dir>/output/<BookKey>_Cover.png` | 2560×1600, source PNG |
| Metadata (5 files) | ✅ Yes | `<book_dir>/` | Keywords, Description, Back Cover, Author Bio, Title |
| Infographics/images | If applicable | `<book_dir>/generated_images/` | All referenced images exist |
| Author_Photo.jpg | ✅ Yes | `<book_dir>/Author_Photo.jpg` | Present and >10KB |
| About_the_Author.txt | ✅ Yes | `<book_dir>/About_the_Author.txt` | Standalone author bio file |

### Step 4: Create Missing Derivables

If the audit found missing files, generate them in this order:

1. **Infographics/images** (if business book) — use `batch-image-generation.md` pattern
2. **EPUB** — rebuild from manuscript HTML
3. **Print PDF** — rebuild from manuscript HTML (weasyprint)
4. **KDP Cover JPEG** — convert PNG to JPEG, ensure 2560×1600 RGB
5. **Metadata files** — generate from book content (AI-written)
6. **Author_Photo.jpg** — copy from canonical source if missing

After creating missing items, **re-audit** to confirm all are now present.

### Step 5: KDP Package Assembly

If all derivables pass audit, assemble the KDP package zip:

```
KDP_PACKAGE/
├── [BookKey].epub                    # Kindle eBook
├── [BookKey]_Cover.jpg               # Kindle cover (2560×1600 JPEG)
├── [BookKey].pdf                     # Print paperback manuscript (6×9")
├── [BookKey]_Wrap_Cover.pdf          # Paperback wrap cover (with spine)
├── [BookKey]_Back_Cover.txt          # Back cover blurb
├── [BookKey]_Author_Bio.txt          # Author biography
├── [BookKey]_Keywords.txt            # 7 keyword phrases
├── [BookKey]_Description.txt         # Listing description
├── [BookKey]_Title.txt               # Structured title/subtitle/series
├── [BookKey]_README.md               # Upload instructions
└── Author_Photo.jpg                  # Author photo
```

### Logging and Output

For every publisher task run, produce a summary report:

```
Publisher Task Report — [Date]
================================
SKIP (already published): [BookTitle1] (ASIN: B0XXXXX)
SKIP (incomplete): [BookTitle2] — missing manuscript
AUDIT PASS: [BookTitle3] — KDP package ready
AUDIT FIXED: [BookTitle4] — generated 3 missing derivables, now ready
FAIL: [BookTitle5] — [reason, manual intervention required]
================================
Total: X books | Published: X | Ready: X | Fixed: X | Incomplete: X | Fail: X
```

### Publisher Task Cron Configuration

When scheduling as a cron job:
- **Frequency**: Weekly (recommended: Monday 10 AM after the Amazon monitor runs)
- **Toolsets**: `terminal`, `file`, `browser`, `web`
- **Context**: Load `book-publishing` skill, `book-deliverable-kdp` skill
- **Model**: Use a model with strong reasoning for editorial judgment (not a small model)
- **Delivery**: Always report results to origin channel

## Social Media Publishing — Book Launches & Promotion

After a book is published on KDP (ASIN assigned), use the `social-direct-publisher` skill to promote it on social media.

### When to Publish Social Posts
- **Book launch day** — Announce the new book with cover image, Amazon link, and compelling hook
- **Post-launch sequence** — Follow-up posts at 3 days, 7 days, and 14 days after launch
- **Series promotion** — When a new book in a series is published, promote the full series
- **Milestone events** — Reviews, rankings, awards, or reader milestones

### Social Post Content per Platform

**LinkedIn** (professional/author brand):
- Author voice: "I'm excited to announce [Book Title] is now live on Amazon."
- Include: 2-3 sentence hook, key themes, Amazon link, relevant hashtags (#SciFi #AI #Author)
- Max 3000 characters; link goes at end of post

**Facebook Page** (reader community):
- Conversational tone: "The wait is over! [Book Title] is finally here."
- Include: Cover image, Amazon link, short blurb, question to engage readers
- Link preview generates automatically

**Instagram** (visual/book cover):
- Caption: Short, evocative teaser + "Link in bio" for Amazon
- Include: Cover image (1080×1080 or 1080×1350), relevant hashtags in first comment
- Max 2200 characters; links not clickable in captions

### Social Post Approval Flow
1. Generate post content for each platform
2. Run through `social-direct-publisher` policy checker
3. Store as draft (default: `approve_then_publish`)
4. Bob reviews and approves
5. Publish via official APIs (LinkedIn Posts API, Meta Graph API)

### Campaign Tagging
Tag all book promotion social posts with campaign name: `book-launch-[book-key]` (e.g., `book-launch-nbs-1`)
This enables tracking and audit via the social publisher's audit log.

### Integration with Pipeline
When the publisher task assigns an ASIN to a book in `pipeline-books.json`, also:
1. Generate launch social posts for all 3 platforms
2. Store drafts in the social publisher system
3. Report draft URLs in the publisher task summary
4. Bob approves → publish → log to audit trail

## KDP Metadata Generation

When preparing a book for KDP upload, generate these 5 metadata files per book:

1. **`[BookTitle]_Keywords.txt`** — 7 KDP search keyword phrases (50 chars max each)
2. **`[BookTitle]_Description.txt`** — Full KDP listing description (hook + synopsis + comp titles)
3. **`[BookTitle]_Back_Cover.txt`** — Back cover blurb (punchy, 100–200 words)
4. **`[BookTitle]_Author_Bio.txt`** — Author biography tailored to the book/series
5. **`[BookTitle]_Title.txt`** — Structured title, subtitle, series info

### Metadata Writing Guidelines
- **Keywords**: Use genre-specific phrases buyers actually search. Include: genre + theme, comp author style, series position, setting/location. 7 slots × 50 chars.
- **Description**: Open with a 1–2 sentence hook. Follow with 2–3 paragraph synopsis. Close with comp titles ("Fans of Andy Weir, Kim Stanley Robinson..."). Include series info and pricing.
- **Back cover blurb**: Shorter than description. Focus on the core conflict/tension. End with a hook question or comp title.
- **Author bio**: Tailor to the book's genre. Sci-fi → mention engineering background. Business → mention production AI agents. Memoir → mention NASA career.
- **Title file**: Machine-readable. Title, subtitle, series name, series number, author.

### File Placement
Place all metadata files directly in the book's directory (e.g., `/home/bob/books/No_Blue_Sky_Series/Book_I_Built_from_Dust/`). Also copy into the KDP publishing package zip alongside the EPUB and cover.

### Image Generation — MANDATORY: Image Generation LLM Only
- ALL book covers AND chapter illustrations MUST be generated using an image generation LLM (Gemini Flash Image via OpenRouter, or Flux) — **NOT** Python/matplotlib/generate_cover.py
- **Style for sci-fi chapter images**: Black/white/grey pencil sketch, realistic Moon/planets, modern equipment, cross-hatching, dramatic lighting
- **Batch generation for series-wide replacement**: Use delegate_task with 10-chapter batches in parallel. Each batch takes ~5-7 minutes. Use 5s delays between API calls, 3 retries per image.
- **Save to both directories**: Always save to both `output/` and `chapter_images/` simultaneously

**Business book cover style** (reference: "AI That Works for Small Business"):
- Dark navy/black background, white bold sans-serif title stacked in 3-4 lines
- Title width = 80% of cover width, large and authoritative
- Single accent color (amber/gold) sparingly
- "A Business Book" tagline between title and author
- Author name at bottom

**Science fiction cover style** (reference: "Moon Rock", Lunar Foundation Book I):
- Dramatic space imagery — planetary surfaces, starships, starfields
- Deep space blacks/blues with warm amber/gold accents
- Series label at top: "The [Series Name] • Book N"
- Title centered with 4-layer shadow for depth
- Author name at bottom bar
- Top 40% of image must remain dark/empty for title text overlay

**Required exports:**
- Source PNG in book's `generated_images/` directory
- KDP Kindle JPEG at 2560×1600 px (1.6:1 ratio), RGB, ≤50MB

**Author photo:** A copy of `Author_Photo.jpg` must be placed in every book's root directory. Source: `/home/bob/books/Business_Series/AI_That_Works/Author_Photo.jpg`

### Cover Generation — MANDATORY: Image Generation LLM Only
- ALL book covers MUST be generated using an image generation LLM (Gemini Flash Image via Google AI Studio API, or Black Forest Labs Flux via OpenRouter) — **NOT** Python/matplotlib/generate_cover.py
- **Business** style: "AI That Works" — dark navy background (#0a0a1a), white bold sans-serif title stacked 3-4 lines, title width = 80% cover width, amber/gold accent, "A Business Book" tagline between title and author name
- **Science fiction** style: "Moon Rock" (Lunar Foundation) — dramatic space imagery, deep blacks/blues with warm amber habitat-light accents, series label at top, 4-layer shadow
- **KDP export**: 1600×2560 px JPEG (1.6:1 ratio), RGB, ≤50MB
- Reference covers: Business = `/home/bob/books/Business_Series/AI_That_Works/MIFECO_AI_Playbook_Cover.png`, Sci-fi = `/home/bob/books/Lunar_Foundation_Series/Book_1_Moon_Rock/LF_1_Moon_Rock_Cover.png`
- See `book-cover-design` skill for full typography pipeline, prompt templates, and pitfalls
- `book-cover-design/scripts/cover_typography.py` — reusable CLI for typography overlay + KDP JPEG export

### Author Photo Required in Every Book Directory
- Copy `Author_Photo.jpg` from `/home/bob/books/Business_Series/AI_That_Works/Author_Photo.jpg` to the root of every book directory: `<book_dir>/Author_Photo.jpg`
- Apply to ALL book directories (business and fiction) without exception

### PDF Rebuild from Markdown — Weasyprint Pipeline

For the complete PDF rebuild workflow, image handling, and pitfalls, see:
`references/pdf-rebuild-weasyprint.md`, `references/print-pdf-image-sizing.md`, and `references/epub-build-from-scratch.md`.

Key points:
- Fiction: 6x9", Business: 8.5x11"
- **Gutter margins:** <200 pages = 0.5" gutter, 200-299 = 0.5", 300+ = 0.625" (see `references/weasyprint-gutter-margins.md`)
- **Images must be ≤460px wide** (4.79in at 96dpi) to fit 5in content area with 0.5" margins
- **Use `max-width: 480px` in CSS** — `max-width: 100%` doesn't work in WeasyPrint (relative to image intrinsic size)
- **Set `p { margin: 0 }`** — default 0.5in paragraph margin adds to page margins causing overflow
- **Set `.chapter-image { margin: 0; padding: 0 }`** — same issue
- Convert all images to B&W (grayscale) before embedding
- Strip YAML frontmatter before markdown conversion
- Remove all ISBN references from manuscripts
- Insert missing chapter image references when `chapter_images/` has files but manuscript has 0 refs
- Detect chapter header format before inserting images (`## Chapter N`, `# Chapter N`, etc.)

### PDF Gutter Margin Rules (KDP Requirement)

KDP requires minimum gutter (inside margin) based on page count. The gutter is the margin on the binding side. **Recommended: 0.5" all around** for simplicity and safety on all books.

| Page Count | Gutter (inside) | Outside | Top | Bottom |
|---|---|---|---|---|
| < 200 pages | **0.5"** | 0.25" | 0.25" | 0.25" |
| 200–299 pages | 0.5" | 0.25" | 0.25" | 0.25" |
| 300+ pages | 0.625" | 0.25" | 0.25" | 0.25" |

> ⚠️ **KDP rejection:** "Insufficient gutter" — books with 158+ pages require at least 0.5" gutter AND at least 0.25" for outside/top/bottom. Books under 200 pages also need 0.5" gutter (NOT 0.375").

> ⚠️ **WeasyPrint pitfall:** `p { margin: 0.5in }` adds to page margins, causing 1.0" effective offset. Use `p { margin: 0 }` and `.chapter-image { margin: 0; padding: 0; }`. See `references/print-pdf-image-sizing.md` for image sizing and the `max-width: 100%` pitfall.

**Estimated pages formula:** `chapters × 10` for fiction/mystery, `chapters × 8` for business. This drives the gutter selection, NOT the actual rendered page count.

**Implementation:** Use `@page :left` and `@page :right` in CSS to set mirrored margins. The gutter goes on the inside (left for odd pages, right for even pages). The `hermes_publish/step_pdf.py` pipeline handles this automatically via `_get_gutter_css()`.

**⚠️ WeasyPrint Pitfall:** `@page :left` and `@page :right` margin overrides are unreliable in WeasyPrint — the default `@page` margin may be applied to all pages regardless. To guarantee the gutter requirement is met, set the default `@page` margin to use the gutter value on BOTH left and right sides as a safety net. See `references/weasyprint-gutter-margins.md` for details and real-world verification.

**⚠️ WeasyPrint Pitfall — Page Number Duplication:** If `@page` default has `@bottom-right { content: counter(page) }` AND `@page :right` also has `@bottom-right { content: counter(page) }`, even pages will get TWO page numbers — one from the default rule and one from the `:left` rule's `@bottom-left`. Fix: only put `@bottom-right` on `@page :right` (not on default `@page`), and only put `@bottom-left` on `@page :left`. See `references/weasyprint-gutter-margins.md`.

**⚠️ WeasyPrint Pitfall — `target-counter()`:** WeasyPrint does NOT support `target-counter()`. CSS like `.toc-page-num::after { content: target-counter(attr(href), page) }` renders nothing. Use hardcoded page numbers from a 2-pass build instead (see TOC Build section below).

**Verification:** After generating the PDF, verify margins with PyMuPDF:
```python
import fitz
doc = fitz.open('output/book.pdf')
for i, page in enumerate(doc):
    blocks = page.get_text('dict')['blocks']
    for b in blocks:
        if 'lines' in b:
            x0 = b['bbox'][0]
            print(f'Page {i+1}: text x0={x0:.1f}pt ({x0/72:.2f}in)')
            break
```
Odd pages should show x0 ≥ 36pt (0.5") for 200+ page books. Even pages should show right margin ≥ 36pt (verified by checking `page.rect.width - x1` of the rightmost text block).

**Common rejection reason:** "Insufficient gutter" — the inside margin is too narrow for the page count. Fix by increasing gutter in the CSS, NOT by changing page size or compressing content.

### TOC Page Number Build (2-Pass)

The TOC requires accurate page numbers matching actual chapter start pages. Because `target-counter()` doesn't work in WeasyPrint, a 2-pass build is required:

**Pass 1 — Render with estimated page numbers:**
1. Estimate chapter start pages from word counts (~275 words/page, ~6 pages front matter)
2. Build TOC with these estimates as hardcoded text (not `target-counter()`)
3. Render to PDF

**Pass — Extract actual page numbers from rendered PDF:**
Use PyMuPDF (`fitz`) to find each chapter heading:
```python
import fitz
doc = fitz.open('pass1.pdf')
toc_pages = {}
for cn, ct, _ in chapters:
    search_text = f"Chapter {cn}:"
    found_page = None
    for page_idx in range(4, len(doc)):  # Start after front matter
        text = doc[page_idx].get_text()
        if search_text in text:
            lines = text.split('\n')
            for li, line in enumerate(lines):
                if search_text in line:
                    # Check if next non-empty line is body text (not a page number)
                    next_text = ''
                    for nli in range(li + 1, min(li + 3, len(lines))):
                        stripped = lines[nli].strip()
                        if stripped:
                            next_text = stripped
                            break
                    # Body text: long (>15 chars), starts with letter
                    # TOC page number: short, starts with digit
                    if next_text and len(next_text) > 15 and not next_text[0].isdigit():
                        found_page = page_idx + 1  # 1-indexed
                        break
            if found_page:
                break
    if found_page:
        toc_pages[cn] = found_page
```

**Critical:** The next-line check is essential. On TOC pages, the line after a chapter entry is a short page number (starts with digit). On content pages, the next line is body text (long, starts with letter). Simply searching for the heading text without this check will match the TOC reference first, returning the wrong page number (e.g., Chapter 30 → page 5 instead of page 168).

**Do NOT use `range(6, ...)` or higher start indices** — this skips Chapter 1 which starts on page 5-6. Use `range(4, ...)` with the next-line check instead.

**Pass 2 — Rebuild with correct page numbers:**
1. Rebuild HTML with extracted page numbers hardcoded in TOC entries
2. Render final PDF
3. Delete pass 1 file

The `hermes_publish/step_pdf.py` pipeline implements this automatically via `_build_pdf_html()`, `_estimate_toc_pages()`, and `_extract_toc_pages()`.

### Image Handling — Double-Bug Fix & Sizing

> **CRITICAL:** See `references/pdf-image-handling.md` for the full image handling fix.
> **Print image sizing:** See `references/print-pdf-image-sizing.md` for WeasyPrint-specific image/table resizing and the CSS completeness trap.

**Rules:**
1. **Manuscript files MUST NOT contain `![image]` references** — the pipeline inserts images manually. Strip all markdown image syntax from manuscript content before passing to `md_to_html_simple()`.
2. **Strip pattern:** `content = re.sub(r'!\[[^\]]*\]\([^)]+\)\s*\n?', '', content)`
3. **PDF image CSS:** `width: auto; max-width: 100%; height: auto; max-height: 400px;` — never `width: 100%` (overflows margins)
4. **Verify:** After rebuild, check `pdfimages -list` shows exactly 1 image per chapter

### Build Pipeline Invocation — CLI Pitfall

**Do NOT use `python hermes_publish.py`** to run individual build steps — the file at `/mnt/usb_4tb/books/hermes_publish.py` conflicts with the `hermes_publish/` package directory, causing `ModuleNotFoundError: No module named 'hermes_publish.config'`.

**Correct approach** — use `python -c` with direct imports:

```bash
cd /mnt/usb_4tb/books/hermes_publish && python -c "
import sys; sys.path.insert(0, '.')
from config import BOOK_REGISTRY
from step_pdf import run as pdf_run
from step_epub import run as epub_run
book = BOOK_REGISTRY['book-key']
pdf_run('book-key', book)   # builds PDF + HTML
epub_run('book-key', book)  # builds EPUB (separate call)
"
```

**⚠️ `step_pdf.py` only builds PDF + HTML.** EPUB requires a separate call to `step_epub.run()`. Always rebuild both after manuscript changes.

### Manuscript File Location — CRITICAL

**`collect_chapters()` reads from `manuscript/MANUSCRIPT.md` (the `manuscript/` subdirectory), NOT the root-level `*MANUSCRIPT.md`.**

The `collect_chapters()` function in `hermes_publish/utils.py` checks for manuscript files in this order:
1. `book_dir/manuscript/*MANUSCRIPT.md` ← **this is what it reads**
2. `book_dir/*MANUSCRIPT.md` ← fallback only if `manuscript/` doesn't exist

**Pitfall:** Many book directories have BOTH a root-level `*MANUSCRIPT.md` AND a `manuscript/MANUSCRIPT.md`. These are often different files with different content, heading formats, and image references. Editing the root-level file has NO effect on the build output.

**Always verify which file `collect_chapters` reads:**
```python
from utils import collect_chapters
chapters = collect_chapters(book)
# Check chapter content — if your edits don't appear, you're editing the wrong file
```

**Image insertion rule:** When adding chapter images to manuscripts, insert them in the `manuscript/MANUSCRIPT.md` file (the one in the `manuscript/` subdirectory). Images inserted in the root-level file are ignored by the build pipeline.

**Duplicate heading pitfall:** Previous editing sessions may have left duplicate headings (e.g., both `## Chapter N: Title` and `## Chapter N — Title`). Always check for and remove duplicates before inserting images, or images may end up after the wrong heading.

### Chapter Renumbering

When renumbering chapters (e.g., offsetting by a fixed amount), **never use a simple descending/ascending str.replace loop** — it causes cascading replacements where already-renumbered text gets matched again. Use either:

1. **Two-pass with unique placeholders** (safe, simple): first replace all numbers with `__CH{N}__` placeholders, then replace placeholders with final numbers.
2. **Regex with callback** (single pass): `re.sub(r'## Chapter (\d+) —(.*)', lambda m: f"## Chapter {int(m.group(1))-offset} —{2}", content)`

Apply the same renumbering to BOTH chapter headers and TOC entries. Verify after: sequential 1-N, no gaps, no duplicates.

See `references/chapter-renumbering.md` for code examples and the cascading bug explanation.

### Manuscript Source Extraction
If manuscript source files (chapter HTML/MD) are not in the book directory but the EPUB exists, extract them:
```bash
# Extract chapter HTML from EPUB into manuscript_src/
mkdir -p /path/to/book/manuscript_src
cd /tmp/extract && unzip /path/to/book.epub
cp OEBPS/ch*.xhtml /path/to/book/manuscript_src/
```
Skip files with "title", "copyright", "cover", "toc", "nav", "about", "series", "front", "dedic" in the name.

### Content Expansion & Page Count Standards (2026-07-17)

**All books must be 160-275 pages.** Hard rule. Page size NEVER changes (6×9" fiction, 8.5×11" business). Fix page count by rewriting content, not formatting.

**OVER 275:** Tighten prose, cut redundant scenes, combine chapters, reduce scene breaks. Use compact build script as last resort.

**UNDER 160:** Expand using PLOT_MAP.md. Add chapters, deepen scenes, add appendices. Business books: add case studies, exercises, checklists.

**Word targets:** 6×9" fiction: 40k-82k words. 8.5×11" business: 56k-110k words.

**Build scripts:** Standard `/tmp/build_book_pdf.py`. Compact (last resort) `/tmp/build_book_compact.py`.

**Backup check MANDATORY:** Check `MANUSCRIPT.md.expanded`, `MANUSCRIPT_CONDENSED.md`, `_archived/`, `publishing_output/` before redoing work.

**Subagent limit:** delegate_task times out at 1200s. Max 2-3 chapters per subagent.

### Chapter Illustrations by Genre

Every illustrated book should include one illustration per chapter, embedded in the manuscript as an image. The illustration type depends on genre:

| Genre | Illustration Type | Generation Method | Style |
|---|---|---|---|
| **Science Fiction** | Black & white pencil sketch of a scene from the chapter | OpenRouter image generation (Gemini Flash Image or Flux.2) | Detailed pencil sketch, cross-hatching, no color, dramatic composition |
| **Business / Non-Fiction** | Infographic, chart, diagram, or data visualization | **Image generation LLM** (NOT Python) — OpenRouter: `google/gemini-2.5-flash-image` or `black-forest-labs/flux.2-max` | Clean, professional, labeled components, high contrast |
| **Memoir** | Simple diagram, timeline, or map | **Image generation LLM** (NOT Python) | Minimal, clean, emotionally resonant |

> ⚠️ **CRITICAL: All infographics, charts, diagrams, and data visualizations MUST be generated using an image generation LLM model. Do NOT use Python (matplotlib, seaborn, etc.) for any published book infographics. This applies to ALL books, but especially The Crisis Ready Company.**

**Prompt template for business infographics:**
```
Professional infographic for a business book. [Description of data/concept to visualize]. Style: clean modern infographic, labeled components, data visualization, white or light background, professional typography, book-quality.
```

**Prompt template for sci-fi pencil sketches:**
```
Black and white pencil sketch illustration for a science fiction novel. [Scene description]. Style: detailed pencil sketch, cross-hatching, no color, book illustration, dramatic lighting, cinematic composition. This must be completely original.
```

**Image generation API notes:**
- Use `google/gemini-2.5-flash-image` via OpenRouter for best pencil sketch results
- **API response format (updated 2026-06):** The response structure is `choices[0].message.images[0].image_url.url` — a nested dict, NOT a flat string. The `image_url` field is `{"url": "data:image/png;base64,..."}` not just `"data:image/png;base64,..."`. Handle both formats in code.
- Minimum 5-6 second delay between API requests to avoid 429 rate limits
- If Gemini fails, fall back to `black-forest-labs/flux.2-max`
- API key: `OPENROUTER_API_KEY` from `~/.hermes/.env`
- Generate images at 1024×1024 minimum resolution
- For print PDF, embed images at 200+ DPI
- **Batch generation pattern**: `references/batch-image-generation.md`

## Table of Contents (TOC) — MANDATORY REQUIREMENT

> ⚠️ **EVERY book MUST have a Table of Contents. This is non-negotiable.**
> 
> **Authoritative spec:** See `book-deliverable-kdp` skill for the full TOC CSS, 2-pass page-number sync, and WeasyPrint pitfalls. Key rules summarized here.

### TOC Requirements
1. **Every book must have a TOC** — no exceptions
2. **TOC must start on a new page** — use `page-break-before: always` on wrapper div
3. **Section after TOC must start on a new page** — use `page-break-after: always` on TOC div
4. **Synchronized page numbers** — page numbers must match actual manuscript pages (2-pass rendering: render → extract via pdftotext → hardcode → re-render)
5. **One line per entry** — each TOC entry MUST fit on exactly ONE line with NO word wrapping
6. **No `<a>` tags in TOC cells** for print PDFs (causes WeasyPrint text corruption) — plain text only
7. **No `string-set` on h1/h2** (corrupts all TOC text in WeasyPrint)
8. **No `target-counter()`** — does not work in WeasyPrint
9. **Dot leaders** between title and page number for readability
10. **Author bio required** — full "About the Author" section after final chapter (not just name), plus standalone `About_the_Author.txt` in book root

### Title Page Requirements (MANDATORY)
- Title: **bold, white, high contrast**, fills **~80% of page width**
- Author name: **bold, white, high contrast**
- Use dark background bars or text-shadow for readability
- `.title-page` div must have `page-break-after: always`
- See `book-deliverable-kdp` skill for the full title-page CSS template

### Author Bio Requirements (MANDATORY)
- Full "About the Author" section after the final chapter — NOT just the author's name
- Must include: who they are, what they write, which series this book belongs to, personal closing line
- Standalone `About_the_Author.txt` file in the book root directory
- `Author_Photo.jpg` must exist in every book directory

### TOC Format Example
```
Preface..................................................v
Chapter 1: Introduction.................................1
Chapter 2: The Crisis Framework.........................15
Chapter 3: Risk Assessment..............................31
```

**Subagent batch size for chapter writing:**
- Maximum 2-3 chapters per delegate_task (10-chapter batches consistently time out at 600s)
- Each subagent should read at most 2-3 existing chapters for context, not the full manuscript
- Provide chapter outlines directly in the subagent context rather than having them discover structure from existing files
- **⚠️ Tool selection for expansion scripts:** Use `terminal()` directly for Python scripts that call subprocess or run external tools. Do NOT use `execute_code` for such scripts — it is blocked for subprocess calls. Write the script to a temp file via `write_file`, then run it via `terminal(command="python3 /tmp/script.py")`.

### EPUB Build — KDP Compliance Checklist

> **Full checklist:** See `references/kdp-epub-compliance.md` for the authoritative KDP EPUB spec, validation procedure, and common rejection reasons.
> **Build from scratch:** See `references/epub-build-from-scratch.md` for the full manual EPUB build pipeline (OPF, nav.xhtml, chapter XHTML, packaging).

> **Build pitfalls:** See `references/epub-build-pitfalls.md` for structural issues discovered in production (duplicate images, OPF duplicate IDs, incomplete spine, TOC page splitting, image reference paths, nav.xhtml title extraction).

**Critical rules (non-negotiable for KDP upload):**

1. **Bare `&` in text** → must be `&amp;` in XHTML. The only valid XML entities are `&amp;` `&lt;` `&gt;` `&quot;` `&apos;` and numeric refs.
2. **HTML named entities** (`&copy;` `&nbsp;` `&mdash;` `&ndash;`) → use numeric refs (`&#169;` `&#160;` `&#8212;` `&#8211;`)
3. **Self-closing tags** → `<br/>` `<img .../>` `<hr/>` (never `<br>` `<img>` `<hr>`)
4. **nav.xhtml landmarks** → must include `<nav epub:type="landmarks">` with `<a epub:type="bodymatter" href="ch01.xhtml">Start Reading</a>`
5. **toc.ncx** → must exist, be declared in OPF manifest, and spine must have `toc="ncx"`
6. **OPF manifest** → every file in the ZIP must be listed; every manifest entry must resolve

**Quick validation before upload:**
```bash
cd /tmp && mkdir -p epub-check && cd epub-check && unzip -o /path/to/book.epub
# Check bare ampersands
grep -rn '&[^a-zA-Z#]' OEBPS/*.xhtml | grep -v '&amp;' | grep -v '&lt;' | grep -v '&gt;' | grep -v '&quot;' | grep -v '&#'
# Check invalid named entities
grep -rn '&\(copy\|nbsp\|mdash\|ndash\|hellip\|trade\|reg\);' OEBPS/*.xhtml
# Check XML validity
python3 -c "import xml.etree.ElementTree as ET, glob
for f in sorted(glob.glob('OEBPS/*.xhtml')):
    try: ET.parse(f); print(f'OK  {f}')
    except ET.ParseError as e: print(f'BAD {f}: {e}')"
# Check landmarks
grep 'bodymatter' OEBPS/nav.xhtml
# Check NCX
test -f OEBPS/toc.ncx && echo "toc.ncx: OK" || echo "toc.ncx: MISSING"
grep 'toc="ncx"' OEBPS/content.opf
```

### EPUB Build — RGBA Image Pitfall
- EPUB builders (and KDP) require RGB images, NOT RGBA. LLM-generated PNGs are often RGBA.
- Before building EPUB, convert ALL images in `generated_images/` to RGB:
  ```python
  from PIL import Image
  import os, glob
  for path in glob.glob('generated_images/**/*.png', recursive=True):
      img = Image.open(path)
      if img.mode == 'RGBA':
          bg = Image.new('RGB', img.size, (255, 255, 255))
          bg.paste(img, mask=img.split()[3])
          bg.save(path)
  ```
- Also convert the cover PNG to RGB before embedding in EPUB
- If EPUB build fails with "cannot write mode RGBA as JPEG", this is the cause
- Run conversion BEFORE calling the EPUB builder, not after

### TOC Duplicate Injection Pitfall
- When injecting a new TOC into HTML that already has a placeholder TOC, the `inject_toc` regex may fail to match the old TOC (due to whitespace/class differences)
- This results in BOTH the old and new TOC being present in the HTML
- Always verify after injection: `grep -c 'class="toc"' manuscript.html` should be 1
- If duplicate, remove the old TOC block manually before re-injecting
- The old TOC often has empty page cells from the placeholder; the new one should have hardcoded numbers

## EPUB Repair — When Source EPUB Exists but Is Broken

See `nbs-book-rebuild` skill's `references/` directory for detailed repair patterns discovered during the Lunar Foundation fix session:
- `references/epub-repair-patterns.md` — full repair script and patterns
- `references/epub-div-fix.md` — div tag orphan/unclosed fix algorithm
- `references/kdp-epub-compliance.md` — KDP compliance checklist

### Quick EPUB Repair Checklist
1. Extract EPUB to temp dir
2. Fix chapter XML (div orphans, named entities)
3. Add front matter to spine in OPF
4. Rebuild nav.xhtml (clean titles, front matter, landmarks)
5. Rebuild toc.ncx (clean titles, front matter, **with playOrder attributes**)
6. Clean front.xhtml (remove nested XML declarations)
7. Repackage with mimetype first + uncompressed
8. Verify XML validity of all XHTML files

> **NCX playOrder is mandatory for KDP.** See `references/ncx-playorder-requirements.md` for the fix pattern and real-world incident details.