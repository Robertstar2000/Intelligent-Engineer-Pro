# EPUB Build From Scratch — No-Blue-Sky / LF / AoLS Pattern

> Built 2026-06-20 for No Blue Sky series, applied to Lunar Foundation + Age of Lightships.
> Use when no existing EPUB build pipeline is available or the existing one produces invalid output.

## When to Use

- EPUB has broken OPF (duplicate IDs, missing spine items)
- EPUB has no TOC or generic TOC (no chapter titles)
- No HTML source exists — only PDF/EPUB/PNG images
- Starting from scratch with manuscript + images

## EPUB Structure

```
mimetype                 # "application/epub+zip" — MUST be first, uncompressed
META-INF/container.xml   # Points to OEBPS/content.opf
OEBPS/
├── content.opf         # Package manifest + spine
├── nav.xhtml           # EPUB3 nav document (toc, landmarks)
├── styles.css          # Shared stylesheet
├── front.xhtml         # Title page + copyright
├── toc.xhtml           # Standalone TOC page (in spine)
├── ch01.xhtml          # Chapter 1
├── ch02.xhtml          # Chapter 2
├── ...
└── images/
    ├── ch01.png
    ├── ch02.png
    └── ...
```

## Critical Rules

### OPF: Unique Manifest IDs

Every `id=` in the OPF manifest MUST be unique. Collision between chapter XHTML and image IDs is the #1 cause of KDP rejection.

**Pattern:**
- Chapters: `id="ch01"`, `id="ch02"`, ...
- Images: `id="img-ch01"`, `id="img-ch02"`, ...
- Special: `id="front"`, `id="toc"`, `id="nav"`, `id="css"`

### OPF: Complete Spine

Every chapter MUST have an `<itemref idref="chNN"/>` in the spine. Missing spine items = KDP rejection.

### nav.xhtml: Chapter Titles

The nav.xhtml MUST contain actual chapter titles, not generic "Chapter 1" labels.

```html
<nav epub:type="toc" id="toc">
  <h2>Table of Contents</h2>
  <ol>
    <li><a href="ch01.xhtml">Chapter 1: The Descent Window</a></li>
    <li><a href="ch02.xhtml">Chapter 2: Counting What Matters</a></li>
    ...
  </ol>
</nav>
```

### Chapter XHTML: Valid, Self-Contained

Each chapter XHTML must be a valid XHTML document:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">
<head>
  <title>Book Title</title>
  <link rel="stylesheet" type="text/css" href="styles.css"/>
</head>
<body>
<div class="chapter" id="ch1">
<h2>Chapter 1: Title</h2>
<div class="chapter-image"><img src="images/ch01.png" alt="Chapter 1" /></div>
<p>Content...</p>
</div>
</body>
</html>
```

### Image References in XHTML

Use relative paths from the XHTML file: `src="images/ch01.png"` (not `src="ch01.png"`).

### Packaging

```python
import zipfile
with zipfile.ZipFile(epub_path, "w", zipfile.ZIP_DEFLATED) as zf:
    # mimetype MUST be first and uncompressed
    zf.write("mimetype", "mimetype", compress_type=zipfile.ZIP_STORED)
    # All other files
    for root, dirs, files in os.walk(epub_dir):
        for file in files:
            if file == "mimetype": continue
            fp = os.path.join(root, file)
            zf.write(fp, os.path.relpath(fp, epub_dir))
```

## Common Pitfalls

1. **Duplicate IDs** — chapters and images both using `ch01` as their ID. Fix: prefix images with `img-`.
2. **Missing spine items** — only ch01 in spine, rest missing. Fix: add `<itemref>` for every chapter.
3. **Generic TOC** — "Chapter 1", "Chapter 2" instead of actual titles. Fix: extract titles from HTML/manuscript.
4. **Full HTML in chapter XHTML** — wrapping content in another `<html><head><body>` inside the chapter file. Fix: chapter XHTML IS the full document, content goes directly in `<body>`.
5. **Wrong image paths** — `src="ch01.png"` instead of `src="images/ch01.png"`. Fix: use `images/` prefix.
6. **RGBA images** — Gemini generates RGBA PNGs. Convert to RGB before embedding.

## Batch Build Script Template

See `references/batch-chapter-image-generation.md` for the image generation pipeline.

For the full EPUB + PDF build pipeline, the pattern is:
1. Generate/resize images (460px max for 6×9" books with 0.5" margins)
2. Build HTML with correct CSS (0.5in margins, no excessive p/section margins)
3. Build EPUB (unique IDs, proper nav, chapter titles)
4. Build PDF (WeasyPrint with absolute file:// image paths)
5. Copy to KDP_Package/Print/ and KDP_Package/Kindle/

## CSS for Print HTML

```css
@page { size: 6in 9in; margin: 0.5in; }
@page :first { @bottom-center { content: none; } }
body { font-family: Georgia, serif; font-size: 10pt; line-height: 1.5; text-align: justify; }
p { text-indent: 1.5em; margin: 0; orphans: 2; widows: 2; }
.chapter-image { text-align: center; margin: 1em 0; page-break-inside: avoid; }
.chapter-image img { max-width: 480px; width: auto; height: auto; max-height: 400px; }
.chapter { page-break-before: always; }
.title-page { text-align: center; page-break-after: always; }
```

**Key:** `p { margin: 0 }` — the original manuscripts had `margin: 0.5in` on p tags which pushed content inward and caused image overflow.
