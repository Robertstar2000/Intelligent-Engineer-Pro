# EPUB Spine Rebuild & Zip-Safe Modification Patterns

## Spine Corruption — Detection & Fix

### Symptom
Source EPUB spine contains `<itemref>` entries for images, and/or fewer chapter refs than the manifest has. Some EPUBs (notably Age of Lightships series) were exported with a broken spine that only lists ch01–ch09 plus image references — despite all 37+ chapters existing in the ZIP.

### Detection (Python)
```python
import re, zipfile

def check_spine(opf_text, expected_chapter_count):
    spine_match = re.search(r'<spine[^>]*>(.*?)</spine>', opf_text, re.DOTALL)
    if not spine_match:
        return False, "No spine found"
    spine_content = spine_match.group(1)
    refs = re.findall(r'idref="([^"]+)"', spine_content)
    
    has_image_refs = any('image' in ref.lower() for ref in refs)
    n_chapters = sum(1 for r in refs if r.startswith('ch'))
    
    if has_image_refs:
        return False, f"Spine contains image references: {refs}"
    if n_chapters < expected_chapter_count:
        return False, f"Spine has {n_chapters} chapters, expected {expected_chapter_count}"
    return True, "OK"
```

### Fix: Rebuild Spine from Manifest
When spine is broken, reconstruct it entirely from manifest item order:

```python
def rebuild_spine(opf_text):
    """Rebuild spine from manifest — front first, then all ch*.xhtml in order."""
    manifest_match = re.search(r'<manifest>(.*?)</manifest>', opf_text, re.DOTALL)
    items = re.findall(r'<item\s+id="([^"]+)"\s+href="([^"]+)"', manifest_match.group(1))
    
    spine_refs = []
    # front.xhtml first
    for item_id, href in items:
        if href == 'front.xhtml':
            spine_refs.append(item_id)
    # then all chapters in order
    for item_id, href in items:
        if re.match(r'ch\d+\.xhtml', href):
            spine_refs.append(item_id)
    
    spine_match = re.search(r'<spine[^>]*>(.*?)</spine>', opf_text, re.DOTALL)
    spine_attrs = re.search(r'<spine([^>]*)>', spine_match.group(0))
    attrs = spine_attrs.group(1) if spine_attrs else ' toc="ncx"'
    
    new_spine = f'<spine{attrs}>\n'
    for ref in spine_refs:
        new_spine += f'    <itemref idref="{ref}"/>\n'
    new_spine += '  </spine>'
    
    return opf_text[:spine_match.start()] + new_spine + opf_text[spine_match.end():]
```

## Safe In-Place EPUB Modification (Python zipfile)

### The Problem with unzip+rezip
Using shell `unzip` + file manipulation + `zip` can silently lose files (especially when chapter counts exceed 9 and file ordering differs). The AL book fix session lost ch10–ch37 because of this.

**NEVER open a zipfile for reading AND writing simultaneously** (`zipfile.ZipFile(path, 'r')` then `zipfile.ZipFile(path, 'w')` in the same block). This corrupts the file. Always read from source, write to a *different* output path.

### The Safe Pattern
Always use Python `zipfile` to read source and write destination in a single pass:

```python
import zipfile

with zipfile.ZipFile(source_path, 'r') as zin:
    with zipfile.ZipFile(output_path, 'w') as zout:  # Different path!
        for item in zin.infolist():
            data = zin.read(item.filename)
            
            # Replace images
            if item.filename.startswith("OEBPS/images/") and item.filename.endswith(".png"):
                new_img = os.path.join(images_dir, os.path.basename(item.filename))
                if os.path.exists(new_img):
                    with open(new_img, 'rb') as f:
                        data = f.read()
            
            # Fix text files
            if item.filename.endswith(('.xhtml', '.ncx', '.opf')):
                text = data.decode('utf-8')
                # ... apply fixes ...
                data = text.encode('utf-8')
            
            zout.writestr(item, data)
```

This preserves ALL files from the source EPUB regardless of count or naming.

## Duplicate Chapter Prefix — Complete Regex Fix

Source EPUBs may have these patterns in nav.xhtml, toc.ncx, and chapter `<h2>` headings:

**Same-number duplicates** (N === M):
- `"Chapter 1: Chapter 1: Title"` (double colon)
- `"Chapter 1: Chapter 1 — Title"` (colon + em-dash)

**Different-number duplicates** (N !== M) — common in renumbered series:
- `"Chapter 1: Chapter 31 — The Audit"` (LF Book 4: ch01 is actually Chapter 31)
- `"Chapter 27: Chapter 28: Recovery"` (AL Book 2: off-by-one from renumbering)
- `"Chapter 37: Chapter 39: Twenty Two"` (AL Book 2: gaps in numbering)

**Partial-fix artifacts**:
- `"Chapter 1 : Title"` (space-before-colon from earlier partial fix)

**The fix — keep the SECOND chapter number** (which is the real chapter number):

```python
def fix_duplicate_chapter(text):
    # "Chapter N: Chapter M: Title" -> "Chapter M: Title" (keep second = real number)
    text = re.sub(r'Chapter\s+\d+\s*:\s*(Chapter\s+\d+)\s*:\s*', r'\1: ', text)
    # "Chapter N: Chapter M — Title" -> "Chapter M — Title"
    text = re.sub(r'Chapter\s+\d+\s*:\s*(Chapter\s+\d+)\s*[—–-]\s*', r'\1 — ', text)
    # Normalize any remaining "Chapter N : " spacing
    text = re.sub(r'(Chapter\s+\d+)\s*:\s*', r'\1: ', text)
    return text
```

**CRITICAL**: The old regex `r'(Chapter\s+\d+):\s*\1:\s*'` only matched same-number patterns (N===M). The new regex drops the backreference and captures the second number instead, handling both same and different number cases.

Apply to ALL `.xhtml`, `.ncx`, and `.opf` files inside the EPUB.

## Bodymatter Landmark Auto-Add

Some source EPUBs (notably Age of Lightships) have landmarks nav but no `bodymatter` entry. Add it automatically:

```python
if 'bodymatter' not in nav_content:
    block = '''  <nav epub:type="landmarks">
    <h2>Landmarks</h2>
    <ol>
      <li><a epub:type="bodymatter" href="ch01.xhtml">Start Reading</a></li>
    </ol>
  </nav>'''
    nav_content = nav_content.replace('</body>', block + '\n</body>')
```

**Note**: Some source EPUBs (e.g., AL Book 3) have NO `front.xhtml` at all — the book starts directly with chapters. Don't add front matter that didn't exist; just ensure the spine is correct.

## Complete Rebuild Script Template

See `scripts/epub-rebuild.py` in the skill directory for the full production script that combines all of the above:
- Image replacement from external directory
- Spine rebuild from manifest
- Duplicate prefix fix across all text files
- Bodymatter landmark addition
- Safe zipfile in-place modification
