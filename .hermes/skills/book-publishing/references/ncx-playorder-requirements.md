# NCX playOrder Requirements for KDP (June 2026)

## Problem
KDP rejects EPUBs or TOC fails to display when the NCX (Table of Contents) file is missing `playOrder` attributes on `<navPoint>` elements.

## Root Cause
The NCX spec requires `playOrder` attributes for Kindle to render the TOC. Without it, the `navPoint` entries exist but Kindle cannot display them in order.

## Fix Pattern
```python
# Add sequential playOrder to all navPoint elements
lines = ncx_content.split('\n')
result = []
play_order = 0
for line in lines:
    if '<navPoint id=' in line and 'playOrder' not in line:
        line = line.replace('<navPoint id=', f'<navPoint playOrder="{play_order}" id=', 1)
        play_order += 1
    result.append(line)
fixed = '\n'.join(result)
```

## Validation
```bash
# Check playOrder count matches navPoint count
unzip -p book.epub toc.ncx | grep -c 'playOrder="'
```

## Real-World Incident
**Lunar Foundation Series (4 books, 20 EPUB files)** — All EPUBs had NCX files without `playOrder`. KDP TOC display was broken. Fixed by adding sequential playOrder to all `<navPoint>` elements across all files.

**Secondary issue:** Some EPUBs had their OPF manifests corrupted by an earlier fix script that used regex `<item\s+href="([^"]+)"\s+id="([^"]+)"` but the actual OPF used `id` before `href`: `<item id="style" href="style.css" ...>`. The regex matched 0 items, producing an empty manifest. Fix: use a more flexible regex that handles both attribute orders:
```python
# Flexible regex for OPF item extraction
items = re.findall(r'<item\s+(?:id="[^"]+"\s+)?href="([^"]+)"', opf)
items += re.findall(r'<item\s+href="([^"]+)"\s+(?:id="[^"]+"', opf)
manifest = len(set(items))
```

**Rebuild pattern:** When EPUB manifests are broken, rebuild them by:
1. Extracting the source EPUB to a temp dir
2. Copying chapter/content files from a known-good source
3. Generating fresh NCX with playOrder, nav.xhtml with epub:type="toc"
4. Rebuilding OPF manifest with ALL files present
5. Repackaging with mimetype first + uncompressed

**Environment-dependent failures (NOT rules):**
- `pip install weasyprint` may timeout at 120s on slow networks — use background=true
- EPUB zip file paths may use `EPUB/` or `OEBPS/` prefix — always search for `.opf` files with `rglob` to find actual structure
