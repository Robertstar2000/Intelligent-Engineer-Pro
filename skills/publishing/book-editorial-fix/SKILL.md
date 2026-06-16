---
name: book-editorial-fix
displayName: Book Editorial Fix Workflow
description: Process for applying editorial fixes from book-review.md files to existing manuscripts. Reading review → locating chapter sources → applying targeted rewrites → verifying changes → recompiling manuscript → rebuilding EPUB/PDF.
category: publishing
tags: [editorial, fix, rewrite, manuscript, chapter, revision, subagent]
related_skills: [book-editorial-review, book-publishing, manuscript-restoration, reader-magnet-production]
triggers: [apply review, fix per review, update book, rewrite chapters, implement editorial, apply book-review.md recommendations, second pass fixes, front matter, back matter, copyright page, table of contents, also by, acknowledgments, template differentiation, genre shift, bulk sed replace, Moon to Mars, template chapters, crisis injection, placeholder removal, thematic rewrite, severe corruption, copy-paste removal]
---

# Book Editorial Fix Workflow

## When to Use

- You have a `book-review.md` file in a book directory with specific rewrite instructions
- You need to apply editorial fixes to existing manuscripts (cut, expand, rewrite chapters)
- You need to rebuild EPUB and PDF after applying fixes
- A user says "update each book IAW the instructions in the book-review.md file"

## Overview

The fix workflow has 6 phases:
0. **Diagnose:** Quantify placeholder damage before choosing a fix strategy
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

## Phase 0: Quantitative Damage Assessment

Before choosing a fix strategy, quantify how much of the manuscript is copy-pasted placeholder content. This diagnostic determines whether you need a targeted fix (Type A / C) or a complete rewrite (Type R).

### Step 1: Baseline — Word Count & Uniqueness Ratio

```bash
cd /path/to/book

# Total vs unique word count
total=$(wc -w < MANUSCRIPT.md)
unique=$(cat MANUSCRIPT.md | tr ' ' '\n' | sort -u | wc -l)
ratio=$(echo "scale=2; $unique * 100 / $total" | bc)
echo "Total words: $total"
echo "Unique words: $unique"
echo "Uniqueness ratio: $ratio%"
```

**Interpretation:**
| Ratio | Diagnosis | Recommended Fix |
|-------|-----------|-----------------|
| >30% | Healthy — some repetition but salvageable | Targeted fixes (Type A/B/C) |
| 15-30% | Moderate damage — significant placeholder content | Type C + partial rewrite |
| <15% | Severe corruption — majority is copy-pasted from other books | Type R (complete rewrite) |

### Step 2: Known Placeholder Phrase Scan

Run a multi-phrase grep for common template blocks that get copy-pasted across books:

```bash
for phrase in \
  "work required patience and precision" \
  "drill bit sang into the regolith" \
  "equipment hummed softly" \
  "silence of the habitat was broken" \
  "monitor flickered, casting blue light" \
  "too far to fail now" \
  "regolith underfoot was finer than talc" \
  "familiar pressure of the EVA gloves" \
  "drifted from technical to personal" \
  "sound conducted through bone" \
  "small table that served as both" \
  "family forged in the crucible" \
  "pressed their palm against the cool glass" \
  "silent communion with the planet" \
  "Sarah's hands were raw" \
  "puzzle with no edge pieces" \
  "Self-Correction:" \
  "Word count:"; \
do
  count=$(grep -ci "$phrase" MANUSCRIPT.md 2>/dev/null || echo 0)
  [ "$count" -gt 0 ] && echo "PLACEHOLDER ($count): $phrase"
done
```

Each match > 0 indicates copy-pasted block from another manuscript. Add any new phrases you discover during the fix to this list for future diagnostics.

### Step 3: Inter-Book Content Check

Scan for content from the WRONG book in the series — pandemic plots, alien signals, or crisis scenes from a different installment:

```bash
for phrase in "alien signal" "spread pattern" "mortality rate" "airborne vector" "pandemic" "water reclamation"; do
  count=$(grep -ci "$phrase" MANUSCRIPT.md 2>/dev/null || echo 0)
  [ "$count" -gt 0 ] && echo "CROSS-BOOK LEAK ($count): $phrase"
done
```

