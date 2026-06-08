#!/usr/bin/env python3
"""Build a KDP-compliant EPUB3 + publishing package from an HTML manuscript.
Handles 4+ HTML heading formats for chapter detection.

Usage:
  python3 html-to-epub.py <source_html> <cover_png> <title> <author> <series> <book_num> <output_dir>

Produces:
  - {Key}.epub (EPUB3 with front/back matter, no embedded cover as page)
  - {Key}_Publishing_Package.zip (EPUB + cover PNG/JPEG + back cover text + author bio + README)

Requires: Python stdlib + PIL (Pillow) for cover resize.
"""
import sys, os, re, shutil, zipfile, json
from pathlib import Path
from datetime import datetime
try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

def main():
    if len(sys.argv) < 7:
        print("Usage: html-to-epub.py <source_html> <cover_png> <title> <author> <series> <book_num> <output_dir>")
        sys.exit(1)

    src_html = sys.argv[1]
    cover_png = sys.argv[2]
    title = sys.argv[3]
    author = sys.argv[4]
    series_name = sys.argv[5]
    book_num = sys.argv[6]
    output_dir = Path(sys.argv[7])

    book_key = f"{series_name.replace(' ', '_')}_{book_num}_{title.replace(' ', '_')}"

    print(f"Building: {title} ({series_name} #{book_num})")

    # 1. Read and parse source HTML
    with open(src_html, 'r', encoding='utf-8') as f:
        html_content = f.read()

    body_match = re.search(r'<body[^>]*>(.*?)</body>', html_content, re.DOTALL)
    body = body_match.group(1) if body_match else html_content
    body = re.sub(r'<style[^>]*>.*?</style>', '', body, flags=re.DOTALL)
    body = re.sub(r'<script[^>]*>.*?</script>', '', body, flags=re.DOTALL)

    # 2. Detect chapters across all heading formats
    chapter_pattern = re.compile(
        r'(<h[12][^>]*>(?:Chapter|PART)\s[^<]+</h[12]>)|'
        r'(<div\s+id="ch\d+"[^>]*>\s*<h[12][^>]*>(?:Chapter|PART)\s[^<]+</h[12]>\s*</div>)',
        re.DOTALL | re.IGNORECASE
    )

    chapters = []
    positions = []
    for m in chapter_pattern.finditer(body):
        ch_text = re.sub(r'<[^>]+>', '', m.group(0)).strip()
        ch_text = ch_text.replace('&mdash;', '—').replace('&nbsp;', ' ')
        ch_text = re.sub(r'\s+', ' ', ch_text).strip()
        chapters.append(ch_text)
        positions.append(m.start())

    print(f"  Chapters detected: {len(chapters)}")

    # 3. Split body into chapter sections
    sections = []
    for i, pos in enumerate(positions):
        end = positions[i+1] if i+1 < len(positions) else len(body)
        sections.append((chapters[i], body[pos:end].strip()))

    if not sections:
        sections = [("Full Content", body)]

    # 4. Build EPUB
    epub_dir = output_dir / f"{book_key}_EPUB"
    oebps_dir = epub_dir / "OEBPS"
    images_dir = oebps_dir / "images"
    os.makedirs(images_dir, exist_ok=True)

    # Copy cover
    if os.path.exists(cover_png):
        shutil.copy2(cover_png, images_dir / "cover.png")
        if HAS_PIL:
            img = Image.open(cover_png)
            img = img.resize((1600, 2560), Image.LANCZOS)
            img.save(str(images_dir / "cover.jpg"), "JPEG", quality=95)

    # mimetype + container.xml
    with open(epub_dir / "mimetype", 'w') as f:
        f.write("application/epub+xml")
    os.makedirs(epub_dir / "META-INF", exist_ok=True)
    with open(epub_dir / "META-INF" / "container.xml", 'w') as f:
        f.write('<?xml version="1.0"?>\n<container version="1.0" '
                'xmlns="urn:oasis:names:tc:opendocument:xmlns:container">\n'
                '  <rootfiles>\n    <rootfile full-path="OEBPS/content.opf" '
                'media-type="application/oebps-package+xml"/>\n  </rootfiles>\n</container>\n')

    book_id = f"urn:uuid:{abs(hash(title + author)):032x}"
    year = datetime.now().year

    # Helper: add XHTML file
    manifest, spine = [], []
    counter = [0]
    xhtml_files = []

    def add_xhtml(filename, content, id_prefix=""):
        xhtml = f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">
