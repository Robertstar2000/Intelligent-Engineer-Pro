#!/usr/bin/env python3
"""
Build EPUB + PDF for a reader magnet novella from a markdown source file.
Outputs to the website magnets directory for deployment.

Usage:
  cd /home/bob/cindy-lou-series/books-mifeco-website
  python3 /path/to/build_reader_magnet.py

Config vars at the top of the file:
  NOVELLA_MD  — path to the markdown source
  MAGNETS_DIR — output directory for website magnets
  TITLE       — book title
  SUBTITLE    — book subtitle
  AUTHOR      — author name
"""

import os, re, io, zipfile
from datetime import datetime, timezone
from xml.sax.saxutils import escape as xmlescape

# --- CONFIGURE THESE ---
NOVELLA_MD = "/home/bob/cindy-lou-series/reader-magnet/Missing_Retainer_Novella.md"
MAGNETS_DIR = "/home/bob/cindy-lou-series/books-mifeco-website/magnets"
OUTPUT_DIR = "/home/bob/cindy-lou-series/reader-magnet/output"

TITLE = "Cindy Lou and the Case of the Missing Retainer"
SUBTITLE = "A Cindy Lou Legal Caper Novella"
AUTHOR = "Bob J Mills"
LANG = "en"
PUBLISHER = "MIFECO"
YEAR = datetime.now().year

os.makedirs(MAGNETS_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)


def slug(name):
    s = name.lower().replace(" ", "-").replace(":", "").replace(",", "").replace("'", "")
    return re.sub(r"[^a-z0-9.-]", "", s)[:40]


# ===================== EPUB BUILDER =====================

CSS_EPUB = """body { font-family: Georgia, 'Times New Roman', serif; line-height: 1.5; margin: 5%; }
h1 { font-family: 'Helvetica Neue', Arial, sans-serif; text-align: center; font-size: 1.4em; margin: 2em 0 1em; page-break-before: always; }
h2 { font-family: 'Helvetica Neue', Arial, sans-serif; text-align: center; font-size: 1.1em; margin: 1.5em 0 0.8em; }
h3 { font-family: 'Helvetica Neue', Arial, sans-serif; font-size: 1.0em; margin: 1.2em 0 0.6em; }
p { margin: 0.3em 0; text-indent: 1.2em; }
hr { border: none; border-top: 0.5px solid #999; margin: 1em 20%; width: 60%; }
.scene { text-align: center; margin: 1em 0; }
blockquote { font-style: italic; margin: 0.5em 1em; padding-left: 0.8em; border-left: 2px solid #ccc; color: #444; }
.center { text-align: center; }
.subtitle { text-align: center; font-style: italic; margin-bottom: 2em; }
.author-line { text-align: center; font-variant: small-caps; }
"""


def md_to_xhtml_body(md_text):
    html = md_text.strip()
    html = re.sub(r"^---$", '<hr/>', html, flags=re.MULTILINE)
    html = re.sub(r"^### (.+)$", r"<h3>\1</h3>", html, flags=re.MULTILINE)
    html = re.sub(r"^## (.+)$", r"<h2>\1</h2>", html, flags=re.MULTILINE)
    html = re.sub(r"^# (.+)$", r"<h1>\1</h1>", html, flags=re.MULTILINE)
    html = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", html)
    html = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", html)
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


