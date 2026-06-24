# HTML to DOCX Conversion for KDP Review

When KDP rejects an EPUB and you need a DOCX for manual review, convert the print HTML manuscript to DOCX using Python. This is the only reliable method on this system — pandoc is not installed and LibreOffice headless cannot convert EPUB.

## Why Not Other Tools

- **LibreOffice `--headless --convert-to docx`**: Silently fails on EPUB input (0-byte output). Works for ODT/HTML→DOCX but not EPUB.
- **pandoc**: Not installed. `apt-get install pandoc` requires sudo (not available). Do not attempt.
- **python-docx + lxml**: ✅ Works. Both are installed. Handles HTML parsing, image embedding, and formatted paragraphs.

## Conversion Script

Run `/tmp/html_to_docx_v3.py` (or a derivative) to convert all books:

```bash
python3 /tmp/html_to_docx_v3.py
```

Output goes to `/mnt/usb_4tb/books/converted_docx/`.

## Key Implementation Details

### HTML Parsing

Parse as **bytes** (not string) to handle `<?xml encoding="UTF-8">` declarations:

```python
with open(html_path, 'rb') as f:
    raw = f.read()
tree = lxml_html.fromstring(raw)
```

Parsing as a string raises: `Unicode strings with encoding declaration are not supported`.

### Image Path Resolution

The HTML references images like `src="ch01.png"` but the actual file may be in several locations. Try in order:

1. `images/` directory (book folder) — direct match
2. `images/` directory — basename only
3. `chapter_images/` directory — direct match
4. `chapter_images_compressed/` — `.jpg` extension
5. **Offset mapping** — some books have renumbered images (e.g., HTML references `ch01.png` but directory has `ch31.png`). Try offsets of ±10, ±20, ±30.

```python
def resolve_image_path(img_src, images_dir, book_dir):
    # ... strategies 1-4 ...
    # Strategy 5: offset mapping
    if img_src.startswith('ch') and len(img_src) > 4:
        num = int(img_src[2:].split('.')[0])
        for offset in [30, -30, 10, -10, 20, -20]:
            mapped = f"ch{num + offset:02d}.png"
            # try all image directories...
```

### Front Matter Structure

The print HTML has these sections in order:
1. `div.title-page` — title, subtitle, author (centered, large font)
2. `div.cp` — copyright line (centered, small font)
3. `div.toc-page` — table of contents (chapter list)
4. `div.chapter` — each chapter with `h2` heading, `div.chapter-image`, and `p` content
5. Back matter paragraphs — "Also by", author website, AI notice

Each section should be separated by a page break (`w:br type="page"`).

### Page Breaks

Add via raw XML (python-docx `add_break()` requires WD_BREAK import):

```python
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

def add_page_break(doc):
    p = doc.add_paragraph()
    r = OxmlElement('w:r')
    br = OxmlElement('w:br')
    br.set(qn('w:type'), 'page')
    r.append(br)
    p._p.append(r)
```

### Chapter Heading Deduplication

HTML chapter headings look like `Chapter 1: Chapter 1 — The Artemis Accord`. Strip the first `Chapter N: ` prefix:

```python
ch_text = re.sub(r'^Chapter \d+:\s*', '', ch_text)
```

### Inline Formatting

Handle `<b>`, `<strong>`, `<i>`, `<em>`, `<a>` tags within paragraphs. Use `element.text_content()` for simple cases, or iterate children for mixed formatting.

## Output Verification

After conversion, verify each docx:
- Front matter present (title, copyright, TOC)
- Image count matches expected chapters
- Back matter present (Also by, author website)
- File size is reasonable (15-35MB for fiction with images)

```python
doc = Document(docx_path)
img_count = sum(1 for rel in doc.part.rels.values() if 'image' in rel.reltype)
paras = len(doc.paragraphs)
```
