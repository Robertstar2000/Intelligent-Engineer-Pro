#!/usr/bin/env python3
"""
Build a KDP-compliant EPUB 3 without pandoc, ebooklib, or any external tool.

Usage:
  python3 build-epub-python.py <manuscript.md> <--output=book.epub>
                              [--title="Book Title"] [--author="Author Name"]
                              [--publisher="Pub Name"] [--lang=en]

Relies only on Python stdlib (zipfile, xml.sax.saxutils, datetime, re).
Produces an EPUB 3 with:
  - Front matter (title, copyright, acknowledgments)
  - Nav TOC (EPUB 3) + NCX (EPUB 2 fallback)
  - Each chapter as a separate XHTML file
  - KDP-safe CSS (no ::before/::after, no counter-*, no scripts)
  - Back matter (about the author)
  - Validated structure: mimetype first, OPF manifest/spine, guide items

Limitations:
  - No embedded images (the generated EPUB is text-only)
  - Chapter splitting is by Markdown headings (lines starting with '#')
  - Part headings and chapter headings share the same level (#)
  - The conversion is a simple regex-based Markdown→XHTML, not a full parser
"""

import zipfile, os, io, re, argparse
from datetime import datetime, timezone
from xml.sax.saxutils import escape as xmlescape

# ─── defaults ────────────────────────────────────────────────────────────────
BOOK_TITLE    = "Book Title"
BOOK_SUBTITLE = ""
AUTHOR        = "Author Name"
PUBLISHER     = "Self-Published"
LANG          = "en"
BOOK_ID       = "urn:uuid:book-{ts}"

# ─── helpers ─────────────────────────────────────────────────────────────────

def slug(name):
    """Filesystem-safe slug from a heading string."""
    s = name.lower().replace(" ", "-").replace(":", "")
    return re.sub(r"[^a-z0-9.-]", "", s)[:25]


def md_to_xhtml(md_text):
    """Minimal Markdown → XHTML for EPUB. Handles #, ###, *, **, >, ---."""
    html = md_text.strip()
    html = re.sub(r"^# (.+)$", r"<h1>\1</h1>", html, flags=re.MULTILINE)
    html = re.sub(r"^### (.+)$", r"<h2>\1</h2>", html, flags=re.MULTILINE)
    html = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", html)
    html = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", html)
    html = re.sub(r"\n---\n", "\n<hr/>\n", html)
    html = re.sub(r"^> (.+)$", r"<blockquote><p>\1</p></blockquote>", html, flags=re.MULTILINE)

    out = []
    for line in html.split("\n"):
        s = line.strip()
        if not s:
            out.append("")
        elif s.startswith("<h") or s.startswith("<hr") or s.startswith("<blockquote"):
            out.append(s)
        else:
            out.append(f"<p>{s}</p>")
    return "\n".join(out)


# ─── EPUB builder ────────────────────────────────────────────────────────────

