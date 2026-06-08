# Infographics Grayscale Conversion

For business books, ALL infographics MUST be grayscale only (black, white, shades of gray). Remove all color while keeping content, data, and text unchanged.

## Why
- Business book print editions are typically B&W interior
- Color infographics lose meaning when printed in grayscale
- Consistent B&W design looks professional in print

## Conversion Recipe (Python)

```python
from PIL import Image, ImageOps, ImageEnhance

def convert_to_grayscale(input_path, output_path=None, contrast_boost=1.5):
    """Convert an infographic to high-contrast grayscale."""
    if output_path is None:
        output_path = input_path
    
    img = Image.open(input_path).convert('RGB')
    
    # Convert to grayscale
    gray = ImageOps.grayscale(img)
    
    # Boost contrast for readability
    enhancer = ImageEnhance.Contrast(gray)
    high_contrast = enhancer.enhance(contrast_boost)
    
    # Convert back to 3-channel RGB (still grayscale values)
    final = Image.merge('RGB', (high_contrast, high_contrast, high_contrast))
    final.save(output_path, 'PNG')
```

## Verification

```python
from PIL import Image

img = Image.open('infographic.png')
pix = img.load()
w, h = img.size
for x in range(0, w, 100):
    for y in range(0, h, 100):
        r, g, b = pix[x, y][:3]
        assert r == g == b, f"Pixel at ({x},{y}) has color: RGB({r},{g},{b})"
print("All sampled pixels are grayscale")
```

## Visual Quality Check
- Text must be clearly readable against its background after conversion
- If dark elements blend into background, increase contrast boost (try 1.5-2.0)
- If light elements wash out, decrease contrast boost
- Thin lines may disappear at low contrast — verify linework is visible