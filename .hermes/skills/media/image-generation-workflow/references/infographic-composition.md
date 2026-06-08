# Marketing Infographic Composition — Standards (Updated 2026-06-02)

## Method: PIL Composite (Preferred) vs Gemini Background Art

### Preferred: Full PIL Composition
For production infographics, **use PIL directly** for the entire layout. This guarantees:
- Exact output dimensions (Gemini always returns 1024x1024 regardless of requested aspect ratio)
- Scannable QR codes (Gemini generates faux-QR decorative squares, not real encodable QR data)
- Pixel-perfect text placement with proper font loading
- Consistent brand colors with no gradient bleed

### When to Use Gemini
Use `google/gemini-2.5-flash-image` ONLY for:
- Background textures/patterns (abstract art, textures, non-text visual elements)
- When you need artistic style that PIL can't produce
- NOT for: text-heavy layouts, precise dimensions, or QR code inclusion

### Composite Workflow (Proven Pattern)
1. Generate QR codes with qrcode library, save as qr_mifeco.png, qr_amazon.png
2. Use PIL to build full infographic: gradient background, text layout, white QR band
3. qr_block() for each QR: white padding, NEAREST resize, URL label below
4. qr_pair() to paste both QRs centered in white band
5. Save to outputs/ directory, copy to KDP Marketing_and_Compliance/ dirs

### QR Code Handling - CRITICAL
- ALWAYS use Image.NEAREST for QR resize - NEVER LANCZOS or BILINEAR
- QR codes padded 10-12px white border on solid white band
- White band: solid fill=(255,255,255), no gradient bleed
- Gold separator line: rectangle 3px above band
- URL labels: Navy 18-22px bold, "books.mifeco.com" and "amazon.com/s?k=bob+j+mills"

### Font Sizes - NON-NEGOTIABLE (1080px wide base)
- Title: 56-72px bold
- Subtitle: 36-44px
- Book titles: 32-36px bold
- Description: 24-32px (never below 24px)
- Tagline: 28-30px italic
- URL labels: 18-22px bold
- Copyright: 13-16px

### Color Palette (Cindy Lou Legal Capers)
- Navy: (25, 25, 50), Gradient lighter: (42, 42, 72)
- Gold: (212, 165, 84)
- White: (255, 255, 255)
- Cream: (245, 235, 210)
- Light gray: (200, 202, 220)
- QR band: Pure white (255, 255, 255)

### Platform Ratios
| Format | Size | Band start | QR size |
|--------|------|-----------|---------|
| Portrait | 1080x1350 | 81-82% | 210-220px |
| Square | 1080x1080 | 72-75% | 160-180px |
| Landscape | 1200x628 | side-by-side | 160-170px |
| Story | 1080x1920 | 80-82% | 210-220px |

### Pitfalls
1. **Gemini aspect ratio**: Always returns 1024x1024 - resize with LANCZOS if using as texture
2. **Gemini QR codes**: NOT scannable - always composite real QR codes from qrcode library
3. **Gradient bleed**: Draw solid white rectangle AFTER all other drawing operations
4. **NEAREST for QR**: resize with NEAREST - any other resampling blurs QR modules
5. **execute_code sandbox**: Scripts run in sandbox - use absolute paths for all file I/O
6. **f-string quoting**: In sandbox scripts, avoid nested single quotes in f-strings, use temp vars
7. **Codex OAuth**: Codex CLI requires active OAuth - if 401, write scripts directly in PIL instead
