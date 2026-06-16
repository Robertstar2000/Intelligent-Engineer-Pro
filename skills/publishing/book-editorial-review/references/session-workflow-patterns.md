# Session Workflow Patterns (June 2026) — Updated

## ⚠️ CRITICAL: Rewrite Weakest Chapters, Don't Expand (User Directive 2026-06-13)

**When books need massive expansion (22K → 50K), the correct approach is to REWRITE the weakest chapters from scratch, NOT to expand existing content.**

User's explicit instruction: "For the books that need massive expansion rewrite the weakest chapters rather then expand them use the writer skills and rules"

### Why Expansion Fails
- `content.replace()` corrupts files (overlapping matches)
- Paragraph-trimming destroys chapters (removes too much)
- Consolidation scripts lose content (wrong string boundaries)
- Even successful expansion only adds 4K words per pass — far short of 22K+ needed

### The Rewrite-First Workflow

1. **Identify weakest chapters** (under 800 words, summary-like, or structurally broken)
2. **Load genre benchmarks** from `references/genre-benchmarks.md`
3. **Load humanizer skill** and apply all 29 patterns
4. **Write 1,500-2,000 words of original content** per weak chapter:
   - Dramatized scenes (not summaries)
   - 2-3 sensory details per scene
   - Dialogue with subtext
   - Personal stakes (not abstract)
   - Genre-specific requirements
5. **Replace safely** using line-number-based extraction (see `references/rewrite-vs-expand-lessons.md`)

### Target Word Counts Per Rewritten Chapter
- **Faction debate chapters**: 2,000-2,500 words (dialogue-heavy, multiple perspectives)
- **Climax/vote chapters**: 2,000-2,500 words (sensory detail, emotional resonance, pacing)
- **Aftermath/epilogue chapters**: 1,500-2,000 words (reflection, earned emotion, future hooks)
- **Technical chapters** (economics, engineering): 1,500-2,000 words (show the work, add conflict)

### See Also
- `references/rewrite-vs-expand-lessons.md` — detailed safe/unsafe patterns
- `references/genre-benchmarks.md` — genre-specific requirements per chapter type

---

*[Previous content continues below]*

---

## Mandatory Maps for Every Review

Every book-review.md MUST include these maps — they are not optional:

### Character Map (Per Book)
| Canonical Name | Aliases/Nicknames | Role | First Appearance | Key Relationships | Voice/Persona Notes | Books Appearing In |

### Series Character Map (Per Series)
| Character | Book 1 | Book 2 | Book 3 | Book 4 |

### Plot Map (Per Book) — Fiction
| Chapter Range | Core Conflict | Stakes | Key Twist/Revelation | Cause→Effect Link to Next | Resolution Status |

### Series Plot Map (Per Series)
| Book | Core Conflict | Stakes Arc | Key Twists | How It Sets Up Next Book | Resolution |

### Framework Map (Per Book) — Non-Fiction
| Chapter Range | Core Thesis/Claim | Framework Element | Key Case Study | Actionable Takeaway | Reader Exercise/Tool | Cross-Chapter Link |

### Series Framework Map (Per Series)
| Book | Core Thesis | Framework Contribution | Key Frameworks Introduced | How It Builds on Previous | Reader Journey Position |

**These maps are the canonical references** — they prevent character drift, plot holes, and series inconsistencies. Update them every iteration.

---

## Subagent Timeout Reality Check

**The 600s timeout is a hard limit that DOES NOT respect config patches.**

| Config Attempted | Value | Actual Behavior |
|---|---|---|
| `delegation.child_timeout_seconds` | 1800 | Subagents still timeout at 600s |
| `delegation.timeout_seconds` | 1800 | No effect |
| Patched `delegate_tool.py`, `config.py`, `cli.py` | 1800 | Patch doesn't take effect |

**Operational Rule: Assume 600s is the hard cap.**
- Design ALL subagent tasks to complete within 300-400s
- Use narrow-goal delegation exclusively
- For tasks requiring more time, use terminal scripts directly
- Never delegate "review this whole book" for 40K+ word manuscripts

**Terminal-based alternative for large edits:**
```bash
python3 << 'PYEOF'
import re
with open('MANUSCRIPT.md', 'r') as f:
    content = f.read()
# ... processing ...
with open('MANUSCRIPT.md', 'w') as f:
    f.write(content)
PYEOF
```

