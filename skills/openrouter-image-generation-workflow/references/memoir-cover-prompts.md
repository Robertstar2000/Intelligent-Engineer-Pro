# Memoir Cover Prompt Patterns

Prompts that worked for Bob's memoir "Tomorrow Is Still Open" — use as templates for future memoir covers.

## The Electrical-Spark-to-Stars Metaphor (This Session)

### Concept
A 1950s Michigan lake cabin at twilight with warm window light, a star-filled sky, and an electrical spark arcing from a porch outlet up into the stars — captures the book's central metaphor: a single moment of childhood curiosity reaching across a lifetime toward infinity.

### Prompt

```
Create a cinematic book cover for a literary memoir. A 1950s Michigan lake cabin at twilight — warm golden light spills from a single window onto a wooden dock. Above the cabin, the night sky transitions from warm amber near the horizon into deep indigo filled with scattered stars. The composition should feel like memory itself: intimate, warm at the edges but vast above.

CRITICAL COMPOSITION REQUIREMENTS:
- The top 40% of the image must be clean dark night sky with scattered stars ONLY — no buildings, trees, or objects intruding. This space is reserved for the book title.
- The bottom 15% must be dark water/tree silhouette with no bright elements — reserved for the author name.
- The middle 45% contains the cabin, warm window light, dock, lake reflection.
- No text, no words, no letters, no symbols, no watermarks anywhere.
- 2:3 portrait aspect ratio (tall, not wide).
- Cinematic quality, photorealistic, high contrast, emotional mood.
- Colors: warm amber and gold from the cabin window, cool deep blues and indigos in the sky.
```

### Result
Gemini Flash Image returned 1024×1024 (square). Resized to 1024×1536 via full-bleed crop (scale to fill height, center-crop width). Top 40% had avg brightness 87/255 — dark enough for white text with subtle gradient overlay.

### Typography (1024×1536 canvas)
```
Title: stacked vertically, 52pt LiberationSans-Bold, white with 2px black shadow
    "TOMORROW" / "IS STILL" / "OPEN"
    Centered within top 35% of canvas, evenly spaced (line_h = font_size × 1.25)
Subtitle: 18pt, lighter italic, below title
    "Through the past the future is born unwritten"
Author: 28pt, centered at bottom, y = h - 140px
    "Bob J Mills"
Gradient overlay: top 35% (alpha 0→60), bottom 12% (alpha 0→50)
```

## General Memoir Cover Principles

### What Works for Memoirs
1. **Single emotional scene** — one evocative image that conveys the book's emotional core
2. **Warm, nostalgic colors** — amber, gold, sepia for past; cool blues for reflection
3. **Strong contrast for text** — dark sky at top for white title, dark ground at bottom for author
4. **Visual metaphor** — the cover should hint at the book's central idea without being literal
5. **Human-scale intimacy** — cabins, windows, docks, porches, small structures work better than grand landscapes

### What to Avoid
- Busy cityscapes or crowds (too much visual noise for text legibility)
- Abstract vectors or geometric patterns (feel generic, not personal)
- Photorealistic faces (hard to nail with AI; cheapens the cover if wrong)
- Text baked into the prompt (always garbled — apply typography locally in PIL)