# WeasyPrint PDF Generation: Gotchas & Verification

## Images fail silently — use base64 data URIs

When building PDFs with WeasyPrint via HTML, local filesystem `src` paths fail. No errors, just missing images.

**Fix for every `<img src=...>` in HTML:**
1. Read image as binary
2. Encode to base64
3. Replace src with `data:image/{jpeg|png};base64,{base64_string}`
4. Count `data:image` in HTML vs `<img` tags — must match
5. **PDF size sanity check**: A 115-page memoir (180K chars, 6×9) with 5 embedded images should be 2+MB. 0.9MB = images NOT embedded.

## Page count verification

After PDF generation, verify:
```python
from pypdf import PdfReader
r = PdfReader("book.pdf")
print("Pages:", len(r.pages))
```
Standard 6x9 book (11pt Georgia, 180K chars) should be 100-150 pages. 200+ = text too dense.

## TOC page numbering

WeasyPrint supports CSS `target-counter` for synced TOC. Anchored headings must have IDs matching TOC links.