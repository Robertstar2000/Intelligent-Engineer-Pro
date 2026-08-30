---
name: book-identity-rebranding
description: Systematically change a book's title, subtitle, author name, and/or series name across all files in the publishing pipeline — manuscripts, build scripts, cover scripts, HTML output, EPUB metadata, marketing docs, KDP disclosures, and package files.
tags: [publishing, rebranding, rename, title-change, series, metadata]
---

## Memory context (Hindsight)

Long-term memory context is now provided automatically by Hindsight (bank
`mifeco-default`) on every turn — the retired MemPalace manual query step no
longer applies. Do NOT attempt to import `~/.hermes/mempalace` (it was removed
2026-08-19).This retrieves previous decisions, domain-specific context, and lessons learned from the vector memory store.

# Book Identity Rebranding

## When to Use
- The user says "change the title to...", "rename this book", "rebrand the series", "update the author name"
- You need to propagate a book's title, subtitle, author, or series name change across every file in its pipeline
- Cover artwork exists as a raw image that just needs new text overlay (no need to regenerate the art)

## Systematic File Pipeline

When rebranding, hit every layer in order:

### 1. Manuscript Source Files
Search in the book's directory for all `.md` files containing the old title/author/subtitle/series name:
```bash
grep -rn 'Old Title\|Old Author' /path/to/book/dir/
```

Update the title header (usually `# Old Title` on line 1), subtitle (`*Old Subtitle*`), author line, copyright line, and any closing "thank you for reading" references.

### 2. Build Scripts (Python/.py)
Search for hardcoded title/author strings in build scripts:
```bash
grep -n 'TITLE = \|AUTHOR = \|Old Title\|Old Author\|old_filename' *.py
```

Key variables to find:
- `TITLE` / `AUTHOR` constants
- `subtitle` / `series` strings passed to build functions
- `next_book_title` (series cross-references in back-cover "coming next" sections)
- Filenames like `Old_Title.epub`, `Old_Title.pdf`
- `dc:title` / `dc:creator` in EPUB content.opf generation code
- Any `filename.replace("Old", "New")` patterns

### 3. Cover Regeneration Scripts
Update the `add_cover_typography.py` or equivalent PIL-based overlay script:
- `title_words` list (stacked words on cover)
- `author_text` string
- `output_path` filename
- Subtitle text (multi-line if needed)
- Volume/series designation text

**Then regenerate:** `python3 add_cover_typography.py`

### 4. Cover Generation Prompts (Optional)
If the user wants entirely new cover art (not just re-texturing), update the `generate_cover.py` prompt with the new title in the prompt description.

**Aspect Ratio Guidance:** When generating new raw cover art, the source image is typically square (1024×1024) and the cover script extends it to 2:3 portrait (1024×1536). If the user requests "full width" or "full portrait" covers, specify `2:3 portrait aspect ratio` in the prompt. Some models may still return square — design your pipeline to handle both.

**Fallback Strategy:** If the primary image model fails, retry with a different model (e.g., `black-forest-labs/flux.2-max`).

### 5. Final Print HTML (main output)
For large (>10MB) HTML files with the old title embedded, use Python for bulk replacement:
```python
with open('output.html', 'r') as f:
    content = f.read()
content = content.replace('Old Title', 'New Title')
content = content.replace('Old Author', 'New Author')
content = content.replace('old_filename', 'new_filename')
with open('output.html', 'w') as f:
    f.write(content)
```

Search for: `<title>` tag, cover `<h1>`, copyright `<p>`, back-cover blurbs, author bio section, back-of-book chapter listings.

### 6. Rebuild EPUB
If the EPUB build script has hardcoded metadata (`dc:title`, `dc:creator`), update those, then rebuild:
```bash
python3 build_epub.py
```

### 7. Marketing & Compliance Docs
Update ALL of these files:
- `MARKETING_COPY.md`
- `KDP_AI_DISCLOSURE.md`
- `PUBLISHING_SCORECARD.md`
- Any `README.md` in package directories