def build_epub():
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    book_id = f"urn:uuid:{slug(TITLE)}-{ts}"

    with open(NOVELLA_MD, encoding='utf-8') as f:
        content = f.read()

    sections = []
    current_heading = None
    current_lines = []
    for line in content.split("\n"):
        stripped = line.strip()
        if stripped.startswith("# ") or stripped.startswith("## "):
            if current_heading:
                sections.append((current_heading, "\n".join(current_lines)))
            current_heading = stripped.lstrip("#").strip()
            current_lines = []
        else:
            current_lines.append(line)
    if current_heading:
        sections.append((current_heading, "\n".join(current_lines)))

    chapters = []
    front_matter = []
    back_matter = []
    for heading, body in sections:
        h_lower = heading.lower()
        if any(x in h_lower for x in ["title", "copyright", "table of contents"]):
            front_matter.append((heading, body))
        elif any(x in h_lower for x in ["thank you", "also by", "about the author", "connect", "ai disclosure"]):
            back_matter.append((heading, body))
        elif "chapter" in h_lower or "epilogue" in h_lower:
            chapters.append((heading, body))
        elif heading.strip():
            chapters.append((heading, body))

    print(f"  EPUB: {len(chapters)} chapters, {len(front_matter)} front, {len(back_matter)} back")

    def make_xhtml(fn, heading, body_html, nav_label=None):
        label = nav_label or heading
        return (f'<?xml version="1.0" encoding="UTF-8"?>\n'
                f'<!DOCTYPE html>\n'
                f'<html xmlns="http://www.w3.org/1999/xhtml">\n'
                f'<head><title>{xmlescape(label)}</title>\n'
                f'<link rel="stylesheet" type="text/css" href="styles/epub.css"/>\n'
                f'</head>\n'
                f'<body>{body_html}</body></html>')

    def make_toc_item(fn, label):
        return f'<li><a href="{fn}">{xmlescape(label)}</a></li>'

    all_files = []
    for heading, body in front_matter:
        fn = slug(heading) + ".xhtml"
        body_html = md_to_xhtml_body(body)
        all_files.append((fn, heading, body_html))
    for heading, body in chapters:
        fn = slug(heading) + ".xhtml"
        body_html = md_to_xhtml_body(body)
        all_files.append((fn, heading, body_html))
    for heading, body in back_matter:
        fn = slug(heading) + ".xhtml"
        body_html = md_to_xhtml_body(body)
        all_files.append((fn, heading, body_html))

    toc_items = "\n".join(make_toc_item(fn, h) for fn, h, _ in all_files)
    nav_xhtml = (f'<?xml version="1.0" encoding="UTF-8"?>\n'
                 f'<!DOCTYPE html>\n'
                 f'<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">\n'
                 f'<head><title>Table of Contents</title></head>\n'
                 f'<body><nav epub:type="toc"><h1>Table of Contents</h1><ol>\n'
                 f'{toc_items}\n'
                 f'</ol></nav></body></html>')

    ncx_items = []
    for i, (fn, h, _) in enumerate(all_files, 1):
        ncx_items.append(
            f'  <navPoint id="{slug(h)}" playOrder="{i}">'
            f'<navLabel><text>{xmlescape(h)}</text></navLabel>'
            f'<content src="{fn}"/></navPoint>')
    ncx = (f'<?xml version="1.0" encoding="UTF-8"?>\n'
           f'<!DOCTYPE ncx PUBLIC "-//NISO//DTD ncx 2005-1//EN"\n'
           f' "http://www.daisy.org/z3986/2005/ncx-2005-1.dtd">\n'
           f'<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">\n'
           f'<head><meta name="dtb:uid" content="{book_id}"/>'
           f'<meta name="dtb:depth" content="1"/></head>\n'
           f'<docTitle><text>{xmlescape(TITLE)}</text></docTitle>\n'
           f'<navMap>{"".join(ncx_items)}</navMap></ncx>')

    manifest_items = [
        '    <item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>',
        '    <item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>',
        '    <item id="css" href="styles/epub.css" media-type="text/css"/>',
    ]
    spine_items = []
    for fn, h, _ in all_files:
        fid = slug(h)
        manifest_items.append(f'    <item id="{fid}" href="{fn}" media-type="application/xhtml+xml"/>')
        spine_items.append(f'    <itemref idref="{fid}"/>')

    opf = (f'<?xml version="1.0" encoding="UTF-8"?>\n'
           f'<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="book-id">\n'
           f'<metadata xmlns:dc="http://purl.org/dc/elements/1.1/">\n'
           f'<dc:identifier id="book-id">{book_id}</dc:identifier>\n'
           f'<dc:title>{xmlescape(TITLE)}</dc:title>\n'
           f'<dc:creator>{xmlescape(AUTHOR)}</dc:creator>\n'
           f'<dc:language>{LANG}</dc:language>\n'
           f'<dc:publisher>{xmlescape(PUBLISHER)}</dc:publisher>\n'
           f'<dc:date>{date_str}</dc:date>\n'
           f'<meta property="dcterms:modified">{ts}</meta>\n'
           f'</metadata>\n'
           f'<manifest>\n' + "\n".join(manifest_items) + '\n</manifest>\n'
           f'<spine page-progression-direction="ltr" toc="ncx">\n' + "\n".join(spine_items) + '\n</spine>\n'
           f'</package>')

    epub_path = os.path.join(OUTPUT_DIR, "cindy-lou-magnet.epub")
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("mimetype", "application/epub+xml", compress_type=zipfile.ZIP_STORED)
        z.writestr("META-INF/container.xml",
                    '<?xml version="1.0" encoding="UTF-8"?>\n'
                    '<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">\n'
                    '<rootfiles><rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>'
                    '</rootfiles></container>')
        z.writestr("OEBPS/content.opf", opf)
        z.writestr("OEBPS/nav.xhtml", nav_xhtml)
        z.writestr("OEBPS/toc.ncx", ncx)
        z.writestr("OEBPS/styles/epub.css", CSS_EPUB)
        for fn, h, body_html in all_files:
            z.writestr(f"OEBPS/{fn}", make_xhtml(fn, h, body_html, h))

    with open(epub_path, "wb") as f:
        f.write(buf.getvalue())

    sz_kb = os.path.getsize(epub_path) // 1024
    print(f"  \u2713 EPUB: {epub_path} ({sz_kb}KB)")

    magnet_epub = os.path.join(MAGNETS_DIR, "cindy-lou-magnet.epub")
    with open(epub_path, "rb") as sf:
        with open(magnet_epub, "wb") as df:
            df.write(sf.read())
    print(f"  \u2713 Copied to: {magnet_epub}")

    return epub_path, magnet_epub