### Step 4: Character Name Audit & Character Map (MANDATORY)

Count occurrences of every character name variant to detect inconsistent naming AND verify a Character Map exists:

```bash
# Character Map verification
if [ -f "CHARACTER_MAP.md" ]; then
  echo "CHARACTER_MAP.md found — verifying against manuscript"
  # Check each canonical name from the map
  while IFS='|' read -r canonical aliases role chapter relationships voice books; do
    [ -z "$canonical" ] && continue
    canonical=$(echo "$canonical" | xargs)
    count=$(grep -c "$canonical" MANUSCRIPT.md 2>/dev/null || echo 0)
    echo "  $canonical: $count occurrences"
  done < CHARACTER_MAP.md
else
  echo "WARNING: No CHARACTER_MAP.md found — creating one is required"
fi

# Name variant audit
for name in "Elena Vargas" "Elena Varga" "Elena Chen"; do
  echo "$name: $(grep -c "$name" MANUSCRIPT.md 2>/dev/null || echo 0)"
done

for auth in "Bob Mills" "Bob J Mills"; do
  echo "$auth: $(grep -c "$auth" MANUSCRIPT.md 2>/dev/null || echo 0)"
done
```

**Character Map Requirements (must exist for every book):**
- **Per Book (CHARACTER_MAP.md in book directory):** Canonical name, aliases/nicknames, role, first appearance chapter, key relationships, voice/persona notes, books appearing in
- **Per Series (SERIES_CHARACTER_MAP.md at series level):** Cross-book canonical reference for every recurring character, with deliberate changes explained
- **Naming Rules Enforced:**
  1. One canonical name per character (no Tom/Thomas/Tommy switching)
  2. Surnames stable (no mid-book or cross-book changes without in-story explanation)
  3. No duplicate names for different characters (Jane Wilson ≠ 4 different people)
  4. Pronouns intentional and consistent (they/them must be deliberate and stable)
  4. Title/rank consistency (pick ONE reference style per scene context)

**Plot Map Requirements (must exist for every book):**
- **Per Book (PLOT_MAP.md in book directory):** Chapter-range table showing core conflict, stakes, key twist/revelation, cause→effect link to next section, resolution status for each major structural segment (Ch1-5, Ch6-10, Ch11-15, Ch16-20, Ch21-25, Ch26-30, Ch31-35, Ch36-40)
- **Per Series (SERIES_PLOT_MAP.md at series level):** Cross-book canonical reference showing each book's core conflict, stakes arc, key twists, how it sets up the next book, resolution status
- **Flow Rules Enforced:**
  1. Plot flows consistently — each scene causes the next, not "and then this happened"
  2. Stakes escalate — complications multiply, tension curves upward, no sagging middle
  3. No idiot plot — characters don't act stupidly just to advance the plot
  4. No deus ex machina — resolutions earned through character agency, not coincidence
  5. Subplots interweave with main plot, not run parallel without intersection
  6. Ending is both surprising and inevitable — the only way it could have gone

**Framework Map Requirements (for Non-Fiction / Business Books):**
- **Per Book (FRAMEWORK_MAP.md in book directory):** Part-level table showing core thesis/claim, framework element, key case study, actionable takeaway ("The One Thing"), reader exercise/tool, cross-chapter link for each major part (Assess/Choose/Implement/Optimize or equivalent 4-part structure)
- **Per Series (SERIES_FRAMEWORK_MAP.md at series level):** Cross-book canonical reference showing each book's core thesis, framework contribution, key frameworks introduced, how it builds on previous, reader journey position
- **Quality Rules Enforced:**
  1. Thesis clarity — core argument stated in Ch 1, reinforced every chapter
  2. Framework utility — each chapter introduces/applies a reusable framework (not just advice)
  3. Case study density — ≥1 concrete case study per chapter (real, specific, with numbers)
  4. Personal storytelling — author's own failures/successes woven throughout
  5. Provocative chapter headers — every title makes a CLAIM, not a description
  6. Implementation apparatus — every chapter ends with "The One Thing" + exercise/checklist/template
  7. No filler — every paragraph advances argument or illustrates framework
  8. Cross-chapter coherence — frameworks build cumulatively
  9. Reader journey clarity — positions reader at competency level (novice→practitioner→expert)
  10. Companion resources — downloadable tools/templates referenced and exist

