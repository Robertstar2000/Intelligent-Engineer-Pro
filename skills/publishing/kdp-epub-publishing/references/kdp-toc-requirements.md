# KDP TOC/Navigation Requirements

## Two Required TOC Structures

### 1. Logical TOC (invisible, powers "Go To" menu)

**nav.xhtml** (EPUB 3):
```xml
<nav epub:type="toc" id="toc">
  <h2>Table of Contents</h2>
  <ol>
    <li><a href="chapter_1.xhtml">Chapter 1: Title</a></li>
    ...
  </ol>
</nav>
<nav epub:type="landmarks" id="landmarks">
  <ol>
    <li><a epub:type="toc" href="nav.xhtml">Table of Contents</a></li>
  </ol>
</nav>
```
- Must be declared in OPF manifest with `properties="nav"`
- Can double as HTML TOC if placed in spine

**toc.ncx** (EPUB 2, backward compat):
```xml
<navMap>
  <navPoint playOrder="0" id="np-0">
    <navLabel><text>Chapter 1: Title</text></navLabel>
    <content src="chapter_1.xhtml"/>
  </navPoint>
  ...
</navMap>
```
- Must have sequential `playOrder` attributes (REQUIRED by Kindle)
- Must be connected via `<spine toc="ncx">` in OPF

### 2. HTML TOC (visible page)
- Must appear near the BEGINNING of the book, before chapter 1
- Each entry must be a clickable link
- Chapter headings must have `id` attributes matching TOC anchors
- No page numbers

## Common KDP Error Codes

| Code | Meaning | Fix |
|------|---------|-----|
| OPF-055 | toc.ncx missing from manifest | Add NCX item to OPF |
| NAV-001 | nav missing epub:type="toc" | Add attribute |
| NCX-002 | NCX has no navPoint entries | Add navPoints with playOrder |

## Key Pitfall: Image Generation Unavailable

The `image_generate` tool requires FAL_API_KEY or Nous Portal credits. If unavailable, the user must:
1. Provide a FAL API key (free at fal.ai), OR
2. Generate images externally and provide them, OR
3. Add credits to Nous Portal

Do not attempt image generation without confirming the tool works first.
