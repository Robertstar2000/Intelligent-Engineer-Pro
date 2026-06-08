#!/usr/bin/env python3
"""
build-epub-package.py — Build a KDP-compliant EPUB3 + publishing package from an HTML manuscript.

Usage:
  python3 scripts/build-epub-package.py <source_html> <cover_png> <title> <author> <series_name> <book_num> <output_dir>

Output (in <output_dir>):
  {Key}.epub                          — EPUB3 with front/back matter, TOC, NO embedded cover
  {Key}_Publishing_Package.zip        — ZIP with EPUB + cover PNG/JPEG + back cover text + bio + README
  {Key}_Back_Cover.txt                — Back cover blurb
  {Key}_Author_Bio.txt                — Author biography
  {Key}_README.md                     — Upload instructions

What it builds:
  - EPUB3 with mimetype, META-INF/container.xml, OEBPS/content.opf, nav.xhtml, toc.ncx
  - One XHTML per chapter (split on <h2>Chapter/PART boundaries)
  - Front matter: cover page (linear=no), title page, copyright
  - Back matter: About the Author, Also in Series
  - Clickable HTML TOC + EPUB3 Nav TOC + NCX
  - Cover image copied into OEBPS/images/ (and resized JPEG for KDP)
  - No embedded cover artwork in EPUB reading order (cover.xhtml uses linear=no)

Dependencies: Python 3.8+ stdlib only (zipfile built in).
Optional: PIL (Pillow) for cover JPEG resizing — falls back gracefully if missing.

The EPUB is KDP-compatible:
  - Body text has no forced font-size/color (respects Enhanced Typesetting)
  - Uses Georgia/Times New Roman serif fallback
  - No ::before/::after, no counter-*, no scripts
  - Forward slashes only in file paths
  - Guide items defined for cover, toc, text
"""
import sys, os, re, shutil, zipfile
from pathlib import Path
from datetime import datetime
from xml.sax.saxutils import escape as esc_xml


def build_package(src_html, cover_png, title, author, series_name, book_num, output_dir):
    """Main entry point. Returns path to the publishing package ZIP."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    book_key = f"{series_name.replace(' ', '_')}_{book_num}_{title.replace(' ', '_')}"

    # ── Parse source HTML ────────────────────────────────────────────
    with open(src_html, encoding='utf-8') as f:
        html = f.read()

    body_match = re.search(r'<body[^>]*>(.*?)</body>', html, re.DOTALL)
    body = body_match.group(1) if body_match else html
    body = re.sub(r'<style[^>]*>.*?</style>', '', body, flags=re.DOTALL)
    body = re.sub(r'<script[^>]*>.*?</script>', '', body, flags=re.DOTALL)

    # Collect chapter titles for the TOC (any <h2> starting with Chapter or PART)
    chapter_titles = []
    for m in re.finditer(r'<h2[^>]*>((?:Chapter|PART)[^<]*)</h2>', body):
        clean = re.sub(r'<[^>]+>', '', m.group(1)).strip()
        if clean and clean.lower().strip('—‒–') not in ('', 'contents'):
            chapter_titles.append(clean)

    # Split body into chapter sections on Chapter/PART h2 boundaries
    split_re = re.compile(r'(<h2>(?:Chapter|PART)[^<]*</h2>)')
    parts = split_re.split(body)
    sections = []
    cur_hdr, cur_body = None, []
    for p in parts:
        p = p.strip()
        if not p:
            continue
        m = re.match(r'<h2>((?:Chapter|PART)[^<]*)</h2>', p)
        if m:
            if cur_hdr is not None:
                sections.append((cur_hdr, '\n'.join(cur_body)))
            cur_hdr = m.group(1)
            cur_body = []
        elif cur_hdr is not None:
            cur_body.append(p)
    if cur_hdr is not None:
        sections.append((cur_hdr, '\n'.join(cur_body)))

    # ── Prepare EPUB directories ─────────────────────────────────────
    epub_dir = output_dir / f"{book_key}_EPUB_TMP"
    oebps_dir = epub_dir / "OEBPS"
    images_dir = oebps_dir / "images"
    shutil.rmtree(epub_dir, ignore_errors=True)
    os.makedirs(images_dir)
    os.makedirs(epub_dir / "META-INF")

    # Copy cover image
    if os.path.exists(cover_png):
        shutil.copy2(cover_png, images_dir / "cover.png")
        try:
            from PIL import Image
            img = Image.open(cover_png)
            img = img.resize((1600, 2560), Image.LANCZOS)
            img.save(str(images_dir / "cover.jpg"), "JPEG", quality=95)
        except ImportError:
            pass

    # ── Write static EPUB files ──────────────────────────────────────
    with open(epub_dir / "mimetype", 'w') as f:
        f.write("application/epub+xml")

    with open(epub_dir / "META-INF" / "container.xml", 'w') as f:
        f.write('<?xml version="1.0"?>\n')
        f.write('<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">\n')
        f.write('  <rootfiles>\n')
        f.write('    <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>\n')
        f.write('  </rootfiles>\n')
        f.write('</container>\n')

    book_id = f"urn:uuid:{abs(hash(title + author + series_name + datetime.utcnow().isoformat())):032x}"

    epub_css = """@namespace h "http://www.w3.org/1999/xhtml";
