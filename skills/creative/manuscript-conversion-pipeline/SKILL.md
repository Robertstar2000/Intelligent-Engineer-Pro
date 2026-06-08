---
name: manuscript-conversion-pipeline
description: A systematic approach for setting up a manuscript conversion pipeline in restricted environments where direct tool installation is limited. This skill captures the methodology used to convert Markdown manuscripts to PDF, EPUB, and Kindle formats when working with locked-down Python environments.
---

## 🔍 MemPalace Query (MANDATORY FIRST STEP)
Before proceeding, query MemPalace for existing context:
```python
import sys, os; sys.path.insert(0, os.path.expanduser('~/.hermes/mempalace'))
import embed; embed.init_embedding(os.path.expanduser('~/.hermes/mempalace'))
results = embed.search_embeddings("manuscript conversion pipeline PDF EPUB Kindle Pandoc WeasyPrint", k=5)
```
This retrieves previous decisions, domain-specific context, and lessons learned from the vector memory store.

# Manuscript Conversion Pipeline Skill

## Overview
A systematic approach for setting up a manuscript conversion pipeline in restricted environments where direct tool installation is limited. This skill captures the methodology used to convert Markdown manuscripts to PDF, EPUB, and Kindle formats when working with locked-down Python environments.

**Note**: For standard builds on this system, use the unified `hermes-publish` pipeline (`/mnt/usb_4tb/books/hermes_publish.py`) which provides `step_epub.py` — a production-grade ZIP-based EPUB 3 generator that handles all 4 manuscript types. This skill's methodology is retained for reference, custom scripts, and restricted environments where the full pipeline is not available.

## Problem
Need to convert Markdown manuscripts to multiple formats (PDF, EPUB, MOBI/Kindle) but the environment may prevent direct installation of required tools like Pandoc, Calibre, or WeasyPrint.

## Solution
A three-tiered approach, tried in order:

### Tier 1: Pure-Python EPUB3 Generator (Preferred — No External Tools)
Create a complete EPUB3 file using only Python stdlib (`zipfile`, `xml.sax.saxutils`) + the `markdown` module. No pandoc, no calibre, no external binary needed.

EPUB3 is just a ZIP with a specific internal structure:
```
book.epub/
├── mimetype                          # "application/epub+zip" — must be first, uncompressed
├── META-INF/
│   └── container.xml                 # Points to OEBPS/content.opf
└── OEBPS/
    ├── content.opf                   # Package manifest + metadata + spine
    ├── nav.xhtml                     # EPUB3 navigation (Table of Contents)
    ├── css/
    │   └── style.css                 # Print-friendly CSS
    ├── images/
    │   └── cover.png                 # Cover image (optional)
    └── xhtml/
        ├── cover.xhtml               # Cover page
        ├── titlepage.xhtml           # Title page
        └── chapter_01_*.xhtml        # One XHTML per chapter
```

**Key implementation:** Split the markdown into chapters by detecting `#`/`##` headers. Convert each chapter body to XHTML using the `markdown` module. Build the `content.opf` with proper spine order, `nav.xhtml` with TOC, and include cover images via `<meta>` properties.

**Cover embedding:** Add `<item id="cover-image" href="images/cover.png" media-type="image/png" properties="cover-image"/>` to the manifest. The cover page (separate XHTML) stays in the spine for visual display.

**This works in any Python 3 environment where `pip install markdown` is possible.** No sudo, no root, no external binaries required.

### Tier 2: Environment-Agnostic Pipeline Script
Create a Python script that uses subprocess calls to external tools (pandoc, calibre), with the assumption that the user will install those tools on their local machine where they have full sudo/admin rights.

### Tier 3: Fallback HTML Converter
Create a simple Markdown-to-HTML converter that can be used as an intermediate step, allowing users to convert to PDF via browser print or wkhtmltopdf.

## Implementation Steps

### 1. Assess Available Tools
```python
# Check what's available in the environment
import subprocess
from pathlib import Path

# Test for uvx availability
has_uvx = Path("/usr/bin/uvx").exists() or Path("/home/bob/.local/bin/uvx").exists()
```

### 2. Create the Main Pipeline Script
The script should:
- Accept a Markdown file as input
- Use subprocess to call external tools (Pandoc, Calibre/ebook-convert, etc.)
- Handle errors gracefully
- Clean up temporary files
- Provide clear progress feedback

