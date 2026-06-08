# Marketing Infographic Generation v2

## When to Use
- Creating social media marketing images for a book or book series
- User asks for "sales infographic", "marketing image", "promo graphic"
- When deploying a book launch campaign (always in Week 1)

## Platform Targeting

### Business Books (AI That Works, Crisis Ready, Owner's Manual)
- **Primary**: LinkedIn (professional audience)
- **Design**: Clean, professional, corporate. Dark navy + gold.
- **Tone**: Authoritative, practical, no-nonsense

### Fiction Series (Lightship, Lunar Foundation, No Blue Sky)
- **Primary**: Facebook, X, Bluesky, Instagram, TikTok
- **Design**: Bold, cinematic, genre-appropriate
- **Tone**: Epic, exciting, emotionally engaging

### Memoir (Tomorrow Remembered)
- **Primary**: Facebook, X, Bluesky, Instagram, TikTok
- **Design**: Warm-to-cool gradient, personal, reflective
- **Tone**: Personal, honest, inspiring

## Output Format

**Single portrait format per series**: 1080x1350px JPEG, saved to series directory as `series_infographic.jpg`.

## Layout Structure (CRITICAL — matches AI That Works example)

Two-column layout:
- **LEFT COLUMN (~40%, 410px)**: Dark charcoal background #1C1C1C
  - Top: Series name header (gold, small)
  - Headline text (big, bold: gold first line + white continuation)
  - Subhead text (italic, light gray)
  - Book cover (prominent, ~260x330px max, centered)
  - "WHY YOU NEED THIS BOOK" section (5 checkmark items)
  - About the Author (at bottom of column)

- **RIGHT COLUMN (~60%, 670px)**: Dark navy background #1A3B5F
  - "WHAT'S INSIDE" gold header bar
  - "THE SERIES FRAMEWORK" subtitle
  - 4 framework icons in HORIZONTAL ROW with arrows between
  - Step names and descriptions below icons
  - "WHAT YOU'LL LEARN" with 4 checkmark bullet points
  - "THIS BOOK IS FOR YOU IF:" with 4 checkmark bullet points
  - Gold quote banner
  - "WHAT READERS ARE SAYING" with 2 star-rated reviews
  - About the Author section

- **BOTTOM QR BAND** (full width, ~210px tall)
  - White background, 3px gold top border
  - "GET YOUR COPY TODAY" CTA
  - Two QR codes (mifeco + amazo) in bordered white cards
  - Copyright text

**White separator line** (2px) between columns.

## Color Specifications

| Series | Left BG | Right BG | Accent | Framework Colors |
|--------|---------|----------|--------|-----------------|
| Business | (28,28,28) | (26,59,95) | (251,183,9) | #67D4EE, #5DE187, #9A69D9, #F39C2D |
| Lightships | (10,10,26) | (13,27,62) | (251,183,9) | #67D4EE, #F39C2D, #9A69D9, #5DE187 |
| Lunar Found. | (10,10,24) | (10,20,48) | (251,183,9) | #67D4EE, #5DE187, #F39C2D, #9A69D9 |
| No Blue Sky | (26,8,0) | (46,18,0) | (255,100,40) | #FF6428, #67D4EE, #FBB709, #5DE187 |
| Cindy Lou | (26,26,48) | (37,26,64) | (212,165,84) | #67D4EE, #5DE187, #FBB709 |
| Tomorrow Rem. | (28,24,37) | (42,32,64) | (200,160,80) | #C8A050, #67D4EE, #5DE187 |

## Typography (MINIMUM SIZES — phone readability)

- Headline: 26pt gold (first line), 20pt white (continuation)
- Subhead: 11pt italic, light gray
- Section headers: 12pt bold, accent color  
- Body text: 10pt regular, white/light gray on dark bg
- Checkmarks: 11pt bold, accent color
- Framework step names: 10pt bold, in respective colors
- Framework descriptions: 8pt regular, dark text
- Reviews: 9pt italic, light gray
- Author roles: 8pt regular, muted color
- QR labels: 9pt bold, dark on white
- Copyright: 7pt regular, gray

