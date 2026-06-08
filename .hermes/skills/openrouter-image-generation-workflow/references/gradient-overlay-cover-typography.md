# Gradient-Overlay Cover Typography

Alternative to letterbox (black bars) for book covers where you want the artwork to show through behind the text. Uses gradient darkening at top/bottom + shadowed white text.

## When to Use

- The AI-generated image has good art across the full canvas (no need for letterbox bars)
- Bright elements near the top or bottom need subtle darkening for text legibility
- You want a professional "text-over-artwork" look rather than black bars
- Title should be ~80% of cover width, bold, centered

## Technique

### Step 1: Add gradient overlays

```python
from PIL import Image, ImageDraw, ImageEnhance, ImageFont

img = Image.open(raw_path).convert("RGBA")
w, h = img.size

overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
draw_overlay = ImageDraw.Draw(overlay)

# Top gradient for title zone (~30% of height, light veil)
grad_height_top = int(h * 0.30)
for y in range(grad_height_top):
    alpha = int(120 * (1 - y / grad_height_top))
    draw_overlay.rectangle([0, y, w, y+1], fill=(0, 0, 0, min(alpha, 90)))

# Bottom gradient for author zone (~15% of height, light veil)
grad_height_bot = int(h * 0.15)
for y in range(grad_height_bot):
    alpha = int(100 * (y / grad_height_bot))
    draw_overlay.rectangle([0, h - grad_height_bot + y, w, h - grad_height_bot + y + 1], 
                          fill=(0, 0, 0, min(alpha, 80)))

img = Image.alpha_composite(img, overlay).convert("RGB")
```

### Multi-Line (4+ lines) Non-Fiction Title Handling

For non-fiction books with long titles split across 4+ lines (e.g., "THE / OWNER'S / MANUAL FOR / AI AGENTS"), use the same iterative font-size search but note:

- **Shadow depth increases with title size**: For titles >90px, use a 4-layer shadow (4,3,2,1 offset) instead of 3-layer (3,2,1) — the larger text needs more shadow to stay legible over artwork gradients.
- **Subtitle placement**: Place the subtitle ~20px below the last stacked line, at ~22% of the title font size. Use a lighter color (220,220,220) and a 2-layer shadow.
- **80% width target**: The iterative search handles this automatically — the widest line fits within 80% of cover width regardless of how many lines the title has. No per-line manual sizing needed.

```python
# Stronger shadow for large non-fiction titles (4 layers)
shadow_depth = 4 if title_size > 90 else 3
for layer in range(shadow_depth, 0, -1):
    draw.text((x+layer, current_y+layer), word, font=title_font, fill=(0, 0, 0, 200))
draw.text((x, current_y), word, font=title_font, fill=(255, 255, 255))
```

### Step 2: Add shadowed typography (stacked title, 80%-width scaling)

```python
draw = ImageDraw.Draw(img)

# Title font sizing: iterative search for widest line within 80% of cover width
title_words = ["THE", "OXYGEN", "GAMBLE"]  # split into word array
for test_size in range(300, 40, -2):  # start high, step down until fits
    font = ImageFont.truetype(font_path, test_size)
    max_w = max(draw.textbbox((0,0), w, font=font)[2] - draw.textbbox((0,0), w, font=font)[0] for w in title_words)
    if max_w <= int(w * 0.80):
        title_font_size = test_size
        break

title_font = ImageFont.truetype(font_path, title_font_size)

# Calculate line dimensions for even centering
line_hs = []
line_ws = []
for word in title_words:
    bb = draw.textbbox((0, 0), word, font=title_font)
    line_ws.append(bb[2] - bb[0])
    line_hs.append(bb[3] - bb[1])

line_gap = int(title_font_size * 0.12)  # proportional gap between stacked words
total_stack_h = sum(line_hs) + line_gap * (len(title_words) - 1)

# Center stacked title vertically within top 35% of cover
title_zone_h = int(h * 0.35)
start_y = (title_zone_h - total_stack_h) // 2 + int(h * 0.02)

current_y = start_y
for i, word in enumerate(title_words):
    x = (w - line_ws[i]) // 2
    # 3-layer shadow for legibility over art
    for ox, oy in [(3, 3), (2, 2), (1, 1)]:
        draw.text((x+ox, current_y+oy), word, font=title_font, fill=(0, 0, 0, 180))
    draw.text((x, current_y), word, font=title_font, fill=(255, 255, 255, 255))
    current_y += line_hs[i] + line_gap
```

