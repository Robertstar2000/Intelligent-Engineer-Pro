#!/usr/bin/env python3
"""
Reader Magnet PDF Generator — WeasyPrint-based pipeline.

Generates free downloadable PDFs from cover images + manuscript markdown files.
Output: 6x9in PDF with Cover → Note from Author → TOC → Manuscript → Sales Pitch → Book List → Amazon CTA

Usage:
    python3 reader-magnet-script.py

Depends on: WeasyPrint, DejaVu Serif fonts
"""

import base64, os, re, subprocess, sys

MAGNET_DIR = "/mnt/usb_4tb/books/books-section/magnets"

BOOKS = [
    {
        "dir": "Age of Lightships Novella",
        "title": "The Age of Lightships: Last Transmission",
        "subtitle": "A Prequel to The Age of Lightships Series",
        "author": "Bob J Mills",
        "cover": "Lightships.png",
        "manuscript": "lightships-last-transmission.md",
        "genre": "science fiction",
        "series_name": "The Age of Lightships",
        "next_book": "Sunward Exodus",
        "next_book_desc": "The signal was just the beginning. The fleet carries the future of humanity into the dark between stars.",
    },
    {
        "dir": "Business Series Magnet",
        "title": "AI for Small Business",
        "subtitle": "A Practical Playbook for Modern Innovation",
        "author": "Bob J Mills",
        "cover": "Business.png",
        "manuscript": "MIFECO_AI_PLAYBOOK.md",
        "genre": "business",
        "series_name": "MIFECO Practical Guide",
        "next_book": "The Crisis Ready Company",
        "next_book_desc": "Build resilience into every part of your operation — before you need it.",
    },
    {
        "dir": "Cindy Lou Novella",
        "title": "Cindy Lou and the Case of the Missing Retainer",
        "subtitle": "A Cindy Lou Legal Caper Novella (Reader Magnet)",
        "author": "Bob J Mills",
        "cover": "CindyLou.png",
        "manuscript": "Missing_Retainer_Novella.md",
        "genre": "fiction",
        "series_name": "Cindy Lou Legal Capers",
        "next_book": "Retainer to Trouble",
        "next_book_desc": "A mysterious retainer check pulls Cindy Lou into her first real case.",
    },
    {
        "dir": "lunar foundation Novella",
        "title": "The Lunar Foundation: First Light",
        "subtitle": "A Prequel to The Lunar Foundation Series",
        "author": "Bob J Mills",
        "cover": "Moon.png",
        "manuscript": "lunar-foundation-first-light.md",
        "genre": "science fiction",
        "series_name": "The Lunar Foundation",
        "next_book": "Moon Rock",
        "next_book_desc": "Beneath the regolith lies the foundation of everything we'll become.",
    },
    {
        "dir": "No Blue Sky Novella",
        "title": "No Blue Sky: Before the Dust",
        "subtitle": "A Prequel to the No Blue Sky Series",
        "author": "Bob J Mills",
        "cover": "Dust.png",
        "manuscript": "no-blue-sky-before-the-dust.md",
        "genre": "science fiction",
        "series_name": "No Blue Sky",
        "next_book": "Built from Dust",
        "next_book_desc": "On Mars, nothing is given — everything is built.",
    },
]


def embed_image(path):
    """Return base64 data URI from image file."""
    with open(path, "rb") as f:
        data = f.read()
    ext = os.path.splitext(path)[1].lower()
    mime = "image/png" if ext == ".png" else "image/jpeg"
    return f"data:{mime};base64,{base64.b64encode(data).decode()}"


