# Book Cover Design Recipes

Design patterns that work for specific book types, accumulated from iterative feedback.

## Memoir / Life-Story Covers: Radial Quadrant Layout

This user prefers a **radial quadrant** layout for memoir covers spanning decades — four scenes of the subject's life radiating from center, blending into each other.

**Layout (for this user's books):**
```
┌──────────────┬──────────────┐
│  TL: 1950s   │  TR: 1980s   │
│  Michigan    │  RF-4C       │
│  lake cabin  │  Phantom jet │
├──────────────┼──────────────┤
│  BL: 2010s   │  BR: 2070s   │
│  data center │  Mars colony │
│  server racks│  under dome  │
└──────────────┴──────────────┘
```
- Four scenes arranged clockwise from past (top-left) to far future (bottom-right)
- Quadrants blend/fade at the center where they meet
- Dark, cinematic quality with high contrast

**Typography Rules (for this user — learned through 4 iterations of feedback):**
- **Title:** Very large (72-90pt), bold, stacked vertically, white with thick shadow
- **Author:** Large (44-52pt), bold, white with shadow
- **KEY PREFERENCE:** Text should OVERLAP the image — NOT stay confined to safe zones. The user explicitly rejected keeping text within black letterbox zones.
- Use semi-transparent dark backdrop bar behind text (alpha 180-185) spanning ~88% of cover width, centered. This ensures readability over any image content.
- Shadow technique: use concentric circular shadow (`sx*sx + sy*sy <= radius*radius`) for smooth, non-blocky outlines. Radius 5 for title, 4 for author.
- When the user says "bigger" — go up significantly (30-50% in font size, not 10%). Going from 64→90pt was accepted. Going from 36→52pt was accepted.

**Canvas Extensions for Black Space:**
- Add **22%** extra height as black at the top for title zone
- Add **15%** extra height as black at the bottom for author zone
- Use gradient overlay (fading from alpha 120→0) where black space meets image to soften the transition
- Use gradient from the IMAGE side too (alpha 0→80 over ~60px) so the dark backdrop bar blends smoothly
- Final aspect ratio: 1024×1536 (2:3) upscaled to 1600×2560 for KDP Kindle

**Generation Workflow (tested on this user's books):**
1. Craft prompt with explicit quadrant layout — describe each quadrant scene in detail (era, lighting, mood, palette)
2. Always specify "no text, no watermarks, no logos, no letters"
3. Request landscape 1536×1024 if you want orientation hints, but expect Gemini Flash Image to return 1024×1024 regardless
4. Scale raw image to fill portrait height, center-crop width for full-bleed 2:3 (this gives the most image coverage)
5. Extend canvas with black bars: 22% top, 15% bottom via `Image.new("RGB", (base_w, new_h), (0,0,0))` and paste scaled art at `(0, extra_top)`
6. Apply gradient overlay at the interface between black space and art
7. Add typography: dark backdrop bar FIRST (alpha ~185), then text with thick shadow, then bright white text
8. Downscale to 1024×1536, then upscale to 1600×2560 for KDP Kindle cover

**Prompt Structure Template:**
```
Book cover design with four radial quadrants blending at center, creating a seamless timeline:

TOP-LEFT: [earliest era — scene, lighting, colors]
TOP-RIGHT: [second era — scene, lighting, colors]
BOTTOM-LEFT: [third era — scene, lighting, colors]
BOTTOM-RIGHT: [latest/future era — scene, lighting, colors]

The four quadrants blend into each other at the center with subtle gradient fades.
CRITICAL: [orientation/size]. [colors/mood]. No text, no watermarks.
```

**Iteration pattern when user wants changes:**
- Don't regenerate the art if the user only wants bigger text or more black space — just adjust the Python parameters (title_font_size, extra_top, extra_bot, backdrop alpha) and re-run the typography script
- The raw art image is the expensive/uncertain part; the typography overlay is cheap and deterministic
- When the user says "bigger" on text, bump by at least 30-50% — small increments (10-15%) will produce multiple rejection loops

## Why This Works for Memoirs

- The quadrant layout communicates "a life in four eras" at a glance
- Radial blend at center suggests memory, connection across time
- Dark tones with bright title create a premium, literary feel
- Large overlapping text signals confidence — the book knows what it is

---

## Sci-Fi Series Cover Pattern: Gradient-Overlay + Stacked Title + Author Bar

Pattern emerged from regenerating two complete sci-fi series (8 books) for Bob J Mills. This produces covers in the "best-selling sci-fi" aesthetic — think The Expanse / Project Hail Mary / The Martian style — with high-contrast titles, visible artwork, and professional polish.

### Typography Rules (proven by iteration)

| Element | Rule |
|---------|------|
| **Title** | Stacked vertically (one word per line), ~80% cover width, bold white, 3px shadow |
| **Author** | Fixed 100px font (not scaled), "Bob J Mills", bold white, in dark bar |
| **Subtitle** | NEVER include unless explicitly requested — "inspired by" does not mean copying subtitle/tagline |
| **Series line** | 18px, top of cover: "SERIES NAME  •  BOOK N" in light gray |
| **Author bar** | Semi-transparent black at bottom 9% of cover, alpha 160 |

### Full Workflow (tested on 8 covers)

**Step 1 — Craft the artwork prompt**

Each prompt must include:
- Scene description (specific to that book's theme)
- Colors palette
- "Leave the top 40% of the image as clean, empty negative space for title text"
- "Leave the bottom 15% clean for author name"
- `CRITICAL: No text, no watermarks, no letters, no logos anywhere.`
- `Inspired by best-selling sci-fi cover aesthetics but completely original — no copied elements.` (mandatory — prevents borrowing visual elements from existing covers)

Prompt structure template:
```
Book cover artwork for a sci-fi novel. [specific scene description].
[Cinematic/dramatic atmosphere note].
Colors: [color palette].
Leave the top 40% of the image as clean, empty negative space ...
Leave the bottom 15% clean for author name ...
CRITICAL: No text, no watermarks, no letters, no logos anywhere.
Inspired by best-selling sci-fi cover aesthetics but completely original — no copied elements.
```

**Step 2 — Generate artwork via Gemini Flash Image**

Use Google Gemini API directly (not OpenRouter). Parser must handle Gemini's response format where a `text` part may appear BEFORE the `inlineData` part:

```python
candidate = data.get('candidates', [{}])[0]
parts = candidate.get('content', {}).get('parts', [])
for part in parts:
    if isinstance(part, dict) and 'inlineData' in part:
        img_bytes = base64.b64decode(part['inlineData']['data'])
```

**Step 3 — Scale and crop to 2:3 portrait (1200×1800)**

Gemini typically returns 1024×1024 squares. Transform to portrait:
```python
target_w, target_h = 1200, 1800
scale = target_h / h  # fill height
img = img.resize((int(w*scale), target_h), Image.LANCZOS)
# If wider than target, center-crop; if narrower, add black sidebars
if img.size[0] > target_w:
    xo = (img.size[0] - target_w) // 2
    img = img.crop((xo, 0, xo+target_w, target_h))
else:
    canvas = Image.new("RGBA", (target_w, target_h), (0,0,0,255))
    canvas.paste(img, ((target_w-img.size[0])//2, 0))
    img = canvas
```

**Step 4 — Brighten the artwork**

```python
from PIL import ImageEnhance
img = ImageEnhance.Brightness(img).enhance(1.20)  # +20%
img = ImageEnhance.Contrast(img).enhance(1.1)     # +10%
```

**Step 5 — Apply gradient overlay**

Light veil only — artwork should show through clearly:
```python
overlay = Image.new("RGBA", (target_w, target_h), (0,0,0,0))
dov = ImageDraw.Draw(overlay)
# Top: 30% of height, alpha 120→0 (capped at 90)
for y in range(int(target_h*0.30)):
    a = int(120 * (1 - y/(target_h*0.30)))
    dov.rectangle([0, y, target_w, y+1], fill=(0,0,0,min(a,90)))
# Bottom: 15% of height, alpha 0→100 (capped at 80)
for y in range(int(target_h*0.15)):
    a = int(100 * (y/(target_h*0.15)))
    dov.rectangle([0, target_h-int(target_h*0.15)+y, target_w, target_h-int(target_h*0.15)+y+1],
                  fill=(0,0,0,min(a,80)))
img = Image.alpha_composite(img, overlay).convert("RGB")
```

**Step 6 — Apply typography**

See `gradient-overlay-cover-typography.md` for the complete code. Key parameters for 1200×1800 covers:
- Title font size: iterative search from 300px down until widest word ≤ 960px (= 80% of 1200)
- Line gap between stacked words: 12% of font size
- Title zone: top 35% of cover, centered vertically within that zone
- Author: 100px, centered in dark bar at bottom 9%
- Series: 18px, top 0.5% of cover

**Step 7 — Batch consistency**

When doing a series, define per-book parameters in a dict:
```python
books = {
    1: {"title_words": ["BUILT", "FROM", "DUST"], "series_line": "NO BLUE SKY  •  BOOK 1"},
    2: {"title_words": ["THE", "OXYGEN", "GAMBLE"], "series_line": "NO BLUE SKY  •  BOOK 2"},
}
```
Use the SAME font, SAME author size, SAME gradient values, SAME overlay approach across all books in the series.

### Pitfalls

1. **Never bake text into the AI artwork prompt** — AI always produces garbled/misspelled text. Apply typography in PIL overlay.
2. **"Inspired by" ≠ "copy elements from"** — When using reference books for aesthetic inspiration, explicitly prohibit copying visual elements (subject, composition, colors). Add `This must be completely original — do not reference or copy elements from any existing book covers.` to every prompt.
3. **Author name from the reference book** — It's easy to accidentally write the wrong author on the cover. The "inspired by The Martian by Andy Weir" mental association can cause "Andy Weir" to end up on the cover. Always verify: **this book's author is Bob J Mills**.
4. **Subtitle bleed** — Reference books often have subtitles or taglines. The prompt inspiration can leak a secondary text line under the title. Always check: is there an extra line of text under the main title? If so, remove it.
5. **Scale black sidebars correctly** — When extending square to portrait, if the image is narrower than target width, add black sidebars but ALSO resize the background first. Don't paste a small image into a large black canvas without scaling.
6. **Batching rate limits** — Each Gemini generation takes 30-60 seconds. Add `time.sleep(3)` between API calls. Run batch generation in background with `notify_on_complete=True`.
7. **Gemini response parsing** — Gemini may return a text `part` BEFORE the `inlineData` part. The parser must iterate ALL parts and find `inlineData`, not just check the first element.