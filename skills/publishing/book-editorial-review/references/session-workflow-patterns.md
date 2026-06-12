# Session Workflow Patterns (June 2026)

Practical patterns from a 6-book, 4-loop editorial session covering Cindy Lou Legal Capers, Lunar Foundation, No Blue Sky, Age of Lightships, Business Series, and Tomorrow Remembered.

## The Fix + Review Split

Never have subagents both fix AND review in one pass. Split the work:

- **Subagents do fixes only.** Delegate with `DO NOT write the review -- I'll handle that. Just make the edits.` in the goal. This conserves their ~50 tool calls for reading, analyzing, and applying changes.
- **Parent writes reviews.** After subagents complete, verify actual word counts (`wc -w`) and file contents. Subagents consistently OVER-REPORT results (e.g., claimed 63K words but actual was 44K -- a 19K gap). Writing reviews yourself catches these discrepancies.
- **Why this works:** Subagents hit the 50-call limit before timeouts. Review-writing burns calls that should go to content changes. The parent also catches structural issues (wrong file being edited, old manuscript being referenced, missing chapters) that subagents overlook.

## Batch-and-Reassess Pattern

For multi-book loops (5-6 books), batch rather than fixing everything at once:

1. **Batch 1 (3 books, parallel):** Delegate the 3 highest-impact or furthest-from-target books. Each subagent gets ONE book and one specific goal.
2. **Pause and verify:** After Batch 1 finishes (or times out), check actual word counts with `wc -w`. Do NOT trust subagent claims.
3. **Batch 2 (2-3 books, parallel):** Delegate remaining books. By now you know which Batch 1 books hit targets and which need follow-up.
4. **Final push:** Books within 100-1,000 words of target are best finished directly with `echo "paragraph..." >> MANUSCRIPT.md`, not a full subagent re-delegation. Subagents waste 5-10 calls just to read and orient.

## Incremental Improvement Across Loops (20-Book Scale)

When running the editorial loop across 20 books in 6 series, books rarely jump from C+/D to B+ in one pass. The typical trajectory:

```
D  →  C+  →  B-  →  B  →  B+  →  A-
^                               ^
First pass (blocker fix)      4-6 iterations later
```

### Large-Scale Loop Sequence

1. **Batch 1 — Critical fixes (3 parallel):** D/C+ books with structural blockers (template repetition, missing chapters, wrong genre). Fix the blocker, not the polish.
2. **Re-review Batch 1:** Did they hit their target? If not, what's the new blocker? Typically D→B- or C+→B is one pass.
3. **Batch 2 — Next tier (3 parallel):** B/B- books that need content expansion, plot threading, or consistency fixes.
4. **Re-review Batch 2:** Confirm new ratings. Some books may need a third pass.
5. **Batch 3 — Polish:** Books that hit B but need B+ — smaller fixes, targeted expansions.
6. **Final re-review:** All books. Confirm ratings, identify any that slipped back.

### Key Learnings from a 20-Book Loop

- **Timeouts are the norm for large manuscripts.** 4 of 13 subagent passes timed out at 600s. Expect 25-30% timeout rate on complex books.
- **Partial progress is still progress.** Timed-out subagents that made 28+ calls typically added 1-5K words. Check `wc -w` before re-deploying.
- **Re-review every time.** A book that was C+ may become B- after a fix pass. Don't assume — re-read and re-rate.
- **The 9-book trap.** After fixing the worst books (D→B+), you'll have ~9 books at B/B- that each need one more targeted pass. These are the hardest because they need individual attention, not structural overhauls.
- **Subagent granularity matters.** Complex 43-chapter template books need 2-3 subagent passes (differentiating chapters 1-15, then 16-30, then 31-43). One subagent can't fix 43 templated chapters in 50 calls.
- **Genre shift fix (D→B+ in one pass):** When a book is set on the wrong planet (Moon vs Mars), bulk sed replacements + rewriting the climax chapters can lift a D to B+ in a single subagent pass. The climax is the highest-leverage target.
- **Chapter structure fix (C→A- in one pass):** A book with ZERO chapter headers can go from C to A- by adding chapter divisions at scene breaks. The minimum structural fix transforms publishability.

