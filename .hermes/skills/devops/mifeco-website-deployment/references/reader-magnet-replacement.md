# Reader Magnet Replacement Workflow (PDF + EPUB)

When replacing a gated reader magnet on the mifeco.com/books/ section, reader magnets ship as **both EPUB and PDF**. The series landing pages link to `/magnets/<series>-magnet.epub` and `/magnets/<series>-magnet.pdf`.

## 0. Editorial Workflow — Expanding/Improving a Reader Magnet Novella

When the user asks you to rewrite or improve a reader magnet novella, the key rule is:

**Build ON the existing story — do NOT replace it.** The original plot, characters, voice, and structure are the foundation. All improvements (more humor, romantic tension, higher stakes, etc.) must be *woven into* the existing chapter framework, not substituted for it. A rewrite that loses the original story beats and replaces them with new content is a failure — the user will say "you lost the experience."

**Approach to use:**
1. Read the full novella source — understand its structure, character voices, and pacing
2. Map the requested improvements to existing chapters (don't add random new chapters unless explicitly asked)
3. Expand within chapters: insert new scenes (e.g., romantic banter, friendship circle moments) between existing story beats rather than removing or replacing beats
4. New chapters should extend the existing plot (e.g., a chapter between the climax and epilogue for the romantic ending)
5. Character arc must feel earned — personal doubt introduced early, resolved by the end
6. Every character introduction from the original stays; new characters (friends, villains) are additive

**Page count for 6x9" PDF:** A 6x9 inch page at 11pt DejaVuSerif with 0.55" margins holds ~280-320 words (text, not counting blank space for chapter breaks). To hit 30 pages of content, target ~7,000+ words (628+ lines of markdown). Front matter (title, copyright) + back matter (about the author, thank you) add ~4-5 pages, for a total of 30-35 pages.

## 0a. Generate EPUB + PDF from Novella Source

Each series has a novella source file at `/home/bob/cindy-lou-series/reader-magnet/Missing_Retainer_Novella.md` (or equivalent for other series under `/home/bob/<series>/reader-magnet/`).

**Build approach:** Pure-Python EPUB (zipfile + stdlib — no ebooklib needed). PDF uses fpdf2 (install: `pip3 install fpdf2`). Both are built from a single Python script at `/tmp/build_reader_magnet.py`.

**Critical — heading level bug in EPUB splitter:** Novella sources typically use `## ` (h2) for chapter headings, NOT `# ` (h1). The section-split parser must match on both `# ` and `## `, or all chapters collapse into one. Use `stripped.startswith("# ") or stripped.startswith("## ")`.

**Critical — font availability:** `/usr/share/fonts/truetype/dejavu/` does NOT have `DejaVuSerif-Italic.ttf`. Available: `DejaVuSerif.ttf`, `DejaVuSerif-Bold.ttf`, `DejaVuSans.ttf`, `DejaVuSans-Bold.ttf`. Use DejaVuSerif regular as the italic fallback.

**6x9" PDF setup (fpdf2):**
```python
from fpdf import FPDF
W = 152.4  # 6 inches in mm
H = 228.6  # 9 inches in mm
MARGIN = 14  # ~0.55 inches
FONT_SIZE = 11
pdf = FPDF(orientation='P', unit='mm', format=(W, H))
pdf.set_auto_page_break(auto=True, margin=MARGIN)
pdf.add_font("DejaVu", "", "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf")
pdf.add_font("DejaVu", "B", "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf")
pdf.add_font("DejaVu", "I", "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf")  # no italic variant, fallback to regular
```
Line height 5.2mm at 11pt for body text gives ~32-35 lines per page, ~280-320 words.

**File naming convention for the website:**
- `books-mifeco-website/magnets/<slug>-magnet.epub` ← what the HTML links to
- `books-mifeco-website/magnets/<slug>-magnet.pdf`  ← what the HTML links to

Slugs match the series landing page directory: `cindy-lou`, `no-blue-sky`, `lunar-foundation`, `age-of-lightships`.

## 1. Upload Both Files

Upload to `/home/dh_mwpxuu/mifeco.com/books/magnets/`:

```python
import pexpect
for f in ['<slug>-magnet.epub', '<slug>-magnet.pdf']:
    local = f'/home/bob/cindy-lou-series/books-mifeco-website/magnets/{f}'
    child = pexpect.spawn(f'scp {local} dh_mwpxuu@mifeco.com:/home/dh_mwpxuu/mifeco.com/books/magnets/{f}', timeout=60, encoding='utf-8')
    child.expect('password:', timeout=15)
    child.sendline('PASSWORD')
    child.expect(pexpect.EOF, timeout=60)
```

**Naming:** Use `<slug>-magnet.epub` + `<slug>-magnet.pdf`, matching what the landing page HTML references.

**Remove old files** after upload — stray old-named files create dead download links. Example:
```
ssh ... rm /home/dh_mwpxuu/mifeco.com/books/magnets/<slug>-missing-retainer.*
```

## 1b. CRITICAL — Server Path Prefix

The local source files use `/magnets/<file>` paths (built for a `books.mifeco.com` root domain). **The actual server path is `mifeco.com/books/magnets/<file>`**. The server-side HTML already uses the correct `/books/magnets/` prefix — never strip it when editing server files.

**What this means when updating a landing page on the server:** Always edit the server's version in place (via sed over SSH) rather than uploading the local HTML. The local file has wrong paths for the server context.

## 2. Update the Series Landing Page HTML

Each series has its own landing page at `books-mifeco-website/<slug>/index.html`. The magnet section has download buttons:

```html
<a href="/magnets/cindy-lou-magnet.epub" download class="series-btn">Download EPUB</a>
<a href="/magnets/cindy-lou-magnet.pdf" download class="series-btn">Download PDF</a>
```

Also check the main `index.html` `#magnets` section for any gated (subscribe-to-unlock) magnet cards.

## 3. Update the Subscribe API (TWO locations — PDF only)

`/home/dh_mwpxuu/mifeco.com/books/api/subscribe.php` has download links in **two code paths:**
1. Duplicate email (returning subscriber) — first occurrence
2. New subscriber — second occurrence near EOF

Both must have title + PDF url updated. **The subscribe API only serves PDF links** (not EPUB) — the EPUB is available via direct download button on the series landing page. Only fix the `.pdf` filename in the API.

Best: fix via SSH sed:
```
ssh ... sed -i 's|old-name\\.pdf|new-name.pdf|g' /home/dh_mwpxuu/mifeco.com/books/api/subscribe.php
```

## 4. Verify — grep for STALE references BEFORE closing

Run a comprehensive stale-reference scan before declaring done:
```bash
grep -rn "old-filename" /home/dh_mwpxuu/mifeco.com/books/
```
Check ALL files — HTML, PHP, JS. A hit in any file means a dead download link on the live site. Fix every hit.

Also verify the new files are HTTP-200:
```bash
curl -sI https://www.mifeco.com/books/magnets/<slug>-magnet.epub | head -3
curl -sI https://www.mifeco.com/books/magnets/<slug>-magnet.pdf | head -3
```