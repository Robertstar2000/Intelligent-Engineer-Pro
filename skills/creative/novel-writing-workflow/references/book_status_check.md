# Checking Book Project Status

When checking the status of a book project, if the `book_source` directory appears empty, check the `output` directory for compiled manuscripts (e.g., EPUB, PDF) to confirm the book has been published and is in the promotion phase.

Example structure:
```
/home/bob/books/[Book_Title]/
├── book_source/          # Should contain chapter markdown files
├── output/               # Contains compiled manuscripts (EPUB, PDF, etc.)
└── ...                   # Other resources (covers, marketing materials)

If `book_source` is empty but `output` contains a manuscript, the book is likely published.