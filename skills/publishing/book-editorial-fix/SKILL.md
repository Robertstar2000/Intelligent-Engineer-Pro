---
name: book-editorial-fix
displayName: Book Editorial Fix Workflow
description: Process for applying editorial fixes from book-review.md files to existing manuscripts. Reading review → locating chapter sources → applying targeted rewrites → verifying changes → recompiling manuscript → rebuilding EPUB/PDF.
category: publishing
tags: [editorial, fix, rewrite, manuscript, chapter, revision, subagent]
related_skills: [book-editorial-review, book-publishing, manuscript-restoration, reader-magnet-production]
triggers: [apply review, fix per review, update book, rewrite chapters, implement editorial, apply book-review.md recommendations, second pass fixes, front matter, back matter, copyright page, table of contents, also by, acknowledgments, template differentiation, genre shift, bulk sed replace, Moon to Mars, template chapters, crisis injection]
---

# Book Editorial Fix Workflow

## When to Use

- You have a `book-review.md` file in a book directory with specific rewrite instructions
- You need to apply editorial fixes to existing manuscripts (cut, expand, rewrite chapters)
- You need to rebuild EPUB and PDF after applying fixes
- A user says "update each book IAW the instructions in the book-review.md file"

## Overview

The fix workflow has 5 phases:
1. **Read:** Understand the review's instructions and the current manuscript state
2. **Apply:** Rewrite/edit chapter files based on review recommendations
3. **Verify:** Confirm changes were applied as instructed
4. **Compile:** Rebuild MANUSCRIPT.md from updated chapter files
5. **Build:** Generate EPUB and PDF

## Phase 1: Read

### What to Read First
1. `book-review.md` — the editorial recommendations (A-F rating, specific chapter rewrites, highest-impact change)
2. `MANUSCRIPT.md` — the compiled manuscript (identify chapter structure, word count, current state)
3. Open a chapter from the start, middle, and end to assess writing quality

### Locate Chapter Source Files
Find where chapter files live. Common locations (check ALL):
- `chapters/` — individual .md chapter files
- `manuscript_src/` — individual .xhtml or .md chapter files
- `manuscript/` — sometimes used instead
- The book root directory sometimes has flat .md files

```bash
# Find all possible chapter sources
ls path/to/book/chapters/ | head -5
ls path/to/book/manuscript_src/ | head -5
find path/to/book -name "ch*.md" -o -name "ch*.xhtml" | sort | head -10
```

### Note: Parallel Storage Issue

Books may have new `.md` chapters in `chapters/` AND old `.xhtml` chapters in `manuscript_src/` for the SAME chapter numbers. The compiled MANUSCRIPT.md may use either. Determine which version is authoritative by:
- Checking file modification dates
- Checking if the review was already partially applied (look for review fix patterns in the text)

## Phase 2: Apply Fixes

### Writing Updated Chapters

For bulk content work across a full manuscript, **write_file() is more reliable than patch().** The patch tool fails when its fuzzy matching can't find the old_string — this happens frequently with long, complex manuscripts. write_file() always succeeds.

When to use each:

| Tool | Best For | Avoid When |
|------|----------|------------|
| write_file() | Whole-file content, new chapters, major expansions | Replacing tiny sections in an otherwise-good file |
| patch() | Targeted fixes, name changes, AI artifact removal | Files with heavy repetition (patch may match wrong instance) |
| terminal (sed) | Bulk find-and-replace across multiple files | Any change where you need to verify context before replacing |

**Write new `.md` files to `manuscript_src/`** (not `chapters/`) so the next compile picks them up automatically. If writing to `chapters/`, note that you'll need to move them afterward.

**Chapter naming convention:** `ch001.md`, `ch002.md`, etc. (zero-padded 3-digit numbers for proper sort order).

### Name Consistency Fixes (Critical Pattern)

When fixing character names across a book:

1. **Search ALL files** — not just the main manuscript:
```bash
grep -rn "OldName" path/to/book/chapters/*.md 2>/dev/null
grep -rn "OldName" path/to/book/manuscript_src/*.* 2>/dev/null
grep -rn "OldName" path/to/book/*MANUSCRIPT*.md 2>/dev/null
grep -rn "OldName" path/to/book/output/* 2>/dev/null
```

