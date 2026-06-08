# KDP Full Spec Reference (Authoritative)

> Source: [KDP Cover Image Guidelines](https://kdp.amazon.com/en_US/help/topic/G200645690) | [Paperback Guidelines](https://kdp.amazon.com/en_US/help/topic/G201857950) | [Hardcover Guide](https://kdp.amazon.com/en_US/help/topic/GDTKFJPNQCBTMRV6) | [Cover Calculator](https://kdp.amazon.com/cover-calculator) | [Formatting Your Book](https://kdp.amazon.com/en_US/help/topic/G200634400) | [eBook Formats](https://kdp.amazon.com/help/topic/G200634390)
> Verified: 2025-05-27
> 
> This is the SINGLE authoritative spec reference. All book skills (book-deliverable-kdp, publishing-workflow, book-publishing, book-cover-design, manuscript-creation) should point here. DO NOT duplicate these tables in other files.

---

## 1. COVER SPECS

### 1A. Quick Reference Table

| Cover Type | File Format | Dimensions | DPI | Color | Max File Size |
|---|---|---|---|---|---|
| **Kindle eBook (marketing)** | JPEG (.jpg) or TIFF | **2560 × 1600 px** ideal; min 1000 × 625 px; max 10k × 10k | 72 (pixel count matters) | **RGB only** (CMYK rejected) | 50 MB |
| **Kindle eBook (internal/EPUB)** | JPEG inside OPF | Large, high-res; ≥50% of first page | — | RGB | — |
| **Paperback wrap** | **PDF** single page (NOT JPEG/PNG) | Calc: 0.125 + Tw + spine + Tw + 0.125 wide × 0.125 + Th + 0.125 tall | **300 min** | CMYK preferred, RGB accepted | 650 MB |
| **Hardcover case laminate** | **PDF** single page | 7-section: wrap+bleed+back+hinge+spine+hinge+front+bleed+wrap | **300 min** | CMYK preferred, RGB accepted | 650 MB |

### 1B. Spine Formulas

**Paperback:**
- White paper (B&W): `page_count × 0.002252"` (0.0572 mm)
- Cream paper (B&W): `page_count × 0.0025"` (0.0635 mm)
- Color interior: `page_count × 0.002347"` (0.0596 mm)

**Hardcover:**
- `(page_count × paper_thickness) + 0.189"` (board thickness)
- Paper thickness: 0.0025" per sheet typical
- Supported trim sizes: 5.5×8.5, 6×9, 6.14×9.21, 6.69×9.61, 7×10, 7.44×9.69, 7.5×9.25, 8.5×11
- Max pages: 550

### 1C. Paperback Cover Dimensions (6×9" Example)

```
200 pages, white paper, B&W:
  Spine = 200 × 0.002252 = 0.4504"
  Width = 0.125 + 6 + 0.4504 + 6 + 0.125 = 12.7004"
  Height = 0.125 + 9 + 0.125 = 9.25"
  At 300 DPI: 3810 × 2775 px
```

### 1D. Hardcover Cover Dimensions (6×9" Example)

```
200 pages:
  Spine = (200 × 0.0025) + 0.189 = 0.689"
  Total Width = (2 × 6) + 0.689 + 1.812 = 14.501"
  Total Height = 9 + 0.236 = 9.236"
  At 300 DPI: 4350 × 2771 px
```

### 1E. Content Rules (All Cover Types)

- **Front must have**: Title + Author name. No pricing, no promotional text.
- **White/light backgrounds**: Add 3–4px medium gray border to prevent disappearing against Amazon's white page.
- **Bleed**: 0.125" (3.2mm) on all sides. Background images must extend to the bleed edge.
- **Safe zone**: All critical text ≥0.25" inside trim edge.
- **Spine text**: Only on books **80+ pages**. Allow 0.0625" variance on fold lines.
- **Prohibited**: Barcode (KDP adds it), pricing, awards/bestseller claims.
- **Submission format**: Print covers = PDF. eBook covers = JPEG. Never the reverse.
- **File preparation**: Flatten all layers. Embed all fonts. No crop marks, trim marks, or watermarks.
- **MIFECO design standard**: Large white bold title (DejaVuSans-Bold, 2px black drop-shadow), author smaller at bottom, highly relevant scene imagery, must pass thumbnail and grayscale tests.

---

## 2. PRINT INTERIOR SPECS (Paperback/Hardcover)

### 2A. Dimensions & Layout

| Requirement | Spec |
|---|---|
| **Standard trim size** | 6" × 9" (trade paperback) |
| **Bleed** | 0.125" all 4 sides. PDF manuscript required if bleed is used. |
| **No-bleed page size** | Exact trim size (e.g. 6" × 9") |
| **Bleed page size** | 6.125" × 9.25" (for 6×9 trim) |

### 2B. Page Count

| Requirement | Spec |
|---|---|
| **Minimum** | 24 pages (KDP rejects fewer) |
| **Maximum (B&W white)** | 828 pages |
| **Maximum (B&W cream)** | 776 pages |
| **Maximum (standard color)** | 600 pages |
| **Maximum (premium color)** | 828 pages |
| **Maximum (hardcover)** | 550 pages |
| **Rounding** | Must be **even** (KDP rounds up if odd — add blank page) |

### 2C. Margins

| Page Count | Inside (Gutter) | Outside (No Bleed) | Outside (With Bleed) |
|---|---|---|---|
| 24–150 | 0.375" (9.6mm) | ≥0.25" (6.4mm) | ≥0.375" (9.6mm) |
| 151–300 | 0.5" (12.7mm) | ≥0.25" (6.4mm) | ≥0.375" (9.6mm) |
| 301–500 | 0.625" (15.9mm) | ≥0.25" (6.4mm) | ≥0.375" (9.6mm) |
| 501–700 | 0.75" (19.1mm) | ≥0.25" (6.4mm) | ≥0.375" (9.6mm) |
| 701–828 | 0.875" (22.3mm) | ≥0.25" (6.4mm) | ≥0.375" (9.6mm) |

### 2D. File Requirements

| Requirement | Spec |
|---|---|
| **Format** | **PDF** (required if bleed; recommended for all print) |
| **Image DPI** | **300 min** (600 max to keep file under 650MB) |
| **Fonts** | All **embedded** in PDF |
| **Color** | CMYK preferred for print; RGB accepted |
| **Max file size** | 650 MB |
| **Page numbering** | Sequential Arabic numerals (body), Roman numerals (front matter optional). Even on left pages, odd on right. |

---

## 3. EBOOK INTERIOR SPECS (Kindle)

### 3A. Format

| Requirement | Spec |
|---|---|
| **Preferred format** | **EPUB 3** |
| **Also accepted** | EPUB 2, DOCX, HTML, RTF, TXT |
| **NOT accepted** | MOBI (no longer accepted for new uploads as of March 2025) |
| **Max file size** | 650 MB (including all embedded images) |

### 3B. Table of Contents

| Requirement | Spec |
|---|---|
| **Required for** | Books **>20 pages** |
| **Two types needed** | (1) HTML TOC visible + clickable in front matter, (2) nav.xhtml logical navigation for Kindle |
| **HTML TOC rules** | Linked/clickable entries resolving to chapter anchors. **No page numbers** (reflowable). In front matter. |
| **nav.xhtml rules** | `<nav epub:type="toc">` with `<ol>`. Max **2 levels** of nesting. Listed in reading order. |
| **Heading consistency** | All chapter titles must use the SAME heading level (`h1` or `h2`). Inconsistent levels break auto-TOC. |

### 3C. Text & Styling

| Rule | Detail |
|---|---|
| **Body text defaults** | No forced font-family, font-size, or color on `<p>` — let Enhanced Typesetting apply reader preferences |
| **Font color** | Leave unspecified (forced black breaks dark mode rendering) |
| **Chapter starts** | Each chapter in own XHTML file OR separated by `page-break-before: always` CSS |
| **First-line indent** | Use `text-indent: 1.5em` on `<p>` — not `<br>` or spaces |
| **Line height** | Avoid forcing; max `line-height: 1.5` if needed |

### 3D. Validation

| Tool | Requirement |
|---|---|
| **epubcheck** | **0 errors** |
| **Kindle Previewer 3** | **0 blocking errors** — fix all warnings to ensure store availability |
| **Cover** | Embedded inside EPUB with `properties="cover-image"` in manifest; displays in Kindle Previewer |
| **Duplicate IDs** | All `id=""` must be unique across ALL XHTML files |
| **File paths** | Forward slashes `/` only. No special characters (!@#$%) in filenames |
| **Max file size** | Under 650 MB |

### 3E. Image Guidelines

| Rule | Detail |
|---|---|
| Resolution | 150–300 DPI recommended |
| Max width | `max-width: 100%; height: auto` in CSS |
| Formats | JPEG (photos), PNG (graphics/diagrams) |
| Alt text | Required for all informative images |
| Gaiji | PNG 8-bit or JPEG, min 128×128 px recommended |
| Separation | Use `<br/>` or separate chapters to prevent images merging |

---

## 4. FRONT MATTER ORDER (Print & eBook)

1. **Title page** — Book title, subtitle, author name
2. **Copyright page** — Copyright notice, rights reserved, AI disclosure (if applicable), ISBN (print), disclaimer (non-fiction)
3. **Table of Contents** — Clickable links (eBook) or manual page numbers (print)
4. **Dedication/Preface** (optional)
5. **Chapter 1** — Begin body matter
6. **Back matter** — About the Author, About the Series (optional), transition page (series books)

---

## 5. PRE-UPLOAD CHECKLISTS

### 5A. Print Checklist
- [ ] PDF page size matches exact trim (or trim + bleed)
- [ ] All margins meet KDP minimums per page count
- [ ] All images ≥300 DPI
- [ ] All fonts embedded in PDF
- [ ] Page count is even and within 24–828 range
- [ ] No crop marks, trim marks, or watermarks
- [ ] File size <650 MB
- [ ] **No front/back cover in manuscript file** — KDP Cover Creator handles covers

### 5B. eBook Checklist
- [ ] EPUB validates with 0 errors (epubcheck)
- [ ] Kindle Previewer reports 0 blocking errors
- [ ] Cover embedded in OPF with `properties="cover-image"`
- [ ] Nav TOC lists all chapters (≤2 levels)
- [ ] HTML TOC links are clickable and resolve
- [ ] Body text has no forced font-size/color on `<p>`
- [ ] No duplicate IDs across XHTML files
- [ ] All images have alt text
- [ ] Metadata (title, author, language) matches KDP listing
- [ ] **No front/back cover in EPUB** — separate JPEG uploaded for marketing cover

---

## 6. PAGE NUMBERING (Print PDF)

Use CSS `@page` for print PDF page numbers:

```css
@page {
  size: 6in 9in;
  margin: 0.75in;
  @bottom-center {
    content: counter(page);
    font-size: 9pt;
    color: #666;
  }
}
@page:first {
  @bottom-center { content: none; }
}
```

For print TOC: render once with placeholder numbers → use `pdftotext` to extract actual pages → hardcode in HTML → re-render.
