# Print Book Page-Break CSS Patterns

## Problem
Print PDFs require precise control over which sections start on a new page:
- Title page, TOC, and each Part must all start on fresh pages
- WeasyPrint must handle page breaks via CSS, not manual insertions

## Verified HTML Structure

```html
<head>
<style>
@page {
    size: 6in 9in;
    margin: 0.7in 0.6in 0.8in 0.6in;
    @bottom-center { content: counter(page); font-size: 8pt; color: #666; }
    @top-center { content: none; }
}
@page :first { @top-center { content: none; } @bottom-center { content: none; } }

/* Title page: ends with page-break-after so TOC starts fresh */
.title-page {
    text-align: center;
    padding-top: 30%;
    page-break-after: always;
}

/* TOC: starts AND ends with page break */
.toc { page-break-before: always; page-break-after: always; }

/* All h1/h2 headings start on new page (for chapter/part breaks) */
h1 { page-break-before: always; /* ... */ }
h2 { page-break-before: always; /* ... */ }
</style>
</head>
<body>

<!-- Title page content wrapped in a div -->
<div class="title-page">
  <h1>The Book Title</h1>
  <h2>Subtitle</h2>
  <p><strong>by Author Name</strong></p>
  <hr />
  <p><strong>Disclaimer:</strong> ...</p>
  <hr />
</div>

<!-- TOC as a self-contained div -->
<div class="toc" id="table-of-contents" style="page-break-before: always;">
  <h2 style="text-align:center;">Table of Contents</h2>
  <table class="toc-table">
    <!-- TOC rows -->
  </table>
</div>

<!-- Part/Chapter headings follow naturally; h1 has page-break-before -->
<h1 id="part-i">PART I: RECOGNIZE — The Risk Landscape</h1>
<h2 id="chapter-1">Chapter 1 — Title</h2>
...
</body>
```

## Key Rules

1. **`page-break-after: always` on title-page div**: Forces TOC to the next page. Without this, the TOC's `page-break-before` may be consumed by the title page content and not produce a visible break.

2. **`page-break-after: always` on .toc div**: Forces Part I heading to start on a new page after the TOC. Without this, the Part I heading and TOC end up on the same page.

3. **Inline `style="page-break-before: always;"` on the TOC div**: Belt-and-suspenders. The CSS class handles it, but the inline style ensures it even if the CSS class is partially overridden.

4. **Global `h1 { page-break-before: always; }`**: This is what makes Part headings (and all chapters) start on new pages. Works because the preceding element (TOC div) has `page-break-after: always`. Do NOT add `string-set: chapter-title content()` to h1/h2 -- it corrupts TOC text in WeasyPrint.

5. **Do NOT put `<hr />` separators between TOC div and Part heading**: The page break handles visual separation. Extra `<hr>` tags create blank space on the new page.

## What Does NOT Work

- `page-break-after: none` on the TOC div — this prevents Part I from starting on its own page
- A `<hr />` between the closing `</div>` of TOC and the `<h1>` of Part I — produces a stray line at the top of the new page
- CSS `page-break-inside: avoid` on part headings — weasyprint sometimes ignores this

## Verification

After generating the PDF, verify page structure:

```python
from pypdf import PdfReader

r = PdfReader("output.pdf")
print(f"Total pages: {len(r.pages)}")

# Find part boundaries
for i in range(len(r.pages)):
    text = r.pages[i].extract_text() or ""
    if any(p in text for p in ["PART I", "PART II", "PART III", "PART IV"]):
        lines = [l for l in text.strip().split('\n') if l.strip()]
        print(f"Page {i+1}: {lines[0][:60]}")
```

Expected: Each "PART X" heading should be the first text element on its page (possibly with a running header from `string-set` above it, which is normal).
