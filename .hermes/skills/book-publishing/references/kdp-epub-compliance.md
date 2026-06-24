# KDP EPUB Compliance Checklist

> Source: KDP Kindle Publishing Guidelines (May 2026), EPUBCheck spec, and production fixes applied 2026-06-18.
> This is the authoritative checklist for EPUB files intended for KDP upload.

## KDP EPUB Requirements (Quick Reference)

| Requirement | Spec | Common Failure |
|---|---|---|
| EPUB version | EPUB 3 (recommended), EPUB 2 accepted | Using EPUB 2 without NCX |
| File size | ≤650 MB (aim for <10 MB text, <25 MB images) | Uncompressed images |
| Encoding | UTF-8 (declared in every XHTML file) | Missing encoding declaration |
| Images | JPEG, PNG, GIF, BMP (JPEG/PNG recommended) | TIFF, WebP rejected |
| Image color space | RGB (even grayscale) | CMYK rejected |
| Cover | Uploaded separately, but embed one for preview | Broken internal cover |
| DRM | None (KDP applies its own) | Embedded DRM |
| TOC | Required: both logical (nav/NCX) AND HTML page | Missing nav.xhtml or toc.ncx |
| Landmarks nav | Required for "Start Reading" location | Missing `epub:type="bodymatter"` |
| Language | BCP-47 string (`en-US` or `en`) | Missing or invalid |

## XHTML/XML Compliance (CRITICAL)

KDP runs EPUBCheck on every upload. XHTML files MUST be valid XML. Common rejections:

### 1. Bare Ampersands
**Invalid:** `TV & Electronics` — `&` is a reserved character in XML.
**Valid:** `TV &amp; Electronics`

The only valid XML entities are: `&amp;` `&lt;` `&gt;` `&quot;` `&apos;` `&#123;` `&#xAB;`

**Fix in markdown-to-HTML converter:**
```python
import re
line = re.sub(r'&(?!(amp|lt|gt|quot|apos|#[0-9]+|#x[0-9a-fA-F]+);)', '&amp;', line)
```

### 2. HTML Named Entities Not Valid in XHTML
**Invalid in XHTML:** `&copy;` `&nbsp;` `&mdash;` `&ndash;` `&hellip;` `&trade;` `&reg;`
**Valid replacements:** `&#169;` `&#160;` `&#8212;` `&#8211;` `&#8230;` `&#8482;` `&#174;`

> **Exception:** `&nbsp;` → `&#160;` is handled by the regex above since `&nbsp;` IS a valid XML entity name, but KDP's converter may still choke. Always use `&#160;` to be safe.

### 3. Self-Closing Tags
**Invalid:** `<br>` `<img src="...">` `<hr>`
**Valid:** `<br/>` `<img src="..." />` `<hr/>`

### 4. Unescaped `<` and `>` in Text
**Invalid:** `x < y` (in text content)
**Valid:** `x &lt; y`

## Navigation Document (nav.xhtml) — Required Structure

```xml
<?xml version="1.0" encoding="UTF-8"?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">
<head><title>Navigation</title></head><body>
<nav epub:type="toc" id="toc">
  <h2>Table of Contents</h2>
  <ol>
    <li><a href="titlepage.xhtml">Title Page</a></li>
    <li><a href="copyright.xhtml">Copyright</a></li>
    <li><a href="toc.xhtml">Table of Contents</a></li>
    <li><a href="ch01.xhtml">Chapter 1: Title</a></li>
    <!-- ... all chapters ... -->
  </ol>
</nav>
<nav epub:type="landmarks" hidden="hidden">
  <h2>Guide</h2>
  <ol>
    <li><a epub:type="toc" href="toc.xhtml">Table of Contents</a></li>
    <li><a epub:type="bodymatter" href="ch01.xhtml">Start Reading</a></li>
  </ol>
</nav>
</body></html>
```

**Key requirements:**
- `epub:type="toc"` on the `<nav>` element
- `epub:type="landmarks"` with `hidden="hidden"` on the landmarks `<nav>`
- `epub:type="bodymatter"` pointing to the first chapter — this is what KDP uses for "Start Reading" location
- Declared in OPF manifest with `properties="nav"`

