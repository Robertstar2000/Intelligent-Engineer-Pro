# Book Cover Typography — Working Code Template
# Copy this into execute_code when generating a book cover.
# Adjust title_words, series_info, and img for each book.

from PIL import Image, ImageDraw, ImageFont, ImageEnhance

target_w, target_h = 1200, 1800  # 2:3 for 6x9 full-bleed
font_path = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
img = Image.open("raw_cover.png").convert("RGBA")
img = img.resize((target_w, target_h), Image.LANCZOS)

# === PER-BOOK PARAMS ===
title_words = ["WATERS", "END"]  # will be joined if short enough
author_text = "Bob J Mills"      # ALWAYS this — never guess
series_info = "The Lunar Foundation  •  Book 3"
brightness = "bright"            # "bright" | "dark" | "neutral"
# ========================

# Gradient overlay — intensity varies by brightness
if brightness == "bright":
    max_alpha = 100  # lighter overlay
    # Also boost brightness and contrast
    img = ImageEnhance.Brightness(img).enhance(1.25)
    img = ImageEnhance.Contrast(img).enhance(1.1)
elif brightness == "dark":
    max_alpha = 200  # heavier darkness
else:
    max_alpha = 140

overlay = Image.new("RGBA", (target_w, target_h), (0, 0, 0, 0))
do = ImageDraw.Draw(overlay)
for y in range(int(target_h * 0.35)):
    if y < 40:
        alpha = max_alpha
    else:
        fade = (y - 40) / (target_h * 0.35 - 40)
        alpha = max(0, int(max_alpha * (1 - fade)))
    do.rectangle([0, y, target_w, y + 1], fill=(0, 0, 0, min(alpha, max_alpha)))
do.rectangle([0, target_h - 55, target_w, target_h], fill=(0, 0, 0, 180))
img = Image.alpha_composite(img, overlay).convert("RGB")
draw = ImageDraw.Draw(img)

# Series label (top)
sf = ImageFont.truetype(font_path, 14)
sx = (target_w - (draw.textbbox((0, 0), series_info, font=sf)[2] -
                   draw.textbbox((0, 0), series_info, font=sf)[0])) // 2
draw.text((sx + 1, 16 + 1), series_info, font=sf, fill=(0, 0, 0, 180))
draw.text((sx, 16), series_info, font=sf, fill=(200, 200, 200, 220))

# Title — single line if short, stacked if long
test_font = ImageFont.truetype(font_path, 58)
one_line_candidate = " ".join(title_words)
olw = draw.textbbox((0, 0), one_line_candidate, font=test_font)[2]
if olw < target_w * 0.95:  # fits on one line?
    title_lines = [one_line_candidate]
else:
    title_lines = title_words  # stack

# Size to 80% width
tf = ImageFont.truetype(font_path, 58)
max_word_w = max(draw.textbbox((0, 0), l, font=tf)[2] for l in title_lines)
scale = (target_w * 0.82) / max_word_w
sz = max(36, min(180, int(58 * scale)))  # allow up to 180pt for single-line
tf = ImageFont.truetype(font_path, sz)

lh_list = [draw.textbbox((0, 0), l, font=tf)[3] -
           draw.textbbox((0, 0), l, font=tf)[1] for l in title_lines]
total_h = sum(lh_list) + 8 * (len(title_lines) - 1)
ty = 16 + 18 + 25  # series_y + series_line_height + gap
max_y = int(target_h * 0.37)
if ty + total_h > max_y:
    ty = max_y - total_h

cy = ty
for line in title_lines:
    bb = draw.textbbox((0, 0), line, font=tf)
    lw, lh = bb[2] - bb[0], bb[3] - bb[1]
    x = (target_w - lw) // 2
    draw.text((x + 2, cy + 2), line, font=tf, fill=(0, 0, 0, 200))
    draw.text((x, cy), line, font=tf, fill=(255, 255, 255, 255))
    cy += lh + 8

# Author (bottom bar — ALWAYS Bob J Mills)
af = ImageFont.truetype(font_path, 28)
ab = draw.textbbox((0, 0), author_text, font=af)
ax = (target_w - (ab[2] - ab[0])) // 2
ay = target_h - 55 + (55 - (ab[3] - ab[1])) // 2
draw.text((ax + 2, ay + 2), author_text, font=af, fill=(0, 0, 0, 200))
draw.text((ax, ay), author_text, font=af, fill=(255, 255, 255, 255))

img.save("Cover.png")
print(f"Cover saved. Title line(s): {title_lines}")
print(f"Title font size: {sz}pt, ~{round(max_word_w * scale / target_w * 100)}% width")
