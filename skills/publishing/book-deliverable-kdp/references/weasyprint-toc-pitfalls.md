# WeasyPrint TOC Rendering Pitfalls

## Problem
WeasyPrint corrupts TOC text and layout when certain CSS properties and HTML structures are used. This manifests as garbled/overlapping text in the rendered PDF.

## Root Causes & Fixes

### 1. `string-set: chapter-title content()` on h1/h2 CAUSES TOC CORRUPTION

**Symptom:** Every TOC entry shows garbled text -- characters from the first chapter title ("Everything Changed") appear overlaid on all other entries. E.g., "Chapter 2 -- Fire, Earthquaything Changed" or "Chapter 37 -- Crisis Leaderything".

**Root cause:** WeasyPrint's string-set mechanism captures the text content of the first h1 with `string-set` and misapplies it during TOC rendering, especially when `<a>` tags are used in table cells.

**Fix:** Remove BOTH:
```css
/* REMOVE from h1 and h2: */
string-set: chapter-title content();

/* REMOVE from @page: */
@top-center { content: string(chapter-title); font-size: 7pt; color: #999; }
```
Replace with:
```css
@top-center { content: none; }
```

### 2. `<a>` Tags in TOC Table Cells Cause Text Corruption

**Symptom:** Same garbled text as above. The PDF text extraction shows overlapping/misplaced characters.

**Root cause:** WeasyPrint mishandles `<a>` (anchor) tags inside table cells, especially combined with `overflow: hidden` and `table-layout: fixed`. The link text from `<a>` tags gets corrupted during rendering.

**Fix:** Replace all `<a>` tags in TOC entries with plain text:
```html
<!-- WRONG: -->
<td class="toc-ch"><a href="#chapter-1">Chapter 1 -- Title</a></td>

<!-- CORRECT: -->
<td class="toc-ch">Chapter 1 -- Title</td>
```
Note: `<a>` tags are only needed for EPUB/HTML navigation. Print PDF doesn't need clickable TOC links.

### 3. `table-layout: fixed` with `width: auto` Cells

**Symptom:** TOC entries render with incorrect widths, text overlapping into adjacent cells.

**Fix:** Use `table-layout: auto` for the TOC table:
```css
.toc-table {
    width: 100%;
    table-layout: auto;  /* NOT fixed */
}
```

### 4. `@top-center` Running Header with `string-set`

Even after fixing the TOC, the `@top-center` running header from `string-set` can cause rendering artifacts on Part/chapter opening pages where the heading appears both as a running header AND the actual heading text, creating a doubled effect.

**Fix:** Disable running headers entirely:
```css
@page {
    @top-center { content: none; }
}
```

## Verified TOC Structure (No Corruption)

```html
<style>
@page {
    size: 6in 9in;
    margin: 0.7in 0.6in 0.8in 0.6in;
    @bottom-center { content: counter(page); font-size: 8pt; color: #666; }
    @top-center { content: none; }
}

h1 { page-break-before: always; /* NO string-set */ }
h2 { page-break-before: always; /* NO string-set */ }

.toc { page-break-before: always; page-break-after: always; }
.toc-table { width: 100%; table-layout: auto; }
.toc-table td { padding: 0.2em 0; vertical-align: baseline; border: none; }
.toc-ch { white-space: nowrap; padding-right: 0.5em; font-size: 9pt; }
.toc-dots { width: 100%; border-bottom: 1px dotted #888; padding: 0 0.3em; }
.toc-pge { width: 2em; white-space: nowrap; text-align: right; padding-left: 0.3em; }
.toc-part { font-weight: bold; font-size: 1.1em; padding-top: 0.8em; }
</style>

<div class="title-page" style="text-align:center; padding-top:30%; page-break-after:always;">
  <h1>The Book Title</h1>
  <h2>Subtitle</h2>
  <p><strong>by Author</strong></p>
  <hr />
  <p><strong>Disclaimer:</strong> ...</p>
</div>

<div class="toc" id="table-of-contents" style="page-break-before: always;">
  <h2 style="text-align:center; margin-bottom:1em;">Table of Contents</h2>
  <table class="toc-table">
    <tr><td class="toc-part" colspan="3">PART I: Section Name</td></tr>
    <tr><td class="toc-ch">Chapter 1 -- Title Here</td><td class="toc-dots"></td><td class="toc-pge">5</td></tr>
    <!-- NO <a> tags in toc-ch cells -->
  </table>
</div>

<h1 id="part-i">PART I: Section Name</h1>
```

## Verification After Render

Always verify TOC text integrity after PDF generation:

```python
from pypdf import PdfReader

r = PdfReader("output.pdf")
for i in range(min(5, len(r.pages))):
    text = r.pages[i].extract_text() or ""
    if "Chapter" in text or "PART" in text:
        lines = [l for l in text.strip().split('\n') if l.strip()]
        for l in lines[:3]:
            if 'thing' in l or 'verythin' in l:
                print(f"CORRUPTION on page {i+1}: {l}")
```

Any occurrence of garbled text fragment strings ("thing Changed", "verythin") means the `string-set` or `<a>` tag fix was not applied.
