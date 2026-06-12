---
name: openrouter-image-generation-workflow
description: Comprehensive workflow for generating images via OpenRouter API with Gemini Flash Image and Flux.2 models, including background processing, error handling, canvas manipulation, typography overlay, vision QA, and HTML integration. Includes pencil sketch illustration support for science fiction books.
version: 1.5.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [image_gen, openrouter, workflow, flux, background-processing]
    related_skills: [openrouter-image-generation, book-publishing]
---

## 🔍 MemPalace Query (MANDATORY FIRST STEP)
Before proceeding, query MemPalace for existing context:
```python
import sys, os; sys.path.insert(0, os.path.expanduser('~/.hermes/mempalace'))
import embed; embed.init_embedding(os.path.expanduser('~/.hermes/mempalace'))
results = embed.search_embeddings("image generation workflow OpenRouter Flux Gemini book cover infographic", k=5)
```
This retrieves previous decisions, domain-specific context, and lessons learned from the vector memory store.

# OpenRouter Image Generation Workflow

## When to Use This Workflow
[existing content...]

## ⚠️ PIL Image Processing Pitfalls

### `.thumbnail()` returns None — do NOT chain it
```python
# WRONG — .thumbnail() returns None, .save() fails:
Image.open(BytesIO(img_data)).thumbnail((600,600), Image.LANCZOS).save(path, "PNG")

# RIGHT — assign to variable first:
img = Image.open(BytesIO(img_data))
img.thumbnail((600,600), Image.LANCZOS)
img.save(path, "PNG", optimize=True)
```

### Gemini API response has text BEFORE inlineData
The Gemini Flash Image response includes a text part (part[0]) before the image part (part[1]). Always loop to find `inlineData`:
```python
parts = resp.json()["candidates"][0]["content"]["parts"]
img_data = None
for part in parts:
    if "inlineData" in part:
        img_data = base64.b64decode(part["inlineData"]["data"])
        break  # Important: break after finding first image
```

### 2x2 inch chapter images
At 300dpi, a 2x2 inch image = 600x600 pixels. Always center-crop to square:
```python
img.thumbnail((600, 600), Image.LANCZOS)
if img.size[0] != img.size[1]:
    sz = min(img.size)
    left = (img.size[0] - sz) // 2
    top = (img.size[1] - sz) // 2
    img = img.crop((left, top, left+sz, top+sz))
```

> ⚠️ **CRITICAL: Book covers and ALL infographics MUST be generated using an image generation LLM. Do NOT use Python/matplotlib for any published book visuals — covers OR interior images.**

## Cover Generation by Genre

### Science Fiction — Pencil Sketch Illustrations
Every sci-fi chapter gets one black & white pencil sketch depicting a scene from that chapter.

**Prompt template:**
```
Black and white pencil sketch illustration for a science fiction novel. [Scene]. Style: detailed pencil sketch, cross-hatching, no color, book illustration, dramatic lighting, cinematic composition. This must be completely original.
```

**API rate limit rules:**
- Minimum 5-6 second delay between requests
- If 429 error: wait 10 seconds, retry; if still failing, simplify prompt
- Do NOT run multiple subagents generating images concurrently (shared API key)

**Model priority:**
1. `google/gemini-2.5-flash-image` (best quality)
2. `black-forest-labs/flux.2-max` (fallback)

### Business / Non-Fiction — Infographics & Charts
**Use image generation LLM (NOT Python/matplotlib)** for all infographics, charts, diagrams, and data entry forms. This is a mandatory quality requirement — Python-generated infographics were identified as unacceptable for published books.

**Prompt template for business infographics:**
```
Professional infographic for a business book. [Description of data/concept to visualize]. Style: clean modern infographic, labeled components, data visualization, white or light background, professional typography, book-quality, print-ready.
```

**Prompt template for data entry forms:**
```
Printable business form for a business book. [Description of form]. Style: clean black and white form design, professional layout, labeled fields, checkbox grids, table structures with bordered cells, signature lines at bottom.
```

