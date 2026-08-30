---
name: reader-magnet-production
displayName: Reader Magnet Production
description: Full workflow for producing and deploying reader magnet novellas — structured editorial rewrites, EPUB/PDF generation with pure Python, DreamHost deployment via pexpect SCP. Covers the editorial spec pattern this user prefers, the 6x9" PDF build technique, and the subscriber-gated website deployment.
category: publishing
tags: [reader-magnet, novella, epub, pdf, deployment, editorial, dreamhost]
related_skills: [mifeco-website-deployment, book-creation, manuscript-restructuring]
---

# Reader Magnet Production

## When to Use

- The user provides structured editorial specs (numbered items, categories, "How:" descriptions) for a novella rewrite
- You need to generate EPUB + PDF from a markdown novella source
- You need to deploy a reader magnet to the DreamHost server at mifeco.com/books/
- You're rewriting an existing reader magnet novella (Cindy Lou, No Blue Sky, Lunar Foundation, Age of Lightships)

## Structural Patterns (Learned from User Corrections)

### Pattern A: Cold Open + Flashback

The user repeatedly requires this structure for maximum commercial impact. The user's phrase: "Open with disaster, not arrival."

**How to do it:**
1. First sentence drops the reader into the middle of a crisis (alarms, signal detection, pressure loss, countdown)
2. No setup, no preamble, no "the Moon had no welcome mat" — start with action
3. After the hook, insert a transition like "72 hours earlier" or "Seventy-two hours earlier:"
4. Then tell the story leading up to the opening moment
5. The opening crisis becomes a payoff when the narrative catches up

**Examples from this session:**
- First Light: "Emergency alarms. Tom was already running..." then flashback 72 hours
- Last Transmission: "The signal arrived at 03:47 ship time, and even then it almost didn't."

### Pattern B: The Character Wound -> Family Goodbye -> Transformation Arc

Every novella rewrite this session required the same emotional architecture:

1. **The Wound:** The protagonist carries a past failure or loss connected to someone they loved.
2. **The Goodbye:** A dedicated family farewell scene is the emotional centerpiece. Place it at roughly 60% mark. Include: a meal, a porch conversation, a moment where a family member says "I'm proud of you" or equivalent.
3. **The Transformation:** The protagonist ends with an internal shift — they realize they came to build something larger than structures. Explicit, not implied.

### Pattern C: Three-Rolling-Complication Escalation

Not one problem. Three. The first attempt to solve problem 1 MUST FAIL DRAMATICALLY.

### Pattern D: EVA / Solo Confrontation Sequence

For space/sci-fi stories, the protagonist goes outside alone. One mistake = death. Environment becomes a character (loneliness, scale, silence).

### Pattern E: Open-Ended Mystery Seeding

The ending must seed a mystery that drives readers into Book 1 (subsurface reflection, instant reply violating light-speed).

## Storage Conventions

All reader magnet source `.md` files live under the website source at:
```
/home/bob/Desktop/hermesfiles/cindy-lou-series/books-mifeco-website/magnets/
```

**Naming:** lowercase kebab-case — `{series}-before-the-dust.md`, `cindy-lou-missing-retainer.md`

