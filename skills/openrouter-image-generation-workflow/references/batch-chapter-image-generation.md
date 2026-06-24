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
    # Example: ("/path/to/book", r"^# Chapter \\d+[\\.:\\—]"),
]

# 3. Generate function
def generate_image(prompt, output_path, retries=3):
    full_prompt = f"{prompt} Style: black and white pencil sketch, cross-hatching, dramatic lighting, no color, book illustration quality."
    for attempt in range(retries):
        try:
            resp = requests.post(API_URL, json={
                "contents": [{"parts": [{"text": full_prompt}]}],
                "generationConfig": {"temperature": 0.9}
            }, headers={"Content-Type": "application/json"}, timeout=120)
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
```

## ⚠️ CRITICAL: Post-Generation B&W Conversion

**Gemini generates RGB images even when prompted for B&W.** The output PNGs have a warm brownish/sepia tint (R > G > B). You MUST convert to grayscale after generation:

```python
from PIL import Image
img = Image.open(path)
gray = img.convert('L').convert('RGB')  # Convert to grayscale, then back to RGB for PNG compatibility
gray.save(path, 'PNG', optimize=True)
```

Apply this to every image immediately after the batch generation loop completes. Verify with:
```python
pixels = list(img.getdata())
gray_count = sum(1 for p in pixels if p[0]==p[1]==p[2])
assert gray_count == len(pixels), "Image is not grayscale!"
```

## ⚠️ CRITICAL: EPUB OPF Structure

When building EPUBs, the OPF manifest **requires unique `id` attributes** across ALL items. A common bug is using `id="ch01"` for both the chapter XHTML and the image — this breaks EPUB validation.

**Correct pattern:**
```xml
<!-- Chapter XHTML -->
<item id="ch01" href="ch01.xhtml" media-type="application/xhtml+xml"/>
<!-- Image — use img- prefix to avoid collision -->
<item id="img-ch01" href="images/ch01.png" media-type="image/png"/>
```

**Spine must reference ALL chapters:**
```xml
<spine>
  <itemref idref="ch01"/>
  <itemref idref="ch02"/>
  <!-- ... every chapter must appear here -->
</spine>
```

**Chapter XHTML must be proper XHTML documents** (with DOCTYPE + html wrapper), not raw HTML body content.

**nav.xhtml must list ALL chapters** in the TOC, matching the spine.

## ⚠️ CRITICAL: WeasyPrint Image Embedding

**Data URIs (base64) do NOT work reliably with WeasyPrint.** Use absolute file paths instead:

```python
# Replace relative paths with absolute file paths
html_content = re.sub(r'src="([^"]*)"', lambda m: f'src="file://{os.path.join(images_dir, os.path.basename(m.group(1)))}"', html_content)
tmp_html = html_path + ".tmp"
with open(tmp_html, "w") as f:
    f.write(html_content)
HTML(filename=tmp_html, base_url=images_dir).write_pdf(pdf_path)
```

## ⚠️ CRITICAL: Duplicate Image References in HTML

Book HTML files often contain **two `<img>` tags per chapter** — one in a `<div class="chapter-image">` and one in a `<p>` tag:
```html
<div class="chapter-image"><img src="ch01.png" alt="Chapter 1" /></div>
<p><img src="chapter_images/ch01.png" alt="" /></p>
```

Before rebuilding PDF/EPUB, strip the duplicate `<p>` wrappers:
```python
content = re.sub(r'\s*<p><img src="chapter_images/[^"]*" alt=""\s*/>\s*', '\n', content)
content = re.sub(r'\s*<p><img src="[^"]*" alt=""\s*/>\s*', '\n', content)
```

## Chapter Format Pre-processing

Run these BEFORE the batch for books with formatting issues:

### Fix inline markers
```python
content = re.sub(r'[\\.\\"\\'\\—]{1,3}\\s*#+ (Chapter \\d+[\\.:\\—])', r'\\1\\n# \\2', content)
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
    m = re.match(r'^# Chapter \\d+[\\.:\\—]: (.+)$', line)
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
| `## Chapter N — Title` (double hash) | No Blue Sky Books 1-2, Lunar Foundation series |
| `# Chapter N — Title` (single hash, em dash) | No Blue Sky Books 3-5 |
| Mixed/inline markers | Ghosts Beyond Neptune (fixed), older manuscripts |
| No chapter headers at all | Some legacy manuscripts — must extract from content |

