---
title: Manuscript Correction and Image Placement
name: manuscript-correction-and-image-placement
id: manuscript-correction-and-image-placement
tags: ["manuscript", "correction", "images", "html", "telegram", "book", "formatting"]
description: A systematic approach for identifying and fixing corrupted manuscripts, ensuring proper chapter image placement, and delivering corrected files via appropriate channels (Telegram media). This workflow handles alignment issues, missing images, structural gaps, and final verification.
---


## 🔍 MemPalace Query (MANDATORY FIRST STEP)
Before proceeding, query MemPalace for existing context:
```python
import sys, os; sys.path.insert(0, os.path.expanduser('~/.hermes/mempalace'))
import embed; embed.init_embedding(os.path.expanduser('~/.hermes/mempalace'))
results = embed.search_embeddings("manuscript correction image placement fix", k=5)
```
This retrieves previous decisions, domain-specific context, and lessons learned from the vector memory store.

# Manuscript Correction and Image Placement

## Overview
A systematic approach for identifying and fixing corrupted manuscripts, ensuring proper chapter image placement, and delivering corrected files via appropriate channels (Telegram media). This workflow handles alignment issues, missing images, structural gaps, and final verification.

## When to Use
- User reports manuscript file is corrupted or images are improperly placed
- Manuscript needs formatting corrections (alignment, structure)
- Chapter images are missing or misplaced
- Back cover or other structural elements are missing
- Need to generate missing images and deliver final file

## Prerequisites
- Manuscript file in HTML format
- Chapter images stored in `generated_images/` directory
- Access to image generation tools if images are missing
- Telegram integration for media delivery

## Step-by-Step Process

### 0. Diagnose the Source First — TOC Entry vs Body Header Confusion

When a Markdown file has `# Chapter X: Title` entries, they could be either:
- **Real chapter headers** — followed by body content (intended as structural dividers)
- **TOC entries** — listed inside a Table of Contents block with page numbers (e.g., `# Chapter 1: The Shock .................... 3`), NOT followed by body content

**Diagnostic check:** After the TOC block, search for actual content. If the only `# Chapter X` occurrences are inside a TOC block and the real content uses `##` or `###` subsections instead, then the Markdown needs chapter headers added, or you should use a different source.

**When chapter content exists from an HTML artifact:** If a previously generated HTML file (e.g., `PRINT_READY_v9.html`) already has all chapters properly split with embedded images, TOC, and correct structure, **use it as the direct source for PDF/EPUB** instead of re-splitting the broken Markdown. Extract images from base64 data URIs, split by DOM structure (heading classes like `.chapter`, `.cover`, `.toc`), and rebuild the final files directly.

### 0b. Choose a Single Source of Truth

When multiple manuscript variants exist (HTML and/or Markdown), **do not reconcile the broken outputs against each other in a loop**. First assess which file has the cleanest narrative structure and chapter boundaries. A previously built HTML that already has correct chapter splits, embedded images, and a TOC is often the best source — even if the Markdown was the "original".

**Revised order of trust:**
1. A known-good HTML artifact with verified chapter structure and embedded images
2. Clean, structured Markdown source with intact top-level chapter headings
3. Earlier compiled manuscript with coherent body text
4. Existing HTML without verified body structure (last resort)

**Practical rule:**
- If the Markdown has `# Chapter X:` entries only inside a TOC block (followed by page numbers, not body text) and the real content uses `##`/`###` subsections, stop patching the Markdown split algorithm — use a known-good HTML artifact instead, or add proper `# Chapter X:` headers to the Markdown body.
- Compare candidates by (1) counting how many chapter headers are followed by real body text, (2) checking for embedded images, (3) verifying the TOC reflects actual content order.

### 1. Assessment & Diagnosis
```python
# Read and parse the manuscript HTML
with open(manuscript_path, 'r') as f:
    content = f.read()
soup = BeautifulSoup(content, 'html.parser')

# Check for common issues:
# - Alignment: text-align: justify; vs text-align: left;
# - Missing chapter images (check <h3> elements)
# - Improper image placement (images not immediately after chapters)
# - Missing structural elements (back cover, page breaks)
# - Missing cover image
```

### 2. Fix Alignment Issues
```python
# Update CSS to change from justify to left alignment
style_tag = soup.find('style')
if style_tag and 'text-align: justify;' in style_tag.string:
    style_content = style_tag.string.replace('text-align: justify;', 'text-align: left;')
    style_tag.string = style_tag.string.replace('text-align: justify;', 'text-align: left;')
```

