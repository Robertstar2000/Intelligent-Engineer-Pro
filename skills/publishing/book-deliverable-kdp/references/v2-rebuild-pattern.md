# V2.0 Manuscript Rebuild Pattern

## Overview
When rebuilding manuscripts with editorial fixes (duplicate removal, title corrections, content replacement, formatting fixes), follow this pattern to avoid context window failures.

## The Rule
**DO NOT delegate full-book rewrites to subagents.** Context window ("Window too small") failures WILL occur when subagents try to read 30+ chapter files simultaneously.

## The Pattern
Write small Python scripts (one per task) that read/write chapter files sequentially. Each script handles ONE concern.

### Script Types
1. **Duplicate removal** - removes consecutive identical heading lines from XHTML chapter files
2. **Content replacement** - bulk find/replace across all chapter files
3. **Chapter rewrite** - generates full chapter content from template functions, one chapter at a time

## Critical: Chapter-Level Duplication Detection

When ALL chapters in a book are near-identical (same scenes, same dialogue, with only character names or minor details swapped), prose-level generic phrase detection is INSUFFICIENT. You need structural duplication detection.

### Detection Method
Read the first chapter body as reference. Compare all other chapters against it. Flag chapters where body text is >70% similar to reference. Also check for alternating template patterns (odd chapters share one template, even chapters share another). Near-duplicate chapters need complete prose-level replacement.

### What to Do
Write a Python script that generates UNIQUE content for EACH chapter based on its title/milestone. Each rewritten chapter should be ~5000 chars for a ~3-4 page contribution at 6x9in.

### Chapter Rewrite Helper
```python
def write_chapter(ch_num, title, body_html):
    xhtml = f'''<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head><title>Chapter {ch_num} — {title}</title>
<style>
p {{ text-indent: 1.2em; margin: 0.3em 0; line-height: 1.6; }}
p.first-para {{ text-indent: 0; }}
.scene {{ text-align: center; text-indent: 0; margin: 1.2em 0; font-style: italic; }}
h1 {{ text-align: center; page-break-before: always; font-size: 1.3em; font-weight: normal; }}
</style></head>
<body><h1>Chapter {ch_num} — {title}</h1>{body_html}</body></html>'''
    with open(f'manuscript_src/ch{ch_num:02d}.xhtml', 'w') as f:
        f.write(xhtml)
```

## Critical: Python String Handling for HTML Content

**NEVER use triple-quoted strings** containing apostrophes, possessives, or contractions:
```python
write_chapter(56, "The Shipyard", '''<p>James Okonkwo's masterwork...''')
# FAILS: SyntaxError
```

**USE instead:**
```python
# Pattern 1: Helper functions
def p(text): return f'<p>{text}</p>'
def fp(text): return f'<p class="first-para">{text}</p>'
def sc(): return '<p class="scene">* * *</p>'

# Pattern 2: Use &#39; for apostrophes
"<p>The crew&#39;s celebration lasted one night.</p>"

# Pattern 3: chr(39) inside f-strings
f"<p>Okonkwo{chr(39)}s drill...</p>"

# Pattern 4: String concatenation
"<p>Robert walked the base alone.</p>" + "<p>Every viewport where she watched Earth rise.</p>"
```

## Output Generation Pipeline
1. **Build HTML**: Assemble chapters into single print-formatted HTML (6x9in, TOC, front/back matter)
2. **Generate PDF**: `/home/bob/.hermes/hermes-agent/venv/bin/weasyprint input.html output.pdf`
3. **Generate EPUB**: Build EPUB3 from individual chapter XHTML files using Python stdlib zipfile
4. **Verify**: `pdftotext book.pdf - | grep -c "^[0-9]+$"` for page count (target 175-225)

## Page Count Targeting
- Target: **175-225 pages** at 6x9in per book
- ~850-1000 chars of body text per page (11pt Georgia, 1.6 line-height, 0.75in margins)
- For 200 pages: need ~170,000-200,000 chars total
- **Do NOT pad with CSS** (huge margins, tiny font). Expand content instead.
- Verify: `pdftotext book.pdf - | grep -c "^[0-9]+$"`

## Series Transition Template
End each book with: (1) thank reader, (2) series description 2-3 sentences, (3) list ALL books in series, (4) hint at next book, (5) "Available on Amazon Kindle and Paperback"

## Common Structural Fixes
- **Duplicate chapter headings**: Remove `<h2>Chapter N</h2>` when `<h1>Chapter N — Title</h1>` follows
- **"End of Chapters" markers**: Assembly artifacts. Remove all.
- **"About the Author" formatting**: Fix concatenation (`About the AuthorBob` → `About the Author\nBob`)
- **Placeholder paragraphs**: Remove all identical generic text; replace with scene-specific content
- **Scene-break markers**: `* * *` in source becomes `<p class="scene">* * *</p>` in XHTML

## Grammar/Style Fixes (common in AI-generated manuscripts)
- "a uncharacteristic" → "an uncharacteristic"
- "back in Indian" → "back in Hindi"
- "back in Mexican-American" → "back in Spanish"
- "back in Jordanian" → "back in Arabic"
- "back in Canadian" → "back in French"
- "artificial gravity at one-sixth Earth normal" → "the familiar one-sixth gravity"
- Generic placeholder paragraphs: "The work continued through the long hours" / "In the silence of the habitat" / "The data painted a complex picture" / "The implications were staggering" / "We need to consider all possibilities" / "What are you thinking about?"