### 3. Create Setup Documentation
Document the installation process for:
- **Pandoc** (for PDF/EPUB conversion)
- **Calibre** (for Kindle MOBI conversion)
- **Python dependencies** (markdown library)

Include platform-specific instructions (Ubuntu/Debian, macOS, Windows).

### 4. Provide Alternative Approaches
- HTML converter script for quick previews
- Browser-based PDF printing
- Online conversion services as temporary solutions

## Key Learnings

### Discovery 1: uvx Limitations
uvx is designed for Python packages, not standalone binary tools like Pandoc or KindleGen. Attempting to use uvx for these tools will fail because they don't provide Python entry points.

### Discovery 2: Environment Restrictions
The Python environment is managed by `uv` and is externally locked down, preventing pip installations. This requires a user-space solution rather than system-wide installation.

### Discovery 3: Two-Phase Strategy
The most effective approach is:
1. Create scripts that assume the tools exist on the user's PATH
2. Provide detailed installation instructions
3. Offer fallback options for immediate needs

## Code Structure

### Tier 1: Pure-Python EPUB3 Generator (`epub_generator.py`)

```python
import markdown, zipfile, os, re, io, html as html_module
from xml.sax.saxutils import escape as xml_escape
from datetime import datetime

def split_into_chapters(content):
    """Split markdown into (title, body) tuples by detecting ## Chapter headers."""
    lines = content.split('\n')
    chapter_starts = []
    for i, line in enumerate(lines):
        stripped = line.strip()
        if re.match(r'^#{1,2}\s+(Chapter|CHAPTER|Part|PART|Introduction|Preface|Epilogue|Appendix|Dedication|Copyright)', stripped, re.IGNORECASE):
            chapter_starts.append(i)
        elif stripped.startswith('## ') and i > 0:
            chapter_starts.append(i)
    if not chapter_starts:
        return [("Full Content", content)]
    chapters = []
    for idx, start in enumerate(chapter_starts):
        end = chapter_starts[idx + 1] if idx + 1 < len(chapter_starts) else len(lines)
        chapter_text = '\n'.join(lines[start:end]).strip()
        title = re.sub(r'^#+\s+', '', lines[start].strip()).strip()
        chapters.append((title, chapter_text))
    return chapters

def create_epub(input_path, output_path, title, author, cover_image=None):
    """Create a complete EPUB3 file from markdown using only stdlib + markdown."""
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()
    chapters = split_into_chapters(content)
    book_id = f"urn:uuid:{hash(input_path + title) & 0xFFFFFFFFFFFFFFFF:016x}"

    buf = io.BytesIO()
    zf = zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED)

    # 1. mimetype (must be first, uncompressed)
    info = zipfile.ZipInfo('mimetype')
    info.compress_type = zipfile.ZIP_STORED
    zf.writestr(info, 'application/epub+zip')

    # 2. META-INF/container.xml
    zf.writestr('META-INF/container.xml',
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">\n'
        '  <rootfiles>\n'
        '    <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>\n'
        '  </rootfiles>\n'
        '</container>')

    # 3. CSS
    css = '''body { font-family: Georgia, "Times New Roman", serif; line-height: 1.6; margin: 2em 1.5em; max-width: 30em; }
h1, h2 { text-align: center; page-break-before: always; font-weight: bold; }
h1 { font-size: 1.8em; margin-top: 2em; }
h2 { font-size: 1.4em; margin-top: 2em; }
p { margin: 0.5em 0; text-indent: 1.5em; orphans: 2; widows: 2; }
.chapter-title { page-break-before: always; text-align: center; font-size: 1.6em; margin-top: 3em; }'''
    zf.writestr('OEBPS/css/style.css', css)

    # 4. XHTML chapters
    manifest, spine = [], []
    def add_item(id_, href, mtype, props=None):
        p = f' properties="{props}"' if props else ''
        manifest.append(f'<item id="{id_}" href="xhtml/{href}" media-type="{mtype}"{p}/>')
        spine.append(f'<itemref idref="{id_}"/>')

    # Cover page
    cover_html = f'''<?xml version="1.0" encoding="UTF-8"?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">
<head><title>Cover</title><link rel="stylesheet" type="text/css" href="css/style.css"/></head>
<body><div style="page-break-after:always;text-align:center;padding-top:30%">
<h1>{xml_escape(title)}</h1><p style="font-size:1.3em;margin-top:1.5em">{xml_escape(author)}</p>
</div></body></html>'''
    zf.writestr('OEBPS/xhtml/cover.xhtml', cover_html)
    add_item('cover', 'cover.xhtml', 'application/xhtml+xml')

    # Cover image
    if cover_image and os.path.exists(cover_image):
        ext = os.path.splitext(cover_image)[1].lower()
        mime = 'image/png' if ext == '.png' else 'image/jpeg'
        zf.writestr(f'OEBPS/images/cover{ext}', open(cover_image, 'rb').read())
        manifest.append(f'<item id="cover-image" href="images/cover{ext}" media-type="{mime}" properties="cover-image"/>')

    # Chapter XHTML files
    nav_items = []
    for i, (ch_title, ch_body) in enumerate(chapters):
        slug = re.sub(r'[^\w]', '-', ch_title.lower())[:50] or f'ch-{i+1:02d}'
        fn = f'chapter_{i+1:02d}_{slug}.xhtml'
        body = markdown.markdown(ch_body, extras=['extra'])
        body = body.replace('<h1>', '<h1 class="chapter-title">', 1).replace('<h2>', '<h2 class="chapter-title">', 1)
        xhtml = f'''<?xml version="1.0" encoding="UTF-8"?>
<html xmlns="http://www.w3.org/1999/xhtml"><head><title>{xml_escape(ch_title)}</title>
<link rel="stylesheet" type="text/css" href="css/style.css"/></head><body>
{body}</body></html>'''
        zf.writestr(f'OEBPS/xhtml/{fn}', xhtml)
        add_item(slug or f'ch{i}', fn, 'application/xhtml+xml')
        nav_items.append(f'<li><a href="xhtml/{fn}">{xml_escape(ch_title)}</a></li>')

    # Navigation
    nav = f'''<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">
<head><title>TOC</title></head><body><nav epub:type="toc"><h2>Contents</h2><ul>
<li><a href="xhtml/cover.xhtml">Cover</a></li>\n{chr(10).join(nav_items)}
</ul></nav></body></html>'''
    zf.writestr('OEBPS/nav.xhtml', nav)
    manifest.append('<item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>')

    # content.opf
    now = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    opf = f'''<?xml version="1.0" encoding="UTF-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="book-id">
  <metadata>
    <dc:identifier id="book-id">{book_id}</dc:identifier>
    <dc:title>{xml_escape(title)}</dc:title>
    <dc:creator>{xml_escape(author)}</dc:creator>
    <dc:language>en</dc:language>
    <dc:date>{now}</dc:date>
    <meta property="dcterms:modified">{now}</meta>
  </metadata>
  <manifest>
    <item id="css" href="css/style.css" media-type="text/css"/>
    {chr(10).join('    ' + m for m in manifest)}
  </manifest>
  <spine>{chr(10) + '    '.join(spine)}</spine>
</package>'''
    zf.writestr('OEBPS/content.opf', opf)
    zf.close()

    with open(output_path, 'wb') as f:
        f.write(buf.getvalue())
    return True

# Usage: create_epub("input.md", "output.epub", "Book Title", "Author", "cover.png")
```

