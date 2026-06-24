# EPUB Build Pitfalls (2026-07-20)

Session fixing all 5 No Blue Sky EPUBs revealed multiple structural issues and the correct build approach.

## Image References in Chapter XHTML

**Pitfall:** HTML references images as `src="ch01.png"` (relative to HTML file). In EPUBs, images are in `OEBPS/images/` but chapter XHTML files are in `OEBPS/`. The reference must be `src="images/ch01.png"`.

```python
# Fix: replace src="chXX.png" with src="images/chXX.png" in chapter content
sec_content = re.sub(r'src="ch(\d+\.png)"', r'src="images/ch\1"', sec_content)
```

## Duplicate Images in HTML

**Pitfall:** Manuscript HTML may contain TWO `<img>` tags per chapter — one in `<div class="chapter-image">` and one in a `<p>` tag. Both reference the same image. This causes duplicate images in the EPUB.

```python
# Fix: remove the duplicate <p><img ...> tags, keep only the chapter-image div
content = re.sub(r'\s*<p><img src="chapter_images/[^"]*" alt=""\s*/>\s*', '\n', content)
```

## OPF Duplicate IDs

**Pitfall:** If chapter XHTML files use `id="ch01"` and images also use `id="ch01"`, the OPF manifest has duplicate IDs. XML IDs must be unique.

```xml
<!-- WRONG: both use id="ch01" -->
<item id="ch01" href="ch01.xhtml" media-type="application/xhtml+xml"/>
<item id="ch01" href="images/ch01.png" media-type="image/png"/>

<!-- RIGHT: prefix image IDs -->
<item id="ch01" href="ch01.xhtml" media-type="application/xhtml+xml"/>
<item id="img-ch01" href="images/ch01.png" media-type="image/png"/>
```

## Incomplete Spine

**Pitfall:** The `<spine>` element must reference ALL chapters. If only `ch01` is listed, the EPUB reader only shows chapter 1.

```xml
<!-- WRONG -->
<spine>
  <itemref idref="ch01"/>
</spine>

<!-- RIGHT: all chapters -->
<spine>
  <itemref idref="ch01"/>
  <itemref idref="ch02"/>
  <!-- ... all chapters ... -->
</spine>
```

## TOC Page as Standalone File

**Pitfall:** The print HTML has `<div class="toc-page">` with chapter listings and page numbers. In the EPUB, this should be a standalone `toc.xhtml` file in the spine (after front matter, before chapters), not embedded in `front.xhtml`.

**Correct EPUB structure:**
```
OEBPS/front.xhtml     — title page + copyright (NOT in spine)
OEBPS/toc.xhtml       — table of contents page (in spine)
OEBPS/ch01.xhtml      — chapter 1 (in spine)
OEBPS/ch02.xhtml      — chapter 2 (in spine)
...
OEBPS/nav.xhtml       — EPUB nav document (properties="nav")
OEBPS/images/         — all images
```

**Split logic:**
```python
# Find TOC page in HTML
toc_start = html_content.find('<div class="toc-page">')
toc_end = html_content.find('</div>', toc_start) + len('</div>') if toc_start >= 0 else -1

# Split: title+copyright | TOC | chapters
title_part = html_content[:toc_start].strip()  # before TOC
toc_content = html_content[toc_start:toc_end].strip()  # TOC page
# Then split remaining on <div class="chapter" id="chN">
```

## nav.xhtml Must Use Real Chapter Titles

**Pitfall:** Generic "Chapter 1, Chapter 2" labels in nav.xhtml. Must extract actual titles from the HTML.

```python
# Extract titles from h3 headings
h3_match = re.search(r'<h3[^>]*>(.*?)</h3>', section, re.DOTALL)
title = re.sub(r'<[^>]+>', '', h3_match.group(1)).strip()
```

```xml
<!-- nav.xhtml TOC entry -->
<li><a href="ch01.xhtml">Chapter 1: The Descent Window</a></li>
```

Also include a "Table of Contents" link pointing to `toc.xhtml`:
```xml
<li><a href="toc.xhtml">Table of Contents</a></li>
```

## Chapter XHTML Must Be Valid Standalone Documents

Each chapter XHTML file must be a complete, valid XHTML document:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">
<head>
  <title>Book Title</title>
  <link rel="stylesheet" type="text/css" href="styles.css"/>
</head>
<body>
<!-- chapter content here (div, h3, p, img, etc.) -->
</body>
</html>
```

**Do NOT** include the full HTML document (DOCTYPE, html, head, style, body) inside chapter content — the script wraps each section in its own XHTML document.

## Splitting on Chapter Boundaries

**Correct split pattern:** Use `<div class="chapter" id="chN">` as the chapter boundary marker. This is more reliable than splitting on `<h3>` because some books have multiple h3 headings per chapter.

```python
chapter_starts = [(m.start(), m.group()) for m in re.finditer(
    r'<div class="chapter" id="ch\d+">', html_content
)]
```

## Verification Checklist

After building, verify:
1. `grep -c '<img' html` equals expected image count (no duplicates)
2. OPF has no duplicate IDs: `len(ids) == len(set(ids))`
3. Spine has all chapters: `spine_count == chapter_count`
4. nav.xhtml has real chapter titles (not generic "Chapter N")
5. All images referenced in XHTML exist in `OEBPS/images/`
6. Chapter XHTML files are valid XML (no nested `<html>` documents)
