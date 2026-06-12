# Fiction Chapter Image Generation Pitfalls

When generating B&W pencil sketch chapter images for fiction books and inserting them into Markdown manuscripts:

## Pre-Flight Checks (Always Do These First)

### 1. Find the REAL manuscript file
```bash
ls -la path/to/book/*MANUSCRIPT*.md | grep -v backup | grep -v "print.html"
wc -w $(ls -S path/to/book/*MANUSCRIPT*.md | grep -v backup | head -1)
```
The largest file is the real manuscript. Some books have a stub `MANUSCRIPT.md` and a real `*_MANUSCRIPT.md`.

### 2. Identify the header format
```bash
# Try multiple patterns to find chapter headers
grep -n -e "^# Chapter" -e "^## Chapter" -e "^- Chapter" MANUSCRIPT.md | head -10
```

Use the reference file at `book-editorial-review/references/chapter-header-formats.md` for book-by-book details.

### 3. Check for existing images
```bash
ls book/chapter_images/ 2>/dev/null | wc -l
# If images exist, skip those chapters during generation
```

## Header Format Edge Cases

| Format | Problem | Fix |
|--------|---------|-----|
| `## Chapter N:` (double hash) | Regex expects single `#` | Use `r"^## Chapter \\d+"` instead |
| `Chapter N — Title` (H1 with em dash) | Standard | Works with `r"^# Chapter \\d+"` |
| `Chapter One:` (worded) | Regex expects digits | Use word-to-number mapping dictionary |
| Inline (no leading `\n`) | Headers start mid-paragraph | Find with broader regex, add newline before header before inserting image |
| Non-sequential (1,2,3,5,7,...) | Script assumes sequential numbering | Find actual header numbers, don't assume max is the count |

## Image Insertion Pattern

For markdown manuscripts, insert images right after the chapter header:
```
# Chapter N — Title

![](chapter_images/ch{NUMBER}.png)

[chapter content...]
```

## Rate Limiting

Gemini 2.5 Flash Image API: ~6s between calls, ~15s per image generation. Budget ~21s per image.
For 60+ chapters: ~21 minutes. Use background processes with `notify_on_complete=true`.

## Verification

```bash
# Count images inserted
grep -c "chapter_images/" MANUSCRIPT.md
# Count chapter headers
grep -c "^# Chapter\|^## Chapter" MANUSCRIPT.md
# They should match
```