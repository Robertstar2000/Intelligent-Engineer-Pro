---
name: manuscript-restoration
description: Restore missing or incorrect chapter headers in a manuscript by comparing TOC with actual content structure
version: 1.0.0
author: Hermes Agent
license: MIT
tags: ["manuscript", "restoration", "chapters", "toc", "formatting"]
related_skills: ["manuscript-preparation-and-delivery", "mempalace-embedding-integration", "creative-ideation"]
---


## 🔍 MemPalace Query (MANDATORY FIRST STEP)
Before proceeding, query MemPalace for existing context:
```python
import sys, os; sys.path.insert(0, os.path.expanduser('~/.hermes/mempalace'))
import embed; embed.init_embedding(os.path.expanduser('~/.hermes/mempalace'))
results = embed.search_embeddings("manuscript restoration missing chapter headers", k=5)
```
This retrieves previous decisions, domain-specific context, and lessons learned from the vector memory store.

# Manuscript Restoration Skill

## Purpose
Restore missing or incorrect chapter headers in a manuscript by comparing the Table of Contents (TOC) with the actual content structure. This skill is useful when importing manuscripts from various sources where formatting may be inconsistent or headers may be missing.

## When to Use
- When the TOC shows chapters that don't match the actual content structure
- When chapter headers are missing or incorrectly formatted
- When preparing a manuscript for publication or conversion to other formats

## Approach

### 1. **Analyze the Current State**
```python
# Read the manuscript file
content = read_file(path)

# Extract TOC entries using regex
toc_pattern = r'Chapter \d+: [^\n]+'
toc_entries = re.findall(toc_pattern, content)

# Extract actual chapter headers
chapter_pattern = r'^# Chapter \d+: [^\n]+'
actual_chapters = re.findall(chapter_pattern, content, re.MULTILINE)
```

### 2. **Identify Missing Chapters**
```python
# Compare TOC with actual chapters
toc_set = set(toc_entries)
actual_set = set(actual_chapters)
missing_chapters = toc_set - actual_set

if missing_chapters:
    print(f"❌ Missing {len(missing_chapters)} chapters")
    for chapter in missing_chapters:
        print(f"  - {chapter}")
else:
    print("✅ All chapters present")
```

### 3. **Restore Missing Headers**
```python
# For each missing chapter, find where it should be inserted
for chapter in missing_chapters:
    # Extract chapter number
    chapter_num = chapter.split(':')[0].split()[1]
    
    # Search for content that belongs to this chapter
    search_pattern = rf'Chapter {chapter_num}[\s:\-]'
    
    for i, line in enumerate(lines):
        if re.search(search_pattern, line) and not line.startswith('#'):
            # Insert header before this line
            header = f"# {chapter}"
            lines.insert(i, header)
            break
```

### 4. **Verify Restoration**
```python
# Re-extract chapters to verify
restored_chapters = re.findall(chapter_pattern, new_content, re.MULTILINE)
print(f"✅ Restored {len(restored_chapters)} chapters")
```

## Key Considerations
- **Backup First**: Always create a backup of the original file before making changes
- **Pattern Matching**: Use regex to identify chapter numbers and content boundaries
- **Order Matters**: Insert chapters in the order they appear in the TOC
- **Handle Duplicates**: Watch for duplicate chapter numbers (e.g., two Chapter 10s)

## Tools Required
- `read_file` - to read manuscript content
- `write_file` - to save restored manuscript
- `execute_code` - for Python processing
- `search_files` - optional for finding content patterns

## Success Criteria
- All TOC chapters are present in the content with proper headers
- Chapter headers follow a consistent format (e.g., `# Chapter X: Title`)
- No duplicate or orphaned content sections
- The manuscript flows logically from chapter to chapter

## Duplicate Content Detection

When a manuscript has duplicate story sections (same event appearing in multiple chapters):

1. **Identify duplicates by scanning for repeated scene headers/subheadings**:
   ```bash
   grep -n "^### \|^## " MANUSCRIPT.md | sort | uniq -d
   ```
2. **Compare line counts** — the longer version is usually the canonical one
3. **Remove the shorter/duplicate version** — typically the later occurrence is the duplicate
4. **Verify flow after removal** — check that the surrounding paragraphs connect logically

**Pattern from Tomorrow Remembered cleanup**: Three duplicate sections (TV repair shop, first car, science fair) were found in Chapter 5 that duplicated content from Chapter 3. The Chapter 3 versions were full-length; Chapter 5 versions were abbreviated duplicates. Removed 67 lines total.

## Title Change Verification

When a book title has changed (e.g., "Tomorrow Is Still Open" → "Tomorrow Remembered"):

1. **Grep across ALL files** in the book directory:
   ```bash
   grep -r "Old Title" /path/to/book/ --include="*.md" --include="*.txt" --include="*.html" --include="*.pdf" --include="*.epub"
   ```
2. **Check PDF metadata** (not just content):
   ```python
   from PyPDF2 import PdfReader
   r = PdfReader("book.pdf")
   print(r.metadata.get("/Title", "NO TITLE"))
   ```
3. **Check EPUB metadata** by extracting and reading `content.opf`:
   ```bash
   unzip -p book.epub OEBPS/content.opf | grep -i "<dc:title>"
   ```
4. **Delete old-title files** — remove any files with the old title in the filename from KDP_PACKAGE and other directories
5. **Update README/metadata files** that reference old filenames

## Limitations
- Works best with manuscripts that have a clear TOC structure
- May not work well with highly irregular formatting
- Requires the content for each chapter to be present somewhere in the file

## Example Usage
```python
# Restore missing chapters in a manuscript
skill = load_skill('manuscript-restoration')
skill.restore_chapters(
    file_path='/path/to/manuscript.md',
    toc_pattern=r'Chapter \d+: [^\n]+'
)
```

## Related Skills
- `manuscript-preparation-and-delivery` - for overall manuscript preparation
- `mempalace-embedding-integration` - for memory-enhanced writing
- `creative-ideation` - for content generation

## Author
Hermes Agent - Generated from conversation on April 23, 2026