### Tier 2: External Tools Pipeline (`pipeline.py`)

### Setup Guide (`setup_guide.md`)
Comprehensive documentation covering:
- Installation commands for different OSes
- Usage examples
- Troubleshooting tips
- KDP-specific formatting options

## Usage Examples

```bash
# Convert a manuscript to all formats
python pipeline.py Second_Generation.md

# Convert to specific formats
python pipeline.py manuscript.md ./output
```

## When to Use This Skill
- When working in a locked-down Python environment where sudo/apt is unavailable
- When needing to convert Markdown to EPUB3 for KDP publishing
- When pandoc or calibre are not installed and can't be installed
- When a quick HTML preview is needed before full conversion
- When the user asks for ebook files formatted for retailer upload
- When building both PDF (WeasyPrint) and EPUB3 from the same revised manuscript in tandem

## Prerequisites
- Python 3 with the `markdown` module (`pip install markdown` — no sudo needed if using pip user install)
- For EPUB: no other dependencies required
- For PDF: WeasyPrint (`pip install weasyprint`) or pandoc + LaTeX
- User must have the ability to install Python packages
- Basic command line familiarity
- Markdown-formatted manuscript with `## Chapter` headers for automatic chapter splitting
- Cover image (PNG recommended) if embedding

## Success Metrics
- PDF generated with proper formatting
- EPUB file validates correctly
- MOBI file loads on Kindle device
- User can successfully install and run the pipeline

