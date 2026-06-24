# B&W Image Conversion for Gemini-Generated Sketches

## Problem

Google Gemini Flash Image generates RGB PNGs even when prompted for "black and white pencil sketch." The output has a warm brownish/sepia tint (R > G > B) instead of true grayscale.

## Solution

Convert all generated images to grayscale immediately after the batch generation loop:

```python
from PIL import Image
import os, glob

for path in glob.glob("/path/to/images/*.png"):
    img = Image.open(path)
    gray = img.convert('L').convert('RGB')  # L = grayscale, then RGB for PNG compat
    gray.save(path, 'PNG', optimize=True)
```

## Verification

```python
img = Image.open(path)
pixels = list(img.getdata())
gray_count = sum(1 for p in pixels if isinstance(p, tuple) and p[0]==p[1]==p[2])
assert gray_count == len(pixels), f"Image {path} is not grayscale!"
```

All pixels should have R=G=B for a true grayscale image.