## ⚠️ CRITICAL: Large File Editing — Avoid content.replace() on Full Manuscript

**Using Python's `content.replace()` on large manuscripts (40K+ words) can cause file corruption — truncation, content loss, or encoding issues.** This happened twice in one session with NBS BkIII (file dropped from 48K to 20K words).

**Safe alternatives:**
1. **Line-by-line processing:** Read lines, process line by line, write lines back
2. **Targeted patch() calls:** Use the `patch()` tool for specific find-and-replace operations
3. **Terminal sed/awk:** For simple replacements, use `terminal` with sed
4. **Write to separate file first:** Write new content to a temp file, verify, then copy over

## ⚡ Progressive Multi-Round Strategy — Concentric Circles Pattern (June 2026)

### Core Pattern

When running review→fix→review cycles across 5+ books, use **concentric circles**: start with ALL books, eliminate those that hit A/A- each round, narrowing focus as you go. Never carry settled books into the next round.

```
Round 1: 13 books → 6 hit A/A- → 7 continue
Round 2: 7 books → 4 hit A/A- → 3 continue
Round 3: 3 books → 1 hit A/A- → 2 continue
Round 4: 2 books → 1 hit A/A- → 1 continues
Round 5: 1 book  → hits A/A- → DONE
```

### Why This Works
- Avoids burning review cycles on books already at target
- Lets you focus deep on the small set of stubborn books
- Each round the fix subagents have fewer books to read and more focused goals
- Gives you data on which books are "fast fixes" vs "deep structural" issues

### Fast-Fix vs Stubborn Book Profiles

| Profile | Typical Rounds | Strategy |
|---------|---------------|----------|
| **Fast fixer** — clear P0/P1 issues, clear fix path (AoLS Bk 2-4, CLLC Bk 2-3) | 1-2 | Apply listed fixes, re-review, done |
| **Word-count deficient** — need expansion but structure is sound (NBS Bk I, Bk II) | 2-4 | Massive expansion pass, then character/pacing fix, then polish |
| **Structural stubborn** — B+ with fundamental structure problem (Mooncoming) | 4-5 | Each round addresses ONE structural dimension: connective tissue → tension arc → secondary cast → late-book crisis |
| **Rebuild needed** — missing content, blocks missing (NBS Bk V, started B-) | 2-3 | Write missing chapters first, then expansion, then polishing |

### When a Book is Stuck at B+ After 3+ Rounds

The single best technique for stubborn B+ books is the **micro-goal delegation**:

❌ **Broad goal that times out:** "Fix all structural issues in Mooncoming"
✅ **Micro-goal that completes:** "Add 2-3 tension-building sentences to each of 14 chapters in the post-crisis arc — specific, narrow, measurable"

