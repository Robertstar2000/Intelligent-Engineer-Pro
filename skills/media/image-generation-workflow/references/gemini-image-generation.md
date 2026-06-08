# Gemini 2.5 Flash Image — Infographic Generation Reference

## Model
`google/gemini-2.5-flash-image` via OpenRouter

## API Pattern
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
        except Exception as e:
            print(f"Attempt {attempt+1}: {e}")
    return 0
```

## Prompting for Infographics
- Specify layout: "TOP SECTION (75%): [content]. BOTTOM SECTION (25%): clean dark background, NO TEXT — reserved for QR codes"
- Specify font sizes: "title in white 56px font", "body text 28px", "stat values 48px"
- Social media minimums: titles 56-72px, body 24-32px, NEVER below 18px
- Request high contrast for mobile readability
- Include series-specific sales pitch text in prompt
- Use hex color codes: "navy background RGB(15,25,55)", "accent orange #FF8C00"

## Social Media Font Size Standards (1080px wide)
- Title: 56-72px bold
- Subtitle: 36-44px
- Hook: 28-32px bold
- Stat values: 48-64px bold
- Stat labels: 22-28px
- Block headings: 32-40px bold
- Body text: 24-32px regular (NEVER below 24px)
- Labels/URLs: 18-22px

## Composition Pattern
1. Generate base art with Gemini (text baked in, bottom 25% clean)
2. Convert to RGBA: `art.convert('RGBA').resize((w,h), Image.LANCZOS)`
3. Add QR codes to bottom band: 160-220px, white cards, 10px padding
4. URL labels: 18-22px centered below each QR
5. Output 4 formats: square, portrait, landscape, story

## Platform Formats
- Square 1080x1080: Art 70%, QR band 30%
- Portrait 1080x1350: Art 55-60%, QR band 40-45%
- Landscape 1200x628: Split 50/50
- Story 1080x1920: Art 45%, QR band 55%
