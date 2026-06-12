# Backup Restoration for Manuscripts

When books have lost content (truncated during front/back matter insertion, expansion scripts, or image generation), use this systematic workflow to inventory, snapshot, and restore from backup.

## Phase 1: Inventory

### Survey All Manuscripts + Backups

```bash
cd /mnt/usb_4tb/books

# All current MANUSCRIPT.md files with word counts
find . -name "MANUSCRIPT.md" -not -path "./_*" -not -path "*/_*" -not -path "*/KDP_PACKAGE/*" | while read f; do
  echo "$(wc -w < "$f")	$f"
done

# All backup files in book directories
find . \( -name "*.backup" -o -name "*.BEFORE_*" -o -name "*.bak" \) -not -path "./_*" | while read f; do
  echo "$(wc -w < "$f")	$f"
done
```

Also check centralized backup locations:
- `books/_archived/book_backups/` — series-level directories with HTML, EPUB, or .md backups
- `books/_archived/backup_2026-05-04_old/` — older chapter-level backups
- Books' own `_archived/` subdirectories — may contain `.bak` files

## Phase 2: Detect Content Loss

Compare current word count vs backup word count. A backup that is **significantly larger** means the book lost content:

| Current | Backup | Verdict |
|---------|--------|---------|
| 6,664 | 40,860 | ⚠️ LOST — restore |
| 17,207 | 62,621 | ⚠️ LOST — restore |
| 22,461 | 65,003 | ⚠️ LOST — restore |
| 8,172 | 104,134 | ⚠️ LOST — restore |
| Same ±5% | Same | Intact — skip |
| Current > Backup | Smaller | Expanded, not damaged — skip |

**Do NOT restore if current ≥ backup.** The backup is then a prior version that the author intentionally grew.

## Phase 3: Create Damaged Copies

```bash
DAMAGE_DIR="books/_archived/damaged_copies/$(date +%Y-%m-%d)"
mkdir -p "$DAMAGE_DIR"

find . -name "MANUSCRIPT.md" -not -path "./_*" -not -path "*/_*" | while read f; do
  safe_name=$(echo "$f" | sed 's|./||; s|/|__|g')
  cp "$f" "$DAMAGE_DIR/$safe_name"
  echo "Saved: $safe_name ($(wc -w < "$f") words)"
done
```

## Phase 4: Restoration Methods

### Direct Copy (fastest — backup is .md in same directory)

```bash
cp Book_X/MANUSCRIPT.md.backup Book_X/MANUSCRIPT.md
cp Book_X/MANUSCRIPT.md.BEFORE_FRONT_BACK Book_X/MANUSCRIPT.md
cp Book_X/_archived/manuscript.md.bak Book_X/MANUSCRIPT.md
```

### HTML → Markdown (use html2text, NOT regex)

Regex HTML stripping leaves `<p>`, `<span>`, and entity artifacts. Use `html2text`:

```bash
pip3 install html2text
```

```python
import html2text
h = html2text.HTML2Text()
h.body_width = 0
with open('book.html', 'r') as f:
    md = h.handle(f.read())
with open('MANUSCRIPT.md', 'w') as f:
    f.write(md)
```

**Verify no artifacts:** `grep -c '<[a-z]' MANUSCRIPT.md` should return 0.

### EPUB → Markdown

EPUBs are zipped HTML. Extract the HTML files and use html2text:

```python
import zipfile, re

with zipfile.ZipFile('book.epub') as z:
    html_files = sorted([f for f in z.namelist() if f.endswith(('.html', '.xhtml', '.htm'))])
    content_files = [f for f in html_files if 'toc' not in f.lower() and 'nav' not in f.lower()]
    all_text = '\n\n'.join(
        re.sub(r'<[^>]+>', ' ', z.read(h).decode('utf-8', errors='replace')) for h in content_files
    )
    with open('MANUSCRIPT.md', 'w') as f:
        f.write(all_text)
```

### From book_backups Archive

Check `books/_archived/book_backups/<Series>__<Book>/` for files. Common formats:
- `manuscript.md` — direct copy to `MANUSCRIPT.md`
- `No_Blue_Sky_X_Title.html` — extract with html2text
- `No_Blue_Sky_X_Title.epub` — extract with zipfile
- `Tomorrow_Remembered_Print_6x9.pdf` — harder to extract; prefer earlier formats

## Phase 5: Post-Restoration Verification

```bash
# Word count matches expected
wc -w Book_X/MANUSCRIPT.md

# No HTML artifacts remain
grep -c '<[a-z]' Book_X/MANUSCRIPT.md   # Must be 0

# Chapter images still exist (from prior generation)
ls Book_X/chapter_images/ | wc -l

# First chapter reads cleanly
head -20 Book_X/MANUSCRIPT.md
```

## Subtle Case: Identical Word Counts

`.BEFORE_FRONT_BACK` files having the same word count as the current MANUSCRIPT.md doesn't mean they're identical. The current version has front/back matter (copyright, TOC, acknowledgments, back-matter book list) that was ADDED to the same content. Restoring from `.BEFORE_FRONT_BACK` removes that structural content.

**Action:** If current ≥ backup in word count AND you know front/back matter was the only change, do NOT restore — the book only gained structure, didn't lose content.

## Timeout Recovery After Partial Restore

If a subagent restoring a book times out mid-operation:
1. Always check `wc -w` to see if content was added
2. Check `grep -c "^## Chapter\|^# Chapter"` for chapter count changes
3. Check `grep -c '<[a-z]'` for new HTML artifacts
4. If partial progress was made (word count increased), accept it and move on — don't retry the exact same task