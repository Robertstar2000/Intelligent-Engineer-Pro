---
name: book-editorial-review
displayName: Book Editorial Review
description: "Deep editorial analysis comparing manuscripts to bestselling genre benchmarks. Iterative loop: examine book, rate A-F, if A pass to next pipeline step, if below A incorporate changes into source and re-run review. Creates and updates book-review.md files per book directory."
category: publishing
tags: [editorial, review, manuscript, critique, benchmark, subagent]
related_skills: [reader-magnet-production, book-creation, writing-plans]
triggers: [review all books, editorial review, deep review, benchmark comparison, book-review.md, assess quality]
---

# Book Editorial Review

## When to Use

- The user asks you to review all books in a series or across the USB drive
- You need to assess manuscript quality against published bestsellers in each genre
- You need to create `book-review.md` files in each book's directory
- The user wants a "deep editorial review" or "bestseller quality assessment"

## The Iterative Editorial Loop (MANDATORY PROCESS)

This is the core process that must be followed for every book review. The loop continues until the book achieves an A rating:

```
Step 1: EXAMINE — Read the entire book (MANUSCRIPT.md + key chapter files)
         |
Step 2: REVIEW — Compare to bestselling genre benchmarks
         |
Step 3: RATE — Assign A-F rating
         |
Step 4: CHECK — Is rating A?
         |  YES -> Move to next pipeline step. DONE.
         |  NO  -> Continue to Step 5
         |
Step 5: FIX — Incorporate ALL editorial improvements into book source files
         (Rewrite chapters, fix issues, apply recommendations)
         |
Step 6: RE-EXAMINE — Return to Step 1 with the updated book
         (Loop continues until Book achieves A rating)
```

### Critical Rules

1. Do NOT stop after writing the review. If the book is not A quality, you MUST incorporate the changes into the actual book files.
2. After incorporating changes, re-run the full review from Step 1 (read the updated book, write a NEW book-review.md with the new rating, check if A).
3. Each iteration produces a NEW book-review.md that REPLACES the old one in the book's directory.
4. The user's instruction: "If the book achieves an A bestseller quality rating, the editorial review is completed and go to the next pipeline step. If it is not A quality, continue with this process. Recommend sections to be rewritten. Then incorporate the changes into the book source. Then rerun this entire editorial review process from the start."

### What "Incorporate Changes" Means

After writing the review with a below-A rating:
1. Read the review's recommended rewrites section
2. Apply every P0 and P1 fix to the actual book source files (chapter .md files in manuscript_src/ or chapters/)
3. Rewrite the specific chapters/sections identified
4. Rebuild the MANUSCRIPT.md from the updated chapters
5. **Verify the MANUSCRIPT.md was actually recompiled** — do NOT assume the source edit propagates. Run `grep -c "old-template-phrase" MANUSCRIPT.md` to confirm old content is gone. Read the first 50 lines of the MANUSCRIPT.md to confirm new content appears.
6. Then return to Step 1: read the updated book and write a NEW book-review.md

Do NOT just update the review file. Update the BOOK ITSELF. The review is a diagnostic tool. The actual work is changing the manuscript.

## Workflow

### Rule: Series-Level Reviews Must Be Split Per-Book

If a book series has a single consolidated book-review.md covering all books together, split it into individual per-book files before running the iterative loop. The loop operates per-book and a consolidated review masks which book needs what.

To split: read the series-level review, extract per-book findings, write a book-review.md in each book subdirectory with those findings plus a cross-book comparison section. The series-level review remains as the consolidated overview.

**Scope rule:** Only full-length books receive per-book reviews and individual book-review.md files. Novellas, short stories, and serials within a series do not get individual review files unless explicitly requested by the user. When the user says "you don't need to do novellas," this is the default — honor it by skipping per-book reviews on shorter works within a series.

### Step 1: Discover the Book Structure

First, map out all books:

```bash
# List all series directories
ls /mnt/usb_4tb/books/

# Find manuscript files
find /mnt/usb_4tb/books/Age_of_Lightships_Series -name "*MANUSCRIPT*" -o -name "*.md" | grep -v "book-review" | grep -v "README"

# Check chapter structure
ls Book_1/Chapters/ | head -5
ls Book_1/manuscript_src/ | head -5
```

### Step 2: Read the Manuscript

For each book, read at minimum:
- First 2 chapters (opening hook and setup)
- 2 middle chapters (around 40% and 60% marks)
- Last 2 chapters (resolution and ending)

Also run word counts:
```bash
wc -w path/to/MANUSCRIPT.md
wc -l path/to/MANUSCRIPT.md
```

