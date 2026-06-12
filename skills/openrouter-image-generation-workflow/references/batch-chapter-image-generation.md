# Batch Chapter Image Generation Script Template

Reusable template for generating B&W pencil sketch images for every chapter of every fiction book.

## Script Structure

```python
#!/usr/bin/env python3
"""Batch generate B&W pencil sketch images for fiction books."""
import subprocess, requests, base64, time, os, re
from io import BytesIO
from PIL import Image

# 1. API Setup
result = subprocess.run(["bash", "-c", "source ~/.hermes/.env && echo $GOOGLE_AI_STUDIO_KEY"],
                       capture_output=True, text=True)
api_key = result.stdout.strip()
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image:generateContent?key={api_key}"

# 2. Book list — define paths and chapter patterns
FICTION_BOOKS = [
    # (book_path, chapter_pattern_regex)
    # Example: ("/path/to/book", r"^# Chapter \\d+[\\.\\d]*[:—]"),
]

# 3. Generate function
def generate_image(prompt, output_path, retries=3):
    full_prompt = f"{prompt} Style: black and white pencil sketch, cross-hatching, dramatic lighting, no color, book illustration quality."
    for attempt in range(retries):
        try:
            resp = requests.post(API_URL, json={
                "contents": [{"parts": [{"text": full_prompt}]}],
                "generationConfig": {"temperature": 0.9}
            }, headers={"Content-Type": "application/json"}, timeout=90)
            if resp.status_code != 200:
                time.sleep(10); continue
            parts = resp.json().get("candidates", [{}])[0].get("content", {}).get("parts", [])
            img_data = None
            for p in parts:
                if "inlineData" in p:
                    img_data = base64.b64decode(p["inlineData"]["data"])
                    break
            if img_data:
                img = Image.open(BytesIO(img_data))
                img.thumbnail((600, 600), Image.LANCZOS)
                # Center-crop to square
                if img.size[0] != img.size[1]:
                    sz = min(img.size)
                    left = (img.size[0] - sz) // 2
                    top = (img.size[1] - sz) // 2
                    img = img.crop((left, top, left+sz, top+sz))
                img.save(output_path, "PNG", optimize=True)
                return True
            time.sleep(10)
        except Exception as e:
            print(f"  Error: {e}")
            time.sleep(10)
    return False

# 4. Main loop
for book_path, ch_pattern in FICTION_BOOKS:
    manuscript = f"{book_path}/MANUSCRIPT.md"
    if not os.path.exists(manuscript):
        continue
    
    img_dir = f"{book_path}/chapter_images"
    os.makedirs(img_dir, exist_ok=True)
    
    with open(manuscript) as f:
        content = f.read()
    
    chapters = re.findall(ch_pattern, content, re.MULTILINE)
    
    for idx, ch_line in enumerate(chapters, 1):
        img_path = f"{img_dir}/ch{idx:02d}.png"
        if os.path.exists(img_path):
            continue
        
        # Create scene-specific prompt
        title = ch_line.strip()  # Clean chapter title
        # ... generate prompt based on title keywords ...
        
        success = generate_image(prompt, img_path)
        if success:
            # Insert image reference
            img_ref = f"chapter_images/ch{idx:02d}.png"
            content = content.replace(ch_line, f"{ch_line}\\n\\n![]({img_ref})", 1)
        
        time.sleep(6)  # Rate limit
    
    with open(manuscript, "w") as f:
        f.write(content)
```

## Chapter Format Pre-processing

Run these BEFORE the batch for books with formatting issues:

### Fix inline markers
```python
content = re.sub(r'[\\.\"\'\\—]{1,3}\\s*#+ (Chapter \\d+[\\.\\d]*[:—])', r'\\1\\n# \\2', content)
```

### Fix double-hash headers
```python
content = re.sub(r'^## (Chapter \\d+)', r'# \\1', content, flags=re.MULTILINE)
```

### Renumber non-sequential chapters
```python
lines = content.split("\\n")
new_lines = []
ch_count = 0
for line in lines:
    m = re.match(r'^# Chapter \\d+[\\.\\d]*: (.+)$', line)
    if m:
        ch_count += 1
        new_lines.append(f"# Chapter {ch_count}: {m.group(1)}")
    else:
        new_lines.append(line)
```

## Known Book Formats

| Format Pattern | Books Using It |
|----------------|----------------|
| `# Chapter N: Title` | AoLS series (Sunward Exodus, Mercury Accord, Ghosts, Last Photon) |
| `## Chapter N — Title` | Lunar Foundation series |
| `# Chapter N — Title` (em dash, single hash) | No Blue Sky series |
| Mixed/inline markers | Ghosts Beyond Neptune (fixed), older manuscripts |
| No chapter headers at all | Some legacy manuscripts — must extract from content |

## Scene Prompt Keywords by Genre

**Sci-Fi (Space/Ships):** ship, fleet, orbit, launch, engine, module, moon, lunar, planet, mars, martian, dome, oxygen, water, ice, signal, transmission, array, communications

**Sci-Fi (Conflict/Tension):** sabotage, uprising, confession, fracture, vote, council, meeting, charter, assembly, accord, loss, dead, sacrifice, fail, break

**Cozy Mystery:** law office, small town, courtroom, evidence, clue, investigation, interview, witness, judge, jury

**Memoir:** reflective, personal, memory, contemplative, family, childhood, home

## Key Parameters

- **Image size:** 600x600 pixels (2x2 inches at 300dpi)
- **Rate limit:** 6 seconds between API calls
- **Temperature:** 0.9 (higher = more creative variation)
- **Retries:** 3 per image, 10s backoff
- **Model:** google/gemini-2.5-flash-image (via Google AI Studio direct API)
- **Cost:** Approximately 1 request per image, ~$0 free tier for Gemini (typically 60+ images/minute free)
