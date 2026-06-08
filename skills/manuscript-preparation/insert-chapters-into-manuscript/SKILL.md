---
name: insert-chapters-into-manuscript
displayName: Insert Chapters into Manuscript
description: Insert pre-written standalone chapter files into a partially-complete fiction manuscript at the correct structural position, handling placeholder/outline-only chapters, part boundaries, and heading hierarchy conventions.
---


## 🔍 MemPalace Query (MANDATORY FIRST STEP)
Before proceeding, query MemPalace for existing context:
```python
import sys, os; sys.path.insert(0, os.path.expanduser('~/.hermes/mempalace'))
import embed; embed.init_embedding(os.path.expanduser('~/.hermes/mempalace'))
results = embed.search_embeddings("insert chapters manuscript fiction standalone", k=5)
```
This retrieves previous decisions, domain-specific context, and lessons learned from the vector memory store.

## When to Use This Skill

Use this skill when:
- You have a main manuscript with some chapters written and others existing only as outlines/placeholders
- Standalone chapter files (`Chapter_XX_Title.md`) have been written and need to be merged into the main manuscript
- Chapters were written out of order and need inserting at specific structural positions
- The manuscript has a part/chapter heading hierarchy (e.g., `# PART II — TITLE` with `## Chapter N – Title`)
- You need to insert multiple chapters in one pass and maintain structural consistency

## Workflow Steps

### 1. Survey the Manuscript Structure

Read the main manuscript to understand:
- **Heading hierarchy**: What level are part headings (`#` or `##`)? What level are chapter headings?
- **Part boundaries**: Where does the current content end? Which part should the new chapters go into?
- **Placeholder chapters**: Are there chapters that exist as outlines but not full prose? Where are they located?
- **Formatting conventions**: Chapter numbers (Arabic vs. Roman numerals), title separators (`—` vs `:` vs `–`), end markers (`*End of Chapter X*` style)

```bash
# Quick heading structure check
grep -n '^#' /path/to/manuscript.md
```

### 2. Read the Source Chapter Files

Read each chapter file to be inserted:
```bash
# Read the files with read_file (preferred) or terminal
```

### 3. Choose the Insertion Strategy

Three common patterns:

**Pattern A: Append after last completed chapter** (most common)
The manuscript has Chapters 1-8 complete. Chapters 9-10 exist as outlines. Chapters 11 and 14 are ready. Insert after Chapter 8:

```python
# Insert after the "End of Chapter X" marker, before the placeholder section
insertion_point = manuscript.find("*End of Chapter 8 — Bridge:*")
if insertion_point >= 0:
    # Find the end of this line
    line_end = manuscript.find("\n", insertion_point)
    insertion_point = line_end  # Insert AFTER the end-of-chapter marker
```

**Pattern B: Insert between existing placeholder markers**
Placeholder comments already exist showing where outlines should go. Insert the chapter file content between or replacing the placeholders.

**Pattern C: Insert into a specific part with renumbering**
If chapters need renumbering, use `re.sub` with sequential renumbering. Note: this is uncommon for fiction; renumbering is covered by `publishing-workflow` §3E for non-fiction.

### 4. Preserve Part Headings

