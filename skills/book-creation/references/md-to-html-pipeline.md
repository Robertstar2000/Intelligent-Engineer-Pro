# Markdown-to-HTML Pipeline Reference

## md_to_html_simple() — What It Handles

Located in `hermes_publish/utils.py`. Converts basic markdown to HTML for PDF/EPUB generation.

### Supported syntax

| Markdown | HTML Output |
|----------|-------------|
| `# Title` | `<h3>Title</h3>` (lv 1-3) or `<h4>` (lv 4+) |
| `**bold**` | `<b>bold</b>` |
| `*italic*` | `<em>italic</em>` |
| `- item` | `<ul><li>item</li></ul>` |
| `1. item` | `<ol><li>item</li></ol>` |
| `\| table \|` | `<table><thead>...<tbody>...</table>` with bordered cells |
| `![alt](src)` | `<img src="..." alt="..." />` |
| `---` / `***` | `<p class="scene-break">* * *</p>` |
| `<br/>` | passed through as-is (for form field separation) |
| `&` (bare) | `&amp;` |
| `<` / `>` (non-tag) | `&lt;` / `&gt;` |

### Table detection rules
- Line must contain `|`
- Next line must match `^\|?[\s\-:|]+\|?$` and contain `-`
- Header row → `<thead><tr><th>...</th></tr></thead>`
- Data rows → `<tbody><tr><td>...</td></tr></tbody>`
- Cell style: `border:1px solid #000;padding:0.3em;font-size:9pt;`

### List detection rules
- Unordered: line starts with `- `, `* `, or `+ `
- Ordered: line starts with `digit. `
- Nested lists: indent with 2+ spaces before `- `

### What it does NOT handle
- Nested markdown (bold inside list items works, but complex nesting may not)
- HTML passthrough (only recognized tags are preserved — see `tag_re` regex)
- `leader(dotted)` CSS — unsupported in WeasyPrint, use `border-bottom: 1px dotted` instead
- `target-counter()` — works in WeasyPrint but only on `<a>` elements with `href`

## Image Pipeline

### B&W conversion
- ALL books (fiction, memoir, mystery, business) use B&W chapter images
- Source: `images/ch{NN}.png` → `images_bw/ch{NN}.png` via PIL `convert('L')`
- Pipeline step: `get_bw_image_path()` returns `images_bw/` path for all genres
- Called by `step_pdf.py` and `step_epub.py` automatically

### Image sizing (PDF)
- CSS: `.chapter-image img { width: auto; max-width: 100%; height: auto; max-height: 400px; }`
- Images are NOT duplicated — pipeline inserts one `<div class="chapter-image">` per chapter
- Markdown `![]()` syntax in manuscript is stripped before conversion (pipeline handles insertion)

## TOC Pipeline (PDF)

### Dot leaders
- Use `border-bottom: 1px dotted #000` on a `<span class="toc-title">` inside the `<a>` tag
- Do NOT use `content: leader(dotted)` — unsupported in WeasyPrint

### Page numbers
- Use `target-counter(attr(href), page)` on `<a>` elements in the TOC
- WeasyPrint resolves these to actual page numbers during PDF rendering
- EPUB TOC (NCX) does NOT include page numbers

### HTML structure
```html
<p class="toc-entry">
  <a href="#ch1">
    <span class="toc-title" style="border-bottom:1px dotted #000;display:inline-block;width:70%;">Chapter 1: Title</span>
    <span class="toc-page-num" style="float:right;"></span>
  </a>
</p>
```
- `::after` pseudo-element on `.toc-page-num` fills in the page number via `target-counter`

## Common Pitfalls (from session corrections)

1. **Duplicate images**: Caused by both pipeline insertion AND markdown `![]()` in manuscript. Fix: strip markdown images from content before `md_to_html_simple()`.

2. **Duplicate chapter titles**: Template generates `<h3>` AND manuscript has `# Chapter N:`. Fix: strip first heading line from each chapter's content.

3. **Broken table layouts**: Inline text with `[item] ______` renders as one wrapping paragraph. Fix: use proper markdown pipe tables.

4. **Broken form fields**: Long labels + long blanks on same line wrap mid-line. Fix: use `<br/>` between label and underline.

5. **Plain text lists**: Items without `-` prefix don't get bullets. Fix: always use `- item` format.

6. **Problem/Solution on one line**: Wraps awkwardly. Fix: put `**Problem:**` and `**Solution:**` on separate lines.

7. **target-counter() on wrong element**: Only works on elements with `href` attribute. Fix: put `href` on the `<a>` element, apply `::after` to a child span.

8. **Business book page size**: Must be 6×9", not 8.5×11. KDP rejects non-standard trim sizes.