Mooncoming was stuck at B+ through 4 rounds. What finally flipped it to A- in Round 5 was three micro-goals:
1. Develop 4 secondary characters with 2-3 lines each (Susan's father story, Dmitri's folk song, Yuki's deep-sea patient, Robert's grandfather's farm)
2. Build a sabotage thread through Ch 35-39 (MAINT-07 ghost account, firmware backdoor, unidentified mole)
3. Humanize all additions

Each micro-goal completed cleanly in 300-600s. The broad "fix the book" goal timed out at 1200s every time.

### Micro-Goal Templates for Stubborn Books

| B+ Issue | Micro-Goal | Expected Words | Calls |
|----------|-----------|---------------|-------|
| "Episodic chapters lack connective tissue" | Add 1-2 sentences end of each vignette chapter tying to main crisis | ~200-400 | 20-30 |
| "Secondary cast is flat" | Give 3-4 supporting characters 2-3 lines of personal backstory/motivation | ~500-800 | 12-18 |
| "Post-climax chapters plateau" | Thread a rising tension subplot through the post-crisis arc (mole, sabotage, political threat) | ~1,500-3,000 | 25-40 |
| "No antagonist" | Create an opposing character with 4+ scenes across the book arguing against the protagonist | ~2,000-3,000 | 30-45 |
| "Early chapters are slow" | Expand chapters 1-3 with hook, tension, character interiority | ~1,000-2,000 | 15-25 |
| "Ending feels rushed" | Expand final 2-3 chapters with aftermath, emotional beats, future hook | ~1,500-2,500 | 20-30 |

### The 3-Book Bottleneck Pattern

After 2-3 rounds of a large multi-book loop, you'll typically have **2-3 books stubbornly at B+**. This is not random — these are books with fundamental structural issues that broad fixes can't address. Common patterns:

- **Mooncoming (this session):** Episodic structure disguised as a thriller. 72% of chapters were slice-of-life vignettes with no narrative drive. Needed round-by-round structural surgery.
- **No Blue Sky Bk I (this session):** Time-jump structure between First Gen (vivid) and Present Day (abstract). Needed a bridging chapter and antagonist injection.
- **Red Charter (this session):** Founding narrative with no opposition. Needed a Charter opponent faction with scenes.

**Key insight:** These 2-3 book are the bottleneck for the entire pipeline. Don't try to parallel-process them. Give each its own round with progressively narrower micro-goals.

### Partial Progress from Timeouts = Real Progress

Subagents that time out at 600-1200s with 36-58 calls completed often save significant work:

| Timeout Stats | What Was Saved |
|--------------|----------------|
| 58 calls, 1200s timeout (NBS batch) | +22,000 words across 5 books |
| 36 calls, 1200s timeout (LF batch 1) | Cole connective tissue added, duplicate Thank You removed |
| 44 calls, 1200s timeout (NBS batch 2) | +6,525 Bk I, +5,607 Bk II, +6,927 Bk V |

**Rule:** If a subagent made 30+ calls before timeout, accept the partial progress and re-review. Do NOT retry the same task — the subagent already used its calls. Move to re-review, identify remaining gaps, and do a narrower fix pass.

**Check after timeout:**
```bash
wc -w path/to/book/MANUSCRIPT.md           # Did word count change?
ls -la path/to/book/MANUSCRIPT.md.BEFORE_FIX  # Backup exists?
```

### Word Count Profile Strategy

Different word-count bands need fundamentally different fix approaches — don't use the same strategy for a 27K book as a 72K book:

| Band | Books | Fix Strategy |
|------|-------|-------------|
| **25-35K** (very short) | NBS Bk I (27K→44K), Bk II (25K→31K) | 1. Add antagonist (gives structure) 2. Deepen existing chapters (sensory detail, dialogue) 3. Add bridging/connective chapters 4. Expand Part II/Present Day timeline |
| **45-55K** (medium) | AoLS Bk 3 (53K), LF Bk 3 (44K→47K) | 1. Specific targeted fixes (name overload, character interiority) 2. Expand weak chapters 3. Add emotional beats |
| **65K+** (long enough) | Mooncoming (72K→78K), Red Charter (64K→68K) | 1. Don't touch word count 2. Fix structural issues (tension arc, pacing, antagonist) 3. Add secondary cast depth 4. Build late-book crisis |

### The Concentric Elimination Workflow

```text
PHASE 1 — Survey all books, get current ratings
PHASE 2 — Launch parallel fix subagents (3 per batch, one series each)
PHASE 3 — Re-review all fixed books, get new ratings
PHASE 4 — Eliminate books that hit A/A-, keep only remaining
PHASE 5 — Repeat until all books at A/A-
```

Each phase eliminates books. The total work shrinks each round, letting you focus more on each remaining book.

---

## Chapter Header Format Detection

**Always verify chapter header format before running grep analysis.** Different books use different formats:
- `## Chapter N: Title` (H2 with colon)
- `# Chapter N — Title` (H1 with em-dash)
- `# Chapter N -- Title` (H1 with double-dash)
- `## Chapter N -- Title` (H2 with double-dash)

**Detection command:**
```bash
grep -n "^#" MANUSCRIPT.md | head -30
```

**Why this matters:** The regex `^## Chapter \d+:` only matches one format. If chapters use `# Chapter N —` (H1), the regex won't match and the script will silently fail.

## Chapter Consolidation Strategy (User Preference)

**When the user says "consolidate chapters":** Instead of expanding every chapter, merge short adjacent chapters into longer ones. This produces fewer, longer chapters that are more readable and easier to expand.

**How to consolidate:**
1. Identify chapters under 1,000 words
2. Merge 2-3 short chapters into one longer chapter
3. Add transition text between merged sections
4. Renumber subsequent chapters
5. Update TOC to match

**Target:** ~20 chapters at 2,000-2,500 words each = 40K-50K words total

## Expansion Script Pattern

For adding content to chapters via terminal Python scripts:

1. Read original file
2. Parse into chapters using regex
3. For each chapter, find insertion point (after image line + first paragraph)
4. Insert expansion text at that position
5. Write to new file first, verify word count, then copy over

**Critical:** Always write to a temp file first, verify the output, then replace the original. Never write directly to the source file in the same script that reads it.

**Insertion point detection:**
```python
img_match = re.search(r'!\[\]\(chapter_images/ch\d+\.png\)', chunk)
if img_match:
    after_img = chunk[img_match.end():]
    para_end = after_img.find('\n\n')
    if para_end >= 0:
        insert_pos = img_match.end() + para_end + 2
        # Insert at insert_pos
```

**Warning:** If the chapter doesn't have an image line, the insertion will silently fail. Always verify the insertion actually happened by checking the output file.

## NBS Series-Specific Patterns

**No Blue Sky Books IV and V** are severely underlength (22-24K words each) and need massive expansion to reach novel length (50K+). These books have:
- Coherent three-act structures
- Good prose quality
- Short chapters (500-1,000 words each)
- No major structural issues

**Recommended approach:** Write expansion scripts that add 500-1,000 words per chapter through dialogue, sensory detail, and internal monologue. Target 23 chapters × 2,000 words = 46K words.

**NBS Book V specific issues:**
- Duplicate chapters (Ch 21 = Ch 2, Ch 20 = Ch 23)
- Ch 2 and Ch 3 overlap (same interviews)
- Truncated text mid-sentence
- No named antagonist
- Population inconsistency (387 vs 412)

**Fix order for NBS BkV:** Remove duplicates → Fix truncated text → Standardize population → Add antagonist → Expand remaining chapters

---

*[Previous content from session-workflow-patterns.md follows below — all existing patterns, tables, and guidance remain valid]*

## ⚠️ CRITICAL: Subagent Parallel Review — File Contention (2026-06-12)

**When delegating multiple subagents in parallel to review books in the SAME series, each subagent may overwrite the other's book-review.md file** if they share a parent directory, OR subagents reading cross-book data (e.g., Book 2 reading Book 1's ending for series flow) may encounter files modified by sibling subagents.

