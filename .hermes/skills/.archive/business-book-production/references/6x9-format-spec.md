# 6"×9" Business Book Format Spec

## Page Setup
- **Trim size**: 6" × 9" (152.4 × 228.6 mm)
- **Margins**: 0.65" top/bottom, 0.75" left/right
- **Font**: 10pt Times New Roman or Georgia
- **Line height**: 1.45
- **Text alignment**: justify

## Page Numbers
- **Location**: Footer, centered
- **Style**: 8pt, color #888
- **TOC pages**: Roman numerals (i, ii, iii)
- **Content pages**: Arabic numerals (1, 2, 3...)
- **Title page**: No page number

## Images
- **Width**: 100% of text area (full page width minus margins)
- **Height**: auto (no max-height constraint)
- **Alignment**: centered
- **Color**: Color (business books retain color; only fiction/memoir get B&W)
- **Page break**: avoid (keep image with surrounding text)

## Title Page
- **ONE title page only** — the PDF template generates it from book metadata
- **Strip any `# Title` heading from the manuscript** to avoid duplication
- **Copyright page** follows the title page

## TOC
- Generated from H1 (`#`) and H2 (`##`) headings
- Chapter-level entries only (not H3 subsections)
- Page numbers auto-resolved by WeasyPrint counters

## Typical Page Flow
| Page | Content | Number |
|------|---------|--------|
| i | Title page | (none) |
| ii | Copyright | ii |
| iii | TOC | iii |
| 4+ | Chapter 1+ | 4, 5, 6... |

## Word Count to Page Count
- ~350 words per page at 6×9 with 10pt font
- 30,000 words ≈ 86 content pages + 6 front/back = ~92 total
- 50,000 words ≈ 143 content pages + 6 = ~149 total
- 70,000 words ≈ 200 content pages + 6 = ~206 total
