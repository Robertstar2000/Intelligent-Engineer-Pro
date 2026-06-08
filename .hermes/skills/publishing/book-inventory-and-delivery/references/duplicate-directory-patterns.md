# Duplicate Directory Patterns — Book Workspace Cleanup

When scanning `/home/bob/books/` for book projects, several directories may
contain the same book under different names or locations. This reference
documents all known duplicates so future agents can identify and merge them.

## Resolved Duplicates (May 2026)

All known duplicates from the initial workspace audit have been resolved.
The table below documents what was found and what action was taken, so future
agents don't waste time re-investigating.

| Duplicate Path | Canonical Path | Issue | Resolution |
|----------------|---------------|-------|------------|
| `/home/bob/books/MIFECO_Bussiness_Series/` | `/home/bob/books/Business_Series/` | Typo: "Bussiness" → "Business" | Source files merged into `Business_Series/Owners_Manual_AI_Agents/` (40 chapters, manuscript, build scripts). Duplicate archived to `_archived/`. |
| `/home/bob/books/Owners_Manual_AI_Agents/` (root) | `/home/bob/books/Business_Series/Owners_Manual_AI_Agents/` | Pre-series root orphan | Output files were identical timestamps to canonical. Duplicate removed (no unique content). |
| `/home/bob/books/The_Lunar_Foundation/` | `/home/bob/books/Lunar_Foundation_Series/` | Missing "_Series" suffix, has "The" prefix | Renamed via `mv`. All 4 books (Book_1–Book_4) intact. |
| `/home/bob/books/Tommrow_Remembered/` | `/home/bob/books/Tomorrow_Remembered/` | Typo: "Tommrow" → "Tomorrow" | Renamed via `mv`. Loose files consolidated into book dir + `_resources/`. |
| `/home/bob/books/publishing_output/` | (per-book directories) | Superseded centralized output | Archived to `_archived/publishing_output/`. All deliverables now live in per-book dirs. |
| `/home/bob/books/_archived_20260504_184630/` | `_archived/backup_2026-05-04_old/` | Scattered timestamped archive | Consolidated into single `_archived/` umbrella. |
| `/home/bob/books/_archived_20260507_123632/` | `_archived/backup_2026-05-07_old/` | Scattered timestamped archive | Consolidated into single `_archived/` umbrella. |
| `/home/bob/books/mifeco-rebuild/` | `_archived/mifeco-website-rebuild/` | Non-book project in books dir | Archived to `_archived/`. |
| `.archived/` inside individual book dirs (7 total) | `_archived/book_backups/` | Scattered inside books | Consolidated into `_archived/book_backups/` with naming `Series__Book`. |

## Current State (Post-Cleanup)

```
/home/bob/books/
├── Business_Series/               ← canonical
├── Lunar_Foundation_Series/       ← canonical (renamed)
├── No_Blue_Sky_Series/            ← canonical
├── Tomorrow_Remembered/           ← canonical (renamed)
└── _archived/                     ← single consolidated archive
    ├── publishing_output/
    ├── backup_2026-05-04_old/
    ├── backup_2026-05-07_old/
    ├── mifeco-website-rebuild/
    └── book_backups/              ← old .archived dirs from inside books
```

## Detection Script

To find potential duplicates in the future:

```bash
# List all directories at books root
ls -d /home/bob/books/*/

# Check for near-miss names (typos, different casing)
find /home/bob/books/ -maxdepth 1 -type d | sort | \
  while read dir; do
    base=$(basename "$dir")
    # Skip _archived, __pycache__, publishing_output
    [[ "$base" == _* ]] && continue
    echo "$base"
  done

# Check for books that exist in multiple locations
for book in "Owners_Manual_AI_Agents" "AI_That_Works"; do
  echo "=== $book ==="
  find /home/bob/books/ -maxdepth 3 -type d -name "*${book}*" 2>/dev/null
done
```

## Merge Strategy

When a duplicate contains source files not present in the canonical location:

1. **Compare timestamps** — don't just `cp -n`. The canonical may have newer outputs while the duplicate has newer source files. Check per file type.
2. **Copy source files** (`.md`, `.py`, `.html`) from duplicate to canonical if missing or newer
3. **Copy output files** (`.epub`, `.pdf`, `.zip`, `.png`) from duplicate to canonical if missing or newer
4. **Archive the duplicate** — move to `_archived/<name>/` (not a new timestamped dir)
5. **Update memory** if the canonical path changed

## Common Patterns to Watch For

| Pattern | Example | Action |
|---------|---------|--------|
| Typo in series name | `MIFECO_Bussiness_Series` | Merge into correctly-named canonical, archive typo'd dir |
| Typo in standalone book name | `Tommrow_Remembered` | Rename directory, consolidate loose files |
| Missing "_Series" suffix | `The_Lunar_Foundation` | Rename to `Lunar_Foundation_Series` |
| Root-level book that belongs in a series | `Owners_Manual_AI_Agents/` at root | Move into `Business_Series/` |
| Scattered `.archived/` inside books | `Book_I/.archived/` | Consolidate into `_archived/book_backups/` |
| Scattered `_archived_*` timestamp dirs | `_archived_20260504_184630/` | Consolidate into single `_archived/` with named subdirs |