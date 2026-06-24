# Hermes Publish Pipeline — Business Book & Memoir Notes

## Manuscript Type for Business Books and Memoirs

Business series books and the memoir use `manuscript_type: "manuscript_md"` in `hermes_publish/config.py`. The MANUSCRIPT.md lives in the `manuscript/` subdirectory.

**Note:** Previously business books were set to `chapters_md` which looks for individual chapter files in `html/`, `chapters/`, or `manuscript_src/` directories. Changed to `manuscript_md` which splits a single MANUSCRIPT.md on chapter headings.

**Warning:** Do NOT use `single_md` for books with MANUSCRIPT.md — it treats each `.md` file as one chapter, so the entire manuscript becomes "Chapter 1: Manuscript" and other .md files (like book-review.md) become separate chapters.

## collect_chapters() — How It Works (2026-06-18 Update)

The `collect_chapters()` function in `hermes_publish/utils.py` handles `manuscript_md` type by:

1. Finding `*MANUSCRIPT.md` in the manuscript directory
2. Splitting on chapter headings using regex
3. Filtering to only count actual chapter headings

### The Regex Pattern (FIXED)

```python
# Split on newline before ## Chapter N or # Chapter N (with any separator)
parts = re.split(r'\n(?=## Chapter \d+[:—\-–]|# Chapter \d+[:—\-–])', content)

# Then match only actual chapter headings (require separator after number)
tm = re.match(r'#{1,2}\s+Chapter\s+\d+\s*[:—\-–]', part)
```

**Key insight:** The em-dash (U+2014, `—`) must be a **literal character** in the regex pattern. Do NOT use `\u2014` inside a raw string — it will be treated as literal `\`, `u`, `2`, `0`, `1`, `4`. Instead, copy-paste the actual em-dash character or use a character class `[:—\-–]` that matches colon, em-dash, hyphen, or en-dash.

### Appendix Answer Key False Positives

Appendix D (Reader Exercise Answer Keys) contains headings like `## Chapter 1: Spot the Action Gap` that get picked up as chapters because the colon matches the separator character class. To filter these out, check that the part does NOT come after an `## Appendix` heading, or require em-dash specifically (not colon) for the chapter match:

```python
# Stricter: require em-dash (not colon) for chapter headings
tm = re.match(r'#{1,2}\s+Chapter\s+\d+\s*[—\-–]', part)  # only em-dash/en-dash/hyphen
```

### Memoir Format

The memoir (Tomorrow Remembered) uses `## Chapter N: Title` format (colon separator, not em-dash). For memoir manuscripts, the colon-based matching works correctly since there are no appendix answer keys with `## Chapter N:` format.

## single_md Type — Filtering MANUSCRIPT.md Only

When `manuscript_type` is `single_md`, the pipeline globs all `*.md` files. For books that have both `MANUSCRIPT.md` and `book-review.md` in the same directory, this causes the review file to appear as a separate chapter. Fix in `collect_chapters()`:

```python
# Only pick up MANUSCRIPT.md files, not other .md files like book-review.md
md_files = sorted(mdx.glob("*MANUSCRIPT.md"))
# Fallback: if no MANUSCRIPT.md, use all .md files
if not md_files:
    md_files = sorted(mdx.glob("*.md"))
```

## Business Book Front Matter Structure

Each business book manuscript should have exactly ONE title page section:
```
# Title
## Subtitle

---

© 2026 Bob J Mills. All rights reserved. [disclaimer]

---

## Table of Contents
[toc content]

---

### **Preface: Title**
[preface content]

---

```

**NOT** multiple title page blocks. The original manuscripts had duplicate title/copyright/TOC sections that needed consolidation.

## Chapter Numbering

Business books may have chapters in multiple heading formats:
- `## Chapter N — Title` (chapters 1-22, within Parts)
- `# Chapter N — Title` (chapters 23+, domain-specific chapters)

Both must be recognized by the pipeline. The em-dash (—) is the separator, not a colon (:).

Memoirs use `## Chapter N: Title` format (colon separator) consistently throughout.

## Adding New Chapters to a Manuscript

When adding chapters to an existing manuscript:
1. Insert the new chapter content BEFORE the next `## Chapter` heading (or before the first appendix)
2. Renumber subsequent chapters if needed
3. Update the TOC to include the new chapter
4. Update chapter count references in the preface
5. Use Python scripts for bulk text manipulation — do NOT try to manually edit 9000+ line files with patch tool
6. Always verify the result by grepping for chapter headings: `grep -n "^# Chapter\|^## Chapter" file.md`

## Regenerating Output Files

```python
from hermes_publish.config import BOOK_REGISTRY
from hermes_publish.step_pdf import run as pdf_run
from hermes_publish.step_epub import run as epub_run

book = BOOK_REGISTRY['book-key']
pdf_run('book-key', book)   # Generates PDF + HTML in output/
epub_run('book-key', book)   # Generates EPUB in output/
```

The HTML file is an intermediate; the PDF is generated from it via WeasyPrint. Chapter images are automatically included from `chapter_images/` or `images/` directories (B&W converted for fiction/memoir/mystery, color retained for business).
