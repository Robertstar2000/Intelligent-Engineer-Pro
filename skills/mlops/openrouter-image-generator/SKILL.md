---
name: openrouter-image-generator
version: 1.0.0
category: mlops
description: Generate images using OpenRouter's chat completions API with image-capable models.
---


## Memory context (Hindsight)

Long-term memory context is now provided automatically by Hindsight (bank
`mifeco-default`) on every turn — the retired MemPalace manual query step no
longer applies. Do NOT attempt to import `~/.hermes/mempalace` (it was removed
2026-08-19).This retrieves previous decisions, domain-specific context, and lessons learned from the vector memory store.

# OpenRouter Image Generator

A systematic approach for generating images using OpenRouter's chat completions API with image-capable models (Flux.2 Max, Flux.2 Pro, Flux.2 Flex, GPT-5.4 Image 2, etc.).

## Key Insight

OpenRouter's API does not have a dedicated image generation endpoint. Instead, image models return base64-encoded data URLs within the standard chat completion response structure.

## Workflow

### 1. API Setup
```python
import requests
import json
import re
import base64

# Load API key from environment
with open('/home/bob/.hermes/.env', 'r') as f:
    env_content = f.read()
match = re.search(r'OPENROUTER_API_KEY=([^#\n]+)', env_content)
if not match:
    raise Exception("Could not find OPENROUTER_API_KEY")
api_key = match.group(1).strip()
```

### 2. Image Generation Function
```python
def generate_image(model_id, prompt, output_path, max_attempts=3):
    """Generate an image using OpenRouter API and save to file."""
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": model_id,
        "messages": [{"role": "user", "content": prompt}],
        "stream": False
    }
    
    for attempt in range(max_attempts):
        try:
            response = requests.post(url, json=data, headers=headers, timeout=180)
            if response.status_code == 200:
                result = response.json()
                
                # Extract images from response
                if 'choices' in result and isinstance(result['choices'], list) and result['choices']:
                    for choice in result['choices']:
                        message = choice.get('message', {})
                        images = message.get('images', [])
                        
                        if images:
                            for img in images:
                                img_url = img.get('image_url', {}).get('url', '')
                                if img_url.startswith('data:image/png;base64,'):
                                    base64_data = img_url.split(',')[1]
                                    with open(output_path, 'wb') as f:
                                        f.write(base64.b64decode(base64_data))
                                    return True
            else:
                print(f"Error: {response.text[:200]}")
                
        except Exception as e:
            print(f"Attempt {attempt+1} failed: {e}")
    
    return False
```

### 3. Supported Models
- `black-forest-labs/flux.2-max` - Top-tier image quality, $0.07/Mpix first mp, $0.03 subsequent
- `black-forest-labs/flux.2-pro` - High-end quality, $0.03/Mpix
- `black-forest-labs/flux.2-flex` - Good quality, fast, $0.06/Mpix
- `openai/gpt-5.4-image-2` - Multimodal, $8/M input, $15/M output

### 4. Usage Patterns

#### Single Image Generation
```python
success = generate_image(
    model_id="black-forest-labs/flux.2-max",
    prompt="Book cover: Martian landscape with Valles Marineris colony...",
    output_path="/path/to/output.png"
)
```

#### Batch Generation with Retry Logic
```python
for i, (model, prompt, path) in enumerate(image_jobs):
    success = generate_image(model, prompt, path)
    if not success:
        print(f"Failed to generate image {i+1}")
```

### 5. Key Considerations

- **Base64 Data URLs**: Images are returned as `data:image/png;base64,<encoded_data>` within the `images` array
- **Response Structure**: Standard chat completion format with `choices` array containing `message` with `images` field
- **Timeout**: Use generous timeouts (120-180 seconds) as image generation can be slow
- **Retry Logic**: Implement retry with exponential backoff for transient failures
- **Model Selection**: Choose models based on quality vs speed vs cost trade-offs

### 6. Troubleshooting

**Issue**: `NoneType` object is not subscriptable
**Cause**: Attempting to access `result['choices']` when it's None
**Fix**: Check `isinstance(result['choices'], list)` before accessing

**Issue**: API returns 200 but no images found
**Cause**: Response structure differs from expected
**Fix**: Print full response for debugging

**Issue**: Base64 decode error
**Cause**: Invalid base64 data
**Fix**: Verify `img_url` starts with `data:image/png;base64,` before splitting

### 7. Cost Management

- Flux.2 Max: $0.07 per first megapixel, $0.03 per subsequent megapixel
- Flux.2 Pro: $0.03 per megapixel
- Flux.2 Flex: $0.06 per megapixel
- GPT-5.4 Image 2: $8/M input, $15/M output (expensive but high quality)

### 8. Best Practices

- Use appropriate model for task (Flux.2 Max for quality, Flux.2 Flex for speed)
- Implement proper error handling and retries
- Monitor API usage to avoid unexpected costs
- Consider image dimensions when calculating cost (first megapixel costs more)
- Test with small prompts before committing to large generation jobs

### 9. When to Use This Skill

- Generating book covers or other visual content via OpenRouter
- When you need to use specific image models available only on OpenRouter
- As an alternative to dedicated image generation APIs (Replicate, HuggingFace)
- When working with Flux.2 family models or GPT-4 Image generation

### 10. Limitations

- Only works with models that support image generation through chat completions
- Base64 data URLs can be large (limit ~5-10MB depending on OpenRouter's limits)
- No streaming support for image generation progress
- Rate limits apply (check OpenRouter documentation)
- Some models may return different response structures

### 11. Related Skills

- `ai-api-integration`: General AI API integration methodology
- `image-generation-workflow`: Broader image generation approaches
- `complex-task-orchestration`: For batch image generation workflows