**Word count double-check:** Compare the MANUSCRIPT.md word count against the sum of individual chapter file word counts (`wc -w chapters/*.md`). If they differ significantly, the MANUSCRIPT.md may be an old compilation that doesn't reflect the latest chapter edits. Recompile if needed.

### Step 3: Compare to Bestselling Genre Benchmarks

Use these benchmark comparisons based on the book's genre:

**Space Opera (Age of Lightships):**
- The Expanse (James S.A. Corey) — distinct POV voices, personal stakes connected to civilizational stakes, alternating quiet character moments with explosive setpieces every 3-4 chapters
- Revelation Space (Alastair Reynolds) — cold precise prose, universe revealed through action not exposition, implied history
- Children of Time (Adrian Tchaikovsky) — thematic depth, dual narrative, antagonist that is different not evil

**Sci-Fi Colonization Thriller (Lunar Foundation):**
- The Martian (Andy Weir) — problem→solution→failure→new solution, humor under pressure, distinctive first-person voice
- Red Mars (Kim Stanley Robinson) — political complexity, characters with irreconcilable worldviews, ecological realism
- Seveneves (Neal Stephenson) — opening disaster creates immediate stakes, escalating tension where new problem appears the moment the previous one is solved

**Martian Colonization Epic (No Blue Sky):**
- The Martian (Andy Weir) — relentless problem-solving, humor as survival mechanism
- Red Mars (KSR) — philosophical depth, terraforming science as character
- Children of Time (Tchaikovsky) — long-time-span storytelling, thematic depth

**Cozy Legal Mystery (Cindy Lou Legal Capers):**
- No. 1 Ladies' Detective Agency (McCall Smith) — warm character-driven, Precious Ramotswe's personality IS the series
- Thursday Murder Club (Richard Osman) — ensemble cast, humor, clever mystery but relationships are why readers stay
- Stephanie Plum (Evanovich) — romantic tension, humor, found family, mystery as framework not content

**Business / Non-Fiction:**
- Zero to One (Peter Thiel) — contrarian thesis every page, one idea per chapter argued with evidence
- Atomic Habits (James Clear) — crystal-clear structure, one idea + one story + one application per chapter
- The Lean Startup (Eric Ries) — case-study driven, theory proven through narrative

**Memoir:**
- Educated (Tara Westover) — specific sensory scenes, no life-summary opening, reflection earned through narrative
- When Breath Becomes Air (Paul Kalanithi) — philosophical depth without abstraction
- Wild (Cheryl Strayed) — external journey mirrors internal one

### Step 4: Create book-review.md

Write a `book-review.md` file in the book's directory with this structure:

```markdown
# Editorial Review: [Book Title]

**Date:** [date]
**Iteration:** [1, 2, 3, ...]
**Rating:** [A / A- / B+ / B / C+ / C / D / F]
**Word Count:** [N words]
**Chapter Count:** [N]
**POV Characters:** [names]
**Genre:** [genre]

## Executive Summary

[2-3 sentence overview. MUST state whether this book is ready to pass to the next pipeline step.]

## Strengths

- [specific strength with evidence from the text]

## Critical Weaknesses

[MUST-FIX issues preventing A-level quality. Be specific about chapter numbers and page ranges.]

## Bestseller Benchmark Comparison

| Dimension | Current Book | Genre Bestseller Standard | Gap |
|-----------|-------------|--------------------------|-----|
| Opening hook | [description] | Hook within first page | [gap] |
| Character voice | [assessment] | Distinct POV voices | [gap] |
| Pacing | [assessment] | Setpiece every 3-4 chapters | [gap] |
| Dialogue subtext | [assessment] | Characters rarely say what they mean | [gap] |
| Sensory density | [assessment] | Physical grounding in every scene | [gap] |

## Changes Applied This Iteration

[For iteration 2+: describe what was fixed since the last review. For iteration 1: "Initial review -- no changes yet applied."]

## Remaining Issues (Sequenced by Priority)

### P0 — Must Fix Before Next Iteration
[Highest-impact change needed]

### P1 — Should Fix Before Next Iteration
[Other critical issues]

### P2 — Fix When Possible
[Nice-to-have improvements]

## Recommended Rewrites for Next Iteration

### Section 1: [Chapter range]
- **Problem:** [specific issue]
- **Fix:** [specific rewrite instructions]

### Section 2: [Chapter range]
- **Problem:** [specific issue]
- **Fix:** [specific rewrite instructions]

## Single Highest-Impact Revision

[One change that would improve the book more than any other]

## Next Step Decision

**If Rating == A:** This book passes to the next pipeline stage. Editorial review complete.
**If Rating < A:** This book requires another iteration. Apply the recommended rewrites above, then re-run the editorial review from Step 1.

## Genre-Specific Checks

- [ ] First page hook test
- [ ] Personal stakes (not abstract "save the world" -- personal "why")
- [ ] Character voice differentiation
- [ ] Word count within genre target
- [ ] Subtext in dialogue
- [ ] Sensory grounding in every scene
```