**CRITICAL**: Body text must be >=10pt. Never use 8pt for body text. 8pt is acceptable only for framework descriptions and author roles.

## QR Code Specs
- Use ACTUAL QR images from book directories (not placeholders)
- QR size: 110x110px, in white cards (140x140px) with colored borders
- Labels: "books.mifeco.com" and "amazon.com/s?k=bob+j+mills"
- Band: white bg, 3px gold top border, ~210px tall

## Technical Approach: Pure PIL Only

**Why NOT WeasyPrint/CSS?**
- CSS Grid does NOT render in WeasyPrint (boxes stack vertically instead)
- `box-shadow`, `object-fit`, `linear-gradient`, flexbox `gap` are NOT supported
- Manual PIL positioning gives pixel-perfect control

**Why NOT Gemini 2.5 Flash Image for full infographic?**
- Gemini generates beautiful backgrounds but GARBLES all body text
- Even as background-only, positions vary each time making consistent overlays impossible
- **Pure PIL is the only reliable approach**

## Implementation Reference

See `scripts/generate_series_infographics_v9.py` for the working reference implementation.

## Content Keep-Short Guidelines

1350px height is TIGHT. Keep content SHORT:
- "Why" section: 5 items max, each <=30 chars
- "What You'll Learn": 4 items max, each <=50 chars
- "For You If": 4 items max, each <=40 chars
- Reviews: 2 reviews, each <=3 short lines
- Books list: numbered lines with short titles

**If text doesn't fit**, reduce item count or shorten text. Never reduce body font below 10pt.

## Pitfalls (MUST READ — learned from 9 iterations)

1. **CSS Grid + WeasyPrint = silent failure** — boxes stack vertically instead of 2x2
2. **Gemini Image = garbled text** — beautiful backgrounds, useless text
3. **Content overflow = #1 problem** — 1350px is tight, every section must be compact
4. **Framework icons**: Horizontal row with arrows (NOT 2x2 grid) matches target
5. **Book cover**: Max 260x330px. Larger covers push everything off-screen
6. **Right column cuts off first** — reviews and author section disappear if too tall
7. **Min font 10pt** for body text. Review quotes can be 9pt.
8. **Use actual QR images** from book directories, size 110x110 in 140x140 cards
9. **Checkmarks**: Use "v" char (not "✓") at bold weight
10. **Accent color**: Use RGB tuples `(251, 183, 9)` for PIL, not hex strings
11. **No box-shadow in PIL** — use borders/outlines instead
12. **WeasyPrint `object-fit: contain`** not supported — resize manually in PIL

## File Locations

QR codes and covers in each book's directory on `/mnt/usb_4tb/books/`:
- Business: `AI_That_Works/` (qr_mifeco.png, qr_amazon.png, MIFECO_AI_Playbook_Cover.png)
- Lightships: `Age_of_Lightships_Series/Book_1_Sunward_Exodus/` (cover_final.png)
- Lunar: `Lunar_Foundation_Series/Book_1_Moon_Rock/` (LF_1_Moon_Rock_Cover.png)
- NBS: `No_Blue_Sky_Series/Book_I_Built_from_Dust/` (NBS_1_Built_from_Dust_Cover.png)
- Cindy Lou: `Cindy_Lou_Legal_Capers/cindy-lou-series/covers/` (retainer-to-trouble_cover.png)
- Tomorrow: `Tomorrow_Remembered/` (Tomorrow_Remembered_Cover.jpg)

## Quality Validation

After generating, validate with Gemini:
```python
content = [
    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_b64}"}},
    {"type": "text", "text": "Rate this book marketing infographic 1-10. All text readable? Framework icons visible? Professional quality?"}
]
```

Target: 9.5/10. Iterate until reached — each iteration closes specific gaps.