## NCX File (toc.ncx) — Required for Backward Compatibility

KDP expects a `toc.ncx` file for older Kindle devices. Must be:
- Declared in OPF manifest with `media-type="application/x-dtbncx+xml"`
- Referenced in OPF spine: `<spine toc="ncx">`
- Contains `<navPoint>` entries for all major sections

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE ncx PUBLIC "-//NISO//DTD ncx 2005-1//EN" "http://www.daisy.org/z3986/2005/ncx-2005-1.dtd">
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">
<head>
  <meta name="dtb:uid" content="urn:isbn:978-..."/>
  <meta name="dtb:depth" content="1"/>
  <meta name="dtb:totalPageCount" content="0"/>
  <meta name="dtb:maxPageNumber" content="0"/>
</head>
<docTitle><text>Book Title</text></docTitle>
<navMap>
  <navPoint id="navpoint-1" playOrder="1">
    <navLabel><text>Title Page</text></navLabel>
    <content src="titlepage.xhtml"/>
  </navPoint>
  <!-- ... all sections ... -->
</navMap>
</ncx>
```

## OPF Manifest Requirements

```xml
<package version="3.0" xmlns="http://www.idpf.org/2007/opf" unique-identifier="uid">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:identifier id="uid">urn:isbn:978-...</dc:identifier>
    <dc:title>Book Title</dc:title>
    <dc:creator>Author Name</dc:creator>
    <dc:language>en</dc:language>
    <dc:date>2026-06-18</dc:date>
    <dc:publisher>Publisher Name</dc:publisher>
    <meta property="dcterms:modified">2026-06-18T07:31:01Z</meta>
  </metadata>
  <manifest>
    <!-- Every file in the EPUB must be listed here -->
    <item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>
    <item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>
    <!-- ... -->
  </manifest>
  <spine toc="ncx">
    <!-- Reading order -->
  </spine>
</package>
```

**Critical:** Every file in the EPUB ZIP must be listed in the manifest. Every manifest entry must point to a file that exists in the ZIP.

## Validation Checklist Before KDP Upload

Run this before every KDP upload:

```bash
# 1. Unzip and inspect
mkdir -p /tmp/epub-check && cd /tmp/epub-check
unzip -o /path/to/book.epub

