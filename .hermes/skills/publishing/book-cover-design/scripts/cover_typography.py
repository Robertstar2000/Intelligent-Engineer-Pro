#!/usr/bin/env python3
"""
cover_typography.py — Apply typography overlay to a base AI-generated book cover.

Usage:
    python3 cover_typography.py <base_image> <output_png> \\
        --title "LINE1" "LINE2" ... \\
        --book-num N \\
        --series "Series Name" \\
        [--author "Author Name"] \\
        [--output-kdp <kdp_jpeg_path>] \\
        [--ratio 3:4|2:3]

Defaults:
    Author: "Bob J Mills"
    Ratio: 3:4 portrait (1024x1536 design, 1600x2560 KDP export)

Examples:
    python3 cover_typography.py base.png output.png \\
        --title "SUNWARD" "EXODUS" --book-num 1 \\
        --series "The Age of Lightships" --output-kdp cover_KDP.jpg

    python3 cover_typography.py base.png output.png \\
        --title "GHOSTS BEYOND" "NEPTUNE" --book-num 3 \\
        --series "The Age of Lightships" --ratio 2:3
"""

import argparse
from PIL import Image, ImageDraw, ImageFont

FONT_PATH_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
FONT_PATH_REG = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"

PRESETS = {
    "3:4": {"w": 1024, "h": 1536, "kdp_w": 1600, "kdp_h": 2560},
    "2:3": {"w": 1200, "h": 1800, "kdp_w": 1600, "kdp_h": 2560},
}

SERIES_LABEL_Y = 15
SERIES_LABEL_GAP = 25
TITLE_MAX_Y_PCT = 0.37
AUTHOR_BAR_HEIGHT = 55


def get_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()


def compute_title_size(draw, title_lines, font_path, target_w, max_w_pct=0.80):
    max_allowed = int(target_w * max_w_pct)
    for size in range(200, 10, -1):
        font = get_font(font_path, size)
        widths = [draw.textbbox((0, 0), line, font=font)[2] for line in title_lines]
        if max(widths) <= max_allowed:
            return size, font
    return 30, get_font(font_path, 30)


def should_use_one_line(title_words, draw, font_path, target_w):
    test_font = get_font(font_path, 58)
    one_line = " ".join(title_words)
    bbox = draw.textbbox((0, 0), one_line, font=test_font)
    return (bbox[2] - bbox[0]) < target_w * 0.95, one_line


