---
title: Manuscript Image Placement Skill
layout: skill
name: manuscript-image-placement
description: A systematic approach for inserting chapter images into HTML manuscripts based on existing image placement patterns. This skill includes a Python script for automated detection and insertion of missing chapter images.
---


## Memory context (Hindsight)

Long-term memory context is now provided automatically by Hindsight (bank
`mifeco-default`) on every turn — the retired MemPalace manual query step no
longer applies. Do NOT attempt to import `~/.hermes/mempalace` (it was removed
2026-08-19).This retrieves previous decisions, domain-specific context, and lessons learned from the vector memory store.

# Manuscript Image Placement Skill

## Overview
A systematic approach for inserting chapter images into HTML manuscripts based on existing image placement patterns. This enhanced version includes a Python script for automated detection and insertion of missing chapter images, making it invaluable for formatting memoirs, novels, and non-fiction books.

## When to Use
- When a manuscript HTML file exists but lacks proper image placement
- When some chapters already have images placed (to establish the pattern)
- When you need to insert missing chapter images in a consistent, professional manner
- When dealing with complex HTML structures with nested parts/chapters

## Prerequisites
- HTML manuscript file with proper structure
- All chapter images available in a known directory
- At least some chapters already have images placed (to establish the pattern)
- Understanding of the desired image styling (size, alignment, etc.)

## Step-by-Step Approach

### 1. **Analyze Existing Image Placements**
```python
# Find all existing image tags to understand the pattern
search_files(pattern='<img src=', target='content')
```
- Identify which chapters already have images
- Note the exact HTML structure and styling used
- Document the image source path pattern

### 2. **Understand the HTML Structure**
- Read the file from the beginning to understand the document structure
- Identify how chapters are organized (h2 for parts, h3 for chapters, etc.)
- Note any special classes or IDs used for styling
- Check for any existing image placement patterns (after which heading types)

### 3. **Identify Missing Chapters**
- Compare the Table of Contents with the actual content
- Create a list of chapters that need images
- For each missing chapter, find the corresponding `<h3>` heading in the content

### 4. **Locate Exact Insertion Points**
- For each missing chapter, find the exact line number of its heading
- Verify the heading matches the expected chapter title
- Note any special context around the heading (transitions, sections, etc.)

### 5. **Automated Image Insertion (Python Script)**
Use the following script to programmatically insert missing images:

```python
# Read the file using Python's built-in open
html_path = "/path/to/manuscript.html"
with open(html_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Define missing chapters with their titles (from TOC) and image filenames
missing_chapters = [
    (3, "The Echoes of Sputnik and a Family Legacy", "chapter3.png"),
    (8, "The Diagnosis", "chapter8.png"),
    (9, "The New Partnership", "chapter9.png"),
    (10, "The Y2K Challenge", "chapter10.png"),
    (11, "The New Beginning", "chapter11.png"),
    (12, "The Legacy", "chapter12.png")
]

new_lines = lines.copy()

# For each missing chapter, find the best insertion point
for chapter_num, title, img_file in missing_chapters:
    # Search for the title in the lines (case-insensitive)
    found = False
    for i, line in enumerate(lines):
        if title.lower() in line.lower():
            # Insert image tag after this line
            img_tag = f'<img src="/home/bob/books/The_Unwritten_Future/generated_images/{img_file}" alt="Chapter {chapter_num} Header" style="max-width: 300px; height: auto; margin: 20px 0;">\n'
            new_lines.insert(i+1, img_tag)
            found = True
            print(f"Inserted image for Chapter {chapter_num} after line containing '{title}'")
            break
    if not found:
        # Try shorter version of the title
        short_title = title.split(':')[0'] if ':' in title else title
        for i, line in enumerate(lines):
            if short_title.lower() in line.lower():
                img_tag = f'<img src="/home/bob/books/The_Unwritten_Future/generated_images/{img_file}" alt="Chapter {chapter_num} Header" style="max-width: 300px; height: auto; margin: 20px 0;">\n'
                new_lines.insert(i+1, img_tag)
                found = True
                print(f"Inserted image for Chapter {chapter_num} after line containing '{short_title}' (shortened)")
                break
    if not found:
        print(f"WARNING: Could not find suitable location for Chapter {chapter_num} - '{title}'")

# Write the modified content back
with open(html_path, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)
print("File updated with missing chapter images.")

# Verify by counting images
img_tags = []
for i, line in enumerate(new_lines):
    if 'chapter' in line and '.png' in line and 'generated_images' in line:
        # Extract chapter number
        import re
        m = re.search(r'chapter(\d+)\.png', line)
        if m:
            img_tags.append(int(m.group(1)))
print(f"Found {len(img_tags)} chapter images after update: {sorted(img_tags)}")

# Check which chapters are missing images now
existing_chapters = set(img_tags)
all_chapters = set(range(1, 13))
missing_after = all_chapters - existing_chapters
print(f"Chapters still missing images: {sorted(missing_after)}")
```

