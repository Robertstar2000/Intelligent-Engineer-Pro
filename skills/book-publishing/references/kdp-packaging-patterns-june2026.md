# KDP Package Build, Cleanup & Maintenance (June 2026)

## Problem
KDP zips accumulate with inconsistent naming (PascalCase, kebab-case, legacy prefixes, archived copies), inflating count 2-3x. Per-book KDP_PACKAGE/ directories and zips scatter across 20 book directories, creating duplicates of the central archive.

## Canonical Structure
`KDP_Packages/PascalName/` — one directory per book, containing:
- `PascalName_KDP_PACKAGE.zip` — full KDP submission zip
- `PascalName.epub` — Kindle-compatible EPUB3
- `Author_Bio.txt` — Author biography
- `Author_Photo.jpg` — Author photo
- `Back_Cover.txt` — Back cover blurb
- `Cover.jpg` or `Cover.png` — Book cover
- `Description.txt` — KDP listing description
- `Infographic.png` — (business books) promotional graphic
- `Keywords.txt` — 7 KDP search keyword phrases
- `Title.txt` — Structured title/subtitle/series

## Naming Convention
- Title_Case (PascalCase) = canonical — `KDP_Packages/Affidavits_and_Alibis/`
- kebab-case = duplicate — `KDP_Packages/affidavits-and-alibis/` — DELETE these
- Per-book copies = redundant — `Book_1_Moon_Rock/KDP_PACKAGE/` — DELETE these

Check naming with:
```bash
ls -d KDP_Packages/*/ | while read d; do
  name=$(basename "$d")
  if [[ "$name" =~ ^[A-Z] ]]; then echo "KEEP: $name"; else echo "DELETE: $name"; fi
done
```

## Full Cleanup Procedure

### Step 1: Verify Central Archive Completeness
Before any removal, verify the canonical archive has everything:
```bash
for d in KDP_Packages/*/; do
  name=$(basename "$d")
  if [[ "$name" =~ ^[A-Z] ]]; then
    zip=$(find "$d" -name "*_KDP_PACKAGE.zip" | head -1)
    if [ -n "$zip" ]; then echo "✅ $name: has zip"; else echo "⚠️ $name: MISSING zip"; fi
  fi
done
```

### Step 2: Remove Duplicate kebab-case Directories
```bash
ls -d KDP_Packages/*/ | while read d; do
  name=$(basename "$d")
  if [[ "$name" =~ ^[a-z] ]]; then rm -rf "$d"; fi
done
```

### Step 3: Remove Per-Book KDP_PACKAGE Directories
```bash
find . -type d -name "KDP_PACKAGE" \
  -not -path "*/KDP_Packages/*" \
  -not -path "*/cindy-lou-series/*" \
  -not -path "*/_resources/*" | while read d; do rm -rf "$d"; done
```

### Step 4: Remove Per-Book Zip Files
```bash
find . -name "*KDP_PACKAGE.zip" \
  -not -path "*/KDP_Packages/*" \
  -not -path "*/cindy-lou-series/*" \
  -not -path "*/_resources/*" -delete
```

### Step 5: Clean Scattered Duplicates
cindy-lou-series/ often has KDP zips, KDP_PACKAGE dirs, KDP_AI_Disclosure files, and KDP cover JPEGs. These are legacy copies from a different directory structure. _resources/output/ contains old KDP_PACKAGE dirs from prior builds.

```bash
find ./Cindy_Lou_Legal_Capers/cindy-lou-series -name "*KDP*" -o -name "*kdp*" -delete
find ./Tomorrow_Remembered/_resources -name "*KDP*" -o -name "*kdp*" -delete 2>/dev/null
```

### Step 6: Final Verification
```bash
echo "Canonical packages: $(ls KDP_Packages/ | wc -l) books"
du -sh KDP_Packages/
echo "Leftover KDP artifacts: $(find . -name '*KDP_PACKAGE*' -not -path '*/KDP_Packages/*' | wc -l)"
```

Expected outcome: 20 Title_Case directories, ~232MB total, zero leftovers.

## Common Cleanup Signals

| Signal | What It Means | Action |
|--------|---------------|--------|
| 34 dirs in KDP_Packages/ | Both naming conventions present | Remove 14 kebab-case dirs |
| KDP_PACKAGE/ in book dirs | Per-book copies redundant with central | Remove all 20 |
| *KDP_PACKAGE.zip in book dirs | Per-book zips redundant with central | Remove all ~21 |
| cindy-lou-series/*KDP* | Legacy duplicates from old structure | Remove fully |
| _resources/output/Tomorrow*KDP* | Old build artifacts | Remove fully |

## Book Dirs (20 books, June 2026)
Series dirs: No_Blue_Sky_Series/ (5), Age_of_Lightships_Series/ (4), Lunar_Foundation_Series/ (4), Business_Series/ (3), Cindy_Lou_Legal_Capers/ (3), Tomorrow_Remembered/ (1)

## Metadata Prefix Inconsistency
- NBS: PascalCase prefix | AoLS: kebab prefix | LF: PascalCase | Business: mixed | Cindy Lou: generic

## KDP_PACKAGE Subdirs ≠ Canonical
Per-book KDP_PACKAGE/ dirs are NOT the canonical package. Canonical = KDP_Packages/PascalName/.