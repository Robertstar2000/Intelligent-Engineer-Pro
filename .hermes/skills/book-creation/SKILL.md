---
name: book-creation
description: "Unified book creation pipeline — manuscript, cover, metadata, infographic, KDP package. Replaces book-publishing, book-deliverable-kdp, book-cover-design, manuscript-creation, novel-writing, and all publishing/* skills."
version: 1.0.0
author: OWL
category: publishing
metadata:
  hermes:
    tags: [book, publishing, kdp, manuscript, cover, infographic, metadata, novel, writing]
    related_skills: [humanizer, openclaw-ui-ux-design, openclaw-hermes, image-generation-workflow]
---

# Book Creation — Unified Pipeline

> **This skill replaces:** book-publishing, book-deliverable-kdp, book-cover-design, manuscript-creation, novel-writing, manuscript-conversion-pipeline, manuscript-publishing-package, book-inventory-and-delivery, book-marketing-launch, books-website, add-book-to-pipeline, book-identity-rebranding.
> All book creation flows through ONE skill to prevent the fragmentation that caused duplicate KDP zips and missing metadata.

## Storage Convention (MANDATORY)

All books live on the USB mount at `/mnt/usb_4tb/books/` with this EXACT structure:

```
/mnt/usb_4tb/books/
├── Age_of_Lightships_Series/
│   ├── SERIES_PLOT_MAP.md
│   ├── SERIES_CHARACTERS_MAP.md
│   ├── SERIES_DESCRIPTION.md
│   ├── SERIES_INFOGRAPHIC.png
│   └── Book_1_Sunward_Exodus/
│       ├── BOOK_PLOT_MAP.md
│       ├── BOOK_CHARACTERS.md
│       ├── manuscript/
│       │   ├── MANUSCRIPT.md
│       │   └── book-review.md
│       ├── html/                    ← chapter source files (.md/.xhtml)
│       ├── images/                  ← chapter images (ch01.png, ch02.png, ...)
│       ├── images_bw/               ← auto-generated B&W conversions (fiction only)
│       ├── KDP_Package/
│       │   ├── cover.jpg/png
│       │   ├── Book_1_Sunward_Exodus_final.pdf
│       │   ├── Book_1_Sunward_Exodus_final.epub
│       │   ├── Author_Bio.txt
│       │   ├── Back_Cover.txt
│       │   ├── Book_Description.txt
│       │   ├── Keywords.txt
│       │   ├── Title.txt
│       │   └── Author_Photo.jpg
│       └── Promotion/
│           ├── infographic.png
│           ├── sales_text.txt
│           ├── target_audience.txt
│           ├── qr_amazon.png
│           └── qr_mifeco.png
│
├── Lunar_Foundation_Series/       (same structure)
├── No_Blue_Sky_Series/            (Book_1 through Book_5)
├── Cindy_Lou_Legal_Capers/        (Book_1 through Book_3)
├── Business_Series/               (Book_1 through Book_3)
└── Tomorrow_Remembered/           (standalone — series dir = book dir)
```

**Naming rules:** `Book_N_Title_Words` (Arabic numerals, underscores, no spaces). No Roman numerals. No lowercase book dir names.

**⚠️ B&W Image Requirement (MANDATORY):**
- **ALL books** (fiction, memoir, mystery, AND business) use B&W chapter images
- The hermes_publish pipeline handles this automatically via the `images-bw` step
- B&W versions are cached in `images_bw/` subdirectory
- Source images go in `images/` → pipeline converts to `images_bw/` → PDF/EPUB use B&W automatically
- Image specs: PNG preferred, 300 DPI, named `ch{NN}.png` matching chapter numbers

**RULE:** Never create KDP zips anywhere except `KDP_Packages/PascalName/`. Never use kebab-case for the zip filename. Always PascalCase_Title_KDP_PACKAGE.zip.

## Pipeline Stages

