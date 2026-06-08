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
This retrieves previous publishing decisions, book-specific context, and lessons learned from the vector memory store.

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
- Toolset: terminal, browser, file
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

### Cover Generation
All book covers MUST be generated using an image generation LLM (Gemini Flash Image, Black Forest Labs Flux, etc.) — NOT Python/matplotlib/generate_cover.py scripts.

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

### Manuscript Source Extraction
If manuscript source files (chapter HTML/MD) are not in the book directory but the EPUB exists, extract them:
```bash
# Extract chapter HTML from EPUB into manuscript_src/
mkdir -p /path/to/book/manuscript_src
cd /tmp/extract && unzip /path/to/book.epub
cp OEBPS/ch*.xhtml /path/to/book/manuscript_src/
```
Skip files with "title", "copyright", "cover", "toc", "nav", "about", "series", "front", "dedic" in the name.

## Chapter Illustrations by Genre

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

### Subagent batch size for chapter writing:
- Maximum 2-3 chapters per delegate_task (10-chapter batches consistently time out at 600s)
- Each subagent should read at most 2-3 existing chapters for context, not the full manuscript
- Provide chapter outlines directly in the subagent context rather than having them discover structure from existing files

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