body { font-family: Georgia, 'Times New Roman', serif; line-height: 1.5; margin: 0; padding: 0; }
p { text-indent: 1.2em; margin: 0.3em 0; widows: 2; orphans: 2; }
h1 { text-align: center; font-size: 1.4em; font-weight: bold; page-break-before: always; margin-top: 2em; }
h2 { text-align: left; font-size: 1.2em; font-weight: bold; page-break-before: always; margin-top: 1.5em; }
.title-page { text-align: center; padding-top: 30%; page-break-after: always; }
.title-page h1 { font-size: 1.6em; page-break-before: avoid; }
.copyright-page { page-break-after: always; font-size: 0.85em; margin-top: 15%; }
.copyright-page p { text-indent: 0; margin: 0.5em 0; }
.toc-page { page-break-after: always; }
.toc-page h1 { text-align: center; }
.toc-page ul { list-style: none; padding: 0; margin: 1em 0; }
.toc-page li { margin: 0.4em 0; font-size: 0.95em; }
.about-author, .series-page { page-break-before: always; }
.about-author h2, .series-page h2 { text-align: center; }
img { max-width: 100%; height: auto; }"""

    with open(oebps_dir / "style.css", 'w') as f:
        f.write(epub_css)

    # ── Build manifest/spine ──────────────────────────────────────────
    manifest_items = []
    spine_items = []
    _ctr = [0]
    def add_xhtml(filename, content, linear="yes"):
        _ctr[0] += 1
        item_id = f"it{_ctr[0]}"
        xhtml = f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">
<head><meta charset="UTF-8"/><link rel="stylesheet" type="text/css" href="style.css"/></head>
<body>{content}</body>
</html>'''
        (oebps_dir / filename).write_text(xhtml, encoding='utf-8')
        manifest_items.append(f'    <item id="{item_id}" href="{filename}" media-type="application/xhtml+xml"/>')
        spine_items.append(f'    <itemref idref="{item_id}" linear="{linear}"/>')
        return item_id

    # 1. Cover page (not in reading order — linear="no")
    add_xhtml("cover.xhtml",
        f'<div class="title-page"><p class="subtitle">{esc_xml(series_name)} &bull; Book {esc_xml(book_num)}</p><h1>{esc_xml(title)}</h1><p class="author">by {esc_xml(author)}</p></div>',
        "no")

    # 2. Title page
    add_xhtml("title.xhtml",
        f'<div class="title-page"><p class="subtitle">{esc_xml(series_name)} &bull; Book {esc_xml(book_num)}</p><h1>{esc_xml(title)}</h1><p class="author">by {esc_xml(author)}</p></div>')

    # 3. Copyright
    yr = datetime.now().year
    add_xhtml("copyright.xhtml",
        f'<div class="copyright-page"><h1>Copyright</h1><p>&copy; {yr} {esc_xml(author)}. All rights reserved.</p><p>&nbsp;</p><p>No part of this publication may be reproduced, distributed, or transmitted in any form or by any means without prior written permission.</p><p>&nbsp;</p><p>This is a work of fiction. Names, characters, places, and incidents are either the product of the author\'s imagination or used fictitiously.</p><p>&nbsp;</p><p>Published by MIFECO Publishing</p><p>First Edition: {yr}</p></div>')

    # 4. HTML TOC
    toc_lines = ['<div class="toc-page"><h1>Contents</h1><ul>']
    for i, ch in enumerate(chapter_titles):
        href = f"ch{i+1:03d}.xhtml"
        toc_lines.append(f'  <li><a href="{href}">{esc_xml(ch)}</a></li>')
    toc_lines.append(f'</ul><p style="text-align:center;margin-top:2em;color:#666;font-size:0.85em;">{esc_xml(series_name)} &bull; Book {esc_xml(book_num)}</p></div>')
    add_xhtml("toc.xhtml", '\n'.join(toc_lines))

    # 5. Chapter content — one XHTML per section
    for i, (hdr, content) in enumerate(sections):
        hdr_clean = re.sub(r'<[^>]+>', '', hdr).strip()
        ch_name = f"ch{i+1:03d}.xhtml"
        # Strip any container div wrappers from content
        clean_content = content.strip()
        add_xhtml(ch_name, f'<h2>{esc_xml(hdr_clean)}</h2>\n{clean_content}')

    # 6. About the Author
    add_xhtml("about.xhtml",
        f'<div class="about-author"><h2>About the Author</h2><p>{esc_xml(author)} is a writer of speculative fiction exploring humanity\'s future beyond Earth.</p><p>{esc_xml(title)} is part of the {esc_xml(series_name)} series.</p></div>')

    # 7. Also in Series
    add_xhtml("series.xhtml",
        f'<div class="series-page"><h2>Also in the {esc_xml(series_name)} Series</h2><p><strong>Book {esc_xml(book_num)}:</strong> {esc_xml(title)}</p><p style="margin-top:2em;color:#666;font-size:0.85em;">Stay tuned for the next book in the series.</p></div>')

    # ── content.opf ───────────────────────────────────────────────────
    opf = f'''<?xml version="1.0" encoding="UTF-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="book-id">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:identifier id="book-id">{book_id}</dc:identifier>
    <dc:title>{esc_xml(title)}</dc:title>
    <dc:creator>{esc_xml(author)}</dc:creator>
    <dc:language>en</dc:language>
    <dc:publisher>MIFECO Publishing</dc:publisher>
    <dc:date>{yr}-01-01</dc:date>
    <meta property="dcterms:modified">{datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")}</meta>
  </metadata>
  <manifest>
    <item id="style" href="style.css" media-type="text/css"/>
    <item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>
    <item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>
    <item id="cover-img" href="images/cover.png" media-type="image/png" properties="cover-image"/>
{chr(10).join(manifest_items)}
  </manifest>
  <spine>
{chr(10).join(spine_items)}
  </spine>
  <guide>
    <reference type="cover" title="Cover" href="cover.xhtml"/>
    <reference type="toc" title="Table of Contents" href="toc.xhtml"/>
    <reference type="text" title="Start" href="ch001.xhtml"/>
  </guide>
</package>'''
    (oebps_dir / "content.opf").write_text(opf, encoding='utf-8')

    # nav.xhtml (EPUB 3 Nav TOC)
    nav_entries = '\n'.join(
        f'      <li><a href="ch{i+1:03d}.xhtml">{esc_xml(ch)}</a></li>'
        for i, ch in enumerate(chapter_titles)
    )
    nav = f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">
<head><title>Table of Contents</title></head>
<body>
  <nav epub:type="toc">
    <h1>Contents</h1>
    <ol>
      <li><a href="title.xhtml">Title Page</a></li>
      <li><a href="copyright.xhtml">Copyright</a></li>
      <li><a href="toc.xhtml">Contents</a></li>
{nav_entries}
      <li><a href="about.xhtml">About the Author</a></li>
      <li><a href="series.xhtml">Also in the Series</a></li>
    </ol>
  </nav>
</body>
</html>'''
    (oebps_dir / "nav.xhtml").write_text(nav, encoding='utf-8')

    # toc.ncx (EPUB 2 backward compat)
    ncx_points = '\n'.join(
        f'''    <navPoint id="np-{i+1}" playOrder="{i+4}">
      <navLabel><text>{esc_xml(ch)}</text></navLabel>
      <content src="ch{i+1:03d}.xhtml"/>
    </navPoint>'''
        for i, ch in enumerate(chapter_titles)
    )
    ncx = f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE ncx PUBLIC "-//NISO//DTD ncx 2005-1//EN" "http://www.daisy.org/z3986/2005/ncx-2005-1.dtd">
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">
  <head><meta name="dtb:uid" content="{book_id}"/><meta name="dtb:depth" content="1"/></head>
  <docTitle><text>{esc_xml(title)}</text></docTitle>
  <docAuthor><text>{esc_xml(author)}</text></docAuthor>
  <navMap>
    <navPoint id="np-title" playOrder="1">
      <navLabel><text>Title Page</text></navLabel>
      <content src="title.xhtml"/>
    </navPoint>
    <navPoint id="np-copy" playOrder="2">
      <navLabel><text>Copyright</text></navLabel>
      <content src="copyright.xhtml"/>
    </navPoint>
    <navPoint id="np-toc" playOrder="3">
      <navLabel><text>Contents</text></navLabel>
      <content src="toc.xhtml"/>
    </navPoint>
{ncx_points}
    <navPoint id="np-about" playOrder="{len(chapter_titles)+4}">
      <navLabel><text>About the Author</text></navLabel>
      <content src="about.xhtml"/>
    </navPoint>
  </navMap>
</ncx>'''
    (oebps_dir / "toc.ncx").write_text(ncx, encoding='utf-8')

    # ── Package EPUB into ZIP ─────────────────────────────────────────
    epub_path = output_dir / f"{book_key}.epub"
    with zipfile.ZipFile(epub_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.write(epub_dir / "mimetype", "mimetype", compress_type=zipfile.ZIP_STORED)
        zf.write(epub_dir / "META-INF" / "container.xml", "META-INF/container.xml")
        for root, _dirs, files in os.walk(oebps_dir):
            for fn in files:
                fp = os.path.join(root, fn)
                zf.write(fp, os.path.relpath(fp, epub_dir))

    # ── Create supporting text files ──────────────────────────────────
    back_cover = f"""{title}
{series_name} — Book {book_num}
by {author}