Use the same bulk-replace pattern as step 5.

### 8. FINAL_PACKAGE Contents
Walk the final package directory and replace old references in:
- `Marketing_and_Compliance/Marketing_Copy.md`
- `Marketing_and_Compliance/KDP_AI_Disclosure.md`
- `Manuscript/` contents (`.md`, `.html`)

## Batch Cover Regeneration for Series (PIL)

When rebranding an entire series (3–5+ volumes), create a **single standalone cover script** that drives all volumes from a BOOKS dictionary. This is more scalable than editing each volume's cover script individually:

```python
#!/usr/bin/env python3
"""Apply series cover typography to all volumes at once."""
from PIL import Image, ImageDraw, ImageFont
import os

target_w, target_h = 1024, 1536
font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

BOOKS = {
    "book_key_1": {
        "subtitle": "Built from Dust",       # Volume subtitle
        "volume": "BOOK I",                  # Volume designation
        "raw": "/path/to/raw_cover.png",     # Raw art without text
        "output": "/path/to/output_cover.png",
        "top_ext": 0.65,                     # Top extension ratio for canvas fitting
    },
    # ... more volumes
}

author_text = "Bob Mills"

for name, spec in BOOKS.items():
    img = Image.open(spec["raw"])
    # Scale to fill height, extend canvas to 2:3 ratio
    ratio = target_w / img.width
    img_resized = img.resize((target_w, int(img.height * ratio)), Image.LANCZOS)
    extra_h = target_h - img_resized.height
    top_ext = int(extra_h * spec["top_ext"])
    canvas = Image.new("RGB", (target_w, target_h), (0, 0, 0))
    canvas.paste(img_resized, (0, top_ext))
    canvas = canvas.convert("RGBA")
    overlay = Image.new("RGBA", (target_w, target_h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    # Top gradient for text readability
    for y in range(int(target_h * 0.22)):
        alpha = int(70 * (1 - y / (target_h * 0.22)))
        draw.rectangle([0, y, target_w, y+1], fill=(0, 0, 0, min(alpha, 55)))
    
    # Series title (stacked, e.g. ["NO", "BLUE", "SKY"])
    f_title = ImageFont.truetype(font_path, 56)
    line_h = int(56 * 1.15)
    curr_y = int(target_h * 0.04)
    for word in ["SERIES", "TITLE", "WORDS"]:
        bbox = draw.textbbox((0, 0), word, font=f_title)
        tw = bbox[2] - bbox[0]
        draw.text(((target_w - tw) / 2 + 1, curr_y + 1), word, font=f_title, fill=(0,0,0,180))
        draw.text(((target_w - tw) / 2, curr_y), word, font=f_title, fill="white")
        curr_y += line_h
    
    # Volume designation (e.g. "BOOK I")
    f_vol = ImageFont.truetype(font_path, 22)
    bbox = draw.textbbox((0, 0), spec["volume"], font=f_vol)
    vw = bbox[2] - bbox[0]
    vol_y = curr_y + 8
    draw.text(((target_w - vw) / 2 + 1, vol_y + 1), spec["volume"], font=f_vol, fill=(0,0,0,180))
    draw.text(((target_w - vw) / 2, vol_y), spec["volume"], font=f_vol, fill=(200,200,200,255))
    curr_y = vol_y + 28
    
    # Volume subtitle
    f_sub = ImageFont.truetype(font_path, 30)
    bbox = draw.textbbox((0, 0), spec["subtitle"], font=f_sub)
    sw = bbox[2] - bbox[0]
    sub_y = curr_y + 6
    draw.text(((target_w - sw) / 2 + 1, sub_y + 1), spec["subtitle"], font=f_sub, fill=(0,0,0,180))
    draw.text(((target_w - sw) / 2, sub_y), spec["subtitle"], font=f_sub, fill="white")
    
    # Author at bottom
    f_auth = ImageFont.truetype(font_path, 26)
    bbox = draw.textbbox((0, 0), author_text, font=f_auth)
    aw = bbox[2] - bbox[0]
    draw.text(((target_w - aw) / 2 + 1, target_h - 80 + 1), author_text, font=f_auth, fill=(0,0,0,180))
    draw.text(((target_w - aw) / 2, target_h - 80), author_text, font=f_auth, fill="white")
    
    final = Image.alpha_composite(canvas, overlay).convert("RGB")
    final.save(spec["output"], "PNG", optimize=True)
```