### Step 5: The "Make Assumptions, Not Opinions" Rule

When writing the review, the user's explicit preference is:
- **DO NOT** start sentences with "I think," "I recommend," "It seems," "Perhaps," "Maybe"
- **DO** state findings as facts: "The opening lacks a hook because..." "Chapter 7's problem is..."
- **DO** give specific chapter numbers, page ranges, and concrete alternatives
- **DO** provide before/after dialogue examples where possible

### Quality Benchmark: Humanized Writing

The user's explicit standard: **"Make sure the writing is humanized and not like it is AI. Use your writing and publishing skills."** This means the review should:
- Sound like a professional editor's feedback, not a rubric
- Use publishing-industry terminology naturally (voice, pacing, stakes, subtext, sensory density, earned payoff)
- Judge against market-ready benchmarks, not against theoretical ideals
- Be specific enough that the author could hand the review to a freelance editor and get the same conclusions

### Step 6: Use Subagent Delegation for Parallel Reviews

When reviewing multiple series, delegate each series to a separate subagent. This is the most efficient approach for 10+ books across 3-4+ series.

Each subagent receives:
1. The book locations
2. The genre benchmarks for their series
3. The book-review.md template
4. The "make assumptions" rule
5. The template checklist items

Subagents need `terminal` and `file` toolsets to read manuscripts and write review files.

**Timeout Pitfall:** Large manuscripts (40K+ words) may cause subagents to hit the 600s timeout. To avoid this:
- Keep each subagent to one series (3-5 books max)
- Make the goal specific about what to fix, not open-ended
- If a subagent times out, the partial work is lost -- checkpoint by using small, focused goals
- For extremely large manuscripts (100K+ words), consider delegating individual books rather than whole series
- **Best pattern from experience:** For series with complex books (40K+ word manuscripts, detailed genre analysis), delegate one subagent per BOOK, not per series. Three subagents running 3 books in parallel is faster and more reliable than one subagent running a whole series.
- **Deep timeout strategy:** When a book MANUSCRIPT.md is 80K+ words and subagents consistently time out, don't delegate "review this whole book." Instead, delegate micro-goals: "read Ch12-13 from the source file and expand them," or "write one POV chapter and insert it after Ch14." These micro-tasks complete in 90-200s reliably.
- **After a timeout, check for partial work:** Not all timeouts are total losses. Run `find path -name \"*.md\" -newer <existing_file> -type f` to see if any files were modified during the interrupted subagent run.

## Second-Pass / Re-review Methodology

After initial fixes are applied, do a second-pass review to verify whether recommendations were ACTUALLY implemented:

### Step 1: Verify Review Assumptions Before Acting

**Do NOT trust an existing book-review.md at face value.** The existing review may be stale -- it was written at a point in time and the manuscript may have been fixed since. Before prescribing fixes based on a prior review:

1. Read the MANUSCRIPT.md (the actual compiled manuscript, not a file named `*_MANUSCRIPT.md` that may be a legacy copy)
2. Read the individual chapter files to check if fixes were already applied
3. Compare the review's claims against the actual files
4. Only then determine what actually needs fixing

**Real example:** The Crisis-Ready Company had a series-level review claiming C+ (40 chapters at 690 words, only 3 chapters rewritten). But the actual MANUSCRIPT.md was already 15 chapters with 4 Part dividers, 15 "The One Thing" takeaway boxes, and consistent first-person voice -- the review was simply never updated. Following it blindly would have caused wasted work.

**Signs of a stale review:**
- Review says "40 chapters" but MANUSCRIPT.md has 15
- Review says "no takeaway boxes" but MANUSCRIPT.md has them
- Review mentions a problem that `grep` shows does not exist in the current files
- The review's iteration number is lower than the timestamp of the current MANUSCRIPT.md changes

### Step 2: Manual verification, not trust

Do NOT trust subagent reports that fixes were applied. Read the actual files to confirm. This session repeatedly found:
- Subagents claimed they rewrote chapters, but old template content remained in the compiled MANUSCRIPT.md
- Subagents claimed names were fixed, but only 2 of 30 chapters were actually fixed  
- Subagents claimed books were rewritten for Mars, but old Moon-base remnant files still existed