### 6. **Verify and Test**
- After all insertions, verify the total chapter count
- Check that images display correctly in a browser
- Ensure the file size and structure remain valid

## Key Considerations

### **HTML Structure Patterns**
- Chapters may be organized within `<div class=\"part\">` containers
- Some chapters may have multiple `<h3>` tags (subsections)
- The main chapter heading is usually the first `<h3>` after the part heading
- Image tags should follow the main chapter heading, not subsections

### **Image Styling**
- Use consistent styling across all chapters
- Typical styling: `max-width: 300px; height: auto; margin: 20px 0;`
- Consider responsive design for different screen sizes
- Ensure images don't break page layout

### **Error Handling**
- If a chapter heading cannot be found, check for alternative titles
- If the HTML structure is complex, read the file in sections
- Verify image file existence before insertion
- Handle cases where chapter titles differ from TOC titles

## Common Pitfalls & Solutions

### **Pitfall**: Chapter titles in content differ from TOC titles
**Solution**: Search for partial matches or first few words of titles

### **Pitfall**: Multiple `<h3>` tags within a chapter
**Solution**: The main chapter heading is usually the first `<h3>` after the part heading

### **Pitfall**: Complex nested HTML structure
**Solution**: Read the file in sections and track line numbers carefully

### **Pitfall**: Image paths may need adjustment
**Solution**: Use the same path pattern as existing images

## Gemini API Image Generation (Markdown Manuscripts)

Modern fiction books use Markdown manuscripts with `## Chapter N:` headers. This section covers generating B&W pencil sketch images via Gemini API and inserting them.

### API Setup

```python
result = subprocess.run(["bash", "-c", "source ~/.hermes/.env && echo $GOOGLE_AI_STUDIO_KEY"],
                       capture_output=True, text=True)
api_key = result.stdout.strip()
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image:generateContent?key={api_key}"
```

### Prompt Style

Append to every image prompt:
```
Style: black and white pencil sketch illustration for a book chapter, detailed cross-hatching, dramatic lighting, cinematic composition, no color, book illustration quality.
```

### Rate Limiting

Wait **6 seconds** between API calls. Decode inline base64 data:
```python
img_data = base64.b64decode(p["inlineData"]["data"])
img = Image.open(BytesIO(img_data)).convert("L").resize((600, 600), Image.LANCZOS)
img.save(f"chapter_images/ch{N:02d}.png")
```

### Chapter Header Pitfalls (Books Have Different Formats)

**Critical:** Book manuscripts do NOT all use the same chapter header format. Detect the format before generating/inserting images:

| Format | Example | Regex | Books |
|--------|---------|-------|-------|
| Single hash | `# Chapter 1 -- Title` | `^# Chapter \d+` | AoLS, LF, NBS |
| Double hash | `## Chapter 1: Title` | `^## Chapter \d+:` | CLLC Bk 1 & 3 |
| Worded numbers | `## Chapter One: Title` | `Chapter (One|Two|...):` | Tomorrow Remembered |
| Inline (no preceding newline) | `...imagine.## Chapter Two:` | Search entire content, not per-line | Tomorrow Remembered |
| Non-sequential | 1,2,3,5,7,10,13... | Insert only for existing headers | CLLC Bk 1 |

**Procedure:**
1. Check BOTH `MANUSCRIPT.md` AND `{book-name}_MANUSCRIPT.md` (some books use different files)
2. Use `grep` to find chapter headers BEFORE writing generation/insertion code
3. For inline headers, insert a `\n` before the header when adding images
4. Save images as `chapter_images/ch{N}.png` (600x600, grayscale)
4. Check for existing images before generating to avoid duplicates

## Verification Steps
1. Count total chapters in TOC vs. actual content
2. Verify each chapter has exactly one image tag
3. Check that image tags follow the correct heading
4. Test file rendering in a browser if possible
5. Confirm file size is reasonable

## Tools Required
- `read_file` for examining content
- `search_files` for finding patterns
- `execute_code` for running the Python script
- `write_file` for saving the final version (if not using direct file I/O)

## Output Format
The final manuscript should be delivered as an HTML file via Telegram media attachment using the `MEDIA:/path/to/file` format.

## Skill ID
manuscript-image-placement