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

[rest of existing content...]