def parse_manuscript(filepath):
    """Parse novella markdown with organic headers (Part/Chapter/Scene breaks)."""
    with open(filepath) as f:
        content = f.read()

    # Strip frontmatter (everything before first ## Part/Chapter)
    lines = content.split("\n")
    body_lines = []
    in_front = True
    for line in lines:
        if in_front:
            s = line.strip()
            if s.startswith("##") and ("Chapter" in s or "Part" in s):
                in_front = False
                body_lines.append(line)
            elif s == "---":
                continue
            elif s == "":
                continue
            continue
        body_lines.append(line)

    body = "\n".join(body_lines)
    chapters = []
    current_lines = []
    heading = None
    level = 0

    def flush():
        nonlocal current_lines, heading, level
        if heading:
            chapters.append({
                "type": "part" if level == 1 else "chapter",
                "heading": heading,
                "content": "\n".join(current_lines).strip(),
            })
        elif current_lines:
            chapters.append({"type": "intro", "heading": "", "content": "\n".join(current_lines).strip()})
        current_lines = []
        heading = None
        level = 0

    for line in body.split("\n"):
        s = line.strip()
        if s == "---":
            if heading is not None:
                flush()
            chapters.append({"type": "scene_break", "heading": "", "content": ""})
            continue
        if s.startswith("#") and not s.startswith("###"):
            if heading is not None:
                flush()
            level = 1 if s.startswith("# ") else 2
            heading = s.lstrip("#").strip()
            continue
        current_lines.append(line)
    if heading or current_lines:
        flush()
    return chapters