This approach avoids touching each volume's individual cover script and lets you run all covers with one command.

## Cover Regeneration Pattern (Single Book)

When the raw artwork already exists and only the text needs updating:

```python
from PIL import Image, ImageDraw, ImageFont

# Find font
font_path = None
for fp in ['/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
           '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf']:
    if os.path.exists(fp): font_path = fp; break

img = Image.open("raw_cover.png").convert("RGB")
target_w, target_h = 1024, 1536  # 2:3 book cover ratio

# Scale to fill height, center-crop width
scale = target_h / img.height
new_w = int(img.width * scale)
img = img.resize((new_w, target_h), Image.LANCZOS)
x_offset = (new_w - target_w) // 2
canvas = img.crop((x_offset, 0, x_offset + target_w, target_h))

# Dark gradients for text readability
overlay = Image.new("RGBA", (target_w, target_h), (0,0,0,0))
draw = ImageDraw.Draw(overlay)
for y in range(int(target_h * 0.18)):
    alpha = int(50 * (1 - y / (target_h * 0.18)))
    draw.rectangle([0, y, target_w, y+1], fill=(0,0,0,alpha))

# Title (stacked, centered)
title_font = ImageFont.truetype(font_path, 62)
title_words = ["NEW", "TITLE", "WORDS"]  # adjust for each book
line_h = int(62 * 1.15)
for i, word in enumerate(title_words):
    bbox = draw.textbbox((0,0), word, font=title_font)
    tx = (target_w - (bbox[2]-bbox[0])) // 2
    ty = 50 + i * line_h
    draw.text((tx+2, ty+2), word, fill=(0,0,0,180), font=title_font)
    draw.text((tx, ty), word, fill=(255,255,255), font=title_font)

# Volume/series designation (between title and subtitle, if applicable)
if volume_text:
    vol_font = ImageFont.truetype(font_path, 28)
    bbox = draw.textbbox((0,0), volume_text, font=vol_font)
    vx = (target_w - (bbox[2]-bbox[0])) // 2
    vy = title_end_y + 8
    draw.text((vx+2, vy+2), volume_text, fill=(0,0,0,180), font=vol_font)
    draw.text((vx, vy), volume_text, fill=(220,220,220), font=vol_font)

# Subtitle (multi-line)
sub_font = ImageFont.truetype(font_path, 18)
for i, line in enumerate(sub_lines):
    bbox = draw.textbbox((0,0), line, font=sub_font)
    sx = (target_w - (bbox[2]-bbox[0])) // 2
    sy = sub_start_y + i * 22
    draw.text((sx+1, sy+1), line, fill=(0,0,0,180), font=sub_font)
    draw.text((sx, sy), line, fill=(200,200,200), font=sub_font)

# Author at bottom
author_font = ImageFont.truetype(font_path, 28)
bbox = draw.textbbox((0,0), author_text, font=author_font)
ax = (target_w - (bbox[2]-bbox[0])) // 2
draw.text((ax+2, target_h-100+2), author_text, fill=(0,0,0,200), font=author_font)
draw.text((ax, target_h-100), author_text, fill=(255,255,255), font=author_font)

final = Image.alpha_composite(canvas.convert("RGBA"), overlay).convert("RGB")
final.save("output_cover.png", "PNG", optimize=True)
```

## Series Rebranding (Multi-Volume)

