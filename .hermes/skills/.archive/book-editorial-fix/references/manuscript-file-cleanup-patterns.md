# Manuscript File Cleanup Patterns

## When to Use
After editorial review, before final publish. Run these checks to ensure the manuscript directory is clean and all files are consistent.

## EPUB Image Embedding Verification

The most common EPUB defect: chapter images exist in `chapter_images/` but are NOT embedded in the EPUB.

```bash
echo "Image files: $(ls chapter_images/ | wc -l)"
echo "Image refs in manuscript: $(grep -c 'chapter_images' MANUSCRIPT.md)"
unzip -l book.epub | grep -E '\.(png|jpg)$'
```

**If mismatch found:** Rebuild EPUB. The build script should embed all images from `chapter_images/`.

**Root cause:** EPUB was built from an older manuscript version or the build script only embedded a cover image.

## Title Change Propagation Checklist

When a book is renamed, verify ALL locations:

```bash
find KDP_PACKAGE/ -name "*OldTitle*" -type f
grep -r "OldTitle" _resources/ 2>/dev/null
grep -r "OldTitle" output/ 2>/dev/null
grep -r "OldTitle" README.md PLOT_MAP.md book-review.md 2>/dev/null
unzip -p book.epub OEBPS/content.opf | grep "OldTitle"
pdfinfo book.pdf | grep -i title
```

Delete all files with old title. Update README.md and metadata files.

## Duplicate Content Detection

```bash
diff MANUSCRIPT.md.backup MANUSCRIPT.md | head -100
grep -n "unique phrase" MANUSCRIPT.md
```

Common duplicate patterns: same job/career section in two chapters, same event in Ch3 and Ch5, science fair/first car/TV repair shop appearing multiple times.

Fix: Remove the duplicate with less detail. Keep the fuller version.

## Chapter Heading Restoration After Cleanup

```bash
grep -c "^## Chapter" MANUSCRIPT.md
grep -c "^- Chapter" MANUSCRIPT.md
```

These should match. If manuscript has fewer, a heading was accidentally deleted.

## Post-Cleanup Verification

```bash
wc -w MANUSCRIPT.md
grep -c "^## Chapter" MANUSCRIPT.md
unzip -l Tomorrow_Remembered_final.epub | grep -E '\.(png|jpg)$' | wc -l
pdfinfo Tomorrow_Remembered_final.pdf | grep Pages
grep -r "Tomorrow Is Still Open" . --include="*.md" --include="*.txt" 2>/dev/null | wc -l
# Should be 0
```