**Verification:** After any fix pass, audit the manuscript against the Character Map AND (Plot Map for fiction OR Framework Map for non-fiction). Flag any deviations as P0 defects.

### Step 5: Chapter Structure Map

```bash
echo "Chapter headers:"
grep "^# Chapter " MANUSCRIPT.md
echo ""
echo "Old/generic titles still present (should be 0):"
for title in "First Footsteps" "Site Selection" "Power Grid Online" "Helium-3 Discovery" "Resupply Mission"; do
  count=$(grep -c "$title" MANUSCRIPT.md 2>/dev/null || echo 0)
  [ "$count" -gt 0 ] && echo "  $title: $count"
done
```

### Decision Tree

```
Quantify damage (Step 1-5)
│
├─ Uniqueness >30% AND no cross-book leaks AND <3 placeholder matches
│   → Targeted fix (Type A/B/C/H/I/N)
│
├─ Uniqueness 15-30% OR 3-10 placeholder matches OR 1-2 cross-book leaks
│   → Partial rewrite + targeted cleanup (Type A/C + H/I/N)
│   └─ Keep salvageable chapters, rewrite contaminated ones
│
└─ Uniqueness <15% OR >10 placeholder matches OR cross-book leaks >2
    → Complete rewrite (Type R)
    └─ Discard all placeholder content, write new manuscript from scratch
```

### Subagent delegate_task Timeout (Critical)

The `delegate_task` tool has a **hard internal timeout of ~600 seconds** regardless of the patched `DEFAULT_CHILD_TIMEOUT` setting (1800s). This was confirmed across multiple sessions: subagents consistently time out at 600s even when the config says 1800s.

**Workaround:** For large editorial expansion tasks (expanding a book from 20K to 50K+ words), do NOT use `delegate_task`. Instead:

1. Write a Python expansion script to a file (e.g., `expand_chapters.py`)
2. Run it via `terminal`: `python3 /path/to/book/expand_chapters.py`
3. The script reads the existing manuscript, generates expanded content, and writes the result
4. Multiple expansion passes can be chained: `python3 expand_pass1.py && python3 expand_pass2.py`

**When to use terminal scripts vs delegate_task:**
| Task | Tool | Why |
|------|------|-----|
| Small fixes (name changes, AI artifact removal) | delegate_task | Fits in 600s |
| Large expansion (20K -> 50K words) | terminal script | Needs 1000+ tool calls |
| Complete rewrite of weak chapters | terminal script | Needs to write 15K+ words |
| Multiple books in parallel | terminal scripts | No concurrency limit |

### Chapter Expansion via Python Strings (Size Limit)

Writing entire chapters as Python string literals in `write_file()` calls hits practical size limits (~8K tokens per call). For large chapters (2,500+ words), use one of these patterns:

**Pattern 1: Terminal heredoc (preferred)**
```bash
python3 << 'PYEOF'
import re
with open('MANUSCRIPT.md', 'r') as f:
    content = f.read()
# ... expansion logic ...
with open('MANUSCRIPT.md', 'w') as f:
    f.write(content)
PYEOF
```

**Pattern 2: Write expansion to separate file, then append**
```bash
# Generate expansion content
python3 -c "
expansion = '''[1500 words of new content]'''
with open('expansion_ch11.txt', 'w') as f:
    f.write(expansion)
"
# Append to chapter
echo "" >> MANUSCRIPT.md
cat expansion_ch11.txt >> MANUSCRIPT.md
```

**Pattern 3: Multiple smaller write_file calls**
Break the expansion into 500-word chunks and write each separately.

### User Communication: "Characters" vs "Words"

When the user says "2500 to 3000 characters" in the context of chapter length, they almost certainly mean **words**, not characters. 2,500 characters is only ~400 words -- far too short for a chapter. Always interpret chapter length targets as words unless explicitly stated otherwise.

