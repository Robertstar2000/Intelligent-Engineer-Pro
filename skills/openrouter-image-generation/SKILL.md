---
name: openrouter-image-generation
description: Generate images using OpenRouter's chat completions API with Black Forest Labs Flux.2 model
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: ["image_gen", "openrouter", "gemini", "ai"]
    related_skills: []
---

## Memory context (Hindsight)

Long-term memory context is now provided automatically by Hindsight (bank
`mifeco-default`) on every turn — the retired MemPalace manual query step no
longer applies. Do NOT attempt to import `~/.hermes/mempalace` (it was removed
2026-08-19).This retrieves previous decisions, domain-specific context, and lessons learned from the vector memory store.

# OpenRouter Image Generation Skill

This skill enables image generation through OpenRouter using Black Forest Labs Flux.2 model. It provides a programmatic way to create images for book covers, chapter sketches, and other visual content.

## Configuration

To use this skill, you need:
- An OpenRouter API key configured in your Hermes Agent settings
- The black-forest-labs/flux.2-max model available on OpenRouter

## Usage

Call the `generate_image(prompt, options)` function with your desired prompt and optional parameters.

## Example Prompts

### Book Cover
```
Create a professional book cover for the memoir "The Future is Unwritten" by Robert Mills.
The cover should feature:
- A vintage microphone with a subtle circuit board pattern in the background
- Warm, nostalgic color scheme with blues and golds
- Clean, elegant typography
- Space for the title and author name
- Style: Modern but with a classic feel, suitable for a memoir
- Aspect ratio: 2:3 (standard book cover)
```

### Chapter Sketch 1
```
A vintage microphone and electrical outlet, representing curiosity and discovery. 
Style: Black and white pencil sketch, hand-drawn, with shading and texture, suitable for a memoir chapter header.
```

### Chapter Sketch 2
```
A dog silhouette, representing companionship and loyalty.
Style: Black and white pencil sketch, hand-drawn, with shading and texture, suitable for a memoir chapter header.
```

## API Integration

This skill uses the OpenRouter API to generate images.

### Alternative: Google Gemini Direct API (More Reliable)

In some environments (including the MIFECO setup), the Google Gemini Flash Image model works more reliably via direct Google API than via OpenRouter. Use this when OpenRouter image generation fails or returns 401.

**Working pattern for Google Gemini Flash Image direct API:**

```python
import requests, json, base64, subprocess
from io import BytesIO
from PIL import Image

# Get the key from environment (sourced from .env)
result = subprocess.run(["bash", "-c", "source ~/.hermes/.env && echo $GOOGLE_AI_STUDIO_KEY"],
                       capture_output=True, text=True)
api_key = result.stdout.strip()

url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image:generateContent?key={api_key}"

payload = {
    "contents": [{"parts": [{"text": prompt}]}],
    "generationConfig": {"temperature": 1.0}
}

response = requests.post(url, json=payload, timeout=90)
if response.status_code == 200:
    parts = response.json()["candidates"][0]["content"]["parts"]
    img_data = None
    for part in parts:
        if "inlineData" in part:
            img_data = base64.b64decode(part["inlineData"]["data"])
    if img_data:
        img = Image.open(BytesIO(img_data))
```

**Key differences from OpenRouter path:**
- Uses direct Google API endpoint, not OpenRouter proxy
- API key goes in URL query string (`?key=...`), not Authorization header
- Response returns image as `inlineData` (base64), not as `image_url`
- No special headers needed beyond content-type
- The `google-generativeai` Python SDK does NOT work against OpenRouter — always use raw requests

### Working integration pattern for Gemini image models via OpenRouter

For `google/gemini-2.5-flash-image`, the reliable approach is to call the OpenRouter **chat completions** endpoint directly:

`https://openrouter.ai/api/v1/chat/completions`

Use a payload like:

```json
{
  "model": "google/gemini-2.5-flash-image",
  "messages": [
    {
      "role": "user",
      "content": [
        {"type": "text", "text": "YOUR IMAGE PROMPT HERE"}
      ]
    }
  ]
}
```

Important headers:

```http
Authorization: Bearer <OPENROUTER_API_KEY>
Content-Type: application/json
HTTP-Referer: https://hermes.local
X-Title: Hermes Memoir Image Generation
```

Successful responses place the generated image under:

```python
response_json["choices"][0]["message"]["images"][0]["image_url"]["url"]
```

For Gemini image responses, this URL may be a `data:image/png;base64,...` URI. Decode the base64 payload and write it to a `.png` file.

### Important experiential finding

Do **not** assume the Google GenAI SDK will work against OpenRouter by only overriding `base_url`. In practice, that produced 404 responses against OpenRouter's web app routes. Raw `requests.post()` to OpenRouter's `/chat/completions` endpoint worked reliably.

### Alternative: Google AI Studio Direct API

For Gemini image generation in this environment, the **Google AI Studio direct API** is more reliable than OpenRouter's Gemini proxy. The key is stored in `~/.hermes/.env` as `GOOGLE_AI_STUDIO_KEY` and is NOT exported as a regular env var — it must be extracted via bash subshell:

```python
import subprocess, requests, base64
from io import BytesIO
from PIL import Image

result = subprocess.run(["bash", "-c", "source ~/.hermes/.env && echo $GOOGLE_AI_STUDIO_KEY"],
                       capture_output=True, text=True)
api_key = result.stdout.strip()

url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image:generateContent?key={api_key}"

payload = {
    "contents": [{"parts": [{"text": prompt}]}],
    "generationConfig": {"temperature": 1.0}
}

response = requests.post(url, json=payload, timeout=90)

if response.status_code == 200:
    parts = response.json()["candidates"][0]["content"]["parts"]
    for part in parts:
        if "inlineData" in part:
            img_data = base64.b64decode(part["inlineData"]["data"])
            img = Image.open(BytesIO(img_data))
```

Use this approach when OpenRouter's Gemini endpoint is returning 401/403 or timing out.

## Parameters

- `prompt`: The text prompt describing the desired image
- `options`: Optional parameters including:
  - `num_images`: Number of images to generate (default: 1)
  - `size`: Image size (default: "512x512")
  - `style`: Artistic style (default: "realistic")
  - `negative_prompt`: Things to avoid in the image

## Error Handling

The skill includes error handling for:
- API connection issues
- Invalid API keys
- Model unavailability
- Rate limiting

## Memory Usage

The skill will remember successful prompts and configurations for future use.

## Safety

This skill should only be used for image generation tasks. The model is selected specifically for its image generation capabilities.