def build_html(book):
    """Assemble self-contained HTML for WeasyPrint."""
    bdir = os.path.join(MAGNET_DIR, book["dir"])
    cover_data = embed_image(os.path.join(bdir, book["cover"]))
    chapters = parse_manuscript(os.path.join(bdir, book["manuscript"]))

    # TOC
    toc = ""
    chapter_html = ""
    for ch in chapters:
        if ch["type"] in ("part", "chapter"):
            anchor = re.sub(r'[^a-z0-9]+', '-', ch["heading"].lower()).strip('-')
            cls = "toc-part" if ch["type"] == "part" else "toc-chapter"
            toc += f'<p class="{cls}"><a href="#{anchor}">{ch["heading"]}</a></p>\n'
            hcls = "part-heading" if ch["type"] == "part" else "chapter-heading"
            chapter_html += f'<h2 id="{anchor}" class="{hcls}">{ch["heading"]}</h2>\n'
            if ch["content"]:
                chapter_html += '<div class="chapter-body">\n'
                for para in ch["content"].split("\n\n"):
                    p = para.strip()
                    if p:
                        chapter_html += f"<p>{p}</p>\n"
                chapter_html += "</div>\n"
        elif ch["type"] == "scene_break":
            chapter_html += '<p class="scene-break">* * *</p>\n'
        elif ch["type"] == "intro" and ch["content"]:
            chapter_html += f'<div class="chapter-body"><p>{ch["content"]}</p></div>\n'

    body_css = "p { text-indent: 0; margin: 6px 0; }" if book["genre"] == "business" else "p { text-indent: 1.5em; margin: 0; }"

    # Series-specific sales pitch
    if book["series_name"] == "The Age of Lightships":
        pitch = f"""<div class="sales-pitch">
<h2>Continue the Journey</h2>
<p>The signal was real. Aria and the crew answered it — and changed everything.</p>
<p><strong>Next: {book['next_book']}</strong></p>
<blockquote>{book['next_book_desc']}</blockquote>
<p><strong>Series Reading Order:</strong></p>
<ol><li>Sunward Exodus</li><li>The Mercury Accord</li><li>Ghosts Beyond Neptune</li><li>The Last Photon Fleet</li></ol>
<p class="cta">Available now on Amazon Kindle and Paperback.</p></div>"""
    elif book["series_name"] == "Cindy Lou Legal Capers":
        pitch = f"""<div class="sales-pitch">
<h2>Continue the Journey</h2>
<p>Cindy Lou reads the fine print so you don't have to.</p>
<p><strong>Next: {book['next_book']}</strong></p>
<blockquote>{book['next_book_desc']}</blockquote>
<p><strong>Series Reading Order:</strong></p>
<ol><li>Retainer to Trouble</li><li>Clause for Alarm</li><li>Affidavits and Alibis</li></ol>
<p class="cta">Available now on Amazon Kindle and Paperback.</p></div>"""
    elif book["series_name"] == "The Lunar Foundation":
        pitch = f"""<div class="sales-pitch">
<h2>Continue the Journey</h2>
<p>One habitat at a time, humanity builds a home on the Moon.</p>
<p><strong>Next: {book['next_book']}</strong></p>
<blockquote>{book['next_book_desc']}</blockquote>
<p><strong>Series Reading Order:</strong></p>
<ol><li>Moon Rock</li><li>Mooncoming</li><li>Waters End</li><li>Waters Horizon</li></ol>
<p class="cta">Available now on Amazon Kindle and Paperback.</p></div>"""
    elif book["series_name"] == "No Blue Sky":
        pitch = f"""<div class="sales-pitch">
<h2>Continue the Journey</h2>
<p>From dust to nation — the colonists trade Earth for Mars.</p>
<p><strong>Next: {book['next_book']}</strong></p>
<blockquote>{book['next_book_desc']}</blockquote>
<p><strong>Series Reading Order:</strong></p>
<ol><li>Built from Dust</li><li>The Oxygen Gamble</li><li>Rivers Under Mars</li><li>The Red Charter</li><li>The First Martian Nation</li></ol>
<p class="cta">Available now on Amazon Kindle and Paperback.</p></div>"""
    else:
        pitch = f"""<div class="sales-pitch">
<h2>Continue Learning</h2>
<p>This playbook is just the beginning.</p>
<ul><li><strong>AI That Works</strong></li><li><strong>The Crisis Ready Company</strong></li><li><strong>Owner's Manual for AI Agents</strong></li></ul>
<p class="cta">Available now on Amazon Kindle and Paperback.</p></div>"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head><meta charset="utf-8"><title>{book['title']}</title>
<style>
@page {{ size: 6in 9in; margin: 0.75in 0.8in; @bottom-center {{ content: counter(page); font-family: 'DejaVu Serif', serif; font-size: 8pt; color: #666; }} }}
@page:first {{ @bottom-center {{ content: none; }} }}
@page cover {{ margin: 0; @bottom-center {{ content: none; }} }}
* {{ box-sizing: border-box; }}
body {{ font-family: 'DejaVu Serif', serif; font-size: 12pt; line-height: 1.5; color: #222; }}
.cover-page {{ page: cover; page-break-after: always; text-align: center; }}
.cover-image {{ width: 100%; height: 9in; object-fit: contain; }}
.title-page {{ page-break-before: always; page-break-after: always; text-align: center; padding-top: 2in; }}
.book-title {{ font-size: 24pt; font-weight: bold; margin-bottom: 12pt; }}
.book-subtitle {{ font-size: 14pt; font-style: italic; color: #555; margin-bottom: 24pt; }}
.book-author {{ font-size: 16pt; margin-top: 36pt; }}
.copyright-page {{ page-break-before: always; page-break-after: always; text-align: center; padding-top: 1.5in; font-size: 10pt; color: #555; }}
.note-page {{ page-break-before: always; page-break-after: always; padding-top: 0.5in; }}
.section-title {{ font-size: 18pt; font-weight: bold; text-align: center; margin-bottom: 24pt; }}
.toc-page {{ page-break-before: always; page-break-after: always; }}
.toc-part {{ font-size: 13pt; font-weight: bold; margin: 6pt 0; }}
.toc-chapter {{ font-size: 11pt; margin: 4pt 0 4pt 20pt; }}
.toc-page a {{ color: #222; text-decoration: none; }}
.part-heading {{ font-size: 20pt; font-weight: bold; text-align: center; margin-top: 1.5in; page-break-before: always; margin-bottom: 12pt; }}
.chapter-heading {{ font-size: 18pt; font-weight: bold; text-align: center; margin-top: 0.8in; page-break-before: always; margin-bottom: 18pt; }}
.chapter-body {{ {body_css} }}
.chapter-body p {{ font-size: 12pt; line-height: 1.5; text-align: justify; }}
.scene-break {{ text-align: center; margin: 24pt 0; font-size: 14pt; color: #999; letter-spacing: 4pt; }}
.sales-pitch {{ page-break-before: always; padding-top: 0.5in; }}
.back-matter {{ page-break-before: always; padding-top: 0.5in; }}
.amazon-section {{ page-break-before: always; padding-top: 0.5in; }}
.signature {{ margin-top: 24pt; font-style: italic; text-align: right; }}
.cta {{ margin-top: 16pt; font-style: italic; text-align: center; font-size: 13pt; }}
blockquote {{ font-style: italic; color: #555; margin: 8pt 20pt; padding: 6pt 12pt; border-left: 3px solid #ccc; }}
.series-title {{ font-size: 14pt; font-weight: bold; margin-top: 18pt; border-bottom: 1px solid #ccc; padding-bottom: 4pt; }}
.book-list {{ list-style: none; padding: 0; }}
.book-list li {{ margin: 4pt 0; font-size: 11pt; }}
</style>
</head>
<body>
<div class="cover-page"><img src="{cover_data}" class="cover-image"/></div>
<div class="title-page"><h1 class="book-title">{book['title']}</h1>
<p class="book-subtitle">{book['subtitle']}</p>
<p class="book-author">by {book['author']}</p></div>
<div class="copyright-page"><p>{book['title']}</p><p>Copyright © 2026 Bob J Mills. All rights reserved.</p>
<p style="font-style:italic;margin-top:20px;">AI Disclosure: This book was written with AI assistance. The story, characters, and voice are original works by Bob J Mills.</p></div>
<div class="note-page">
<h2 class="section-title">Note from the Author</h2>
<p>Thank you for downloading this reader magnet novella...</p>
<p class="signature">— Bob J Mills</p></div>
<div class="toc-page"><h2 class="section-title">Contents</h2>{toc}</div>
{chapter_html}
{pitch}
<div class="back-matter"><h2 class="section-title">Also by Bob J Mills</h2>
<h3 class="series-title">The Age of Lightships</h3><ul class="book-list"><li><strong>Sunward Exodus</strong> — Book 1</li><li><strong>The Mercury Accord</strong> — Book 2</li><li><strong>Ghosts Beyond Neptune</strong> — Book 3</li><li><strong>The Last Photon Fleet</strong> — Book 4</li></ul>
<h3 class="series-title">The Lunar Foundation</h3><ul class="book-list"><li><strong>Moon Rock</strong> — Book 1</li><li><strong>Mooncoming</strong> — Book 2</li><li><strong>Waters End</strong> — Book 3</li><li><strong>Waters Horizon</strong> — Book 4</li></ul>
<h3 class="series-title">No Blue Sky</h3><ul class="book-list"><li><strong>Built from Dust</strong> — Book 1</li><li><strong>The Oxygen Gamble</strong> — Book 2</li><li><strong>Rivers Under Mars</strong> — Book 3</li><li><strong>The Red Charter</strong> — Book 4</li><li><strong>The First Martian Nation</strong> — Book 5</li></ul>
<h3 class="series-title">Cindy Lou Legal Capers</h3><ul class="book-list"><li><strong>Retainer to Trouble</strong> — Book 1</li><li><strong>Clause for Alarm</strong> — Book 2</li><li><strong>Affidavits and Alibis</strong> — Book 3</li></ul>
<h3 class="series-title">Business Books</h3><ul class="book-list"><li><strong>AI That Works</strong></li><li><strong>The Crisis Ready Company</strong></li><li><strong>Owner's Manual for AI Agents</strong></li></ul>
<h3 class="series-title">Memoir</h3><ul class="book-list"><li><strong>Tomorrow Remembered</strong></li></ul></div>
<div class="amazon-section"><h2 class="section-title">Available from Amazon and Kindle</h2>
<p>Visit <strong>www.mifeco.com/books</strong> for direct links to each title and free downloads.</p></div>
</body></html>"""

    return html


def main():
    import weasyprint
    for book in BOOKS:
        bdir = os.path.join(MAGNET_DIR, book["dir"])
        safe = re.sub(r'\s+', '_', book["title"].replace(":", "").replace("?", ""))
        pdf_path = os.path.join(bdir, f"{safe}_Magnet.pdf")
        ms = os.path.join(bdir, book["manuscript"])
        cv = os.path.join(bdir, book["cover"])
        if not os.path.exists(ms) or not os.path.exists(cv):
            print(f"  SKIP {book['title']}: missing manuscript or cover")
            continue
        html = build_html(book)
        weasyprint.HTML(string=html).write_pdf(pdf_path)
        kb = os.path.getsize(pdf_path) // 1024
        print(f"  ✅ {book['title']} — {kb} KB")


if __name__ == "__main__":
    main()