**Symptoms:** Subagent reports: "subagent modified files the parent previously re-read before editing: /path/to/book-review.md."

**Prevention:**
- **One subagent per series** for reviews (not per book) — each subagent writes all book-review.md files in its assigned series
- **Never delegate subagents to review books in the same series in parallel** — they will read each other's MANUSCRIPT.md files mid-edit if any fix work is happening simultaneously
- **For reviews-only passes**, parallel by series is safe (different directories)

---

## ⚠️ CRITICAL: Trim Scripts Can Destroy Manuscripts (2026-06-12)

**A Python trim script with incorrect regex chapter-boundary detection truncated NBS BkIV from 53,720 words to 3,933 words.** The regex `rf'\n# Chapter {ch_num} -- '` failed to find chapter boundaries (no leading newline on some headings), causing the script to write a nearly empty file.

**Root cause:** Assuming `^# Chapter` patterns always have a leading `\n` before them. Some chapters start at position 0 of the file or after a different separator.

**Prevention — ALWAYS:**
---

## ⚠️ Large File Editing — Avoid content.replace() on Full Manuscript

**Using Python's `content.replace()` on large manuscripts (40K+ words) causes file corruption — truncation, content loss, or encoding issues.**

### Safe Alternatives
1. **Line-by-line processing:** Read lines, process line by line, write lines back
2. **Targeted patch() calls:** Use the `patch()` tool for specific find-and-replace
3. **Terminal sed/awk:** For simple replacements, use `terminal` with sed
4. **Write to separate file first:** Write new content to temp file, verify, then copy over

---

## Subagent Parallel Review — File Contention

**When delegating multiple subagents in parallel to review books in the SAME series, each subagent may overwrite the other's book-review.md file if they share a parent directory.**

### Prevention
- **One subagent per series** for reviews (not per book) — each subagent writes all book-review.md files in its assigned series
- **Never delegate subagents to review books in the same series in parallel** — they will read each other's MANUSCRIPT.md files mid-edit if any fix work is happening simultaneously
- **For reviews-only passes**, parallel by series is safe (different directories)

---

