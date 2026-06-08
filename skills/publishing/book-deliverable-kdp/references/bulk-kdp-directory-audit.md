# Bulk KDP Directory Audit & Fill

## When to Use

When the user asks to "check all book directories", "make sure every book has X", "audit KDP readiness across all books", or "fill in missing metadata for all books". This is the **audit-and-fill** path — distinct from building a single book's KDP package from scratch (which the main SKILL.md covers).

## Required Assets Per Book Directory

Every book directory should contain these 11 items:

| # | Asset | Type | Notes |
|---|-------|------|-------|
| 1 | Cover image | `.jpg` / `.png` | Front cover, high-res |
| 2 | EPUB | `.epub` | Kindle-compatible EPUB3 |
| 3 | Print PDF | `.pdf` | 6x9in, with/without bleeds |
| 4 | KDP package | `.zip` | Complete submission package |
| 5 | Manuscript source | `.html` / `.md` / `.docx` | Chapter files OR `manuscript_src/` dir |
| 6 | Keywords | `.txt` | 7 KDP search keyword phrases |
| 7 | Description | `.txt` | Full KDP listing description |
| 8 | Back cover blurb | `.txt` | Punchy back-cover copy |
| 9 | Author bio | `.txt` / `.md` | 2-3 sentence bio, tailored to book |
| 10 | Author image | `.jpg` / `.png` | Headshot, copied to each directory |
| 11 | Title/subtitle file | `.txt` | Structured title, subtitle, series info |

## Workflow

### Step 1: Audit All Directories

Walk each book directory recursively and check for all 11 assets. Use `os.walk` in Python. Key pitfalls:
- Manuscript source may be in a `manuscript_src/` subdirectory — check `os.walk`'s `dirs` list, not just filenames
- Author bio files may end in `_Bio.txt` or `_Bio.md`
- Keywords files may contain "keyword", "search", or "phrase" in the name
- EPUBs inside KDP zip packages count — check inside `.zip` files too

### Step 2: Generate Missing Metadata

For each book missing metadata files, create all 5 text assets (keywords, description, back cover blurb, author bio, title/subtitle). Write them using Python `open()` / `write()` — not heredoc — to avoid quote escaping issues with backslashes in f-strings.

**Generating accurate descriptions from EPUBs:**
1. Extract the first chapter from the EPUB to understand the actual plot
2. Also check `_resources/` and `_archived/` directories for existing descriptions/bios from previous work
3. Write unique, book-specific content — never re-use generic/template descriptions
4. **Critical**: Archived packages often contain template-quality generic blurbs ("When humanity reaches for the stars, what does it take..."). Always rewrite with book-specific content based on actual chapter text

Extract chapter text from EPUB:
```python
import zipfile, re
def get_first_chapter_text(epub_path, chars=600):
    with zipfile.ZipFile(epub_path, 'r') as zf:
        htmls = sorted([n for n in zf.namelist() if n.endswith(('.html', '.xhtml'))
                       and not any(s in n.lower() for s in ['title','copyright','cover','toc','nav','about','series'])])
        if htmls:
            content = zf.read(htmls[0]).decode('utf-8', errors='replace')
            text = re.sub(r'<[^>]+>', ' ', content)
            text = re.sub(r'&[a-z]+;', ' ', text)
            return re.sub(r'\s+', ' ', text).strip()[:chars]
```

**Keywords file format** (7 slots, each a phrase):
```
# KDP Search Keywords for {Title}
1. phrase one
2. phrase two
...
7. phrase seven
```

**Back cover blurb format:**
```
{Title}
{Series} — {Book#}
by Bob J Mills

[Blurb text — 100-200 words, hook + stakes + comp titles]

ISBN: [TBD]
Cover design: MIFECO Publishing
```

**Author bio variation**: Tailor to book type. Sci-fi series bios emphasize the sci-fi background. Business books emphasize real-world experience. Memoirs emphasize the personal journey.

### Step 3: Extract Manuscript Source from EPUBs

When a book has no manuscript source files but has an EPUB, extract chapter HTML into `manuscript_src/` subdirectory:

```python
import zipfile, os
skip = ['title','copyright','cover','toc','nav','about','series','front','dedic']
with zipfile.ZipFile(epub_path, 'r') as zf:
    htmls = sorted([n for n in zf.namelist() if n.endswith(('.html', '.xhtml'))
                   and not any(s in n.lower() for s in skip)])
    for h in htmls:
        content = zf.read(h)
        out = os.path.join(out_dir, os.path.basename(h))
        with open(out, 'wb') as f:
            f.write(content)
```

### Step 4: Copy Shared Assets (Author Photo)

```bash
for dir in /path/to/books/*/; do
  cp "$AUTHOR_IMG" "$dir/Author_Photo.jpg"
done
```

### Step 5: Final Verification

Run a recursive check across all directories. Report:
- Complete vs incomplete count
- Any remaining missing items
- Total files created

**Critical verification: detect partial KDP packages.** A directory that has
`KDP_PACKAGE/Marketing_and_Compliance/*.txt` but is missing
`KDP_PACKAGE/Kindle/`, `KDP_PACKAGE/Print/`, and `KDP_PACKAGE/*.zip` is
**NOT** KDP-ready. It is "marketing-ready, publishing-incomplete." Flag these
clearly in the report — do NOT count them as having a KDP package. See
`references/kdp-publishing-techniques.md` → "Partial KDP Package Anti-Pattern"
for the full detection and fix workflow.

## Pitfalls

- **Case sensitivity**: File extension checks must be case-insensitive (`.JPG` vs `.jpg`) — use `.lower()` on all filenames
- **EPUB-in-zip**: Some books only have EPUBs inside their KDP zip — check inside zips, not just top-level files
- **manuscript_src directory**: `os.walk` returns `(root, dirs, files)` — check the `dirs` list for manuscript subdirectory names, don't just check filenames in `files`
- **Generic descriptions in archives**: Archived packages contain template-quality blurbs that are identical across all books. Always check: does the description mention the specific book's plot, characters, or themes? If not, rewrite it.
- **Stream stalls during large operations**: When generating content for 12+ books, break into smaller batches. Write files for 3-4 books at a time rather than all at once in a single script.
- **Partial KDP_PACKAGE directories**: A `KDP_PACKAGE/` directory that only contains `Marketing_and_Compliance/` is NOT a complete package. The audit MUST also check for `Kindle/`, `Print/`, images, and the final zip. Counting a marketing-only KDP_PACKAGE as "having a KDP package" is a false positive.