### Rewrite vs Expand Preference

When a book needs massive expansion (e.g., 23K -> 50K words), the user prefers **rewriting the weakest chapters from scratch** over appending expansion content to existing chapters. This produces more cohesive, higher-quality prose.

**Approach:**
1. Identify the weakest chapters (under 1,000 words, summary-like, or heavily templated)
2. Rewrite them from scratch using genre benchmarks and humanizer rules
3. Keep strong chapters (over 2,000 words) as-is
4. Target 2,000-3,000 words per rewritten chapter
5. Apply multiple expansion passes if needed, verifying word count after each pass

### Expansion Pass Strategy

For books needing 20K+ words of new content, use multiple expansion passes:

| Pass | Target | Approach |
|------|--------|----------|
| 1 | +4-6K | Rewrite the 6-8 weakest chapters from scratch |
| 2 | +4-6K | Expand remaining weak chapters with new scenes |
| 3 | +3-5K | Add dialogue, sensory detail, internal monologue |
| 4 | +2-3K | Final polish, ensure all chapters hit 2,000+ |

After each pass, verify with `wc -w MANUSCRIPT.md` and check chapter-level distribution.

### Tool Call Budget for Expansion Scripts

When writing expansion scripts via terminal, be aware of the 50 tool call limit per script execution. For large expansions:

1. **One script per chapter** -- don't try to expand all chapters in one script
2. **Use file I/O** -- read/write files directly rather than making many small edits
3. **Batch operations** -- use `cat >>` to append content rather than individual `write_file` calls
4. **Verify after each script** -- run `wc -w` to confirm the expansion was applied

## Phase 2: Apply Fixes

### Writing Updated Chapters

For bulk content work across a full manuscript, **write_file() is more reliable than patch().** The patch tool fails when its fuzzy matching can't find the old_string — this happens frequently with long, complex manuscripts. write_file() always succeeds.

When to use each:

| Tool | Best For | Avoid When |
|------|----------|------------|
| write_file() | Whole-file content, new chapters, major expansions | Replacing tiny sections in an otherwise-good file |
| patch() | Targeted fixes, name changes, AI artifact removal | Files with heavy repetition (patch may match wrong instance) |
| terminal (sed) | Bulk find-and-replace across multiple files | Any change where you need to verify context before replacing |

**⚠️ Pitfall: Overbroad find/replace creates cascading typos.** When using sed or patch for bulk replacements, ALWAYS verify the replacement didn't corrupt other words. A subagent's "I wa" → "I was" fix produced 22 new typos in one session: "I wanted" became "I wasnted", "I want" became "I wasnt", "I walked" became "I waslked", "I watched" became "I wastched". Prevention:
```bash
# After bulk fix, check for corruption
grep -n "I wasnted\|I waslked\|I wastched\|I wastch" MANUSCRIPT.md
```
Always use `\b` word boundaries in sed: `sed -i 's/\bI wanted\b/I wanted/g'` not `sed -i 's/I wa/I was/g'`.

**⚠️ Pitfall: Fix regressions from compilation layer.** In this session, fixes applied to `output/` HTML/PDF files or `manuscript_src/` chapter files did NOT propagate to the compiled `MANUSCRIPT.md`. The review would verify the source files were fixed, but the live manuscript still had the old errors. **Always verify changes in the final compiled `MANUSCRIPT.md`**, not just the source files. After any fix pass, re-compile and re-verify the compiled manuscript.

**⚠️ Pitfall: Name fix regressions from partial patterns.** When fixing name inconsistencies (e.g., "Patricia Chen" → "Patricia Okonkwo"), search for ALL variants including hyphenated, accented, and partial matches ("Zhào", "Varma", "Osei"). Use `grep -i` with multiple patterns and verify zero hits remain for ALL variants. After applying fixes, re-run the full name audit including cross-checking against the series bible.

**⚠️ Pitfall: read_file pipe characters leak into patch() calls.** When you read text from `read_file`, the output includes `LINE_NUM|CONTENT` formatting. If you copy text from a read_file result (including the `|` prefix) into a `patch()` old_string or new_string, those pipe characters end up in the actual file. **Always use `terminal` with `tail`/`head` to extract raw text for patch(), or use `cat >>` for end-of-file additions where old_string matching is not needed.**

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