The Books Creation pipeline has 8 stages that map to the MIFECO product pipeline:

| # | Stage | Description |
|---|-------|-------------|
| 1 | Review Market | Review Market for Best series and best selling genres. Select 3 similar books from different authors |
| 2 | Build Book Bible | Extract styles, plots, character descriptions and consolidate them. Do not use character names from existing works |
| 3 | Build Framework | Create list of characters (name from random US top 50 names), create list of chapters, write chapter beats |
| 4 | Write | Write chapter contents for all chapters |
| 5 | Enrich | Add front matter, TOC and page numbering, and back matter, add images to `images/` directory (color source; B&W conversion is automatic in stage 6) |
| 6 | Convert Images | Run `images-bw` step via hermes_publish pipeline — converts all chapter images to grayscale for fiction/memoir/mystery. Business books skip automatically. |
| 7 | Edit | Run iterative editorial review loop (see `publishing/book-editorial-review` skill): load skill, examine book > compare to bestselling genre benchmarks > create `book-review.md` with A-F rating. If A, pass to Step 8. If below A, incorporate changes into BOOK SOURCE FILES (not just the review), recompile MANUSCRIPT.md, and re-run review. Repeat until A achieved. **WARNING:** Existing book-review.md may be stale — read actual MANUSCRIPT.md to verify what still needs fixing. |
| 8 | Build PDF/EPUB | Run `pdf` and `epub` steps via hermes_publish pipeline. B&W images from `images_bw/` are used automatically for fiction/memoir. |
| 9 | Prep for KDP | Create front cover color image, description, back cover materials, author bio, keywords, etc. |
| 10 | Finish | Save book project, update in dashboards, Hermes memory and mifeco.com/books |

**Email Inbox:** bigtruck444@agentmail.to
**Nurture:** 4-email sequence over 14 days

### Stage 0: Discover Existing Books

Before creating anything, always scan existing books:
```bash
# List all book directories
find /mnt/usb_4tb/books -maxdepth 3 -type d | grep -v KDP_Packages | grep -v _archived | sort

# Check which books already have KDP packages
ls /mnt/usb_4tb/books/KDP_Packages/

# Check pipeline state
cat ~/.hermes/pipeline-engine/dashboard/pipeline-books.json | python3 -c "import sys,json; d=json.load(sys.stdin); [print(t['title'],t.get('asin','—')) for t in d['pipeline']['products'].get('titles',[])+d['pipeline']['products'].get('standalone',[])]"
```

### Stage 1: Create Manuscript

Use `delegate_task` with subagents for parallel chapter writing (max 2-3 chapters per subagent to avoid timeout).

**Chapter format:** Markdown files named `ch01.md`, `ch02.md`, etc. in `book_dir/manuscript_src/`.

**Front matter per chapter:**
```markdown
# Chapter N: [Title]

[Content — 2000-4000 words, humanized prose, Humanizer skill on all output]
```

**TOC:** Every book MUST have a Table of Contents. Generate after all chapters complete.

#### Extending an Existing Manuscript with New Chapters

When the task is to write new chapters for an already-existing manuscript (e.g., a new final chapter, a new appendix, a missing chapter), the priority is **matching the established voice, not creating one**. Do this before writing anything. The more thorough you are in the analysis phase, the less the user will need to correct you.

**Phase 1: Voice & Structure Analysis (read 3+ points in the manuscript)**

1. **Read the END of the manuscript** — The last 100-200 lines show the author's most recent voice, chapter-closing conventions, and any recent stylistic decisions. For books in active development, the latest chapters are the most reliable style reference.

2. **Read an EARLY chapter opening** — The first full chapter (after front matter) establishes the narrative pattern that runs through the entire book. Extract: does each chapter open with a story? A quote? A statistic? Does it follow story → analysis → framework → case study → exercise structure? Note the exact conventions and sequence of sections.

