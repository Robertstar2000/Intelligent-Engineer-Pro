# User Profile: Bob J Mills

Used by the editorial review skill to adapt voice, genre benchmarks, and workflow to the author's preferences.

## Identity & Work
- **Name:** Bob J Mills
- **Company:** Founder/operator of MIFECO (logistics platform — thousands of shipments/month, conveyor sensors, warehouse tracking, carrier invoices)
- **Role:** Author, publisher, business operator
- **Platform:** Communicates via Telegram

## Book Catalog (19 books across 6 series/genres)

| Series | Genre | Volumes | Status |
|--------|-------|---------|--------|
| Age of Lightships | Space opera | 4 | Legacy/out-of-print |
| No Blue Sky | Martian colonization epic | 5 | Active/in-print |
| Lunar Foundation | Sci-fi colonization thriller | 4 | Active/in-print |
| Cindy Lou Legal Capers | Cozy legal mystery (misclassified) | 3 | Draft/unpublished |
| Business Series | Business non-fiction | 4 | Active/in-print |
| Tomorrow Remembered | Memoir | 1 | Active/in-print |

## Editorial Workflow Preferences

1. **Iterative loop is mandatory:** Never stop after writing a review. If below A, fix the source files and re-review. Continue until A is achieved.
2. **Surgical fixes over full rewrites:** When possible, patch specific sections rather than rewriting entire manuscripts. Only rewrite when structural issues demand it.
3. **"Make assumptions, not opinions":** State findings as facts. Do not use "I think," "I recommend," "It seems," "Perhaps," "Maybe." Use specific chapter numbers and concrete alternatives.
4. **Humanized writing:** Reviews should sound like a professional editor's feedback, not a rubric. Use publishing-industry terminology naturally.
5. **Full books only:** Only full-length books get individual book-review.md files. Novellas, short stories, and serials within a series do not — unless explicitly requested.
6. **Series-level reviews must be split:** A consolidated series review should be distributed into per-book files, each getting its own book-review.md with a cross-book comparison section.
7. **Build pipeline awareness:** For business/non-fiction books, check build scripts (build_html.py, build_epub.py, build_package.py) for disclaimer language that can undercut authority.
8. **Stale review detection:** Always verify a book-review.md's claims against the actual manuscript before acting on them. Subagents may have updated the manuscript since the review was written.
9. **Do not trust filenames alone:** Verify file contents (read first ~30 lines) before using as compilation sources. _RW files may contain experimental alternate versions, not the expected content.
10. **Word count verification:** Use `wc -w MANUSCRIPT.md`, not file byte size (ls -l). The difference can be dramatic (39K bytes ≠ 39K words).