When renaming an entire series (e.g., "Lunar Settlement Chronicle" → "No Air, No Mercy"):

1. Update each volume's manuscript title header
2. Update each volume's cover typography script with new series title words
3. Update each volume's build script (series string, next_book_title reference)
4. Regenerate covers for ALL volumes
5. Rebuild ALL volumes
6. Verify cross-references (back-cover "Coming Soon" sections pointing to other volumes)

## Series Interleaving (Books Moving Between Series)

When books from one series are re-slotted as volumes in a different series (e.g., taking 2 books from "Series A" and making them Vol IV & V of "Series B"):

1. **Update each volume's manuscript title** — The title header changes entirely: `# Series A: Volume II` → `# Series B: Volume IV`
2. **Update subtitle line** — `*Series A — Book 2 of 2*` → `*Series B — Book 4 of 5*`
3. **Update build scripts** — Every script that hardcodes the old series name, volume numbers, and cross-references (e.g., `next_book_title`) must be updated
4. **Generate covers from a batch script** — Use the Batch Cover Regeneration pattern above so all volumes get consistent series branding
5. **Update `next_book_title` references** — Back-cover "Coming Soon" / "Next in Series" text in build scripts may reference books by old series names
6. **Check for stale old-series references** — Build scripts may still refer to the old series name in `series = "Old Series"`, author bio text, or copyright text
7. **Rebuild all volumes in sequence** — Each volume may have its own build script; run them all
8. **Verify cross-volume consistency** — All 5 volumes should show the same series name, consistent volume numbering, and matching cover typography

## Series Naming Research

When the user asks you to find a new series name (e.g., "research and find some names" for the series title):

### 1. Understand the Series' Tone
Read the first few pages of at least one manuscript to understand the series' genre, mood, and voice. A name that fits a hard-sci-fi survival story won't work for a political space opera.

### 2. Search for Existing Series
Use `web_search` to find existing book series with similar themes. Record which names are already taken so you don't propose duplicates:

```
web_search: "lunar colony book series names"
web_search: "moon base sci-fi series"  
web_search: "best sci-fi lunar series" 
```

Check Goodreads, Wikipedia, and publisher pages for confirmation.

### 3. Generate Candidate Names
Brainstorm 5–8 unique, untaken options. Each should have:
- A clear **vibe** (1–2 words describing the feel)
- A **reason it works** tied to the series' content
- Confirmation it's **not already used** by an existing series

### 4. Present in a Comparison Table
| Name | Vibe | Why It Works |
|:-----|:-----|:-------------|
| **The Lunar Foundation** | Strong, grounded | Ties to Book 1's ending, evokes permanence |

Include a "Notable Avoids" subsection listing already-taken names with author/series references so the user sees due diligence.

### 5. Let the User Decide
Present your recommendations and wait for a decision before applying any changes. Do NOT pick a name unilaterally — the series name is a creative branding decision.

## Title Uniqueness Validation

Whenever renaming a book within a series, validate that the new title does not conflict with:

1. **Other books in the same series** — search sibling directories or the series directory:
```
search_files(path='/books/Series_Name/', pattern='Old_Title')
```
Check the manuscript.md `# Title` line, not just filenames.

2. **Books in other series by the same author** — check `/books/` for any `.md` files whose `# Title` line matches.

3. **Existing published works** — the new name shouldn't accidentally match a famous book. A quick web search for the proposed title is sufficient.

Present the results in a table with columns: Book #, Current Title, New Title, Unique? (✓/✗).

## Cross-Book Reference Updates

When renaming a single book in a series, other books in the same series may reference it by name in:

- **Back-matter "About the Series" sections** — Book 3's final pages often list all books in the series with descriptions
- **Character biographies** — character documents may say "character X first appeared in [Old Title]"
- **Concept documents** — series bibles, timelines, and outlines often reference books by name
- **"Coming Next" teasers** — the end of Book 2 may preview Book 3 by its title
- **HTML back-matter** — rendered in the other books' final HTML output (not just manuscripts)
- **Author bio** — each book's HTML `<div class="about-author">` often lists the series name (e.g., "Bob Mills is the author of the [Series Name] series"). This is a subtle, easy-to-miss reference that must be updated in EVERY volume of the series, not just the renamed one.