PDF/EPUB output files go to the same directory (they're served from `/books/magnets/` on the server).

## Editorial Rewrite Pattern

### CRITICAL LESSON: Weave, Don't Replace

The user explicitly corrected this approach. When given editorial specs for a novella rewrite:

**WRONG:** Create a completely new story from scratch using the specs as a template. This loses the original's plot, characters, and emotional architecture.

**RIGHT:** Take the EXISTING story as the foundation. Weave all improvements INTO it alongside the existing scenes. Preserve:
- The original character names and relationships
- The original plot structure and key scenes
- The original tone and voice
- The original chapter flow and pacing

The user's exact words: "Instead of adding the new features to the existing story you lost the experience."

### Spec Pattern Recognition (from 3 novella rewrites this session)

The user provides specs in three distinct formats. Learn to recognize each:

**Format 1: 10-Item List with "How:" (Cindy Lou/30k word rewrite patch)**
- Each line has a number, emoji, label, and "How:" line
- 10 items is a PATCH — weave into existing without changing plot
- Each "How:" is a specific scene to add or change

**Format 2: 5-Priority + 25-Item Grid (No Blue Sky full rewrite)**
- First 5 items are PRIORITIES (labeled "important changes")
- Then 25 items organized into categories (Character, Worldbuilding, Structural, Prose, Ending)
- This is a FULL REWRITE — start from scratch using the existing plot skeleton

**Format 3: 44-Item Deep Spec (Last Transmission full rewrite)**
- Organized by category: Character, Plot, Structure, Prose, Ending
- Includes SPECIFIC LINES for the ending (e.g., "Final line: 'The signal had been waiting for humanity. It had been waiting for her.'")
- This is a PRESCRIPTIVE rewrite — follow the spec literally

### The Data-Driven Page Count

The user specified "at least 30 pages at 6x9 inch" for the Cindy Lou novella. Here's the actual math:

| Font | Line Spacing | Words per 6x9 page | Pages for 3K words | Pages for 7K words | Pages for 10K words |
|------|-------------|-------------------|-------------------|-------------------|--------------------|
| 11pt | 1.5 | ~300 | 10 (+6 front/back = 16) | 23 (+6 = 29) | 33 (+6 = 39) |
| 12pt | 1.5 | ~260 | 12 | 27 | 38 |

To hit "at least 30 pages," the story content needs ~7,500+ words when including front/back matter (title, copyright, TOC, about author, other books).

Always check: `wc -w <novella_source.md>` to confirm target before building.

### "Expand to 7000 words" Requests

When the user says "expand to 7000 words" AND provides complex specs (25-44 items), the approach is:
1. Read the original story fully
2. Map every spec item to a place in the existing narrative
3. Write new scenes corresponding to each spec item
4. DO NOT delete original scenes unless they conflict with spec items
5. Aim for 600-650 lines / 7,000 words / 27-35 pages at 6x9"

### What the user wants (learned from corrections)

When the user gives you editorial specs for a novella rewrite:

1. **Weave improvements INTO the existing story.** Do NOT replace or truncate the original — expand it. The user corrected: "Instead of adding the new features to the existing story you lost the experience." Keep the original plot structure, characters, and scenes. Weave new content alongside them.

2. **Follow the numbered spec format.** The user provides specs as:
   ```
   # Number | Emoji | Label
   • How: [specific change]
   ```
   Address every numbered item. Each must be visible in the output.

3. **Hit the page count target.** The user frequently specifies "at least 30 pages at 6x9 inch." 30 pages at 6x9" with 11pt font requires ~9,000-10,500 words of story content (plus front/back matter).

4. **Prioritize these five changes** (most important per user signals):
   - Family goodbye chapter (emotional centerpiece)
   - Character vulnerability / personal sacrifice
   - Father/abandonment theme (or parent wound)
   - Mission uncertainty / risk / stakes
   - "Earth" or "NYC" as a character readers will miss

5. **Emotional depth hierarchy** (most to least important per user's specs):
   - Family relationships (siblings, parent-child)
   - Romantic tension (optional, genre-depending)
   - Female friendship circles
   - Personal villain confrontation
   - Character arc from doubt to confidence

6. **Sensory grounding** — Every scene needs physical details: smells, sounds, textures, temperature, food. The user repeatedly asks for Earth/NYC to feel alive before the character leaves it.

### When the user provides "25 improvements" (like the No Blue Sky rewrite):

They tend to group into these categories — address them systematically:
- **Character improvements** -> family goodbye, vulnerability, differentiate voices
- **Worldbuilding improvements** -> Earth as character, Mars awe, decline shown not told
- **Structural improvements** -> expanded opening, emotional stakes before technical
- **Prose improvements** -> sensory detail, subtext, show don't tell
- **Ending improvements** -> launch tension, Mars arrival wonder

### When the user provides "44 improvements" (like the Last Transmission rewrite):

The extra density comes from:
- **Personal connection to the discovery** (signal pattern linked to mother's childhood game)
- **Hidden layers** (golden ratio is layer 1; second encoding beneath)
- **Signal as a character** (it learns, changes when observed, rearranges into mathematics nobody entered)
- **Crew politics and vote** (senior staff disagree, fleet command pushes back)
- **Impossible reply violating light-speed** (creates the cliffhanger)
- **Final revealed connection** (mother's lost vessel appears in reply data)

### Target Length

The user explicitly said "make it 50% longer" and "expand to 7000 words." For expanded novellas:

| Target | Lines | Words | 6x9 Pages |
|--------|-------|-------|-----------|
| Standard rewrite | ~500-550 | ~5,000-6,000 | ~25-30 |
| Expanded rewrite | ~600-650 | ~7,000-7,500 | ~27-35 |

Always check word count after writing: `wc -w <file>`.

### Proofreading

Always scan for:
- Encoding artifacts (the AUTHOR line in Python build scripts consistently gets corrupted)
- Stray foreign characters from prior versions
- Markdown consistency (heading levels, scene break markers)

### The Build Script AUTHOR Encoding Bug

After writing any Python build script, verify the AUTHOR line isn't corrupted:
```bash
grep -n "^AUTHOR" /tmp/build_script.py
```

If it shows garbage characters, fix by reading the file, replacing the line, and writing it back. Always verify after fixing.

### "No Chapter Headings" Mode (Last Transmission Pattern)

For stories with "no front-loaded structure" — remove numbered `## Part X` headings, let story flow continuously. Add descriptive `##` headings afterward at natural pivot points so the EPUB/PDF builder can split the content into chapters for the TOC.

## EPUB Generation (Pure Python, no ebooklib)

Use `zipfile` + `xml.sax.saxutils` — no external dependencies needed:

```python
import zipfile, io, re
from xml.sax.saxutils import escape as xmlescape
from datetime import datetime, timezone

def build_epub(md_path, epub_path, title, author, slug):
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    book_id = f"urn:uuid:{slug}-{ts}"

    with open(md_path, encoding='utf-8') as f:
        content = f.read()

    # Split on # or ## headings
    sections = []
    cur_h, cur_l = None, []
    for line in content.split("\n"):
        s = line.strip()
        if s.startswith("# ") or s.startswith("## "):
            if cur_h is not None:
                sections.append((cur_h, "\n".join(cur_l)))
            cur_h = s.lstrip("#").strip()
            cur_l = []
        else:
            cur_l.append(line)
    if cur_h:
        sections.append((cur_h, "\n".join(cur_l)))

    # Classify: front_matter, chapters, back_matter
    # Write EPUB zip (see build script for full implementation)
```

**CSS for EPUB:**
```css
body { font-family: Georgia, 'Times New Roman', serif; line-height: 1.5; margin: 5%; }
h1 { font-family: 'Helvetica Neue', Arial, sans-serif; text-align: center; }
h2 { font-family: 'Helvetica Neue', Arial, sans-serif; text-align: center; page-break-before: always; }
p { margin: 0.3em 0; text-indent: 1.2em; }
```

## PDF Generation (fpdf2, 6x9 Trim)

Use `fpdf2` (installed via pip). Generate at 6x9 (152.4×228.6 mm) with DejaVu Serif:

**Cover embedding:** After generating the interior PDF, prepend the cover image as the first page using the workflow in `references/cover-embedding-pdf.md`. This is essential for reader magnet PDFs served as direct downloads — readers opening the file should see the cover first.

```python
from fpdf import FPDF

W, H = 152.4, 228.6  # 6x9 inches in mm
MARGIN = 14
FS = 11

pdf = FPDF(orientation='P', unit='mm', format=(W, H))
pdf.set_auto_page_break(auto=True, margin=MARGIN)
pdf.add_font("DV", "", "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf")
pdf.add_font("DV", "B", "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf")
# Use DejaVuSerif for italic too (no DejaVuSerif-Italic available)
pdf.add_font("DV", "I", "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf")
pdf.set_left_margin(MARGIN)
pdf.set_right_margin(MARGIN)
```

## Deployment to DreamHost

### Server Info
```
Host: IAD1-SHARED-B8-42.DREAMHOST.COM
User: dh_mwpxuu
Password: Rm2214ri#### (literal — includes the ####)
Web root: /home/dh_mwpxuu/mifeco.com/books/
Site URL: mifeco.com/books/ (NOT books.mifeco.com — that subdomain isn't configured)
```

### Upload via pexpect SCP

```python
import pexpect
import os

# Read password from .env (never hardcode)
env_path = os.path.expanduser("~/.hermes/.env")
PASS = None
with open(env_path) as f:
    for line in f:
        if "DREAMHOST_PASSWORD" in line and "=" in line:
            PASS = line.split("=", 1)[1].strip().strip('"').strip("'")
            break

REMOTE_DIR = "/home/dh_mwpxuu/mifeco.com/books/magnets"

for local_path in [epub_path, pdf_path]:
    fname = local_path.split("/")[-1]
    child = pexpect.spawn('scp', [
        '-o', 'StrictHostKeyChecking=accept-new',
        '-o', 'PubkeyAuthentication=no',
        local_path,
        f'dh_mwpxuu@iad1-shared-b8-42.dreamhost.com:{REMOTE_DIR}/{fname}'
    ], timeout=60, encoding='utf-8')
    child.expect('password:', timeout=15)
    child.sendline(PASS)
    child.expect(pexpect.EOF, timeout=60)
    child.close()
```

### Post-Deploy Checklist

After uploading new magnet files:

1. **Check the series landing page** — grep the remote `index.html` for magnet links. Fix filename if it changed.
2. **Check the subscribe API** — grep `/api/subscribe.php` for old filenames. There are TWO code paths (duplicate subscriber + new subscriber), and BOTH must be updated.
3. **Check the main HTML page** — grep `index.html` for old magnet references.
4. **Remove old files** — `rm -f` the old magnet PDF/EPUB from the server.
5. **Remove old `.md` source** — the `.md` source file isn't needed on the server; remove it.
6. **Verify no stale references** — `grep -rn "old-filename" /home/dh_mwpxuu/mifeco.com/books/` should return nothing.

## Delivery for Approval

After completing a rewrite or review, send the summary to the user via Telegram for approval before considering the task done:

1. Format key findings per novella as a structured summary
2. Send to `telegram:Robert Mills (dm)` with `send_message`
3. Include: word count, page count, key changes, and any blockers
4. Wait for user response before assuming the work is accepted

The user reviews work through Telegram and provides feedback or sign-off there.

### Common Pitfalls

- **Filename mismatch:** The HTML may reference a different filename than what you uploaded. The Cindy Lou page initially linked to `/magnets/cindy-lou-magnet.epub` but the old files were named `cindy-lou-missing-retainer.epub`. Always check the actual HTML on the server.
- **Two subscribe code paths:** The subscribe.php has `cindy-lou-magnet.pdf` (or similar) at TWO locations — a duplicate-subscriber return block and a new-subscriber block. Both must be updated.
- **URL prefix:** The server uses `/books/` prefix in all paths (e.g., `/books/magnets/cindy-lou-magnet.epub`), not bare `/magnets/`.
- **AUTHOR line encoding bug:** When writing Python build scripts via `write_file`, the AUTHOR line consistently gets corrupted (characters replaced with `***`). Fix by patching the file directly with sed after writing. Always verify after writing: `grep -n "^AUTHOR" build_script.py`

- **USB sync:** After updating local magnet files, sync to both USB directories:
  ```bash
  cp /home/bob/Desktop/hermesfiles/cindy-lou-series/books-mifeco-website/magnets/*.epub /mnt/usb_4tb/books/Cindy_Lou_Legal_Capers/books-mifeco-website/magnets/
  cp /home/bob/Desktop/hermesfiles/cindy-lou-series/books-mifeco-website/magnets/*.pdf /mnt/usb_4tb/books/Cindy_Lou_Legal_Capers/books-mifeco-website/magnets/
  cp /home/bob/Desktop/hermesfiles/cindy-lou-series/books-mifeco-website/magnets/*.md /mnt/usb_4tb/books/Cindy_Lou_Legal_Capers/books-mifeco-website/magnets/
  ```
  Also sync to the secondary USB path at `/mnt/usb_4tb/books/books-section/magnets/`. Remove old-named files from USB mirrors.

## Session-Specific Details

See the `mifeco-website-deployment` skill's `references/reader-magnet-replacement.md` for the single-PDF replacement workflow.

See `references/cover-embedding-pdf.md` for the PIL+PyPDF2 workflow to prepend cover images to reader magnet PDFs before deployment.

See session history for specific editorial specs for each reader magnet novella.

### Reference: Editorial Spec Patterns

See `references/editorial-spec-examples.md` for the three proven spec formats the user provides (10-item list, 5-priority + 25-item, 44-item deep rewrite), with the critical lesson about weaving improvements into the existing story foundation.