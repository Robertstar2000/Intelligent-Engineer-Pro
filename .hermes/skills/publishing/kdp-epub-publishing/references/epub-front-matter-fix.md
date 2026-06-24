# EPUB Front Matter & TOC Fix — Lunar Foundation Pattern

## Problem
The Lunar Foundation EPUBs had `front.xhtml` with title/copyright/TOC but it was NOT in the OPF spine.

## Fix
1. Add `<itemref idref="front"/>` to spine before ch01
2. Rebuild nav.xhtml with clean titles + front matter entry + landmarks
3. Rebuild toc.ncx with clean titles + front matter navPoint
4. Clean front.xhtml (remove nested XML)
5. Repackage EPUB

## Chapter Title Extraction
```bash
unzip -p EPUB OEBPS/nav.xhtml | grep -o 'ch[0-9]*\.xhtml">[^<]*' | sed 's/ch[0-9]*\.xhtml">//'
```

## Cleaning Duplicated Prefixes
```python
parts = re.split(r'Chapter \d+:\s*', raw_title)
cleaned = parts[-1] if len(parts) > 1 else raw_title
```