2. **Replace in EVERY file** — chapters, MANUSCRIPT.md, _MANUSCRIPT.md, HTML output, KDP package files. Forgetting one file means the old name survives.

3. **Use `patch` tool for efficiency** — find all files with the wrong name, then apply `patch` to each with the same old_string/new_string pair. For bulk replacements across many files, use terminal with `sed`.

4. **Verify zero instances remain**:
```bash
grep -rn "OldName" path/to/book/ | grep -v "book-review.md" | wc -l
# Should return 0
```

### Third-Person to First-Person Conversion (Memoir Pattern)

When converting a memoir from third person ("Bob remembered...") to first person ("I remembered..."):

The critical replacement patterns:
- "Bob" → "I" (when Bob is the subject)
- "Bob's" → "my"
- "he" → "I" (when referring to the author)
- "him" → "me"
- "his" → "my"
- "the author" → "I" or "me"

**But be careful:** Not every "he" in the manuscript refers to the author. Some refer to the author's father, brother, or other male figure. Blind search-and-replace will destroy those references.

**Safe approach:**
1. Read the chapter first to understand who "he" refers to in each context
2. Apply specific, context-aware replacements
3. Write the chapter fresh rather than attempting bulk regex replacement
4. After writing, read through for lingering third-person holdovers

### Removing AI Filler Paragraphs

Common AI artifacts to find and remove:
- "The work required patience and precision" (or any variant)
- "The [noun] was a [adjective] thing of [abstraction]" 
- "He/She stared at the [noun], thinking about what it meant"
- "The silence of the habitat was broken only by..."
- "Nothing about [situation] was ever simple"
- Visible generation instructions: "Word count: ~1050" or "(Self-Correction: I will expand...)"

Search:
```bash
grep -rn "patience and precision\|patience, precision\|the silence of\|Self-Correction\|Word count:" path/to/book/manuscript_src/
```

Remove by rewriting affected paragraphs to be specific and concrete.

## Phase 3: Verify

### Critical: Don't Trust Subagent Reports

Subagents frequently CLAIM fixes were applied but the actual files tell a different story. Always verify by reading the compiled MANUSCRIPT.md:

```bash
# Check if a template phrase still exists
grep "CO2\|viewport\|the work continued\|status board\|as ready as" path/to/book/MANUSCRIPT.md | head -5

# Check if name fix took effect
grep "OldName" path/to/book/MANUSCRIPT.md

# Check if chapters exist at all
ls path/to/book/manuscript_src/*.md | wc -l

# Compare to what the review asked for
```

### Common Verification Failures

| Claimed Fix | How to Verify | Failure Pattern |
|-------------|---------------|-----------------|
| "6 chapters rewritten" | Count .md files in manuscript_src/ | Only 1-2 files exist; rest are old .xhtml |
| "Name fixed across all files" | grep -r for old name | Old name still in MANUSCRIPT.md or output files |
| "Template content removed" | grep for unique template phrases | Old phrasing remains in compiled output |
| "Book rewritten for Mars" | grep for "Moon" or "lunar" references | Old Moon-base content still in manuscript |
| "All 39 chapters unique" | Check chapter 1, 20, 39 for identical structure | Same scene template repeated |

## Phase 4: Recompile MANUSCRIPT.md

After all chapter fixes are applied, rebuild the compiled manuscript:

```bash
# For .md files only (sorted numerically)
cat manuscript_src/ch*.md > MANUSCRIPT.md

# Or using a Python script for mixed .md/.xhtml sources
```

The compiled MANUSCRIPT.md should:
- Include title page, copyright, TOC (if available as separate files)
- Include all chapters in order
- Have NO duplicate chapters
- Have NO old template content

## Phase 5: Build EPUB and PDF

After applying fixes, regenerate EPUB and PDF using the script in this skill:

```bash
python3 /home/bob/.hermes/skills/publishing/book-editorial-fix/scripts/generate-ebook.py /path/to/book/dir
```

