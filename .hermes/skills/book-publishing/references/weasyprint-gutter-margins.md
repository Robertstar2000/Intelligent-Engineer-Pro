# WeasyPrint Gutter Margins & Page Number Gotchas

## Gutter Margin Rules (KDP)

Gutter thresholds are based on **estimated** page count (chapters × pages_per_ch), NOT actual rendered page count. The `_get_gutter_css()` function in `step_pdf.py` uses this estimation.

| Est. Page Count | Gutter (inside) | Outside | Top/Bottom |
|---|---|---|---|
| < 200 pages | 0.5" | 0.25" | 0.25" / 0.25" |
| 200–299 pages | 0.5" | 0.25" | 0.25" / 0.25" |
| 300+ pages | 0.625" | 0.25" | 0.25" / 0.25" |

**Verified:** KDP rejects books with 158+ pages at 0.375" gutter — requires 0.5" minimum.
**Verified:** 318-page book rejected at 0.5" — KDP requires 0.625" for 300+ pages.

**Estimated pages formula:** `chapters × 10` for fiction/mystery, `chapters × 8` for business.

**Examples:**
- Book 1 (30 ch × 10 = 300 est.) → 0.625" gutter
- Book 2 (28 ch × 10 = 280 est.) → 0.5" gutter
- Book 3 (24 ch × 10 = 240 est.) → 0.5" gutter

## CSS Margin Structure

```css
@page {
    size: 6in 9in;
    margin: 0.5in 0.375in 0.6in 0.625in;  /* top right bottom left */
    @bottom-center { content: counter(page); text-align: right; margin-right: 0.1in; margin-bottom: 0.1in; }
}
@page :right {
    margin: 0.5in 0.375in 0.6in 0.625in;  /* gutter on LEFT (binding side for odd pages) */
    @bottom-center { content: counter(page); text-align: right; margin-right: 0.1in; margin-bottom: 0.1in; }
}
@page :left {
    margin: 0.5in 0.625in 0.6in 0.375in;  /* gutter on RIGHT (binding side for even pages) */
    @bottom-center { content: counter(page); text-align: left; margin-left: 0.1in; margin-bottom: 0.1in; }
}
```

**Key:** `@page :right` = odd pages (gutter left), `@page :left` = even pages (gutter right).

## Page Number Positioning — CRITICAL

**Do NOT use `@bottom-right` / `@bottom-left`** — places text at extreme corner, bleeds past KDP outer margin. KDP flags as "page numbers sticking outside allowed outer margins."

**Use `@bottom-center` with `text-align` + `margin` padding:**

```css
@page :right {
    @bottom-center {
        content: counter(page);
        text-align: right;
        margin-right: 0.1in;
        margin-bottom: 0.1in;
    }
}
@page :left {
    @bottom-center {
        content: counter(page);
        text-align: left;
        margin-left: 0.1in;
        margin-bottom: 0.1in;
    }
}
```

**Outside margin >= 0.375"**, **Bottom margin >= 0.6"**.

## Gotchas

1. **Page number duplication:** Don't put `@bottom-right` on both default `@page` AND `@page :right`
2. **`target-counter()` not supported:** Use 2-pass build with hardcoded page numbers
3. **`manuscript_type` mismatch:** `"chapters_md"` looks for individual files in `html/`. Use `"manuscript_md"` for single MANUSCRIPT.md files.
4. **Gemini image model:** Use `gemini-2.5-flash-image` (not `gemini-2.5-flash-image-preview`). Image data is raw bytes, not base64.

## TOC Page Number Extraction — 2-Pass Build

### The Problem
WeasyPrint doesn't support `target-counter()`, so TOC page numbers must be extracted from a first PDF render and hardcoded into the final HTML.

### The Algorithm (`_extract_toc_pages()` in `step_pdf.py`)

```python
def _extract_toc_pages(pdf_path, chapters):
    doc = fitz.open(pdf_path)
    toc_pages = {}
    for cn, ct, _ in chapters:
        search_text = f"Chapter {cn}:"
        found_page = None
        for page_idx in range(4, len(doc)):  # Start after front matter
            page = doc[page_idx]
            text = page.get_text()
            if search_text in text:
                lines = text.split('\n')
                for li, line in enumerate(lines):
                    if search_text in line:
                        # Check if next non-empty line is body text (not a page number)
                        next_text = ''
                        for nli in range(li + 1, min(li + 3, len(lines))):
                            stripped = lines[nli].strip()
                            if stripped:
                                next_text = stripped
                                break
                        # Body text: long (>15 chars), starts with letter
                        # TOC page number: short, starts with digit
                        # Header repeat: starts with "Chapter" (also long, but we take first match)
                        if next_text and len(next_text) > 15 and not next_text[0].isdigit():
                            found_page = page_idx + 1  # 1-indexed
                            break
                if found_page:
                    break
        if found_page:
            toc_pages[cn] = found_page
    return toc_pages
```

### Why the Old Approach Failed

**Old approach (BROKEN):** Start at `range(4, ...)` and check `len(line.strip()) > 20`.

This failed because:
1. The last TOC page (e.g., page 5) contains entries like "Chapter 30: Retainer to Trouble" — same length as actual chapter headings
2. Starting at `range(4, ...)` includes the TOC page itself, so the first match is the TOC reference, not the actual chapter
3. Starting at `range(6, ...)` to avoid the TOC was too far — missed Chapter 1 which starts on page 5-6

**New approach (WORKING):** Check the *next non-empty line* after the heading:
- **TOC page:** Next line is a page number (short, starts with digit) → skip
- **Content page:** Next line is body text (long, starts with letter) → use this page
- **Header repeat:** On content pages, the heading may appear twice (header + h3). The first occurrence's next line is the h3 heading itself (starts with "Chapter", long). This is fine — it's on the correct page.

### Critical Details

1. **Search for `"Chapter N:"` (colon):** The manuscript uses colon format in headings. The TOC also uses colon format. The distinction is the *next line*, not the heading format.

2. **Start at `range(4, ...)` (page 5):** This is early enough to find Chapter 1 (which starts on page 5-6) but the next-line check filters out TOC references.

3. **Skip logic:** TOC pages have the pattern `Chapter N: Title\n\nPAGE_NUM\n` where PAGE_NUM is a short digit string. Content pages have `Chapter N: Title\nChapter N: Title\nBody text...` or `Chapter N: Title\nBody text...`.

4. **Verification:** After building, verify TOC accuracy by comparing hardcoded page numbers against actual chapter heading positions in the rendered PDF. All chapters should match exactly.

### Build Pipeline Summary

1. **Pass 1:** Build PDF with estimated page numbers in TOC
2. **Extract:** Use `_extract_toc_pages()` to find actual chapter start pages
3. **Pass 2:** Rebuild PDF with correct hardcoded page numbers
4. **Verify:** Confirm all TOC entries match actual positions
