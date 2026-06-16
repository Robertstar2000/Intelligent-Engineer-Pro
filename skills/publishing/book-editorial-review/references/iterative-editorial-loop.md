# Iterative Editorial Loop: Review → Fix → Re-review

## Overview
This documents the proven workflow for the 20-book improvement loop (3 iterations as of June 2026).

## Phase 1: Discovery & Inventory
```bash
# Find all manuscripts with word counts
find /mnt/usb_4tb/books -name "MANUSCRIPT.md" -not -path "*/KDP_PACKAGE/*" -not -path "*/_*" | while read f; do
  echo "$(wc -w < "$f")	$f"
done

# Check for backup files that may be larger (content loss detection)
find /mnt/usb_4tb/books \( -name "*.backup" -o -name "*.BEFORE_*" -o -name "*.bak" \) -not -path "*/_*" | while read f; do
  echo "$(wc -w < "$f")	$f"
done
```

## Phase 2: Parallel Review Delegation (Batch Size = 3)

### Delegation Pattern (MUST FOLLOW)
```python
delegate_task(
    toolsets=["terminal", "file"],
    tasks=[  # Max 3 concurrent
        {"goal": "Review all books in Series X using 12-point checklist...", "context": "..."},
        {"goal": "Review all books in Series Y...", "context": "..."},
        {"goal": "Review all books in Series Z...", "context": "..."}
    ]
)
```

### Critical Rules
- **One subagent per series** (not per book) — avoids file contention
- **REVIEW ONLY** — include: "DO NOT modify MANUSCRIPT.md. Only write book-review.md."
- **Rating scale enforcement** — verbatim in every delegation:
  ```
  Use EXACTLY: A / A- / B+ / B / B- / C+ / C / D / F
  Final line: **Rating: [LETTER]** — [Above/Below B+]
  ```
- **Timeout: 600s hard limit** — subagents consistently timeout at 600s despite 1800s config
- **Narrow goals for large books** — "Review Ch12-13" not "Review whole book"

### Fix + Review Split (Proven Most Reliable)
1. Subagents do ONLY fixes: "DO NOT write review — I'll handle that. Just make edits."
2. Parent verifies actual word counts: `wc -w path/to/*MANUSCRIPT*.md`
3. Parent writes reviews with accurate ratings

## Phase 3: Fix Delegation (Batch Size = 3)

### Delegation Pattern
```python
delegate_task(
    toolsets=["terminal", "file"],
    tasks=[
        {"goal": "Fix Book X per book-review.md: [specific P0 items]", "context": "..."},
        ...
    ]
)
```

### Fix Verification (MANDATORY)
```bash
# After each fix pass
wc -w Book_X/MANUSCRIPT.md                    # Did word count change?
grep -c "^## Chapter\|^# Chapter" Book_X/MANUSCRIPT.md  # Chapter count
grep "old-template-phrase" Book_X/MANUSCRIPT.md  # Template removal check
```

## Phase 4: Re-review & Re-rate

### Fresh Review Cycle
- Read updated MANUSCRIPT.md
- Write NEW book-review.md (replaces old)
- Use "**Fresh Rating:**" for iteration 1, "**Rating:**" for iteration 2+
- Include "## Changes Applied" section describing what was fixed
- Update Character Map, Series Character Map, Plot Map, Series Plot Map

## Tool Call Budget (Per Subagent)

| Phase | Calls | Strategy |
|---|---|---|
| Read & analyze | 10-15 | read_file + search_files + grep |
| Apply changes | 25-30 | write_file preferred over patch (patch fails on unmatched old_string) |
| Verify | 5-10 | wc -w, grep, spot-read |

## Per-Pass Expectations by Book Profile

| Book Type | Typical Start | Gain/Pass | Iterations to Target |
|---|---|---|---|
| Cozy/Legal Mystery | 25-40K | 5-10K | 4-8 |
| Sci-Fi Colonization | 23-30K | 3-6K | 10-16 |
| Non-Fiction/Business | 15-40K | 2-4K | 10-20 |

## Terminal-Based Alternatives (When Delegation Times Out)

For books >40K words where subagents timeout:

```bash
# Write expansion script
cat > expand_book.py << 'PYEOF'
# ... expansion logic ...
PYEOF
python3 expand_book.py

# Or append directly for final 200-1000 words
cat >> MANUSCRIPT.md << 'EOF'

## New Section

Content here.

**The One Thing**
Takeaway.
EOF
```

## Batch-and-Reassess Pattern (For 5-6 Books)

1. **Batch 1 (3 books):** Highest-impact / furthest-from-target
2. **Pause & verify:** Check actual `wc -w` — don't trust subagent claims
3. **Batch 2 (2-3 books):** Remaining books
4. **Final push:** Books within 500-1000 words → manual `cat >>`

## Common Pitfalls & Solutions

| Pitfall | Solution |
|---|---|
| Subagent over-reports (claimed 63K, actual 44K) | Parent writes reviews after verifying |
| Subagent destroys content (rebuild from wrong source) | "DO NOT rebuild from manuscript_src/ — use patch()" |
| Read_file pipe chars in patch() | Use `terminal` with `tail`/`head` for raw text |
| Duplicate chapter numbering after insert | Post-fix audit: `grep "^## Chapter" MANUSCRIPT.md` |
| Formulaic chapter template | Search for repeated opening patterns; rewrite |
| Subagent timeout at 600s | Use terminal scripts for large expansions |

## Post-Timeout Verification

```bash
wc -w Book_X/MANUSCRIPT.md
grep -c "^## Chapter\|^# Chapter" Book_X/MANUSCRIPT.md
find path -name '*.md' -newer <existing_file> -type f
```

## Rating Thresholds (User-Configurable)

| Target | Meaning | User Says |
|---|---|---|
| A | Published bestseller | "get this to A" |
| Above B (B+ or higher) | Publishable with minor polish | "work on all books B or less, repeat until above B" |
| B- | Structurally sound draft | "just make it readable" |

**Default target: Above B (B+ or higher)**

## Iteration Convention

| Field | Iteration 1 (Fresh) | Iteration 2+ (Re-review) |
|---|---|---|
| Heading | `**Fresh Rating:** B+` | `**Rating:** B+` |
| Iteration | `**Iteration:** 1` | `**Iteration:** 2` |
| Changes Applied | "Initial review — fresh assessment" | Specific fixes described |

## Quality Benchmark: Humanized Writing

**MANDATORY:** Before writing any manuscript content, load `humanizer` skill and apply 29 pattern checks + PERSONALITY AND SOUL section. No AI-isms, no filler, real voice, variable rhythm, opinions where they fit, first-person when honest.