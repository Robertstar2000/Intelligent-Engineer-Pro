#!/usr/bin/env python3
"""
Build a text-only KDP-compliant EPUB3 from a print-formatted HTML file.
No embedded cover images — just front matter + chapters + back matter.
Usage: python3 build-epub-from-html.py <html_path> <title> <author> <book_key> <output_dir>
"""
import sys, os, re, zipfile
from pathlib import Path
from datetime import datetime

if len(sys.argv) < 5:
    print("Usage: build-epub-from-html.py <html_path> <title> <author> <book_key> <output_dir>")
    sys.exit(1)

html_path = Path(sys.argv[1])
TITLE = sys.argv[2]
AUTHOR = sys.argv[3]
BOOK_KEY = sys.argv[4]
OUTPUT = Path(sys.argv[5]) if len(sys.argv) > 5 else Path("output")

html = html_path.read_text(encoding='utf-8')
body_m = re.search(r'<body[^>]*>(.*?)</body>', html, re.DOTALL)
body = body_m.group(1) if body_m else html
body = re.sub(r'<style[^>]*>.*?</style>', '', body, flags=re.DOTALL)

# Find chapter sections
ch_sections = []
for m in re.finditer(r'<h2[^>]*class="chapter-title"[^>]*>.*?</h2>', body, re.DOTALL):
    ch_sections.append(m.group())

# Build EPUB
EPUB_DIR = OUTPUT / f"{BOOK_KEY}_epub"
OEBPS = EPUB_DIR / "OEBPS"
os.makedirs(OEBPS, exist_ok=True)
os.makedirs(EPUB_DIR / "META-INF", exist_ok=True)

with open(EPUB_DIR / "mimetype", 'w') as f: f.write("application/epub+xml")
with open(EPUB_DIR / "META-INF" / "container.xml", 'w') as f:
    f.write('<?xml version="1.0"?><container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">'
            '<rootfiles><rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/></rootfiles></container>')

book_id = f"urn:uuid:{abs(hash(TITLE + AUTHOR)):032x}"

EPUB_CSS = """body { font-family: Georgia,'Times New Roman',serif; line-height:1.5; }
p { text-indent:0; margin:6px 0; widows:2; orphans:2; }
h2 { text-align:center; font-size:1.3em; page-break-before:always; }
.title-page { text-align:center; padding-top:25%; page-break-after:always; }
.copyright-page { page-break-after:always; font-size:0.85em; }
"""
(OEBPS / "style.css").write_text(EPUB_CSS)

manifest, spine = [], []
counter = [0]

def add_item(fn, content, linear="yes"):
    xhtml = f'<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE html><html xmlns="http://www.w3.org/1999/xhtml">'
    xhtml += f'<head><meta charset="UTF-8"/><link rel="stylesheet" type="text/css" href="style.css"/></head><body>{content}</body></html>'
    (OEBPS / fn).write_text(xhtml, encoding='utf-8')
    counter[0] += 1
    iid = f"item{counter[0]}"
    manifest.append(f'<item id="{iid}" href="{fn}" media-type="application/xhtml+xml"/>')
    spine.append(f'<itemref idref="{iid}" linear="{linear}"/>')

add_item("cover.xhtml", f'<div class="title-page"><h1>{TITLE}</h1><p>{AUTHOR}</p></div>', "no")
add_item("title.xhtml", f'<div class="title-page"><h1>{TITLE}</h1><p>{AUTHOR}</p></div>')

# Find chapters in body
ch_positions = [m.start() for m in re.finditer(r'<h2[^>]*class="chapter-title"[^>]*>.*?</h2>', body, re.DOTALL)]
for i, pos in enumerate(ch_positions):
    end = ch_positions[i+1] if i+1 < len(ch_positions) else len(body)
    bm = body.find('<div class="back-matter"', pos)
    if bm > 0 and bm < end: end = bm
    add_item(f"ch{i+1:03d}.xhtml", body[pos:end].strip())

# Nav TOC
nav_items = ''.join(f'<li><a href="ch{i+1:03d}.xhtml">Chapter {i+1}</a></li>' for i in range(len(ch_positions)))
nav_xhtml = f'<?xml version="1.0"?><html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">'
nav_xhtml += f'<head><title>TOC</title></head><body><nav epub:type="toc"><h2>Contents</h2><ol>{nav_items}</ol></nav></body></html>'
(OEBPS / "nav.xhtml").write_text(nav_xhtml)
manifest.append(f'<item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>')

opf = f'''<?xml version="1.0"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="book-id">
<metadata><dc:identifier id="book-id">{book_id}</dc:identifier>
<dc:title>{TITLE}</dc:title><dc:creator>{AUTHOR}</dc:creator><dc:language>en</dc:language>
<dc:publisher>Self-Published</dc:publisher>
<meta property="dcterms:modified">{datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")}</meta></metadata>
<manifest><item id="style" href="style.css" media-type="text/css"/>
{"".join(manifest)}</manifest>
<spine>{"".join(spine)}</spine></package>'''
(OEBPS / "content.opf").write_text(opf)

epub_path = OUTPUT / f"{BOOK_KEY}.epub"
with zipfile.ZipFile(epub_path, 'w', zipfile.ZIP_DEFLATED) as zf:
    zf.write(EPUB_DIR / "mimetype", "mimetype", compress_type=zipfile.ZIP_STORED)
    zf.write(EPUB_DIR / "META-INF" / "container.xml", "META-INF/container.xml")
    for root, dirs, files in os.walk(OEBPS):
        for file in files:
            zf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), EPUB_DIR))
print(f"EPUB: {epub_path} ({epub_path.stat().st_size//1024} KB)")
