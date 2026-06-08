# EPUB Condensed Book Workflow — Lessons from Cindy Lou Condensation

## The 474-Page Problem

After condensing a book, the user may report the EPUB still shows the OLD page
count. Causes and fixes:

### Cause 1: Stale Output Files

Old PDF/EPUB from BEFORE condensation are still in the output/ directory.
Users open those by habit.

**Fix:** Delete all output files before regenerating:
```bash
rm -f output/*.pdf output/*.epub *.zip
```
Then regenerate with `--force`.

### Cause 2: Wrong Directory

The BOOK_REGISTRY may point to a different directory than the one containing
the condensed chapters. Verify with:
```bash
python3 hermes_publish.py --book [book-key] --status
```
This shows when each step was last built.

### Cause 3: Stale Python Bytecode

After modifying `hermes_publish/*.py` files, Python caches old bytecode.
The EPUB generator may still be running old code.

**Fix:**
```bash
find /mnt/usb_4tb/books/hermes_publish/ -name "__pycache__" -type d -exec rm -rf {} +
```

## EPUB Rendering: "Entity 'nbsp' not defined"

Fix in `md_to_html_simple()` in `hermes_publish/utils.py`:
```python
line = line.replace('&nbsp;', '&#160;')
```
Add as the FIRST line of the `for line in lines:` loop, before any `strip()`.

## Chapter Title Double Header

If EPUB shows `<h2>Chapter 4: Chapter 4</h2>` or the title appears both in
the H2 and as the first body paragraph:

1. Fix `collect_chapters()` to handle plain text titles (no `#` prefix):
   - If first line starts with `#`, strip `#` and optional `Chapter N:` prefix
   - If first line is plain text, use it directly as the title
   - Use `re.sub(r'^Chapter\s+\d+:\s*', '', title)` to strip prefix
2. Fix `step_epub.py` to strip the title line from `content` before
   passing to `md_to_html_simple()` — it's already rendered in `<h2>`
3. Clear `__pycache__` after editing either file

## Book Condensation Target

For a 150-190 page 6x9" trade paperback:
- Target: ~36,000-51,000 words
- Per chapter: ~1,200-1,700 words for 30 chapters
- At 250-270 words per page

## Directory Cleanup After Condensation

Delete these files to prevent confusion:
- `output/Retainer_to_Trouble_Print.pdf` (old 474-page PDF)
- `output/Retainer_to_Trouble.epub` (old full-length EPUB)
- `Retainer_to_Trouble_MANUSCRIPT.md` (old full manuscript, only if condensed chapters exist)

## Mechanical Condensation (Books 2+)

When condensing a second/third book in a series, use Python to score
paragraphs by importance:
- Dialogue: +10 points
- Plot keywords (character names, evidence, arrest, etc.): +2 each
- Scene breaks: always keep
- First 2 and last 2 paragraphs: always keep
- Long pure-description paragraphs (>80 words, no quotes): -2
- Keep top-scoring paragraphs until target word count reached
- Maintain original paragraph order
