# Page Count Targeting via Content Compression

When a book exceeds the target page range (180-200 pages for 6"×9") and changing CSS (margins, font size, line-height) is not an option, compress content while preserving narrative integrity.

## Measured Words-Per-Page

At 11.5pt Georgia, 1.5 line-height, 0.75in margins on 6"×9":
- 205-210 words per page (no page-break-before waste)
- With `page-break-before: always` on each chapter: ~190-200 wpp (each chapter wastes ~1/3 page)
- At 11pt Georgia, 1.45 line-height: ~240-256 wpp (tighter spacing)

Always verify with `pdftotext + pdfinfo` rather than calculating — CSS details matter.

## Compression Strategy

### Strategy 1: Scene-Break Trimming (best for quality retention)

Each chapter typically has 3-5 scene-break sections separated by `* * *`. The first 1-2 scenes usually contain the chapter's core plot development and character work. Later scenes often expand on what was already established.

```python
# Keep only the first N scenes per chapter
scenes = body.split('* * *')
compressed = ' * * * '.join(scenes[:2])  # Keep first 2 scenes
```

**Rule of thumb:** Each scene-break removal saves ~150-250 words. For a 20-chapter book, keeping first 2 instead of 4 scenes saves ~20-30 pages.

### Strategy 2: Proportional Sentence Trimming

For each paragraph, keep the first X% of sentences:

```python
sentences = re.split(r'(?<=[.!?])\s+', paragraph_text)
keep = max(1, int(len(sentences) * ratio))  # ratio = target_wc / current_wc
trimmed = ' '.join(sentences[:keep])
```

**Warning:** This can damage narrative flow if overused (>20% removal). Best used WITH scene-break trimming, not instead of it.

### Strategy 3: PDF → HTML Rebuild (when source HTML is lost)

If the book's HTML has been corrupted or over-compressed, rebuild from the PDF:

```python
import subprocess, re

# Extract text from PDF
result = subprocess.run(["pdftotext", pdf_path, "-"], capture_output=True, text=True)
lines = result.stdout.split('\n')

# Find real chapters (those with em-dash — not bare number headers)
chapters = []
for i, line in enumerate(lines):
    m = re.match(r'^Chapter (\d+)\s*[—\-–]\s*(.*)', line.strip())
    if m:
        ch_num = int(m.group(1))
        ch_title = m.group(2).strip()
        next_ch = len(lines)
        for j in range(i+1, len(lines)):
            if re.match(r'^Chapter \d+\s*[—\-–]', lines[j].strip()):
                next_ch = j
                break
        body_lines = [l for l in lines[i+1:next_ch] if not re.match(r'^\s*\d+\s*$', l)]
        chapters.append((ch_num, ch_title, body_lines))
```

**Pitfall:** `pdftotext` often extracts duplicate chapter headings (both the bare "Chapter 02" and the titled "Chapter 2 — Title"). Only match on lines WITH the em-dash to get clean chapters.

## Quick Estimation

For a ~47K word book at 6"×9" with standard CSS:
- At 205 wpp: ~229 pages
- Remove 8 scene-break sections: ~-8 pages (221)
- Trim 15% of sentences: ~-33 pages (188)
- Combined: ~188 pages ✅

## File Structure Recovery

When rebuilding a book from PDF text, the output HTML needs these elements reconstructed:
1. `@page { size: 6.25in 9.25in; margin: 0.75in; }` — print CSS
2. Title page with book title, series, author
3. Copyright page
4. TOC with chapter list (table-based layout)
5. Chapter content with `<h1 class="chapter-title">` headings
6. Back matter with "About the Author"

The original CSS from Book_3_Waters_End.html or Book_6_Moon Rock.html can serve as template.