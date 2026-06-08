# TOC Page-Number Synchronization — 2-Pass Rendering Workflow

## Problem
WeasyPrint cannot reliably render single-line TOC entries with CSS `white-space: nowrap` on table cells or divs — inline elements always wrap. CSS `target-counter(attr(href url), page)` with `float: right` is also unreliable when titles wrap.

## Solution: 2-Pass Rendering with `<pre>` tag

The ONLY approach proven to work: use `<pre>` tag with `white-space: pre` and embed page numbers as plain text in a second pass.

### Pass 1: Render with Empty Page Numbers

Build HTML with a `<pre>` TOC containing chapter number + title, no page numbers:

```html
<pre style="font-family:Georgia,serif;font-size:10pt;line-height:1.5;white-space:pre;overflow:hidden;page-break-after:both;">
Chapter 1  The Artemis Accord
Chapter 2  First Footsteps
Chapter 3  Site Selection
</pre>
```

Render: `weasyprint input.html output1.pdf`

### Extract Page Numbers from PDF

```python
import subprocess, re

def extract_pages(pdf_path, chapters):
    """Extract page numbers for each chapter heading from a rendered PDF."""
    r = subprocess.run(['pdftotext', pdf_path, '-'], capture_output=True, text=True)
    lines = r.stdout.split('\n')
    page_num = 0
    ch_pages = {}
    
    for line in lines:
        s = line.strip()
        if s.isdigit() and int(s) < 1000:
            page_num = int(s)
        for ch in chapters:
            # Match "Chapter N — Title" pattern
            if re.match(r'^Chapter\s+%d\s*[—–-]' % ch['n'], s, re.IGNORECASE):
                ch_pages[ch['n']] = page_num
                break
            if s == ("Chapter %d" % ch['n']):
                ch_pages[ch['n']] = page_num
                break
    
    # Fill any missing with sequential estimates
    last_pg = 3
    for ch in chapters:
        if ch['n'] in ch_pages:
            last_pg = ch_pages[ch['n']]
        else:
            ch_pages[ch['n']] = last_pg
            last_pg += 3  # rough estimate per chapter
    return ch_pages
```

### Pass 2: Inject Page Numbers and Re-render

Replace the `<pre>` TOC content with page numbers appended:

```html
<pre style="font-family:Georgia,serif;font-size:10pt;line-height:1.5;white-space:pre;overflow:hidden;page-break-after:both;">
Chapter 1  The Artemis Accord  3
Chapter 2  First Footsteps  8
Chapter 3  Site Selection  13
</pre>
```

Re-render: `weasyprint input.html output_final.pdf`

## Chapter Title Extraction

When extracting titles from XHTML chapter files, use this function that handles both `<h1>` and `<h2>` tags:

```python
def get_title(content):
    """Extract chapter title, stripping 'Chapter N — ' prefix."""
    for tag in ['h1', 'h2']:
        m = re.search(r'<%s[^>]*>(.*?)</%s>' % (tag, tag), content, re.DOTALL)
        if m:
            t = re.sub(r'<[^>]+>', '', m.group(1)).strip()
            # Handle both literal dash and &mdash; entity
            t = re.sub(r'^Chapter\s+\d+\s*(&mdash;|—|–|-)\s*', '', t, flags=re.IGNORECASE).strip()
            return t
    # Fallback to <title> tag
    m = re.search(r'<title>(.*?)</title>', content)
    if m:
        t = m.group(1).strip()
        return re.sub(r'^Chapter\s+\d+\s*(&mdash;|—|–|-)\s*', '', t, flags=re.IGNORECASE).strip()
    return None
```

**CRITICAL**: The `&mdash;` HTML entity must be in the regex. Books generated with Python often use `&mdash;` (HTML entity) instead of `—` (Unicode character). Missing the entity causes doubled titles like "Chapter 37 Chapter 37 — The New Drill".

## Verifying TOC in Final PDF

```bash
# Check that each TOC entry is exactly 1 line (no wrapping)
pdftotext output_final.pdf - | grep -A2 "Contents"

# Or verify with Python:
python3 -c "
import subprocess
r = subprocess.run(['pdftotext', 'output_final.pdf', '-'], capture_output=True, text=True)
for line in r.stdout.split(chr(10))[:20]:
    if line.strip():
        print('|%s|' % line.strip()[:80])
"
```

Expected output:
```
|Contents|
|Chapter 1 The Artemis Accord 3|
|Chapter 2 First Footsteps 8|
|Chapter 3 Site Selection 13|
```

Each entry on one line with title and page number together.

## Common Pitfalls

1. **`&mdash;` not handled in title extraction regex**: Always include `&mdash;` in the regex pattern. Books use either literal `—` or `&mdash;` depending on how they were generated.

2. **Whitespace matters in `<pre>`**: The `<pre>` tag preserves all whitespace. Use two spaces between elements, not tabs, to ensure consistent rendering.

3. **`table-layout: fixed` does NOT work**: CSS `white-space: nowrap` on `<table>` cells is ignored by WeasyPrint for TOC entries. The `<pre>` approach is the ONLY reliable method.

4. **pdftotext -layout flag**: If `pdftotext -layout` returns garbled text, drop the `-layout` flag. It's not needed for `<pre>`-based TOC extraction.

5. **Book title extraction**: Waters End book uses `<h2>` for chapter titles (not `<h1>`). Always check both heading levels.