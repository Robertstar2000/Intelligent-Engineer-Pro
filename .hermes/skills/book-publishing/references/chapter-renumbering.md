# Chapter Renumbering — Pitfalls & Correct Approach

## The Cascading Replacement Bug

When renumbering chapters (e.g., 22-53 → 1-32), a naive descending loop causes cascading replacements:

```python
# ❌ WRONG — cascading replacement
for old_num in range(53, 21, -1):
    new_num = old_num - 21
    content = content.replace(f"## Chapter {old_num} —", f"## Chapter {new_num} —")
```

**Why it fails**: After replacing "Chapter 43" → "Chapter 22", when the loop reaches old_num=22, it replaces ALL "Chapter 22" (including the one just created from 43). Result: multiple chapters get the same number.

Even descending order doesn't help if the replacement target matches a value that will be processed later in the loop.

## Correct Approach: Two-Pass with Unique Placeholders

```python
# ✅ CORRECT — use unique placeholders first
# Pass 1: Replace all chapter numbers with unique placeholders
for old_num in range(22, 54):
    content = content.replace(f"## Chapter {old_num} —", f"## Chapter __CH{old_num}__ —")

# Pass 2: Replace placeholders with final numbers
for old_num in range(22, 54):
    new_num = old_num - 21
    content = content.replace(f"## Chapter __CH{old_num}__ —", f"## Chapter {new_num} —")
```

## Alternative: Line-by-Line Regex Replacement

```python
# ✅ CORRECT — regex with callback, single pass
import re
offset = 21  # subtract this from all chapter numbers
def renumber_match(m):
    old_num = int(m.group(1))
    new_num = old_num - offset
    return f"## Chapter {new_num} —{m.group(2)}"

content = re.sub(r'## Chapter (\d+) —(.*)', renumber_match, content)
```

This works because regex processes each match independently — no cascading.

## Same Fix Applies to TOC Entries

The TOC has the same numbering as chapter headers. Apply the same renumbering to TOC lines:

```python
# TOC entries use the same chapter numbers
for old_num in range(22, 54):
    new_num = old_num - 21
    content = content.replace(f"| Chapter {old_num}:", f"| Chapter {new_num}:")
    # Also handle TOC dot-leader lines
    content = content.replace(f"Chapter {old_num} —", f"Chapter {new_num} —")
```

## Verification After Renumbering

Always verify:
1. All chapter numbers are sequential 1-N with no gaps
2. No duplicate chapter numbers
3. TOC entries match chapter headers exactly
4. Total count matches expected chapter count

```python
import re
headers = sorted(set(int(m) for m in re.findall(r'## Chapter (\d+)', content)))
toc_entries = sorted(set(int(m) for m in re.findall(r'Chapter (\d+):', content)))
assert headers == list(range(1, len(headers)+1)), f"Header gap: {headers}"
assert toc_entries == list(range(1, len(toc_entries)+1)), f"TOC gap: {toc_entries}"
assert len(headers) == expected_chapter_count
```

## Build Pipeline Invocation

After renumbering, rebuild all three outputs:

```bash
cd /mnt/usb_4tb/books/hermes_publish && python -c "
import sys; sys.path.insert(0, '.')
from config import BOOK_REGISTRY
from step_pdf import run as pdf_run
from step_epub import run as epub_run
book = BOOK_REGISTRY['oxygen-gamble']
pdf_run('oxygen-gamble', book)
epub_run('oxygen-gamble', book)
"
```

**⚠️ Do NOT use `python hermes_publish.py`** — the file conflicts with the package directory and causes `ModuleNotFoundError`. Use `python -c` with direct imports instead.

**⚠️ `step_pdf.py` only builds PDF + HTML.** EPUB requires a separate call to `step_epub.run()`.
