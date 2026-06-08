# Back Cover PDF Generation

Generate a standalone back-cover PDF (6×9in) containing the book description, author bio, barcode/ISBN placeholder, and genre categories.

## When to Use

After a book's front cover is finalized and before delivering the KDP package. The back cover PDF is a separate deliverable — not embedded in the interior PDF — but should be included in the Print/ folder of the KDP package alongside the wrap cover.

## Template

Create an HTML file with this structure:

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Back Cover - [Book Title]</title>
<style>
@page {
    size: 6in 9in;
    margin: 0.5in;
}
body {
    font-family: Georgia, 'Times New Roman', serif;
    font-size: 10pt;
    line-height: 1.6;
    max-width: 4.5in;
    margin: 0 auto;
    padding: 20px;
}
h1 { font-size: 14pt; text-align: center; margin-bottom: 5px; }
.subtitle { font-size: 11pt; font-style: italic; text-align: center; color: #555; }
hr { border: none; border-top: 1px solid #ccc; margin: 20px 0; }
.description p { text-align: justify; margin-bottom: 12px; }
.quote { font-style: italic; text-align: center; color: #666; font-size: 9pt; }
.author-bio { font-size: 9pt; border-top: 1px solid #ddd; padding-top: 15px; }
.barcode-area { text-align: center; margin-top: 30px; border: 1px dashed #aaa; padding: 10px; font-size: 8pt; color: #999; }
.isbn { text-align: center; font-size: 8pt; color: #777; }
.genre { text-align: center; font-size: 8pt; color: #888; margin-top: 25px; }
</style>
</head>
<body>
  <!-- INSERT BOOK INFO HERE -->
</body>
</html>
```

## Content to Include

1. **Title + Subtitle** — centered at top
2. **Description** — 3-5 paragraphs, compelling hook first, then deeper narrative summary
3. **Endorsement/Quote** — optional, e.g. "For readers of [Author]..."
4. **Author Bio** — 1-2 sentences about the author's background
5. **Barcode placeholder** — `[ BARCODE / ISBN ]` with actual ISBN number below
6. **Genre categories** — Amazon BISAC categories (e.g., "BIOGRAPHY & AUTOBIOGRAPHY / Personal Memoirs")

## Generation

```bash
weasyprint back_cover.html BackCover.pdf
```

## KDP Package Placement

Copy the resulting PDF to: `BookName_KDP_PACKAGE/Print/BookName_BackCover.pdf`

This is a standalone asset — KDP's cover creator handles the full wrap cover separately.

## Pitfalls

- Don't use large images or heavy CSS — the back cover is text-only for most KDP scenarios
- If using a barcode image, generate it at 300 DPI and embed as base64 in the HTML
- The PDF page size must match the book trim size (6×9in), not the wrap cover dimensions
- Author bio should match the one in `Marketing_and_Compliance/Author_Bio.md` for consistency