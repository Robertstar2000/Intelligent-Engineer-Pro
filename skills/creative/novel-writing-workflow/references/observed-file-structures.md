# Observed File Structure for Book Projects

Based on session observations of the "Tomorrow Remembered" book project:

## Standard Book Project Structure
```
/home/bob/books/[Book_Title]/
├── book-sources/
│   └── [Book_Title]/
│       ├── Chapter_01_[Title].md
│       ├── Chapter_02_[Title].md
│       └── ... (continuing through all chapters)
├── COMPILED_MANUSCRIPT.md (optional, for publishing preparation)
├── manuscript/ (alternative location for compiled manuscript)
│   └── COMPILED_MANUSCRIPT.md
├── output/ (alternative location for compiled manuscript)
│   └── COMPILED_MANUSCRIPT.md
└── [Other project files like SPECIFICATION.md, character docs, etc.]
```

## Chapter File Naming Convention
- Format: `Chapter_XX_[Title].md` where XX is the zero-padded chapter number
- Example: `Chapter_01_The_Beginning.md`, `Chapter_64_Final_Resolution.md`
- Chapter titles should be descriptive and consistent

## Header Format Within Chapter Files
- Use markdown header: `## Chapter XX — [Chapter Title]`
- Followed by required elements:
  - *Mission AI: "[Relevant dialogue reflecting chapter theme]"*
  - *[Character Name]: "[Relevant quote reflecting chapter theme]"*
- Then the main narrative content

## Compiled Manuscript Format
When compiling chapters for publishing:
1. Title page with book title and subtitle
2. Horizontal rule (---) 
3. Chapters in numerical order with consistent formatting:
   - `## Chapter XX` header
   - Original chapter content preserved exactly
   - Horizontal rule (---) between chapters
4. No duplicate chapter headings or filename-slug headings

## File Management Best Practices
- Save each chapter as individual markdown file in book-sources directory
- Use clear, descriptive chapter titles
- Maintain consistent header formatting
- Periodically consolidate chapters into master document for review
- For publishing preparation, compile all chapters into a single manuscript

## Tools Used
- `read_file`: To consult specification and reference materials
- `write_file`: To create individual chapter files
- `execute_code`: To run consolidation scripts (optional)
- `session_search`: To reference previous chapters or writing decisions when needed