# Fix-Review Loop Methodology

## Overview

The fix-review loop is an iterative process: Review → Fix → Re-review → Repeat until target rating achieved.

## Core Principles

1. **Review First, Then Fix** — Never fix without a current review. The review identifies exactly what needs fixing.
2. **Verify in Compiled Manuscript** — Fixes applied to source files (`manuscript_src/`, `output/`) must be verified in the compiled `MANUSCRIPT.md`. The compilation layer often breaks propagation.
3. **One Book Per Subagent** — For complex fixes (>10K words change), delegate ONE book per subagent. Series-level delegation causes 600s timeouts.
4. **Write Reviews Yourself** — Subagents over-report results. After subagents complete, YOU verify actual word counts and file contents, then write the new review.
5. **Mechanical Fixes First, Structural Later** — Front/back matter, TOC, image placeholders, name fixes are fast and high-impact. Do them before structural rewrites.

## Subagent Delegation Pattern

```python
# GOOD: One book, specific goal
delegate_task(
    goal="Fix AoLS Book 1: insert Chapter 1, remove duplicate Ch7, fix names",
    toolsets=["terminal", "file"],
    context="Working directory: /mnt/usb_4tb/books/Age_of_Lightships_Series/Book_1_Sunward_Exodus/"
)

# BAD: Whole series, vague goal
delegate_task(
    goal="Fix all AoLS books to A-",
    toolsets=["terminal", "file"]
)
```

## Timeout Mitigation

| Problem | Solution |
|---------|----------|
| 600s timeout on large edits | Break into mechanical fixes (terminal) + targeted subagent |
| Subagent reads entire manuscript | Have subagent read ONLY the specific chapters needing changes |
| Subagent writes full review | Subagent does FIX ONLY; you write the review after verifying |

## Verification Checklist After Every Fix Pass

```bash
# 1. Word count
wc -w MANUSCRIPT.md

# 2. Chapter count & numbering
grep -c '^# Chapter ' MANUSCRIPT.md
grep '^# Chapter ' MANUSCRIPT.md | head -20

# 3. Name consistency
for name in "Elena Varga" "Elena Vargas" "Elena Chen"; do
  echo "$name: $(grep -c "$name" MANUSCRIPT.md)"
done

# 4. Front/back matter
grep -c "Copyright" MANUSCRIPT.md
grep -c "Also by Bob J Mills" MANUSCRIPT.md

# 5. Image placeholders
grep -c 'chapter_images/ch' MANUSCRIPT.md

# 6. Placeholder content
grep -ci "work required patience and precision" MANUSCRIPT.md

# 7. Duplicate chapters
grep -c '^# Chapter [0-9]*:' MANUSCRIPT.md  # Should match chapter count
```

## Rating Progression Guide

| Current | Target | Typical Fixes |
|---------|--------|---------------|
| C+ → B- | Add missing front/back matter, fix name consistency, add Ch1 |
| B- → B | Remove duplicate chapters, fix TOC, add image placeholders |
| B → B+ | Trim to page count, break template chapters, add hooks |
| B+ → A- | Consolidate POVs, deepen antagonist, elevate prose, perfect pacing |

## Session Tracking

Track each book's iteration:
```
Book: AoLS Bk1
Iteration 1: C+ (initial)
Iteration 2: B- (Ch1 added, names fixed, front/back added)
Iteration 3: ? (need: dedup Ch6/7, trim 15K, fix 2 names, reduce POV)
```

## Cross-Book Consistency Checks

After fixing one book, verify against series bible:
- Character names match across all books
- Author name is "Bob J Mills" everywhere
- Series events referenced correctly (Oxygen Gamble, Mercury Accord, etc.)
- TOC format consistent within series
- Image naming convention consistent

## When to Stop Iterating

A book is ready when:
- ✅ Rating ≥ A-
- ✅ All 11 checklist items PASS
- ✅ Page count 160-190
- ✅ No duplicate chapters, no placeholder content, no name errors
- ✅ Front/back matter complete
- ✅ Image placeholders present and files exist