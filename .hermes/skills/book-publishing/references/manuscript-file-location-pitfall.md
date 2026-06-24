# Manuscript File Location Pitfall

> Critical lesson learned 2026-06-19: Editing the wrong manuscript file.

## The Problem

Many book directories have **two** manuscript files:

```
book_dir/
├── built-from-dust_MANUSCRIPT.md      ← root-level (IGNORED by build)
└── manuscript/
    └── MANUSCRIPT.md                   ← ACTUAL source read by collect_chapters()
```

The `collect_chapters()` function in `hermes_publish/utils.py` reads from the `manuscript/` subdirectory first:

```python
manuscript_dir = book_dir / "manuscript"
mdx = manuscript_dir if manuscript_dir.exists() else book_dir
files = list(mdx.glob("*MANUSCRIPT.md"))
```

The root-level file is **only** used as a fallback when `manuscript/` doesn't exist.

## Symptoms of Editing the Wrong File

- Chapter numbering changes don't appear in the build output
- Inserted images don't appear in the PDF/EPUB/HTML
- TOC page numbers don't match expected values
- Verification scripts show no changes despite editing

## How to Verify

```python
from utils import collect_chapters
chapters = collect_chapters(book)
# Print first 100 chars of chapter 1 content to see which file was read
print(chapters[0][2][:100])
```

## The Fix

Always edit `book_dir/manuscript/MANUSCRIPT.md`, NOT the root-level file.

## Additional Pitfall: Different Heading Formats

The root-level and `manuscript/` files may use **different heading formats**:
- Root: `## Chapter N — Title` (em-dash with `##`)
- Manuscript/: `# Chapter N — Title` (single `#`) or even bare `Chapter N — Title` (no `#`)

When inserting images, detect the heading format first, then insert the image line after the heading using the correct format as the search pattern.

## Duplicate Headings

Previous editing sessions may leave **duplicate headings** — e.g.:
```
## Chapter 9: Born Under Two Suns        ← original (colon format)
## Chapter 9 — Born Under Two Suns         ← added later (em-dash format)
![](chapter_images/ch09.png)               ← inserted after wrong heading
```

The image ends up after the second heading, but `collect_chapters` splits on the first heading pattern it finds. The image becomes part of the **previous** chapter's content, not the target chapter.

**Always check for and remove duplicate headings before inserting images.**
