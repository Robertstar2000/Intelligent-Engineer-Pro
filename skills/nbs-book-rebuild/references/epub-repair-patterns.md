# EPUB Repair Patterns — Lunar Foundation Fix Session

## Source EPUB Location
`/mnt/usb_4tb/books/Lunar_Foundation_Series/Book_X/output/book_x_xxx.epub`

## Output Pattern
`/mnt/usb_4tb/books/Lunar_Foundation_Series/Book_X/output/book-x-xxx_fixed.epub`

## Issues Found & Fixed

### 1. front.xhtml Not in Spine
**Symptom**: Title page / TOC page exists in EPUB but is unreachable in reading order.
**Cause**: `front.xhtml` was not listed in `<spine>` in `content.opf`.
**Fix**: Add `<itemref idref="front"/>` before `<itemref idref="ch01"/>` in spine.

### 2. Duplicate "Chapter N:" Prefix in Titles
**Symptom**: nav.xhtml shows "Chapter 1: Chapter 1 — The Artemis Accord"
**Cause**: Chapter XHTML has `<h2>Chapter 1: Chapter 1 — The Artemis Accord</h2>` (prefix duplicated from filename + content).
**Fix**: Split on `Chapter \d+:\s*` and take the last segment:
```python
parts = re.split(r'Chapter \d+:\s*', raw_title)
cleaned = parts[-1] if len(parts) > 1 else raw_title
```

### 3. Orphan `</div>` Tags in Chapter XHTML
**Symptom**: `xml.etree.ElementTree.ParseError: mismatched tag`
**Cause**: PDF extraction pipeline leaves unbalanced div tags.
**Fix**: See `references/epub-div-fix.md` for tag-stacking repair algorithm.

### 4. HTML Named Entities in XHTML
**Symptom**: `xml.etree.ElementTree.ParseError: undefined entity: line N, column M`
**Cause**: `&mdash;`, `&ldquo;`, `&rdquo;` etc. are HTML entities, not valid XML.
**Fix**: Replace with numeric entities before parsing:
```python
named_entities = {
    '&mdash;': '&#8212;', '&ndash;': '&#8211;',
    '&ldquo;': '&#8220;', '&rdquo;': '&#8221;',
    '&lsquo;': '&#8216;', '&rsquo;': '&#8217;',
    '&hellip;': '&#8230;', '&nbsp;': '&#160;',
    '&copy;': '&#169;', '&reg;': '&#174;', '&trade;': '&#8482;',
}
entity_pattern = re.compile('|'.join(re.escape(k) for k in named_entities))
content = entity_pattern.sub(lambda m: named_entities[m.group(0)], content)
```

### 5. Nested XML Declarations in front.xhtml
**Symptom**: `front.xhtml` contains nested `<?xml version="1.0"?>` and `<html>` tags.
**Cause**: PDF extraction pipeline embeds a full HTML document inside another.
**Fix**: Rewrite `front.xhtml` as a single clean XHTML document with title page, copyright, and TOC entries.

### 6. Missing Landmarks nav
**Symptom**: KDP requires `epub:type="landmarks"` nav with `bodymatter` landmark.
**Fix**: Add to `nav.xhtml`:
```html
<nav epub:type="landmarks">
  <h2>Landmarks</h2>
  <ol>
    <li><a epub:type="bodymatter" href="ch01.xhtml">Start Reading</a></li>
  </ol>
</nav>
```

## EPUB Naming Conventions (Lunar Foundation)
Source EPUBs use underscore naming: `book_1_moon_rock.epub`
Short names also exist: `moon-rock.epub`
Always check multiple patterns when locating source files.

## Chapter Title Extraction
Chapter titles are in `<title>` tag in `<head>`, NOT in `<h1>`/`<h2>` in body:
```html
<head><title>Chapter 1 — The Artemis Accord</title></head>
```
Some files have `<h2>` with the title, some don't. Always fall back to `<title>`.

## Verification Checklist
After repair, verify:
```bash
# 1. XML validity
python3 -c "
import xml.etree.ElementTree as ET, glob
for f in sorted(glob.glob('OEBPS/ch*.xhtml')):
    try: ET.parse(f)
    except ET.ParseError as e: print(f'BAD {f}: {e}')
"

# 2. Front matter in spine
grep 'idref="front"' OEBPS/content.opf

# 3. Landmarks present
grep 'epub:type="landmarks"' OEBPS/nav.xhtml

# 4. No duplicate chapter entries in nav
grep -c 'ch01' OEBPS/nav.xhtml  # Should be 2 (toc + landmarks), not 3+
```
