---
name: book-cover-design
description: "Design professional book covers and chapter illustrations. ALL covers MUST use image generation LLM (Gemini Flash Image, Black Forest Labs Flux) — NOT Python/matplotlib. Business books use 'AI That Works for Small Business' cover style (dark background, white bold title, clean professional). Sci-fi books use 'Moon Rock' (Lunar Foundation) cover style (space-themed, dramatic, planetary). Author photo must be placed in every book directory."
category: publishing
tags: [covers, typography, gemini, pil, design]
---

## 🔍 MemPalace Query (MANDATORY FIRST STEP)
Before proceeding, query MemPalace for existing context:
```python
import sys, os; sys.path.insert(0, os.path.expanduser('~/.hermes/mempalace'))
import embed; embed.init_embedding(os.path.expanduser('~/.hermes/mempalace'))
results = embed.search_embeddings("book cover design typography genre cover art Gemini Flux", k=5)
```
This retrieves previous decisions, domain-specific context, and lessons learned from the vector memory store.

# Book Cover Design

A systematic approach for designing professional-grade book covers that are competitive in their genre, from initial market research through final typography overlay.

## When to Use This Skill

- A new book needs a cover for delivery or KDP submission
- An existing cover needs typography fixes (overlapping text, wrong font size, bad contrast)
- A series needs visually consistent covers
- The user asks for cover artwork generation
- The user complained about cover typography issues in a previous session

## Workflow Steps

### Step 1: Research the Genre First

Before writing a single prompt, research the subgenre's best-selling covers. Different subgenres have different visual languages:

