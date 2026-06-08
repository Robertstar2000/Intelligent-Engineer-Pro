#!/usr/bin/env python3
"""
Multi-line book cover typography with gradient overlay.
Generates a 2:3 portrait cover (1024x1536) from square or any-source raw art.

Usage:
  python3 multi-line-cover-typography.py <raw_image.png> <output.png>

Edit the TITLE_LINES, SUBTITLE, AUTHOR constants below for your book.
"""

import os, sys
from PIL import Image, ImageDraw, ImageFont, ImageEnhance

# ─── CONFIG ───────────────────────────────────────────────────
TITLE_LINES = ["THE", "OWNER'S", "MANUAL FOR", "AI AGENTS"]
# Widest line auto-scales to 80% of cover width.
# Each element can be 1+ words — mixed lengths handled automatically.

SUBTITLE = "What Every Business Owner Needs to Know"
AUTHOR = "Bob J Mills"

WIDEST_LINE_PCT = 0.80       # widest line as fraction of total width
TOP_GRADIENT_PCT = 0.38      # how far the top gradient veil extends
BOT_GRADIENT_PCT = 0.15      # bottom gradient veil
TITLE_ZONE_PCT = 0.35        # vertical zone for stacked title (top portion)
LINE_GAP_MULT = 0.15         # gap between stacked lines as fraction of font size
SHADOW_LAYERS = 4            # shadow passes (more = bolder)
BRIGHTNESS = 1.15            # artwork brightness boost
CONTRAST = 1.05              # artwork contrast boost
TARGET_W, TARGET_H = 1024, 1536  # 2:3 portrait

# ─── FONT ─────────────────────────────────────────────────────
font_path = None
for fp in [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
]:
    if os.path.exists(fp):
        font_path = fp
        break
assert font_path, "No bold sans-serif font found!"

# ─── LOAD & EXTEND ART ────────────────────────────────────────
raw_path = sys.argv[1] if len(sys.argv) > 1 else "raw_cover.png"
out_path = sys.argv[2] if len(sys.argv) > 2 else "Cover.png"

img = Image.open(raw_path).convert("RGB")
ow, oh = img.size

# Scale to fill target height, center-crop width
scale = TARGET_H / oh
nw = int(ow * scale)
img = img.resize((nw, TARGET_H), Image.LANCZOS)
xo = (nw - TARGET_W) // 2
img = img.crop((xo, 0, xo + TARGET_W, TARGET_H))

# Brighten
img = ImageEnhance.Brightness(img).enhance(BRIGHTNESS)
img = ImageEnhance.Contrast(img).enhance(CONTRAST)

# ─── GRADIENT OVERLAY ────────────────────────────────────────
overlay = Image.new("RGBA", (TARGET_W, TARGET_H), (0, 0, 0, 0))
do = ImageDraw.Draw(overlay)

tg = int(TARGET_H * TOP_GRADIENT_PCT)
for y in range(tg):
    a = int(130 * (1 - y / tg))
    if a > 0:
        do.rectangle([0, y, TARGET_W, y + 1], fill=(0, 0, 0, min(a, 100)))

bg = int(TARGET_H * BOT_GRADIENT_PCT)
for y in range(bg):
    a = int(110 * (y / bg))
    if a > 0:
        do.rectangle([0, TARGET_H - bg + y, TARGET_W, TARGET_H - bg + y + 1],
                     fill=(0, 0, 0, min(a, 90)))

img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
draw = ImageDraw.Draw(img)

# ─── TITLE FONT SIZE (iterative, widest line at N% of width ────
max_w_px = int(TARGET_W * WIDEST_LINE_PCT)
font_size = 12
for ts in range(220, 10, -1):
    ft = ImageFont.truetype(font_path, ts)
    ws = [draw.textbbox((0, 0), ln, font=ft)[2] for ln in TITLE_LINES]
    if max(ws) <= max_w_px:
        font_size = ts
        break

font = ImageFont.truetype(font_path, font_size)

# ─── VERTICAL CENTERING ─────────────────────────────────────
metrics = []
for ln in TITLE_LINES:
    bb = draw.textbbox((0, 0), ln, font=font)
    metrics.append({"text": ln, "w": bb[2] - bb[0], "h": bb[3] - bb[1]})

gap = int(font_size * LINE_GAP_MULT)
total_h = sum(m["h"] for m in metrics) + gap * (len(metrics) - 1)
zone_h = int(TARGET_H * TITLE_ZONE_PCT)
cy = (zone_h - total_h) // 2 + 10

# ─── DRAW TITLE ──────────────────────────────────────────────
for m in metrics:
    x = (TARGET_W - m["w"]) // 2
    for n in range(SHADOW_LAYERS, 0, -1):
        draw.text((x + n, cy + n), m["text"], font=font, fill=(0, 0, 0, 200))
    draw.text((x, cy), m["text"], font=font, fill=(255, 255, 255))
    cy += m["h"] + gap

widest_line_w = max(m["w"] for m in metrics)
actual_pct = widest_line_w / TARGET_W
print(f"Widest line: {widest_line_w}px ({actual_pct*100:.0f}% — target {WIDEST_LINE_PCT*100:.0f}%)")
print(f"Font size: {font_size}px")

# ─── SUBTITLE ────────────────────────────────────────────────
if SUBTITLE:
    sf = ImageFont.truetype(font_path, int(font_size * 0.22))
    sb = draw.textbbox((0, 0), SUBTITLE, font=sf)
    sw = sb[2] - sb[0]
    sx = (TARGET_W - sw) // 2
    sy = cy + gap + 20
    for ox, oy in [(2, 2), (1, 1)]:
        draw.text((sx + ox, sy + oy), SUBTITLE, font=sf, fill=(0, 0, 0, 180))
    draw.text((sx, sy), SUBTITLE, font=sf, fill=(220, 220, 220))

# ─── AUTHOR BAR ─────────────────────────────────────────────
af = ImageFont.truetype(font_path, int(font_size * 0.35))
ab = draw.textbbox((0, 0), AUTHOR, font=af)
aw = ab[2] - ab[0]
ax = (TARGET_W - aw) // 2
ay = TARGET_H - int(TARGET_H * 0.06) - (ab[3] - ab[1])

bar_h = int(TARGET_H * 0.08)
draw.rectangle([0, TARGET_H - bar_h, TARGET_W, TARGET_H], fill=(0, 0, 0, 160))

for ox, oy in [(2, 2), (1, 1)]:
    draw.text((ax + ox, ay + oy), AUTHOR, font=af, fill=(0, 0, 0, 180))
draw.text((ax, ay), AUTHOR, font=af, fill=(255, 255, 255))

# ─── SAVE ────────────────────────────────────────────────────
img.save(out_path, "PNG", optimize=True)

# Also generate KDP JPEG (1600×2560)
jpg = img.resize((1600, 2560), Image.LANCZOS)
jpg_path = out_path.replace(".png", ".jpg")
jpg.save(jpg_path, "JPEG", quality=95)

print(f"Cover: {out_path}")
print(f"KDP  : {jpg_path}")