# ===================== PDF BUILDER (fpdf2) =====================

def build_pdf():
    from fpdf import FPDF

    with open(NOVELLA_MD, encoding='utf-8') as f:
        content = f.read()

    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_font("DejaVu", "", "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf")
    pdf.add_font("DejaVu", "B", "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf")
    pdf.add_font("DejaVu", "I", "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf")

    pdf.add_page()
    pdf.ln(60)
    pdf.set_font("DejaVu", "B", 22)
    pdf.multi_cell(0, 12, TITLE, align="C")
    pdf.ln(6)
    pdf.set_font("DejaVu", "I", 13)
    pdf.cell(0, 8, SUBTITLE, align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(10)
    pdf.set_font("DejaVu", "", 12)
    pdf.cell(0, 8, f"by {AUTHOR}", align="C", new_x="LMARGIN", new_y="NEXT")

    pdf.add_page()
    pdf.set_font("DejaVu", "", 10)
    pdf.ln(20)
    pdf.cell(0, 7, TITLE, align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 7, SUBTITLE, align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(8)
    pdf.cell(0, 7, f"\u00a9 {YEAR} Bob J Mills", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 7, "All rights reserved.", align="C", new_x="LMARGIN", new_y="NEXT")

    lines = content.split("\n")
    ch_num = 0
    in_chapter = False
    ch_title = ""
    ch_lines = []

    for line in lines:
        s = line.strip()
        if s.startswith("## ") and ("chapter" in s.lower() or "epilogue" in s.lower()):
            if in_chapter:
                _write_chapter(pdf, ch_title, ch_lines)
            ch_num += 1
            ch_title = s[3:]
            ch_lines = []
            in_chapter = True
        elif in_chapter:
            ch_lines.append(line)

    if in_chapter and ch_lines:
        _write_chapter(pdf, ch_title, ch_lines)

    pdf.add_page()
    pdf.set_font("DejaVu", "B", 14)
    pdf.cell(0, 10, "Thank You for Reading", align="L", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)
    pdf.set_font("DejaVu", "", 11)
    pdf.multi_cell(0, 5.5, (
        "Thank you for reading this novella. "
        "If you enjoyed the story, the full trilogy awaits you on Amazon."
    ))

    pdf_path = os.path.join(OUTPUT_DIR, "cindy-lou-magnet.pdf")
    pdf.output(pdf_path)
    sz_kb = os.path.getsize(pdf_path) // 1024
    print(f"  \u2713 PDF: {pdf_path} ({sz_kb}KB) [{pdf.pages_count} pages]")

    magnet_pdf = os.path.join(MAGNETS_DIR, "cindy-lou-magnet.pdf")
    with open(pdf_path, "rb") as sf:
        with open(magnet_pdf, "wb") as df:
            df.write(sf.read())
    print(f"  \u2713 Copied to: {magnet_pdf}")

    return pdf_path, magnet_pdf


def _write_chapter(pdf, title, lines):
    pdf.add_page()
    pdf.set_font("DejaVu", "B", 16)
    pdf.cell(0, 10, title, align="L", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)
    pdf.set_font("DejaVu", "", 11)
    for line in lines:
        s = line.strip()
        if not s:
            pdf.ln(3)
        elif s == "---":
            pdf.ln(2)
            pdf.set_font("DejaVu", "", 10)
            pdf.cell(0, 6, "* * *", align="C", new_x="LMARGIN", new_y="NEXT")
            pdf.set_font("DejaVu", "", 11)
            pdf.ln(2)
        elif s.startswith("### "):
            pdf.ln(2)
            pdf.set_font("DejaVu", "B", 12)
            pdf.cell(0, 8, s[4:], align="L", new_x="LMARGIN", new_y="NEXT")
            pdf.set_font("DejaVu", "", 11)
        else:
            s = s.replace("**", "").replace("*", "")
            pdf.multi_cell(0, 5.5, s)


if __name__ == "__main__":
    print("=" * 50)
    print(f"Building Reader Magnet: {TITLE}")
    print("=" * 50)
    epub_result = build_epub()
    pdf_result = build_pdf()
    print("\n" + "=" * 50)
    print("Complete! Files ready for deployment:")
    print(f"  EPUB: {epub_result[1]}")
    print(f"  PDF:  {pdf_result[1]}")
    print("=" * 50)