## Rating Scale Enforcement (Every Delegation)

**Review subagents used wildly different rating scales:**
- Some: A-/B+/B/C+ letter grades (correct)
- Some: ★★★★☆ star ratings
- Some: 3.3/5.0 or 7.5/10 numeric scales
- Some: No rating at all

**Prevention:** In EVERY delegation goal, explicitly specify:
```
Use EXACTLY this scale: A / A- / B+ / B / B- / C+ / C / D / F
The final line MUST read: **Rating: [LETTER]** — [Above/Below B+].
Do NOT use star ratings, numeric scores, or any other scale.
```

---

## max_concurrent_children=3 Limit

**Delegating 4+ tasks in a single delegate_task() call FAILS with:** `Too many tasks: 4 provided, but max_concurrent_children is 3.`

**Prevention:**
- Maximum 3 tasks per delegate_task() call
- For 4+ books, use 2+ delegate_task() calls: first 3 books, then remaining
- Series with 4 books (AoLS, LF): delegate 3 books first, then book 4 separately OR put all 4 in one subagent
- Most reliable: **one subagent per series** with all books in its goal, NOT one subagent per book across series

---

## Fresh-Review-Only Delegation (Distinct from Fix-Review Loop)

When the user asks for a FRESH review pass across all books (not a fix loop), separate the concerns:

**Review-only delegation** (`Phase 2` in the workflow):
- Delegate ONE subagent per series, not per book — each subagent reads 3-5 books and writes individual book-review.md files
- Set toolsets to `["terminal", "file"]` — no browser, no web needed
- Include genre benchmarks from `references/genre-benchmarks.md` in the context
- Include the 11-point checklist items
- Include prior ratings for reference but stress "FRESH assessment — ignore previous"
- Each book gets its own P0/P1/P2 plan specific to that book

**Optimal batch for 20 books across 6 series:**
- Batch 1 (3 parallel): 3 largest series (AoLS 4 + LF 4 + NBS 5 = 13 books)
- Batch 2 (3 parallel): Remaining 3 series (CLLC 3 + Business 3 + Memoir 1 = 7 books)
- Total: ~8-10 minutes wall clock time for all 20 fresh reviews

## The Fix + Review Split

Never have subagents both fix AND review in one pass. Split the work:

- **Subagents do fixes only.** Delegate with `DO NOT write the review -- I'll handle that. Just make the edits.` in the goal.
- **Parent writes reviews.** After subagents complete, verify actual word counts (`wc -w`) and file contents. Subagents consistently OVER-REPORT results.
- **Why this works:** Subagents hit the 50-call limit before timeouts. Review-writing burns calls that should go to content changes.

## Batch-and-Reassess Pattern

For multi-book loops (5-6 books), batch rather than fixing everything at once:

1. **Batch 1 (3 books, parallel):** Delegate the 3 highest-impact or furthest-from-target books.
2. **Pause and verify:** After Batch 1 finishes (or times out), check actual word counts with `wc -w`.
3. **Batch 2 (2-3 books, parallel):** Delegate remaining books.
4. **Final push:** Books within 100-1,000 words of target are best finished directly with `echo "paragraph..." >> MANUSCRIPT.md`.

## Incremental Improvement Across Loops (20-Book Scale)

Typical trajectory: D → C+ → B- → B → B+ → A-

Key learnings:
- **Timeouts are the norm.** Expect 25-30% timeout rate on complex books.
- **Partial progress is still progress.** Timed-out subagents that made 28+ calls typically added 1-5K words.
- **Re-review every time.** A book that was C+ may become B- after a fix pass.
- **The 9-book trap.** After fixing the worst books, ~9 books at B/B- each need one more targeted pass.

## Narrow-Goal Delegation (Timeout Avoidance)

| Broad Goal | Narrow Goal | Expected Calls | Timeout Risk |
|---|---|---|---|
| "Expand to 40K words" | "Add 200 words to each of 23 chapters" | ~28-35 | Low |
| "Fix all structural issues" | "Fix the TOC formatting and add image placeholders" | ~12-18 | Very low |
| "Rewrite all 43 template chapters" | "Differentiate chapters 1-15" | ~38-45 | Medium |
| "Trim 37K words" | "Cut the 3 longest chapters by 1K each" | ~15-20 | Very low |

## Post-Timeout Verification