## Large Restoration (Pre-Review Prerequisite)

When books have lost content (backup is 2-20× larger than current MANUSCRIPT.md):

1. **Snapshot first:** Copy all current MANUSCRIPT.md to `_archived/damaged_copies/YYYY-MM-DD/` before any restoration
2. **Restore from backup:** Use the best available source (.BEFORE_FRONT_BACK > .backup > .bak > HTML/EPUB extraction)
3. **html2text for HTML sources** — regex stripping leaves artifacts. `pip3 install html2text`
4. **Verify:** word count matches expected, 0 HTML artifacts, chapter images directory exists
5. **Then review:** Only start the editorial loop after restoration is confirmed

Books that lost content (NBS I-V, CLLC Bk1, LF Bk4) were each 6-22K when backup was 40-104K. Restoration is not optional — reviewing a truncated book wastes the pass.

Not all book types gain the same per-pass:

| Book Type | Words per Pass | Notes |
|-----------|---------------|-------|
| Cozy/Legal Mystery (25-40K start) | 5-10K | Chapter headers, B-plots, expanded scenes are high-impact, low-reading-cost |
| Sci-Fi Colonization Thriller (23-30K start) | 3-6K | Structural thread insertion + chapter expansion. 3-4x word count gap (80K target) needs 8-12 passes |
| Non-Fiction/Business (15-40K start) | 2-4K | Case studies, examples, takeaway boxes, build-pipeline fixes |
| Memoir (40-50K start) | 1-3K | Source material often exhausted. Limited by available user content |
| Space Opera (45-60K start) | 4-8K | New POV chapters, fleet politics scenes, character arcs |

## Tool Call Budget Management

Each subagent gets ~50 tool calls (configurable via max_iterations). Plan:

| Phase | Calls | Notes |
|-------|-------|-------|
| Read and analyze | 10-15 | Opening manuscripts, searching for patterns, checking word counts |
| Apply changes | 25-30 | write_file is more reliable than patch for bulk content (patch frequently fails on unmatched old_string) |
| Verification | 5-10 | grep checks, word count, spot-read changed sections |

If subagent hits 50 calls before reaching target: Accept partial progress. A subagent that added 5K words and threaded a plot line is a win. Write a review that acknowledges the progress and identifies the remaining gap. Do NOT re-delegate the same book in the same batch -- the new subagent will waste calls re-reading already-known content.

## Post-Timeout Verification

When a subagent times out at 600s, always check whether it accomplished anything:

```bash
# Check if word count changed
wc -w path/to/book/MANUSCRIPT.md

# Check for new files or backups
ls -la path/to/book/*backup* path/to/book/*bak*
find path/to/book/ -name "*.py" -newer path/to/book/book-review.md -type f 2>/dev/null
```

**Timeout signals:**
- 38+ calls before timeout: Likely added significant content. Accept as partial progress.
- 11-25 calls before timeout: Made some progress. Check what was modified before re-deploying.
- 10 or fewer calls before timeout: Likely did nothing useful. Re-deploy with tighter goal.

## Word Count Strategy

### The 65K Minimum Rule
When the user says "all books except novellas need a minimum of 65K," strategy:

| Current | Gap | Strategy |
|---------|-----|----------|
| 60-64K | ~150/chapter | Add dialogue lines to existing scenes. Fast. |
| 40-50K | ~500/chapter | Add B-plot, expand court/council scenes, add cozy texture |
| 25-35K | ~1500-2000/chapter | Major expansion. Plan 6-10 subagent passes. |
| Finishing (within 1K of target) | ~200-1000 total | Direct echo >> from parent. Faster than re-delegating. |

