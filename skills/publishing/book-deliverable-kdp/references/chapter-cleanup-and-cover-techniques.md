# Chapter Cleanup Reference

## Common Issues in AI-Generated Chapters

### 1. Duplicate Paragraphs
Entire `<p>` blocks appearing twice in the same chapter. Common when AI generates multiple drafts that get concatenated.

Detection: Extract all `<p...>...</p>` blocks, compare cleaned text content, flag second occurrences of blocks >30 chars.

Fix: Remove duplicates in reverse position order to preserve offsets:
```python
paras = list(re.finditer(r'<p[^>]*>.*?</p>', content, re.DOTALL))
seen = {}
to_remove = []
for m in paras:
    clean = re.sub(r'<[^>]+>', '', m.group(0)).strip()
    clean = re.sub(r'\s+', ' ', clean)
    if len(clean) > 30 and clean in seen:
        to_remove.append((m.start(), m.end()))
    else:
        seen[clean] = True
for start, end in reversed(to_remove):
    content = content[:start] + content[end:]
```

### 2. Double Scene Breaks
`<p class="scene">* * *</p><p class="scene">* * *</p>` always wrong. Fix with simple string replace BEFORE other edits.

### 3. Mixed Em-dash Formats
Normalize all `&mdash;` to unicode `—`. Also replace ` -- ` with ` — `.

### 4. Mismatched Paragraph Tags
After removing duplicates, always verify:
```python
opens = len(re.findall(r'<p[\s>]', content))
closes = len(re.findall(r'</p>', content))
```
If mismatched, find the affected line and add missing `</p>` at line end.

## Cover Generation Reference

### Gemini Image Generation (OpenRouter)
- Correct model name: `google/gemini-2.5-flash-image`
- DO NOT use `google/gemini-2.5-flash-image-preview` (returns 404 on OpenRouter)
- Returns base64 PNG in `choices[0].message.images[0].image_url.url`

### Cover Text Compositing (PIL)
- KDP size: 2560x1600 (1.6:1)
- Title (2 words, single line): Liberation Sans Bold 200pt → ~71% page width
- Author name: Liberation Sans Bold 255pt → ~53% page width
- Always add dark gradient overlay behind text for high contrast
- Shadow offset: 3-4px black behind white text

### Marketing Infographic Generation
- Use same Gemini model for background art
- Composite QR codes with PIL `paste()` (not visual design, just placement)
- `qrcode` library installed at system level
- Output: PNG, 1080x1350 or 1024x1280 (4:5 ratio)