```bash
wc -w path/to/book/MANUSCRIPT.md
ls -la path/to/book/*backup* path/to/book/*bak*
```

- 38+ calls before timeout: Likely added significant content. Accept as partial progress.
- 11-25 calls: Made some progress. Check what was modified.
- 10 or fewer: Likely did nothing useful. Re-deploy with tighter goal.

## Word Count Strategy

| Current | Gap | Strategy |
|---------|-----|----------|
| 60-64K | ~150/chapter | Add dialogue lines to existing scenes. |
| 40-50K | ~500/chapter | Add B-plot, expand scenes, add texture |
| 25-35K | ~1500-2000/chapter | Major expansion. Plan 6-10 passes. |
| Finishing (within 1K) | ~200-1000 total | Direct echo >> from parent. |

## Series-Specific Fix Patterns

### No Blue Sky (Martian Colonization Epic)
- Word count is the primary gap — books are 22-48K vs 50K+ target
- Books IV and V (22-24K each) need massive expansion
- **Chapter consolidation approach:** Merge short chapters (under 1K words) into longer ones, then expand each consolidated chapter to 2,000-2,500 words
- Target: ~20 chapters × 2,500 words = 50K words per book

### Cindy Lou Legal Capers (Cozy-Legal Hybrid)
- Target: 60-75K (but 85-95K acceptable for hybrid format)
- Add chapter headers, expand cozy texture, fix duplicate chapter numbering

### Lunar Foundation (Sci-Fi Colonization Thriller)
- Target: 80-110K (minimum 65K)
- Thread antagonist through ALL chapters, add visible crisis, create irreversible choice

### Business/MIFECO Non-Fiction
- Target: 40-60K words
- First-person founder voice, "The One Thing" takeaway boxes, part dividers

### Age of Lightships (Space Opera)
- Target: 80K+ from ~55-65K
- Add POV chapters, fleet politics scenes, character arcs

## Subagent Timeout Configuration

| Timeout | Config Key | Default | What It Controls |
|---------|-----------|---------|------------------|
| Session timeout | `delegation.child_timeout_seconds` | 600 | Total subagent session duration |
| Per-call timeout | `delegation.timeout_seconds` | varies | Single LLM API call duration |

**Note:** Patching these values may not take effect without a Hermes restart. Assume 600s is the effective cap.

---

## ⚡ Fix + Review Split Pattern (Mandatory)

**Never have subagents both fix AND review in one pass.**

### Why This Works
- Subagents hit 50-call limit before timeouts; review-writing burns calls needed for content changes
- Subagents consistently OVER-REPORT results (claimed 63K words, actual 44K — 19K gap)
- Writing reviews yourself catches inflated claims and structural issues

### Implementation
1. **Subagents do fixes only.** Delegation goal includes: `"DO NOT write the review — I'll handle that. Just make the edits."`
2. **Parent writes reviews.** After subagents complete, verify actual word counts (`wc -w`) and file contents.
3. **Subagents use toolsets `["terminal", "file"]`** — no browser, web, or other tools needed for fixes.

### Review Delegation Template
```text
Perform a fresh editorial review (Iteration N) of [Book Title] after fixes applied.
Read the full MANUSCRIPT.md, evaluate against all 13 checklist criteria, and write a NEW book-review.md with iteration=N.

CRITICAL: Do NOT modify MANUSCRIPT.md. Only write book-review.md. Use terminal and file tools only.

RATING SCALE ENFORCEMENT — use EXACTLY: A / A- / B+ / B / B- / C+ / C / D / F
The final line MUST read: **Rating: [LETTER]** — [Above/Below B+].
```

### Phase 1: Discovery & Inventory

```bash
# Find all manuscripts with word counts
find /mnt/usb_4tb/books -name "MANUSCRIPT.md" -not -path "*/_*" -not -path "*/KDP_Packages/*" -exec wc -w {} \;

# Find all existing reviews
find /mnt/usb_4tb/books -name "book-review.md" -not -path "*/_*" -not -path "*/KDP_Packages/*"
```

### Phase 2: Batch Fresh Reviews (by Series)
- Max 3 subagents parallel (one per series)
- Each subagent reads ALL books in its series
- Writes individual book-review.md per book
- Uses A/A-/B+/B/B-/C+/C/D/F scale with explicit "Rating: X — Above/Below B+" line

