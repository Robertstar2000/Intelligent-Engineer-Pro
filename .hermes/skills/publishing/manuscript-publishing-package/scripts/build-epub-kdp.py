#!/usr/bin/env python3
"""
Build a KDP-compliant EPUB3 + publishing package for one book.

Usage:
    python3 build-epub-kdp.py <source_html> <cover_png> <title> <author> <series_name> <book_num> <output_dir>

Output:
    - {key}.epub — KDP-compliant EPUB3 (no cover embedded inside, no thumbnails)
    - {key}_Publishing_Package.zip — full package with EPUB, cover, back cover text, author bio, README

Handles all common HTML heading formats:
    - <h2>Chapter N — Title</h2>            (Built from Dust style)
    - <h1 class="chapter-title">Chapter N — Title</h1>  (Oxygen Gamble style)
    - <h1>Chapter N &mdash; Title</h1>       (Red Charter style)
    - <div id="chN"><h1>Chapter N — Title</h1>  (Moon Rock style)
"""

import sys, os, re, shutil, zipfile, base64
from pathlib import Path
from datetime import datetime
from PIL import Image


def main():
    if len(sys.argv) < 7:
        print(__doc__)
        sys.exit(1)

    src_html = sys.argv[1]
    cover_png = sys.argv[2]
    title = sys.argv[3]
    author = sys.argv[4]
    series_name = sys.argv[5]
    book_num = sys.argv[6]
    output_dir = Path(sys.argv[7])

    key = f"{series_name.replace(' ', '_')}_{book_num}_{title.replace(' ', '_')}"
    print(f"Building: {series_name} #{book_num} — {title}")

    # === READ & PARSE ===
    with open(src_html, 'r', encoding='utf-8') as f:
        html = f.read()

    body_match = re.search(r'<body[^>]*>(.*?)</body>', html, re.DOTALL)
    body = body_match.group(1) if body_match else html
    body = re.sub(r'<style[^>]*>.*?</style>', '', body, flags=re.DOTALL)
    body = re.sub(r'<script[^>]*>.*?</script>', '', body, flags=re.DOTALL)

    # Detect chapters via ANY heading format
    ch_pat = re.compile(
        r'(<h[12][^>]*>(?:Chapter|PART)\s[^<]+</h[12]>)|'
        r'(<div\s+id="ch\d+"[^>]*>\s*<h[12][^>]*>(?:Chapter|PART)\s[^<]+</h[12]>\s*</div>)',
        re.DOTALL | re.IGNORECASE
    )

    chapters, positions = [], []
    for m in ch_pat.finditer(body):
        t = re.sub(r'<[^>]+>', '', m.group(0)).strip()
        t = t.replace('&mdash;', '—').replace('&nbsp;', ' ')
        t = re.sub(r'\s+', ' ', t).strip()
        chapters.append(t)
        positions.append(m.start())

    sections = []
    for i, pos in enumerate(positions):
        end = positions[i+1] if i+1 < len(positions) else len(body)
        sections.append((chapters[i], body[pos:end].strip()))

    print(f"  Chapters: {len(chapters)}")

    # === BUILD EPUB ===
    epub_dir = output_dir / f"{key}_EPUB"
    oebps = epub_dir / "OEBPS"
    images = oebps / "images"
    os.makedirs(images, exist_ok=True)
    os.makedirs(epub_dir / "META-INF", exist_ok=True)

    # Copy cover (for the package, NOT embedded in EPUB content)
    if os.path.exists(cover_png):
        shutil.copy2(cover_png, images / "cover.png")
        try:
            img = Image.open(cover_png)
            img.resize((1600, 2560), Image.LANCZOS).save(str(images / "cover.jpg"), "JPEG", quality=95)
        except Exception:
            pass

    # mimetype
    with open(epub_dir / "mimetype", 'w') as f:
        f.write("application/epub+xml")

    # container.xml
    with open(epub_dir / "META-INF" / "container.xml", 'w') as f:
        f.write('<?xml version="1.0"?>\n')
        f.write('<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">\n')
        f.write('  <rootfiles>\n')
        f.write('    <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>\n')
        f.write('  </rootfiles>\n')
        f.write('</container>\n')

    book_id = f"urn:uuid:{abs(hash(title + author)):032x}"
    year = datetime.now().year

    # KDP-safe CSS
    css = """@namespace h "http://www.w3.org/1999/xhtml";
body { font-family: Georgia,'Times New Roman',serif; line-height:1.5; margin:0; padding:0; }
p { text-indent:1.2em; margin:0.3em 0; widows:2; orphans:2; }
h1 { text-align:center; font-size:1.4em; font-weight:bold; page-break-before:always; margin-top:2em; }
h2 { text-align:left; font-size:1.2em; font-weight:bold; page-break-before:always; margin-top:1.5em; }
.title-page { text-align:center; padding-top:30%; page-break-after:always; }
.title-page h1 { font-size:1.6em; page-break-before:avoid; }
.copyright-page { page-break-after:always; font-size:0.85em; margin-top:15%; }
.copyright-page p { text-indent:0; margin:0.5em 0; }
.toc-page { page-break-after:always; }
.toc-page h1 { text-align:center; font-size:1.4em; }
.toc-page ul { list-style:none; padding:0; margin:1em 0; }
.toc-page li { margin:0.4em 0; font-size:0.95em; }
.about-author { page-break-before:always; }
.about-author h2 { text-align:center; }
img { max-width:100%; height:auto; }"""

    def write_xhtml(filename, content, manifest_refs, spine_refs, id_suf=""):
        xhtml = f'<?xml version="1.0" encoding="UTF-8"?>\n'
        xhtml += '<!DOCTYPE html>\n<html xmlns="http://www.w3.org/1999/xhtml">\n'
        xhtml += f'<head><meta charset="UTF-8"/><link rel="stylesheet" type="text/css" href="style.css"/></head>\n<body>\n{content}\n</body>\n</html>'
        with open(oebps / filename, 'w', encoding='utf-8') as f:
            f.write(xhtml)
        idx = len(manifest_refs) + 1
        manifest_refs.append(f'    <item id="i{idx}" href="{filename}" media-type="application/xhtml+xml"/>')
        spine_refs.append(f'    <itemref idref="i{idx}"/>')
        return idx

    manifest, spine = [], []

    # Cover page (linear="no")
    write_xhtml("cover.xhtml",
        f'<div class="title-page"><p>{series_name} &bull; Book {book_num}</p><h1>{title}</h1><p class="author">by {author}</p></div>',
        manifest, spine)

    # Title page
    write_xhtml("title.xhtml",
        f'<div class="title-page"><p>{series_name} &bull; Book {book_num}</p><h1>{title}</h1><p>by {author}</p></div>',
        manifest, spine)

    # Copyright
    write_xhtml("copyright.xhtml",
        f'<div class="copyright-page"><h1>Copyright</h1><p>&copy; {year} {author}. All rights reserved.</p>'
        f'<p>This is a work of fiction. Names, characters, places, and incidents are either the product of the author\'s imagination or are used fictitiously.</p>'
        f'<p>Published by MIFECO Publishing | First Edition: {year}</p></div>',
        manifest, spine)

    # HTML TOC
    toc_lines = ['<div class="toc-page"><h1>Contents</h1><ul>']
    for i, ch in enumerate(chapters):
        clean = re.sub(r'<[^>]+>', '', ch).strip()
        ch_id = f"ch{i+1:03d}"
        toc_lines.append(f'  <li><a href="{ch_id}.xhtml">{clean}</a></li>')
    toc_lines.append(f'</ul><p style="text-align:center;margin-top:2em;font-size:0.85em;">{series_name} &bull; Book {book_num}</p></div>')

    write_xhtml("toc.xhtml", '\n'.join(toc_lines), manifest, spine)

    # Chapter files
    for i, (header, content) in enumerate(sections):
        ch_id = f"ch{i+1:03d}"
        clean_h = re.sub(r'<[^>]+>', '', header).strip()
        write_xhtml(f"{ch_id}.xhtml", f'<h2>{clean_h}</h2>\n{content}', manifest, spine)

    # About the Author
    write_xhtml("about.xhtml",
        f'<div class="about-author"><h2>About the Author</h2>'
        f'<p>{author} is a writer of speculative fiction exploring humanity\'s future beyond Earth. '
        f'{title} is part of the {series_name} series.</p></div>',
        manifest, spine)

    # Series page
    write_xhtml("series.xhtml",
        f'<div class="about-author"><h2>Also in the {series_name} Series</h2>'
        f'<p><strong>Book {book_num}:</strong> {title}</p></div>',
        manifest, spine)

    # Write CSS
    with open(oebps / "style.css", 'w') as f:
        f.write(css)

    # Nav TOC (EPUB 3)
    nav_entries = []
    for i, ch in enumerate(chapters):
        clean = re.sub(r'<[^>]+>', '', ch).strip()
        nav_entries.append(f'    <li><a href="ch{i+1:03d}.xhtml">{clean}</a></li>')

    nav = f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">
