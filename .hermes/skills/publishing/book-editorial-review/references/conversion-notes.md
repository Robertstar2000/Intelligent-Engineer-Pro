# DOCX to Markdown Conversion Notes

## Process
1. Use `python-docx` to extract paragraphs with style information
2. Map Word styles to markdown: Heading 1 → `#`, Heading 2 → `##`, Heading 3 → `###`
3. Skip TOC entries (lines matching `text\tpage_number` pattern)
4. Handle bold/italic runs within paragraphs
5. Process tables as markdown tables

## Post-Conversion Checklist
- [ ] Remove duplicate title heading at start (if PDF template generates title page)
- [ ] Fix image paths (remove `images/` prefix for WeasyPrint compatibility)
- [ ] Insert chapter image references if images exist but aren't in manuscript
- [ ] Add "About the Author" section if missing
- [ ] Wrap image references in HTML for WeasyPrint: `![alt](path)` → `<img src="path" alt="alt" />`
- [ ] Ensure `md_to_html_simple()` converts markdown images to HTML `<img>` tags

## Common Issues
- **Images not rendering**: WeasyPrint doesn't process markdown syntax. Must convert to HTML first
- **Duplicate title page**: Strip manuscript's `# Title` when PDF template generates one
- **Wrong page size**: Must use 6×9 for business, never 8.5×11
- **Duplicate toc.ncx**: Both EPUB 3 (nav.xhtml) and EPUB 2 (toc.ncx) should be present for KDP