## Pitfalls to Avoid
1. **Don't try to install tools with apt/sudo** — use `pip install --user` instead when sudo is unavailable
2. **Don't assume uvx can run any tool** — it only works with Python packages
3. **EPUB chapter-splitting pitfall** — using `re.split(r'\\n(?=#+\\s)')` on markdown that has both TOC entries (single `#` chapter headings with page numbers like `# Chapter 1: The Shock .................... 3`) AND actual content headers (`## Chapter 1: The Shock`) will create tiny TOC-only chunks that become empty EPUB chapters. **Fix**: The best approach is to use a known-good HTML artifact (which already has correct chapter splits and embedded images) as the EPUB/PDF source instead of re-splitting the broken Markdown. If no HTML artifact exists, either (a) add proper `# Chapter X:` headers to the Markdown body first, or (b) after splitting, merge any chunk under ~300 chars with the next chunk.
4. **Duplicate EPUB slugs** — when multiple chapters share the same base slug (e.g., "part-two-the-building" appears twice), the EPUB builder produces duplicate file entries. **Fix**: Track slug counts and append `-2`, `-3` suffixes for duplicates.
5. **Don't forget error handling** — external tools may fail
4. **Don't hardcode paths** — use relative paths and user input
5. **EPUB mimetype file must be first** — in the ZIP, `mimetype` must be the first entry and stored uncompressed, or some readers (Apple Books, KDP) will reject the file
6. **Cover image manifest entry** — the cover image needs `<item ... properties="cover-image"/>` in content.opf AND a separate cover XHTML in the spine for visual display. Both are required for KDP.
7. **Chapter detection** — markdown manuscripts need `## Chapter` or `# Chapter` headers for automatic splitting. If chapters are numbered differently (e.g., `### 1. Chapter`), adjust the regex in `split_into_chapters()`
8. **Markdown module extras** — use `extras=['extra']` for table support, fenced code blocks, and other extended markdown features
9. **Don't skip the final polish** — after generation, spot-check the EPUB by opening it in a reader. Verify cover displays, TOC is complete, chapters are in order, and no content is truncated

## Verification Steps
1. Check that Pandoc is installed: `pandoc --version`
2. Check that Calibre is installed: `ebook-convert --version`
3. Test with a simple Markdown file first
4. Verify output files open correctly

## Final Polish Stage
After the main conversion succeeds, include a dedicated final polish stage before delivery.

### Final polish checklist
- **Humanization mandate**: Run the `humanizer` skill's 29 pattern checks on the final manuscript. No AI-isms, no filler, real voice, variable rhythm, opinions where they fit. Mandatory for all book prose.
- Re-open the generated HTML/PDF and spot-check front matter, first chapter start, mid-book chapter start, and ending pages
- Verify the Table of Contents reflects the actual current chapter order
- If page numbers are printed in the TOC, compute them from the near-final PDF only after TOC styling is frozen
- Remove leftover placeholders, scaffolding text, duplicated section headings, and editor notes
- Run a final spelling/grammar/consistency cleanup on the source manuscript or generated HTML
- Confirm images still appear in the intended chapters and not in front matter or TOC blocks
- Note any remaining page-number instability explicitly instead of pretending the TOC is exact

### Rule of thumb
Do not treat format conversion as the end of the pipeline. The deliverable is only complete after one explicit publication-polish review of the generated artifacts.

## Related Skills
- `markdown-conversion`: Basic Markdown processing
- `document-generation`: General document creation
- `kdp-publishing`: Amazon KDP specific formatting

## Maintenance
This skill should be updated when:
- New conversion tools become available
- Pandoc or Calibre release new versions with breaking changes
- Additional output formats are needed (e.g., DOCX, LaTeX)
- Platform-specific installation steps change