This handles:
- Multi-format chapter headers (## Chapter N:, # Chapter N —, worded numbers)
- CLLC _MANUSCRIPT.md vs MANUSCRIPT.md file selection
- EPUB via ebooklib with proper CSS
- PDF via WeasyPrint at 6x9" with configurable formatting

**Page count check after build:** Verify the generated PDF is 160-190 pages:
```bash
python3 -c "from PyPDF2 import PdfReader; r=PdfReader('book.pdf'); print(f'{len(r.pages)} pages')"
```

If outside 160-190 range, adjust formatting (10pt/0.7in margins for fewer pages, 11pt/1in for more) or expand/trim content. See `book-editorial-review` → `references/page-count-target.md`.

For reader magnet novellas (shorter works), use the fpdf2-based generation in `reader-magnet-production` skill instead.

## Parallel Work Strategy

When fixing multiple books simultaneously:

1. Group by fix type (name fixes, complete rewrites, partial edits)
2. Delegate each group to a separate subagent
3. Each subagent gets the FULL context from the book-review.md
4. Set subagent toolsets to `["terminal", "file"]`
5. Limit each subagent to 1-2 books to avoid 600s timeout

**Timeout-safe pattern:** For complete rewrites (Books 4-5 style), delegate ONE BOOK per subagent, not a series. Each book takes ~4-6 chapter rewrites at ~1500 words each, which fits in a 300-400s subagent window.

### Fix Only — Don't Delegate Review Writing

The most reliable pattern is: **delegate ONLY the fix work to subagents, write the review yourself after verifying.**

Include this instruction in every subagent goal:
```
DO NOT write the review — I'll handle that. Just make the actual edits to the manuscript file.
```

**Why:**
- Subagents consistently over-report results. One subagent claimed 63K words written but only 44K were actually present. The fixes were real but the quantity was inflated.
- Subagents have a 50-call tool limit. Spending calls on review writing steals from content changes.
- Writing reviews yourself lets you verify actual file contents before rating.

**Workflow:**
1. Delegate fix-only subagents (no review-writing in their goal)
2. After all complete, verify actual word counts: `wc -w path/to/book/*MANUSCRIPT*.md`
3. Read key sections to confirm changes were applied
4. Write the new book-review.md yourself

### Tool Call Budget Management

Subagents hit 50 tool calls before the 600s timeout. Budget their calls:

| Phase | Calls Needed | Strategy |
|-------|-------------|----------|
| Read & analyze | 10-15 | read_file + search_files + grep to understand current state |
| Apply changes | 25-30 | write_file() for new content (faster than patch, which often fails on unmatched old_string) |
| Verify | 5-10 | wc -w, grep for patterns, spot-read |

For bulk content work across a full manuscript, **write_file() is more reliable than patch().** The patch tool fails when its fuzzy matching can't find the old_string — this happens frequently with long, complex manuscripts. write_file() always succeeds.

### Per-Book Fix Gains by Type

Different book profiles yield different gains per subagent pass:

| Book Type | Typical Start | Typical Gain/Pass | Iterations to Target |
|-----------|--------------|-------------------|---------------------|
| Cozy/Legal Mystery | 25-40K | 5-10K (chapters, B-plot, texture) | 4-8 |
| Sci-Fi Colonization Thriller | 23-30K | 3-6K (thread insertion, expansion) | 10-16 |
| Non-Fiction/Business | 15-40K | 2-4K (cases, examples, build fixes) | 10-20 |

Set expectations accordingly. A single pass won't triple word count.

### Critical: Which MANUSCRIPT.md to Work On

Some books have MULTIPLE `*MANUSCRIPT*.md` files. Always check which is authoritative:

```bash
ls -la path/to/book/*MANUSCRIPT*.md
wc -w path/to/book/*MANUSCRIPT*.md
```

Common problem: `MANUSCRIPT.md` is a 620-line excerpt or old compilation, while `retainer-to-trouble_MANUSCRIPT.md` is the active 5,900-line manuscript. Tell subagents explicitly which file to edit.

### Important: After ALL subagents complete, verify files directly before declaring done. Do not trust the subagent's self-report.

---

### Common Mistake: Multiple Chapter Header Formats

Subagents may add chapter headers in bold (`**Chapter 1:**`) instead of markdown `## Chapter 1:`. Both will render but the bold format loses markdown structure (TOC generation, anchor links). If you see `**Chapter N:**` at the top of chapters, convert them.

```bash
# Check format
head -1 path/to/chapter-file.md
```

**Standard:** `## Chapter N: Descriptive Subtitle` (H2 with subtitle)
**Non-standard:** `**Chapter N:** Descriptive Subtitle` (bold only)

Also note: subagents that expanded a book via `patch()` may leave behind `||` pipe artifacts in headers (e.g., `||## Epilogue:`) from adjacent text being consumed during the replacement. These should be cleaned up.

**Duplicate chapter numbering:** When subagents expand a manuscript by inserting new chapter headers, they sometimes create duplicate numbers (e.g., two "Chapter 3" headers) or fractional numbers (e.g., "Chapter 29.5"). Fix these by:
1. List all headers: `grep "^## Chapter" path/to/MANUSCRIPT.md`
2. Rename duplicates: add "(Continued)" suffix or renumber
3. Rename fractions: promote "29.5" to "30" and renumber subsequent chapters

## Common Book Fix Types

### Type A: Partial Rewrite (fewer than 10 chapters)
- Same as Type A below — delegate, but verify more aggressively

### Type A: Complete Chapter Rewrite
- Rewrite specific chapters as new .md files
- Overwrite old .xhtml files when placing new .md in manuscript_src/
- Targets: ~1500 words per chapter
- Must: deliver what the chapter title promises
- Must NOT: repeat scene templates from other chapters

### Type B: Name Consistency Fix
- Search all files for wrong name(s)
- Replace across chapters, manuscripts, output files
- Verify zero instances remain

### Type C: AI Artifact Removal
- Search for and remove template phrases, generation instructions
- Rewrite affected paragraphs

### Type D: Genre Tone Shift
- More subtle — requires reading and understanding the genre
- Cozy mystery: add warmth, humor, found family, food, quick dialogue
- Legal thriller: add tension, procedural detail, higher stakes
- Memoir: add sensory detail, earned reflection, first-person voice

### Type E: Word Count Adjustment
- Cut: remove redundant scenes, compress dialogue, merge chapters
- Expand: add scenes, develop subplots, increase sensory detail
- Over: see Type G below — when a book is 10K+ over target and trimming fails

### Type H: Add Front Matter (Copyright, Dedication, TOC)
Add a complete front matter section to MANUSCRIPT.md before Chapter 1:

```markdown
# [Book Title]

[Series name, if applicable]

**Copyright © 2026 Bob J Mills**

All rights reserved. No part of this book may be reproduced in any form or by any electronic or mechanical means, including information storage and retrieval systems, without written permission from the author, except for the use of brief quotations in a book review.

This is a work of fiction. Names, characters, places, and incidents either are the product of the author's imagination or are used fictitiously. Any resemblance to actual persons, living or dead, events, or locales is entirely coincidental.

ISBN: [placeholder]

First Edition: 2026

---

## Table of Contents

- [Chapter 1: Title](#chapter-1-title)
- [Chapter 2: Title](#chapter-2-title)
...

---

## Acknowledgments

[Thank you text]

---

```

### Type I: Add Back Matter (Also by + Author Bio)
Add a complete back matter section at the end of MANUSCRIPT.md after the final chapter:

```markdown
---

## Also by Bob J Mills

### The Age of Lightships Series
- [**Sunward Exodus**](https://www.amazon.com/dp/XXXXXXXXXX)
- [**The Mercury Accord**](https://www.amazon.com/dp/XXXXXXXXXX)
- [**Ghosts Beyond Neptune**](https://www.amazon.com/dp/XXXXXXXXXX)
- [**The Last Photon Fleet**](https://www.amazon.com/dp/XXXXXXXXXX)

### The Lunar Foundation Series
- [**Moon Rock**](https://www.amazon.com/dp/XXXXXXXXXX)
- [**Mooncoming**](https://www.amazon.com/dp/XXXXXXXXXX)
- [**Waters End**](https://www.amazon.com/dp/XXXXXXXXXX)
- [**Waters Horizon**](https://www.amazon.com/dp/XXXXXXXXXX)

### No Blue Sky Series
- [**Built from Dust**](https://www.amazon.com/dp/XXXXXXXXXX)
- [**The Oxygen Gamble**](https://www.amazon.com/dp/XXXXXXXXXX)
- [**Rivers Under Mars**](https://www.amazon.com/dp/XXXXXXXXXX)
- [**The Red Charter**](https://www.amazon.com/dp/XXXXXXXXXX)
- [**The First Martian Nation**](https://www.amazon.com/dp/XXXXXXXXXX)

### Cindy Lou Legal Capers Series
- [**Retainer to Trouble**](https://www.amazon.com/dp/XXXXXXXXXX)
- [**Clause for Alarm**](https://www.amazon.com/dp/XXXXXXXXXX)
- [**Affidavits and Alibis**](https://www.amazon.com/dp/XXXXXXXXXX)

### Business / Non-Fiction
- [**The Crisis-Ready Company**](https://www.amazon.com/dp/XXXXXXXXXX)
- [**AI That Works**](https://www.amazon.com/dp/XXXXXXXXXX)
- [**The Owner's Manual for AI Agents**](https://www.amazon.com/dp/XXXXXXXXXX)

### Memoir
- [**Tomorrow Remembered**](https://www.amazon.com/dp/XXXXXXXXXX)

---

**Get free prequel novellas** at [mifeco.com/books](https://www.mifeco.com/books)

**Visit the author's website:** [mifeco.com](https://www.mifeco.com)

---

## About the Author

Bob J Mills is a [brief bio]. He lives in [location]. This is his [Nth] book.

---

```

### Type J: Remove Cover Images from MANUSCRIPT.md
Check if any images at the start of MANUSCRIPT.md are cover-style images (full-page graphic with title text). If found, remove them — covers go in the EPUB/PDF build pipeline, not the manuscript source. Search: `grep -n "cover\\|Cover\\|COVER" MANUSCRIPT.md` should return zero matches for actual cover images.

### Type K: Template Differentiation (43-Chapter Template Fix)

When a book has 40+ chapters all following the identical structure (same scene beats, same character lineup, same emotional arc), **do NOT delegate all chapters to one subagent.** A single subagent cannot differentiate 43 chapters in 50 tool calls.

**The 3-pass split pattern:**

- **Pass 1 (subagent):** Fix the antagonist + climax + final 10 chapters. The highest leverage is creating a genuine antagonist with ideology and giving the ending real stakes. This alone can lift C+→B-.
- **Pass 2 (subagent):** Differentiate chapters 1-20. Change POV characters, vary the problem type, add rising tension. Each block of 5 chapters should feel distinct.
- **Pass 3 (subagent):** Differentiate chapters 21-33 (or wherever the template still repeats). Consolidate template chapters into scene-based arcs using the antagonist subplot as engine.
- **Parent review after each pass:** Re-rate before deciding whether to loop again.

**What makes a template chapter:**
```
Alert → Mission AI query → bullet points → great-grandparent reflection → Kaito channel → tear-wiping → 5-point framework → resolution
```
Every variant maps to this structure. The fix is to break the pattern: different character combinations, different problems, different emotional stakes per chapter block.

### Type L: Genre/Setting Bulk Shift (e.g., Moon→Mars)

When a book is set on the wrong planet/territory (Moon instead of Mars):
1. **Bulk sed replacements first** (fastest, most reliable):
```bash
sed -i 's/\blunar\b/Martian/g' MANUSCRIPT.md
sed -i 's/\bMoon\b/Mars/g' MANUSCRIPT.md
sed -i 's/Shackleton Crater/Valles Marineris/g' MANUSCRIPT.md
sed -i 's/LunaNet/MarsNet/g' MANUSCRIPT.md
# Verify:
grep -ci '\blunar\b' MANUSCRIPT.md  # Must be 0
grep -ci '\bMoon\b' MANUSCRIPT.md   # Must be 0
```
2. **Fix artifacts** from bulk replace: "the Mars" → "Mars", "the The Red Charter" → "The Red Charter"
3. **Rewrite climax chapters** (20-25) with planet-correct content: dust storms, thin atmosphere, specific Martian geography
4. **Verify:** 0 old-territory references, 120+ new-territory references

This approach can lift a D to B+ in a single pass because the climax is the highest-leverage target.

### Type F: Central Crisis Injection (Sci-Fi Pattern)

When a book has 40+ chapters all following the identical structure (same scene beats, same character lineup, same emotional arc), **do NOT delegate all chapters to one subagent.** A single subagent cannot differentiate 43 chapters in 50 tool calls.

**The 3-pass split pattern:**

- **Pass 1 (subagent):** Fix the antagonist + climax + final 10 chapters. The highest leverage is creating a genuine antagonist with ideology and giving the ending real stakes. This alone can lift C+→B-.
- **Pass 2 (subagent):** Differentiate chapters 1-20. Change POV characters, vary the problem type, add rising tension. Each block of 5 chapters should feel distinct.
- **Pass 3 (subagent):** Differentiate chapters 21-33 (or wherever the template still repeats). Consolidate template chapters into scene-based arcs using the antagonist subplot as engine.
- **Parent review after each pass:** Re-rate before deciding whether to loop again.

**What makes a template chapter:**
```
Alert → Mission AI query → bullet points → great-grandparent reflection → Kaito channel → tear-wiping → 5-point framework → resolution
```
Every variant maps to this structure. The fix is to break the pattern: different character combinations, different problems, different emotional stakes per chapter block.

### Type L: Genre/Setting Bulk Shift (e.g., Moon→Mars)

When a book is set on the wrong planet/territory (Moon instead of Mars):
1. **Bulk sed replacements first** (fastest, most reliable):
```bash
sed -i 's/\blunar\b/Martian/g' MANUSCRIPT.md
sed -i 's/\bMoon\b/Mars/g' MANUSCRIPT.md
sed -i 's/Shackleton Crater/Valles Marineris/g' MANUSCRIPT.md
sed -i 's/LunaNet/MarsNet/g' MANUSCRIPT.md
# Verify:
grep -ci '\blunar\b' MANUSCRIPT.md  # Must be 0
grep -ci '\bMoon\b' MANUSCRIPT.md   # Must be 0
```
2. **Fix artifacts** from bulk replace: "the Mars" → "Mars", "the The Red Charter" → "The Red Charter"
3. **Rewrite climax chapters** (20-25) with planet-correct content: dust storms, thin atmosphere, specific Martian geography
4. **Verify:** 0 old-territory references, 120+ new-territory references

This approach can lift a D to B+ in a single pass because the climax is the highest-leverage target.

For plotless sci-fi books where chapters are independent "construction diary" episodes, the single highest-impact fix is to inject a central engineering or political crisis at the midpoint.

**The full timeline pattern (crisis → cascade → antagonist → resolution):**

When executing a crisis injection, structure the arc across 12-14 chapters at the book's midpoint:

```
Chapter N (midpoint):    Crisis appears — visible, specific, personal
Chapter N+1:             Initial fix attempt fails — crisis worsens
Chapter N+2:             Underlying cause discovered (e.g., contamination)
Chapter N+3:             Cascade — secondary systems start failing
Chapter N+4:             New character or expertise arrives (e.g., estranged child)
Chapter N+5:             New solution attempted — partial success buys time
Chapter N+6 (60% mark):  Antagonist makes first move — external pressure appears
Chapter N+7:             Protagonist counters / takes dangerous action
Chapter N+8:             Antagonist escalates — recall order, threat, leverage
Chapter N+9-10:          Desperate gamble — last resort, high-risk solution
Chapter N+11 (75% mark): Crisis resolution — partial victory, permanent cost
```

The antagonist should NOT appear before the 60% mark. Their introduction IS the escalation — it transforms the crisis from engineering problem to political/ethical choice. Before introducing the antagonist, the crisis is a puzzle; after, it's an enemy.

**Sci-fi crisis types** (choose one, don't mix):
- Life support failure (CO2 scrubber, oxygen generator, water recycler)
- Micrometeorite strike (hull breach, module decompression)
- Power system cascade (solar array failure, battery thermal runaway)
- Structural failure (stress crack in critical load-bearing element / contamination weakening all components)
- Communication loss (antenna damage, cannot coordinate with Earth for help)

The contamination type (structural failure via material impurity) is the most versatile because it naturally cascades: every component made from the contaminated batch is ticking time bomb.

**Real example — Mooncoming (Book 2 of Lunar Foundation):**
- Before: 39 independent construction episodes — no rising tension, no through-line
- Fix: Ch16 — Critical Systems Failure (power node overload at 85°C→120°C, repair in 1:47, crack pattern matches a bridge collapse). Cascade through Ch17-25: contamination revealed → cascade failure → daughter arrives → impurity trap → Cole's First Move (InterSolar) → Remote Mine → Recall Order → Desperate Gamble → Resolution
- Antagonist (Harrison Cole/InterSolar) introduced at Ch21 (60% mark) with a recall order that Tom counters using bridge-collapse evidence
- Cole's escalation: Article 14 → 48-hour evacuation → negotiated to 72-hour extension
- Result: B+ → A- in one iteration; word count hit 80K target

**How to apply:**
```python
# Find chapters around the midpoint
midpoint = total_chapters // 2  # For 39 chapters, ~19-20
# Look for a 'lull' chapter — one where nothing important happens
# Replace it with a chapter titled "Chapter N: [The Crisis Name]"
# Write the crisis as: problem appears → initial solution attempt fails → 
#   crisis worsens → new solution attempted → partial success buys time →
#   crisis is contained but revealed a worse underlying problem
```

### Type G: Over-Word-Count Acceptance

Not every book needs trimming. When a book is 10K+ over its genre word-count target but the voice, plot, and character work are strong, the editorial judgment call is to **accept the natural length** rather than force a cut that damages the voice.

**When to use:**
- Book is at 85-100K in a genre targeting 60-75K (e.g., cozy mystery)
- The extra length comes from procedural or genre-hybrid content (e.g., court scenes, cross-examinations, depositions)
- The voice is distinctive, the plot is complete, the character work is consistent
- Multiple subagent trimming attempts timed out or produced poor results (trimming dispersed bloat programmatically often fails)
- The reader's experience is "enjoyable and immersive" not "bloated and slow"

**Signs that trimming is NOT the answer:**
- The book is over target but readers enjoy spending time with the protagonist
- The genre is a hybrid (cozy-legal, thriller-romance, sci-fi-political) — hybrid formats naturally run longer than pure genre
- The extra word count comes from entertaining dialogue and character scenes, not redundant exposition
- Trimming subagents consistently time out because the manuscript is too large to read (>85K words) — this signals the book is at its natural working size

**Real example — Cindy Lou Legal Capers, Book 1 (88K vs 60-75K target):**
- Two subagent passes timed out. The dispersed bloat (redundant cross-examination rounds, extended descriptions) was impossible to target programmatically without damaging voice
- The review's own assessment: "Accept 85-95K as the book's natural length. At this length the book has strong voice, complete plot, and consistent character work."
- Decision: Accepted at B+ (above B threshold) at natural length 88K words
- The hybrid cozy-legal format readers (Evanovich/Osman audience) prefer longer books where they can spend time with characters they enjoy

**If you must trim (subagent keeps timing out):**
1. Use `terminal` with inline Python (`python3 << 'PYEOF'`) to analyze chapter word counts — `execute_code` may be blocked on Telegram
2. Identify the 3 longest chapters (typically 8-10K words each in a 30-chapter book)
3. Target ~1,000-1,500 words from each by patching out one redundant scene per chapter
4. This reduces total by ~3-4K without affecting voice, character, or plot

When delegating a book fix, include this in the context:

```
Read the book-review.md FIRST. Then find MANUSCRIPT.md and chapter files.
Apply ALL changes from the review. Write updated chapter files as .md to manuscript_src/.

KEY CHANGES FROM REVIEW:
[copy from the review's specific instructions]

CRITICAL: Do NOT use CO2 coolant leaks, spectrometer dialogue, viewport endings,
or any template structure that repeats across chapters. Each chapter must be unique.

Write ~1500 words per chapter. Use write_file tool.
```

## Support Files

This skill provides:

### Templates (copy-and-adapt for manuscript fixes)
- `templates/front-matter.md` — copyright page + TOC + acknowledgments boilerplate
- `templates/back-matter.md` — "Also by Bob J Mills" full book list across all 6 series

### Scripts (run directly)
- `scripts/generate-ebook.py` — regenerate EPUB + PDF from MANUSCRIPT.md using ebooklib + WeasyPrint
  - Usage: `python3 scripts/generate-ebook.py /path/to/book/dir`
  - Auto-detects CLLC _MANUSCRIPT.md vs MANUSCRIPT.md
  - Reports page count and target compliance

### References
- See `book-editorial-review` → `references/page-count-target.md` for the 160-190 page target specification