3. **Read a MIDDLE chapter** — Check if the pattern holds across the entire book. Sometimes the first chapter is more elaborate and later chapters are tighter. Document both the ideal pattern (from early chapters) and the "real" pattern (what actually appears in chapters 10–15).

4. **Cross-reference the Table of Contents** — Check that the new chapter follows the naming convention (e.g., `# Chapter N — Title` vs `## Chapter N: Title`), fits in the correct Part, and doesn't conflict with existing appendices. Also check: are there existing appendices? If not, the first appendix establishes the format.

5. **Check for recurring signature elements** — Document every structural pattern you find:
   - Does every chapter end with "The One Thing"? (Exact phrasing and formatting)
   - Does it include a "Reader Exercise" or "Reader Reflection Questions"?
   - Are there case studies with specific dollar amounts and company names?
   - Are checkboxes `- [ ]` used for implementation checklists?
   - Are there tables (and if so, what format — pipe tables or HTML)?
   - What's the chapter-opening convention? (Bold tagline in italics? A story hook? A quote?)
   - Is there an "Implementation Checklist" before or after the reflection questions?

**Phase 2: Framework & Domain Extraction**

For NEW sections (final chapters, appendices) that need to reference existing content:

6. **Extract the book's core framework** — Search the manuscript for the framework name (e.g., READY, SPADE, etc.). Document each pillar/step and what it means. Ensure any new chapter references all pillars and uses the same terminology. For business books, also check the `book-review.md` for the editorial review's framework map description.

7. **Extract key terms for glossary/new appendices** — If writing a glossary or reference appendix, search the manuscript for all terms that should be included. Don't guess — actually grep/search the manuscript for terms like "force majeure", "single point of failure", etc. to confirm they appear in the book before adding them to a glossary. Cross-reference with the ToC chapter list to ensure coverage.

8. **Note the author's persona and data conventions** — Does the author use first-person "I" stories? Are there specific numbers with dollar signs (e.g., "$47,000")? Does the author refer to MIFECO as a case study? Are client stories anonymized? Match these conventions exactly.

**Phase 3: Writing & Verification**

9. **Write to the existing voice** — Match sentence rhythm, level of conversational directness, and the pattern of personal story → business lesson. If the book is first-person with specific dollar amounts, don't write third-person with hypotheticals. Use the same paragraph length, same use of bold or italics for emphasis, same frequency of data citations.

10. **Use consistent formatting for new elements** — For appendices with unique formatting (glossaries, reference tables, checklists), match the manuscript's existing conventions. If the book uses `**Term** — Definition.` for bold-term style, use that. If it uses `- **Term**: Definition`, use that. Look for any existing appendix or the closest structural element in the book as a template.

11. **Write section-by-section, not all at once** — After you understand the voice, write the new content in logical sections. For a glossary, write term by term (alphabetical). For a final chapter, write story → phases → scorecard → decision tree → checklists → close, following the book's established section pattern.

12. **Verify word count separately from formatting** — When the target is specific (e.g., "~4,000-4,500 words" or "~10 pages"), use `wc -w` but also strip markdown formatting to get the prose-only count. Tables, checkboxes, and list markers inflate raw word counts. Run: `cat file.md | sed 's/^- \[ \] //g; s/|//g; s/\[//g; s/\]//g' | wc -w` for a cleaner count.

13. **Do NOT modify the original MANUSCRIPT.md** — Write new content to a separate file (e.g., `/tmp/new_chapter.md`) for review. The user integrates it. Never make assumptions about integration points — write standalone files.

### Stage 2: Generate Cover

ALL covers MUST use an image generation LLM — NOT Python/matplotlib.

**API:** `google/gemini-2.5-flash-image` via Google AI Studio (key in `~/.hermes/.env` as `GOOGLE_AI_STUDIO_KEY`) or via OpenRouter.