### 3. Ensure All Chapter Images Are Present
```python
# Get list of available chapter images from filesystem
chapter_images = [f for f in os.listdir('generated_images/') 
                 if re.fullmatch(r'chapter\d+\.png', f)]
chapter_images.sort(key=lambda x: int(re.search(r'chapter(\d+)', x).group(1)))

# Map the TARGET chapter order, not subsection titles
chapter_mapping = {
    1: "Chapter 1: The Shock",
    2: "Chapter 2: Mr. Chips",
    3: "Chapter 3: The Echoes of Sputnik and a Family Legacy",
    4: "Chapter 4: The Garage",
    5: "Chapter 5: The Spark Ignites",
    6: "Chapter 6: Life as an Engineer",
    7: "Chapter 7: Foundations",
    8: "Chapter 8: The Diagnosis",
    9: "Chapter 9: The New Partnership",
    10: "Chapter 10: The Y2K Challenge",
    11: "Chapter 11: The New Beginning",
    12: "Chapter 12: The Legacy",
}

# For each chapter, ensure an image exists immediately after the chapter header
for chapter_num, chapter_title in chapter_mapping.items():
    chapter_header = find_chapter_header(soup, chapter_title)
    if chapter_header:
        next_node = chapter_header.find_next_sibling()
        next_img = next_node if next_node and next_node.name == 'img' else None
        if not next_img or not correct_chapter_image(next_img.get('src', ''), chapter_num):
            correct_img_file = f'chapter{chapter_num}.png'
            if correct_img_file in chapter_images:
                img_tag = soup.new_tag('img',
                    src=f'generated_images/{correct_img_file}',
                    alt=f'Chapter {chapter_num} image')
                chapter_header.insert_after(img_tag)
```

**Critical verification rule:** do not just search for chapter titles globally in the HTML, because titles often appear in the Table of Contents. Verify against the actual chapter header in the body, then confirm the **immediate next sibling** is the correct `<img>` tag. This avoids false positives where images were accidentally inserted inside the TOC instead of after chapter headings.

### 4. Add Missing Structural Elements
```python
# Add back cover if missing
if not soup.find(id='back-cover'):
    back_cover = create_back_cover()
    soup.body.append(back_cover)

# Add page breaks between chapters
# Remove existing page breaks first, then add new ones
for br in soup.find_all('div', class_='page-break'):
    br.decompose()

# Add page break after each chapter (after image if present)
for chapter in chapters:
    # Insert page break logic
```

### 5. Generate Missing Images or Create Safe Fallbacks
```python
# If a required chapter image is missing, first try to locate an alternate variant
# (e.g. chapter3_20260423_175012.png). If none exists or the candidate is invalid,
# create a neutral placeholder so the manuscript remains structurally complete.

required = [f'chapter{i}.png' for i in range(1, 13)]
existing = set(os.listdir('generated_images'))

for name in required:
    path = os.path.join('generated_images', name)
    if name not in existing or os.path.getsize(path) < 1000:
        alternate = find_alternate_image_variant(name)  # user-defined helper
        if alternate:
            shutil.copy2(alternate, path)
        else:
            create_placeholder_png(path, width=1200, height=675)
```

### 5b. Detect "Technically Present but Visually Blank" Images
A chapter image can still be wrong even when:
- an `<img>` tag exists,
- the source is an embedded `data:image/png;base64,...` URI, and
- structural verification says the image is present.

In practice, this can happen when an earlier placeholder or corrupt file was embedded into standalone HTML. A useful detection pattern is:

```python
img = chapter_header.find_next_sibling('img')
src = img.get('src', '') if img else ''

# Suspicious signs:
# - data URI is very short
# - underlying file on disk is tiny
# - image is known placeholder / flat-color fallback
if src.startswith('data:image/') and len(src) < 10000:
    regenerate_or_replace_image(chapter_num)
```

When the user reports a "blank image" after the chapter title, do not trust structural verification alone. Inspect the actual embedded image or underlying file, then replace it with a newly generated illustration if needed.

### 5c. Regenerate a Replacement Chapter Illustration
For damaged or blank chapter art, generate a replacement tuned to the chapter's content. Example reusable prompt pattern:

```text
Create a black-and-white pencil sketch chapter illustration for Chapter X.
Subject: [historical objects / symbolic scene from chapter]
Style: hand-drawn graphite pencil sketch, monochrome only, detailed shading,
textured paper feel, elegant book-illustration style.
Composition: balanced, uncluttered, suitable beneath a chapter title.
Avoid: text, logos, gibberish, cartoon style, color effects.
```

Then run a quick visual QA pass to confirm:
- it is truly monochrome,
- it reads like a pencil sketch,
- no baked-in text is visible,
- the composition works as chapter art.

**Reusable lesson:** for Telegram/HTML delivery, the most robust final artifact is often a **standalone HTML file with embedded base64 image data URIs**. This prevents broken rendering caused by relative paths or missing companion files.