<head><meta charset="UTF-8"/><link rel="stylesheet" type="text/css" href="style.css"/></head>
<body>{content}</body></html>'''
        with open(oebps_dir / filename, 'w', encoding='utf-8') as f:
            f.write(xhtml)
        counter[0] += 1
        iid = f"{id_prefix or 'item'}{counter[0]}"
        manifest.append(f'    <item id="{iid}" href="{filename}" media-type="application/xhtml+xml"/>')
        spine.append(f'    <itemref idref="{iid}" linear="yes"/>')
        xhtml_files.append(filename)

    # Cover (linear="no"), Title, Copyright, TOC, chapters, About, Series
    add_xhtml("cover.xhtml",
        f'<div class="title-page"><p class="subtitle">{series_name} &bull; Book {book_num}</p>'
        f'<h1>{title}</h1><p class="author">by {author}</p></div>', "cover")
    
    # Fix cover spine linear="no" - need to go back and patch
    # Override the last spine entry
    spine[-1] = spine[-1].replace('linear="yes"', 'linear="no"')
    
    add_xhtml("title.xhtml",
        f'<div class="title-page"><p class="subtitle">{series_name} &bull; Book {book_num}</p>'
        f'<h1>{title}</h1><p class="author">by {author}</p></div>', "title")
    
    add_xhtml("copyright.xhtml",
        f'<div class="copyright-page"><h1>Copyright</h1>'
        f'<p>&copy; {year} {author}. All rights reserved.</p>'
        f'<p>No part of this publication may be reproduced, distributed, or transmitted in any form...</p>'
        f'<p>This is a work of fiction. Any resemblance to actual persons is entirely coincidental.</p>'
        f'<p>Published by MIFECO Publishing</p><p>First Edition: {year}</p></div>', "copy")

    # TOC page
    toc_items = ''.join(f'<li><a href="ch{i+1:03d}.xhtml">{ch}</a></li>' for i, ch in enumerate(chapters))
    add_xhtml("toc.xhtml",
        f'<div class="toc-page"><h1>Contents</h1><ul>{toc_items}</ul>'
        f'<p style="text-align:center;margin-top:2em;font-size:0.85em;color:#666;">'
        f'{series_name} &bull; Book {book_num}</p></div>', "toc")

    # Chapter files
    for i, (header, content) in enumerate(sections):
        ch_id = f"ch{i+1:03d}"
        header_clean = re.sub(r'<[^>]+>', '', header).strip()
        add_xhtml(f"{ch_id}.xhtml", f'<h2>{header_clean}</h2>\n{content}', f"ch{i+1}")

    # About the Author
    add_xhtml("about.xhtml",
        f'<div class="about-author"><h2>About the Author</h2>'
        f'<p>{author} is a writer of speculative fiction exploring humanity\'s future beyond Earth. '
        f'With a background in systems engineering and a lifelong fascination with space exploration, '
        f'their work focuses on the intersection of technology, society, and the human spirit.</p>'
        f'<p>{title} is part of the {series_name} series.</p></div>', "about")

    # Series page
    add_xhtml("series.xhtml",
        f'<div class="series-page"><h2>Also in the {series_name} Series</h2>'
        f'<p><strong>Book {book_num}:</strong> {title}</p>'
        f'<p style="margin-top:2em;font-size:0.85em;color:#666;">Stay tuned for the next book.</p></div>', "series")

    # CSS
    css = """body { font-family: Georgia,'Times New Roman',serif; line-height:1.5; margin:0; padding:0; }
p { text-indent:1.2em; margin:0.3em 0; widows:2; orphans:2; }
h1 { text-align:center; font-size:1.4em; font-weight:bold; page-break-before:always; margin-top:2em; }
h2 { text-align:left; font-size:1.2em; font-weight:bold; page-break-before:always; margin-top:1.5em; }
.title-page { text-align:center; padding-top:30%; page-break-after:always; }
.title-page h1 { font-size:1.6em; page-break-before:avoid; }
.copyright-page { page-break-after:always; font-size:0.85em; margin-top:15%; }
.copyright-page p { text-indent:0; margin:0.5em 0; }
.toc-page { page-break-after:always; }
.toc-page h1 { text-align:center; }
.toc-page ul { list-style:none; padding:0; margin:1em 0; }
.toc-page li { margin:0.4em 0; font-size:0.95em; }
.about-author { page-break-before:always; }
.about-author h2 { text-align:center; }
.series-page { page-break-before:always; }
img { max-width:100%; height:auto; }"""
    with open(oebps_dir / "style.css", 'w') as f:
        f.write(css)

    # OPF
    manifest_items = '\n'.join(manifest)
    spine_items = '\n'.join(spine)
    opf = f'''<?xml version="1.0" encoding="UTF-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="book-id">
<metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
<dc:identifier id="book-id">{book_id}</dc:identifier>
<dc:title>{title}</dc:title>
<dc:creator>{author}</dc:creator>
<dc:language>en</dc:language>
<dc:publisher>MIFECO Publishing</dc:publisher>
<dc:date>{year}-01-01</dc:date>
<meta property="dcterms:modified">{datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")}</meta>
</metadata>
<manifest>
    <item id="style" href="style.css" media-type="text/css"/>
    <item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>
    <item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>
    <item id="cover-img" href="images/cover.png" media-type="image/png" properties="cover-image"/>
{manifest_items}
</manifest>
<spine>
{spine_items}
</spine>
<guide>
    <reference type="cover" title="Cover" href="cover.xhtml"/>
    <reference type="toc" title="Contents" href="toc.xhtml"/>
    <reference type="text" title="Start" href="ch001.xhtml"/>
</guide>
</package>'''
    with open(oebps_dir / "content.opf", 'w', encoding='utf-8') as f:
        f.write(opf)

    # Nav TOC
    nav_links = ''.join(
        f'<li><a href="ch{i+1:03d}.xhtml">{ch}</a></li>' for i, ch in enumerate(chapters))
    nav_xhtml = f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html><html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">
<head><title>Table of Contents</title></head>
<body><nav epub:type="toc"><h1>Table of Contents</h1><ol>
<li><a href="title.xhtml">Title Page</a></li>
<li><a href="copyright.xhtml">Copyright</a></li>
<li><a href="toc.xhtml">Contents</a></li>
{nav_links}
<li><a href="about.xhtml">About the Author</a></li>
<li><a href="series.xhtml">Also in the Series</a></li>
</ol></nav></body></html>'''
    with open(oebps_dir / "nav.xhtml", 'w', encoding='utf-8') as f:
        f.write(nav_xhtml)

    # NCX
    ncx_points = ''
    po = 3
    for i, ch in enumerate(chapters):
        po += 1
        ncx_points += f'''    <navPoint id="nav-ch{i+1:03d}" playOrder="{po}">
      <navLabel><text>{ch}</text></navLabel>
      <content src="ch{i+1:03d}.xhtml"/>
    </navPoint>\n'''
    ncx = f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE ncx PUBLIC "-//NISO//DTD ncx 2005-1//EN" "http://www.daisy.org/z3986/2005/ncx-2005-1.dtd">
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">
<head><meta name="dtb:uid" content="{book_id}"/><meta name="dtb:depth" content="1"/></head>
<docTitle><text>{title}</text></docTitle>
<docAuthor><text>{author}</text></docAuthor>
<navMap>
    <navPoint id="nav-title" playOrder="1"><navLabel><text>Title Page</text></navLabel><content src="title.xhtml"/></navPoint>
    <navPoint id="nav-copyright" playOrder="2"><navLabel><text>Copyright</text></navLabel><content src="copyright.xhtml"/></navPoint>
    <navPoint id="nav-toc" playOrder="3"><navLabel><text>Contents</text></navLabel><content src="toc.xhtml"/></navPoint>
{ncx_points}
    <navPoint id="nav-about" playOrder="{po+1}"><navLabel><text>About the Author</text></navLabel><content src="about.xhtml"/></navPoint>
</navMap>
</ncx>'''
    with open(oebps_dir / "toc.ncx", 'w', encoding='utf-8') as f:
        f.write(ncx)

    # Zip EPUB
    epub_path = output_dir / f"{book_key}.epub"
    with zipfile.ZipFile(epub_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.write(epub_dir / "mimetype", "mimetype", compress_type=zipfile.ZIP_STORED)
        zf.write(epub_dir / "META-INF" / "container.xml", "META-INF/container.xml")
        for root, dirs, files in os.walk(oebps_dir):
            for file in files:
                fp = os.path.join(root, file)
                rel = os.path.relpath(fp, epub_dir)
                zf.write(fp, rel)

    # Back cover text
    with open(output_dir / f"{book_key}_Back_Cover.txt", 'w') as f:
        f.write(f"""{title}\n{series_name} — Book {book_num}\nby {author}\n\n[BACK COVER BLURB]\n\nWhen humanity reaches for the stars, what does it take to build a new world?\n\n{title} is a gripping science fiction novel that explores the challenges, triumphs, and sacrifices of space colonization.\n\nPerfect for fans of hard science fiction and epic space sagas.\n""")

    # Author bio
    with open(output_dir / f"{book_key}_Author_Bio.txt", 'w') as f:
        f.write(f"About {author}\n\n{author} is a writer of speculative fiction exploring humanity's future beyond Earth. {title} is part of the {series_name} series.\n")

    # README
    with open(output_dir / f"{book_key}_README.md", 'w') as f:
        f.write(f"""# {title}\n## {series_name} — Book {book_num}\n\n### Files:\n1. **{book_key}.epub** — Kindle-compatible EPUB3 (no cover embedded internally)\n2. **{book_key}_Cover.png** — Front cover image (for KDP upload)\n3. **{book_key}_Cover.jpg** — Cover at KDP 1600x2560\n4. **{book_key}_Back_Cover.txt** — Back cover blurb\n5. **{book_key}_Author_Bio.txt** — Author biography\n""")

    # Final ZIP package
    pkg_path = output_dir / f"{book_key}_Publishing_Package.zip"
    with zipfile.ZipFile(pkg_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.write(epub_path, f"{book_key}.epub")
        zf.write(output_dir / f"{book_key}_Back_Cover.txt", f"{book_key}_Back_Cover.txt")
        zf.write(output_dir / f"{book_key}_Author_Bio.txt", f"{book_key}_Author_Bio.txt")
        zf.write(output_dir / f"{book_key}_README.md", f"{book_key}_README.md")
        if os.path.exists(cover_png):
            zf.write(cover_png, f"{book_key}_Cover.png")
        jpg = images_dir / "cover.jpg"
        if os.path.exists(jpg):
            zf.write(jpg, f"{book_key}_Cover.jpg")

    print(f"  EPUB: {epub_path}")
    print(f"  Package: {pkg_path}")
    print(f"  ✅ {title} complete")

if __name__ == "__main__":
    main()
