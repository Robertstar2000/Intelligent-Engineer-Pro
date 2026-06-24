---
name: business-book-production
displayName: Business Book Production Pipeline
description: "End-to-end workflow for producing business books from authoritative source documents (DOCX/PDF). Covers manuscript conversion, image handling, 6x9 PDF/EPUB generation, quality assessment, and KDP readiness. Triggered when producing, updating, or rebuilding business book outputs."
category: publishing
tags: [business-book, manuscript, docx-to-markdown, pdf, epub, 6x9, kdp, image-handling, quality-assessment]
triggers: [business book, rebuild business book, update business book, convert docx to manuscript, business book pdf, business book epub, 6x9 business book, kdp business book]
---

# Business Book Production Pipeline

## When to Use

- Producing a business book from a source document (DOCX, PDF, etc.)
- Rebuilding business book outputs (HTML, EPUB, PDF) after source changes
- Converting an authoritative source document into the pipeline's MANUSCRIPT.md format
- Fixing formatting issues specific to business books (images, title pages, page numbers, trim size)
- Running quality assessment on a business book manuscript

## CRITICAL RULE: Authoritative Source First

**NEVER rewrite, generate, or "improve" a business book manuscript from scratch.** The user provides authoritative source documents (typically DOCX). The workflow is:

1. Convert the source document to markdown
2. Replace MANUSCRIPT.md with the converted content
3. Run quality assessment
4. Rebuild outputs (HTML, EPUB, PDF)

The user explicitly corrected: "you have rewriten the book with to much made up and fake examples use this privious version." When a source document exists, it IS the manuscript. Don't add fictional case studies, don't invent examples, don't "expand" with generated content.

## Source Document Conversion

### DOCX to Markdown

Use `python-docx` to extract text with style information:

```python
import docx, re

def convert_docx_to_md(doc):
    lines = []
    for para in doc.paragraphs:
        style = para.style.name
        text = para.text.strip()
        if not text:
            lines.append('')
            continue
        # Skip TOC entries (tab-separated page numbers)
        if re.match(r'^.+\t\d+$', text):
            continue
        if style == 'Heading 1':
            lines.append(f'# {text}')
        elif style == 'Heading 2':
            lines.append(f'## {text}')
        elif style == 'Heading 3':
            lines.append(f'### {text}')
        else:
            # Handle bold/italic runs
            formatted = []
            for run in para.runs:
                t = run.text
                if run.bold and run.italic:
                    formatted.append(f'***{t}***')
                elif run.bold:
                    formatted.append(f'**{t}**')
                elif run.italic:
                    formatted.append(f'*{t}*')
                else:
                    formatted.append(t)
            lines.append(''.join(formatted))
    return '\n'.join(lines)
```

### Post-Conversion Fixes

After converting, apply these fixes to the MANUSCRIPT.md:

1. **Remove duplicate title page** — If the source has `# Title` at the start AND the PDF template generates a title page, strip the manuscript's title to avoid duplication:
   ```python
   # Remove lines matching "# Title" and "## Subtitle" at the start
   # Keep from "# Contents" or first chapter heading onward
   ```

2. **Fix image paths** — Convert `images/filename.png` to just `filename.png` (WeasyPrint resolves relative to the output directory):
   ```python
   content = re.sub(r'!\[([^\]]*)\]\(images/([^)]+)\)', r'![\1](\2)', content)
   ```

3. **Insert chapter images** — If images exist in `images/` but aren't referenced in the manuscript, insert them after chapter headings:
   ```python
   # Map chapter numbers to image files
   # Insert: ![Chapter N — Title](filename.png) after each # Chapter N: heading
   ```

4. **Add missing back matter** — If the source lacks "About the Author", append it.

## Business Book Format Specifications

### Trim Size: 6"×9" (Trade Paperback)

All business books use 6×9. **NOT 8.5×11" (letter).** The user explicitly corrected this.

### PDF Page Setup

```
@page {
    size: 6in 9in;
    margin: 0.65in 0.75in;
    @bottom-center { content: counter(page); font-size: 8pt; color: #888; }
}
@page:first { @bottom-center { content: none; } }
@page toc { @bottom-center { content: counter(page, lower-roman); }}
```

- Font: 10pt Times New Roman/Georgia, line-height 1.45
- Page numbers: Arabic for content pages, Roman for TOC
- First page (title): no page number

### Images: Full Page Width, B&W, No Duplicates

All book images are converted to B&W (grayscale) for print output — including business books. The `get_bw_image_path()` function in `utils.py` handles conversion for all genres.

