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
├── KDP_Packages/                          ← FINAL KDP zips ONLY (one per book)
│   ├── PascalName/                        ← PascalCase book title
│   │   ├── PascalName_KDP_PACKAGE.zip     ← the uploadable zip
│   │   ├── Cover.jpg                      ← front cover
│   │   ├── Back_Cover.txt                 ← back cover blurb
│   │   ├── Author_Bio.txt                 ← author biography
│   │   ├── Description.txt                ← listing description
│   │   ├── Keywords.txt                   ← 7 KDP keywords
│   │   ├── Title.txt                      ← title/subtitle/series
│   │   ├── Infographic.png                ← marketing infographic
│   │   └── Author_Photo.jpg               ← author photo
│   └── ... (one per book, 20 total)
│
├── No_Blue_Sky_Series/                    ← working source for NBS books
│   └── Book_I_Built_from_Dust/
│       ├── manuscript_src/                ← chapter .xhtml files
│       ├── generated_images/               ← cover + chapter illustrations
│       ├── output/                         ← EPUB, PDF builds
│       └── (metadata .txt files)
│
├── Age_of_Lightships_Series/
├── Lunar_Foundation_Series/
├── Business_Series/
├── Cindy_Lou_Legal_Capers/
└── Tomorrow_Remembered/                    ← standalone (no series dir)
```

**RULE:** Never create KDP zips anywhere except `KDP_Packages/PascalName/`. Never use kebab-case for the zip filename. Always PascalCase_Title_KDP_PACKAGE.zip.

## Pipeline Stages

The Books Creation pipeline has 8 stages that map to the MIFECO product pipeline:

| # | Stage | Description |
|---|-------|-------------|
| 1 | Review Market | Review Market for Best series and best selling genres. Select 3 similar books from different authors |
| 2 | Build Book Bible | Extract styles, plots, character descriptions and consolidate them. Do not use character names from existing works |
| 3 | Build Framework | Create list of characters (name from random US top 50 names), create list of chapters, write chapter beats |
| 4 | Write | Write chapter contents for all chapters |
| 5 | Enrich | Add front matter, TOC and page numbering, and back matter, add B&W images where needed |
| 6 | Edit | Run iterative editorial review loop (see `publishing/book-editorial-review` skill): load skill, examine book > compare to bestselling genre benchmarks > create `book-review.md` with A-F rating. If A, pass to Step 7. If below A, incorporate changes into BOOK SOURCE FILES (not just the review), recompile MANUSCRIPT.md, and re-run review. Repeat until A achieved. **WARNING:** Existing book-review.md may be stale — read actual MANUSCRIPT.md to verify what still needs fixing. |
| 7 | Prep for KDP | Create front cover color image, description, back cover materials, author bio, keywords, etc. |
| 8 | Finish | Save book project, update in dashboards, Hermes memory and mifeco.com/books |

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

**Available tools on this system:**
- **EPUB:** Pure Python via `zipfile` + `xml.sax.saxutils` — no external dependencies needed
- **PDF:** `fpdf2` (install via `pip3 install fpdf2`). **WeasyPrint is NOT available** on this system.
- **Fonts:** DejaVuSerif.ttf and DejaVuSerif-Bold.ttf at `/usr/share/fonts/truetype/dejavu/`. No `DejaVuSerif-Italic.ttf` — use DejaVuSerif as italic fallback.

**EPUB — Build from manuscript chapter files:**

```python
import zipfile, io, re
from xml.sax.saxutils import escape as xmlescape
from datetime import datetime, timezone
# Split content on # and ## headings, build content.opf + nav.xhtml + toc.ncx
# Write as ZIP with uncompressed mimetype entry
# See publishing/reader-magnet-production skill for full implementation
```

Convert RGBA images to RGB before building:
```bash
python3 -c "
from PIL import Image; import glob
for p in glob.glob('generated_images/**/*.png', recursive=True):
    img = Image.open(p)
    if img.mode == 'RGBA':
        bg = Image.new('RGB', img.size, (255, 255, 255))
        bg.paste(img, mask=img.split()[3]); bg.save(p)
"
```

**Print PDF (6x9 inch):** Use fpdf2 (NOT WeasyPrint — it is not installed). 6x9" = 152.4x228.6 mm:

```python
from fpdf import FPDF
W, H = 152.4, 228.6
MARGIN = 14  # ~0.55 inches
FS = 11
pdf = FPDF(orientation='P', unit='mm', format=(W, H))
pdf.set_auto_page_break(auto=True, margin=MARGIN)
pdf.add_font("D", "", "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf")
pdf.add_font("D", "B", "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf")
pdf.add_font("D", "I", "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf")  # no italic variant
```

**Page count estimate at 6x9 with 11pt:** ~280-320 words per page of body text. 7,000 words ≈ 22-25 pages. Front/back matter adds ~4-5 pages.

**AUTHOR line encoding bug:** When writing Python build scripts via write_file, the line `AUTHOR=*** J Mills"` frequently corrupts (characters replaced with `***`). After writing, verify: `grep -n "^AUTHOR" build_script.py`. If corrupted, patch carefully.

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
3. Synchronized page numbers (2-pass: render → extract → hardcode → re-render)
4. One line per entry, dot leaders between title and page number
5. No `<a>` tags in TOC for print PDFs
6. No `string-set` on h1/h2 (breaks WeasyPrint)
7. No `target-counter()` (doesn't work in WeasyPrint)

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

## Subagent Batch Rules

- Max 2-3 chapters per `delegate_task` (10-chapter batches timeout at 600s)
- Each subagent reads at most 2-3 existing chapters for context
- Provide chapter outlines directly in context (don't have them discover structure)
- Max concurrency: 3 (`max_concurrent_children=3`)

## Image Generation Rules

- Use `google/gemini-2.5-flash-image` (Gemini API key) or via OpenRouter
- 5-6 second delay between API requests (avoid 429)
- Fallback: `black-forest-labs/flux.2-max`
- Minimum 1024×1024 resolution for covers
- For print PDF: embed images at 200+ DPI

## TOC Duplicate Pitfall

When injecting a new TOC into HTML that already has a placeholder: verify after injection: `grep -c 'class="toc"' manuscript.html` should be 1.
If duplicate, remove old block before re-injecting.