### How to Find Them

Search the ENTIRE series directory hierarchy, not just the book being renamed. **Use the `search_files` tool** (which greps file content) rather than relying on filename patterns alone — the old name may live inside `.md`, `.html`, `.json`, or `.py` files whose filenames don't contain it:

```
search_files(path='/books/Series_Name/', pattern='Old Title')
```

This catches references in all manuscript.md, HTML, character docs, outlines, and concept files across every volume.

### Update Strategy
- **Manuscripts (.md)**: Direct find-and-replace in each file
- **HTML output**: Same replacement, but also check the `<title>` tag and title-page `<h1>`
- **PDF**: Must be regenerated from updated HTML (weasyprint or equivalent)
- **Supporting documents** (characters, concept, outline): Update references but preserve the descriptive context — the reference is just changing what the book is called, not its role in the story

### Pitfall
Do NOT search only the renamed book's directory. Other books in the series commonly reference earlier books by name in their "About the Series" back matter and are easily missed. Always do a cross-series search.

## Cover Art Swapping Between Volumes

When rebranding a series, you may decide that a specific volume's artwork would work better for another volume. The raw images get swapped, then each cover is regenerated with its correct text overlay — no need to re-generate art from scratch.

**Process:**

1. **Back up both raw files** first, then swap:
```bash
cp /path/to/Book3/generated/raw_cover_raw.png /tmp/bk3_raw.bak.png
cp /path/to/Book5/covers/Book5_raw.png /path/to/Book3/generated/raw_cover_raw.png
cp /tmp/bk3_raw.bak.png /path/to/Book5/covers/Book5_raw.png
```

2. **Re-run the batch cover script** to apply correct text to the swapped art:
```bash
python3 generate_series_covers.py
```

3. **Verify by file size** — the swapped volumes should have exchanged sizes:
- Book 3's output cover size ≈ old Book 5 size
- Book 5's output cover size ≈ old Book 3 size

**Rule of thumb:** Always swap the *raw* images (pre-text), not the final cover output. This ensures the text rendering (gradient positions, title spacing) uses the correct art dimensions for each volume.

### Chained/Sequential Swaps (Provenance Tracking)

When doing **multiple sequential swaps** (e.g., Book3↔Book5, then Book3↔Book2), the raw art moves through a chain and the end state can be confusing:

```
Original:  B2=Art_A  B3=Art_B  B5=Art_C
Swap 1 (B3↔B5):  B3=Art_C  B5=Art_B
Swap 2 (B3↔B2):  B2=Art_C  B3=Art_A
Final:     B2=Art_C  B3=Art_A  B5=Art_B
```

**Always maintain a provenance ledger** by telling the user the full chain of where each volume's art originated. After each swap, state clearly:

- Which volumes were swapped
- What the new state is for each affected volume
- Where each image *originally* came from

This prevents confusion when the user later says "Book 2's art doesn't look right" — you need to know that Book 2 got Book 5's original art, not Book 2's own.

**Verification for chained swaps:** After all swaps, check each volume's output cover — the sizes should match the *original source volume's* typical output size, not the current volume's previous output size. Then summarize the full final state in a table.

## Common Pitfalls