# Author name at bottom with dark bar (fixed 100px for series consistency)
author_text = "Bob J Mills"
author_font = ImageFont.truetype(font_path, 100)
ab = draw.textbbox((0, 0), author_text, font=author_font)
aw = ab[2] - ab[0]
ax = (w - aw) // 2
ay = h - int(h * 0.07)
bar_h = int(h * 0.09)
draw.rectangle([0, h - bar_h - 5, w, h], fill=(0, 0, 0, 160))
for ox, oy in [(2, 2), (1, 1)]:
    draw.text((ax+ox, ay+oy), author_text, font=author_font, fill=(0, 0, 0, 180))
draw.text((ax, ay), author_text, font=author_font, fill=(255, 255, 255, 255))
```

### Step 3: Subtitle (for non-fiction books)

When the user explicitly asks for a subtitle below the stacked title, add a smaller italic/lighter line:

```python
subtitle = "What Every Business Owner Needs to Know"
sub_font_size = int(title_size * 0.22)  # proportionally sized to title
sub_font = ImageFont.truetype(font_path, sub_font_size)
sb = draw.textbbox((0, 0), subtitle, font=sub_font)
sw = sb[2] - sb[0]
sx = (w - sw) // 2
sy = current_y + line_gap + 20  # below the last title line
for ox, oy in [(2, 2), (1, 1)]:
    draw.text((sx+ox, sy+oy), subtitle, font=sub_font, fill=(0, 0, 0, 180))
draw.text((sx, sy), subtitle, font=sub_font, fill=(220, 220, 220))
```

- NEVER add a subtitle unless the user explicitly requests one. Business books sometimes want them; fiction never does.
- Subtitle font size should be ~22% of title font size for proportional balance.
- Position ~20-30px below the last stacked line of the main title.

### Step 3: Series branding line

Add a small series + book number line at the very top:

```python
sub_font = ImageFont.truetype(font_path, 16)
series_text = "The Lunar Foundation  •  Book 2"
sb = draw.textbbox((0, 0), series_text, font=sub_font)
sub_x = (w - (sb[2] - sb[0])) // 2
sub_y = int(h * 0.01)
draw.text((sub_x+1, sub_y+1), series_text, font=sub_font, fill=(0,0,0,160))
draw.text((sub_x, sub_y), series_text, font=sub_font, fill=(200,200,200,255))
```

## Comparison with Letterbox Approach

| Factor | Gradient Overlay | Letterbox (Black Bars) |
|--------|-----------------|----------------------|
| Artwork visibility | Art shows through behind text | Art completely hidden under bars |
| Text legibility | Good but varies with art brightness | Excellent (pure black behind white text) |
| Professional look | Modern, integrated | Clean, traditional cover |
| Best for | Dark/moody artwork with good contrast | Bright/busy artwork |
| Shadow needed | 2px shadow essential | 1px shadow sufficient |

## Critical Rules for All Covers

1. **No subtitle unless explicitly requested** — Never add a secondary text line under the main title. "Inspired by" does not mean copying the subtitle or tagline from another book.

2. **Verify the author name** — Every book cover must use THIS book's author, not the author from any reference or inspiration source. For Bob J Mills's books: always "Bob J Mills". Never carry over a name from a source of inspiration.

3. **"Completely original" in artwork prompts** — When the artwork is inspired by a best-selling book, add this exact constraint to the prompt: `This must be completely original — do not reference or copy elements from any existing book covers.`

4. **Make artwork brighter** — After generating, apply PIL brightness/contrast enhancement if the art is too dark:
   ```python
   from PIL import ImageEnhance
   img = ImageEnhance.Brightness(img).enhance(1.20)  # +20% brightness
   img = ImageEnhance.Contrast(img).enhance(1.1)     # +10% contrast
   ```

5. **Author font size consistency** — Within a series, use the same author font size across all books. For Bob's 1200×1800 covers, 100px for "Bob J Mills" produces a clean 528px-wide line (44% of cover width).

## Per-Book Tweaking

Store per-book parameters in a dict for easy iteration:

```python
books = {
    "Moon_Rock": {
        "title_lines": ["MOON", "ROCK"],
        "title_size": 72,
        "top_grad_pct": 0.35,
        "bot_grad_pct": 0.15,
        "need_author_box": True
    }
}
```

This pattern is library-agnostic (works with any bold sans-serif font) and produces professional-grade covers comparable to trad-published sci-fi.