<head><title>Table of Contents</title></head>
<body>
<nav epub:type="toc">
<h1>Table of Contents</h1>
<ol>
<li><a href="title.xhtml">Title Page</a></li>
<li><a href="copyright.xhtml">Copyright</a></li>
<li><a href="toc.xhtml">Contents</a></li>
{chr(10).join(nav_entries)}
<li><a href="about.xhtml">About the Author</a></li>
</ol>
</nav>
</body>
</html>'''
    with open(oebps / "nav.xhtml", 'w', encoding='utf-8') as f:
        f.write(nav)
    manifest.append(f'    <item id="inav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>')

    # NCX (EPUB 2 backward compat)
    ncx_pts = []
    po = 4
    for i, ch in enumerate(chapters):
        clean = re.sub(r'<[^>]+>', '', ch).strip()
        ncx_pts.append(f'''    <navPoint id="n{i+1:03d}" playOrder="{po}">
      <navLabel><text>{clean}</text></navLabel>
      <content src="ch{i+1:03d}.xhtml"/>
    </navPoint>''')
        po += 1

    ncx = f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE ncx PUBLIC "-//NISO//DTD ncx 2005-1//EN" "http://www.daisy.org/z3986/2005/ncx-2005-1.dtd">
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">
<head><meta name="dtb:uid" content="{book_id}"/><meta name="dtb:depth" content="1"/></head>
<docTitle><text>{title}</text></docTitle>
<docAuthor><text>{author}</text></docAuthor>
<navMap>
    <navPoint id="ntitle" playOrder="1"><navLabel><text>Title Page</text></navLabel><content src="title.xhtml"/></navPoint>
    <navPoint id="ncopyright" playOrder="2"><navLabel><text>Copyright</text></navLabel><content src="copyright.xhtml"/></navPoint>
    <navPoint id="ntoc" playOrder="3"><navLabel><text>Contents</text></navLabel><content src="toc.xhtml"/></navPoint>
{chr(10).join(ncx_pts)}
</navMap>
</ncx>'''
    with open(oebps / "toc.ncx", 'w', encoding='utf-8') as f:
        f.write(ncx)
    manifest.append(f'    <item id="incx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>')
    manifest.append(f'    <item id="icss" href="style.css" media-type="text/css"/>')
    manifest.append(f'    <item id="icimg" href="images/cover.png" media-type="image/png" properties="cover-image"/>')

    # content.opf
    opf = f'''<?xml version="1.0" encoding="UTF-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="bid">
<metadata>
<dc:identifier id="bid">{book_id}</dc:identifier>
<dc:title>{title}</dc:title>
<dc:creator>{author}</dc:creator>
<dc:language>en</dc:language>
<dc:publisher>MIFECO Publishing</dc:publisher>
<dc:date>{year}-01-01</dc:date>
<meta property="dcterms:modified">{datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")}</meta>
</metadata>
<manifest>
{chr(10).join(manifest)}
</manifest>
<spine>
{chr(10).join(spine)}
</spine>
<guide>
<reference type="cover" title="Cover" href="cover.xhtml"/>
<reference type="toc" title="Table of Contents" href="toc.xhtml"/>
<reference type="text" title="Start" href="ch001.xhtml"/>
</guide>
</package>'''
    with open(oebps / "content.opf", 'w', encoding='utf-8') as f:
        f.write(opf)

    # === CREATE EPUB ZIP ===
    epub_path = output_dir / f"{key}.epub"
    with zipfile.ZipFile(epub_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.write(epub_dir / "mimetype", "mimetype", compress_type=zipfile.ZIP_STORED)
        zf.write(epub_dir / "META-INF" / "container.xml", "META-INF/container.xml")
        for root, dirs, files in os.walk(oebps):
            for fname in files:
                fp = os.path.join(root, fname)
                rel = os.path.relpath(fp, epub_dir)
                zf.write(fp, rel)
    print(f"  EPUB: {epub_path}")

    # === BACK COVER TEXT ===
    bc = f"""{title}
{series_name} — Book {book_num}
by {author}

[BACK COVER BLURB]

When humanity reaches for the stars, what does it take to build a new world?

ISBN: [TBD]
Cover: MIFECO Publishing
"""
    with open(output_dir / f"{key}_Back_Cover.txt", 'w') as f:
        f.write(bc)

    # === AUTHOR BIO ===
    bio = f"""About {author}

{author} is a writer of speculative fiction exploring humanity's future beyond Earth.
"""
    with open(output_dir / f"{key}_Author_Bio.txt", 'w') as f:
        f.write(bio)

    # === README ===
    readme = f"""# {title}
## {series_name} — Book {book_num}

Files:
1. {key}.epub — KDP-compliant EPUB3 (no embedded cover)
2. {key}_Cover.png — Front cover image
3. {key}_Cover.jpg — Cover at 1600×2560 for KDP upload
4. {key}_Back_Cover.txt — Back cover text
5. {key}_Author_Bio.txt — Author biography

KDP Upload:
1. Upload {key}.epub as manuscript
2. Upload {key}_Cover.jpg as cover
"""
    with open(output_dir / f"{key}_README.md", 'w') as f:
        f.write(readme)

    # === PACKAGE ZIP ===
    pkg = output_dir / f"{key}_Publishing_Package.zip"
    with zipfile.ZipFile(pkg, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.write(epub_path, f"{key}.epub")
        zf.write(output_dir / f"{key}_Back_Cover.txt", f"{key}_Back_Cover.txt")
        zf.write(output_dir / f"{key}_Author_Bio.txt", f"{key}_Author_Bio.txt")
        zf.write(output_dir / f"{key}_README.md", f"{key}_README.md")
        if os.path.exists(cover_png):
            zf.write(cover_png, f"{key}_Cover.png")
        cjpg = images / "cover.jpg"
        if os.path.exists(cjpg):
            zf.write(cjpg, f"{key}_Cover.jpg")
    print(f"  Package: {pkg}")
    print(f"  ✅ {title}")


if __name__ == "__main__":
    main()