- **EPUB metadata hardcoded in build scripts**: The EPUB `content.opf` is often generated by a Python script that has hardcoded `dc:title` and `dc:creator` strings. Always check the build script — don't assume the EPUB was regenerated from the updated HTML.
- **Cover output filename mismatch**: The cover script saves to one filename, the build script references a different filename. Check both are the same after renaming.
- **Copyright year embedded in strings**: Author name changes often propagate into copyright lines inside build scripts' f-strings. Search for the old name in ALL string literals.
- **Filenames with old title**: The EPUB output path in the build script may contain the old title (e.g., `Old_Title.epub`). Update the filename constant.
- **Multiple book series cross-reference**: If Book 1's back cover says "Coming Soon: Book 2 — Old Title", you must update that reference text in the build script too.
- **ISBN/manuscript CSS metadata**: Some HTML/CSS files embed the title in comments, alt text, or CSS `@page` margin boxes.
- **Back cover PDF is separate**: The back cover PDF is a standalone document with hardcoded title text. It does NOT auto-update when you rebuild the main HTML/PDF. You must regenerate it separately (write new HTML → weasyprint) with the new title.
- **Marketing docs need fresh creation when package dir is new**: If the KDP package directory is created from scratch (new name), marketing docs don't exist yet. Running `shutil.copytree` from the old package keeps old filenames. Instead, write fresh marketing doc files with updated titles. The `marketing-copy` templates in the `book-marketing-launch` skill can be used as a reference.
- **Source manuscript file gets renamed**: When rebranding, rename the master manuscript file (e.g., `Old_Title.md` → `New_Title.md`) FIRST, then fix all build scripts that reference the old filename. Search for `_REVISED.md`, `_FINAL.html`, `_FINAL.pdf` patterns in scripts — these are common hardcoded paths.
- **Build script path references lag behind renames**: After renaming the manuscript file, build scripts using `MD_PATH = BASE / "Old_Title.md"` will break silently (FileNotFoundError at runtime). Always check MD_PATH, OUT_HTML, OUT_PDF, COVER paths in build scripts after a rename.

## Agent-Internal References (Cron Prompts, Memory, Skills, Task Queue)

After rebranding is applied to the publishing pipeline, the agent's own persistent references may still use old titles. These stale references can cause the agent to keep generating tasks for a book that no longer exists under that name.

### 1. Agent Task Queue (agent-communications.jsonl) ⬅ CRITICAL

The CEO orchestrator writes tasks to `agent-communications.jsonl` that reference books by their old titles. Pending and overdue tasks will keep the writer agent attempting to work on a nonexistent project.

```bash
# Check for stale task references:
grep 'Old Title' ~/.hermes/.openclaw/workspace/memory/agent-communications.jsonl

# Total count:
grep -c 'Old Title' ~/.hermes/.openclaw/workspace/memory/agent-communications.jsonl
```

For each stale task, mark it as **failed** with the rebranding reason so no agent polls it:

```python
import json

path = '/home/bob/.hermes/.openclaw/workspace/memory/agent-communications.jsonl'
with open(path) as f:
    lines = [l.strip() for l in f if l.strip()]

updated = []
for line in lines:
    entry = json.loads(line)
    if 'Old Title' in str(entry) and entry.get('status') in ('pending', 'overdue', 'assigned', 'active'):
        entry['status'] = 'failed'
        entry['payload']['reason'] = 'Book renamed/completed. No reconstruction needed.'
        entry['payload']['resolved_at'] = '<current-ISO-timestamp>'
        entry['payload']['resolved_by'] = 'ceo-cleanup'
    updated.append(json.dumps(entry))

with open(path, 'w') as f:
    for line in updated:
        f.write(line + '\n')
```

**Don't delete completed/historical entries** — they preserve the audit trail. Only fail pending/overdue/active ones that would generate new work.

**Always check both the task title AND the payload context** — old titles can be embedded in instructions, context strings, and requirements arrays, not just the task field.

### 2. CEO Orchestrator Skill Template

The `ceo-agent-orchestrator` skill contains example JSON template blocks that show task writers how to format assignments. If these examples use an old book title, the next cron run may generate a task referencing it:

```json
{\"task\":\"Write the next chapter for OLD TITLE manuscript\",\"payload\":{\"instructions\":\"Check which chapter needs writing next...\"}}
```

```bash
grep -n 'Old Title' ~/.hermes/skills/business/ceo-agent-orchestrator/SKILL.md
```