**Image sizing CSS:**
```css
.chapter-image { text-align: center; margin: 1em 0; page-break-inside: avoid; }
.chapter-image img { width: auto; max-width: 100%; height: auto; max-height: 400px; }
```

**Critical: No duplicate images.** The pipeline inserts images manually via `<div class="chapter-image">` in `step_pdf.py` and `step_epub.py`. Therefore, markdown image syntax `![alt](path)` in the manuscript must be stripped before HTML conversion — otherwise `md_to_html_simple()` converts it to a second `<img>` tag, causing every image to appear twice.

```python
# In step_pdf.py and step_epub.py, before md_to_html_simple():
content = re.sub(r'!\[[^\]]*\]\([^)]+\)\s*\n?', '', content)
```

**Critical: No duplicate chapter headings.** The PDF/EPUB templates generate `<h3>Chapter N: Title</h3>` headings. If the manuscript also contains `# Chapter N: Title`, it gets converted to a duplicate `<h3>` by `md_to_html_simple()`. Strip it:

```python
# Strip the chapter heading line that matches the template's heading
content = re.sub(r'^#{1,2}\s+Chapter\s+\d+\s*[:—\-–]?\s*.*?\n', '', content, count=1)
```

In the PDF generator, copy images to the output directory and reference by filename only.

### Single Title Page

The PDF template generates its own title page from book metadata. The manuscript should NOT contain a duplicate `# Title` heading at the start. Strip it during conversion.

### Page Numbers Synced with TOC (PDF Only)

The PDF TOC must show page numbers with dot leaders. The EPUB TOC must NOT show page numbers.

**PDF TOC HTML structure:**
```html
<p class="toc-entry"><span class="toc-title">Chapter N: Title</span><a href="#chN" class="toc-page-num"></a></p>
```

**PDF TOC CSS:**
```css
.toc-entry { margin: 0.3em 0; text-indent: 0; font-size: 9.5pt; overflow: hidden; }
.toc-entry .toc-title { border-bottom: 1px dotted #000; display: inline-block; width: 70%; vertical-align: bottom; }
.toc-entry .toc-page-num { float: right; text-decoration: none; color: inherit; }
.toc-entry .toc-page-num::after { content: target-counter(attr(href), page); }
```

WeasyPrint's `target-counter(attr(href), page)` resolves the page number from the anchor's `href`. The `border-bottom: 1px dotted` on the title span creates the dot leader. Do NOT use `leader(dotted)` CSS — WeasyPrint does not support it.

Typical page flow:
- Page i: Title page (no number shown)
- Page ii: Copyright page
- Page iii: TOC
- Page 4+: Content chapters

## EPUB Generation

Use the `hermes_publish/step_epub.py` pipeline. Key settings for business books:
- Images: B&W (all genres convert to grayscale for print via `images_bw/` directory)
- CSS: `img { max-width: 100%; height: auto; display: block; margin: 1em auto; }`
- Include toc.ncx for KDP backward compatibility
- Include landmarks nav with bodymatter for "Start Reading" location

## Quality Assessment Checklist

Run this checklist before rebuilding outputs:

- [ ] **Source fidelity**: Manuscript matches the authoritative source document
- [ ] **No made-up content**: No fictional case studies, names, or examples not in the source
- [ ] **Structure**: Proper heading hierarchy (H1 for chapters, H2 for sections, H3 for subsections)
- [ ] **TOC present**: Table of contents at the front
- [ ] **Images present**: All referenced images exist in `images/` directory
- [ ] **Image paths correct**: Paths are relative to output directory (not `images/...`)
- [ ] **Single title page**: No duplicate title in manuscript
- [ ] **About the Author**: Present at end of manuscript
- [ ] **Word count**: Sufficient for target page count (~350 words/page for 6×9)
- [ ] **No duplicate content**: No repeated paragraphs across chapters (template elements like ROI formulas are OK)
- [ ] **Chapter numbering**: Sequential, no gaps

## Common Pitfalls

### WRONG: Generating content from scratch
When the user provides a DOCX, convert it. Don't write a new manuscript inspired by the DOCX.

### WRONG: Using letter size (8.5×11)
Business books are 6×9. Always.

### WRONG: Keeping duplicate title page
If the PDF template generates a title page, strip the manuscript's `# Title` heading.

### WRONG: Forgetting to convert markdown images to HTML
`md_to_html_simple()` must convert `![alt](path)` to `<img src="path" alt="alt" />` for WeasyPrint to render them.