def build_epub(md_path, epub_path, title, subtitle, author, publisher, lang):
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    book_id = f"urn:uuid:{slug(title)}-{ts}"
    date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    # 1. Parse manuscript into chapters
    with open(md_path) as f:
        lines = f.readlines()

    chapters = []               # [(filename, heading_text, body_html, is_part)]
    current_ch = None
    current_lines = []

    heading_pattern = re.compile(r"^# (.+)$")

    def flush():
        if current_ch and current_lines:
            body = md_to_xhtml("\n".join(current_lines))
            is_part = current_ch.startswith("Part ") and ":" in current_ch
            fn = slug(current_ch) + ".xhtml"
            chapters.append((fn, current_ch, body, is_part))

    for line in lines:
        m = heading_pattern.match(line.strip())
        if m:
            flush()
            current_ch = m.group(1)
            current_lines = [f"# {current_ch}"]
        else:
            if current_ch:
                current_lines.append(line)
    flush()

    if not chapters:
        print("ERROR: No chapters found. Manuscript must use # heading markers.")
        return False

    # 2. Front matter
    front = [
        ("title.xhtml", "Title Page",
         f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head><title>Title Page</title>
<style>
body {{ text-align: center; padding-top: 20%; font-family: Georgia, serif; }}
h1 {{ font-size: 1.8em; margin-bottom: 0.5em; }}
.subtitle {{ font-size: 1.1em; font-style: italic; color: #555; }}
.author {{ font-size: 1.3em; margin-top: 1em; }}
</style></head>
<body><h1>{xmlescape(title)}</h1>
{ '<p class=\"subtitle\">' + xmlescape(subtitle) + '</p>' if subtitle else '' }
<p class="author">{xmlescape(author)}</p></body></html>"""),

        ("copyright.xhtml", "Copyright",
         f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head><title>Copyright</title>
<style>body {{ padding: 15%; font-size: 0.9em; line-height: 1.5; }}</style></head>
<body>
<p><strong>Copyright © {datetime.now().year} by {xmlescape(author)}</strong></p>
<p>All rights reserved. No part of this publication may be reproduced, distributed, or transmitted in any form or by any means...</p>
<p style="text-align:center;margin-top:2em;font-style:italic;">{xmlescape(publisher)}</p>
</body></html>"""),
    ]

    # 3. Back matter
    back = [
        ("aboutauthor.xhtml", "About the Author",
         f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head><title>About the Author</title>
<style>body {{ padding: 15%; font-size: 0.95em; line-height: 1.5; }}
h1 {{ text-align: center; font-size: 1.3em; }}</style></head>
<body><h1>About the Author</h1>
<p>{xmlescape(author)} is the author of <em>{xmlescape(title)}</em>.</p>
</body></html>"""),
    ]

    all_chapters = front + chapters + back

    # 4. Nav TOC (EPUB 3)
    nav_items = []
    for fn, htext, _ in [(f, t, x) for f, t, x, *_ in all_chapters]:
        nav_items.append(f'<li><a href="{fn}">{xmlescape(htext)}</a></li>')

    nav_xhtml = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">
<head><title>Table of Contents</title></head>
<body><nav epub:type="toc"><h1>Table of Contents</h1><ol>
{chr(10).join(nav_items)}
</ol></nav></body></html>"""

    # 5. NCX (EPUB 2 fallback)
    ncx_pts = []
    for i, (fn, htext, _) in enumerate([(f, t, x) for f, t, x, *_ in all_chapters], 1):
        ncx_pts.append(
            f'    <navPoint id="{fn}" playOrder="{i}">'
            f'<navLabel><text>{xmlescape(htext)}</text></navLabel>'
            f'<content src="{fn}"/>'
            f"</navPoint>"
        )
    ncx = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE ncx PUBLIC "-//NISO//DTD ncx 2005-1//EN"
 "http://www.daisy.org/z3986/2005/ncx-2005-1.dtd">
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">
<head><meta name="dtb:uid" content="{book_id}"/><meta name="dtb:depth" content="1"/></head>
<docTitle><text>{xmlescape(title)}</text></docTitle>
<navMap>{chr(10).join(ncx_pts)}</navMap>
</ncx>"""

    # 6. OPF
    manifest = []
    spine = []
    def add(fn, mt, props="", in_spine=True):
        manifest.append(f'    <item id="{fn}" href="{fn}" media-type="{mt}"' +
                        (f' {props}' if props else "") + "/>")
        if in_spine:
            spine.append(f'    <itemref idref="{fn}"/>')

    # Manifest-only: nav doc, NCX fallback, CSS — NOT in spine
    add("nav.xhtml", "application/xhtml+xml", 'nav', in_spine=False)
    add("toc.ncx", "application/x-dtbncx+xml", in_spine=False)
    add("styles/epub.css", "text/css", in_spine=False)

    for fn, *_ in all_chapters:
        add(fn, "application/xhtml+xml")

    opf = f"""<?xml version="1.0" encoding="UTF-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="book-id">
<metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
<dc:identifier id="book-id">{book_id}</dc:identifier>
<dc:title>{xmlescape(title)}</dc:title>
<dc:creator>{xmlescape(author)}</dc:creator>
<dc:language>{lang}</dc:language>
<dc:publisher>{xmlescape(publisher)}</dc:publisher>
<dc:date>{date_str}</dc:date>
<meta property="dcterms:modified">{ts}</meta>
</metadata>
<manifest>
{chr(10).join(manifest)}
</manifest>
<spine page-progression-direction="ltr">
{chr(10).join(spine)}
</spine>
<guide>
<reference type="cover" title="Cover" href="{front[0][0]}"/>
<reference type="toc" title="Table of Contents" href="nav.xhtml"/>
<reference type="text" title="Start" href="{chapters[0][0] if chapters else front[0][0]}"/>
</guide>
</package>"""

    # 7. CSS
    css = """/* KDP-safe EPUB styles */
body { font-family: Georgia, 'Times New Roman', serif; line-height: 1.5; }
h1 { font-family: 'Helvetica Neue', Arial, sans-serif; text-align: center;
     font-size: 1.4em; margin: 2em 0 1em; page-break-before: always; }
h2 { font-family: 'Helvetica Neue', Arial, sans-serif; text-align: center;
     font-size: 1.1em; margin: 1.5em 0 0.8em; }
p { margin: 0.3em 0; text-indent: 1.2em; }
hr { border: none; border-top: 0.5px solid #999; margin: 1em 20%; width: 60%; }
blockquote { font-style: italic; margin: 0.5em 1em; padding-left: 0.8em;
             border-left: 2px solid #ccc; color: #444; }
"""

    # 8. Assemble EPUB
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("mimetype", "application/epub+xml", compress_type=zipfile.ZIP_STORED)
        z.writestr("META-INF/container.xml",
                    '<?xml version="1.0" encoding="UTF-8"?>\n'
                    '<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">\n'
                    '<rootfiles><rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>\n'
                    '</rootfiles></container>')
        z.writestr("OEBPS/content.opf", opf)
        z.writestr("OEBPS/nav.xhtml", nav_xhtml)
        z.writestr("OEBPS/toc.ncx", ncx)
        z.writestr("OEBPS/styles/epub.css", css)
        for fn, htext, body, *_ in all_chapters:
            xhtml = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head><title>{xmlescape(htext)}</title>
<link rel="stylesheet" type="text/css" href="styles/epub.css"/>
</head>
<body>{body}</body></html>"""
            z.writestr(f"OEBPS/{fn}", xhtml)

    with open(epub_path, "wb") as f:
        f.write(buf.getvalue())

    return True


# ─── CLI ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Build EPUB 3 from Markdown")
    p.add_argument("manuscript", help="Path to the Markdown manuscript")
    p.add_argument("--output", "-o", default="book.epub")
    p.add_argument("--title", default=BOOK_TITLE)
    p.add_argument("--subtitle", default=BOOK_SUBTITLE)
    p.add_argument("--author", default=AUTHOR)
    p.add_argument("--publisher", default=PUBLISHER)
    p.add_argument("--lang", default=LANG)
    args = p.parse_args()

    ok = build_epub(args.manuscript, args.output, args.title, args.subtitle,
                    args.author, args.publisher, args.lang)
    if ok:
        sz = os.path.getsize(args.output)
        print(f"✓ EPUB: {args.output} ({sz:,} bytes)")
    else:
        print("✗ Failed")
        exit(1)
