---
name: book-inventory-and-delivery
description: Find all book projects, identify latest output files per format (PDF, EPUB), fill any missing formats, and deliver everything via MEDIA links in an organized way.
tags: [publishing, delivery, inventory, batch, pdf, epub, bulk]
---

## Memory context (Hindsight)

Long-term memory context is now provided automatically by Hindsight (bank
`mifeco-default`) on every turn — the retired MemPalace manual query step no
longer applies. Do NOT attempt to import `~/.hermes/mempalace` (it was removed
2026-08-19).This retrieves previous decisions, domain-specific context, and lessons learned from the vector memory store.

# Book Inventory and Bulk Delivery

## When to Use

- User asks "deliver all my books", "latest versions", "send me everything"
- User asks to mark books as published/unpublished (see `references/bulk-publish-update.md`)
- User has multiple book projects (3+) across a complex directory layout
- Books have multiple naming formats coexist (e.g., old branding preserved alongside new rebrand) and you need to identify the LATEST per project
- You need to find missing output formats (PDF exists but EPUB doesn't, or vice versa) and fill them in before delivery
- User asks "what changed" between old and new versions of books after a rebranding

## Step-by-Step Process

### 1. Discover All Book Projects

Scan the workspace for distinct book projects. Key indicators:

```bash
# Look for manuscript directories with output files
ls /home/bob/books/ | sort
```

**What constitutes a "book project":**
- A directory containing a manuscript (`.md` or `.html`)
- With published output files (`.pdf`, `.epub`) either inside or in a `publish/` subdirectory
- Distinct subdirectories for separate volumes in a series

### 2. Identify Latest Output Files Per Book

For each book, find the most recent PDF and EPUB by modification time:

```bash
# Check publication directories
ls -lt /path/to/book/publish/*.pdf /path/to/book/*.pdf 2>/dev/null
ls -lt /path/to/book/publish/*.epub /path/to/book/*.epub 2>/dev/null
```

**Key considerations:**
- Multiple naming formats may coexist (e.g., `No_Blue_Sky_4.pdf` AND `No_Air_No_Mercy_V1.pdf`) — these are different editions of the same content
- Check both `publish/` subdirectory and the root book directory
- Compare timestamps to find truly latest files
- If the user has rebranded, both old and new editions may need delivery

### 3. Handle Multiple Versions

When books have been rebranded and both old + new versions coexist:

**Identify the version sets:**
- Old branding files (e.g., `No_Air_No_Mercy_V1.pdf`)
- New branding files (e.g., `No_Blue_Sky_4.pdf`)

**Cross-reference internal titles** by reading HTML `<title>` tags or manuscript headers to confirm which version is which:

```bash
head -20 /path/to/book.html | grep '<title>'
```

**Deliver both** unless the user specifies only the latest. Always label which is which.

### 4. Find and Fill Missing Formats

After identifying all books and their output files, check each book for missing formats:

```python
books = {
    "Book Name": {
        "pdf": "/path/to/book.pdf",
        "epub": "/path/to/book.epub",
    },
}

missing_pdf = [name for name, files in books.items() if not files.get("pdf")]
missing_epub = [name for name, files in books.items() if not files.get("epub")]
```

**When a format is missing, generate it from the available source:**

- **Missing PDF, have HTML:** Use `weasyprint` to convert HTML to PDF
  ```bash
  weasyprint /path/to/book.html /path/to/book.pdf
  ```

- **Missing PDF, have EPUB:** Use `ebook-convert`
  ```bash
  ebook-convert /path/to/book.epub /path/to/book.pdf
  ```

- **Missing EPUB, have HTML:** Use `ebook-convert`
  ```bash
  ebook-convert /path/to/book.html /path/to/book.epub
  ```

- **Missing both, have Markdown manuscript:** Build from scratch using the manuscript preparation pipeline (see `manuscript-preparation-and-delivery` skill)

### 5. Organize and Present the Delivery

Group books logically (by series, then by category) for clear delivery:

```
## 🚀 Series Name (N books)
### 📘 Book Title
MEDIA:/path/to/book.pdf
MEDIA:/path/to/book.epub

## 📖 Standalone Books
### 📓 Book Title
MEDIA:/path/to/book.pdf
MEDIA:/path/to/book.epub
```

**Prefix each book with a short label** (series name, volume number) so the user can scan quickly.

### 6. Compare Changes Between Versions (Optional)

When the user asks "what changed" between old and new versions after a rebranding:

| Aspect | Check | Method |
|--------|-------|--------|
| Title | HTML `<title>`, `<h1>`, manuscript header | `grep -i 'title' book.html \| head` |
| Author | Copyright line, author tag | `grep -i 'author\|by ' book.html \| head` |
| Series label | Subtitle, series line | Read front matter |
| Cover | Visual | Compare old vs new cover PNGs |
| Body content | Chapter text | grep chapter openings — should be identical if only branding changed |

**Present as a table** showing:
| **What** | **Old** | **New** | **Changed?** |
|----------|---------|---------|:---:|
| Title | First Generation | No Blue Sky I: Built from Dust | ✅ |
| Author | Robert Mills | Bob Mills | ✅ |
| Series | Martian Sovereignty | No Blue Sky | ✅ |
| Body text | — | — | ❌ (identical) |

## Common Pitfalls

- **Old vs new filename confusion**: When multiple naming schemes coexist (`No_Blue_Sky_4.pdf` vs `No_Air_No_Mercy_V1.pdf`), always verify the internal `<title>` tag to confirm which is which
- **Missing PDF assumed to not exist**: Check subdirectories like `publish/`, `publish_ready/`, `FINAL_PACKAGE/` — the PDF may be nested deeper than expected
- **Only EPUB found**: Some books may only have EPUB (e.g., Book III). Always check and offer to generate the PDF
- **Cover art swaps**: When covers are swapped between volumes (e.g., Book 2 ↔ Book 3), the raw image files may have been exchanged but the cover PNGs in the final covers directory may not match. Verify the actual cover content matches the expected volume
- **Multiple PDF versions**: A book might have both a full with-cover PDF and a smaller text-only PDF. Prefer the most recent complete version
- **WeasyPrint availability**: Check `which weasyprint` or use the full path from the Hermes venv: `/home/bob/.hermes/hermes-agent/venv/bin/weasyprint`

## Verification Checklist

- [ ] All book projects identified
- [ ] Latest PDF located or generated per book
- [ ] Latest EPUB located or generated per book
- [ ] Old/new versions correctly labeled (if both coexist)
- [ ] All files delivered via MEDIA links in a clear, organized format
- [ ] Missing formats filled before delivery
- [ ] File sizes verified (corrupted files are typically <50KB for images, empty for PDFs)

## KDP Package Completeness Check

When auditing book directories for KDP readiness, distinguish between **marketing-ready** and **publishing-ready**:

**Marketing-ready (partial):**
- `cover.jpg/png` ✓
- `Marketing_Infographic.png` ✓
- `Author_Photo.jpg` ✓
- `KDP_PACKAGE/Marketing_Compliance/*.txt` ✓
- Missing: `KDP_PACKAGE/Kindle/`, `KDP_PACKAGE/Print/`, `KDP_PACKAGE/*.zip`

**Publishing-ready (complete):**
- All of the above, PLUS:
- `KDP_PACKAGE/Kindle/cover.jpg` (Kindle cover)
- `KDP_PACKAGE/Print/{Book}_Print.pdf` (print-ready PDF)
- `KDP_PACKAGE/images/` (chapter illustrations, if applicable)
- `KDP_PACKAGE/{Book}_KDP_PACKAGE.zip` (final zip for KDP upload)

**Flag partial packages clearly** — do NOT report them as "KDP-ready." Books 2-4 of the Age of Lightships series had complete marketing files but zero publishing assets inside KDP_PACKAGE.

## Step 6b: Filesystem Organization — Placing Deliverables into Structured Directories

After identifying the latest files, you may be asked to physically place the canonical deliverables into well-organized subdirectories under series/franchise folders, rather than just listing them via MEDIA links.

### 6b.1. When to Use

- User says "put the latest versions into the correct directory under the series name"
- User wants a production-ready file tree with every book's deliverables in a single clean folder
- User has multiple series and standalone books and wants them organized under `books/SeriesName/Book_N_Title/`

### 6b.2. Canonical Deliverables (The "4 Files Per Book" Pattern)

Every completed book should have exactly these 4 deliverable files at the top level of its folder:

| File type | What | Example |
|-----------|------|---------|
| `.zip` | KDP publishing package or full publishing package | `No_Blue_Sky_1_Built_from_Dust_Publishing_Package.zip` |
| `.epub` | Kindle/ebook file | `No_Blue_Sky_1_Built_from_Dust.epub` |
| `.pdf` | Print-ready PDF | `No_Blue_Sky_1_Built_from_Dust_Print_Ready.pdf` |
| Cover image | Book cover PNG or JPG | `NBS_1_Built_from_Dust_Cover.png` |

### 6b.3. Directory Structure Convention

```
books/
├── No_Blue_Sky_Series/               # Series name (PascalCase + _Series suffix)
│   ├── Book_I_Built_from_Dust/       # Roman numeral + title
│   │   ├── No_Blue_Sky_1_....epub
│   │   ├── No_Blue_Sky_1_....pdf
│   │   ├── NBS_1_...Cover.png
│   │   ├── No_Blue_Sky_1_...Package.zip
│   │   └── .archived/                # Old artifacts (build scripts, old-name files)
│   ├── Book_II_The_Oxygen_Gamble/
│   └── ...
├── Lunar_Foundation_Series/          # Drop "The" prefix, add _Series suffix
│   ├── Book_1_Moon_Rock/
│   ├── Book_2_Mooncoming/
│   └── ...
├── Business_Series/                  # Business books — one level, no roman numerals
│   ├── AI_That_Works/
│   └── Owners_Manual_AI_Agents/
├── Tomorrow_Remembered/              # Standalone books at top level
└── ...
```

**Naming conventions:**
- **Series folders:** Use readable PascalCase with `_Series` suffix (`No_Blue_Sky_Series`, `Lunar_Foundation_Series`, `Business_Series`). Drop "The" prefix from series directory names (e.g., `The_Lunar_Foundation/` → `Lunar_Foundation_Series/`).
- **Book folders:** `Book_N_Title` with underscore separators, roman numerals for one series and Arabic for another (keep existing convention per series).
- **Series root loose files:** Any utility scripts, UUID-named images, `__pycache__`, or planning docs at the series root should go into a `_resources/` subdirectory. Only book subdirectories and `_resources/` should live at series root level.
- **Deliverable files:** Use the established naming from the publishing_output/packages (they are authoritatively the latest).

### 6b.4. Step-by-Step Execution

**Step 1: Discover all books and their latest deliverables**

Use the steps in Section 2 to find latest .epub, .pdf, .zip, and cover per book. Key sources:
- `publishing_output/packages/` — has the latest KDP packages, epubs, and print PDFs
- `publishing_output/covers/` — has final cover images
- `publishing_output/` — some books may have deliverables here but no package

**Step 2: Map books to series and folders**

Identify the series structure. Books from different series may exist across multiple directories. Match books to their series by examining content or filenames.

**Step 3: Create the target directories**

```bash
mkdir -p "books/Series_Name/Book_N_Title/"
```

**Step 4: Copy the 4 canonical files**

```bash
cp "$PACKAGES/Book_N_Title_Publishing_Package.zip"  "target/"
cp "$PACKAGES/Book_N_Title.epub"                    "target/"
cp "$PUB_OUT/Book_N_Title_Print.pdf"                "target/"
cp "$COVERS/SERIES_N_Title_Cover.png"               "target/"
```

**Pitfall — source file names may not match exactly.** Check the actual filenames in the source directories before hardcoding. See `references/filename-mismatch-patterns.md` for the full mapping of every book's package-zip vs epub vs print-pdf vs cover naming conventions across all series.

**Pitfall — archive script accidentally moves the canonical files (keep-file logic bug).** This happens when the keep-file list in a bash `case` block uses wrong variable names (e.g., `KEEP_ZIP` resolves to a Book_1 filename while processing Book_2). The safest algorithm to avoid this:

```bash
# SAFE pattern: 1) move EVERYTHING to .archived, 2) copy keepers back
mkdir -p "$DIR/.archived"
for item in "$DIR"/*; do
    [ "$(basename "$item")" = ".archived" ] && continue
    mv "$item" "$DIR/.archived/"
done
# Then copy the canonical files into $DIR
cp "$ZIP_SRC" "$DIR/"
cp "$EPUB_SRC" "$DIR/"
cp "$PDF_SRC" "$DIR/"
cp "$COVER_SRC" "$DIR/"
```

This eliminates the variable-name mismatch problem entirely. Compare-only approaches (looping with `[ "$base" = "$KEEP_ZIP" ] && continue`) are fragile because typos in the variable name silently archive everything.

**Pitfall — Waters Horizon has no publishing zip and no cover.** Book 4 of The Lunar Foundation was never packaged. When delivering, note this gap explicitly. The user will need to either generate the cover (see `book-cover-design` skill) and/or build a KDP package (see `manuscript-publishing-package` skill).

**Step 5: Archive remaining old artifacts**

After placing the 4 canonical files, move all other files (build scripts, old-name artifacts, planning docs, duplicate intermediate builds) into `.archived/` subdirectory. Follow the keep/archive rules in Step 7.

### 6b.5. Reporting

After organizing, present a compact summary showing each book's 4 files:

```
Book I - Built from Dust
  ZIP:  5.0M  No_Blue_Sky_1_Built_from_Dust_Publishing_Package.zip
  EPUB: 2.6M  No_Blue_Sky_1_Built_from_Dust.epub
  PDF:  511K  No_Blue_Sky_1_Built_from_Dust_Print_Ready.pdf
  COVER:1.8M  NBS_1_Built_from_Dust_Cover.png
```

If any book is missing one of the 4 canonical files, note it clearly. The user can then decide to generate the missing item.

### 6b.6. Post-Discovery Duplicate Cleanup

After identifying all books and their canonical series directories, check for duplicate/orphan directories that need cleanup.

**What to look for:**

1. **Same book under multiple directory names** — e.g., `MIFECO_Bussiness_Series/` (typo) vs `Business_Series/`. Check for near-miss directory names with typos, different casing, or missing/extra words.

2. **Root-level book directories that should be inside a series** — e.g., `Owners_Manual_AI_Agents/` at `/home/bob/books/` root when it should be inside `Business_Series/`. These are leftovers from before the series structure was established.

3. **Series directories with inconsistent naming** — e.g., `The_Lunar_Foundation/` instead of `Lunar_Foundation_Series/`. Rename to match the convention (drop "The", add "_Series").

4. **Typos in standalone book directory names** — e.g., `Tommrow_Remembered/` → `Tomorrow_Remembered/`. These sit at the books root, not inside a series.

5. **Old centralized output directories** — `publishing_output/` with packages, covers, and PDFs that are now superseded by per-book deliverables. These can be archived.

6. **Scattered `.archived/` directories inside individual book folders** — Each book may have its own `.archived/` subdirectory with old build artifacts. Consolidate these into a single location rather than leaving them scattered.

**Cleanup steps:**

#### Step A: Rename misnamed directories

Before merging duplicates, fix directory names that don't match the convention:

```bash
# Fix series naming: drop "The" prefix, add "_Series" suffix
mv /home/bob/books/The_Lunar_Foundation /home/bob/books/Lunar_Foundation_Series

# Fix typo'd standalone book names
mv /home/bob/books/Tommrow_Remembered /home/bob/books/Tomorrow_Remembered

# Fix typo'd series names
mv /home/bob/books/MIFECO_Bussiness_Series /home/bob/books/MIFECO_Business_Series  # but merge/archive after
```

#### Step B: Detect duplicates

```bash
# List all directories at books root
ls -d /home/bob/books/*/

# For each duplicate, check if it's a subset of a canonical series dir
diff -rq /home/bob/books/Duplicate/ /home/bob/books/Canonical/ 2>/dev/null
```

#### Step C: Timestamp-aware merge

⚠️ **CRITICAL: Don't just `cp -n`.** The canonical directory may have *newer outputs* while the duplicate has *newer source files* (or vice versa). Compare modification times per file type:

```bash
# For source files (.md, .py, .html): check if canonical already has them
# If canonical is missing them entirely, copy from duplicate
# If both have them, compare timestamps and keep the newest

# SAFE pattern: copy each source file with timestamp check
for src in /home/bob/books/Duplicate/*.md /home/bob/books/Duplicate/*.py /home/bob/books/Duplicate/*.html; do
    f=$(basename "$src")
    dst="/home/bob/books/Canonical/$f"
    if [ ! -f "$dst" ]; then
        cp "$src" "$dst"
        echo "COPIED (new): $f"
    elif [ "$src" -nt "$dst" ]; then
        cp "$src" "$dst"
        echo "UPDATED (newer): $f"
    else
        echo "SKIPPED (older or same): $f"
    fi
done

# For output files (.epub, .pdf, .zip, .png): same timestamp check
# Prefer the file in the canonical location if newer, otherwise copy from duplicate
for ext in epub pdf zip png jpg; do
    for src in /home/bob/books/Duplicate/*."$ext"; do
        [ -f "$src" ] || continue
        f=$(basename "$src")
        dst="/home/bob/books/Canonical/$f"
        if [ ! -f "$dst" ] || [ "$src" -nt "$dst" ]; then
            cp "$src" "$dst"
            echo "COPIED output: $f"
        fi
    done
done

# Copy entire subdirectories that don't exist in canonical
for subdir in output Owners_Manual_AI_Agents_KDP_PACKAGE generated_images; do
    [ -d "/home/bob/books/Duplicate/$subdir" ] && \
        [ ! -d "/home/bob/books/Canonical/$subdir" ] && \
        cp -r "/home/bob/books/Duplicate/$subdir" "/home/bob/books/Canonical/"
done
```

This avoids overwriting newer deliverables with older ones while still pulling in source files that were missing.

#### Step D: Archive the duplicate — consolidated, not scattered

❗ **Do NOT create a new `_archived_YYYYMMDD_HHMMSS/` each time.** Instead, consolidate into a single `_archived/` directory with named subdirectories:

```bash
# Create the consolidated archive root if it doesn't exist
mkdir -p /home/bob/books/_archived

# Move the duplicate into a named subdirectory
mv /home/bob/books/Duplicate /home/bob/books/_archived/Duplicate

# Add old orphan directories to the same _archived/ location
mv /home/bob/books/publishing_output /home/bob/books/_archived/publishing_output
mv /home/bob/books/_archived_20260504_184630 /home/bob/books/_archived/backup_2026-05-04_old
```

This keeps the books root clean — a single `_archived/` directory instead of a dozen timestamped ones.

#### Step E: Consolidate scattered `.archived/` dirs from inside books

Many book folders have a `.archived/` subdirectory with old build scripts, old-name artifacts, and intermediate builds. These should be moved to the central `_archived/book_backups/`:

```bash
mkdir -p /home/bob/books/_archived/book_backups

for d in $(find /home/bob/books/Series/Book_N_Title -type d -name '.archived' 2>/dev/null); do
    book=$(basename "$(dirname "$d")")
    series=$(basename "$(dirname "$(dirname "$d")")")
    target="/home/bob/books/_archived/book_backups/${series}__${book}"
    mv "$d" "$target"
    echo "Consolidated: $d -> $target"
done
```

#### Step F: Clean up `__pycache__` dirs

```bash
find /home/bob/books/ -type d -name '__pycache__' -exec rm -rf {} + 2>/dev/null
```

**Key principle:** Move, don't delete. But consolidate into a single `_archived/` umbrella with named subdirectories, not scattered timestamped `_archived_*` dirs.

**Common duplicate patterns found in this workspace:**

| Duplicate | Canonical | Issue |
|-----------|-----------|-------|
| `MIFECO_Bussiness_Series/` | `Business_Series/` | Typo ("Bussiness") |
| `Owners_Manual_AI_Agents/` (root) | `Business_Series/Owners_Manual_AI_Agents/` | Pre-series root orphan |
| `The_Lunar_Foundation/` | `Lunar_Foundation_Series/` | Missing "_Series" suffix, has "The" prefix |
| `publishing_output/` | (per-book dirs) | Superseded centralized output |

See `references/duplicate-directory-patterns.md` for the full mapping of every known duplicate in this workspace.

### 6b.7. Common Problems and Resolutions

| Problem | Resolution |
|---------|------------|
| No .zip package for a book | Book may be in progress; deliver what exists |
| No cover image for a book | Search publishing_output/covers/, backups, generated_images/. If not found anywhere, report it |
| Duplicate file names (old vs new version) | Keep the one with the newest timestamp; archive the other |
| Book exists in both old branding and new branding directories | Check internal HTML `<title>` tags to identify which is which |
| Archive script accidentally moves the canonical files too | Happens when keep-file list has a typo or case statement uses wrong variables. Always verify after the first run and fix before proceeding |

## Step 7: Post-Delivery Archival Cleanup

After delivering the latest files, you may be asked to **archive** old/stale/pre-rebrand artifacts from the book's working directory. This solves the problem of accumulated debris: build scripts, generated images, planning docs, old-name cover files, and intermediate builds that clutter the workspace.

### 7.1. When to Use

- User says "clean up my book folders", "archive old versions", "remove previous versions before rebranding"
- After a rebranding (old-title files, packages, and covers litter the directory)
- After multiple build iterations (build scripts v1–v7 accumulate)
- User says "keep only the latest" or "make this folder production-clean"

### 7.2. What to Keep vs Archive

**KEEP (latest deliverables):**
- `output/{BOOK_KEY}.html` — latest HTML build
- `output/{BOOK_KEY}.pdf` — latest PDF
- `output/{BOOK_KEY}.epub` — latest EPUB
- `output/{BOOK_KEY}_Final.md` — latest source manuscript
- `output/{BOOK_KEY}_KDP_PACKAGE/` — latest KDP package directory (all files inside)
- `output/{BOOK_KEY}_KDP_PACKAGE.zip` — packaged KDP zip
- Source cover image (`{BOOK_KEY}_Cover.png` or similar)
- Generated KDP cover files (e.g., in `generated_images/` if they end with `_KDP_Cover` or `_KDP_Kindle_Cover`)
- Latest build scripts (e.g., `build_kdp_package.py`, latest version of build scripts)
- Any `{BOOK_KEY}_Print_Ready.pdf` or `{BOOK_KEY}_Print.html` needed for print

**ARCHIVE (everything else):**
- **Old-title packages:** Entire directories of old-name final packages (e.g., `OLD_TITLE_FINAL_PACKAGE/`)
- **Old-title ZIPs:** `OLD_TITLE_FINAL_PACKAGE.zip` sitting in the root books directory
- **Build scripts:** All past iteration build scripts (`build_final.py`, `build_final_v2.py`, `build_correct.py`, `build_rebrand.py` etc.) — keep only the latest
- **Generated images:** Chapter images, AI-generated cover variants, prompt files, JSON metadata — keep only final KDP covers
- **Chapter source files:** Individual chapter `.md` files if a compiled manuscript already exists
- **Planning/status docs:** `CONTEXT.md`, `PROJECT_CONTROL_SHEET.md`, `PUBLISHING_SCORECARD.md`, `CAREER_TIMELINE.md`, `market-research.md`, status files
- **Root duplicates:** EPUB/PDF copies of the book in the root directory (the ones in `output/` are authoritative)
- **Empty dirs:** Remove `__pycache__/`, empty directories
- **Old-name cover files:** Cover PNGs, wrap covers, back covers using old title
- **Marketing docs in root:** `KDP_AI_DISCLOSURE.md`, `MARKETING_COPY.md` if duplicated in the KDP package
- **Test files, sketches:** Placeholder sketch images, test scripts, test output files
- **Old compiled docs:** `Compiled.md`, `MIFECO_PLAYBOOK_COMPLETE.md` etc.
- **Generated chart images:** Chart PNGs (re-generatable from data)

### 7.3. Execution Pattern

Create a timestamped archive directory and move, don't delete:

```bash
ARCHIVE_DIR="/home/bob/books/_archived_$(date +%Y%m%d_%H%M%S)"
```

**Step A: Inventory the book directory** — walk all files, categorize them by whether they belong to the "keep" or "archive" list above.

**Step B: Move to archive** — for each file to archive, preserve its relative path inside the archive. For entire subdirectories (like `OLD_TITLE_FINAL_PACKAGE/`), move the whole directory.

**Step C: Check for strays outside the book directory** — search for files with the old title name in sibling directories and the parent books directory:
```bash
find /home/bob/books -maxdepth 4 \
  \( -name "*OLD_TITLE*" -o -name "*OLD_PACKAGE*" \) \
  -not -path "*/_archived_*" \
  -not -path "*/BOOK_DIR/*" \
  | sort
```
Common strays: `MIFECO_AI_Playbook_Final_Package/` (outside `MIFECO_AI_Playbook/`), `.zips` in the parent books dir.

**Step D: Remove empty dirs** — `rmdir` any vacated directories.

### 7.4. Common Stray Locations

These are easily missed because they sit OUTSIDE the book's own directory:
- `/home/bob/books/{OLD_NAME}_FINAL_PACKAGE/` — old package directory at the books root level
- `/home/bob/books/{OLD_NAME}_FINAL_PACKAGE.zip` — old zipped package
- `/home/bob/books/{OLD_NAME}_Cover.png` — old cover in books root
- Empty sibling directories that were never populated or became obsolete

### 7.5. What NOT to Touch

- **Other books** — if the user says "clean up these 2 books," leave the other 7+ books completely alone
- **`archived-versions/`** — pre-existing archive of tarballs (already consolidated)
- **Source cache** — `.hermes/cache/documents/` contains original uploaded source manuscripts; leave these unless the user explicitly asks
- **Cross-book references** — a chapter file in another book that references the old title (e.g., `Third_Generation/.../Chapter_40_The_Unwritten_Future.md`) is part of that book's source material, not a stray artifact of THIS book

### 7.6. Reporting

After archiving, always show a summary grouped by book:
- Total files archived per book
- Archive size
- Categories of what was archived (old-name packages, build scripts, generated images, planning docs, etc.)
- What was kept

### 7.7. Edge Cases

- **Multiple build scripts with same name but different versions**: Archive all except the latest/modified most recently
- **Large files archived from root**: Sometimes root EPUB/PDF duplicates can be 23+ MB (old builds with embedded images) while the `output/` versions are 1.5-2.2 MB. The root versions need archiving too
- **Old-name KDP packages nested inside a book with a different modern name**: The whole package directory should go to archive, not just loose files

## Overlap Note

This archival cleanup workflow overlaps partially with `book-identity-rebranding` — that skill covers the *rename* phase, while this covers the *cleanup after the rename*. If both are triggered in the same session, run rebranding first, then cleanup. The skills could potentially be consolidated into a single "book lifecycle management" skill, but the current separation (rename vs deliver+cleanup) keeps each at a manageable scope.

## References

- `references/bulk-publish-update.md` — Bulk publish status update pattern
- `references/filename-mismatch-patterns.md` — File naming conventions per book
- `references/duplicate-directory-patterns.md` — Known duplicate directories