def apply_typography(base_image_path, output_png, title_lines, book_num, series_name,
                     author="Bob J Mills", output_kdp=None, ratio="3:4"):
    preset = PRESETS.get(ratio, PRESETS["3:4"])
    TW, TH = preset["w"], preset["h"]

    img = Image.open(base_image_path).convert("RGB")
    w, h = img.size
    new_h = int(h * TW / w)
    img = img.resize((TW, new_h), Image.LANCZOS)

    if img.height > TH:
        top = (img.height - TH) // 2
        img = img.crop((0, top, TW, top + TH))
    elif img.height < TH:
        padded = Image.new("RGB", (TW, TH), (0, 0, 0))
        padded.paste(img, (0, (TH - img.height) // 2))
        img = padded

    draw = ImageDraw.Draw(img, "RGBA")

    # Gradient overlays
    overlay = Image.new("RGBA", (TW, TH), (0, 0, 0, 0))
    draw_ov = ImageDraw.Draw(overlay)
    for y in range(int(TH * TITLE_MAX_Y_PCT)):
        if y < 40:
            alpha = 200
        else:
            fade = (y - 40) / (TH * TITLE_MAX_Y_PCT - 40)
            alpha = max(0, int(200 * (1 - fade)))
        draw_ov.rectangle([0, y, TW, y + 1], fill=(0, 0, 0, min(alpha, 180)))
    draw_ov.rectangle([0, TH - AUTHOR_BAR_HEIGHT, TW, TH], fill=(0, 0, 0, 180))
    img = Image.alpha_composite(img.convert("RGBA"), overlay)
    draw = ImageDraw.Draw(img)

    # Series label
    series_label = f"{series_name} • Book {book_num}"
    series_font = get_font(FONT_PATH_REG, 14)
    bbox = draw.textbbox((0, 0), series_label, font=series_font)
    sw = bbox[2] - bbox[0]
    sx = (TW - sw) // 2
    for ox, oy in [(2, 2), (1, 1)]:
        draw.text((sx + ox, SERIES_LABEL_Y + oy), series_label, font=series_font, fill=(0, 0, 0, 180))
    draw.text((sx, SERIES_LABEL_Y), series_label, font=series_font, fill=(180, 180, 200, 255))

    # Title — decide single-line vs stacked
    tf = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    use_one_line, one_line_text = should_use_one_line(title_lines, tf, FONT_PATH_BOLD, TW)
    if use_one_line and len(title_lines) <= 3:
        title_lines_final = [one_line_text]
    else:
        title_lines_final = title_lines

    title_size, title_font = compute_title_size(draw, title_lines_final, FONT_PATH_BOLD, TW)

    line_heights = []
    for line in title_lines_final:
        bb = draw.textbbox((0, 0), line, font=title_font)
        line_heights.append(bb[3] - bb[1])
    spacing = max(4, int(title_size * 0.15))
    total_title_h = sum(line_heights) + spacing * (len(title_lines_final) - 1)

    title_start_y = SERIES_LABEL_Y + 14 + SERIES_LABEL_GAP
    if title_start_y + total_title_h > int(TH * TITLE_MAX_Y_PCT):
        title_start_y = max(title_start_y, int(TH * TITLE_MAX_Y_PCT) - total_title_h)

    # Draw title with 4-layer shadow
    cy = title_start_y
    for i, line in enumerate(title_lines_final):
        bb = draw.textbbox((0, 0), line, font=title_font)
        lw = bb[2] - bb[0]
        lx = (TW - lw) // 2
        lh = line_heights[i]
        for ox, oy in [(4, 4), (3, 3), (2, 2), (1, 1)]:
            draw.text((lx + ox, cy + oy), line, font=title_font, fill=(0, 0, 0, 200))
        draw.text((lx, cy), line, font=title_font, fill=(255, 255, 255, 255))
        cy += lh + spacing

    # Author name
    author_font = get_font(FONT_PATH_REG, 28)
    bb = draw.textbbox((0, 0), author, font=author_font)
    aw, ah = bb[2] - bb[0], bb[3] - bb[1]
    ax = (TW - aw) // 2
    ay = TH - AUTHOR_BAR_HEIGHT + (AUTHOR_BAR_HEIGHT - ah) // 2
    for ox, oy in [(4, 4), (3, 3), (2, 2), (1, 1)]:
        draw.text((ax + ox, ay + oy), author, font=author_font, fill=(0, 0, 0, 200))
    draw.text((ax, ay), author, font=author_font, fill=(255, 255, 255, 255))

    img.save(output_png)
    print(f"Saved: {output_png} ({TW}x{TH})")

    # KDP export
    if output_kdp:
        kdp_w, kdp_h = preset["kdp_w"], preset["kdp_h"]
        img_kdp = img.convert("RGB")
        w, h = img_kdp.size
        target_ratio = kdp_w / kdp_h
        current_ratio = w / h
        if current_ratio > target_ratio:
            new_h = kdp_h
            new_w = int(new_h * current_ratio)
            img_kdp = img_kdp.resize((new_w, new_h), Image.LANCZOS)
            left = (new_w - kdp_w) // 2
            img_kdp = img_kdp.crop((left, 0, left + kdp_w, kdp_h))
        else:
            new_w = kdp_w
            new_h = int(new_w / current_ratio)
            img_kdp = img_kdp.resize((new_w, new_h), Image.LANCZOS)
            top = (new_h - kdp_h) // 2
            img_kdp = img_kdp.crop((0, top, kdp_w, top + kdp_h))
        img_kdp.save(output_kdp, "JPEG", quality=95)
        v = Image.open(output_kdp)
        print(f"KDP: {output_kdp} ({v.size[0]}x{v.size[1]}) ratio={v.size[1]/v.size[0]:.2f}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Apply typography overlay to book cover")
    parser.add_argument("base_image", help="Path to base AI-generated image (no text)")
    parser.add_argument("output_png", help="Path for output PNG with typography")
    parser.add_argument("--title", nargs="+", required=True, help="Title lines")
    parser.add_argument("--book-num", type=int, required=True, help="Book number in series")
    parser.add_argument("--series", default="The Age of Lightships", help="Series name")
    parser.add_argument("--author", default="Bob J Mills", help="Author name")
    parser.add_argument("--output-kdp", default=None, help="Path for KDP JPEG export")
    parser.add_argument("--ratio", choices=["3:4", "2:3"], default="3:4", help="Aspect ratio")
    args = parser.parse_args()
    apply_typography(args.base_image, args.output_png, args.title, args.book_num,
                     args.series, args.author, args.output_kdp, args.ratio)