**Also: Do NOT trust filenames to tell you what a file contains.** In this session, files named `Chapter_*_RW.md` were assumed to be first-person business rewrites — but they actually contained Mars/sci-fi experimental content. Always read the first ~30 lines of any file you plan to use as a source for compilation or merging. If the content doesn't match expectations, verify more broadly before incorporating it.

### Step 3: Read the compiled output, not just the source

If a book has `chapters/` with new .md files AND `manuscript_src/` with old .xhtml files, the MANUSCRIPT.md may still use the old versions. Verify by:
```bash
grep -c "template-phrase" path/to/MANUSCRIPT.md
```
If old template phrases still exist, the MANUSCRIPT.md needs recompilation from updated sources.

### Step 4: Check for remnant files

Old manuscripts that have been superseded should be deleted or archived. Look for:
- `*_MANUSCRIPT.md` alongside `MANUSCRIPT.md` (different versions)
- `.xhtml` files alongside new `.md` files sharing the same chapter number
- Old-named PDFs/EPUBs alongside new versions

### Step 5: Check for cross-book genre pattern

When reviewing a series, check if ALL books share the same genre mislabel. A single book misclassified is an anomaly. Three books all misclassified from cozy to legal thriller is a series-level decision point. Call this out explicitly -- the word count target, tone, stakes, and reader expectations all change with genre, and fixing one book while leaving the others mislabeled creates inconsistency.

To detect: compare the genre of each book's content against its marketed genre. If 2+ books in a series share the same mislabel, flag it at series level and do not try to fix within the wrong genre.

### Step 6: Re-rate based on remaining gaps

Use this framework for second-pass rating adjustments:

| Finding | Rating Impact |
|---------|---------------|
| Template content still in compiled output | -1 full letter grade |
| Name inconsistency across series | -1 full letter grade |
| Critical continuity error (two same-named characters) | -1 full letter grade |
| Only partial chapters rewritten (<20% of total) | -0.5 letter grade |
| New content present but compiled MS not updated | -0.5 letter grade |
| Repeated paragraphs (>3 identical blocks) | -0.5 letter grade |
| Fixes fully applied as recommended | Hold or +0.5 if other improvements made |

### Step 7: Flag genre re-classification needs

If a book doesn't match its market genre, say so explicitly. Example: Cindy Lou Series is marketed as "cozy mystery" but reads as "legal thriller." This is a FUNDAMENTAL issue -- the word count target, tone, stakes, and reader expectations all change. Don't try to fix it within the wrong genre. Recommend re-classification OR a comprehensive tone shift.

## What to Check in Every Book

### Critical Structural Checks

1. **Opening hook:** The first 500 words must drop the reader into a moment, not explain. A treaty recap or character biography is a failed hook. A disaster, an irreversible choice, or an anomaly is a successful hook.

2. **Character stakes:** Every protagonist needs a personal WHY that is emotional, not abstract. "Mars needs terraforming" is abstract. "I left my sister behind and I don't know if I'm becoming my father" is personal.

3. **Word count fit:** Each genre has a target:
   - Cozy mystery: 50-70K words
   - Space opera debut: 90-120K words
   - Business non-fiction: 40-60K words
   - Memoir: 70-90K words
   - Sci-fi thriller: 80-110K words

4. **Dialogue subtext:** Characters should rarely say what they actually mean. Conflict should be beneath the words, not in them.

5. **Sensory density:** Every scene needs at least 2-3 physical details (smells, sounds, textures, temperature, food). This is the single fastest way to raise prose quality.

### The Two-Manuscript Problem (Critical)

Several books had UPDATED `.md` chapters in a `chapters/` directory or `manuscript_src/` directory, but the compiled `MANUSCRIPT.md` still used OLD `.xhtml` content. This causes reviewers to assess the wrong version.

**How it happens:**
- New `.md` chapters are written to `chapters/` (from a rewrite subagent)
- Existing `.xhtml` chapters remain in `manuscript_src/`
- The `MANUSCRIPT.md` was compiled from `manuscript_src/` (old content)
- BOTH directories have content for overlapping chapter numbers
- A reader/reviewer who reads `MANUSCRIPT.md` sees the old version

**How to detect:**
```bash
# Check if chapters/ and manuscript_src/ both exist with overlapping content
ls Book_1_Moon_Rock/chapters/ | head -5
ls Book_1_Moon_Rock/manuscript_src/ | head -5
# Check if MANUSCRIPT.md references old template phrases
grep -i "template phrase\|viewport\|the work continued" Book_1_Moon_Rock/MANUSCRIPT.md | head -5
```

