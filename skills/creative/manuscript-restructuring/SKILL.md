---
name: manuscript-restructuring
displayName: Manuscript Restructuring
description: A systematic approach for restructuring manuscripts by identifying patterns, rewriting content in a more personal voice, repositioning sections, and performing bulk automated text transformations with output format rebuild. Also covers editorial proposal-driven chapter compression (removing AI voice, tightening), chapter expansion (adding scene work, sensory detail, dialogue, vignettes), and hybrid chapter revision (mixed compress/expand/deduplicate operations on the same chapter).
---

## Memory context (Hindsight)

Long-term memory context is now provided automatically by Hindsight (bank
`mifeco-default`) on every turn — the retired MemPalace manual query step no
longer applies. Do NOT attempt to import `~/.hermes/mempalace` (it was removed
2026-08-19).This retrieves previous decisions, domain-specific context, and lessons learned from the vector memory store.

## When to Use This Skill

Use this skill when:
- Editing long-form content that needs structural changes
- Finding and replacing specific patterns in documents
- Moving sections to improve narrative flow
- Restructuring manuscripts while preserving formatting
- Transforming generic content into more personal, engaging prose
- Applying editorial improvement proposals to compress and remediate memoir chapters — removing AI lecture-voice, tightening transitions, converting to first-person, and hitting target word counts
- Rewriting AI-generated memoir content that suffers from academic tone, named psychologists, clinical framing, or third-person distance

## Approach

### 0. **Plan Order of Operations**
Bulk transformations must be applied in the correct sequence to avoid conflicts. For a **comprehensive manuscript overhaul** (multiple categories of changes), use this expanded sequence:

1. **Name/term replacements** — do FIRST on raw text. These are non-content-affecting (e.g., "MCRcore"→"Small Business", "Jimenez"→""). Safe to do before anything else.
2. **Structural edits** — shorten chapters, rewrite sections, reposition content.
3. **Bulk text transformations** (regex, find-replace) — apply next. Example: first-person→third-person, case study bullet-lists→prose.
4. **New content insertion** — add summaries, new topic sections, transitions, front matter. Do LAST on text (after all existing content has been settled). Each new section may have its own voice/tone constraints — write them in the author's voice, not the editor's.
5. **Visual enhancement** — generate B&W charts or diagrams. Use matplotlib with Agg backend (no display needed), save as PNG to a `charts/` directory. Number charts sequentially with descriptive names (e.g., `01-time-distribution.png`, `02-time-savings.png`). Create a caption dict in the build script mapping each filename to a "Figure N: ..." description. Insert chart references in the build script (not the markdown source) using marker comments like `[CHART:01-time-distribution]` so the build script calls `insert_chart(name)` which handles Image placement + caption rendering. Use consistent sizing: `CONTENT_W * 0.75` width for readability within margins.
6. **Build pipeline update** — rewrite the PDF/EPUB build script if needed. This is the FINAL step since it depends on content structure being finalized. Common enhancements:

   **TOC with page numbers**: SimpleDocTemplate builds sequentially, so page numbers aren't known during story assembly. Use a *two-phase approach*: (a) estimate pages by counting lines per chapter (~38 body lines per page on 8.5×11 letter with 1in margins, 12pt text), then (b) build TOC entries with estimated page numbers as paragraphs with dot leaders. Alternatively, build once to get `pdfinfo Pages`, then rebuild with known page numbers.

   **6"×9" book format sizing**: For standard trade paperback trim (6" × 9"), use ~275 words per page estimate. CSS: `@page { size: 6in 9in; margin: 1in; @bottom-center { content: counter(page); font-family: Georgia, serif; font-size: 9pt; } @top-center { content: "BOOK TITLE"; font-family: Georgia, serif; font-size: 8pt; } }`. Body font: 11pt Georgia, 1.6 line height, 4in max-width. TOC page estimate: Start at page 5 (after title, copyright, 2-page TOC), then `cumulative_words // 275`.

   **Table formatting with grid borders**: Use ReportLab's `TableStyle` with `GRID` command (0.8pt black lines) and `BOX` (1.2pt outer). Add header row shading (`BACKGROUND` + gray), `LINEBELOW` for header separator, `ROWBACKGROUNDS` for alternating rows, and `VALIGN: MIDDLE` for spreadsheet-style alignment. Font size can go down to 7.5pt for table cells.

   **Data entry fields**: For exercises/surveys where users should fill data, render as bordered single-cell tables or use underlined spaces (`___`) with consistent spacing. Keep font at 7.5pt minimum.

   **Page numbering**: Override `afterPage()` on a custom `SimpleDocTemplate` subclass. Use `canvas.drawCentredString()` at 0.5in from bottom. Skip front matter (cover, title, copyright) by checking page number.

   Includes: TOC with page numbers, table styling (border grids, alternating rows), page numbering in headers/footers, chart image insertion.

Example of why order matters: adding a 3-page book summary (step 4) changes page numbers, so the TOC page estimates (step 6) must come after. Chart generation (step 5) is independent and can parallelize with steps 3-4.

### 1. **Analyze Document Structure**
```python
# Read and understand the document's current structure
with open(filepath, 'r') as f:
    content = f.read()
lines = content.split('\n')

# Identify key sections, chapters, and patterns
```

### 2. **Pattern Identification**
Use regex to find specific text structures that need transformation:
```python
# Find transition sections with generic language
pattern = r'Between the memory of "([^"]+)" and the unfolding of "([^"]+)"'
matches = re.findall(pattern, content)
```

