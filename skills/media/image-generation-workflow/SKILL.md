---
name: image-generation-workflow
description: Workflow for generating AI images in Hermes
version: 2.1.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [image, ai, generation, workflow]
    homepage: https://github.com/NousResearch/hermes-agent
---


## Memory context (Hindsight)

Long-term memory context is now provided automatically by Hindsight (bank
`mifeco-default`) on every turn — the retired MemPalace manual query step no
longer applies. Do NOT attempt to import `~/.hermes/mempalace` (it was removed
2026-08-19).This retrieves previous decisions, domain-specific context, and lessons learned from the vector memory store.

# AI Image Generation Workflow

> **Note:** Image generation is done via Python scripts calling Gemini/Flux APIs directly. Codex (the coding agent CLI) can WRITE the Python scripts but cannot run them in its read-only sandbox — copy the generated code to the host and run it there. Use the scripts and patterns below for the actual image generation.

This skill provides approaches for generating AI images in Hermes.

## Preferred Method: Gemini 2.5 Flash Image via OpenRouter

**Best for:** Book covers, artistic backgrounds, non-text images, concept art.

> ⚠️ **CRITICAL LIMITATIONS (discovered 2026-06-02):**
> - Gemini 2.5 Flash Image **always generates 1024x1024 square** regardless of requested aspect ratio (1080x1350, etc.)
> - Gemini **always bakes text into images** even when explicitly asked not to ("NO TEXT" in prompt is ignored)
> - Text rendered by Gemini is often garbled, misspelled, or incorrectly positioned
> - **DO NOT use Gemini for infographics requiring precise text, QR codes, or specific aspect ratios**
> - For infographics with text/QR codes: use HTML/CSS → WeasyPrint (see Infographic Composition Pattern below)

```python
import requests, json, re, base64, os

with open('/home/bob/.hermes/.env', 'r') as f:
    env_content = f.read()
match = re.search(r'OPENROUTER_API_KEY=([^#\n]+)', env_content)
api_key = match.group(1).strip()

def generate_image(prompt, output_path, model="google/gemini-2.5-flash-image"):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    data = {"model": model, "messages": [{"role": "user", "content": prompt}], "stream": False}
    for attempt in range(3):
        try:
            resp = requests.post(url, json=data, headers=headers, timeout=300)
            if resp.status_code == 200:
                result = resp.json()
                for choice in result.get('choices', []):
                    for img in choice.get('message', {}).get('images', []):
                        iu = img.get('image_url', {}).get('url', '')
                        if iu.startswith('data:image/png;base64,'):
                            with open(output_path, 'wb') as f:
                                f.write(base64.b64decode(iu.split(',')[1]))
                            return os.path.getsize(output_path)
            else:
                print(f"HTTP {resp.status_code}: {resp.text[:200]}")
        except Exception as e:
            print(f"Attempt {attempt+1}: {e}")
    return 0
```

### Prompting for Infographics
- **For backgrounds only** (text will be added via PIL/HTML): specify "NO TEXT — just visual design elements"
- Specify layout zones: "TOP SECTION (75%): [content]. BOTTOM SECTION (25%): clean dark background"
- Specify font sizes for the text overlay plan: "title in white 56px font", "body text 28px", etc.
- Request high contrast for mobile readability
- Include series-specific color schemes with hex codes
- **DO NOT rely on Gemini for final infographic with text** — use it for backgrounds only, then composite with PIL or HTML/CSS

### Social Media Font Size Standards
- Title: 56-72px (must be readable at phone thumbnail)
- Subtitle: 36-44px
- Headings: 32-40px
- Body: 24-32px
- Stats values: 48-64px
- Labels: 20-28px
- URLs: 16-20px
- NEVER smaller than 18px

## Infographic Composition: HTML/CSS → WeasyPrint (PREFERRED for 2026-06+)

**For infographics requiring precise text, QR codes, and professional layout:**

1. **Create HTML/CSS template** with the exact layout (two-column, sections, etc.)
2. **Embed images as base64** (book covers, QR codes, author photos)
3. **Render with WeasyPrint**: `HTML(string=html).write_pdf(pdf_path)`
4. **Convert PDF to image**: `pdftoppm -png -r 300 -singlefile pdf_path output`
5. **Resize to target**: 1080x1350 (portrait), 1080x1080 (square), etc.
6. **Save as JPEG** at quality=95

**Advantages over PIL:**
- Perfect text rendering (no font issues)
- CSS Grid/Flexbox for precise layout
- Professional typography with proper kerning
- Easy to iterate on design

**Advantages over Gemini:**
- Exact aspect ratio control
- Perfect text (no AI garbling)
- Scannable QR codes (not decorative)
- Reproducible results

**Template structure:**
```html
<!DOCTYPE html>
<html><head><style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { width: 1080px; height: 1350px; overflow: hidden; }
  .container { display: flex; width: 100%; height: 100%; }
  .left-col { width: 42%; background: #1C1C1C; }
  .right-col { width: 58%; background: #1A3B5F; border-left: 2px solid white; }
  /* ... section styling ... */
</style></head><body>
  <div class="container">
    <div class="left-col"><!-- Cover, reading order, author --></div>
    <div class="right-col"><!-- Framework, learn, for-you, quote, reviews --></div>
  </div>
  <div class="qr-band"><!-- QR codes --></div>
</body></html>
```

## Infographic Composition Pattern (PIL — Legacy)
1. Use PIL for full composition (NOT Gemini — Gemini returns 1024x1024, not requested aspect ratio; QR codes are decorative not scannable)
2. Generate QR codes with qrcode library, resize with `Image.NEAREST` (NEVER LANCZOS — blurs modules)
3. Output 4 formats: square (1080x1080), portrait (1080x1350), landscape (1200x628), story (1080x1920)
4. QR codes: 160-220px, white card backgrounds, URL labels below in Navy bold
5. Include both: books.mifeco.com + amazon.com/s?k=bob+j+mills
6. White QR band: solid fill, gold separator line above — NO gradient bleed
## Infographic Composition Pattern
1. Use PIL for full composition (NOT Gemini — Gemini returns 1024x1024, not requested aspect ratio; QR codes are decorative not scannable)
2. Generate QR codes with qrcode library, resize with `Image.NEAREST` (NEVER LANCZOS — blurs modules)
3. Output 4 formats: square (1080x1080), portrait (1080x1350), landscape (1200x628), story (1080x1920)
4. QR codes: 160-220px, white card backgrounds, URL labels below in Navy bold
5. Include both: books.mifeco.com + amazon.com/s?k=bob+j+mills
6. White QR band: solid fill, gold separator line above — NO gradient bleed

### Reusable Scripts
- `scripts/generate_infographic_v2.py` — Full production script, generates all 4 series formats
- Run: `python3 scripts/generate_infographic_v2.py`

## References
- `references/infographic-composition.md` — Detailed compositing standards, color palette, pitfalls
- `references/gemini-image-generation.md` — Gemini API usage (best for backgrounds/art, NOT text/QR)

## Platform Targeting
- Business books: LinkedIn (professional design)
- Fiction books: Facebook, X, Bluesky, Instagram, TikTok (bold, colorful)