**API rate limit rules for infographics:**
- Minimum 5-6 second delay between requests
- If 429 error: wait 10 seconds, retry; if still failing, simplify prompt
- Do NOT run multiple subagents generating images concurrently (shared API key)

**Model priority:**
1. `google/gemini-2.5-flash-image` (best quality for infographics)
2. `black-forest-labs/flux.2-max` (fallback)

> ⚠️ **Vision QA requires a vision-capable model.** After generating images, you need to verify them visually. If the active model doesn't support image input (e.g., `nvidia/nemotron-3-super-120b-a12b:free` on OpenRouter returns 404 for images), you cannot use `vision_analyze` or browser vision. Workarounds: (1) switch to a vision-capable model like `google/gemini-2.5-flash`, (2) inspect images via `PIL` metadata (dimensions, color samples), or (3) send images to the user on Telegram and ask for visual feedback. See `hermes-model-configuration` skill for configuring a vision model.

## Batch Chapter Image Generation (Entire Book or Series)

When generating images for every chapter of every fiction book, use a Python script approach rather than one-at-a-time tool calls. The 6-second API rate limit makes manual generation impractical for 500+ chapters.

### Preprocessing: Fix Chapter Formatting FIRST

Before generating images, ensure every chapter in the MANUSCRIPT.md has a proper markdown heading (`# Chapter N: Title`). Common issues found in legacy manuscripts:

**1. Inline chapter markers (no line break before heading):**
```
end of paragraph.# Chapter 8: Ship 15 Gone
"some dialogue."# Chapter 10: Electromagnetic Theory
```
Fix with: `content = re.sub(r'[\\.\\"\\'\\—]{1,3}\\s*#+ (Chapter \\d+[\\.\\d]*[:—])', r'\\1\\n# \\2', content)`

**2. Double-hash headers (`##` instead of `#`):**
Fix: `content = re.sub(r'^## (Chapter \\d+)', r'# \\1', content, flags=re.MULTILINE)`

**3. Non-sequential chapter numbering:**
Renumber sequentially before generating images so filenames stay consistent.

**4. .5 chapters (interleaved half-chapters):**
Treat as separate chapters with their own image. They count toward the total.

### Google Gemini Direct API (Primary Approach)

The Google Gemini Flash Image model via the direct Google AI Studio API is more reliable than going through OpenRouter's proxy. The key lives in `~/.hermes/.env` as `GOOGLE_AI_STUDIO_KEY`.

**Endpoint (raw requests, NOT generative-ai SDK):**
```
POST https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image:generateContent?key={api_key}
```

**Payload:**
```python
payload = {
    "contents": [{"parts": [{"text": prompt}]}],
    "generationConfig": {"temperature": 0.9}
}
```

**Response:** `candidates[0].content.parts[]` where part[0] is text description and part[1] is `inlineData` (base64 PNG). Always loop through parts — never assume index.

### Book Cover as Seed for Series Chapter Images

For series like Cindy Lou where visual consistency matters, seed chapter prompts with the cover descriptor:
```
cover = "Cozy mystery: small law office, magnolia trees, warm small-town feel"
prompt = f"{cover} scene from chapter '{title}': [scene]. Style: B&W pencil sketch..."
```

### Execution Strategy

1. Run the batch script as a **background process** with `notify_on_complete=True`
2. Time budget: ~6 seconds per chapter at 6s rate limit. For 500+ chapters, budget 50-60 minutes
3. Handle books with non-standard formatting (No Blue Sky, Cindy Lou, Tomorrow Remembered) in separate fix scripts BEFORE the batch
4. Start with properly-formatted books first, then handle edge-cases

### Image Insertion Into MANUSCRIPT.md

After generating images, insert references at the start of each chapter:
```python
img_ref = f"chapter_images/ch{ch_num:02d}.png"
old = f"# Chapter {ch_num}: {title}"
content = content.replace(old, f"{old}\\n\\n![]({img_ref})", 1)
```

See `references/batch-chapter-image-generation.md` for the full reusable script template.

[rest of existing content...]