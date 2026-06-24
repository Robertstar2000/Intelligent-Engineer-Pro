# Image Generation & TOC Extraction — Lessons Learned (2026-06-19)

## Gemini Image Generation via OpenRouter

### Response Format Change
The Gemini 2.5 Flash Image model via OpenRouter changed its response format. The image URL is now nested:

```python
# OLD format (no longer works):
img_data = images[0]["image_url"]  # Returns a string

# NEW format (current):
img_field = images[0]
img_url = img_field.get("image_url", "")  # Returns a dict
if isinstance(img_url, dict):
    img_url = img_url.get("url", "")  # Extract the actual URL string
```

The fix was applied to `step_images.py` `generate_image_gemini()` function.

### Image Generation Prompt Style
For B&W pencil sketch chapter images, use this prompt structure:
```
"{Scene description}. Black and white pencil sketch, fine detail cross-hatching, no color, no text, no letters, no words. Science fiction novel chapter illustration. Detailed, atmospheric, cinematic composition."
```

### Image Post-Processing
Generated images come at 1024×1024px. Resize to 440×439px at 150 DPI for print:
```python
from PIL import Image
img = Image.open(path)
img = img.resize((440, 439), Image.LANCZOS)
img.save(path, "PNG", dpi=(150, 150))
```

## TOC Page Number Extraction Fix

### Problem
The `_extract_toc_pages()` function in `step_pdf.py` was matching TOC page entries (short lines with page numbers) instead of actual chapter headings.

### Solution
Check that the line AFTER the chapter heading is body text (long, starts with a letter) rather than a page number (short, starts with a digit):

```python
for page_idx in range(4, len(doc)):  # Start after front matter
    text = doc[page_idx].get_text()
    if search_text in text:
        lines = text.split('\n')
        for li, line in enumerate(lines):
            if search_text in line:
                next_text = ''
                for nli in range(li + 1, min(li + 3, len(lines))):
                    stripped = lines[nli].strip()
                    if stripped:
                        next_text = stripped
                        break
                # Body text: long, starts with letter
                # TOC page number: short, starts with digit
                if next_text and len(next_text) > 15 and not next_text[0].isdigit():
                    found_page = page_idx + 1
                    break
```

### Key Insight
Start the search at page index 4 (page 5) to skip the front matter and TOC pages. The actual chapter content always has the heading followed by paragraph text, while TOC entries have the heading followed by a page number.