### WRONG: Image paths with `images/` prefix
WeasyPrint resolves paths relative to the output directory. Use `filename.png` not `images/filename.png`.

### WRONG: Color images for business books
ALL books use B&W images for print output. The `get_bw_image_path()` function converts all images to grayscale. Business books are NOT exempt.

### WRONG: Duplicate images (markdown + manual insertion)
If the manuscript contains `![alt](path)` AND the pipeline inserts `<div class="chapter-image"><img>`, every image appears twice. Strip markdown image syntax from content before HTML conversion.

### WRONG: Duplicate chapter headings (template + manuscript)
If the manuscript starts a chapter with `# Chapter N: Title` AND the template generates `<h3>Chapter N: Title</h3>`, the heading appears twice. Strip the manuscript's chapter heading line.

### WRONG: Images overflowing margins
Using `width: 100%` on chapter images causes them to overflow the page margins. Use `width: auto; max-width: 100%; height: auto; max-height: 400px;` instead.

### WRONG: PDF TOC missing page numbers
The PDF TOC must show page numbers with dot leaders. Use `target-counter(attr(href), page)` on a separate `<a>` element with `border-bottom: 1px dotted` on the title span. The EPUB TOC must NOT show page numbers.

## Manuscript Formatting Requirements

### Tables: Use Markdown, Not Inline Text

When the source has structured data (timelines, comparison tables, exercise grids), convert to markdown tables — NOT inline text with brackets and underscores. `md_to_html_simple()` now supports markdown tables:

```markdown
| Quarter | Focus Area 1 | Focus Area 2 |
|---------|-------------|-------------|
| Q1 | [Quick Win] ____________ | [Foundation] ____________ |
```

**Detection:** Lines containing `|` where the next line is a separator (`|---|---|`) are converted to `<table>` HTML with proper `<thead>`, `<tbody>`, `<th>`, `<td>` tags.

**Pitfall:** Inline text like `Quarter 1: [Item] ____ [Item] ____` renders as a single wrapping paragraph — columns don't align, lines break randomly. Always use markdown tables for grid-like content.

### Lists: Use Markdown Bullet Syntax

When the source has "Do:" / "Don't:" lists or any enumerated items, use markdown bullet syntax:

```markdown
- Start with Why: Always begin with your business objectives
- Involve Your Team: Get input from those who will use AI
```

`md_to_html_simple()` converts `- item` to `<ul><li>` and `1. item` to `<ol><li>`.

**Pitfall:** Plain text lists (no `-` or `*` prefix) render as a single justified paragraph with no visual separation between items.

### Form Fields: Label on Its Own Line

For fill-in-the-blank exercise sections, put the label and the underline on SEPARATE lines using `<br/>`:

```markdown
**Biggest Financial Frustration:**<br/>_____________________________________________
```

**Pitfall:** Putting the label and underline on the same line (`**Label:** ________`) causes WeasyPrint to wrap the underscores to the next line, splitting the label across the page width. The `<br/>` tag forces the underline onto its own line below the label.

### Checkbox Lists

For checkbox-style lists, use `- [ ] item` syntax:

```markdown
- [ ] Automated bookkeeping
- [ ] Cash flow forecasting
```

This renders as a bulleted list with the `[ ]` text preserved in each item.

## Pipeline Integration

For CSS code snippets and pipeline patterns, see `references/pipeline-image-css.md`.
For markdown table/list formatting rules, see `references/md-to-html-tables-lists.md`.

This skill works with the `hermes_publish` pipeline at `/mnt/usb_4tb/books/hermes_publish/`:
- `step_pdf.py` — PDF generation via WeasyPrint
- `step_epub.py` — EPUB 3 generation via zipfile
- `utils.py` — `collect_chapters()`, `md_to_html_simple()` (now supports tables, lists), `get_bw_image_path()`
- `config.py` — Book registry with title, author, series, genre, manuscript_type

### Rebuild All Three Formats

After updating MANUSCRIPT.md, rebuild ALL three output formats — PDF, EPUB, and HTML:

```bash
cd /mnt/usb_4tb/books
python3 -c "
from hermes_publish.step_pdf import run as run_pdf
from hermes_publish.step_epub import run as run_epub
from hermes_publish.config import BOOK_REGISTRY
k = 'ai-that-works'
b = BOOK_REGISTRY[k]
run_pdf(k, b)  # Generates PDF + HTML
run_epub(k, b)  # Generates EPUB
"
```

The HTML is generated as a byproduct of the PDF step (same HTML that WeasyPrint converts). All three are written to the `output/` directory.
