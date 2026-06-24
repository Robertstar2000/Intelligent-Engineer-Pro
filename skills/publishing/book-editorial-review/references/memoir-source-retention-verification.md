# Memoir Source Retention Verification

## Purpose
Verify ALL original stories are retained in a memoir and no plot/storyline was changed during editing.

## Technique

### 1. Locate Sources
```bash
find /mnt/usb_4tb/books -name "MANUSCRIPT.md" -path "*BookName*"
find /mnt/usb_4tb/books -name "*.backup" -o -name "*.BEFORE_*" -o -name "*.bak" | grep -i bookname
ls /mnt/usb_4tb/books/_archived/book_backups/ | grep -i bookname
find /mnt/usb_4tb/books -name "PLOT_MAP.md" -path "*BookName*"
```

### 2. Word Count Comparison
```bash
wc -w MANUSCRIPT.md && wc -w MANUSCRIPT.md.backup
wc -l MANUSCRIPT.md && wc -l MANUSCRIPT.md.backup
```
Backup 2×+ larger = content loss during editing.

### 3. Plot Map Verification
For each scene in PLOT_MAP.md, grep MANUSCRIPT.md. Create checklist table.

### 4. Duplicate Content Detection
```bash
grep -n "same_topic" MANUSCRIPT.md | head -10  # Same story in multiple chapters?
grep -oP '^#+ Chapter.*' MANUSCRIPT.md | sort | uniq -d  # Duplicate titles?
diff MANUSCRIPT.md.backup MANUSCRIPT.md | head -50  # What was removed?
```

### 5. Rebranding Detection
```bash
grep -r "old title\|rebrand" /path/to/book/
ls /path/to/book/_resources/ | grep -i "package\|old\|original"
```

### 6. Output Verification
```bash
ls -la /path/to/book/*.pdf /path/to/book/*.epub
ls -la /path/to/book/KDP_PACKAGE/
```

## Common Patterns
- **Duplicate content**: Same story in multiple chapters (e.g., TV Repair Shop in Ch3 AND Ch5)
- **Backup larger**: Reflective content trimmed, reducing page count
- **Chapter renumbering**: TOC count ≠ header count
- **Title change**: Old title in `_resources/` directory names
- **Multiple outputs**: Different PDF/EPUB sizes indicate different build pipelines
