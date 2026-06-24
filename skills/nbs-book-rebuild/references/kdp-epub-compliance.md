# KDP EPUB Compliance Checklist

## Required Files
| File | Required | Purpose |
|------|----------|---------|
| `mimetype` | ✅ | Must be first in ZIP, uncompressed, content: `application/epub+zip` |
| `META-INF/container.xml` | ✅ | Points to OPF file |
| `OEBPS/content.opf` | ✅ | Package manifest + spine + metadata |
| `OEBPS/toc.ncx` | ✅ | Legacy NCX TOC (KDP still requires this) |
| `OEBPS/nav.xhtml` | ✅ | EPUB3 nav document with toc + landmarks |

## OPF Requirements
```xml
<package version="3.0" unique-identifier="uid"
         xmlns="http://www.idpf.org/2007/opf"
         xmlns:dc="http://purl.org/dc/elements/1.1/">
  <metadata>
    <dc:identifier id="uid">urn:uuid:UNIQUE_ID</dc:identifier>
    <dc:title>Book Title</dc:title>
    <dc:creator>Author Name</dc:creator>
    <dc:language>en</dc:language>
  </metadata>
  <manifest>
    <item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>
    <item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>
    <!-- Every file must be listed -->
  </manifest>
  <spine toc="ncx">
    <!-- Front matter BEFORE chapters -->
    <itemref idref="front"/>
    <itemref idref="ch01"/>
    <!-- ... all chapters ... -->
  </spine>
</package>
```

## nav.xhtml Requirements
```xml
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">
<body>
  <!-- TOC nav (required) -->
  <nav epub:type="toc" id="toc">
    <h2>Table of Contents</h2>
    <ol>
      <li><a href="front.xhtml">Title Page</a></li>
      <li><a href="ch01.xhtml">Chapter 1 — Title</a></li>
      <!-- ... -->
    </ol>
  </nav>
  
  <!-- Landmarks nav (required by KDP) -->
  <nav epub:type="landmarks">
    <h2>Landmarks</h2>
    <ol>
      <li><a epub:type="bodymatter" href="ch01.xhtml">Start Reading</a></li>
    </ol>
  </nav>
</body>
</html>
```

## toc.ncx Requirements
```xml
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">
  <head>
    <meta name="dtb:uid" content="urn:uuid:UNIQUE_ID"/>
    <meta name="dtb:depth" content="1"/>
  </head>
  <docTitle><text>Book Title</text></docTitle>
  <navMap>
    <navPoint id="nav-front" playOrder="1">
      <navLabel><text>Title Page</text></navLabel>
      <content src="front.xhtml"/>
    </navPoint>
    <navPoint id="nav-ch01" playOrder="2">
      <navLabel><text>Chapter 1 — Title</text></navLabel>
      <content src="ch01.xhtml"/>
    </navPoint>
    <!-- ... -->
  </navMap>
</ncx>
```

## XHTML Chapter File Requirements
- Valid XML (parseable by `xml.etree.ElementTree`)
- Self-contained XHTML document with `<?xml version="1.0"?>` declaration
- `<!DOCTYPE html>` declaration
- `xmlns="http://www.w3.org/1999/xhtml"` on `<html>` element
- **NO HTML named entities** — use numeric only (`&#8212;` not `&mdash;`)
- **NO bare `&`** — must be `&amp;`
- Self-closing tags: `<br/>`, `<img .../>`, `<hr/>`
- Image paths relative to XHTML: `src="images/ch01.png"`

## Common KDP Rejection Reasons
1. **"Invalid TOC"** — Missing or broken `toc.ncx` or `nav.xhtml`
2. **"Missing landmarks"** — No `epub:type="landmarks"` nav
3. **"XML parsing error"** — Invalid XHTML (named entities, unclosed tags, bare `&`)
4. **"Missing spine items"** — Files in manifest but not in spine
5. **"Duplicate IDs"** — Non-unique `id=` attributes in OPF manifest
6. **"Invalid OPF"** — Missing `toc="ncx"` on `<spine>` element

## Packaging Rules
```python
with zipfile.ZipFile(epub_path, 'w', zipfile.ZIP_DEFLATED) as zf:
    # mimetype MUST be first and uncompressed
    zf.write("mimetype", "mimetype", compress_type=zipfile.ZIP_STORED)
    # All other files
    for root, dirs, files in os.walk(epub_dir):
        for file in files:
            if file == "mimetype": continue
            fp = os.path.join(root, file)
            zf.write(fp, os.path.relpath(fp, epub_dir))
```