3. **Use `patch` with `replace_all=true` for bulk replacements across large files** — safer than sed because patch has fuzzy matching and auto-runs syntax checks. For 400+ occurrences in a single file:
```
patch(mode='replace', path='MANUSCRIPT.md', old_string='OldName', new_string='NewName', replace_all=true)
```

Alternative: Use `terminal` with `sed` for very large replacement sets (>1000 occurrences) where patch may time out:
```bash
sed -i 's/OldName/NewName/g' path/to/MANUSCRIPT.md
```

4. **Verify both old AND new names** — confirm the old count is zero AND the new count is the expected total:
```bash
grep -c "OldName" MANUSCRIPT.md   # Should be 0
grep -c "NewName" MANUSCRIPT.md   # Should match expected total (e.g., 36 for "Elena Varga" in a full manuscript)
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

**Mars-colonization-specific placeholders** (copy-pasted across No Blue Sky books):
- "The drill bit sang into the regolith, a sound conducted through bone"
- "The regolith underfoot was finer than talc, sharper than shattered glass"
- "The equipment hummed softly in the background, a constant reminder"
- "The monitor flickered, casting blue light across the huddle of exhausted faces"
- "We've come too far to fail now... whatever it takes, whatever we have to sacrifice"
- "Every movement was deliberate, every check double-verified"
- "Drifted from technical to personal — a coping mechanism as old as exploration itself"
- "A cylinder of Martian history, layers visible even in the monochrome suit lighting"
- "Later that evening, back in the habitat's common module, the crew gathered"
- "They pressed their palm against the cool glass, feeling the vibration"
- "Sarah's hands were raw from gripping the same valve for three hours"
- "Every hour brought a new data point. Every data point brought a new question."
- "We have seventy-two hours... The water reclamation system is failing"
- "The silence of Mars pressed in — not empty, but full of questions"
- "Like assembling a puzzle with no reference image"

Search for all at once:

```bash
full_scan() {
  local file="$1"
  local count=0
  for phrase in \
    "patience and precision" "drill bit sang" "equipment hummed softly" \
    "monitor flickered" "too far to fail" "regolith underfoot" \
    "familiar pressure of the EVA gloves" "Sarah's hands were raw" \
    "puzzle with no edge pieces" "Self-Correction:" "Word count:"; do
    c=$(grep -ci "$phrase" "$file" 2>/dev/null || echo 0)
    [ "$c" -gt 0 ] && echo "  HIT ($c): $phrase" && count=$((count + c))
  done
  echo "Total placeholder hits: $count"
  [ "$count" -gt 0 ] && echo "WARNING: Placeholder content still present" || echo "CLEAN: No placeholder content detected"
}
full_scan MANUSCRIPT.md
```

Remove by rewriting affected paragraphs to be specific and concrete. For severe cases (>10 hits), see Type R (Complete Thematic Rewrite).

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

### Uniqueness Ratio Check (Post-Fix Validation)

After applying fixes, run a uniqueness ratio check to confirm placeholder content was replaced:

```bash
cd /path/to/book
total=$(wc -w < MANUSCRIPT.md)
unique=$(cat MANUSCRIPT.md | tr ' ' '\n' | sort -u | wc -l)
ratio=$(echo "scale=2; $unique * 100 / $total" | bc)
echo "Total: $total  Unique: $unique  Ratio: $ratio%"

# Expected: ratio > 30% for a healthy manuscript after fix
# If still < 20%, placeholder content remains
```

Also compare against the backup to confirm the fix reduced the total/unique ratio gap:

```bash
echo "=== Before ==="
total=$(wc -w < MANUSCRIPT.md.ITERATION1_BACKUP)
unique=$(cat MANUSCRIPT.md.ITERATION1_BACKUP | tr ' ' '\n' | sort -u | wc -l)
echo "Scale=2; $unique * 100 / $total" | bc