Fix with `patch` or direct replacement. Use a generic placeholder like "the currently active No Blue Sky series book" rather than a specific title that could go stale again.

### 3. Cron Job Prompts
Cron jobs that generate briefings or reports often hardcode book titles in their prompt text. Search for old titles across all job prompts:
```bash
hermes cron list
```
For each job whose prompt preview contains an old title, update it:
```bash
hermes cron update <job_id> --prompt 'New prompt text with new titles...'
```

### 4. Update Agent Memory

Use the `memory` tool to replace or add an entry reflecting the new series/book names. This prevents future sessions from working with stale titles:

```
memory(action='replace', target='memory', old_text='Old Title', content='New Title')
memory(action='replace', target='user', old_text='Old Title', content='New Title')
```

### 5. Skills That Reference Titles
Skills with hardcoded book names in their description or workflow steps. Search skill content:
```bash
grep -rn 'Old Title\\|Old Author' ~/.hermes/skills/
```
Use `skill_manage(action='patch')` to fix any matches.

## Post-Rebranding Pipeline

After text replacements are complete, run these steps in order:

### 1. Regenerate PDFs

After all text replacements in the HTML files, regenerate the print PDFs:

```bash
python3 -m weasyprint /path/to/Book_X.html /path/to/Book_X.pdf
```

Verify page counts match expectations:
```bash
pdfinfo /path/to/Book_X.pdf | grep Pages
```

Do NOT skip this step — the old PDFs still contain the old title/series name in their rendered text.

### 2. Rename Directories & Clean Up

If the book title changed, rename the directory (and its internal files) to match:

```bash
mv Book_1_Old_Title Book_1_New_Title
mv Book_1_New_Title/Book_1_Old_Title.html Book_1_New_Title/Book_1_New_Title.html
mv Book_1_New_Title/Book_1_Old_Title.pdf Book_1_New_Title/Book_1_New_Title.pdf
```

**After confirming** the new directory has all files and the PDFs render correctly, remove the old directory:

```bash
rm -rf Book_1_Old_Title
```

If mid-series or multi-volume renames happened, clean up ALL stale directories. A stale directory with an old name will confuse the next agent session.

### 3. Final Sweep with search_files

After all text changes, directory renames, and PDF regenerations, do a **zero-tolerance sweep** across the entire series directory:

```python
search_files(path='/books/Series_Name/', pattern='Old Title')
search_files(path='/books/Series_Name/', pattern='Old Series Name')
```

Every count should be **0**. If any file still contains the old string, patch it and regenerate its PDF. The most common missed files are:
- Chapter fragment/split files (`chapters_01_10.md`, etc.) — these often have a `# Title — Book N of Series Name` header
- Character biography / concept / outline documents
- Other books' About-the-Series sections mentioning the renamed book
- Author bios in every volume

## Verification Checklist

After all changes are applied:
- [ ] Title appears correctly on the cover image
- [ ] Title page in the ebook shows new title + author
- [ ] Copyright page shows new author
- [ ] EPUB metadata (dc:title, dc:creator) shows new values
- [ ] Filenames are updated (or old stubs cleaned up)
- [ ] Old title/author strings no longer appear in any source file (verified by search_files sweep)
- [ ] Series name is consistent across all volumes
- [ ] Back-cover "Coming Soon" cross-references use the new book name
- [ ] Other volumes "About the Series" sections updated if they reference the renamed book
- [ ] Author bios in ALL volumes updated with new series name
- [ ] Chapter fragment files (if any) updated with new series/book name
- [ ] Character/concept/outline docs updated for cross-references
- [ ] PDFs regenerated from updated HTML
- [ ] Directories renamed and old stubs deleted
- [ ] Marketing/KDP docs updated
- [ ] Cron job prompts updated with new titles
- [ ] Agent memory and user profile updated with new titles
- [ ] Skills checked for hardcoded old titles