## No Blue Sky Series — Special Instructions

### Folder Structure
- `Book_N_Title/images/chXX.png` — **source of truth** (generate here)
- `Book_N_Title/images_bw/chXX.png` — greyscale variant (copy from images/)
- `Book_N_Title/output/chXX.png` — used by HTML output (copy from images/)
- `Book_N_Title/manuscript/MANUSCRIPT.md` — chapter headers live here

### Chapter Header Quirks
- Books 1-2 use `## Chapter N — Title` (double hash) — the batch script must normalize to single `#` before parsing
- Books 3-5 use `# Chapter N — Title` (single hash with em dash separator)
- Some chapters have `.5` suffix (e.g., `Chapter 9.5`) — treat as separate chapters

### Image Prompt Requirements (CRITICAL)
When generating for No Blue Sky, prompts MUST include:
1. **Real Mars terrain**: reddish-brown iron oxide regolith, impact craters, thin pale pink sky, rust-colored horizon — NOT grey moonscape
2. **Modern SpaceX-style astronauts**: sleek form-fitting suits, angular 3D-printed helmets, minimal bulk — NOT bulky Apollo-era suits
3. **Modern equipment**: clean solar arrays, contemporary habitats, advanced rovers — NOT retro-futuristic

See `references/mars-space-image-prompts.md` for the full prompt template and per-scene keyword mappings.

## Scene Prompt Keywords by Genre

**Sci-Fi (Space/Ships):** ship, fleet, orbit, launch, engine, module, moon, lunar, planet, mars, martian, dome, oxygen, water, ice, signal, transmission, array, communications

**Sci-Fi (Conflict/Tension):** sabotage, uprising, confession, fracture, vote, council, meeting, charter, assembly, accord, loss, dead, sacrifice, fail, break

**Cozy Mystery:** law office, small town, courtroom, evidence, clue, investigation, interview, witness, judge, jury

**Memoir:** reflective, personal, memory, contemplative, family, childhood, home

## Key Parameters

- **Image size:** 600x600 pixels (2x2 inches at 300dpi) — **resize to 460px max before embedding in PDF/EPUB**
- **Rate limit:** 6 seconds between API calls
- **Temperature:** 0.9 (higher = more creative variation)
- **Retries:** 3 per image, 10s backoff
- **Model:** google/gemini-2.5-flash-image (via Google AI Studio direct API)
- **Cost:** Approximately 1 request per image, ~$0 free tier for Gemini (typically 60+ images/minute free)

## ⚠️ CRITICAL: Image Sizing for Print PDF

**600px images DO NOT FIT in a 6×9" book with 0.5" margins.** At CSS 96dpi, 600px = 6.25" which exceeds the 5" content area.

**Always resize to 460px max before embedding:**
```python
from PIL import Image
img = Image.open(path)
if img.size[0] > 460:
    ratio = 460 / img.size[0]
    img = img.resize((460, int(img.size[1] * ratio)), Image.LANCZOS)
img.save(path, 'PNG', optimize=True)
```

**CSS for chapter images:**
```css
.chapter-image img { max-width: 480px; width: auto; height: auto; max-height: 400px; }
```

**Do NOT use `max-width: 100%`** — WeasyPrint interprets it relative to the image's intrinsic pixel width, not the CSS content box.

## ⚠️ CRITICAL: CSS Margin Pitfalls in Manuscripts

Manuscript HTML often has excessive margins that compound with page margins:

| Element | Common Bad Value | Fix To |
|---|---|---|
| `p` | `margin: 0.5in` | `margin: 0` |
| `.chapter-image` | `margin: 0.5in` | `margin: 0; padding: 0` |
| `.scene-break` | `margin: 0.5in` | `margin: 0` |

When `p { margin: 0.5in }` combines with `@page { margin: 0.5in }`, the effective margin becomes 1.0in, pushing images outside the content area.
