# TOC HTML Template for Print PDFs

## Problem
TOC entries in WeasyPrint PDFs wrap across multiple lines:
```
Chapter 1
The Artemis Accord
            3
```

## Solution: Use `<pre>` tag with `white-space: pre`

The ONLY reliable way to prevent TOC entry wrapping in WeasyPrint.
Table-based layouts with `white-space: nowrap` DO NOT WORK -- WeasyPrint
breaks lines inside table cells regardless of CSS nowrap settings.

## HTML Pattern

```html
<pre class="toc">
Chapter 1  The Artemis Accord  3
Chapter 2  First Footsteps  6
Chapter 3  Site Selection  9
</pre>
```

## Required CSS

```css
pre.toc {
  font-family: Georgia, serif;
  font-size: 10pt;
  line-height: 1.5;
  white-space: pre;
  margin: 1em 0 2em 0;
  padding: 0;
  overflow: hidden;
  page-break-after: both;
}
```

## Page Numbers -- 2-Pass Render Approach

WeasyPrint cannot auto-fill page numbers in the TOC reliably. Use 2-pass:

**Pass 1:** Render with empty page numbers, then extract actual page numbers:
```python
def extract_pages(pdf_path, chapters):
    r = subprocess.run(['pdftotext', pdf_path, '-'], capture_output=True, text=True)
    lines = r.stdout.split('\n')
    page_num = 0
    ch_pages = {}
    for line in lines:
        s = line.strip()
        if s.isdigit() and int(s) < 1000:
            page_num = int(s)
        for ch in chapters:
            if re.match(r'^Chapter\s+%d\s*[--]' % ch['n'], s, re.IGNORECASE):
                ch_pages[ch['n']] = page_num
                break
    return ch_pages
```

**Pass 2:** Re-render with hardcoded page numbers.

## Chapter Title Extraction
- Try h1 first, then h2 (some books use h2), then `<title>` tag
- NEVER use filenames (ch001, ch002) as titles
- Strip prefix including HTML entity: `re.sub(r'^Chapter\s+\d+\s*(&mdash;|\xe2\x80\x94|-)\s*', '', t, flags=re.IGNORECASE)`

## What Does NOT Work
- `<table>` with `table-layout: fixed` -- WeasyPrint ignores nowrap in cells
- `display: flex` with `white-space: nowrap` -- flex items still wrap
- `target-counter()` -- unreliable, fails when titles wrap
- `white-space: nowrap` on `<li>` -- WeasyPrint breaks inline children

## Why `<pre>` Works
`white-space: pre` tells WeasyPrint: do NOT reflow. Source line breaks = output line breaks.