#!/usr/bin/env python3
"""
generate_infographic_v2.py
Professional marketing infographics for The Cindy Lou Legal Capers series.
Generates 4 formats: Portrait (1080x1350), Square (1080x1080),
Landscape (1200x628), Story (1080x1920).

All QR codes are embedded as scannable images with URL labels.
Usage: python3 generate_infographic_v2.py
"""

from PIL import Image, ImageDraw, ImageFont
import os, shutil

# ── Paths ───────────────────────────────────────────────────────────
OUTPUT_DIR    = "/home/bob/cindy-lou-series/outputs"
QR_MIFECO     = "/home/bob/cindy-lou-series/qr_mifeco.png"
QR_AMAZON     = "/home/bob/cindy-lou-series/qr_amazon.png"
FONT_BOLD     = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG      = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_SERIF    = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
FONT_SERIF_B  = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"

# ── Colors ──────────────────────────────────────────────────────────
NAVY      = (25, 25, 50)
GOLD      = (212, 165, 84)
WHITE     = (255, 255, 255)
CREAM     = (245, 235, 210)
GRAY      = (200, 202, 220)
DARK_GRAY = (100, 102, 120)

os.makedirs(OUTPUT_DIR, exist_ok=True)

def fnt(path, size):
    try: return ImageFont.truetype(path, size)
    except: return ImageFont.load_default()

