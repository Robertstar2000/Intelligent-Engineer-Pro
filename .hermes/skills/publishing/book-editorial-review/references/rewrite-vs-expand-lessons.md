# Rewrite vs Expand: Lessons from Session 2026-06-13 (Updated 2026-06-12)

## ⚠️ CRITICAL: Trim Scripts Must Write to Temp File First (2026-06-12)

**A trim script destroyed NBS BkIV's MANUSCRIPT.md, dropping it from 53,720 to 3,933 words.** The regex for chapter boundary detection failed silently, and the script wrote the truncated result directly to the source file.

**Safe trim pattern:**
```python
import re, shutil

SOURCE = "MANUSCRIPT.md"
TEMP = SOURCE + ".new"

# ALWAYS backup first
shutil.copy2(SOURCE, SOURCE + ".BEFORE_TRIM")

with open(SOURCE) as f:
    text = f.read()

original_words = len(text.split())

# ... do processing ...

with open(TEMP, 'w') as f:
    f.write(new_text)

new_words = len(open(TEMP).read().split())
print(f"Original: {original_words:,} → New: {new_words:,}")

# VERIFY before replacing
if new_words < original_words * 0.9:
    print("WARNING: Lost >10% of words. Aborting. Check your regex.")
else:
    shutil.move(TEMP, SOURCE)
    print("OK — replaced.")
```

**Key rules for ANY destructive script (trim or expand):**
1. Never write to the same file you're reading in a Python script
2. Write to `.new` or `.tmp` file first, verify, then `shutil.move()`
3. Verify word count change is reasonable (<10% loss for trims, >0% gain for expansions)
4. If regex matches ≠ expected chapter count, ABORT before writing
5. Create a backup with timestamp before ANY destructive operation
6. Test regex on a copy first — run match count before doing replacements

---

## The Core Problem

When books are severely underlength (23K words vs 50K target), expanding existing content by adding paragraphs consistently fails. The correct approach is to rewrite the weakest chapters from scratch using genre benchmarks and humanizer rules.

## The Correct Approach

1. Identify chapters under 800 words
2. Rewrite from scratch (1,500-2,000 words each) using:
   - Genre benchmarks (personal stakes, show don't tell, sensory detail)
   - Humanizer rules (strip AI-isms, add voice, vary rhythm)
3. Replace safely using line-number-based extraction

## What NOT To Do

- `content.replace()` for chapter manipulation — matches overlapping strings
- Paragraph-trimming scripts — destroys chapter content
- Complex string splitting — loses content at wrong boundaries
- Writing `content` instead of `new_content` — discards all changes

## Safe Patterns

- Append: `cat >> file << 'EOF'`
- Insert: `lines.insert(n, content)`
- Replace between known boundaries: `content[:start] + new + content[end:]`
- Always verify after: `wc -w`, chapter count, spot-check

## Book Targets

| Book | Current | Target | Action |
|------|---------|--------|--------|
| NBS BkIV | 28K | 50K | Rewrite 7 weak chapters (+22K) |
| NBS BkV | 24K | 50K | Rewrite 6 weak chapters, remove duplicates (+26K) |
| CLLC Bk1 | 92K | 65K | Trim bloated chapters (-27K) |
| Memoir | 45K | 70K | Rewrite thin chapters (+25K) |