### 2B. **Bulk Automated Text Transformations**
For large-scale programmatic edits, prefer regex-based matching over `str.replace()`:
- **Character encoding pitfall**: `text.replace()` silently fails when Unicode characters differ (e.g., `'` U+2019 smart apostrophe vs `'` U+0027 ASCII apostrophe). Always use regex with flexible character classes for exact text matching.
- Use `re.compile()` with `search()` rather than `in` operator to handle encoding variants:
  ```python
  # Flexible: matches both smart and ASCII apostrophes
  pattern = re.compile(r"Bob[`'\\u2019]s family")
  match = pattern.search(text)
  ```
- **Context-dependent replacements**: When replacing first-person pronouns, distinguish between narration and quoted dialogue by tracking quote state character-by-character:
  ```python
  def fix_first_person(text):
      in_quote = False
      result = []
      for c in text:
          if c == '"': in_quote = not in_quote
          if not in_quote and text[i:i+2] == 'my' and not text[i+2].isalpha():
              result.append('his')
              continue
          result.append(c)
      return ''.join(result)
  ```
- Common transformation patterns:
  | Task | Approach |
  |------|----------|
- **First-person → third-person** | Process char-by-char tracking `"` state; replace `I`→`Bob`, `my`→`his`, `me`→`him`, `I'm`→`Bob was`, `I've`→`Bob had`, `I'll`→`Bob would`, `I'd`→`Bob had/would`, `I don't`→`Bob didn't`, `I didn't`→`Bob didn't`, `I could`→`Bob could`, `I was`→`Bob was`, `I had`→`Bob had`, `I knew`→`Bob knew`, `I remember`→`Bob remembered`, `I think`→`Bob thought`, `I felt`→`Bob felt`, `we`→`they`, `our`→`their`, `us`→`them`, `myself`→`himself`. **Reusable script at** `scripts/convert_to_third_person.py` — handles ALL patterns including contractions, multi-word phrases, and quote-state tracking. Usage: `python3 scripts/convert_to_third_person.py input.md output.md` |
  | Name changes | `str.replace()` is safe when names are unique text (e.g., Heather→daughter) |
  | Date removal | Use regex `r'(?<!\w)(19|20)\d{2}(?!\w)'` with context-aware rewrites for standalone years |
  | Passage deletion | Match opening and closing phrases with `[\s\S]*?` (non-greedy) to delete spans |
  | Context-dependent renames | Only rename when referring to specific individuals (e.g., Bobby→son only for Bob's child, not young Bob)

### 3. **Content Transformation**
Rewrite identified patterns with more personal, engaging language:
```python
def rewrite_transition(match):
    chapter_x, chapter_y = match.groups()
    
    # Generate personal, memoir-style transition
    transitions = [
        f"As I moved from reflecting on '{chapter_x}' to confronting '{chapter_y}', I found myself in that peculiar mental space where memories blend with anticipation...",
        f"Between the story of '{chapter_x}' and the unfolding of '{chapter_y}', my mind dwelled in that threshold where experience meets expectation...",
        # ... more variations
    ]
    return transitions[hash(match.group(0)) % len(transitions)]
```

### 4. **Section Repositioning**
Move content to improve narrative flow:
```python
def move_section(current_index, target_index):
    # Extract section content
    section_lines = []
    i = current_index
    while i < len(lines):
        section_lines.append(lines[i])
        # Stop when reaching next section or chapter
        if i > current_index and (lines[i].startswith('##') or lines[i].startswith('# Part')):
            break
        i += 1
    
    # Remove from original position
    del lines[current_index:i]
    
    # Insert at target position
    lines = lines[:target_index] + section_lines + lines[target_index:]
```

### 5. **Front Matter Management**
Add or move introductory content:
```python
def add_or_move_front_matter(content, new_content, position=2):
    # Insert new content after title page
    if lines and lines[0].strip() == "# The Future is Unwritten":
        insert_position = 2
    else:
        insert_position = 0
    
    lines = lines[:insert_position] + new_content_lines + lines[insert_position:]
```

### 7. **Output Format Rebuild**

After editing, regenerate the distribution format (EPUB, HTML, or PDF).

**Critical: Strip Markdown Artifacts from Rendered Headings**

When converting markdown to HTML manually (not using a library like `markdown.markdown()`), `# Part One` must become `<h1>Part One</h1>` — NOT `<h1># Part One</h1>`. The same applies to `## Chapter` → `<h2>Chapter</h2>`.

```python
if s.startswith('# Part ') or s.startswith('# Final Section'):
    text = s.lstrip('#').strip()  # Removes the leading # and whitespace
    html += f'<h1>{text}</h1>\n'
elif s.startswith('## Chapter '):
    text = s.lstrip('#').strip()
    html += f'<h2>{text}</h2>\n'
```

After PDF generation, verify no stray `#` appear in the rendered text:
```bash
pdftotext output.pdf - | grep -n '#'
```
Any hits need fixing — either the markdown source or the HTML generator.

**EPUB conversion script pattern:**
A standalone `convert_to_epub.py` script that takes: markdown file path, output EPUB path, title, author, optional cover image path. It creates a valid EPUB3 with mimetype, META-INF/container.xml, CSS stylesheet, XHTML files per chapter, TOC/nav document, content.opf manifest, and spine ordering. Key details:
- `mimetype` must be first in the ZIP archive with `ZIP_STORED` (no compression)
- Use `zipfile.ZipInfo` to set mimetype as uncompressed
- Chapter slugs from heading titles via `slugify()`
- CSS handles page-break-before on chapter headings, proper typography for body text, centered chapter titles
- Include `dc:identifier`, `dc:title`, `dc:creator`, `dc:language`, `dc:date` in metadata
- Use `urn:uuid:` for unique identifier
- `python3 convert_to_epub.py input.md output.epub "Title" "Author" cover.png`

**PDF: Run conversion only after ALL text edits are finalized
**PDF: Use the WeasyPrint build script pattern (see §7B below)**
- Verify the output file exists and has expected size
- For EPUB: ensure cover image path is correct and accessible
- Deliver via MEDIA: prefix for Telegram delivery

### 7B. **PDF Generation with Cover Page + Chapter Images (WeasyPrint)**

For print-ready review PDFs with embedded cover image AND chapter images, use WeasyPrint with paged media CSS.

**Two approaches for inserting chapter images:**

**Approach A: Markdown image references (simpler)**
Before converting to HTML, insert `![alt](path)` references in the markdown after each chapter heading:
```python
for ch_title, img_file in chapter_images.items():
    img_path = f"/path/to/images/{img_file}"
    if not os.path.exists(img_path): continue
    for pattern in [f"\n# {ch_title}", f"## {ch_title}"]:
        idx = md.find(pattern)
        if idx >= 0:
            line_end = md.find('\n', idx)
            img_md = f"\n\n![{ch_title}]({img_path})\n\n"
            md = md[:line_end] + img_md + md[line_end:]
            break
```

**Approach B: Insert in post-HTML (for finer control)** — Use BeautifulSoup after markdown-to-HTML conversion.

**Full build script pattern:**
```python
import markdown, os
from weasyprint import HTML

# 1. Read markdown
with open(input_md) as f: md = f.read()

# 2. Insert chapter images as markdown references
chapter_images = {
    "Chapter 1:": "chapter1_tesla_coil_bw.png",
    "Chapter 2:": "chapter2_dog_portrait_bw.png",
    # ... map each chapter heading to its image file
}
for ch_title, img_file in chapter_images.items():
    img_path = f"/path/to/images/{img_file}"
    if not os.path.exists(img_path): continue
    for pattern in [f"\n# {ch_title}", f"## {ch_title}", f"\n### {ch_title}"]:
        idx = md.find(pattern)
        if idx >= 0:
            line_end = md.find('\n', idx)
            md = md[:line_end] + f"\n\n![{ch_title}]({img_path})\n\n" + md[line_end:]
            break

# 3. Convert to HTML
html_body = markdown.markdown(md, extensions=['extra', 'smarty', 'toc', 'sane_lists'])

# 4. CSS with proper paged-media controls
css = '''
@page {
    size: A4;
    margin: 2.2cm 2.5cm;
    @bottom-center { content: counter(page); font-family: Georgia, serif; font-size: 10pt; color: #555; }
    @top-center { content: "Book Title - Author"; font-family: Georgia, serif; font-size: 8pt; color: #999; }
}
@page:first { @top-center { content: none; } @bottom-center { content: none; } }
body { font-family: Georgia, serif; font-size: 12pt; line-height: 1.7; color: #111; orphans: 3; widows: 3; text-align: justify; }

/* Cover page */
.cover-page { page-break-after: always; text-align: center; width: 100%; height: 100%; }
.cover-page img { width: 100%; height: auto; max-height: 100vh; object-fit: contain; }

/* Chapter images - prevent page break between image and heading */
img { max-width: 100%; height: auto; display: block; margin: 0.5cm auto 1cm auto; page-break-inside: avoid; page-break-after: avoid; }
img + h1, img + h2, img + h3 { page-break-before: avoid; }  /* prevent double page break */

/* Headings */
h1 { text-align: center; font-size: 20pt; margin-top: 2.5cm; page-break-before: always; font-weight: bold; }
h1:first-of-type { page-break-before: avoid; }
h2 { text-align: center; font-size: 16pt; margin-top: 2cm; page-break-before: always; font-weight: bold; }
h3 { font-size: 13pt; margin-top: 1.2cm; page-break-after: avoid; }
h4 { font-size: 12pt; margin-top: 0.8cm; font-weight: bold; font-style: italic; }

/* Body text */
p { margin: 0.15em 0; text-indent: 1.5em; }
h1 + p, h2 + p, h3 + p, h4 + p { text-indent: 0; }

blockquote { font-style: italic; margin: 0.8em 2em; color: #555; border-left: 3pt solid #bbb; padding-left: 1.2em; }
hr { border: none; border-top: 1pt solid #ddd; margin: 1cm 4cm; }
'''

# 5. Build HTML document
html = '<!DOCTYPE html><html><head><meta charset="UTF-8"><title>Book Title</title><style>' + css + '</style></head><body>'
html += '<div class="cover-page"><img src="file://' + cover_image + '" alt="Cover"/></div>'
html += '<div class="copyright-page"><h1>Book Title</h1><p>By Author</p><p>Copyright &copy; 2025</p></div>'
html += html_body + '</body></html>'

# 6. Generate PDF
HTML(string=html).write_pdf(output_path)
```

**Key details:**
- Use `file://` absolute paths for cover image (WeasyPrint needs full paths)
- `img + h1 { page-break-before: avoid; }` prevents double page breaks when a chapter heading follows an image
- `@page:first { @top-center { content: none; } }` hides headers on the cover page
- Use smaller B&W images for print PDFs (~800KB each) vs full-color (~2MB each) to keep file size manageable
- Avoid f-string syntax for CSS (braces `{}` conflict) — use string concatenation

**TOC page-break prevention:**
If the Table of Contents has page breaks splitting chapter titles across pages, add:
```css
/* Prevent page breaks inside TOC content */
ul, ol { page-break-inside: avoid; }
```

**Two-Pass TOC Resync from PDF (Verified Page Numbers):**

Estimated TOC page numbers (~275 words/page) are often wrong after the first PDF generation. Use this two-pass workflow to get accurate page numbers and regenerate:

**Pass 1:** Generate the initial PDF from your HTML source.
**Pass 2:** Extract exact chapter start pages from the PDF using `pdftotext` with per-page targeting, then rebuild the HTML TOC and regenerate.

```python
import subprocess

pdf_path = "output.pdf"

# Pass 2: Find each chapter's body start page
# Use a unique content snippet from each chapter (not the title — titles appear in the TOC)
chapters = [
    ("Ch 1", "Chapter One: The Shock", "unique body text for Ch 1"),
    ("Ch 2", "Chapter 2: The Echoes", "unique body text for Ch 2"),
    # ... one entry per chapter with a unique content marker
]

chapter_pages = {}
for short, header, marker in chapters:
    for pg in range(1, 165):  # Search all pages
        r = subprocess.run(['pdftotext', '-f', str(pg), '-l', str(pg), pdf_path, '-'],
                          capture_output=True, text=True, timeout=10)
        text = r.stdout.strip()
        body = text.replace('Tomorrow Is Still Open', '').replace(str(pg), '')
        if marker.lower() in body.lower():
            chapter_pages[header] = pg
            break

# Update HTML TOC with verified page numbers
# Replace the old `<div class="toc">...</div>` with new entries
```

**Key insight for content markers:** The chapter title text appears in the TOC (page 1), so searching for it finds page 1 for every chapter. Instead, search for a **unique sentence or phrase** from the chapter's body content that won't appear elsewhere.

**Pitfall — Running header interference:** When the PDF has running headers (`@top-center`), `pdftotext` extracts them on every page. Strip the running header text before searching:
```python
body = text.replace('TOMORROW IS STILL OPEN', '').replace(str(pg), '')
```

**Pitfall — Chapter title in running header:** If the PDF uses `@top-center` that includes the chapter title, every page will match that chapter. Verify matches by checking `body.count(chapter_title) > 0` after removing the running header — if it appears only once, that's the actual chapter heading page.

**PDF verification:**
```bash
# Check page count and metadata
pdfinfo output.pdf

# Extract text from first/last pages to verify content
pdftotext output.pdf - -l 5 | head -20   # First 5 pages
pdftotext output.pdf - -f 90 | head -20   # Page 90 onwards
```

**If the first PDF attempt seems empty or missing content:**
- Count chars in the HTML body to verify conversion preserved everything
- Check stylesheet doesn't hide content (`overflow: hidden`)  
- Try A4 instead of A5 if text appears too compressed
- Extract text with `pdftotext` and compare word count to source markdown

## Common AI-Generated Artifact Patterns (Memoir/Creative Non-Fiction)

When reviewing manuscripts that used AI assistance, check for and remove these templated transition artifacts that indicate AI-generated placeholder text:

### Pattern Group 1: "Psychological Threshold" variants
- `"The journey from 'X' to 'Y' carried him through a psychological threshold where past and future meet."`
- `"Between 'X' and 'Y', his mind dwelled in the space between what was and what will be."`
- `"The shift from contemplating 'X' to engaging with 'Y' carried him through a psychological threshold."`
- `"As he left 'X' behind and turned toward 'Y', he found himself in that liminal space where..."`
- `"As he moved from reflecting on 'X' to confronting 'Y', he found himself in that peculiar mental space where memories blend with anticipation."`
- `"Between the story of 'X' and the unfolding of 'Y', his mind dwelled in that threshold where experience meets expectation."`
- `"These liminal spaces, as he's come to call them, are where the real work of understanding happens."`

### Removal Technique
```python
artifact_patterns = [
    r"The journey from '[^']*' to '[^']*' carried .*?threshold where past and future meet\.",
    r"Between '[^']*' and '[^']*', his mind dwelled .*?between what was and what will be\.",
    r"The shift from contemplating '[^']*' to engaging with '[^']*' carried .*?psychological threshold\.",
    r"As .*? left '[^']*' behind and turned toward '[^']*', .*? found (myself|himself) .*?liminal space.*",
    r"As .*? moved from reflecting on '[^']*' to confronting '[^']*', .*? found (myself|himself) .*?memories blend with anticipation\.",
    r"Between the story of '[^']*' and the unfolding of '[^']*', .*?mind dwelled.*threshold.*",
    r"The journey from '[^']*' to '[^']*' carried .*?psychological threshold.*",
    r"Between '[^']*' and '[^']*', .*?mind dwelled .*?never static.*",
    r"These liminal spaces.*",
]
for pattern in artifact_patterns:
    manuscript = re.sub(pattern, '', manuscript, flags=re.DOTALL)
```

### Pattern Group 2: "Between the memory of X and the unfolding of Y"
- `"Between the memory of 'X' and the unfolding of 'Y', my mind rested in a space of integration."`
- `"Leaving behind 'X' and turning toward 'Y', I inhabited a mental landscape where..."`
- `"Moving from 'X' to 'Y', I inhabited what I've come to think of as..."`

### 6B. **Appending a New Final Section** (Memoir/Creative Non-Fiction)

When the user provides a new standalone section to append as the ending of an existing memoir or creative non-fiction book:

#### Step 1: Find the Natural Cut Point
Identify the existing manuscript's ending — typically a final paragraph, a closing line like "That is enough.", or the natural end of the narrative before the epilogue/back matter.

```python
cut_marker = "That is enough."
cut_idx = manuscript.find(cut_marker)
if cut_idx >= 0:
    manuscript = manuscript[:cut_idx + len(cut_marker)]
```

#### Step 2: Remove Old Epilogue & Artifacts
Strip everything after the cut point — old epilogues, AI transition artifacts, extraneous front matter that doesn't belong.

```python
# Remove TOC/front matter from middle of manuscript
toc_end = manuscript.find("### First real chapter header")
toc_start = manuscript.find("Table of Contents")
if 0 <= toc_start < toc_end:
    manuscript = manuscript[:toc_start] + manuscript[toc_end:]

# Remove artifact patterns (see Pattern Group 1 above)
for pattern in artifact_patterns:
    manuscript = re.sub(pattern, '', manuscript, flags=re.DOTALL)

# Clean excess blank lines
manuscript = re.sub(r'\n{4,}', '\n\n\n', manuscript)
```

#### Step 3: Write a Transition Paragraph
Compose a short (1-3 paragraph) transition that:
- Acknowledges the story has reached its natural conclusion
- References a specific image from the book's closing (e.g., "Bob closes the document", "Cindy calls from downstairs", "dinner on the table")
- Looks forward rather than backward (distinguishing this from an epilogue)
- Introduces the new section as Bob's imagination/gift to future generations

```markdown
---

## The Threshold

[Character reference from ending]. [Domestic scene — ordinary, daily].

But a story this size does not end at [the dinner table]. [Metaphor about the life's wake traveling forward]. [Hook into new section].

What follows is not Bob's memory. It is Bob's imagination — offered to the generations who will inherit what he could only dream of building.

---

```

#### Step 4: Append New Content
Add the user-provided section directly after the transition, maintaining its original formatting.

```python
manuscript = manuscript.strip() + transition + "\n\n" + new_section_content
```

#### Step 5: Update Table of Contents
The TOC may be embedded in the manuscript markdown or generated programmatically. If inline, update it by appending an entry for the new section. If programmatic, adjust the TOC generation code to include the new section's subsection headers.

**For inline TOC:** Find and append:
```python
toc_match = re.search(r"(?s)(Table of Contents.*?)(?=\n\n###|$)", manuscript)
if toc_match:
    new_toc = toc_match.group(0).rstrip() + "\nFinal Section: The Future After Bob ......... 501"
    manuscript = manuscript.replace(toc_match.group(0), new_toc)
```

**For programmatic TOC:** Extract headings from the new section and add them to the TOC entries list before generating HTML.

#### Step 6: Rebuild All Output Formats
Regenerate HTML, PDF, and EPUB from the updated manuscript. Verify the new section is included, the TOC reflects the change, and no old endings survived the cut.

### 6C. **Splitting a Final Section into Continuation Chapters** (Memoir/Creative Non-Fiction)

When a manuscript has a final "future-looking" section with multiple subsections (e.g., 16 subsections imagining different future scenarios) that should become proper numbered chapters continuing from the previous chapter sequence.

**When to Use:** The manuscript ends with a single large section containing 8+ subsections (e.g., `## The Empty Chair`, `## The Children of the Assistant Age`). The user wants: "break into N separate chapters, each with M future tech sections." The new chapters should continue the existing numbering (e.g., Chapters 13-16 follow Chapter 12).

**Workflow:**
1. Count the subsections and divide evenly: total_subsections // target_chapters = subsections per chapter
2. Name each new chapter with a thematic title that reflects its subsection topics
3. Replace the single section header with new chapter headers using `## Chapter N:` format
4. Preserve all subsection content — do not cut, compress, or rewrite anything
5. Verify total subsection count across new chapters equals original count
6. Add all new chapter entries to the TOC with page number estimates

**Example split (16 subsections → 4 chapters):**
```
## Chapter 13: Echoes of Tomorrow     (subsections 1-4)
## Chapter 14: The Human Horizon      (subsections 5-8)
## Chapter 15: The World Remade       (subsections 9-12)
## Chapter 16: Inheritance            (subsections 13-16)
```

### 7. **Inserting New Content (e.g., Physiological/Historical Transitions)**

When adding original transitional content to a manuscript (rather than just editing existing text), follow this pattern:

**Transition structure for memoirs:** Each transition should weave together three threads:
1. **Historical context** — the broader world events happening at the time of the adjacent content
2. **Physiological effects** — the body's biological response (cortisol, oxytocin, adrenaline, dopamine, amygdala activation, hippocampal encoding, etc.)
3. **Narrative bridge** — connecting the emotional arc of what came before to what follows

**Example pattern (use as a template for generating similar transitions):**
```markdown
### Transition: [Thematic Title]

The physiology of [topic] is a lesson in the biology of [emotion/response]. Every [action] Bob took triggered a release of [neurotransmitter/hormone] — not merely [simple explanation], but the neural signature of [deeper meaning]. The [brain region], that ancient sentinel of the brain, registered each [stimulus] as a [cognitive appraisal]. He did not know this vocabulary then. He only knew the specific feeling of [visceral description].

The historical context of his era — [specific historical detail about the period] — gave his efforts a gravity he could not fully appreciate at the time. He was [action], brick by brick, [metaphor], in a world that would soon [future change]. The body remembers what the mind forgets: [specific physical sensation], [another sensation], the strange exhilaration of [unexpected positive feeling].
```

**Key elements to include in each transition:**\n- A specific neurotransmitter/hormone: cortisol (stress), oxytocin (bonding), dopamine (reward), adrenaline (fear/excitement), serotonin (mood)\n- A brain region: amygdala (threat detection), hippocampus (memory), prefrontal cortex (decision-making), hypothalamus (stress response)\n- A historical reference specific to the era: political events, technological changes, cultural shifts\n- A visceral physical sensation that connects the reader to the body's experience\n\n**Expanding existing transitions to a target character count:**\nWhen transitions already exist but need to be substantially longer (e.g., ~12,000 chars for a memoir), use this marker-based insertion pattern:\n1. Find a unique text marker near the end of the existing transition (e.g., "This is the physiology of hope:")\n2. Append additional content after that marker using `text.replace()` or regex\n3. The additional content should weave together: historical context of the era, physiological mechanisms (specific hormones, brain regions, nervous system responses), sensory details (smells, sounds, physical sensations), and narrative reflection\n4. Each additional block should be 4,000-6,000 chars of new content that seamlessly continues from the marker\n5. After expanding ALL transitions in one pass, verify each with a character count check\n\n```python\nextra_text = \"\"\"\nThe smell of solder smoke clinging to his clothes after a long shift. The particular ache in his fingers from gripping tools for hours. These sensory memories were not incidental details; they were the building blocks of an identity. Each successful repair confirmed something essential: that he was the kind of person who could figure things out, who could face complexity without being overwhelmed, who could persist through frustration until the problem yielded.\n\nThe historical moment of his education gave his struggle a particular texture. He was coming of age in the twilight of the post-war American consensus, when a university degree was still a reliable ladder to the middle class, when hard work was still widely believed to guarantee advancement.\n\"\"\"\n\n# Find marker and insert extra content after it\nmarker = \"This is the physiology of hope:\"\nsection_start = md.find(\"### Transition: The Cost of Dreams\")\nsection_end = md.find(\"\\n\\n### \", section_start + 50)\nsection = md[section_start:section_end]\ninsertion_point = section.find(marker)\nif insertion_point >= 0:\n    actual_pos = section_start + insertion_point + len(marker)\n    md = md[:actual_pos] + \"\\n\\n\" + extra_text + \"\\n\\n\" + md[actual_pos:]\n\n# Verify length\nfor name in [\"Cost of Dreams\", \"Weight of New Life\"]:\n    s = md.find(f\"### Transition: {name}\")\n    e = md.find(\"\\n\\n### \", s + 50)\n    if e < 0: e = len(md)\n    print(f\"{name}: {len(md[s:e])} chars\")\n```

### 5B. **Bullet List → Prose Conversion** (Case Studies & Reference Chapters)

When converting bullet lists to flowing prose in case studies (or entire reference chapters like AI Ethics), apply this pattern:

1. **Identify the list header** — bold line like `**Time Audit Findings:**` or `**Practical guidance:**`
2. **Read all bullet items** under that header (lines starting with `- `)
3. **Replace the entire list** (header + bullets) with a single prose paragraph that:
   - Starts with the bold header intact: `**Time Audit Findings:**`
   - Continues with a flowing narrative that connects items with transitions like "including", "such as", "paired with", "alongside"
   - Keeps ALL original information — just changes format
   - Writes in the chapter's established voice (practical, direct)
   - Uses proper punctuation and sentence flow

**Example conversion:**

BEFORE:
```
**AI Implementation:**
- Implemented a phone AI assistant for orders
- Used inventory prediction software
- Automated social media scheduling
```

AFTER:
```
**AI Implementation:**
Maria's team implemented a phone AI assistant for orders and common questions, paired with inventory prediction software integrated directly with their POS system, and automated social media scheduling with AI-powered content suggestions.
```

**Scope rules:**
- Convert ONLY unordered lists (`- ` prefix items) — NOT numbered lists (`1. `, `2. `)
- Do NOT convert tables or appendix content
- Merge WITH the preceding bold header if one exists
- If there's a lead-in sentence between the header and the list, merge it into the prose

### 5C. **Title/Author Change Propagation** (Multi-file)

When changing a book's title, subtitle, or author name, update ALL of these files:

| File | What to Change |
|------|---------------|
| `Compiled.md` | Line 1 (`# Title`), subtitle (`*...*`), closing line (`"Thank you for reading..."`) |
| `build_manuscript.py` | `TITLE =`, `AUTHOR =`, sSubtitle text, sCopyright text, sBackSub text, EPUB body_epub heading, back cover review author name, TOC entries referencing author |
| `generate_cover.py` | Prompt text with book name |
| `apply_cover_text.py` | Title words list, subtitle lines, author string |
| `FRONT_MATTER.md` | Title/author references |
| `outline.md` | Title/author references |
| Individual chapter files | Opening/front matter references |

**Safety check after changes:** Search across the entire project directory for old title/author strings:
```bash
grep -r "Old Title\|Old Author" /path/to/project/ --include="*.md" --include="*.py" --include="*.sh"
```

**Common patterns to catch:**
- `"Thank you for reading \"Old Title\""` — closing line in the last chapter
- `"Introduction by OLD AUTHOR"` — heading and TOC entries
- Old subtitle in copyright, back cover, and EPUB body
- Image filename patterns that embed the old title

### 5D. **Author Name Update via Introduction Signatures**

When changing the author name (e.g., "Robert Mills" → "Bob Mills"), update these specific locations:

1. `Compiled.md`: `## Introduction by [Old Name]` heading → new name
2. `Compiled.md`: `— [Old Name]` closing signature → new name
3. `build_manuscript.py`: `AUTHOR = "..."` variable
4. `build_manuscript.py`: skip list entry `'Introduction by [Old Name]'` → new name
5. `build_manuscript.py`: TOC entry `'title': 'Introduction by [Old Name]'` → new name
6. `build_manuscript.py`: Back cover review: `"[Name] has done something remarkable..."` → new name
7. `build_manuscript.py`: Comment `# INTRODUCTION (by [Old Name])` → new name

Always search for remaining occurrences with `grep -rn "Old Name" /project/path --include="*.py" --include="*.md"` after making changes.

- **Always work from a clean source copy** — create a copy of the original source file before making edits (e.g., `WORKING.md` = copy of `COMPLETE.md`). If the user says "go back to before [X]", restart from the pristine original, not from a partially-modified file. Each new set of edits should start from the unmodified source.
- When expanding transitions to a target character count, **identify each transition by title** and verify character count after expansion. Default target is ~5000 chars per transition (~2000 words).
- For memoir transitions with history + physiology content, prepare **9 transition sections** covering: childhood→Sputnik, Sputnik→garage, garage→technology, high school→university, college→career, career→fatherhood, stability→illness, grief→new relationship, and epilogue bridge.
- Test on small samples first
- Verify changes don't break document structure
- Handle edge cases (multiple occurrences, nested patterns)
- Use hash-based selection for consistent variation choices
- **Order of operations is critical**: structural edits → bulk text transforms → new content insertion → format rebuild. Reversing this order causes cascading failures.
- **After bulk transforms, always do a quick sanity check**: grep for remaining first-person pronouns, check for "his his" or "Bob Bob" artifacts, verify quoted dialogue wasn't corrupted.
- **Save the final transformation script** alongside the manuscript for reproducibility. If edits need to be re-applied, having the exact Python script avoids re-doing the work.

### 7D. **Integrating Raw User-Provided Autobiographical Content** (Memoir/Creative Non-Fiction)

When the user provides unedited, raw autobiographical text (typos, stream-of-consciousness, non-standard formatting) and asks you to integrate it into an existing memoir manuscript:

**When to Use:**
- User provides raw narrative text (bullet points, stream of consciousness, rough notes) about their life
- The text needs rewriting in the manuscript's established voice and style
- The new material must fit chronologically without conflicting with existing content
- Front matter metadata (subtitle, author name) may also need updates

**Do NOT use for:** Clean chapter files (use `insert-chapters-into-manuscript` skill instead), fictional content, or content where the original text must be preserved verbatim.

#### Step 0: Survey the Existing Manuscript First

Before writing anything, read the current manuscript and identify:
- **All existing chapters/sections** — list them with their chronological timeframes
- **Existing content on the same topics** — search for keywords related to the new material (e.g., "weight", "food", "friend", "rocket", "scout", "drill", "boat")
- **The book's narrative voice** — first-person or third-person? Reflective or immediate? How are scenes structured (summary-only or scene-with-dialogue)?
- **Existing overlap** — is there already a version of this story in the book? If so, plan to merge rather than duplicate

Use `grep` across the manuscript to find potential overlaps:
```bash
grep -n "keyword1\|keyword2\|keyword3" manuscript.md | head -30
```

#### Step 1: Audit for Redundancy

For each piece of user-provided content, ask:
1. Does a version of this story already exist in the manuscript?
2. If yes, does the user's version add new details (neuroscience, therapy, specific numbers, emotional texture) that should be integrated into the existing passage?
3. If the existing version is more complete, can the user's version be condensed to just the new facts?
4. Mark each piece as: **NEW** (does not exist yet), **MERGE** (adds to existing story), or **SKIP** (fully covered already)

#### Step 2: Place Chronologically

Map each new piece to where it fits in the existing timeline:
- Identify the year/age for each piece
- Find the existing chapter or section that falls immediately before that timeframe
- Decide: insert as a new `###` subsection within an existing chapter, or as a standalone section between chapters?
- For subsections: use `### Heading` to match the manuscript's existing heading hierarchy
- For standalone sections: use a thematic break (`---`) before and after, plus a clear heading

**Typical placements for memoir content:**
| Content Era | Likely Position |
|-------------|----------------|
| Early childhood (ages 5-9) | Part One, between existing early chapters |
| Pre-teen / early teen (ages 10-14) | Part One ending or Part Two beginning |
| Late teen / early adult (ages 15-25) | Part Two, between chapters |
| Young adult / early career (ages 25-35) | Between Part Two and Part Three, or early Part Three |

#### Step 3: Rewrite Raw Text in Book's Voice

Transform the user's raw text using the manuscript's established patterns:

**Raw input pattern (what the user provides):**
- Run-on sentences, missing punctuation, inconsistent capitalization
- Stream-of-consciousness, emotional but unstructured
- Typos, phonetic spellings, dropped words
- Contradictory details that need reconciliation

**Rewrite rules:**
1. **Fix grammar and structure** — complete sentences, proper punctuation, consistent tense
2. **Match the existing voice** — if the book uses first-person ("I remember"), rewrite in first-person. If the book uses present-tense reflection, match that.
3. **Add sensory detail** — what did things look like, smell like, feel like? The user's raw text will have emotional content but may lack sensory anchors.
4. **Remove clinical/psychology framing** — if the raw text says "neuroscientific research links to memory circuits," integrate it as personal realization rather than academic citation (matching the book's existing approach to science content)
5. **Cut redundant exposition** — if something was already explained earlier in the book, reference it briefly instead of re-explaining
6. **Add connective tissue** — write a sentence or two that bridges from the preceding section to this new one

**Voice consistency checklist:**
- [ ] Pronouns match the book (first-person: I/my/me; third-person: Bob/his/him)
- [ ] Tense is consistent (memoir often uses past-tense narration with present-tense reflection)
- [ ] Sentence length and complexity match surrounding paragraphs
- [ ] No abrupt style shifts between old and new material

#### Step 4: Insert Into Manuscript

Python insertion pattern using line-level operations (NOT read_file which corrupts format):

```python
with open(md_path) as f:
    lines = f.readlines()

# Find insertion point: line containing the target marker
insert_at = None
for i, line in enumerate(lines):
    if "Part Two: The Building" in line:  # or some other marker
        insert_at = i
        break

# Insert new content before the marker
new_section = "\n\n### New Section Title\n\nContent here...\n\n---\n\n"
new_lines = new_section.split("\n")
lines[insert_at:insert_at] = new_lines

with open(md_path, "w") as f:
    f.write("\n".join(lines))
```

**IMPORTANT:** Never use `read_file` from Hermes tools for file editing — it returns content with line-number prefixes (`    73|content`). Instead, use `terminal()` or `write_file()` with direct Python file I/O to read and write manuscript files.

#### Step 5: Fix Chapter Numbering Format

If the build script expects word-format chapter numbers ("Chapter Two") but the manuscript uses numeric format ("Chapter 2"), convert them:
```python
num_to_word = {"2":"Two","3":"Three","4":"Four","5":"Five","6":"Six","7":"Seven",
               "8":"Eight","9":"Nine","10":"Ten","11":"Eleven","12":"Twelve",
               "13":"Thirteen","14":"Fourteen","15":"Fifteen","16":"Sixteen"}
for i, line in enumerate(lines):
    stripped = line.strip()
    for num, word in num_to_word.items():
        if stripped.startswith(f"Chapter {num}:"):
            lines[i] = stripped.replace(f"Chapter {num}:", f"Chapter {word}:", 1)
            break
```

#### Step 6: Update Front Matter Metadata

If the subtitle or author name changed, update all locations:
1. The markdown source (subtitle line, author line)
2. The build script (title page HTML, TOC generation, metadata)
3. The copyright page text
4. Cover generation scripts (if applicable)

Search across the project for old strings:
```bash
grep -rn "Old Subtitle\\|Old Author" /project/path --include="*.py" --include="*.md"
```

#### Step 7: Rebuild and Verify

1. Run the build script to regenerate HTML and PDF
2. Verify chapter counts match expectations (`grep -c "chapter-title" output.html`)
3. Verify subtitle/author updated in the final output
4. Spot-check at least one new section in the rendered output
5. Build the KDP publishing package if required
6. Deliver via MEDIA: path

**Overlap check after insertion:**
After inserting new material, do a final pass to ensure the same story didn't accidentally end up in two places. Search for distinctive phrases from the new content within the original manuscript sections.

## Tools Required

- Python with `re` module for regex
- File I/O operations (direct, not through read_file tool which corrupts format)
- String manipulation functions
- Basic understanding of markdown structure

## Output Format

Returns the transformed manuscript content and a summary of changes made.

## Post-Cleanup Verification Checklist

After removing AI artifacts and before delivering the manuscript, run these checks:

```python
verification_checks = {
    "AI artifacts": ["Between the memory of", "liminal space", "memory reconsolidation",
                     "hippocampus and prefrontal cortex", "I didn't write this book",
                     "Total words:"],
    "Zero remaining": lambda content: all(p not in content for p in (
        "Between the memory of", "liminal space", "memory reconsolidation",
        "hippocampus and prefrontal cortex", "I didn't write this book"))
}

def verify_clean(content):
    remaining = []
    for pattern in verification_checks["AI artifacts"]:
        if pattern in content:
            remaining.append(pattern)
    if remaining:
        # Calculate line numbers and remove each
        for pattern in remaining:
            count = content.count(pattern)
            print(f"  ❌ '{pattern}' found {count} times — removing...")
    return len(remaining) == 0
```

**Post-restructuring checks:**
- ✅ All chapter headers are sequential (no gaps, no duplicates)
- ✅ No duplicate stories appear across multiple chapters
- ✅ Placeholder markers like "xx" or "TBD" or "..." are resolved
- ✅ Chapter title format is consistent (all "Chapter N:" or all "Chapter N — Title")
- ✅ Narrative voice is consistent within each chapter (no first/third-person switching)
- ✅ Part/PART headers are sequential and non-duplicated
- ✅ The Transition bridge sections are present and connect chapters
- ✅ Total word count is within expected range after compression

## Editorial Proposal-Driven Chapter Compression (Memoir/Non-Fiction)

## Editorial Proposal-Driven Chapter Expansion with Scene Work (Memoir/Non-Fiction)

When the user provides a list of specific editorial improvement proposals and asks you to rewrite a chapter by EXPANDING specific sections with scene work, sensory detail, and dialogue while preserving other sections intact.

### When to Use This Sub-Skill

- User provides a numbered list of editorial improvement proposals calling for **expansion** (e.g., "expand with scene work", "add sensory detail", "show not tell", "add connective tissue", "preserve section X intact")
- The chapter needs to grow from a shorter to longer word count (e.g., ~2,289 → ~2,600-2,800 words)
- Specific sections need to be **shown** as scenes rather than **summarized** as descriptions
- Some sections must be preserved word-for-word while others are expanded
- The task involves rewriting a memoir/creative non-fiction chapter, not fiction

### Workflow Steps

#### Step 0: Categorize the Editorial Proposals
Group each proposal into one of four action categories:

| Category | Example | Action |
|----------|---------|--------|
| **Preserve** | "Keep London section intact" | Do not modify these sections at all — preserve prose, voice, structure |
| **Expand with scene work** | "Show Nancy with dialogue, not describe" | Transform summary into scene with dialogue, sensory detail, specific moment |
| **Expand with sensory depth** | "Add 2-3 sentences of connective depth to Fermilab" | Layer in specific sensory detail (smells, sounds, physical sensations) |
| **Add vignette moments** | "Add 2-3 specific vignette moments" | Create small standalone scenes with dialogue, setting, emotional beat |
| **Connective tissue** | "Add transitions between sections" | Write bridge sentences/paragraphs connecting disparate sections |

#### Step 1: Identify Preserve-Zone Sections
Before rewriting, tag each section with its treatment:
- **🔒 PRESERVE** — Do not touch beyond minor grammar fixes
- **🔨 EXPAND** — Add scene work, sensory detail, dialogue
- **🌉 CONNECT** — Need bridge transitions to/from adjacent sections

Read the original chapter and mark which sections fall into each bucket. Block out the preserve sections mentally and never modify them during the rewrite.

#### Step 2: Transform Summary into Scene (Show, Don't Tell)
For sections marked for expansion with scene work:

**Before (summary):**
> Bob met Nancy in a grocery store when he was visiting his company's HQ in Michigan. She was standing near the eggs. Bob and Nancy talked for a few minutes and then went their separate ways.

**After (scene with dialogue):**
> I met Nancy in a grocery store in Michigan, on one of those trips home between flight test rotations. I was standing near the eggs — I remember that detail with absurd clarity, the way you remember the trivial things that frame the moments that change your life — when I noticed the woman next to me, studying the price tag with an expression of genuine outrage.
> "Can you believe these prices?" I said, because I had to say something. "Eggs are up, what, a hundred percent?"
> She looked at me. Not the quick glance of polite dismissal, but a real look, appraising and amused. "You're not from here," she said.
> "How can you tell?"
> "The eggs," she said, deadpan. "Only an out-of-towner starts a conversation about eggs."

**Key transformation rules:**
- Give the character **dialogue** that reveals personality (wit, warmth, intelligence)
- Add a **specific physical detail** about the setting (the dairy aisle, the price tag, the expression)
- Create a **moment of recognition** — something that signals "this is different"
- Use the pause/beat structure of real conversation

#### Step 3: Layer in Sensory Depth
For sections marked for expansion with sensory depth, add 2-5 sentences that engage the senses:

- **Smell**: ozone and solder in a control room, hydraulic fluid in a cockpit, disinfectant in a hospital
- **Sound**: the hum of cooling fans, the thud of a canopy sealing, the click of electronics
- **Touch**: vibration through a seat, the tightness of a cockpit, the cold of a server room
- **Sight**: green text on monitors, cornfields outside a lab window, leaves in autumn
- **Emotional weight**: the sacred feeling of being part of something larger, the hollow satisfaction of handoff

Each sensory detail should serve a narrative purpose — revealing something about the character's emotional state or the importance of the moment.

#### Step 4: Add Specific Vignette Moments
For sections marked for vignettes, write 2-4 standalone scenelets that:

1. **Anchor in a specific time/place**: "We were walking through a park near her apartment, late autumn, leaves piled gold and red along the path."
2. **Include a line of dialogue that reveals character**: "A house. A husband. A writing desk by a window. But the house and the husband were the wrong ones. The desk was the only part I got right."
3. **End with an emotional beat**: the moment of knowing, the shift in feeling, the recognition
4. **Advance the relationship**: each vignette should show the connection deepening

Good vignette placement: the moment they met, the moment they first had a real conversation, the moment he knew, the night before a separation, a specific shared experience.

#### Step 5: Write Connective Tissue Between Sections
Between sections that were originally abrupt, write bridge sentences/paragraphs that:

- **Contrast** the previous and next environments: "The transition was jarring. At Fermilab, the culture was academic — professorial, collaborative, unhurried. At Eglin, everything moved at the speed of jet exhaust."
- **Show the character's emotional state** at the transition point: "When the final handoff came, I felt a hollow satisfaction. The system worked beautifully. But it belonged to someone else now."
- **Use a physical action** to mark the transition: "I packed my desk, walked past the cornfields one last time, and drove away wondering what came next."

Avoid generic transition phrases like "meanwhile," "later," "after that." Use specific imagery from the setting being left behind.

#### Step 6: Preserve Voice Consistency
When expanding sections, maintain consistent narrative voice:

- For a **first-person memoir**: all new expansion must be in first-person (I, my, me) — but leave quoted dialogue in the speaker's natural voice
- For a **third-person biography**: stay in third-person
- The preserved sections set the voice — match it exactly in all new material
- No "lecture voice" in expansions: avoid "As I reflect on this now..." or academic framing

#### Step 7: Hit the Expansion Word Count Target
Write the full rewrite in one pass, then check word count:

- If **under target**: Add more sensory detail to the thinnest section, or add another vignette moment
- If **over target**: Tighten connective tissue and vignette descriptions without removing the scene-dialogue-emotional beat structure

Target within ~50 words of the requested range. Favor landing closer to the top of the range when expanding (the goal is richness, not tightness).

#### Step 8: End-of-Rewrite Verification

Run this checklist before delivering:
- [ ] Preserve-zone sections are verbatim (aside from minor grammar/consistency fixes)
- [ ] Expanded sections have dialogue + sensory detail + emotional beat
- [ ] Vignette moments are specific (time, place, dialogue, feeling)
- [ ] Connective tissue bridges abrupt section transitions
- [ ] Word count is within target range
- [ ] Voice is consistent throughout (no drift between old and new material)
- [ ] All original facts preserved (dates, names, locations unchanged)
- [ ] No AI lecture-voice introduced in expansions
- [ ] Grammar fixes applied throughout (no "returned back", "could of", double words, etc.)

### Expansion Patterns Reference

| Summary → Scene |
|----------------|
| "Bob met Nancy in a grocery store" → scene with dialogue about eggs, her deadpan humor, the laughter, the moment of connection |
| "They talked and went their separate ways" → "I spent the next three days kicking myself for not asking for her number" |
| "He learned the systems intimately" → "I spent my days in a windowless control room, surrounded by racks of electronics that hummed and clicked like living things. The air smelled of ozone and solder." |

| Thin Description → Sensory Depth |
|-----------------------------------|
| "He worked on avionics integration" → "The cockpit was tight, switches and dials packed so densely it felt like sitting inside a circuit diagram. The canopy sealed shut with a thud that cut off the outside world." |

| No Transition → Connective Tissue |
|------------------------------------|
| "The job ended." → "When the final handoff came, I felt a hollow satisfaction. The system worked beautifully. But it belonged to someone else now. I packed my desk, walked past the cornfields one last time, and drove away wondering what came next." |

### Common Pitfalls

| Pitfall | Solution |
|---------|----------|
| Accidentally modifying preserve sections | Block them out mentally. After writing, diff against original to confirm preserves. |
| Adding dialogue that doesn't match the character's voice | Base dialogue on any existing dialogue in the preserved sections for tone. |
| Expanding without adding emotional weight | Each expansion should do double duty: add detail AND reveal character/emotion. |
| Breaking narrative voice between new and old material | Read the entire chapter aloud after writing — voice breaks are audible. |
| Losing track of the word count target during expansion | Write generously first, then trim to fit. |
| Introducing new facts not in the original | Never add new biographical details. Expand only what's already implied. |

### Editorial Proposal-Driven Hybrid Chapter Revision (Mixed Operations)

When the user provides a numbered list of editorial proposals that require BOTH compression (some sections) AND expansion (other sections) on the SAME chapter — plus fixes like placeholder titles, duplicate-story deduplication, and style upgrades. This is the most common real-world editorial scenario: a chapter that's over-length but has thin scenes, contains a duplicate from another chapter, and has a placeholder that needs resolving.

#### When to Use This Sub-Skill

- User provides a numbered list of editorial improvement proposals for one chapter
- The proposals include a **mix** of operations on different sections: compress X, expand Y, fix Z, deduplicate W, smooth pacing, upgrade style
- Some sections need to be **compressed** (tightened, excess removed) while others need **expansion** (sensory detail, scene work)
- There are specific editorial housekeeping items: placeholder titles ("Chapter xx"), duplicate stories, cross-chapter references
- There is a target word count range (usually compressed overall despite localized expansions)
- The chapter section structure (subheadings) should be **preserved** — you're polishing content, not restructuring

**Do NOT use for:** Pure compression jobs (use the compression sub-skill above), pure expansion jobs (use the expansion sub-skill above), structural reorganization (use the main skill sections), or bulk automated transforms.

#### Workflow Steps

##### Step 1: Parse the Proposal List

Read the user's numbered proposals and categorize each into one of five action types. Use a table like this:

| Proposal | Type | Section Affected | Action |
|----------|------|-----------------|--------|
| "Expand hangar fire scene slightly" | 🔨 EXPAND | The Fire | Add 2-4 sentences of sensory detail (smell, heat, sight, sound) |
| "Remove duplicate aplastic anemia story" | ✂️ DEDUP | A Sick Child | Replace full narrative with brief reference + cross-chapter note |
| "Fix 'Chapter xx' placeholder" | 🔧 FIX | Engineer vs. Executive | Find the heading with "xx" and replace with proper section title |
| "Compress from ~2,972 to ~2,500-2,700" | 📏 COMPRESS | Entire chapter | Tighten prose, cut redundancy, keep all storylines |
| "Smooth choppy pacing" | 🌉 CONNECT | Between sections | Add or strengthen transitional sentences/paragraphs |
| "Write in bestseller style" | 🎨 STYLE | Entire chapter | Upgrade prose: active voice, varied sentence rhythm, sensory anchors |

##### Step 2: Baseline Word Count and Compression Math

```bash
# Get current word count for just the chapter
# First isolate the chapter (between ## Chapter N: and the next chapter heading)
sed -n '/^## Chapter 7/,/^## Chapter 8/p' manuscript.md | head -n -1 | wc -w
```

Calculate:
- **Current word count** (e.g., ~2,972)
- **Target word count** (e.g., ~2,500-2,700)
- **Sections to compress** — these carry the weight of the word count reduction
- **Sections to expand** — these add a small amount, so extra compression is needed elsewhere
- **Net reduction needed** = current - target (e.g., ~300-500 words saved)

##### Step 3: Pre-Write — Identify and Verify Cross-Chapter Duplicates

If a proposal says "remove duplicate [story] — keep only brief reference," do this first:

1. **Search for the duplicate story** in other chapters:
   ```bash
   grep -n "Aplastic Anemia\|aplastic anemia" manuscript.md
   ```
2. **Read the other chapter's version** to confirm it contains the full telling
3. **Verify the other chapter's word count and quality** — if the other version is also thin, flag it; don't just assume it's complete
4. In your rewrite, replace the full duplicate with a **brief reference** (2-4 sentences) that:
   - Names the event (diagnosis, condition)
   - States the emotional weight in one sentence
   - Includes an explicit cross-reference: *"The full story belongs to another chapter."*
   - Shows what was learned from it (the emotional takeaway, not the medical details)

**Template for a deduplicated reference:**

```
### A Sick Child

There is nothing that terrifies a parent more than a sick child. Bob learned this when [child] went for a routine checkup and the doctor pulled him aside with words no parent ever wants to hear: *[the diagnosis].*

The diagnosis was [condition]. At that time, nearly always [the prognosis].

The full story belongs to another chapter. What matters here is what it taught Bob: that the deadlines and promotions and arguments about whose turn it is to do the dishes — none of it matters. What matters is the small hand reaching for yours in the darkness. The recovery took years, but she survived. She grew up. Every birthday since has been a celebration, every hug precious, every "I love you" said with the full weight of meaning.
```

##### Step 4: Resolve Placeholder Titles

If a section heading contains "### Chapter xx:" or similar, the fix is:

1. **Identify the theme** of the section below the heading
2. **Replace the placeholder** with a proper section title that summarizes the section's content
3. **Examples:**
   - `### Chapter xx: Engineer vs. Executive` → `### The Engineer and the Executive`
   - `### Chapter xx:` → Extract themes from the section body and compose a title

Common placeholder-to-title conversions for memoirs:
| Placeholder | Theme | Proper Title |
|-------------|-------|-------------|
| "Chapter xx: Engineer vs. Executive" | Career evolution, dual identity | "The Engineer and the Executive" |
| "Chapter xx:" | General reflections | Extract from the section's opening line or thesis |

If the placeholder text also has a subtitle like `*The Evolution of a Career*`, keep the subtitle as italic text. The new heading should flow naturally with the chapter's existing subheading style.

##### Step 5: Expand Targeted Sections with Sensory Detail

For sections marked 🔨 EXPAND, use the expansion techniques from the "Editorial Proposal-Driven Chapter Expansion" sub-skill above. But adapt for the **compression context**:

- Add only **2-6 sentences** per expanded section — you're enriching, not bloating
- Choose **one dominant sense** per expansion (smell for the fire, sound for the silence, touch for the cold)
- Make every added sentence do double duty: sensory detail + character revelation
- If the section already has good content, add depth to the **pivotal moment** (the instant before, during, or after the key event)

**Example (adding sensory depth to a fire scene):**
> Before: "The fire exploded. Bob turned off the power. He ran."
> After: "The heat hit him before the sound did, a wall of warmth that turned to searing within seconds. The smell of burning jet fuel filled his lungs, acrid and chemical — the unmistakable scent of something becoming a catastrophe."

##### Step 6: Compress Non-Expanded Sections

For sections marked 📏 COMPRESS, apply these techniques:

- **Cut redundant explanations** — if you've said it once, don't say it again
- **Cut transitional throat-clearing** — "In the aftermath, there were lots of jokes about..." → "In the aftermath, jokes about..."
- **Merge short adjacent paragraphs** of the same topic
- **Remove secondary adjectives** — "the cold, damp, metallic smell" → "the metallic smell"
- **Replace multi-sentence descriptions** with single vivid images
- **Remove AI lecture-voice** — cut academic framing, named psychologists, clinical language
- **Every paragraph should advance story or character** — if a paragraph is pure commentary, fold it into a sentence in the adjacent scene

**Compression checklist for each section:**
- [ ] Can any paragraph become a sentence?
- [ ] Can any sentence lose an adjective without losing meaning?
- [ ] Is there a clinical/academic framing I can cut?
- [ ] Is this the first or only time this information appears in the book?

##### Step 7: Smooth Pacing with Connective Tissue

For sections marked 🌉 CONNECT, add transitional sentences at section boundaries:

- **Between disparate topics:** Use the 1980s paragraph or similar bridge section to acknowledge the passage of time and shift in focus
- **Between emotional tones:** Acknowledge the tonal shift (light → heavy, heavy → light) with a sentence that marks it
- **The connective formula:** `[One-sentence callback to previous section]` + `[One-sentence preview of next section]`

Avoid generic transitions ("Meanwhile," "Later," "After that"). Use specific imagery or thematic echoes.

##### Step 8: Write the Full Revision in One Pass

Write the complete revised chapter from scratch, applying all treatments simultaneously. This is more coherent than patching section by section because:

- You can naturally calibrate compression vs. expansion for the entire word budget
- The strengthened sections (expanded fire, deduplicated sick child) balance the tightened ones
- You can weave connective sentences that refer forward and backward within the chapter
- Voice and style stay consistent across the whole chapter

##### Step 9: Verify Word Count and All Changes

```bash
wc -w revised_chapter.md
```

Check against target range. If over: tighten a section that wasn't expanded. If under: add one more sensory detail or expand the connective tissue slightly.

**Post-revision checklist:**
- [ ] All proposals from the numbered list are addressed
- [ ] Duplicate story replaced with brief reference + cross-chapter note
- [ ] Placeholder heading ("Chapter xx") resolved to proper title
- [ ] Expanded sections have credible sensory detail (not just more words)
- [ ] Compressed sections lost words but kept meaning and storyline
- [ ] Pacing smoothed with connective transitions between sections
- [ ] Word count is within target range
- [ ] Voice consistent throughout (no drift between old and new material)
- [ ] All original facts preserved (dates, names, locations unchanged)
- [ ] No new facts introduced
- [ ] No AI lecture-voice introduced in expansions

### When to Use Compression vs. Expansion

| Use Compression when... | Use Expansion when... | Use Hybrid when... |
|------------------------|----------------------|-------------------|
| Chapter is too wordy / over target | Chapter is too thin / under target | Chapter is over target BUT some sections are thin |
| Removing AI lecture-voice | Adding scene work to summary sections | Editorial proposals mix compress, expand, and fix |
| Tightening transitions | Adding sensory detail | Placeholder titles or duplicates need resolution |
| Removing redundancy | Building up shown-not-told moments | The chapter structure is fine but content needs polishing |
| Streaming narrative flow | Deepening emotional resonance | Word count net needs compression despite localized expansions |

When the user provides a list of specific editorial improvement proposals and asks you to rewrite a chapter applying ALL of them while compressing to a target word count, use this workflow.

### When to Use This Sub-Skill

- User provides a numbered list of editorial improvement proposals (e.g., "remove AI lecture-voice", "tighten transitions", "reduce redundancy", "preserve all storylines", "write in first-person bestseller memoir style", "compress from X to Y words")
- The chapter suffers from AI-derived problems: academic citations, named psychologists, clinical/analytic framing, textbook language, "flashbulb memories" style exposition
- You are asked to compress while keeping ALL original storylines intact
- The target is a specific memoir/creative non-fiction chapter, not fiction

### Workflow Steps

#### Step 1: Read and Categorize the Improvement Proposals
Parse the user's list and group each proposal into one of four action categories:

| Proposal Type | Example | Action |
|--------------|---------|--------|
| **Tone remediation** | "Remove AI lecture-voice" | Strip academic citations, named psychologists, textbook language, clinical framing. Replace with sensory detail and personal reflection. |
| **Structural** | "Tighten transitions", "Remove bold headers" | Replace section subheadings (`### The Builder's Blood`) with flowing `---` horizontal rules. Write connective sentences that bridge sections naturally. |
| **Content** | "Reduce redundancy", "Remove overlap with Ch1" | Cut repeated themes. Check for stories told in other chapters. Trim without losing narrative threads. |
| **Style** | "Write in first-person engaging memoir style" | Convert third-person to first-person. Use active voice. Add sensory detail. Show don't tell. Target emotional resonance. |

#### Step 2: Baseline Read + Word Count
- Read the original chapter in full
- Note current word count via `wc -w`
- Calculate compression ratio: `target / original`
- Identify which sections are the wordiest — these are your primary compression targets

#### Step 3: Identify AI Lecture-Voice Markers
Before rewriting, scan for these specific patterns and mark them for removal:

- **Named psychologists/psychology**: "Psychologists have a term for such moments...", "Psychologists who study military service often note...", "psychological researchers would later classify it...", "Neuroscientific research now confirms..."
- **Clinical framing**: "flashbulb memories", "neural snapshot burned into the hippocampus", "reward circuits can be hijacked", "hardwired into neural pathways before the prefrontal cortex has fully developed"
- **Academic explanatory asides**: "This is how memory works...", "This, too, was memory at work...", "They were identity scripts, passed down to give shape to lives..."
- **Third-person distance**: "Bob can trace a direct line", "Bob's generation, Sputnik became exactly that", "Bob's family roots ran deep"
- **Textbook transition**: "To understand X, you must first understand Y..."

**Replacement strategy for each:**
- Replace clinical framing with the raw sensory experience (the beep, the photograph's faded edges, the feel of the saw, the clink of the fork)
- Replace named psychologists with the character's own realization or feeling
- Replace "This is how memory works" with "That is how memory shapes us" - a reflective, first-person insight, not a lecture
- Convert third-person narration to first-person throughout (Bob → I, his → my, Bob's → my)

#### Step 4: Convert Section Headings to Flowing Transitions
Replace bold subheadings (`### The Builder's Blood`) with a simpler visual separator (`---`) and write a one-sentence bridge at the start of each new section that connects to the previous one.

**Before (with heading):**
```
### The Builder's Blood
If Sputnik represented humanity reaching upward, Bob's family roots ran deep in the opposite direction...
```

**After (with flow):**
```
---
If Sputnik represented humanity reaching upward, my family roots ran deep in the opposite direction...
```

**Pro tip:** The first sentence of each section should both signal the new topic AND echo something from the previous section (e.g., "the infinite black canvas above" → "roots ran deep in the opposite direction" — contrast creates flow without an explicit transition phrase).

#### Step 5: Preserve ALL Storylines While Compressing
Before writing, checklist every storyline in the chapter. For each, capture:
- **The minimum viable version** — what is the one sensory detail or moment that carries this thread?
- **What can be cut** — academic asides, repeated explanations, meta-commentary about memory

During compression:
- Keep the visceral, sensory moments (the beep, the photograph, the old man's rasping voice, the garage smell, the fork clinking)
- Cut the analysis-of-the-moment ("Psychologists call this...")
- If a story appears in another chapter (e.g., the garage/boat building covered in Chapter 3), reference it lightly here and save the detail for that chapter
- Each storyline needs just ONE vivid anchor detail to stay alive

#### Step 6: First-Person Voice Conversion
Convert the entire chapter to first-person memoir voice:
- **Pronouns**: Bob/he/him → I/me/my. Bob's → my. His → my.
- **Verbs**: "Bob remembers" → "I remember" or just show the memory
- **Observations**: "Bob would later understand" → "I understand now" or cut entirely
- **Retrospective insight**: Keep the wisdom, lose the lecture. "This is how memory works" → "That is how memory shapes us"
- **Dialogue and quotes**: Keep in original voice — don't convert quoted speech

The difference:
- ✗ *AI lecture:* "Psychologists have a term for such moments: 'flashbulb memories,' vivid recollections encoded during times of intense emotion..."
- ✓ *Memoir voice:* "That sound — mechanical, relentless, somehow both cold and alive — lodged in my bones and stayed there for seven decades and counting."

#### Step 7: Hit the Word Count Target
Write the full rewrite in one pass, then check with `wc -w`:
- If **under target**: Layer in more sensory detail — what did things smell like, look like, feel like? Add one more specific memory or moment to a thin section.
- If **over target**: Look for redundant phrases, repeated explanations, or paragraphs that could become sentences without losing meaning. Cut secondary adjectives.

Target within ~50 words of the requested range. When in doubt, favor landing slightly under rather than over — a tight chapter reads better than a bloated one.

#### Step 8: End-of-Rewrite Verification
Run this checklist before delivering:
- [ ] All AI lecture-voice markers removed (no named psychologists, no textbook language, no clinical framing)
- [ ] First-person memoir voice throughout (no third-person drift)
- [ ] All original storylines present (none dropped during compression)
- [ ] Section headings converted to flowing transitions (`---` + bridge sentences)
- [ ] Word count is within target range
- [ ] Emotional depth preserved — the chapter still carries the same emotional weight despite being shorter
- [ ] No new AI-voice accidentally introduced in the rewrite

### Compression Patterns Reference

| Original (Too Long) | Compressed (Tight) |
|--------------------|--------------------|
| "Psychologists have a term for such moments: 'flashbulb memories,' vivid recollections encoded during times of intense emotion or historical significance." | *(Cut entirely — the beep itself carries the weight)* |
| "This is how memory works, he would later understand: not a faithful recording but a palimpsest, written and rewritten..." | "That is how memory shapes us. Not as a passive record but as an active participant in the ongoing construction of who we are." |
| "Years later, genealogical research would find no documentary evidence of Templar connections. The stories, it seemed, were exactly that—stories, embroidered... They were identity scripts, passed down to give shape to lives that might otherwise feel random and unmoored." | "Years later, genealogical research found no documentary evidence. They were stories. But sitting at that old man's bedside, watching his thin fingers gesture through the air, I didn't need proof." |
| "To understand Bob's father, you must first understand the crucible that forged him." | "To understand my father, you have to understand the crucible that forged him." *(Keep the sentence but make it first-person — the direct address to the reader is a memoir convention)* |

### Common Pitfalls

| Pitfall | Solution |
|---------|----------|
| Losing a storyline during aggressive compression | Before delivering, cross-check: did every thread from the original appear in the rewrite? |
| First-person drifting back to third-person mid-chapter | Do a final grep for "Bob" or "his" (when referring to the narrator) |
| Over-compressing emotional moments | Keep the visceral details that carry the emotion — cut the explanation, not the image |
| Making sections too abrupt without transitions | Each `---` needs at least a one-sentence bridge that connects back to the previous section |

## Part Divider Enrichment (Add Image + Context Pages Between Sections)

When a book manuscript needs **structural part divider pages** between major sections — each containing a generated illustration and a historical/contextual passage (~1 page of text) — use this workflow.

### When to Use
- A completed manuscript has major parts (Part One, Part Two, etc.) but lacks visual divider pages between them
- Each part needs a **B&W pencil sketch image** relevant to its content
- Each part needs a **historical context passage** (~1 page) explaining the broader world events of that era
- For future/speculative parts, context passages should imagine plausible future events
- The output formats (HTML + PDF) need to be regenerated with all enrichment in place

### When NOT to Use
- If you're only editing existing text content (use the compression/expansion sub-skills instead)
- If you're only adding a cover image (use publishing-workflow instead)
- If you're only converting formats (use manuscript-conversion-pipeline instead)

### Step 1: Identify Part Boundaries
Scan the manuscript for part titles (e.g., "Part One: The Ignition", "Part Two: The Building"). Count the parts and list:
- Part number and title
- Chapters within each part
- Era/time period covered by each part
- Key events/subject matter for each part (for image prompts and context writing)

### Step 2: Generate B&W Pencil Sketch Images
Use Gemini Flash Image (`google/gemini-2.5-flash-image`) via OpenRouter API to generate 5 B&W pencil sketch images.

**Prompt structure** — include these elements:
```python
prompt = f"Black and white pencil sketch, highly detailed, of {SCENE_DESCRIPTION}. Hand-drawn graphite style, photorealistic pencil technique, no text, no labels, atmospheric lighting."
```

**Key constraints for every prompt:**
- "Black and white pencil sketch" — forces monochrome
- "no text, no labels" — prevents AI from embedding text
- Atmospheric detail specific to the scene

**Post-generation processing:**
- Convert to grayscale: `Image.open(f).convert('L').save(f)`
- Gemini returns 1024×1024 squares — this is fine for interior illustrations at ~3.4" at 300 DPI
- For true B&W look, convert PNG from RGB to L mode

**Example prompts by part type:**
| Part Era | Scene Suggestion |
|----------|-----------------|
| Childhood/1950s | Cabin interior, boy reaching for outlet, Michigan lake |
| Adolescence/1960s | Garage workshop, boat under construction, tools |
| Early Career | Control room, oscilloscopes, lab equipment, schematics |
| Mid-Life/Loss | Hospital or quiet interior, caregiving scene |
| Future/Speculative | Workshop with advanced tools, space colony window |

### Step 3: Write Historical Context Passages (~1 page each)
Each passage should be approximately 2500-3500 characters of text, formatted as an HTML `<div class="context-box">` with:

1. **Title**: "The World That Raised Him: 1952–1964" style
2. **Intro paragraph** (italic, lead-in): Sets the stakes
3. **Body paragraphs** (5-7 paragraphs of ~10pt text):
   - For **historical parts**: weave together world events, technological changes, cultural context
   - For **future parts**: imagine plausible scenarios based on current trajectories (AI, climate, space, medicine, warfare)
   - Connect the broader context to the personal story in the adjoining chapters
4. **CSS border styling**:
   ```css
   .context-box {
       border: 2px solid #8B7355;
       padding: 0.3in 0.25in;
       margin: 0.25in 0;
       text-align: left;
       page-break-inside: avoid;
       background-color: #faf8f5;
   }
   .context-title {
       font-size: 14pt; font-weight: bold; text-align: center;
       color: #5C4033; border-bottom: 1px solid #ccc; padding-bottom: 0.1in;
   }
   .context-intro {
       font-style: italic; font-size: 10pt; color: #555; text-indent: 0;
   }
   .context-box p {
       font-size: 10pt; line-height: 1.5; text-indent: 0;
   }
   ```

### Step 4: Rebuild the HTML from Scratch (Do NOT Patch)
The enrichment changes are too structural for find-and-replace. Instead, rebuild the HTML entirely:

**Approach:** Parse the markdown source, classify each line as (part_title, chapter_title, or content), and build a new document:

```python
# Pseudo-code structure
html_parts = [
    '<!DOCTYPE html>...<head><style>...</style></head><body>',
    '<div class="title-page">...',                    # Title + author
    build_toc(),                                       # Single clean TOC
    build_part_divider(part1, img1, context_html1),   # Part 1 divider
    '<h2 class="chapter-title">Chapter One: ...</h2>',  # Chapters 1-3
    ...,
    build_part_divider(part2, img2, context_html2),   # Part 2 divider
    '<h2 class="chapter-title">Chapter 4: ...</h2>',  # Chapters 4-5
    ...,
    '</body></html>'
]
```

Key details:
- Part titles: `<h1 class="part-title">` with page-break-before
- Chapter titles: `<h2 class="chapter-title">` with page-break-before
- Embed images as base64 data URIs for self-contained HTML
- Context boxes appear inside the part divider `<div>`
- TOC must be generated once, not embedded from the markdown source

### Step 5: Critical Verification Checks
After rebuilding, verify these counts match expectations:
```python
toc_count = html.count('<div class="toc">')           # Must be 1
part_count = html.count('class="part-title"')         # Must match number of parts
ch_count = len(re.findall(r'<h2 class="chapter-title">', html))  # Must match chapter count
img_count = html.count('<img src="data:')             # Must match part count
```

Also verify no stray duplicate content:
- No "Table of Contents" as a `<p>` text (should only be in the TOC div)
- No duplicate part or chapter titles in the body
- PDF page count should be roughly: original_pages + (part_count × ~2.5) for dividers

### Step 6: Regenerate PDF
Use WeasyPrint for 6"×9" book format:
```bash
weasyprint input.html output.pdf
```

Verify:
- `pdfinfo output.pdf | grep Pages` — reasonable page count
- `pdftotext output.pdf - | grep -c '#'` — should be 0 (no markdown artifacts)
- Spot-check a context box page and a chapter page

### Common Pitfalls
| Pitfall | Solution |
|---------|----------|
| Chapter headings not recognized | Check exact markdown format: "Chapter One" vs "Chapter 1" — manuscripts often mix word and numeric formats. Use a list of exact strings for detection. |
| Double TOC in output | The markdown source often has its own TOC. Remove it programmatically by finding the second occurrence of "Tomorrow Is Still Open" (or equivalent title). |
| Image file sizes | Raw Gemini images are ~2.3MB each in RGB. Converting to grayscale (L mode) reduces them to ~750KB each. |
| Base64 bloat in HTML | 5 images × 750KB each = ~3.75MB of base64 data in the HTML. This is fine for WeasyPrint but may slow editing. |
| Context passages too short | Target 2500-3500 chars per passage. The intro paragraph sets the frame, body paragraphs deliver content, and a closing paragraph connects back to the personal narrative. |

---

## Quality Audit Workflow (Propose Improvements Without Changes)

When the user asks you to review chapters and propose improvements (but NOT make changes), use this workflow:

### 1. Read Every Chapter Sequentially
Read the full manuscript or designated chapters. For each, assess:
- **Pacing** — does the chapter move at the right speed? Are there slow patches?
- **Redundancy** — does it repeat themes or stories from other chapters?
- **Engagingness** — does it pull the reader in, or is it flat/expository?
- **Clarity** — is the narrative thread clear? Are transitions smooth between sections within the chapter?
- **Voice consistency** — any first-person/third-person switching? Any AI lecture-tone (e.g., naming psychological studies)?
- **Emotional depth** — does it show rather than tell? Are there specific sensory details?
- **True story integrity** — for memoirs, are the facts preserved even if the telling changes?
- **AI-voice indicators** — academic citations, named psychologists, textbook language ("Psychologists have a term for such moments...")

### 2. Group Findings by Chapter
For each chapter, list:
1. **The specific issue** (with a quoted example from the text)
2. **Why it matters** (how it affects reader experience)
3. **A proposed fix** (what you'd do, without actually doing it)

### 3. Flag Cross-Chapter Issues
Note when the same story appears in multiple chapters (e.g., a daughter's medical crisis told in Chapter 7 AND Chapter 11 with nearly identical language — this is a critical find).

### 4. Prioritize
Mark issues as:
- **Critical** (duplicate stories, broken structure, AI voice dominating)
- **Important** (pacing problems, underdeveloped characters, weak transitions)
- **Optional** (minor tightening, single typos, subjective tone preferences)

### 5. Present as a Structured List
Format your findings so each chapter has its own clearly delineated section. The user can then choose which to action.

## Parallel Rewrite via Delegate Task

When a manuscript overhaul requires BOTH:
(a) automated cleanup (garbage removal, renumbering, restructuring)
(b) creative rewrites (chapter 1 compression, last chapter split, bestseller-style prose)

Use `delegate_task` to parallelize:
```python
# Task A does the automated cleanup and extraction
# Task B rewrites Chapter 1
# Task C rewrites the last section
# Then you assemble all pieces in final order
```

This is effective because:
- The automated cleanup is fast and deterministic (regex in Python)
- The creative rewrites are expensive (require thinking/API calls)
- They don't depend on each other — cleanup removes garbage, rewrites produce fresh content
- After both complete, a final assembly script merges everything

**Important:** Provide both task agents with the full relevant context — they have no memory of your conversation. Include file paths, exact content to rewrite, character counts/targets, and style guidelines.

## Post-Parallel-Rewrite Assembly

After spawning multiple subagents to rewrite different chapters, assemble the final manuscript systematically to avoid corruption from overlapping edits.

### The Problem

Subagents may write to different files (clean, preferred) OR patch the same source file directly. When multiple agents patch the same file, chapter boundaries can get corrupted — a rewrite of Chapter 2 may accidentally consume Chapter 3 if the end-boundary regex matches inside the rewritten content. The result: missing chapters, duplicated content, broken structure.

### The Two-Phase Assembly Workflow

#### Phase 1: Detect Where Subagents Wrote

```python
# Check for both patterns
import glob
separate_files = glob.glob("output/Chapter*_Rewrite.md")  # Wrote to separate files
patched_file = "output/Manuscript_REVISED.md"              # PATCHED the same file

# Read each separate file
rewrites = {}
for f in separate_files:
    num = re.search(r'Chapter(\d+)', f).group(1)
    with open(f) as fh: rewrites[num] = fh.read()

# Read the patched file to see what survives
with open(patched_file) as f: patched = f.read()
```

#### Phase 2: Extract Intact Sections from Patched/Corrupted Files

When a subagent patched the main file but later operations corrupted it, extract intact sections by chapter header:

```python
def extract_intact(content, ch_header, fallback_content=""):
    """Extract a chapter intact, with fallback if corrupted."""
    start = content.find(ch_header)
    if start < 0:
        return fallback_content  # Use separate rewrite file as fallback
    # Find the next chapter header to mark the end
    rest = content[start + len(ch_header):]
    end = len(content)
    for pat in [r'^## Chapter \d+', r'^# Part ', r'^# Final Section']:
        m = re.search(pat, rest, re.MULTILINE)
        if m:
            candidate = start + len(ch_header) + m.start()
            if candidate < end: end = candidate
    # Verify the extracted section has reasonable content
    section = content[start:end]
    if len(section.split()) < 20:  # Too short — corrupted
        return fallback_content
    return section
```

#### Phase 3: Clean & Verify Each Rewrite File

Strip Part headers from rewrite files — they may contain `# Part Two: The Building` headers that will collide with the assembly:

```python
def clean_chapter(text):
    """Remove # Part headers from chapter content."""
    return re.sub(r'^# Part[^\n]*\n\n?', '', text.strip())
```

#### Phase 4: Build from Scratch (Not by Patching)

Always rebuild the final manuscript from scratch by concatenating all sections in order, NEVER by doing find-and-replace patches on a large file:

```python
parts = [
    "Title\n\nSubtitle",
    "# Part One: The Ignition",
    clean_chapter(ch1_rewrite),
    clean_chapter(ch2_rewrite),
    echoes_section,
    ch3_content,
    "# Part Two: The Building",
    clean_chapter(ch4_rewrite),
    ...
]

final = '\n\n'.join(p for p in parts if p and p.strip())
final = re.sub(r'\n{4,}', '\n\n\n', final)
```

#### Phase 5: Deduplicate Part Headers

After assembly, check for duplicate `# Part` headers — they appear when rewrite files contained embedded Part headers:

```python
lines = final.split('\n')
seen_parts = set()
clean_lines = []
for line in lines:
    s = line.strip()
    if re.match(r'^# Part (One|Two|Three|Four|Five)', s):
        if s in seen_parts: continue  # Skip duplicate
        seen_parts.add(s)
    clean_lines.append(line)
final = '\n'.join(clean_lines)
```

#### Phase 6: Verification Checklist

Run AFTER assembly, BEFORE TOC rebuild:

```
[ ] Total word count is reasonable (not wildly different from sum of parts)
[ ] All chapter headers present and sequential
[ ] No duplicate Part headers
[ ] No duplicate chapter content
[ ] No AI artifacts re-introduced ("Between the memory of", "liminal space", etc.)
[ ] Echoes/Transition bridge sections present
[ ] Each chapter has reasonable word count (not 0, not absurdly large)
```

#### Phase 7: Rebuild TOC

After all content is finalized, regenerate the Table of Contents with updated page number estimates (~250 words per page, +4 for front matter):

```python
# Find all ## Chapter headers, estimate cumulative page for each
for i, line in enumerate(lines):
    if re.match(r'^## Chapter (One|Two|\d+)', line.strip()):
        # Count words until next chapter
        wc = sum(len(l.split()) for j in range(i+1, end_line) for l in [lines[j]])
        word_count += wc
        page = 4 + word_count // 250
        toc_entry = f"- **{title}** ..... {page}"
```

## Book-Length Novel Condensation (150-190 pages, 6x9" format)

When condensing a full novel-length manuscript to a publishable 150-190 page book (6x9" trim):

### Target Math
- **Page count**: 150-190 pages
- **Words per page**: ~250-270 (6x9" with proper margins, Georgia 11-12pt)
- **Total target**: ~38,000-51,000 words (aim for ~40,000)
- **Chapter target**: ~1,200-1,700 words per chapter (for 25-30 chapters)
- **Compression ratio**: ~40-50% of original (cut 50-60%)

### Condensation Strategy
1. **Read chapter outline FIRST** — know every plot beat before reading the full chapter
2. **Keep ALL plot beats** — every event that advances the story must survive
3. **Preserve voice** — the narrator's personality, humor, and style are non-negotiable
4. **Keep all dialogue** that reveals character or advances plot
5. **Cut redundant internal monologue** — if the narrator thinks the same thing twice, keep the funnier/more vivid version
6. **Cut atmospheric description by ~50%** — keep the best sensory details, cut the rest
7. **Cut transitional filler** — bridge sentences between scenes can be compressed or removed
8. **Preserve humor beats** — jokes, running gags, and character quirks must survive
9. **Preserve formatting** — indented paragraphs with &nbsp;&nbsp;&nbsp;&nbsp;, scene breaks with ---

### Workflow
1. Restore original chapters from the compiled manuscript (individual chapter files get overwritten during condensation)
2. Extract chapters from manuscript: read the markdown source, find `## Chapter N` headers, extract content between consecutive headers
3. For each chapter: read the full original, read the outline beats, write condensed version targeting ~1,300-1,500 words
4. **Verify after each batch**: spot-check that plot beats survived and voice is intact

### Subagent Delegation Pattern
- Use `delegate_task` for parallel chapter processing
- Provide each subagent with: file paths, condensation rules, target word count, style guidelines
- **3-5 chapters per agent is optimal** — larger batches risk timeout
- After subagents complete, verify all files were written and word counts are in the 1,200-1,700 range

### Common Pitfall: Over-Condensing Then Under-Condensing
- First pass often leaves chapters too long (70-80% of original)
- Second pass may over-condense chapters to 20-30% of original  
- **Solution**: Aim for 40-50% compression on each pass. Check word counts after every 5 chapters.
- Target ~1,300 words per chapter as a sanity check; flag anything under 800 or over 2,000

### Common Pitfall: Losing the Narrative Voice
- Mechanical sentence-level compression destroys narrative voice and rhythm
- **Solution**: After writing condensed chapters, read them aloud. If they don't sound like the original narrator, re-read the original chapter and recapture the rhythm and personality before rewriting

### Common Pitfall: Losing Humor During Condensation
- Humor is often embedded in the "atmospheric" description or "redundant" internal monologue that gets cut first
- **Solution**: Before condensing, identify every humor beat in the chapter (running gags, character quirks, funny observations). Mark them as "KEEP" and ensure every one survives the condensation

## Success Criteria

- **Humanization mandate**: ALL book prose — transitions, expanded scenes, bridge passages, new sections, connective tissue — MUST pass the `humanizer` skill's 29 pattern checks. No AI-isms, no filler, real voice, variable rhythm. This is mandatory for every piece of book text.
- **Reader engagement mandate**: Every piece of added material — transitions, expanded scenes, bridge passages, new sections, connective tissue — MUST be interesting, exciting, and engaging to readers. This is a non-negotiable quality bar.
- Added material must open with a hook, include sensory detail, and end with narrative momentum.
- No filler transitions: every bridge section must reveal something, deepen understanding, or build anticipation.
- Voice consistency: all added material matches the surrounding narrative voice perfectly.
- All target patterns have been replaced
- Sections moved to correct positions
- Document structure remains intact
- Content flows logically and naturally
- Original information preserved while improving style
- All remaining AI artifacts verified absent with checklist
- Chapter numbers sequential with no gaps
- No duplicate storylines across different chapters
- Assembly completed without corruption from overlapping subagent edits

## Common Pitfalls & Solutions

| Pitfall | Solution |
|---------|----------|
| Regex too broad/narrow | Test on sample content first |
| Breaking document structure | Preserve headings and section markers |
| Losing content during moves | Extract full section before deleting |
| Inconsistent voice | Use hash-based variation selection |
| Overwriting needed content | Create backup before modifications |
| Character encoding mismatch in str.replace() | Use regex with flexible character classes instead of exact string match |
| read_file line-number prefix | `read_file` returns lines prefixed like "    42|content" — strip this prefix before processing, or use raw file open/write for editing |
| Quoted dialogue corruption | Track `"` state character-by-character to avoid replacing first-person pronouns inside dialogue |

## Example Use Cases

1. **Manuscript Editing**: Transform generic transitions into personal reflections
2. **Document Restructuring**: Move chapters to improve chronological flow
3. **Content Modernization**: Update outdated language while preserving meaning
4. **Style Transformation**: Change from academic to conversational tone
5. **Section Reordering**: Improve narrative arc by rearranging content

## Verification Steps

After applying changes:
```python
# Check original patterns are gone
assert not re.search(original_pattern, new_content)

# Verify moved sections are in correct position
assert new_content.find(target_section) > new_content.find(reference_point)

# Count replacements
assert new_content.count(new_pattern) == expected_count
```

## Performance Considerations

- For large documents, process in chunks
- Use efficient regex patterns
- Consider memory usage when reading entire file
- Profile performance on representative samples