### Cutting vs. Expanding
- Books 10-15K over genre max but good content: Accept natural length. A great 90K book beats a mediocre 75K one.
- Books 25K+ over genre max: Must cut. Bloat is bloat.
- Books 40%+ under genre minimum: Must expand. Can't sell a novella as a novel.
- Books 15-30% under but strong structure: Deepen existing before adding new subplots.

## Series-Specific Fix Patterns

### Cindy Lou Legal Capers (Cozy-Legal Hybrid)
**To reach A-:**
- Add chapter headers (## Chapter N: Descriptive Subtitle) replacing scene breaks
- Move spoiler/flash-forward content to an epilogue
- Expand daily cozy texture (bakery visits, doorman interactions, neighborhood walks)
- Cut Bill Parker Jr. romance to professional-only if still lingering
- Fix duplicate chapter numbering (common after subagent merges)
- Clean NYYLA epilogue markdown format if artifacts appear (||## Epilogue: fix to ## Epilogue:)

**Genres:** Stephanie Plum + Grisham lite. Target: 60-75K (but 85-95K is acceptable for the hybrid format).

### Lunar Foundation (Sci-Fi Colonization Thriller)
**To reach A-:**
- Thread antagonist through ALL chapters, not just first half
- Add a VISIBLE antagonist-caused crisis (sabotaged equipment, recall order, blocked shipment)
- Create an irreversible choice the protagonist can't take back
- The crisis must CASCADE: each fix attempt reveals a worse underlying problem
- Expand each chapter to ~2,000+ words
- Add Cole POV chapter showing Earth-side legal strategy
- Replace placeholder transitions ("The work continued") with original content
- For severely broken books: Phase 1 = fix blocker, Phase 2 = fix structure, Phase 3 = fix volume

**Genres:** The Martian + Red Mars + Seveneves. Target: 80-110K (minimum 65K on user request).

### No Blue Sky (Martian Colonization Epic)
**To reach A:**
- Word count is the only gap -- all five books are structurally A- at 12-16K vs 90-120K target
- Each book needs 70-100K more words. Requires full chapter-by-chapter expansion.
- Strongest prose in the library. Political debates, declaration scenes, and character arcs are all A quality.
- Estimated: 4-8 weeks per book to reach 90K.

### Business/MIFECO Non-Fiction
**To reach A:**
- First-person founder voice with specific verifiable numbers (NOT consultant-speak)
- Each chapter opens with a personal failure story
- "The One Thing" takeaway boxes at chapter ends
- Part dividers for framework (Assess / Choose / Implement / Optimize)
- Front matter title must match public title
- Target: 40-60K words

### Age of Lightships (Space Opera)
**To reach A-:**
- Word count: expand to 80K+ from ~55-65K
- Add Sarah Chen flashback to pre-eruption Earth life
- Add hibernation-dream sequence for tonal variety
- Fill the Ch25-35 gap with fleet politics or character development
- Expand each chapter from ~1,000 to ~1,500 words

## Subagent Timeout Configuration

Subagents can hit two different timeout boundaries:

| Timeout | Config Key | Default | What It Controls | Symptom |
|---------|-----------|---------|------------------|---------|
| Session timeout | `delegation.child_timeout_seconds` | 600 | Total subagent session duration | "timed out after ...s with N call(s)" |
| Per-call timeout | `delegation.timeout_seconds` | varies | Single LLM API call duration | "stuck on a slow API call" — few calls made |

**Adjust:**
```bash
hermes config set delegation.child_timeout_seconds 1200
hermes config set delegation.timeout_seconds 1200
hermes config set delegation.max_iterations 100
```

**Model switching:** If 600s timeouts persist with single-digit calls, the provider is too slow for expansion. Switch delegation model:
```bash
hermes config set delegation.model "openai/gpt-4o-mini"
hermes config set delegation.provider "openrouter"
hermes config set delegation.api_mode chat_completions
```

Recommend `openai/gpt-4o-mini` (fast, reliable, cheap) or `anthropic/claude-sonnet-4` (best quality, most expensive) for expansion tasks.
