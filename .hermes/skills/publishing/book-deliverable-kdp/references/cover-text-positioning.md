# Cover Text Positioning (Font Baseline + Alpha Composite)

Precise text placement on book covers requires understanding PIL's font baseline system.

## Font Baseline Model

PIL's `ImageDraw.text((x, y), text, font=font)` uses `y` as the **ascender line** 
(not the top of the text). `textbbox()` returns offsets relative to this line.

**To place text top edge at pixel_y:**
```python
baseline_y = pixel_y - bbox[1]
d.text((x, baseline_y), text, font=font)
```

**LiberationSans-Bold.ttf metrics:**
- 100pt: bbox=(0, 19, 194, 112), height=93
- 94pt:  bbox=(0, 18, 194, 106), height=88
- 46pt:  bbox=(0, 9, 613, 52),   height=43
- 38pt:  bbox=(0, 7, 241, 43),   height=36

## Alpha Composite for High-Contrast Text

Semi-transparent bars wash out text colors (yellow becomes brown). Use fully 
opaque overlay + alpha mask:

```python
overlay = Image.new('RGB', (w, h), (0, 0, 0))
draw = ImageDraw.Draw(overlay)
draw.rectangle([40, 60, w-40, 400], fill=(0, 0, 0))
draw.text((cx, baseline_y), "TITLE", font=font, fill='white')

alpha = overlay.convert('L').point(lambda p: 220 if p > 30 else 0)
overlay_rgba = overlay.convert('RGBA')
overlay_rgba.putalpha(alpha)
result = Image.alpha_composite(bg.convert('RGBA'), overlay_rgba).convert('RGB')
```

## Verification
Scan y-values around expected text position (text may be 5-10px off from 
calculated due to font hinting). Check for RGB(255,255,255) white and 
RGB(255,255,0) yellow at center x-positions.