**Sci-fi style** (reference: Moon Rock, Lunar Foundation):
- Dramatic space imagery, deep blacks/blues, warm amber/gold accents
- Series label at top: "Series Name • Book N"
- Title centered with 4-layer shadow for depth
- Top 40% remains dark for title overlay
- Export: 1600×2560 px JPEG, RGB, ≤50MB

**Business style** (reference: AI That Works for Small Business):
- Dark navy/black background (#0a0a1a), white bold sans-serif title
- Title width = 80% cover width, stacked 3-4 lines
- Amber/gold accent, "A Business Book" tagline

**KDP export:** 1600×2560 px JPEG (1.6:1), RGB, ≤50MB. Save as `generated_images/Cover.jpg`.

### Stage 3: Generate Back Cover, Author Bio, Description, Keywords, Title

Create these 5 metadata files (per book) using AI:

| File | Content |
|------|---------|
| `Back_Cover.txt` | Punchy 100-200 word blurb, core conflict/tension, hook question |
| `Author_Bio.txt` | Genre-tailored author bio (sci-fi → engineering background, business → AI agents) |
| `Description.txt` | Hook + synopsis + comp titles ("Fans of Andy Weir...") + series info |
| `Keywords.txt` | 7 keyword phrases, 50 chars max each, genre-specific search terms |
| `Title.txt` | Title, subtitle, series name, series number, author |

Also create:
- `Infographic.png` — Use image generation LLM (NOT Python). For business books: charts/diagrams. For sci-fi: timeline/map.
- `About_the_Author.txt` — Standalone author bio for EPUB front matter
- `Author_Photo.jpg` — Copy from `/home/bob/books/Business_Series/AI_That_Works/Author_Photo.jpg`

> ⚠️ CRITICAL: All infographics/charts/diagrams MUST be generated using image generation LLM. Do NOT use Python (matplotlib, seaborn) for any published book infographic.

### Stage 4: Build EPUB + Print PDF

**The hermes_publish pipeline handles all builds.** Run via:
```bash
cd /mnt/usb_4tb/books && python3 hermes_publish.py --book <key> --steps images-bw pdf epub
```

**Available tools on this system:**
- **EPUB:** Pure Python via `zipfile` — no external dependencies
- **PDF:** `weasyPrint` (installed). Falls back to HTML-only if WeasyPrint unavailable.
- **B&W conversion:** PIL/Pillow via `hermes_publish.utils.convert_image_to_bw()`
- **Fonts:** DejaVuSerif at `/usr/share/fonts/truetype/dejavu/`

**Page sizes:**
- ALL books (fiction, memoir, business): 6×9" (152.4×228.6 mm)
- **NEVER** use 8.5×11 for business books — KDP rejects non-standard trim sizes

**Page count estimate at 6x9 with 11pt:** ~280-320 words per page. Front/back matter adds ~4-5 pages.

### Stage 5: Assemble KDP Package

Create `KDP_Packages/PascalName/PascalName_KDP_PACKAGE.zip` containing:

```
PascalName_KDP_PACKAGE.zip
├── PascalName.epub              # Kindle eBook
├── Cover.jpg                   # 2560×1600 JPEG
├── PascalName.pdf               # Print paperback (6×9")
├── Wrap_Cover.pdf              # Paperback wrap (with spine calc)
├── Back_Cover.txt              # Back cover blurb
├── Author_Bio.txt              # Author biography
├── Keywords.txt                # 7 KDP keyword phrases
├── Description.txt             # Listing description
├── Title.txt                   # Title/subtitle/series
├── README.md                   # Upload instructions
└── Author_Photo.jpg            # Author photo
```

Also copy all files unpacked into `KDP_Packages/PascalName/` for easy inspection.

### Stage 6: Update Pipeline State

Update these files (not the zip — the zip is immutable once created):
1. `~/.hermes/pipeline-engine/dashboard/pipeline-books.json` — add/update book entry
2. Sync dashboard: `bash ~/.hermes/scripts/dashboard-sync.sh` (or use paramiko/SFTP directly)

### Stage 7: Report

```
Book Creation Report — [Date]
================================
✅ [BookTitle] — KDP package ready (or: created, missing: [list])
❌ [BookTitle] — [reason]
Total: X complete | X incomplete | X blocked
================================
```

## KDP Cover Specs (Quick Reference)

| Cover Type | Format | Spec |
|---|---|---|
| Kindle eBook | JPEG | 1600×2560 px, RGB, ≤50MB |
| Paperback wrap | PDF | Trim×2 + spine + 0.25" bleed, 300 DPI |
| Hardcover wrap | PDF | 7-section, 300 DPI |

## Known ASINs (update when new books publish)

| Book | ASIN | Price |
|------|------|-------|
| Tomorrow Remembered | B0GX2XC5YF | $3.99 |
| AI That Works for Small Business | B0H15NLBW8 | $2.99 |
| Built from Dust | B0GX2YJ92K | $2.99 |
| Owner's Manual for AI Agents | B0H1KSCRYC | $3.99 |

## TOC Requirements (MANDATORY)

1. Every book MUST have a TOC
2. Starts on new page, next section on new page
3. Synchronized page numbers via CSS `target-counter()` on `<a>` tags — WeasyPrint resolves these automatically
4. Dot leaders: use `border-bottom: 1px dotted #000` on a title span (NOT `leader(dotted)` CSS — unsupported in WeasyPrint)
5. PDF TOC: page numbers ARE shown (via `target-counter` on `<a>` elements)
6. EPUB TOC: NO page numbers (NCX format doesn't support them)
7. No `<a>` tags with `href` in TOC for print PDFs — use `<span>` with `id` for cross-references
8. No `string-set` on h1/h2 (breaks WeasyPrint)
9. **EPUB NCX playOrder**: Every `<navPoint>` in the NCX file MUST have a `playOrder` attribute (sequential integers starting from 0). Without this, Kindle cannot display the TOC. See `references/epub-ncx-toc-fix.md` for the fix script and details.

## The 11 Editorial Review Rules (WRITE TO THESE FROM DAY ONE)

Every manuscript must be built with these 11 checks as design requirements, not afterthoughts. These are the editorial review criteria that determine the book's rating (A-F). Writing to them from the start prevents fix loops.

### Structural Checks (1-6) — Front/Back Matter & Layout

**1. Chapter Images Placement**
- Every chapter needs `![](chapter_images/chNN.png)` AFTER the chapter header and BEFORE the chapter content — NOT before the header, not after the content
- Verify the image file exists in `chapter_images/` directory
- NO covers should be embedded in MANUSCRIPT.md (covers go in the EPUB/PDF build pipeline)

**2. Copyright and Acknowledgments Page**
- Must include: Copyright © [year] Bob J Mills, book title/series, all rights reserved, ISBN placeholder, fiction disclaimer, edition info
- Acknowledgments section thanking contributors
- Must appear as front matter BEFORE Chapter 1

**3. Table of Contents (TOC)**
- All chapter titles listed and synced with actual headers
- No numbering gaps, no wrong titles, no missing chapters
- Front matter (copyright, dedication) included if present
- Handle worded numbers (`Chapter One`) and non-sequential numbering correctly
- Page number references are for print layout, not markdown

**4. Back Matter — Complete Book List**
- Every book MUST end with "Also by Bob J Mills" listing ALL 6 series in reading order
- Include reader magnet novella mention: "Get the free prequel novella at mifeco.com/books"
- Include author website: mifeco.com
- Cross-promote all series even if the current book is in only one

**5. No Cover Images in MANUSCRIPT.md**
- Cover images MUST NOT appear in the manuscript markdown
- Covers go in the EPUB/PDF build pipeline only
- Verify: `grep "cover" MANUSCRIPT.md` should return NO matches for cover-type images

**6. Page Count Target (160-190 Pages)**
- Every full-length book must generate a 6×9" PDF between 160 and 190 pages
- Word count target: ~50K-70K words depending on formatting density (use ~275 words/page estimate)
- Below 160 pages → P0: Must expand. Above 190 pages → P1: Must trim or tighten formatting

### Series-Level & Readability Checks (7-11) — Writing Quality

**7. Consistent Character Identity (Names & Personas)**
- Character names must be stable across every chapter — no name-switching (Tom/Thomas/Tommy)
- Cross-book consistency: same character in Book 1 and Book 4 must have the same name, personality baseline, relationships
- Character personas must be coherent — brave in Ch 3 not cowardly in Ch 12 without arc explanation
- Name inconsistency across a series = -1 full letter grade. Persona drift = -0.5

**8. Series Flow (Transition Between Books)**
- Each book should feel like the next chapter of a saga, not a reboot
- Previous events acknowledged with consequences that carry forward (not summarized)
- Ending hook pulls toward next book: mystery unsolved, a choice that will ripple, a new threat glimpsed
- Tone continuity: Book 1's genre/mood should evolve organically in Book 2, not abruptly shift
- Tone break = -1 letter grade. Missing/excessive recap = -0.5. Continuity error = -1

**9. Engagement & Bestseller Readability**
- Every chapter must end with a reason to keep reading (cliffhanger, revelation, emotional punch, new question)
- Pacing: story should not drag in the middle; tension curve has proper peaks and valleys
- Emotional resonance: reader must CARE about the outcome
- Sentence-level rhythm: read 3 paragraphs aloud — do they flow or feel mechanical?
- Technically correct but boring = capped at B. Pacing problems = -0.5. Page-turner quality = +0.5

**10. Plot Coherence (Follow-Through)**
- Every setup must have a payoff — no loose threads
- Cause and effect visible: characters' decisions ripple through later chapters
- No deus ex machina: problems solved by character actions, not coincidence or sudden new abilities
- Subplots must have clear resolution (even if resolution is "character accepts the mystery")
- Dropped plot thread = -1 per thread. Deus ex machina climax = -1.5

**11. Genre-Appropriate Formatting**
- Chapter header format consistent: same style, punctuation, spacing for EVERY chapter
- Scene break convention uniform: all `---` or all `***`, never mixed
- Paragraph style fits genre: business uses headers + boxes, fiction uses prose only (no bullet lists), memoir avoids script-style
- Dialogue formatting: consistent quotation marks, proper punctuation, new speaker = new paragraph
- White space adequate: fiction chapters should not look like dense legal documents
- Inconsistent format = -0.5. Genre-mismatched = -1 (e.g., bullet lists in novel prose)

## HTML to DOCX Conversion (KDP Review)

When KDP rejects an EPUB and you need a DOCX for manual review, convert the print HTML manuscript to DOCX using python-docx + lxml. **Do not use LibreOffice or pandoc** — neither works for EPUB→DOCX on this system.

**Reference:** See `references/html-to-docx-conversion.md` for the full conversion technique, image path resolution strategies, and verification steps.

Quick usage (pre-built script at `/tmp/html_to_docx_v3.py`):
```bash
python3 /tmp/html_to_docx_v3.py
```
Output: `/mnt/usb_4tb/books/converted_docx/`

## Image Update (Replacing Chapter Images in Published EPUBs/PDFs)

When chapter_images have been regenerated and existing EPUB/PDF files need updating:

1. **Compare dates**: Check `os.path.getmtime()` of latest image vs EPUB/PDF
2. **Update EPUBs**: Use `zipfile` to replace `OEBPS/images/chXX.png` — write to `.tmp` then move
3. **Update PDFs**: Use PyMuPDF `page.replace_image(xref, stream=data)` — save to `_updated.pdf`
4. **Skip**: `_fixed.epub` (no images), `KDP_PACKAGE/Kindle` (legacy), non-overlapping chapter ranges

See `nbs-book-rebuild` skill's `references/image-update-workflow.md` for complete code.

## Subagent Batch Rules

- Max 2-3 chapters per `delegate_task` (10-chapter batches timeout at 600s)
- Each subagent reads at most 2-3 existing chapters for context
- Provide chapter outlines directly in context (don't have them discover structure)
- Max concurrency: 3 (`max_concurrent_children=3`)

## Image Generation Rules

### Cover Images (Color — Always)
- Use `google/gemini-2.5-flash-image` (Gemini API key) or via OpenRouter
- 5-6 second delay between API requests (avoid 429)
- Fallback: `black-forest-labs/flux.2-max`
- Minimum 1024×1024 resolution for covers
- Covers are always in COLOR — saved to `KDP_Package/cover.jpg`

### Chapter Images (B&W for Fiction/Memoir/Mystery)
- Source images placed in `images/` directory as `ch01.png`, `ch02.png`, etc.
- The hermes_publish `images-bw` step auto-converts to grayscale → `images_bw/`
- B&W images are embedded in PDF and EPUB during build
- Business books (charts, infographics) skip B&W conversion — kept in color
- For print PDF: embed images at 300 DPI, max height 4" (fiction) or 5" (business)
- Image format: PNG preferred; JPEG accepted
- **Reference:** See `references/bw-image-pipeline.md` for function signatures and integration details
- **Markdown-to-HTML pipeline:** See `references/md-to-html-pipeline.md` for `md_to_html_simple()` capabilities, table/list support, TOC pipeline, and common pitfalls

## Business Book Manuscript Formatting (MANDATORY)

Business books have dense structured content that `md_to_html_simple()` must render correctly. The pipeline's markdown-to-HTML converter supports tables, lists, and inline HTML — use them.

### Tables
Use markdown pipe tables for timelines, matrices, comparisons, and any grid layout:
```markdown
| Quarter | Focus Area 1 | Focus Area 2 |
|---------|-------------|-------------|
| Q1 | [Quick Win] ____________ | [Foundation] ____________ |
```
- Header row + separator row required
- `md_to_html_simple()` converts to `<table style="width:100%;border-collapse:collapse;">` with bordered cells
- Do NOT put all items on one line with brackets/underscores — that renders as a broken paragraph

### Lists
Use `- item` for bullets, `1. item` for numbered lists:
```markdown
### Do:
- Start with Why: Always begin with business objectives
- Involve Your Team: Get input from affected people
```
- `md_to_html_simple()` converts to `<ul><li>` and `<ol><li>` with proper margins
- Do NOT write list items as plain text paragraphs — they won't have bullets

### Fill-in-the-Blank Form Fields
Use `<br/>` between label and underline to prevent line-wrapping:
```markdown
**Biggest Financial Frustration:**<br/>_____________________________________________
```
- Short fields can be inline: `Bookkeeping: _____ hours`
- Long fields MUST be on separate lines with `<br/>`
- Do NOT put long labels + long blanks on the same line — WeasyPrint wraps mid-line

### Problem/Solution and Bottleneck/Solution Patterns
Put labels on separate bold lines:
```markdown
**Problem:** Text here.
**Solution:** Text here.
```
- Do NOT put "Problem: ... Solution: ..." on a single line — it wraps awkwardly

### Checkbox Lists
Always use `- [ ]` format:
```markdown
- [ ] Problem/solution fit verified
- [ ] Free trial completed
```
- Do NOT use `[ ]` without the `-` prefix — won't be recognized as list items

### Chapter Title Deduplication
The PDF/EPUB templates already generate `<h3>Chapter N: Title</h3>` headings. Strip the first `# Chapter N: Title` line from each chapter's content in the manuscript to avoid duplicate headings. The pipeline does this automatically via `content = re.sub(r'^#{1,2}\s+Chapter\s+\d+\s*[:—\-–]?\s*.*?\n', '', content, count=1)`.
