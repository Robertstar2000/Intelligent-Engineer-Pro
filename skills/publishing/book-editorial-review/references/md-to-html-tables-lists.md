# md_to_html_simple() Table and List Support

## What It Does

The `md_to_html_simple()` function in `hermes_publish/utils.py` converts basic markdown to HTML. As of 2026-06-18, it supports:

- Headings (`#`, `##`, `###`)
- Paragraphs with bold (`**bold**`) and italic (`*italic*`)
- Images (`![alt](path)` → `<img>`)
- Scene breaks (`---`, `***`)
- **Unordered lists** (`- item`, `* item`, `+ item` → `<ul><li>`)
- **Ordered lists** (`1. item`, `2. item` → `<ol><li>`)
- **Markdown tables** (pipe-delimited with separator row → `<table><thead><tbody>`)

## Table Detection Rules

A markdown table is detected when:
1. A line contains `|` characters (cells)
2. The NEXT line matches `|---|---|` or `|:---|---|` (separator with dashes)

The first row becomes `<thead><th>`, subsequent rows become `<tbody><td>`.

**Example input:**
```markdown
| Quarter | Focus Area 1 | Focus Area 2 |
|---------|-------------|-------------|
| Q1 | [Quick Win] ____________ | [Foundation] ____________ |
| Q2 | [Quick Win 3] ____________ | [Optimization] ____________ |
```

**Output:** Proper HTML table with borders, padding, and 9pt font.

## List Detection Rules

- Lines starting with `- `, `* `, or `+ ` → unordered list items (`<ul><li>`)
- Lines starting with `1. `, `2. `, etc. → ordered list items (`<ol><li>`)
- Consecutive list items are grouped into a single list
- A non-list line closes any open list

**Important:** Checkbox syntax `- [ ] item` works — the `[ ]` is preserved in the `<li>` text.

## When to Use Tables vs Lists in Manuscripts

| Content Type | Format | Example |
|---|---|---|
| Timeline grids | Markdown table | Quarterly implementation plans |
| Comparison charts | Markdown table | Feature comparisons |
| Do/Don't lists | Markdown bullet list | Best practices, pitfalls |
| Exercise checklists | Markdown bullet list with `- [ ]` | Priority rankings |
| Fill-in-the-blank forms | Separate lines with `<br/>` | Assessment forms |

## Pitfalls

1. **Inline text with brackets/underscores is NOT a table** — `Quarter 1: [Item] ____ [Item] ____` renders as a broken paragraph. Always use `|` pipe syntax.

2. **Tables need blank lines around them** — A blank line before and after the table block ensures proper detection.

3. **List items need consistent prefixes** — Mixing `-` and `*` in the same list works, but switching to plain text breaks the list.

4. **`<br/>` in form fields** — Use `<br/>` between a bold label and its underline to prevent WeasyPrint from wrapping the underline to the next line mid-label.