| Subgenre | Color Palette | Typography | Imagery |
|----------|--------------|------------|---------|
| Hard Sci-Fi | Deep space blues, blacks, whites, cold steel | Clean sans-serif (Eurostile, Orbitron, Exo 2) | Single object, lots of negative space, technical/clinical |
| Space Opera | Warm oranges, deep blues, gold, vibrant | Bold serif or metallic fonts, epic scale | Starships, sprawling nebulae, dramatic vistas |
| Survival / Thriller | Cold whites, deep blacks, emergency red accents | Bold, high-contrast sans-serif, minimal | Cracked visors, damaged equipment, extreme close-ups |
| Mystery / Conspiracy | Sterile white, deep shadows, bioluminescent accent colors | Clinical clean fonts, sharp | Corridors, vials, hazmat suits, hidden figures |
| Cyberpunk | Electric blues, hot pinks, deep purples, black | Glitched/digital sans-serif, neon effects | Neon cityscapes, lone figures, rain |
| Business / Tech / Non-fiction | Dark navy (#0a0a1e), charcoal, clean whites, single accent (cyan/amber) | Bold sans-serif, high contrast white text, 4-layer shadow, title scaled to exactly 80% width, subtitle below stack at ~22% of title size | Typography-only with 4-line stacked title — no people, no code screenshots. Abstract neural/pipeline/constellation artwork behind gradient overlay. | Minimalist, professional, system-designer feel. Use 4-layer shadow for depth. See "Font Sizing for 80% Width (including multi-line stacked titles)" below for the iterative sizing recipe.

**Research method:** Search for "best selling [subgenre] book covers [current year]" and analyze:
- Dominant color
- Typography style (serif vs sans-serif, bold vs light)
- Composition (centered hero image vs. spread vs. symbolic)
- Text placement and size
- Common clichés to avoid

### Step 1a: Replicating an Existing Cover's Design Style

When the user asks for a cover "like" or "in the style of" an existing cover (one of their own covers or a reference image), systematically analyze the reference before recreating.

**Find reference covers:**
```bash
ls /home/bob/books/publishing_output/covers/
```
The covers directory holds all completed cover PNGs. Use the filename to identify which cover the user means.

**Pixel analysis with PIL + numpy:**
Extract design parameters programmatically from the reference image — this is more reliable than eyeballing or guessing:

```python
from PIL import Image
import numpy as np
from collections import Counter

img = Image.open('/path/to/reference_cover.png')
arr = np.array(img)
print(f'Size: {img.size}, Mode: {img.mode}')

# 1. Extract background color (most common pixel)
bg_color = tuple(Counter([tuple(p) for p in arr.reshape(-1, 3)]).most_common(1)[0][0])
print(f'Background: RGB{bg_color}')

# 2. Find content bounding box (non-background pixels)
mask = np.any(np.abs(arr.astype(int) - np.array(bg_color)) > 15, axis=2)
rows = np.any(mask, axis=1)
cols = np.any(mask, axis=0)
if rows.any():
    rmin, rmax = np.where(rows)[0][[0, -1]]
    cmin, cmax = np.where(cols)[0][[0, -1]]
    print(f'Text/graphics zone: y={rmin}-{rmax} (top {100*rmin/img.height:.0f}% → bottom {100*(img.height-rmax)/img.height:.0f}%)')
    print(f'Horizontal center: x={cmin}-{cmax} ({100*cmin/img.width:.0f}% to {100*cmax/img.width:.0f}% from left)')

# 3. Locate white text regions
white_mask = np.all(arr > 200, axis=2)
white_rows = np.any(white_mask, axis=1)
if white_rows.any():
    wrmin, wrmax = np.where(white_rows)[0][[0, -1]]
    print(f'White text band: y={wrmin}-{wrmax} ({100*wrmin/img.height:.0f}%-{100*wrmax/img.height:.0f}% from top)')

# 4. Get accent/colorful regions
accent_mask = np.any(arr[:,:,0].astype(int) - arr[:,:,1].astype(int) > 30, axis=0)  # red-dominant
# (adjust channel logic per palette)
```

**What to extract from the analysis:**
- **Background color** — reproduce exactly (e.g., RGB(10,10,30) dark navy)
- **Text placement** — is the title in the upper 25%? Centered? What gap from top?
- **Content width** — is text centered with generous margins (~25% on each side) or full-bleed?
- **Color palette** — only white/gray text? Any accent color? Gradient overlays?
- **Art vs typography ratio** — is the cover purely typography, or is there artwork?
- **Author placement** — bottom bar? Below title? What size relative to title?

**Design parameters to carry forward:**
- Background → use same RGB for new cover
- Typography position → same y-range percentage for title
- Text centering → same horizontal margin ratio
- Color palette → same white/gray hierarchy, accent color if present
- Font choice → same style (sans-serif bold for business, serif for literary, etc.)

**Then recreate with new title + different art** using the extracted parameters in Steps 2-4 below.

### Step 2: Design the Image Prompt

Based on the research, craft a prompt for AI image generation (Gemini Flash Image or Flux). Essential rules for book cover prompts:

**Reference file:** `references/prompt-templates.md` has reusable prompt templates for common sci-fi subgenres and aspect ratio guidance.

**Must include:**
- "BOOK COVER" or "book cover art" at the start
- The specific scene from the book's story
- Colors from the genre-appropriate palette
- "TOP 40% MUST BE COMPLETELY EMPTY — just [sky/void/ceiling] with no details"
- "3:4 portrait aspect ratio"
- Style descriptors: "photorealistic", "cinematic lighting", "high detail"

**Example hard sci-fi prompt:**
```
SCIENCE FICTION BOOK COVER. Lunar surface horizon with Earth rising huge and brilliant against the black sky. Construction equipment silhouetted against the glowing Earth. FIRST PERMANENT MOON BASE. TOP 40% MUST BE COMPLETELY EMPTY — just black starry space with Earth below the 40% line. High contrast: dark lunar foreground, brilliant blue-white Earth. Deep blacks, lunar grays, Earth blue. 3:4 portrait.
```

**Example survival thriller prompt:**
```
SCIENCE FICTION SURVIVAL BOOK COVER. Extreme close-up of a cracked astronaut helmet visor. Through the crack we see a desperate human eye and reflection of a crashed lunar lander. HARSH UNFILTERED SUNLIGHT. Deep sharp shadows. Gritty, textured. Cold whites, deep blacks, emergency red accents. TOP 40% MUST BE EMPTY — just dark sky. 3:4 portrait.
```

### Step 3: Generate Base Image Using Google Gemini

This environment uses the Google AI Studio API key directly (not OpenRouter) for Gemini Flash Image generation. The key lives in `~/.hermes/.env` as `GOOGLE_AI_STUDIO_KEY` and must be extracted via bash subshell — it is NOT a regular environment variable.

**Working API call pattern:**

```python
import requests, json, base64
from io import BytesIO
from PIL import Image

# Get the key from .env — critical: must use bash subshell
import subprocess
result = subprocess.run(["bash", "-c", "source ~/.hermes/.env && echo $GOOGLE_AI_STUDIO_KEY"],
                       capture_output=True, text=True)
api_key = result.stdout.strip()

url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image:generateContent?key={api_key}"

payload = {
    "contents": [{"parts": [{"text": prompt}]}],
    "generationConfig": {"temperature": 1.0}
}

response = requests.post(url, json=payload, timeout=90)

if response.status_code == 200:
    parts = response.json()["candidates"][0]["content"]["parts"]
    for part in parts:
        if "inlineData" in part:
            img_data = base64.b64decode(part["inlineData"]["data"])
            img = Image.open(BytesIO(img_data))
```

**Important:** 
- The `google-generativeai` SDK does NOT work in this environment against OpenRouter. Always use raw `requests.post()` to the Google endpoint directly.
- Timeout should be 90 seconds minimum — Gemini Flash Image can take 30-60s to generate.
- The response returns base64-encoded inline data, not a URL.
- If HTTP 403, the API key may not be loaded correctly — verify the bash subshell approach works.
- **OpenRouter alternative**: You can also use `google/gemini-2.5-flash-image` via OpenRouter (with `OPENROUTER_API_KEY`). This is often simpler than the direct Google API. Use the same `requests.post()` pattern to `https://openrouter.ai/api/v1/chat/completions`. DO NOT use `google/gemini-2.5-flash-image-preview` — it returns 404 "No endpoints found".

### Step 3a: Iterative Refinement Pattern

Cover generation is rarely perfect in one shot. Expect to iterate 2-3 times based on user feedback. The pattern:

1. **First pass**: Generate with a broad scene description, genre-appropriate palette, and basic typography
2. **Refine art**: If user says "art weak" or "needs to be more dramatic," add `DRAMATIC` (all-caps), specify backlighting, extreme angles, and make the scene description more specific
3. **Refine typography**: If user says "topography bad overlapping text," check the spacing rules above (most common issue: series label and title overlapping)
4. **Adjust brightness**: Some covers (especially those with water, hope, or optimistic themes) benefit from being brighter. If user says "too dark," remove "deep blacks" from the prompt, add "BRIGHT, LUMINOUS" in all-caps, and use a lighter gradient overlay
5. **Fix author name**: The author is always "Bob J Mills" — never use any other name
6. **Switch ratio**: If user says "full width" or "6×9," switch from 3:4 to 2:3 (1200×1800) full-bleed and regenerate the art

**Brightness by theme (proactive, not reactive):** Rather than waiting for "too dark" feedback, match brightness to the book's emotional tone:
- **Hope / life / discovery / water themes** → BRIGHT, LUMINOUS. Remove "deep blacks" from prompt. Add "bright, sunlit, glowing." Use lighter gradient overlays (max alpha 100 instead of 180). **Also use PIL ImageEnhance** after generation to boost brightness and contrast.
- **Survival / thriller / danger** → Dark, high-contrast. Deep blacks, emergency red accents, harsh shadows.
- **Mystery / conspiracy** → Sterile cold whites + pools of deep shadow. Clinical.
- **Space / void / isolation** → Deep space blacks, cold stars. Can be very dark.
- **Colony / civilization** → Warm, inhabited feel. Greens, warm ambers, livable light.

**PIL brightness enhancement for bright themes:**
```python
from PIL import ImageEnhance
img = ImageEnhance.Brightness(img).enhance(1.25)  # 25% brighter
img = ImageEnhance.Contrast(img).enhance(1.1)     # slightly more contrast
```

Apply this BEFORE generating — don't generate moody dark art for a water-theme book and wait to be told to brighten it.

**Feedback signals and their fixes:**

| User says | The fix |
|-----------|---------|
| "overlapping text" / "topography bad" | Check series-to-title gap (needs 25px), title line spacing (needs 8px), title height limit (37%) |
| "title is too small" | Resize to exactly 80% of cover width. For short words like "MOON ROCK" or "WATERS END," keep on one line |
| "needs to be more dramatic" | Add DRAMATIC to prompt, specify backlighting/extreme angle, increase contrast |
| "not sci-fi enough" | Add specific sci-fi elements (spacesuits, spacecraft, alien tech, lunar/planetary surfaces) |
| "too dark" | Remove dark color refs from prompt, add BRIGHT/LUMINOUS, lighten gradient overlay |
| "full width / 6×9" | Switch to 1200×1800 (2:3 ratio) full-bleed, no empty zone in prompt |
| "wrong author" | Change to "Bob J Mills" — never guess or use AI-generated author names |

### Step 4: Apply Typography Overlay (PIL)

This is the most critical step and the most common source of user corrections. The typography MUST NOT overlap and MUST follow these spacing rules:

#### Layout Constants (for 1024×1536 working canvas — 3:4 portrait)
> **Note:** This is the *design* working size. Final export to KDP must be **2560×1600 JPEG** (see Step 5).
```
SERIES_LABEL_Y = 15        # Series name at very top
SERIES_LABEL_GAP = 25      # Gap between series label and title start
TITLE_LINE_SPACING = 8     # Pixels between title lines
TITLE_MAX_Y = target_h * 0.37  # Title must not go below this
AUTHOR_BAR_HEIGHT = 55     # Dark bar at bottom for author name
```

#### Full-Bleed 6×9 Covers (2:3 ratio — 1200×1800px)

When the user requests "full width 6×9" or "full bleed," use **2:3 portrait aspect ratio** (1200×1800px at 200 DPI) instead of 3:4. The 2:3 ratio matches standard trade paperback trim size and requires edge-to-edge art with no empty zone:

- Image dimensions: **1200 × 1800** (or 1800 × 2700 at 300 DPI)
- Art should fill the entire frame — no "leave top 40% empty" prompt instruction
- Typography overlay still uses the same gradient + shadow approach, but the gradient can be lighter since the art is designed to be behind all text
- Use this aspect ratio for print-ready covers, especially when the user says "full width" or "6x9"

**Prompt adjustment for full-bleed:**
```
SCI-FI BOOK COVER 6x9 FULL BLEED. Edge-to-edge [scene description spanning the full frame]. 
The composition fills the entire image — no empty space. 2:3 aspect ratio.
```

#### Typography Element Order (Top to Bottom)

1. **Series label** — Small (14pt), centered, light gray. Position: 15px from top edge. Format: `"Series Name  •  Book N"`

2. **Title** — Bold sans-serif (LiberationSans-Bold.ttf), centered, white with black shadow. Scaled to ~80% of cover width. Each line gets 8px spacing below it. Title must have at least 25px gap below series label. Title must NOT extend below 37% of cover height.

3. **Author name** — 28pt, white, centered in a dark bar at the bottom of the cover. Bar is 55px tall, solid black at 180 alpha.

#### Font Selection
```python
font_path = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
# Fallback: /usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf
```

#### Font Sizing for 80% Width (including multi-line stacked titles)
```python
# Calculate font size so the widest title line takes 80% of cover width
# Works for both single-line and multi-line stacked titles
TITLE_LINES = ["THE", "OWNER'S", "MANUAL FOR", "AI AGENTS"]  # Can be 1-6 lines
MAX_WIDTH_PCT = 0.80

# Iterative search: start high, step down until widest line fits
title_size = 12
for test_size in range(200, 10, -1):
    font_test = ImageFont.truetype(font_path, test_size)
    widths = [draw.textbbox((0, 0), line, font=font_test)[2] for line in TITLE_LINES]
    max_w = max(widths)
    if max_w <= int(target_w * MAX_WIDTH_PCT):
        title_size = test_size
        break

title_font = ImageFont.truetype(font_path, title_size)
```

**For 4-line business book titles** (common pattern on non-fiction covers):
Split the title into logical reading groups, not arbitrary word breaks:
- "THE / OWNER'S / MANUAL FOR / AI AGENTS" (4 lines) — groups by natural phrasing
- "THE / AUTONOMOUS / ENTERPRISE" (3 lines) — each word on its own line for impact
- "WHAT EVERY / BUSINESS OWNER / NEEDS TO KNOW" (3 lines) — by prepositional phrases

The widest line will typically be the longest phrase. "MANUAL FOR" at 10 chars ≈ 80% at 110px on 1024px canvas. Add a subtitle line below the stacked title in a smaller font (~22% of title size) if the book has one.

**Non-fiction business cover specific guidelines:**
- Title should feel authoritative and large — 110px+ on 1024px canvas (much larger than fiction covers which run 58-72px)
- Use 4-layer shadow (4,3,2,1px offsets) instead of the standard 2px, because business titles are on dark abstract backgrounds and need deeper depth
- The widest line hitting exactly 80% of canvas width is the target — print it after calculation for verification:
  ```python
  print(f"Widest line: {max_w}px ({max_w/target_w*100:.0f}% of width)")
  ```
- Subtitle goes below the stack, not between title and author — use ~22% of title font size

#### Single-Line vs Multi-Line Title Decision

**RULE: Short titles (2-3 words, under ~12 characters total per word) MUST be on ONE line.** Stacking short words like "WATERS END" or "MOON ROCK" creates vertically cramped covers with massive, ugly letterforms that look amateurish. Only stack multi-word titles when a single line would make the font smaller than 36pt.

Decision logic:
```python
# Check if title fits on one line at 58pt
test_font = ImageFont.truetype(font_path, 58)
one_line = " ".join(title_words)
one_line_w = draw.textbbox((0,0), one_line, font=test_font)[2]
if one_line_w < target_w * 0.95:  # Fits at 58pt on one line?
    title_lines = [one_line]  # Use single line!
    # Then scale to exactly 80% below
else:
    title_lines = title_words  # Stack as-is
```

For single-line titles at 80% width: calculate font size so the text fills 80-85% of cover width. A 2-word title like "WATERS END" at 1200px width needs approximately 145pt to hit 80% width. Don't be afraid of large sizes — big bold text looks professional.

#### Shadow Pass (Four-Layer)
Every text element gets a 4px offset shadow for readability against any background. Both business and sci-fi covers use the same 4-layer pattern:
```python
# 4-layer shadow (both genres)
for ox, oy in [(4, 4), (3, 3), (2, 2), (1, 1)]:
    draw.text((x + ox, y + oy), text, font=font, fill=(0, 0, 0, 200))
# Main text
draw.text((x, y), text, font=font, fill=(255, 255, 255, 255))
```

#### Gradient Overlays for Legibility
Before drawing text, apply gradient overlays to the base image:
```python
overlay = Image.new("RGBA", (target_w, target_h), (0, 0, 0, 0))
draw_over = ImageDraw.Draw(overlay)

# Top gradient: very dark at top edge, fading down through the title zone
for y in range(int(target_h * 0.35)):
    if y < 40:
        alpha = 200  # Dark strip at very top
    else:
        fade = (y - 40) / (target_h * 0.35 - 40)
        alpha = max(0, int(200 * (1 - fade)))
    draw_over.rectangle([0, y, target_w, y + 1], fill=(0, 0, 0, min(alpha, 180)))

# Bottom bar for author name
draw_over.rectangle([0, target_h - 55, target_w, target_h], fill=(0, 0, 0, 180))
```

### Step 5: Export to KDP-Compliant Format

After the cover is designed at working resolution, export to KDP specs:

**Kindle eBook (marketing cover):**
```python
from PIL import Image

# Open the designed cover (any size/ratio)
img = Image.open('{BOOK_KEY}_Cover.png')

# Crop or pad to exactly 2560×1600 (1.6:1 ratio)
# If source is taller (e.g., 1024×1536), resize width to 1600, then crop height to 2560
# If source is wider, resize height to 2560, then crop width to 1600

w, h = img.size
target_ratio = 1600 / 2560  # width / height = 0.625
current_ratio = w / h

if current_ratio > target_ratio:
    # Too wide — resize by height, then center-crop width
    new_h = 2560
    new_w = int(new_h * current_ratio)
    img = img.resize((new_w, new_h), Image.LANCZOS)
    left = (new_w - 1600) // 2
    img = img.crop((left, 0, left + 1600, 2560))
else:
    # Too tall — resize by width, then center-crop height
    new_w = 1600
    new_h = int(new_w / current_ratio)
    img = img.resize((new_w, new_h), Image.LANCZOS)
    top = (new_h - 2560) // 2
    img = img.crop((0, top, 1600, top + 2560))

# Ensure RGB (not RGBA)
img = img.convert('RGB')

# Save as JPEG with quality 95+
img.save('{BOOK_KEY}_KDP_Kindle_Cover.jpg', 'JPEG', quality=95)

# Verify
from PIL import Image as V
v = V.open('{BOOK_KEY}_KDP_Kindle_Cover.jpg')
print(f'KDP Kindle cover: {v.size}, mode={v.mode}, ratio={v.size[1]/v.size[0]:.2f}')
# Expected: (1600, 2560), mode=RGB, ratio=1.60
```

**Paperback wrap cover** — generate from the same source art using the wrap cover calculation. See `book-deliverable-kdp` skill for `build_kdp_package.py` pattern.

### Step 5b: Quality Checklist (including Vision QA)

Before delivering, verify:

- [ ] Title text does NOT overlap with series label (25px+ gap)
- [ ] Multi-line titles have consistent 8px line spacing
- [ ] Title does NOT extend past 37% of cover height into artwork area
- [ ] Author name is fully visible in the bottom bar
- [ ] All text has shadow for legibility
- [ ] Top 40% of cover is mostly empty (no important visual elements obscured by title)
- [ ] **EPUBs updated**: All EPUB files (digital, hardcover, paperback) have the new cover embedded at `EPUB/images/cover.jpg`. See `references/epub-cover-embedding.md` for the Python batch update pattern.
- [ ] Source cover PNG saved in book directory (for future edits)
- [ ] Paperback wrap cover PDF generated (if applicable, per trim size + page count)
- [ ] Colors match the genre/subgenre palette
- [ ] No duplicate text elements
- [ ] No AI-generated text artifacts in the image itself

**Vision QA via alternate model when agent lacks vision:**

When the active agent model doesn't support image input (e.g., deepseek-v4), use a direct API call to a vision-capable model for quality checks:

```python
import requests, base64

with open("/path/to/cover.png", "rb") as f:
    img_b64 = base64.b64encode(f.read()).decode()

api_key = "..."  # from ~/.hermes/.env OPENROUTER_API_KEY
headers = {"Authorization": f"Bearer {api_key}"}
payload = {
    "model": "openai/gpt-4o-mini",
    "messages": [{"role": "user", "content": [
        {"type": "text", "text": "Describe this book cover. Is there baked-in text or watermarks? Is the title area clear (top 40%)? How's the composition and color palette?"},
        {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img_b64}"}}
    ]}]
}
resp = requests.post("https://openrouter.ai/api/v1/chat/completions", json=payload, headers=headers, timeout=30)
print(resp.json()["choices"][0]["message"]["content"])
```

This catches baked-in AI text, wrong author names, artifacts, and inappropriate compositions before showing the user. Use `openai/gpt-4o-mini` for cost efficiency — it's cheap and fast enough for cover QA.

## Cover Style Reference Standards

### Business Books — "AI That Works" Style
Reference cover: `/home/bob/books/Business_Series/AI_That_Works/MIFECO_AI_Playbook_Cover.png`
- **Background:** Dark solid color (deep navy #0a0a1a or black)
- **Title treatment:** Large, white, bold sans-serif title stacked in 3-5 lines, centered
- **Title sizing:** Widest line = exactly 80% of cover width
- **Subtitle:** Below title stack, ~22% of title font size, lighter color
- **Author name:** Bottom of cover, white text on dark bar or background
- **Accent colors:** Single accent color (amber/gold or cyan) sparingly
- **Art:** Minimal or abstract — geometric shapes, neural networks, constellation patterns. No people, no buildings, no literal illustrations.
- **Tagline:** "A Business Book" or similar small label between title and author
- **KDP export:** 2560×1600 px JPEG, RGB, ≤50MB

### Science Fiction Books — "Moon Rock" (Lunar Foundation) Style
Reference covers: `/home/bob/books/Lunar_Foundation_Series/Book_1_Moon_Rock/LF_1_Moon_Rock_Cover.png`
- **Background:** Dramatic space imagery — planetary surfaces, starfields, spacecraft, dramatic lighting
- **Color palette:** Deep space blacks/blues with warm amber/gold accents (habitat lights, sun)
- **Title treatment:** Bold, centered, white with 4-layer shadow for depth against busy backgrounds
- **Series label:** "The [Series Name] • Book N" at top in small white/gray text
- **Title sizing:** Large and impactful, 110pt+ on 1024px canvas (business) or 58-72pt (sci-fi)
- **Author name:** Bottom bar, white, smaller than title
- **Gradient overlay:** Dark gradient on top 35% for title legibility, dark strip on bottom 10% for author name
- **Shadow:** 4-layer shadow (4,3,2,1px offsets) for sci-fi covers on complex backgrounds
- **KDP export:** 2560×1600 px JPEG, RGB, ≤50MB

### Author Photo Requirement
A copy of the author's photo MUST be placed in the root directory of every book project.
- Source: `/home/bob/books/Business_Series/AI_That_Works/Author_Photo.jpg`
- Copy to: `<book_directory>/Author_Photo.jpg`
- This applies to ALL book directories, both business and fiction

- **Shadow layers: 4 for both genres** — Both business and sci-fi covers use 4-layer shadow (4,3,2,1px offsets). The old "Shadow Pass (Two-Layer)" code pattern below is superseded. Never use a single 2px shadow on any book cover.
- **KDP JPEG naming with _new suffix** — When source is `cover_new.png`, strip `_new` before adding `_KDP`: export as `cover_KDP.jpg`, NOT `cover_new_KDP.jpg`. Same for `cover_b1_new.png` → `cover_b1_KDP.jpg`.

### Reusable Scripts

#### `scripts/cover_typography.py` — Cover Typography CLI

Apply typography overlay to a base LLM-generated image via CLI:

```bash
# Sci-fi cover (default)
python3 scripts/cover_typography.py base.png output.png \
  --title "SUNWARD" "EXODUS" \
  --series "The Age of Lightships • Book 1"

# With KDP export
python3 scripts/cover_typography.py base.png output.png \
  --title "GHOSTS BEYOND" "NEPTUNE" \
  --book-num 3 --output-kdp cover_KDP.jpg

# Full-bleed 6x9
python3 scripts/cover_typography.py base.png output.png \
  --title "THE LAST" "PHOTON FLEET" \
  --book-num 4 --ratio 2:3
```

Handles: image resize/crop, gradient overlay, series label, iterative font sizing, single-line vs stacked title decision, 4-layer shadow, author name, and KDP JPEG export.

#### `references/epub-cover-embedding.md` — EPUB Cover Update Pattern

When covers change, use the Python pattern in `references/epub-cover-embedding.md` to batch-update all EPUB files for a book (digital, hardcover, paperback). The pattern extracts the ZIP, replaces `EPUB/images/cover.jpg`, preserves `cover.xhtml`, and repacks with mimetype-first ordering.

### Reusable Scripts

#### `scripts/cover_typography.py` — Cover Typography CLI

Apply typography overlay to a base LLM-generated image via CLI:

```bash
# Sci-fi cover (default)
python3 scripts/cover_typography.py base.png output.png \
  --title "SUNWARD" "EXODUS" \
  --series "The Age of Lightships • Book 1"

# Business cover
python3 scripts/cover_typography.py base.png output.png \
  --title "THE CRISIS-" "READY" "COMPANY" \
  --subtitle "Disaster-Proof Strategies for Modern Business" \
  --business \
  --output-kdp cover_KDP.jpg
```

Handles: image resize/crop, gradient overlay, series label, iterative font sizing, single-line vs stacked title decision, 4-layer shadow, subtitle, author name, and KDP JPEG export.

### Common Pitfalls

- **Overlapping series label and title** — Always maintain 25px minimum gap between series label bottom and title top
- **Title extending into artwork** — If title has too many lines, reduce font size or increase line-count before compressing further. Hard limit: 37% of cover height
- **No shadow on text** — Always use 2px black shadow. White text on light background is unreadable without it
- **Wrong aspect ratio** — Book covers must be 3:4 portrait (1024×1536). Never use square or landscape
- **Missing top gradient** — Light backgrounds need the top gradient overlay for text to be readable
- **Gemini API returns mixed text+image parts** — Gemini's response can contain BOTH text parts (descriptions) AND image parts (inlineData). The text part comes FIRST. Always iterate ALL parts and use `isinstance(part, dict) and 'inlineData' in part` to find the image. A simple `if 'inlineData' in part` will fail silently when it encounters a text-only dict. Example robust pattern:
  ```python
  for part in parts:
      if isinstance(part, dict) and 'inlineData' in part:
          img_bytes = base64.b64decode(part['inlineData']['data'])
          break
  ```
- **Text in the artwork** — If Gemini generates text in the image, you can't control it via the prompt. Just overlay your own text on top — the viewer reads your clean text, not the AI muddle
- **Inspired by best-selling book trap** — When the user says "inspired by [Book X]" or "make it like [Book Y]," capture the *genre/style/mood* (cinematic lighting, color temperature, composition style) but NEVER replicate specific visual elements (specific color palettes, recognizable compositions, named objects/vehicles/landmarks, or character poses) from that book. **CRITICAL: this also applies to TEXT elements** — do NOT put the other book's author name, subtitle, series name, or any text from the inspiration book on the cover. Real case: a cover was "inspired by" a best-selling book and accidentally had that book's author (Aurora Novak) and subtitle (Celestial Tears) instead of the correct ones. The cover must feel distinct from any existing title. When in doubt, use completely different scene elements from the user's actual book content and always hardcode the correct author name.
- **NO subtitles or extra words** — The cover must ONLY contain: series label, title, author name. Never add taglines like "A Novel", "Book 3 of the Series", subtitles, pull quotes, or any other text unless the user explicitly asks for it. Every extra word is a point of failure and user correction.
- **Author name is always "Bob J Mills"** — This is the default. Never prompt-infer, guess, or use any other name. The typography template must hardcode this value. If you're generating multiple covers in batch, triple-check none of them picked up a different author name from a stale variable or copy-paste error.
- **Business vs fiction covers use different conventions** — Business/tech/non-fiction covers are often typography-only on dark backgrounds, with no artwork or illustration. Fiction covers are scene-based. Don't apply fiction composition rules (top-40%-empty zone, dramatic scene prompts) to business covers. Business covers should feel like a system designer's manual, not a novel. Use the genre table in Step 1 to select the right approach.
- **Replicating a cover's style requires pixel analysis, not eyeballing** — When the user says "make it like [cover X]," don't guess the parameters. Use the pixel analysis technique in `references/cover-style-analysis.md` to extract exact background color, text placement, margin ratios, and color palette from the reference image.

> **Session-level detail:** See `references/cover-pitfalls-sessions.md` for real correction transcripts behind these pitfalls — including the "inspired by" trap, single-line vs stacked title fixes, and baked-in AI text issues. See `references/cover-style-analysis.md` for the pixel-analysis technique used to replicate existing cover designs.

### Filling a Missing Cover in a Series

When a book in a series has no cover at all (e.g., the fourth book was never completed to cover stage), you need to generate one that matches the series visually. This is a different challenge from fixing typography on an existing cover:

1. **Study the existing series covers** — Examine the Cover.png files for books 1-N. Note the color palette, typography layout (same font, same title_size, same author placement, same series label format), gradient treatment, and general mood.

2. **Read the manuscript** — Extract the story's key themes, setting, and emotional tone from the HTML/epub. Look for pivotal scenes that could work as cover art.

3. **Design the prompt** using the genre table and prompt rules in Step 2 — but tailor it to match the series tone while being unique to this book's story.

4. **Generate the raw image** — Follow Step 3 using Gemini Flash Image. The raw image may come back square (1024×1024); apply full-bleed crop to 1024×1536.

5. **Apply identical typography parameters** from the series — same title_size, same series_label position, same author placement, same gradient overlay parameters. Only the artwork and book-specific text change.

6. **Place the cover** into both `publishing_output/covers/` (canonical source) and the book's target directory.

**Real example — Waters Horizon (Book 4 of The Lunar Foundation):**
- Existing covers (Moon Rock, Mooncoming, Waters End) used: deep space blues/black, warm amber habitat lights, 58pt stacked title ("MOON / ROCK", "MOONCOMING", "WATERS / END"), series label "The Lunar Foundation  •  Book N" at top, "Bob Mills" author at bottom, gradient overlay at 28% top / 10% bottom
- Manuscript themes: post-water-crisis transformation, expanded base, thriving hydroponics, second borehole, memorials, looking toward the horizon
- Generated artwork: panoramic lunar base with glowing biodomes, drill rig, Earth in dark sky, rover tracks — unique to Waters Horizon but same color palette (amber/gold, green hydroponics, deep space black/blue)
- Same typography parameters applied directly (58pt, same shadow/gradient values, same positioning)
- QA confirmed: no baked-in text, clear title area, appropriate scene

### Generating a Cover for a Brand-New Book (No Existing Series Reference)

When the book is a standalone or the first in a series, there are no existing covers to match. Start from Step 1 (Research the Genre) and build from scratch. See `references/cover-generation-sessions.md` for step-by-step walkthroughs of full cover creation sessions including the Waters Horizon case.

### Lessons from Previous Sessions

The user explicitly corrected cover typography across 7 books with the feedback "topography bad overlapping text" and "duplicate text." The root causes were:
1. Series label and title had insufficient gap
2. Multi-line title lines were too close together (needs 8px minimum)
3. Title was positioned too high (overlapping the series label)
4. Author text was rendered twice by mistake (ghost text)

All of these are now encoded as spacing rules and pitfalls above.
