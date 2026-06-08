# Batch LLM Image Generation Pattern

## Use Case
Generating 40+ infographics and forms for a book using OpenRouter's image generation API (Gemini Flash Image).

## Script Pattern

Key requirements:
- **Sequential generation** (not parallel — shared API key, rate limits)
- **6-second delay** between requests to avoid 429 errors
- **Resume support** — skip existing files so re-runs don't re-generate
- **Retry logic** — 3 retries with exponential backoff on 429

```python
import subprocess, requests, base64, os, time
from io import BytesIO
from PIL import Image

def generate_image(prompt, output_path, retries=3):
    for attempt in range(retries):
        try:
            response = requests.post(URL, json=payload, headers=headers, timeout=120)
            if response.status_code == 429:
                time.sleep(15 * (attempt + 1))
                continue
            if response.status_code != 200:
                if attempt < retries - 1:
                    time.sleep(10)
                    continue
                return False
            # Decode base64 image from response
            img_url = response.json()["choices"][0]["message"]["images"][0]["image_url"]["url"]
            if img_url.startswith("data:image/png;base64,"):
                img_data = base64.b64decode(img_url.split(",", 1)[1])
            img = Image.open(BytesIO(img_data))
            img.save(output_path, "PNG")
            return True
        except Exception:
            if attempt < retries - 1:
                time.sleep(10)
    return False

# Task list: (filename, prompt, output_directory)
tasks = [
    ("ch01_name.png", "Professional business infographic...", infographics_dir),
    # ... 40+ more
]

for i, (fn, prompt, out_dir) in enumerate(tasks, 1):
    out_path = os.path.join(out_dir, fn)
    if os.path.exists(out_path) and os.path.getsize(out_path) > 1000:
        continue  # Resume support
    generate_image(prompt, out_path)
    if i < len(tasks):
        time.sleep(6)  # Rate limit delay
```

## Prompt Style for Business Infographics

Each prompt should include:
1. **What**: Description of the diagram/chart/visualization
2. **Layout**: Specific structure (2x2 matrix, horizontal timeline, flowchart, etc.)
3. **Data**: Key statistics or labels to include
4. **Style directive**: "clean modern infographic, labeled components, white background, professional color scheme, book-quality print-ready"

Example:
```
Professional business infographic showing a 2x2 risk matrix.
X-axis: 'Likelihood' (Low to High). Y-axis: 'Impact' (Low to High).
Four quadrants colored: Green (Accept), Yellow (Monitor), Orange (Mitigate), Red (Act Now).
Style: clean modern infographic, labeled components, white background, professional color scheme, book-quality print-ready.
```

## Model Priority
1. `google/gemini-2.5-flash-image` via OpenRouter (best quality)
2. `black-forest-labs/flux.2-max` (fallback)

## API Key
`OPENROUTER_API_KEY` from `~/.hermes/.env` — extract via bash subshell:
```python
result = subprocess.run(["bash", "-c", "source ~/.hermes/.env && echo $OPENROUTER_API_KEY"],
                       capture_output=True, text=True)
api_key = result.stdout.strip()
```
