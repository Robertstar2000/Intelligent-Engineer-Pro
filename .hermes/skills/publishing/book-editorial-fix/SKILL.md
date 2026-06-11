---
name: book-editorial-fix
displayName: Book Editorial Fix Workflow
description: Process for applying editorial fixes from book-review.md files to existing manuscripts. Reading review → locating chapter sources → applying targeted rewrites → verifying changes → recompiling manuscript → rebuilding EPUB/PDF.
category: publishing
tags: [editorial, fix, rewrite, manuscript, chapter, revision, subagent]
related_skills: [book-editorial-review, book-publishing, manuscript-restoration, reader-magnet-production]
triggers: [apply review, fix per review, update book, rewrite chapters, implement editorial, apply book-review.md recommendations, second pass fixes]
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

Write new `.md` files to `manuscript_src/` (not `chapters/`) so the next compile picks them up automatically. If writing to `chapters/`, note that you'll need to move them afterward.

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

Use the standard build pattern (see `reader-magnet-production` skill for full implementation):

**EPUB:** zipfile-based EPUB 3 with mimetype STORED, META-INF/container.xml, OEBPS/content.opf, OEBPS/nav.xhtml, OEBPS/toc.ncx, OEBPS/styles/epub.css

**PDF:** fpdf2 at 6x9" (152.4 x 228.6 mm), DejaVu Serif at 11pt

Save output files as `book-name.epub` and `book-name.pdf` in the book's root directory.

## Parallel Work Strategy

When fixing multiple books simultaneously:

1. Group by fix type (name fixes, complete rewrites, partial edits)
2. Delegate each group to a separate subagent
3. Each subagent gets the FULL context from the book-review.md
4. Set subagent toolsets to `["terminal", "file"]`
5. Limit each subagent to 1-2 books to avoid 600s timeout

**Timeout-safe pattern:** For complete rewrites (Books 4-5 style), delegate ONE BOOK per subagent, not a series. Each book takes ~4-6 chapter rewrites at ~1500 words each, which fits in a 300-400s subagent window.

**Important:** After ALL subagents complete, verify files directly before declaring done. Do not trust the subagent's self-report.

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

## Subagent Instructions Template

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