def center(draw, y, text, font, fill, W):
    bb = draw.textbbox((0, 0), text, font=font)
    tw = bb[2] - bb[0]
    draw.text(((W - tw) // 2, y), text, fill=fill, font=font)
    return bb[3] - bb[1]

def wrap(text, font, max_w, draw):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        test = (cur + " " + w).strip()
        bb = draw.textbbox((0, 0), test, font=font)
        if bb[2] - bb[0] > max_w and cur:
            lines.append(cur); cur = w
        else:
            cur = test
    if cur: lines.append(cur)
    return lines

def gradient(W, H, c1, c2):
    img = Image.new('RGB', (W, H))
    d = ImageDraw.Draw(img)
    for y in range(H):
        t = y / H
        d.line([(0,y),(W,y)], fill=tuple(int(c1[i]+(c2[i]-c1[i])*t) for i in range(3)))
    return img

def rounded(draw, xy, r, fill, outline=None, ow=2):
    draw.rounded_rectangle(xy, radius=r, fill=fill, outline=outline, width=ow)

def qr_block(qr_path, url, ursize, pad, url_font):
    if not os.path.exists(qr_path): return None
    qr = Image.open(qr_path).resize((ursize, ursize), Image.NEAREST)
    bg = Image.new('RGB', (ursize+pad*2, ursize+pad*2+36), WHITE)
    bg.paste(qr, (pad, pad))
    bd = ImageDraw.Draw(bg)
    rounded(bd, [0,0,bg.width-1,ursize+pad-1], 6, None, outline=GOLD, ow=1)
    bb = bd.textbbox((0,0), url, font=url_font)
    tw = bb[2]-bb[0]
    bd.text(((bg.width-tw)//2, ursize+pad+4), url, fill=NAVY, font=url_font)
    return bg

def qr_pair(img, y, W, ursize=200, pad=12, gap=80):
    uf = fnt(FONT_BOLD, 18)
    qm = qr_block(QR_MIFECO, "books.mifeco.com", ursize, pad, uf)
    qa = qr_block(QR_AMAZON, "amazon.com/s?k=bob+j+mills", ursize, pad, uf)
    if not qm or not qa: return 0
    total = qm.width + gap + qa.width
    x0 = (W - total) // 2
    img.paste(qm, (x0, y))
    img.paste(qa, (x0 + qm.width + gap, y))
    return max(qm.height, qa.height)

def gen_portrait():
    W, H = 1080, 1350
    img = gradient(W, H, NAVY, (42, 42, 72))
    d = ImageDraw.Draw(img)
    d.rectangle([15,15,W-15,H-15], outline=GOLD, width=2)
    d.rectangle([22,22,W-22,H-22], outline=(90,90,120), width=1)
    y = 30
    d.rectangle([40,y,W-40,y+48], fill=GOLD)
    center(d, y+10, "A ROMANTIC LEGAL MYSTERY SERIES", fnt(FONT_BOLD,24), NAVY, W)
    y += 62
    for line in ["THE CINDY LOU", "LEGAL CAPERS"]:
        h = center(d, y, line, fnt(FONT_BOLD,62), WHITE, W); y += h+4
    y += 15
    sl = wrap("She passed the bar. Nobody said anything about survival.", fnt(FONT_SERIF_B,34), W-120, d)
    for line in sl:
        h = center(d, y, line, fnt(FONT_SERIF_B,34), GOLD, W); y += h+4
    y += 22
    d.line([(W//2-80,y),(W//2+80,y)], fill=GOLD, width=1)
    d.polygon([(W//2,y-5),(W//2+7,y+4),(W//2-7,y+4)], fill=GOLD)
    y += 14
    for b in ["Book 1: Retainer to Trouble","Book 2: Clause for Alarm","Book 3: Affidavits and Alibis"]:
        bx = W//2-220
        d.polygon([(bx,y+10),(bx+8,y+18),(bx+16,y+10),(bx+8,y+2)], fill=GOLD)
        d.text((bx+22,y), b, fill=WHITE, font=fnt(FONT_BOLD,32))
        bb = d.textbbox((0,0), b, font=fnt(FONT_BOLD,32))
        y += bb[3]-bb[1]+18
    y += 18
    h = center(d, y, "Two almost-boyfriends. One very bad idea.", fnt(FONT_SERIF_B,28), CREAM, W); y += h+8
    h = center(d, y, "Each book: 3 clients. 1 big conspiracy.", fnt(FONT_BOLD,22), GOLD, W); y += h+22
    d.line([(100,y),(W-100,y)], fill=(80,82,110), width=1); y += 18
    desc = "Cindy Lou is a brand-new solo lawyer in NYC with a forensic roommate, a polished stockbroker, a bike messenger, and a talent for finding trouble in the fine print."
    dl = wrap(desc, fnt(FONT_REG,22), W-160, d)
    ch = len(dl)*28+28
    rounded(d, [70,y-8,W-70,y-8+ch], 12, (35,35,65), outline=GOLD, ow=1)
    for i,line in enumerate(dl):
        center(d, y+6+i*28, line, fnt(FONT_REG,22), GRAY, W)
    y = y-8+ch+22
    h = center(d, y, "Available on Amazon Kindle & Paperback", fnt(FONT_BOLD,26), WHITE, W); y += h+8
    h = center(d, y, "SCAN TO EXPLORE", fnt(FONT_BOLD,20), GOLD, W); y += h+15
    band_y = H-258
    d.rectangle([0,band_y,W,H], fill=WHITE)
    d.rectangle([0,band_y,W,band_y+3], fill=GOLD)
    qr_y = band_y+14
    qh = qr_pair(img, qr_y, W, ursize=210, pad=12, gap=80)
    center(d, H-20, "© 2025 Bob J Mills. All rights reserved.", fnt(FONT_REG,13), DARK_GRAY, W)
    out = os.path.join(OUTPUT_DIR, "Marketing_Infographic_Portrait.png")
    img.save(out, 'PNG')
    print(f"  Portrait: {out} ({os.path.getsize(out)//1024}KB)")
    return img

def gen_square():
    W, H = 1080, 1080
    img = gradient(W, H, NAVY, (42,42,72))
    d = ImageDraw.Draw(img)
    d.rectangle([15,15,W-15,H-15], outline=GOLD, width=2)
    d.rectangle([22,22,W-22,H-22], outline=(90,90,120), width=1)
    y = 35
    d.rectangle([40,y,W-40,y+42], fill=GOLD)
    center(d, y+8, "A ROMANTIC LEGAL MYSTERY SERIES", fnt(FONT_BOLD,22), NAVY, W)
    y += 56
    for line in ["THE CINDY LOU","LEGAL CAPERS"]:
        h = center(d, y, line, fnt(FONT_BOLD,56), WHITE, W); y += h+4
    y += 10
    sl = wrap("She passed the bar. Nobody said anything about survival.", fnt(FONT_SERIF_B,28), W-100, d)
    for line in sl:
        h = center(d, y, line, fnt(FONT_SERIF_B,28), GOLD, W); y += h+3
    y += 16
    d.line([(W//2-60,y),(W//2+60,y)], fill=GOLD, width=1); y += 14
    for b in ["Book 1: Retainer to Trouble","Book 2: Clause for Alarm","Book 3: Affidavits and Alibis"]:
        bx = W//2-190
        d.polygon([(bx,y+8),(bx+7,y+15),(bx+14,y+8),(bx+7,y+1)], fill=GOLD)
        d.text((bx+18,y), b, fill=WHITE, font=fnt(FONT_BOLD,28))
        bb = d.textbbox((0,0), b, font=fnt(FONT_BOLD,28))
        y += bb[3]-bb[1]+14
    y += 14
    h = center(d, y, "Two almost-boyfriends. One very bad idea.", fnt(FONT_SERIF_B,24), CREAM, W); y += h+6
    h = center(d, y, "Each book: 3 clients. 1 big conspiracy.", fnt(FONT_BOLD,18), GOLD, W); y += h+14
    d.line([(100,y),(W-100,y)], fill=(80,82,110), width=1); y += 14
    h = center(d, y, "Available on Amazon  -  SCAN TO EXPLORE", fnt(FONT_BOLD,20), WHITE, W); y += h+8
    band_y = H-230
    d.rectangle([0,band_y,W,H], fill=WHITE)
    d.rectangle([0,band_y,W,band_y+3], fill=GOLD)
    qr_pair(img, band_y+10, W, ursize=170, pad=10, gap=60)
    center(d, H-16, "© 2025 Bob J Mills", fnt(FONT_REG,12), DARK_GRAY, W)
    out = os.path.join(OUTPUT_DIR, "Marketing_Infographic_Square.png")
    img.save(out, 'PNG')
    print(f"  Square:   {out} ({os.path.getsize(out)//1024}KB)")
    return img

def gen_landscape():
    W, H = 1200, 628
    img = gradient(W, H, NAVY, (42,42,72))
    d = ImageDraw.Draw(img)
    d.rectangle([12,12,W-12,H-12], outline=GOLD, width=2)
    lx, lx2 = 45, W//2-15
    y = 35
    d.rectangle([lx,y,lx+440,y+30], fill=GOLD)
    d.text((lx+8,y+5), "A ROMANTIC LEGAL MYSTERY SERIES", fill=NAVY, font=fnt(FONT_BOLD,17))
    y += 42
    for line in ["THE CINDY LOU","LEGAL CAPERS"]:
        bb = d.textbbox((0,0), line, font=fnt(FONT_BOLD,40))
        tw = bb[2]-bb[0]
        d.text((lx+(lx2-lx-tw)//2,y), line, fill=WHITE, font=fnt(FONT_BOLD,40))
        y += bb[3]-bb[1]+3
    y += 8
    for line in ["She passed the bar.","Nobody said anything about survival."]:
        bb = d.textbbox((0,0), line, font=fnt(FONT_SERIF_B,20))
        tw = bb[2]-bb[0]
        d.text((lx+(lx2-lx-tw)//2,y), line, fill=GOLD, font=fnt(FONT_SERIF_B,20))
        y += bb[3]-bb[1]+3
    y += 12
    for b in ["B1: Retainer to Trouble","B2: Clause for Alarm","B3: Affidavits and Alibis"]:
        d.text((lx+8,y), "◆ "+b, fill=WHITE, font=fnt(FONT_BOLD,17))
        bb = d.textbbox((0,0), "◆ "+b, font=fnt(FONT_BOLD,17))
        y += bb[3]-bb[1]+7
    y += 6
    txt = "Available on Amazon  -  SCAN TO EXPLORE"
    bb = d.textbbox((0,0), txt, font=fnt(FONT_BOLD,15))
    d.text((lx+(lx2-lx-bb[2]+bb[0])//2,y), txt, fill=GOLD, font=fnt(FONT_BOLD,15))
    d.rectangle([W//2,25,W//2+2,H-25], fill=GOLD)
    rx = W//2+30
    ry = 45
    center_txt = "SCAN TO EXPLORE"
    bb = d.textbbox((0,0), center_txt, font=fnt(FONT_BOLD,22))
    d.text((rx+(W-20-rx-bb[2]+bb[0])//2,ry), center_txt, fill=GOLD, font=fnt(FONT_BOLD,22))
    ry += bb[3]-bb[1]+18
    qr_uf = fnt(FONT_BOLD,13)
    qm = qr_block(QR_MIFECO, "books.mifeco.com", 160, 8, qr_uf)
    qa = qr_block(QR_AMAZON, "amazon.com/s?k=bob+j+mills", 160, 8, qr_uf)
    if qm and qa:
        total = qm.width+40+qa.width
        qx = rx + ((W-20-rx)-total)//2
        img.paste(qm, (qx, ry))
        img.paste(qa, (qx+qm.width+40, ry))
    center(d, H-16, "© 2025 Bob J Mills", fnt(FONT_REG,11), DARK_GRAY, W)
    out = os.path.join(OUTPUT_DIR, "Marketing_Infographic_Landscape.png")
    img.save(out, 'PNG')
    print(f"  Landscape:{out} ({os.path.getsize(out)//1024}KB)")
    return img

def gen_story():
    W, H = 1080, 1920
    img = gradient(W, H, NAVY, (42,42,72))
    d = ImageDraw.Draw(img)
    d.rectangle([15,15,W-15,H-15], outline=GOLD, width=2)
    d.rectangle([22,22,W-22,H-22], outline=(90,90,120), width=1)
    y = 80
    d.rectangle([40,y,W-40,y+50], fill=GOLD)
    center(d, y+10, "A ROMANTIC LEGAL MYSTERY SERIES", fnt(FONT_BOLD,26), NAVY, W)
    y += 68
    for line in ["THE CINDY LOU","LEGAL CAPERS"]:
        h = center(d, y, line, fnt(FONT_BOLD,72), WHITE, W); y += h+5
    y += 18
    for line in ["She passed the bar.","Nobody said anything","about survival."]:
        h = center(d, y, line, fnt(FONT_SERIF_B,38), GOLD, W); y += h+4
    y += 30
    d.line([(W//2-100,y),(W//2+100,y)], fill=GOLD, width=2)
    d.polygon([(W//2,y-6),(W//2+8,y+5),(W//2-8,y+5)], fill=GOLD)
    y += 22
    for b in ["Book 1: Retainer to Trouble","Book 2: Clause for Alarm","Book 3: Affidavits and Alibis"]:
        bx = W//2-250
        d.polygon([(bx,y+10),(bx+9,y+19),(bx+18,y+10),(bx+9,y+1)], fill=GOLD)
        d.text((bx+25,y), b, fill=WHITE, font=fnt(FONT_BOLD,36))
        bb = d.textbbox((0,0), b, font=fnt(FONT_BOLD,36))
        y += bb[3]-bb[1]+22
    y += 25
    h = center(d, y, "Two almost-boyfriends.", fnt(FONT_SERIF_B,32), CREAM, W); y += h+5
    h = center(d, y, "One very bad idea.", fnt(FONT_SERIF_B,32), CREAM, W); y += h+10
    h = center(d, y, "Each book: 3 clients. 1 big conspiracy.", fnt(FONT_BOLD,24), GOLD, W); y += h+26
    d.line([(100,y),(W-100,y)], fill=(80,82,110), width=1); y += 22
    desc = "Cindy Lou is a brand-new solo lawyer in NYC with a forensic roommate, a polished stockbroker, a bike messenger, and a talent for finding trouble in the fine print."
    dl = wrap(desc, fnt(FONT_REG,26), W-140, d)
    ch = len(dl)*34+24
    rounded(d, [65,y-5,W-65,y-5+ch], 14, (35,35,65), outline=GOLD, ow=1)
    for i,line in enumerate(dl):
        center(d, y+6+i*34, line, fnt(FONT_REG,26), GRAY, W)
    y = y-5+ch+26
    h = center(d, y, "Available on Amazon Kindle & Paperback", fnt(FONT_BOLD,28), WHITE, W); y += h+10
    h = center(d, y, "SCAN TO EXPLORE", fnt(FONT_BOLD,24), GOLD, W); y += h+18
    band_y = H-305
    d.rectangle([0,band_y,W,H], fill=WHITE)
    d.rectangle([0,band_y,W,band_y+3], fill=GOLD)
    qr_pair(img, band_y+16, W, ursize=210, pad=12, gap=80)
    center(d, H-20, "© 2025 Bob J Mills. All rights reserved.", fnt(FONT_REG,14), DARK_GRAY, W)
    out = os.path.join(OUTPUT_DIR, "Marketing_Infographic_Story.png")
    img.save(out, 'PNG')
    print(f"  Story:    {out} ({os.path.getsize(out)//1024}KB)")
    return img

if __name__ == "__main__":
    print("CINDY LOU LEGAL CAPERS - Marketing Infographics v2")
    gen_portrait()
    gen_square()
    gen_landscape()
    gen_story()
    main = "/home/bob/cindy-lou-series/Marketing_Infographic.png"
    shutil.copy2(os.path.join(OUTPUT_DIR,"Marketing_Infographic_Portrait.png"), main)
    print(f"Main -> {main}")
    for kd in [
        "/home/bob/cindy-lou-series/kdp-packages/Retainer_to_Trouble/Marketing_and_Compliance",
        "/home/bob/cindy-lou-series/kdp-packages/Clause_for_Alarm/Marketing_and_Compliance",
        "/home/bob/cindy-lou-series/kdp-packages/Affidavits_and_Alibis/Marketing_and_Compliance",
    ]:
        os.makedirs(kd, exist_ok=True)
        for fn in os.listdir(OUTPUT_DIR):
            shutil.copy2(os.path.join(OUTPUT_DIR,fn), os.path.join(kd,fn))
        print(f"KDP -> {kd}")
    print("Done!")
