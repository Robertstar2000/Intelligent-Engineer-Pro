# Cover Style Analysis — Pixel Extraction

Extract design parameters from an existing cover image to reproduce its style with a new title and different artwork.

## When to Use This

- User says "make it like [this existing cover]"
- User says "same style but with new title"
- You need to match an existing series' visual identity
- User provides a reference image (local file or URL)

## The Analysis Script

Save this as a reusable script or run inline. It works on any cover PNG.

```python
import numpy as np
from PIL import Image
from collections import Counter

def analyze_cover(path):
    img = Image.open(path).convert('RGB')
    arr = np.array(img)
    h, w, _ = arr.shape
    
    print(f"=== Cover Analysis: {path} ===")
    print(f"Dimensions: {w}×{h} (ratio {w/h:.2f})")
    
    # 1. BACKGROUND COLOR — dominant color in the image
    flat = arr.reshape(-1, 3)
    bg_color = tuple(Counter([tuple(p) for p in flat]).most_common(1)[0][0])
    print(f"\nBackground: RGB{bg_color}")
    
    # 2. SECONDARY COLORS — colors that appear >2% of pixels
    total = len(flat)
    color_counts = Counter([tuple(p) for p in flat])
    others = {c: n for c, n in color_counts.most_common(50) 
              if n > total * 0.02 and c != bg_color}
    if others:
        print(f"Secondary colors (>{2}% of pixels):")
        for c, n in sorted(others.items(), key=lambda x: -x[1]):
            print(f"  RGB{c}: {n/total*100:.1f}% — {n}px")
    
    # 3. TEXT REGIONS — find non-background bounding box
    bg = np.array(bg_color)
    mask = np.any(np.abs(arr.astype(int) - bg) > 20, axis=2)
    rows = np.any(mask, axis=1)
    cols = np.any(mask, axis=0)
    
    if rows.any():
        rmin, rmax = np.where(rows)[0][[0, -1]]
        cmin, cmax = np.where(cols)[0][[0, -1]]
        print(f"\nContent bounding box:")
        print(f"  Top:    y={rmin} ({100*rmin/h:.0f}% from top)")
        print(f"  Bottom: y={rmax} ({100*(h-rmax)/h:.0f}% from bottom)")
        print(f"  Left:   x={cmin} ({100*cmin/w:.0f}% from left)")
        print(f"  Right:  x={cmax} ({100*(w-cmax)/w:.0f}% from right)")
        print(f"  Width:  {cmax-cmin}px ({100*(cmax-cmin)/w:.0f}% of cover)")
        print(f"  Height: {rmax-rmin}px")
        
        # Height ratio of content zones
        third = h // 3
        zones = [
            ("Top third (title zone)", 0, third),
            ("Middle third (art)", third, 2*third),
            ("Bottom third (author)", 2*third, h),
        ]
        for label, y0, y1 in zones:
            zone_mask = mask[y0:y1, :]
            if zone_mask.any():
                pct = zone_mask.sum() / (zone_mask.shape[0] * zone_mask.shape[1]) * 100
                print(f"  {label}: {pct:.0f}% content coverage")
    
    # 4. WHITE TEXT placement
    white_mask = np.all(arr > 200, axis=2)
    white_rows = np.any(white_mask, axis=1)
    if white_rows.any():
        wrmin, wrmax = np.where(white_rows)[0][[0, -1]]
        print(f"\nWhite text band:")
        print(f"  y={wrmin}-{wrmax} ({100*wrmin/h:.0f}%-{100*wrmax/h:.0f}% from top)")
    
    # 5. COLORFUL / ACCENT regions
    # Look for pixels where one channel dominates
    accent = np.max(np.abs(arr.astype(int) - arr.mean(axis=2, keepdims=True)), axis=2) > 30
    if accent.any():
        accent_ys = np.where(np.any(accent, axis=1))[0]
        if len(accent_ys) > 0:
            print(f"\nAccent color region: y={accent_ys[0]}-{accent_ys[-1]}")
    
    print(f"\n=== End Analysis ===")

# Usage:
# analyze_cover('/home/bob/books/publishing_output/covers/The_Autonomous_Enterprise_Cover.png')
```

## Interpreting Results for Business/Minimalist Covers

A typography-heavy business cover (like "The Autonomous Enterprise") typically yields:

| Metric | Typical Value | Design Implication |
|--------|---------------|-------------------|
| Background | ~RGB(10,10,30) dark navy | Use same deep navy |
| Text content | Top 25-30% only | Title + subtitle in upper third |
| Content width | ~50-75% of cover | Centered with wide margins |
| White text band | y=24%-32% from top | Title sits in upper quarter |
| Accent colors | None or minimal gray only | Pure typography, no illustration |
| Bottom zone | Empty or small author bar | ~55px bar at bottom if present |

## Reproducing the Style

```python
# Constants from analysis
BG_COLOR = (10, 10, 30)        # extracted above
COVER_W, COVER_H = 1200, 1800  # 2:3 ratio
TITLE_Y_START = int(COVER_H * 0.24)  # match reference placement
CONTENT_WIDTH = int(COVER_W * 0.50)  # match reference margins

# Create canvas
canvas = Image.new('RGB', (COVER_W, COVER_H), BG_COLOR)

# Apply any gradient overlays from reference
# Then add new title typography (Step 4 of main skill)
# Then generate/place new artwork (Steps 2-3 of main skill)
```

## Example: The Autonomous Enterprise Cover

```
=== Cover Analysis: The_Autonomous_Enterprise_Cover.png ===
Dimensions: 1200×1800 (ratio 0.67)
Background: RGB(10, 10, 30)
Content bounding box:
  Top:    y=438 (24% from top)
  Bottom: y=1625 (10% from bottom)
  Left:   x=305 (25% from left)
  Right:  x=890 (26% from right)
  Width:  585px (49% of cover)
  Height: 1187px
White text band: y=438-574 (24%-32% from top)
```

**Design summary:** Dark navy background, centered content at ~50% width, title text in upper 25-32% region, no artwork, text-only design. The remaining content below (y=574-1625) is likely gray subtitle/body text.