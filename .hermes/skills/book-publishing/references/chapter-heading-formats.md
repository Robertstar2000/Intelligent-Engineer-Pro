# Chapter Heading Format Reference

> Quick reference for the `collect_chapters()` regex in `hermes_publish/utils.py`.
> Last updated: 2026-06-19

## Supported Formats

The split regex must handle ALL of these:

| Format | Example | Books Using This |
|---|---|---|
| `## Chapter N — Title` | `## Chapter 1 — The Shock` | Tomorrow Remembered, No Blue Sky #1, Business #1-3 |
| `## Chapter N: Title` | `## Chapter 1: The Shock` | Some appendix answer keys |
| `# Chapter N — Title` | `# Chapter 1 — The Edge of Silence` | Lunar Foundation #1-3 |
| `# Chapter N -- Title` | `# Chapter 1 -- The Declaration` | No Blue Sky #3-5 |
| `## Chapter N — Title` (space before dash) | `## Chapter 1 — The $200 Mistake` | Business #1, Age of Lightships |
| `Chapter N — Title` (bare, no `#`) | `Chapter 1 — The Edge of Silence` | No Blue Sky #3-5 (in `manuscript/` file) |

## ⚠️ Bare Chapter Headings (No `#` Prefix)

Some `manuscript/MANUSCRIPT.md` files use bare `Chapter N — Title` without any `#` prefix. The `collect_chapters()` regex requires `#{1,2}`, so these headings are **NOT detected** as chapter boundaries.

**Impact:** If the `manuscript/` file has bare headings but the root-level file has `## Chapter N` format, `collect_chapters` reads the root-level file and works correctly. But if you edit the `manuscript/` file to add images using bare heading format, the images won't be in the chapter content.

**Fix:** When working with `manuscript/` files that have bare headings, either:
1. Add `##` prefix to all bare headings (recommended), OR
2. Insert images using the bare heading format as the search pattern, knowing they'll only work if `collect_chapters` actually reads this file

**Always verify with `collect_chapters()` after editing.**

## The Regex

```python
# Split regex (splits on newline before chapter heading)
parts = re.split(r'\n(?=#{1,2}\s+Chapter\s+\d+\s*[:—\-–]{1,2})', content)

# Match regex (extracts chapter number and title from a part)
tm = re.match(r'#{1,2}\s+Chapter\s+\d+\s*[:—\-–]{1,2}', part)
title_m = re.match(r'#{1,2}\s+Chapter\s+\d+\s*[:—\-–]{1,2}\s*(.+)', part)
```

## Key Details

- `{1,2}` for hash count handles both `#` and `##` prefixed headings
- `\s*` between digit and separator is **critical** — without it, `Chapter 1 — Title` (space before em-dash) won't match
- `{1,2}` at the end handles both single (`—`) and double (`--`) separators
- The split uses a lookahead `(?=...)` so the heading line is preserved in the part

## Manuscript Type Selection

| Source Structure | manuscript_type | Notes |
|---|---|---|
| Single `MANUSCRIPT.md` in `manuscript/` or root | `manuscript_md` | Most books — compiled manuscript |
| Multiple `.md` files in `html/` or `chapters/` | `chapters_md` | Cindy Lou #1-3 |
| Multiple `.xhtml` files in `html/` or `manuscript_src/` | `chapters_xhtml` | Rare — individual chapter files |

**Rule:** If `html/` directory is empty but `MANUSCRIPT.md` exists → use `manuscript_md`.

## ⚠️ File Location Matters

`collect_chapters()` reads from `book_dir/manuscript/MANUSCRIPT.md` FIRST, then falls back to `book_dir/*MANUSCRIPT.md`. These two files often differ in:
- Heading format (`##` vs `#` vs bare)
- Image references (root may have images, manuscript/ may not)
- Chapter numbering

**Always verify which file is being read before editing.** See `references/manuscript-file-location-pitfall.md`.