# 2. Check for bare ampersands
grep -rn '&[^a-zA-Z#]' OEBPS/*.xhtml | grep -v '&amp;' | grep -v '&lt;' | grep -v '&gt;' | grep -v '&quot;' | grep -v '&#'

# 3. Check for invalid named entities
grep -rn '&copy;' OEBPS/*.xhtml
grep -rn '&nbsp;' OEBPS/*.xhtml
grep -rn '&mdash;' OEBPS/*.xhtml
grep -rn '&ndash;' OEBPS/*.xhtml

# 4. Check XML validity
python3 -c "
import xml.etree.ElementTree as ET
import glob
for f in sorted(glob.glob('OEBPS/*.xhtml')):
    try:
        ET.parse(f)
        print(f'OK  {f}')
    except ET.ParseError as e:
        print(f'BAD {f}: {e}')
"

# 5. Check nav.xhtml has landmarks
grep 'landmarks' OEBPS/nav.xhtml
grep 'bodymatter' OEBPS/nav.xhtml

# 6. Check toc.ncx exists
test -f OEBPS/toc.ncx && echo "toc.ncx: OK" || echo "toc.ncx: MISSING"

# 7. Check OPF spine has toc="ncx"
grep 'toc="ncx"' OEBPS/content.opf

# 8. Check all manifest files exist
python3 -c "
import zipfile, re, os
with zipfile.ZipFile('/path/to/book.epub') as z:
    opf = z.read('OEBPS/content.opf').decode()
    hrefs = re.findall(r'href=\"([^\"]+)\"', opf)
    names = z.namelist()
    for h in hrefs:
        if h not in names:
            print(f'MISSING: {h}')
    print(f'{len(hrefs)} manifest entries checked')
"
```

## Common KDP Rejection Reasons

| Error Message | Cause | Fix |
|---|---|---|
| "EPUB doesn't pass EPUBCheck validation" | Malformed XHTML, bare `&`, invalid entities | Run checklist above |
| "No TOC found" | Missing nav.xhtml landmarks or toc.ncx | Add landmarks nav + toc.ncx |
| "Table of Contents links don't resolve" | Broken anchors in nav/toc | Verify all href targets exist |
| "File size over 650MB" | Uncompressed images | Compress images, target <10MB |
| "Image format not allowed" | TIFF or WebP images | Convert to JPEG or PNG |
| "Start reading location not set" | Missing `epub:type="bodymatter"` in landmarks | Add bodymatter landmark |

## Chapter Heading Format Variations

The `collect_chapters()` function in `utils.py` must handle these heading formats:

| Format | Example | Notes |
|---|---|---|
| `## Chapter N — Title` | `## Chapter 1 — The Shock` | em-dash, most common |
| `## Chapter N: Title` | `## Chapter 1: The Shock` | colon separator |
| `# Chapter N — Title` | `# Chapter 1 — The Edge` | single hash + em-dash |
| `# Chapter N -- Title` | `# Chapter 1 -- The Declaration` | double hyphen |
| `## Chapter N — Title` | `## Chapter 1 — The $200 Mistake` | title may contain `&`, `<`, `>` |

**Critical:** The split regex must include `\s*` between the digit and the separator:
```python
# WRONG — requires separator immediately after digit
re.split(r'\n(?=## Chapter \d+[:—\-–]|# Chapter \d+[:—\-–])', content)

# RIGHT — allows optional space before separator
re.split(r'\n(?=#{1,2}\s+Chapter\s+\d+\s*[:—\-–]{1,2})', content)
```

## Chapter Title Escaping in nav.xhtml / toc.ncx

Chapter titles extracted from source text may contain `&`, `<`, `>` characters. These must be XML-escaped before embedding in nav.xhtml, toc.xhtml, or NCX:

```python
def _esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')
```

Apply `_esc(ct)` wherever a chapter title (`ct`) is interpolated into XHTML/XML in `step_epub.py`.

## Manuscript Type Detection

Books with a single `MANUSCRIPT.md` file (compiled manuscript) must use `manuscript_type: "manuscript_md"`, NOT `chapters_xhtml` or `chapters_md`. The latter types look for individual chapter files in `html/`, `chapters/`, or `manuscript_src/` directories. Using the wrong type results in 0 chapters found.

**Rule of thumb:**
- Single `MANUSCRIPT.md` in `manuscript/` or book root → `manuscript_md`
- Multiple `.md` files in `html/` or `chapters/` → `chapters_md`
- Multiple `.xhtml` files in `html/` or `manuscript_src/` → `chapters_xhtml`

## Production Fixes Applied (2026-06-18)

These fixes were applied to `hermes_publish/step_epub.py` and `hermes_publish/utils.py`:

1. **`utils.py` — `md_to_html_simple()`**: Added bare `&` escaping regex after the `&nbsp;` replacement
2. **`utils.py` — `md_to_html_simple()`**: Added `<`/`>` escaping for characters not part of recognized HTML tags
3. **`utils.py` — `collect_chapters()`**: Fixed regex to handle `# Chapter N — Title` (space before em-dash) and `# Chapter N -- Title` (double hyphen)
4. **`step_epub.py` — Copyright page**: Changed `&copy;` to `&#169;` (numeric entity)
5. **`step_epub.py` — nav.xhtml**: Added landmarks nav with `epub:type="toc"` and `epub:type="bodymatter"`
6. **`step_epub.py` — toc.ncx**: Added full NCX generation with navPoints for all sections
7. **`step_epub.py` — content.opf**: Added `toc="ncx"` to `<spine>` element, added NCX to manifest
8. **`step_epub.py` — Chapter titles**: Added `_esc()` helper for XML-safe chapter titles in nav/toc/NCX
9. **`config.py`**: Corrected `manuscript_type` for 13 books from `chapters_xhtml`/`chapters_md` to `manuscript_md`
