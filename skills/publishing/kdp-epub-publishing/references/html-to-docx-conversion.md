# HTML to DOCX Conversion

When EPUBs fail KDP upload and you need to review manuscript content in MS Word / Google Docs, convert the HTML manuscripts to DOCX.

## Why

- KDP may reject EPUBs for reasons that are hard to diagnose from the EPUB alone
- MS Word / Google Docs can open DOCX files for visual review
- The HTML manuscripts in `output/` are the most recent versions (same source as the EPUBs)

## Source Files

The print-ready HTML manuscripts live in each book's `output/` directory:

```
/mnt/usb_4tb/books/<Series>/<Book>/output/<book_name>_print.html
```

Use the `_print.html` files — they are the most recent versions, synced with the EPUBs.

## Conversion Script

```python
#!/usr/bin/env python3
"""Convert HTML book manuscripts to DOCX. Requires: python-docx, lxml."""

import os, re
from docx import Document
from docx.shared import Pt
from lxml import html

def process_element(doc, element):
    tag = element.tag.lower() if hasattr(element, 'tag') else None
    if tag in ('h1','h2','h3','h4','h5','h6'):
        level = int(tag[1])
        p = doc.add_paragraph()
        p.style = f'Heading {level}'
        p.add_run(element.text_content().strip())
        return
    if tag == 'p':
        text = element.text_content().strip()
        if not text:
            doc.add_paragraph()
            return
        p = doc.add_paragraph()
        if element.text:
            p.add_run(element.text)
        for child in element:
            ct = child.tag.lower() if hasattr(child, 'tag') else ''
            if ct in ('b','strong'):
                p.add_run(child.text_content().strip()).bold = True
            elif ct in ('i','em'):
                p.add_run(child.text_content().strip()).italic = True
            else:
                p.add_run(child.text_content().strip())
            if child.tail:
                p.add_run(child.tail)
        return
    if tag in ('div','section','article','main','body'):
        for child in element:
            process_element(doc, child)
        return
    if tag in ('ul','ol'):
        for li in element.findall('.//li'):
            t = li.text_content().strip()
            if t:
                doc.add_paragraph(t, style='List Bullet')
        return
    if tag == 'blockquote':
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Inches(0.5)
        p.add_run(element.text_content().strip()).italic = True
        return
    for child in element:
        process_element(doc, child)

def html_to_docx(html_path, docx_path):
    with open(html_path, 'rb') as f:
        content = f.read()
    doc = Document()
    style = doc.styles['Normal']
    style.font.name = 'Times New Roman'
    style.font.size = Pt(12)
    tree = html.fromstring(content)
    body = tree.find('.//body')
    if body is None:
        body = tree
    for element in body:
        process_element(doc, element)
    doc.save(docx_path)

# Usage:
# html_to_docx('/path/to/book_print.html', '/path/to/output.docx')
```

## Dependencies

- `python-docx` (pip3 install python-docx) — usually pre-installed
- `lxml` (pip3 install lxml) — usually pre-installed
- pandoc is NOT required
- LibreOffice CANNOT convert epub→docx (headless mode fails on epub input)

## Output

Place converted DOCX files in `/mnt/usb_4tb/books/converted_docx/` with naming convention `Book_N_Title.docx`.
