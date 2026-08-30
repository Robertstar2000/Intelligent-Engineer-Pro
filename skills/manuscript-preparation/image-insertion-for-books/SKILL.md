---
name: image-insertion-for-books
version: 1.0
description: Systematic approach for inserting images into HTML manuscripts based on Table of Contents mapping
skills:
  - manuscript-preparation-and-delivery
  - creative
tools:
  - bs4
  - re
  - weasyprint
---


## Memory context (Hindsight)

Long-term memory context is now provided automatically by Hindsight (bank
`mifeco-default`) on every turn — the retired MemPalace manual query step no
longer applies. Do NOT attempt to import `~/.hermes/mempalace` (it was removed
2026-08-19).This retrieves previous decisions, domain-specific context, and lessons learned from the vector memory store.

# Image Insertion for Books

## Overview
Systematic approach for inserting images into HTML manuscripts based on Table of Contents (TOC) mapping. This skill is particularly useful when chapter content headings don't directly match TOC entries, requiring structural analysis.

## When to Use
- Preparing manuscripts for print or PDF conversion
- Inserting illustrations, figures, or chapter headers
- Working with complex HTML structures where chapter starts aren't obvious
- Mapping TOC entries to actual content sections

## Prerequisites
- Complete HTML manuscript with TOC (usually `<ul>` or `<ol>` containing chapter entries)
- Image files named consistently (e.g., `chapter1.png`, `chapter2.png`)
- Basic understanding of document structure (h1-h3 tags, etc.)

## Step-by-Step Process

### 1. Analyze Document Structure
```python
# Load HTML and parse with BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Identify TOC structure (usually <ul> or <ol> with <li> chapter entries)
toc_list = soup.find('ul') or soup.find('ol')
```

### 2. Map TOC Entries to Content Sections
```python
# Find all TOC <li> elements with chapter numbers
toc_by_chapter = {}
for li in soup.find_all('li'):
    match = re.search(r'chapter\s*(\d+)', li.text, re.IGNORECASE)
    if match:
        chapter_num = int(match.group(1))
        toc_by_chapter[chapter_num] = li
```

### 3. Locate Chapter Start Headings
```python
# For each TOC entry, find the next h3 heading after it
for chapter_num, toc_li in toc_by_chapter.items():
    next_h3 = toc_li.find_next('h3')
    if next_h3:
        # This h3 likely marks the start of the chapter content
        chapter_headings[chapter_num] = next_h3
```

### 4. Insert Images with Proper Formatting
```python
# Insert image after the chapter heading
img_filename = f'chapter{chapter_num}.png'
img_path = f'generated_images/{img_filename}'
img_tag = soup.new_tag('img', src=img_path, alt=f'Illustration for Chapter {chapter_num}', 
                      style='max-width: 100%; height: auto; display: block; margin: 20px auto;')
next_h3.insert_after(img_tag)

# Add spacing and page breaks for print
br_tag = soup.new_tag('br')
img_tag.insert_after(br_tag)
pb_tag = soup.new_tag('div', style='page-break-before: always;')
br_tag.insert_after(pb_tag)
```

### 5. Handle Edge Cases
```python
# Check if image already exists
existing_img = next_h3.find_next('img')
if existing_img and f'Chapter {chapter_num}' in existing_img.get('alt', '').lower():
    # Skip insertion - image already present
    continue

# Handle missing images gracefully
if chapter_num not in available_images:
    # Log warning and continue
    print(f"⚠️  No image available for Chapter {chapter_num}")
```

## Key Insights from Experience

1. **TOC entries are usually in `<li>` tags** - These are the most reliable markers for chapter locations
2. **Chapter content starts with h3** - After the TOC li, the next h3 is typically the chapter heading
3. **Check for existing images** - Avoid duplicates by verifying if an image already exists after the heading
4. **Maintain print formatting** - Always add `<br>` and `page-break-before` for proper PDF conversion

## Verification Steps
```python
# After insertion, verify:
1. Count images in final document
2. List chapters with images
3. Identify any chapters still missing images
4. Check that images are placed after correct headings
```

## Common Pitfalls & Solutions

| Pitfall | Solution |
|---------|----------|
| TOC entries not mapping to h3s | Look for other heading levels (h2, h4) or use text search |
| Images inserted in wrong order | Sort TOC entries by chapter number before processing |
| Duplicate images | Check for existing images with same alt text before inserting |
| Broken image paths | Use relative paths and verify file existence before insertion |

## Best Practices

- Always backup original HTML before modification
- Use relative paths for image sources
- Test with a sample chapter first before processing all chapters
- Log all actions for debugging
- Verify final structure with a quick visual check

## Output
- Modified HTML file with images inserted
- Optionally, generate PDF using WeasyPrint or similar
- Log file with insertion details and any issues encountered

## Tools Required
- BeautifulSoup (for HTML parsing)
- Python stdlib (os, re)
- WeasyPrint (optional, for PDF conversion)
- Image generation API (if creating new images)

## Success Criteria
- All chapters have appropriate images inserted
- No duplicate images
- Proper print formatting (page breaks, spacing)
- Valid HTML structure maintained
- PDF conversion works correctly