When chapters belong to a new part (e.g., Part II — WATER, AIR, AND GROUND that hasn't been written into the manuscript yet):

```markdown
---
# PART II — WATER, AIR, AND GROUND
---
```

- Match the existing part heading style (e.g., `# PART X — TITLE` with em-dash)
- Add the standard separator (`---`) before and after
- Use the same heading level as existing part headings (typically `#` H1 for parts)

### 5. Match Heading Conventions

**Critical**: Chapter headings in the manuscript MUST match the existing convention. Check the level used by existing chapters:

```python
# Check heading level — manuscript may use ## (H2) not # (H1)
header_pattern = re.compile(r'^#{1,3} Chapter', re.MULTILINE)
# Returns e.g. '##' if all chapters use H2
```

Common fiction conventions:
- Part headings: `# PART I — TITLE` (H1)
- Chapter headings: `## Chapter N — Title` (H2) — most common for fiction
- Title separator: `—` (em dash), `:` (colon), or `–` (en dash)

### 6. Add Placeholder Markers

For chapters that exist as outlines but haven't been written yet, add clear HTML comment markers:

```markdown
<!-- ============================================================ -->
<!-- SECTION: Chapters 9 & 10                                    -->
<!-- ============================================================ -->
<!--                                                              -->
<!-- Chapters 9 and 10 currently exist as outlines (not full      -->
<!-- prose). Insert them here when written.                       -->
<!--                                                              -->
<!-- ============================================================ -->
```

This makes it obvious where missing chapters go without breaking the markdown rendering.

### 7. Insert Chapter Content

For each chapter file:

1. **Read the chapter heading** — the file may start with `# Chapter N – Title` but the manuscript uses `##`. Adjust level.
2. **Insert the full prose** with appropriate heading level
3. **Add the end marker** — match the existing convention (`*End of Chapter X*` or `*End of Chapter X — Bridge: ...*`)
4. **Add separators** — use `---` between chapters

```python
new_section = f"""
---

## Chapter {num} – {title}

{content}

*End of Chapter {num}*

"""
```

### 8. Write the Merged File

Use `patch` (preferred — smaller diff, preserves file history) or `write_file` (for complete overwrite):

```bash
# Using patch with the last line as anchor
patch old_string="*End of Chapter 8 — Bridge: ...*" \
      new_string="*End of Chapter 8 — Bridge: ...*\n\n---\n\n...new content..."
```

If the insertion point is unique, use `patch` with `replace` mode. For very large insertions, `write_file` may be simpler.

### 9. Verify

Check that the final manuscript is well-formed:

```bash
# Check heading structure
grep -n '^#' /path/to/manuscript.md

# Verify word count isn't drastically wrong
wc -l -w /path/to/manuscript.md

# Spot-check beginning, middle, and end of inserted chapters
```

Key verifications:
- [ ] Part heading level matches existing convention
- [ ] Chapter heading level matches existing convention
- [ ] Chapter separator style matches existing convention
- [ ] End-of-chapter markers match existing convention
- [ ] All original chapters are preserved (no deletions)
- [ ] Inserted chapters appear in the correct position
- [ ] Placeholder markers are present for outline-only chapters

## Pitfalls to Avoid

| Pitfall | Solution |
|---------|----------|
| **Heading level mismatch** | Existing chapters use `##` (H2) but insertion uses `#` (H1) — always check `grep -n '^#'` first |
| **Title separator mismatch** | Manuscript uses `—` (em dash) but chapter file uses `–` (en dash) — normalize to the manuscript's convention |
| **Deleting end-of-chapter markers** | When inserting after the last chapter, don't overwrite its end marker — insert AFTER it |
| **Missing part boundary** | If chapters belong to a new part, add the part heading before them with proper separators |
| **Overlapping with placeholder chapters** | If chapters 9-10 are placeholders, don't accidentally overwrite or skip them — insert after them |
| **Renumbering when unnecessary** | These chapters are already numbered (11, 14). Don't renumber unless explicitly asked |
| **Patching the wrong anchor** | Verify the patch anchor string is unique in the file before using it |
| **Forgetting placeholders for unwritten chapters** | Always add visible markers so the next writer knows where to insert |

## Examples

### Fiction Manuscript Insertion

**Situation**: Manuscript has Chapters 1-8 complete. Chapters 9-10 exist as outlines. Chapters 11 and 14 are ready.

**Insertion point**: After line `*End of Chapter 8 — Bridge: ...*`

**Result**:
```
*End of Chapter 8*

---
<!-- Placeholder for Chapters 9 & 10 -->
---
# PART II — WATER, AIR, AND GROUND
---
## Chapter 11 – False Ice
[full prose]
*End of Chapter 11*
---
## Chapter 14 – Air Made Useful
[full prose]
*End of Chapter 14*
---
*First Generation — Manuscript in progress*
```

## Verification Code Snippet

```python
import re

with open(manuscript_path) as f:
    content = f.read()

# Check heading levels
headers = re.findall(r'^(#{1,3}) Chapter', content, re.MULTILINE)
levels = set(h.count('#') for h in headers)
assert len(levels) == 1, f"Inconsistent heading levels: {levels}"

# Check part heading levels
parts = re.findall(r'^# PART', content, re.MULTILINE)
# Parts should all use the same level
assert all(p.startswith('# ') for p in parts) or all(p.startswith('## ') for p in parts)

# Check all original chapters preserved
for ch_num in range(1, 9):
    assert f"Chapter {ch_num}" in content

# Check new chapters present
for ch_num in [11, 14]:
    assert f"Chapter {ch_num}" in content

print(f"✅ Manuscript OK: {len(content.split())} words, {len(content.splitlines())} lines")
```

## Related Skills

- `publishing-workflow` §3E — Non-fiction chapter insertion with renumbering (different header format `# Chapter N:`)
- `manuscript-restoration` — Fixing missing/incorrect chapter headers where content already exists
- `manuscript-restructuring` — Rewriting, repositioning, and bulk text transformations within manuscripts