echo "=== After ==="
total=$(wc -w < MANUSCRIPT.md)
unique=$(cat MANUSCRIPT.md | tr ' ' '\n' | sort -u | wc -l)
echo "Scale=2; $unique * 100 / $total" | bc
```

The after ratio should be notably higher than the before ratio — ideally >2x.

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

### Subagent Timeout Configuration

The default subagent timeout is now **1800 seconds (30 minutes)** in three locations (patched from 600s/10 minutes):
- `tools/delegate_tool.py`: `DEFAULT_CHILD_TIMEOUT = 1800`
- `hermes_cli/config.py`: `delegation.child_timeout_seconds = 1800`
- `cli.py`: `delegation.child_timeout_seconds = 1800` in defaults

This allows large editorial fix tasks (expanding 20K+ words, converting HTML to markdown, trimming 15K+ words) to complete without timeout. For extremely large tasks (100K+ words), still consider the micro-goal delegation pattern described in `book-editorial-review` → Timeout Pitfall section.

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

### Type M: Missing Chapter Addition (e.g., Brand-New Chapter 1)

When a manuscript starts at Chapter 2 and needs a **new Chapter 1** written from scratch:

1. **Understand the series context first** — read the editorial review, Books I-II context, and the existing Chapter 2 to understand protagonist, setting, and established lore
2. **The new chapter must:**
   - Establish the protagonist (name, role, voice, physical description)
   - Set the series/colony context (reference Books I-II events like the Oxygen Gamble, mention Mission AI, ground the story in the setting)
   - Introduce the central hook (the anomalous signal, the alien threat, the crisis the book will follow)
   - Run ~1,200–1,700 words as a proper scene with sensory detail and dialogue
   - Include the image placeholder: `![](chapter_images/ch01.png)`
3. **Write to `manuscript_src/ch001.md`** (not chapters/) so the compile picks it up
4. **Add to the TOC** in MANUSCRIPT.md:
```
Chapter 1 -- The Edge of Silence| 3  
Chapter 2 -- Frequency Shift| 6  
```

### Type N: Image Placeholder Insertion (Markdown Manuscripts)

When a Markdown manuscript needs `![](chapter_images/chNN.png)` placeholders after each chapter header:

1. **Detect the existing chapter header format** — different books use different patterns:
   - `# Chapter 2 -- Frequency Shift` (single hash, em-dash) — NBS, AoLS, LF series
   - `## Chapter 1: Title` (double hash, colon) — CLLC series
   - `## Chapter One: Title` (worded numbers) — Tomorrow Remembered
2. **Add placeholders one chapter at a time** using `patch()` — target the unique `# Chapter N ...` header line:
```
patch(mode='replace', path='MANUSCRIPT.md', 
  old_string='# Chapter 4 -- Title',
  new_string='# Chapter 4 -- Title\n\n![](chapter_images/ch04.png)')
```
3. **For chapters 1-40, do them sequentially** — each patch is fast since the match is unique
4. **Skip chapters that don't exist in the body** — if Chapter 4 is in the TOC but missing from the body, don't add a placeholder for it
5. **Verify count**:
```bash
grep -c '!\[\](chapter_images/ch' MANUSCRIPT.md  # Should match number of body chapters
```

### Type O: TOC Formatting Consistency Fix

When the Table of Contents has mixed entry styles (some using ` -- `, others using `: `):
1. **Identify the inconsistent entries** — common pattern: Chapters 1-16 and 25-40 use em-dash, but Chapters 17-24 use colon
2. **Fix each inconsistent entry via `patch()`** — the TOC entries include page numbers so they're uniquely identifiable:
```
patch(mode='replace', path='MANUSCRIPT.md',
  old_string='Chapter 17: Sub-Quantum Parlay| 68',
  new_string='Chapter 17 — Sub-Quantum Parlay| 68')
```
3. **Also fix the chapter BODY headers** — they'll have the same inconsistency:
```
patch(mode='replace', path='MANUSCRIPT.md',
  old_string='# Chapter 17: Sub-Quantum Parlay',
  new_string='# Chapter 17 — Sub-Quantum Parlay')
```
4. **Verify**: `grep -c 'Chapter [0-9]*: ' MANUSCRIPT.md` should return 0

