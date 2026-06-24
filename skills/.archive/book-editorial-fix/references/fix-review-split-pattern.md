# Fix + Review Split Pattern

## Problem
The old approach had subagents do BOTH the fix AND write the new review. This failed because:
- Subagents ran out of tool calls on the review (50-call limit)
- Subagents over-reported results (claimed 63K words, actual was 44K — 19K gap)
- Subagents hit timeouts before finishing the review
- Structural issues (wrong file, old manuscript, missing chapters) were missed

## Solution: Fix + Review Split

**Subagent does:** ONLY the fix work (reading, analyzing, applying changes)
**Parent does:** Verification + writing the new book-review.md

### Delegation Goal Template
```
DO NOT write the review — I'll handle that. Just make the actual edits to the manuscript file.

[Specific fix instructions from the review]
```

### Workflow
1. Delegate fix-only subagents (no review-writing in their goal)
2. Subagents use all 50 tool calls on reading, analyzing, and applying changes
3. After all complete, verify actual word counts: `wc -w path/to/book/*MANUSCRIPT*.md`
4. Read key sections to confirm changes were applied
5. Write the new book-review.md yourself with accurate ratings

### Why This Works Better
- Subagents consistently OVER-REPORT their results. One subagent claimed 63,430 words but actual was 44,491 — a 19K-word gap. The fixes were real but the quantity was inflated.
- Subagents hit the 50-call tool limit before timeouts. Giving them review-writing work burns calls that should go to content changes.
- Writing reviews yourself also catches structural issues (wrong file, old manuscript, missing chapters) that the subagent may have overlooked.

### When NOT to Use This Pattern
- Simple one-pass fixes where the fix is trivial and verification is easy
- When the subagent is already writing a review and has capacity
- One-off tasks where the overhead isn't justified

### Verification Checklist (Parent Must Do)
- [ ] `wc -w` on all MANUSCRIPT.md files matches expected
- [ ] `grep -c "chapter_images"` matches chapter count
- [ ] Front matter (copyright, TOC) present
- [ ] Back matter (Also by, About Author) present
- [ ] Name consistency: `grep` for old names returns 0
- [ ] No HTML tags in manuscript: `grep -c '<[a-z]'` returns 0
- [ ] Chapter numbering is sequential
- [ ] No duplicate chapters or sections