### 6. Verify Corrections
```python
# Check alignment
assert 'text-align: left;' in style_tag.string

# Check all 12 chapters have correct images as immediate next siblings
for chapter_num, chapter_title in chapter_mapping.items():
    header = find_chapter_header(soup, chapter_title)
    assert header is not None
    next_node = header.find_next_sibling()
    assert next_node is not None and next_node.name == 'img'
    assert correct_chapter_image(next_node.get('src', ''), chapter_num)

# If using standalone delivery, verify images are embedded
html_text = str(soup)
assert html_text.count('data:image/png;base64,') >= 12

# Check dedication / front matter updates if requested by user
assert 'To my wife and all of our children' in html_text
```

### 7. Second-Pass Structural Rebuild
If the first repair only restores image placement but the manuscript body is still structurally messy, perform a **second pass**:
- Rebuild from the cleanest Markdown source
- Promote or split content into the user's target chapter architecture
- Move overflow material into better-fitting later chapters
- Re-render the full manuscript into fresh HTML instead of continuing to patch the old HTML

Example pattern used successfully:
- Use a 10-chapter source with reliable prose blocks
- Split one overloaded mid-book chapter to extract `The Y2K Challenge` into its own chapter
- Split the late-life chapter into `The New Beginning` and `The Legacy`
- Integrate epilogue material into the final legacy chapter when the user wants a clean 12-chapter edition

### 8. Deliver Final File
```python
# Save corrected manuscript
with open('THE_UNWRITTEN_FUTURE_CORRECTED.html', 'w') as f:
    f.write(str(soup))

# Send via Telegram media link
send_message(
    message="Manuscript correction complete. Attached is the corrected file.",
    target='telegram'
)
send_message(
    message=f"MEDIA:/path/to/THE_UNWRITTEN_FUTURE_CORRECTED.html",
    target='telegram'
)
```

## Key Considerations
- **Avoid reconciliation loops**: When multiple manuscript variants exist, do not keep merging corrupted outputs into each other. First score the candidates and choose the single best base file to repair.
- **Choose the best base quantitatively**: Compare candidates by (1) whether all target chapter headers exist, (2) whether each chapter header is immediately followed by the correct image, (3) whether misplaced images appear in the Table of Contents, and (4) whether dedication/front matter already exists. Repair the strongest base instead of synthesizing from several weak ones.
- **Image Placement**: Images must be immediately after chapter headers, not elsewhere.
- **Chapter Mapping**: Use chapter titles, not just numbers, to identify chapters since headers may differ across drafts.
## Key Considerations
- **Image Placement**: Images must be immediately after chapter headers, not elsewhere
- **Chapter Mapping**: Use chapter titles, not numbers, to identify chapters since headers may not contain numbers
- **Multiple Checks**: Verify each fix systematically to avoid missed issues
- **Error Handling**: Gracefully handle missing images by generating them
- **Delivery**: Use MEDIA: prefix for Telegram file delivery to ensure complete file transfer
- **Do Not Reconcile Broken Variants Against Each Other**: When several HTML outputs are partially corrupted, stop diffing broken outputs and identify the cleanest narrative source (for example a better Markdown master such as `THE_UNWRITTEN_FUTURE_FULL.md`). Rebuild from that source instead of trying to repair drift introduced by previous automation.
- **Prefer Standalone HTML for Telegram Delivery**: If chapter images are referenced by relative filesystem paths, embed them as base64 `data:` URIs so the delivered HTML remains self-contained and renders correctly after download or forwarding.
- **Structural Rebuild May Beat Micro-Fixes**: If the manuscript body and chapter map disagree, it can be faster and more reliable to re-split the source into the intended chapter architecture (for example, promoting Y2K / New Beginning / Legacy into distinct final chapters) than to keep patching malformed HTML.

## Additional Verification Pattern
```python
# For each target chapter title, find the heading node in parsed HTML
# and confirm its immediate next sibling is an <img> for the correct chapter.
# Do this in the main manuscript body, not the TOC.
for title, chapter_num in chapter_map:
    node = find_heading_in_main_content(soup, title)
    assert node is not None
    next_node = node.find_next_sibling()
    assert next_node and next_node.name == 'img'
    assert f'chapter{chapter_num}.png' in next_node.get('src', '') or next_node.get('src', '').startswith('data:image/')
```

## Expected Outcomes
- Manuscript file fully corrected and properly formatted
- All chapter images present and correctly placed
- Left-justified text throughout
- Complete front and back matter
- Properly formatted for PDF conversion
- Delivered via appropriate channel with confirmation

## Pitfalls to Avoid
- Don't assume chapter numbers from header order - map by title
- Don't place images before chapter headers or in wrong positions
- Don't forget to remove old page breaks before adding new ones
- Don't skip verification - multiple issues often coexist
- Don't deliver without using MEDIA: prefix for Telegram