#!/usr/bin/env python3
"""
Build print-ready HTML + PDF + EPUB for a non-fiction business book.
Reads manuscript.md, generates:
  - print-formatted HTML with CSS paged media
  - KDP-compliant EPUB3 (text-only, no cover embed)
Usage: python3 build.py
Edit paths and CSS at top of file as needed.
"""
import re, os, zipfile
from pathlib import Path
from datetime import datetime

# --- CONFIGURE THESE ---
MANUSCRIPT = Path("manuscript.md")
OUTPUT_DIR = Path("output")
TITLE = "The Owner's Manual for AI Agents"
SUBTITLE = "What Every Business Owner Needs to Know About Building Autonomous Systems"
AUTHOR = "Bob J Mills"
BOOK_KEY = "Owners_Manual_AI_Agents"
CSS_FILE = None  # or Path("book-style.css")

def esc(text):
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

def md_to_html(text):
    """Simple markdown to HTML for print."""
    result = []
    in_list = False
    for line in text.split('\n'):
        s = line.strip()
        if not s:
            if in_list: result.append('</ul>'); in_list = False
            result.append('')
            continue
        if s.startswith('### '):
            if in_list: result.append('</ul>'); in_list = False
            result.append(f'<h3>{esc(s[4:])}</h3>'); continue
        if s.startswith('#### '):
            if in_list: result.append('</ul>'); in_list = False
            result.append(f'<h4>{esc(s[5:])}</h4>'); continue
        def fmt(t):
            t = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', t)
            t = re.sub(r'\*(.+?)\*', r'<em>\1</em>', t)
            return t
        if s.startswith('- ') or s.startswith('* '):
            if not in_list: result.append('<ul>'); in_list = True
            result.append(f'<li>{fmt(esc(s[2:]))}</li>'); continue
        if re.match(r'^\d+\.\s', s):
            if not in_list: result.append('<ol>'); in_list = True
            c = re.sub(r'^\d+\.\s', '', s)
            result.append(f'<li>{fmt(esc(c))}</li>'); continue
        if in_list: result.append('</ul>'); in_list = False
        p = fmt(esc(s))
        p = p.replace(' . ', ' — ')
        result.append(f'<p>{p}</p>')
    if in_list: result.append('</ul>')
    return '\n'.join(result)

PRINT_CSS = """
@page { size: 6in 9in; margin: 0.85in;
  @bottom-center { content: counter(page); font-family: Georgia,serif; font-size: 9pt; color: #888; }
  @top-center { content: "THE TITLE"; font-family: Georgia,serif; font-size: 8pt; color: #aaa; } }
@page:first { @top-center { content: none; } @bottom-center { content: none; } }
body { font-family: Georgia,'Times New Roman',serif; line-height: 1.55; font-size: 11pt; color: #000; }
.title-page { text-align: center; padding-top: 30%; page-break-after: always; }
.title-page h1 { font-size: 22pt; margin-bottom: 6pt; }
.title-page .subtitle { font-size: 14pt; font-style: italic; color: #444; margin-bottom: 30pt; }
.title-page .author { font-size: 14pt; margin-top: 30pt; }
.copyright-page { page-break-after: always; font-size: 9pt; line-height: 1.4; }
.copyright-page p { margin: 4pt 0; text-indent: 0; }
h2.chapter-title { text-align: center; font-size: 15pt; page-break-before: always; padding-top: 1.5in; margin-bottom: 0.5in; }
h3 { font-size: 12pt; margin: 18pt 0 8pt; }
h4 { font-size: 11pt; font-style: italic; margin: 14pt 0 6pt; }
p { margin: 0.15em 0; text-indent: 1.2em; orphans: 2; widows: 2; }
ul, ol { margin: 0.3em 0 0.3em 1.5em; }
li { margin: 0.1em 0; }
.part-divider { page-break-before: always; text-align: center; padding-top: 35%; font-size: 18pt; font-weight: bold; }
.note-section { page-break-after: always; }
.toc { page-break-after: always; }
.toc h2 { text-align: center; font-size: 14pt; margin-bottom: 20pt; }
.toc-entry { margin: 3pt 0; font-size: 10pt; }
.toc-entry.part { font-weight: bold; margin-top: 8pt; font-size: 10.5pt; }
.back-matter { page-break-before: always; }
.back-matter h2 { text-align: center; font-size: 13pt; }
"""

OUTPUT_DIR.mkdir(exist_ok=True)
text = MANUSCRIPT.read_text()

# Parse chapters
lines = text.split('\n')
chapters, part_dividers = [], []
current_ch, current_lines = None, []
for line in lines:
    if line.startswith('## Chapter '):
        if current_ch: chapters.append((current_ch, '\n'.join(current_lines).strip()))
        current_ch = line.replace('## ', '').strip()
        current_lines = []
    elif line.startswith('# PART '):
        if current_ch: chapters.append((current_ch, '\n'.join(current_lines).strip())); current_ch = None
        part_dividers.append(line.replace('# ', '').strip())
        current_lines = []
    elif current_ch is not None:
        current_lines.append(line)
if current_ch: chapters.append((current_ch, '\n'.join(current_lines).strip()))

html_parts = []
html_parts.append(f'<div class="title-page"><h1>{esc(TITLE)}</h1><p class="subtitle">{esc(SUBTITLE)}</p><p class="author">{esc(AUTHOR)}</p></div>')
html_parts.append(f'<div class="copyright-page"><p><strong>© {datetime.now().year} {esc(AUTHOR)}. All rights reserved.</strong></p><p>No part of this publication may be reproduced...</p></div>')

# TOC
toc_lines = ['<div class="toc">', '<h2>Contents</h2>']
for p in part_dividers: toc_lines.append(f'<p class="toc-entry part">{esc(p)}</p>')
for ch, _ in chapters: toc_lines.append(f'<p class="toc-entry">{esc(ch)}</p>')
toc_lines.append('</div>')
html_parts.append('\n'.join(toc_lines))

for ch_title, ch_content in chapters:
    html_parts.append(f'<h2 class="chapter-title">{esc(ch_title)}</h2>')
    html_parts.append(md_to_html(ch_content))

# About the Author would be injected here if in back matter

css = (CSS_FILE.read_text() if CSS_FILE else PRINT_CSS).replace("THE TITLE", TITLE)
full = f'<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><title>{esc(TITLE)}</title><style>{css}</style></head><body>{"".join(html_parts)}</body></html>'
(OUTPUT_DIR / f"{BOOK_KEY}.html").write_text(full)
print(f"HTML: {OUTPUT_DIR / f'{BOOK_KEY}.html'}")