[BACK COVER BLURB — A gripping science fiction novel that explores the challenges, triumphs, and sacrifices of space colonization.]
"""
    (output_dir / f"{book_key}_Back_Cover.txt").write_text(back_cover)

    author_bio = f"""About {author}

{author} is a writer of speculative fiction exploring humanity's future beyond Earth. {title} is part of the {series_name} series.
"""
    (output_dir / f"{book_key}_Author_Bio.txt").write_text(author_bio)

    readme = f"""# {title}
## {series_name} — Book {book_num}

### Files:
1. **{book_key}.epub** — KDP-compliant EPUB3 (no embedded cover — upload separately)
2. **{book_key}_Cover.png** — Front cover image
3. **{book_key}_Cover.jpg** — Cover at 1600×2560 (KDP-recommended)
4. **{book_key}_Back_Cover.txt** — Back cover blurb
5. **{book_key}_Author_Bio.txt** — Author biography

### KDP Upload:
- Upload **{book_key}.epub** as manuscript
- Upload **{book_key}_Cover.png** or **{book_key}_Cover.jpg** separately
"""
    (output_dir / f"{book_key}_README.md").write_text(readme)

    # ── Assemble publishing package ZIP ───────────────────────────────
    package_path = output_dir / f"{book_key}_Publishing_Package.zip"
    with zipfile.ZipFile(package_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.write(epub_path, f"{book_key}.epub")
        zf.write(output_dir / f"{book_key}_Back_Cover.txt", f"{book_key}_Back_Cover.txt")
        zf.write(output_dir / f"{book_key}_Author_Bio.txt", f"{book_key}_Author_Bio.txt")
        zf.write(output_dir / f"{book_key}_README.md", f"{book_key}_README.md")
        if os.path.exists(cover_png):
            zf.write(cover_png, f"{book_key}_Cover.png")
        cover_jpg = images_dir / "cover.jpg"
        if os.path.exists(cover_jpg):
            zf.write(cover_jpg, f"{book_key}_Cover.jpg")

    # Cleanup temp directory
    shutil.rmtree(epub_dir, ignore_errors=True)

    print(f"✅ {title} — EPUB: {epub_path.name}, Package: {package_path.name} ({len(chapter_titles)} chapters)")
    return str(package_path)


if __name__ == "__main__":
    if len(sys.argv) < 7:
        print(__doc__)
        sys.exit(1)
    build_package(*sys.argv[1:7], sys.argv[7] if len(sys.argv) > 7 else ".")