### Phase 3: Analyze Results & Prioritize Fixes
- Collect P0/P1 issues from all reviews
- Group by fix type (global find-replace, structural, mechanical)
- Create fix batches by series

### Phase 4: Apply P0/P1 Fixes (Mechanical First)
- Global sed/perl for numbers, star names, pronoun fixes
- Python for complex restructuring (moving sections, removing duplicates)
- Terminal `echo >>` for end-of-file additions (epilogues, hooks)
- ALWAYS create `MANUSCRIPT.md.PRE_FIXES` backup first

### Phase 5: Re-review Fixed Books (Iteration 2)
- Fresh reviews of only the fixed books
- Verify P0 issues resolved
- Rate against target (B+ or A-)

### Key Commands That Worked

**Global number/word replacement (Book 1 AoLS colonist counts):**
```bash
sed -i 's/580,000\\|580000/17,980/g' MANUSCRIPT.md
sed -i 's/600,000\\|600000/17,980/g' MANUSCRIPT.md
sed -i 's/12,180/17,980/g' MANUSCRIPT.md
sed -i 's/18,900/17,980/g' MANUSCRIPT.md
```

**Destination star fix:**
```bash
sed -i 's/Tau Ceti.*/Proxima Centauri/g' MANUSCRIPT.md
sed -i 's/Epsilon Eridani/Proxima Centauri/g' MANUSCRIPT.md
sed -i 's/Lacaille 9352/Proxima Centauri/g' MANUSCRIPT.md
```

**Convert HTML comment image refs to markdown:**
```bash
sed -i 's/<!-- IMAGE: \\(chapter_images\\/ch[0-9]*\\.png\\) -->/![](\\1)/g' MANUSCRIPT.md
```

**Remove duplicate patterns (Tomorrow Remembered Bridge summaries):**
```bash
python3 -c "
import re
with open('MANUSCRIPT.md') as f: content = f.read()
content = re.sub(r'\\s*\\*End of Chapter \\d+ — Bridge: [^*]+\\*\\s*\\n', '\\n', content)
with open('MANUSCRIPT.md', 'w') as f: f.write(content)
"
```

**Move section between Part I and Part II:**
```bash
python3 -c "
import re
with open('MANUSCRIPT.md') as f: content = f.read()
# Extract section, remove from end, insert before Part II
# ... see full script in session transcript
"
```

**Add epilogue/hook at end of manuscript:**
```bash
cat >> MANUSCRIPT.md << 'EOF'

## Epilogue: The Anomaly

[Content here]

EOF
```

### Pitfalls to Avoid

1. **Subagent timeouts at 600s** — Use terminal scripts for large global edits instead of delegation
2. **patch() fails with multiple matches** — Use sed/perl for global replacements, patch() only for unique context
3. **Book-review.md overwrites in parallel** — One subagent per series, not per book
4. **Missing chapter images = P0 blocker** — Always verify `grep -c "chapter_images" MANUSCRIPT.md` matches chapter count
5. **Character name drift across series** — Track 3 recurring chars per book AND across series
6. **Empty TOC = P0** — Always verify TOC has entries matching chapter count

### Series-Specific Fix Notes (This Session)

**Age of Lightships Book 1:**
- Colonist count: 58 ships × 310 = 17,980 (eliminated 600K, 580K, 12,180, 18,900 variants)
- Destination: Proxima Centauri b only (removed Tau Ceti, Epsilon Eridani, Lacaille 9352)
- Added Epilogue with prime-number signal from Proxima direction (Book 2 hook)

**No Blue Sky Book I:**
- 29 HTML comment image refs → markdown format
- "Bob N." → "Bob J Mills" in back matter
- Removed 29 "End of Chapter — Bridge" summaries
- Moved "The Years Between" between Part I and Part II
- Removed duplicate "Also by" section with wrong titles

**Tomorrow Remembered:**
- 8+ "they" → "we" pronoun fixes
- Katie/Robbie → Heather/Bobby
- 6 broken sentences at image transitions rejoined
- Duplicate Acknowledgments removed, Part Two heading standardized

**Cindy Lou Legal Capers (3 books):**
- Book 1: 30 image refs added, Acknowledgments added
- Book 2: 28 descriptive chapter titles added, Acknowledgments added
- Book 3: TOC populated (24 entries), 24 image refs added