### Type P: Duplicate Back Matter Removal

When author bio or book list blocks appear multiple times at the end of a manuscript:

1. **Read the last 80 lines** of MANUSCRIPT.md to see the full end-matter structure
2. **Identify which block is the duplicate** — look for identical blocks (same bio, same book list) that appear serially
3. **Remove the duplicate using `patch()`** — include enough surrounding context to make the old_string unique. Anchor on separator text:
```bash
# Read the end to see the structure
tail -80 MANUSCRIPT.md
```

### Type R: Complete Thematic Rewrite (Severe Corruption)

When >50% of the manuscript is copy-pasted placeholder text from other books in the series (uniqueness ratio <15%), do NOT patch individual chapters. The approach is to discard all placeholder content and write a new manuscript from scratch.

**When to use (diagnosed via Phase 0):**
- Uniqueness ratio <15%
- 10+ known placeholder phrase matches
- Cross-book content leaks (alien plots, pandemic crises, wrong-character names)
- Chapters 1-19 are generic colonization scenes unrelated to the book's actual theme

**Process:**

1. **Backup first:** `cp MANUSCRIPT.md MANUSCRIPT.md.ITERATION1_BACKUP`

2. **Identify salvageable chapters:** Scan late chapters (typically 20-25) for strong original content that fits the actual book theme. Note those chapter numbers/titles to integrate into the new structure.

3. **Design a new chapter structure** around the book's actual theme. For a political/constitutional book:

```
PART 1: THE GATHERING STORM
  Ch 1-5:   Seeds of discontent, Earth ultimatum, delegates called, journey
PART 2: THE CONVENTION
  Ch 6-10:  Assembly opens, three factions present, stalemate
PART 3: CRISIS AND COMPROMISE
  Ch 11-15: External crisis forces unity, great debate, compromise framed
PART 4: THE CHARTER
  Ch 16-19: Vote, signing ceremony, new dawn, charter's first test
LEGACY
  Ch 20-23: Earth's response, foundations laid, a generation later, appendix
```

4. **Write the entire manuscript in one pass** using `write_file()` (NOT patch — patch cannot handle a complete rewrite). Each chapter should:
   - Have a Mission AI context line
   - Feature a character epigraph
   - Contain ~400-600 words of original content (dialogue, description, political drama)
   - Include the image placeholder after the chapter header: `![](chapter_images/chNN.png)`

5. **Salvage the best existing chapters** by renumbering and integrating them into the new structure. Fix character names in those chapters.

6. **Add front matter** in a single block before Chapter 1:
   - Title, author (verify correct name: Bob J Mills, not Bob Mills)
   - Copyright line with correct year and author
   - All rights reserved boilerplate
   - Disclaimer of fiction (names, places, incidents are fictional)
   - Complete TOC listing all chapters

7. **Add back matter** after the final chapter:
   - "## About the Author" with correct name
   - "## The No Blue Sky Series" listing all books
   - Appendix with key document text (e.g., the complete charter for a constitution book)

8. **Add image placeholders inline** — insert `![](chapter_images/chNN.png)` right after each `# Chapter N -- Title` header during writing. This is faster than adding them as a separate pass.

**Key technique: write_file() wins for complete rewrites**

For severely corrupted manuscripts, `write_file()` to write the ENTIRE manuscript at once is both faster and more reliable than patching individual chapters. The old content is so contaminated that nothing is worth saving except 3-5 late chapters.

```bash
# File size comparison confirms the rewrite
ls -la MANUSCRIPT.md*
wc -w MANUSCRIPT.md MANUSCRIPT.md.ITERATION1_BACKUP

# Old had more total words but fewer unique — that's the placeholder signature
```

**Verification after Type R:**
- Run Phase 0 diagnostic again — uniqueness ratio should now be >30%
- All placeholder phrase counts should be 0
- All cross-book leak counts should be 0
- Character names should be correct (Elena Varga, not Vargas)
- Image placeholder count should match chapter count (grep the `![](chapter_images/` pattern)
- Front matter and back matter should each be present once

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