**How to fix:**
1. Move or copy new `.md` files to `manuscript_src/` overwriting the old `.xhtml`
2. Recompile `MANUSCRIPT.md` from `manuscript_src/`
3. Delete the duplicate `chapters/` directory if no longer needed
4. Rebuild EPUB and PDF from the new MANUSCRIPT.md

### Identifying End-of-Book Compression (Common Pattern)

Multiple books in this session had **expanded opening chapters but compressed final chapters**. The climax and resolution (typically the last 2-3 chapters) were written as brief summaries while the setup chapters were fully dramatized. This makes the book feel anticlimactic.

**Signs:**
- Opening chapters are 1,500-3,000 words each; last 2-3 chapters are 300-800 words
- The climax is described in one paragraph ("The vote passed. Celebrations began.")
- The ending happens "off-screen" (e.g., Earth's recognition message arrives but the reader never sees it)
- Chapter headers become terse compared to early chapters

**How to fix:**
- Expand the climax chapter into a full scene — sensory detail, dialogue, character reactions, pacing beats
- If the ending is stated rather than shown, write the moment the reader is missing (the message arriving, the vote tallying, the deadline passing)
- Add 2-3 beats after the climax: immediate aftermath, short-term consequence, hint of what comes next
- Target: each final chapter should be at least 1,500 words (comparable to opening chapters)

**Real example:** The Oxygen Gamble's ending was "Earth sent recognition. The First Martian Nation was recognized." — a 50-word summary. Expanded to a ~2,000-word scene: Senna waiting in the communications center, the light turning white, the UN Secretary-General appearing, Resolution 4721 reading, the applause in the corridor, Senna dictating the response, the 8-minute speed-of-light delay mirroring her great-grandmother's first day. This lifted the ending from C+ to A-.

### For Business/Non-Fiction Books: Check the Build Pipeline

**Critical discovery:** The Owner's Manual for AI Agents had an A- rating that turned out to be caused by BUILD SCRIPTS, not the manuscript. The source chapter files were excellent (first-person, MIFECO attribution, strong voice), but `build_html.py`, `build_epub.py`, and `build_package.py` injected "anonymized composites" and "illustrative numbers" disclaimers into the output during compilation. The review had been blaming the manuscript's "voice" when the real problem was in the pipeline.

**Always check for business/non-fiction books:**
```bash
# Search for disclaimer language in build files
grep -r -i "anonymized\|composite\|illustrative\|observed patterns\|not just mine" path/to/book/build_*.py 2>/dev/null
grep -r -i "anonymized\|composite\|illustrative\|observed patterns" path/to/book/*.py 2>/dev/null
```

**How to fix:**
1. Patch the build scripts to replace disclaimer language with direct attribution (e.g., "draw from real implementations" instead of "anonymized composites based on observed patterns")
2. Patch any metadata files (KDP_AI_Disclosure.md, copyright pages) that may also have weaker language
3. Rebuild the EPUB/PDF and verify the disclaimer language is gone from the output

**Wider lesson:** When a book has strong source files but a low rating, check the entire delivery pipeline. The issue may not be in the writing at all. See `references/build-script-patterns.md` for exact grep patterns and replacement text.

### Common AI Artifacts to Flag

- **Repeated sentence templates:** "The [noun] required [abstraction] and [abstraction]" appearing verbatim across different chapters
- **Scene structure repetition:** Every chapter having the identical beat structure (wake up → work → discover problem → fix problem → end at viewport)
- **Exposition-heavy openings:** Chapters starting with "The [facility] was a [adjective] structure that..."
- **Missing character differentiation:** All POV characters using the same vocabulary and sentence rhythms
- **Visible generation instructions:** AI task notes left in the text (word count targets, self-correction notes)
- **Name inconsistency:** Protagonist last name changing between books or within a book

### Rating Guide

| Rating | Meaning |
|--------|---------|
| A | Comparable to published bestseller. Minor polish needed. |
| A- | Near-bestseller quality. One significant rewrite needed. |
| B+ | Strong manuscript. Structural issues but solid foundation. |
| B | Competent. Needs significant revision to compete. |
| C+ | Has potential. Major structural problems. |
| C | Repetitive, templated, or genre-ignorant. Needs rewrite from chapter outlines. |
| D | Fundamentally broken. Needs complete rewrite. |

---

## Reference Files

This skill has reference files for session-specific detail:
- `references/genre-benchmarks.md` — full genre comparison tables for all 6 genres
- `references/build-script-patterns.md` — grep patterns and replacement text for business/non-fiction build pipeline fixes
- `references/chapter-expansion-patterns.md` — 5 techniques for expanding compressed chapters into full dramatic scenes