# Manuscript Directory Patterns

## chapters_md Book Type — Directory Lookup Order

When `manuscript_type: "chapters_md"` is set in BOOK_REGISTRY, the pipeline
looks for chapter files in this order:

1. `book_dir/chapters/chNN.md` — preferred for condensed/rewritten books
2. `book_dir/manuscript_src/chNN.md` — legacy location for original manuscripts

This allows condensed books to sit alongside their original source files without
conflict. The `chapters/` directory is checked first.

## Other Manuscript Types

| Type | Source | Description |
|------|--------|-------------|
| `chapters_md` | `chapters/` or `manuscript_src/` | Individual .md chapter files |
| `chapters_xhtml` | `manuscript_src/` | Individual .xhtml chapter files |
| `manuscript_md` | `*MANUSCRIPT.md` in book_dir | Single compiled manuscript file |
| `single_md` | `*.md` in book_dir | One or more flat markdown files |

## BOOK_REGISTRY Config Pattern

The BOOK_REGISTRY in `/mnt/usb_4tb/books/hermes_publish/config.py` must point
`dir` to the parent of the `chapters/` directory. Example:

```python
"retainer-to-trouble": {
    "title": "Retainer to Trouble",
    ...
    "dir": BASE_DIR / "Cindy_Lou_Legal_Capers" / "cindy-lou-series" / "book-1-retainer-to-trouble",
    "manuscript_type": "chapters_md",
}
```

## Legacy Directory Structure

The old directories at `Cindy_Lou_Legal_Capers/book-N-*/` are LEGACY and should
not be used for pipeline operations. The `cindy-lou-series/book-N-*/` directories
contain the active condensed chapter files.
