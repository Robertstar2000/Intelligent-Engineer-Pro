# KDP Navigation Requirements (from Amazon KDP docs)

Source: Amazon KDP Help Pages — visited during 2026-02-22 session

## Three Required Navigation Structures

KDP requires ALL three of these in every EPUB:

### 1. Logical TOC (invisible, powers "Go To" menu)
- **toc.ncx** file with `<navPoint playOrder="N">` entries
- Connected from `<spine toc="ncx">` in OPF
- Must follow book order (ch01 before ch02)
- Every navPoint MUST have sequential `playOrder` starting from 1
- dtb:uid must exactly match dc:identifier in OPF
- Kindle supports 2 levels of nesting max

### 2. HTML TOC (visible page in book)
- Must be placed BEFORE chapter 1 (not at the end)
- Each entry must be a clickable `<a href="">` link
- Do NOT use `<table>` tags for layout
- Do NOT use page numbers
- If importing from Word, use Heading styles and Word's TOC feature
- For bundled editions: overarching TOC at the beginning

### 3. Landmarks nav (EPUB 3)
```xml
<nav epub:type="landmarks">
  <ol>
    <li><a epub:type="toc" href="toc.xhtml">Table of Contents</a></li>
    <li><a epub:type="cover" href="cover.xhtml">Cover</a></li>
  </ol>
</nav>
```

## NCX Specification

```xml
<navMap>
  <navPoint class="titlepage" id="L1T" playOrder="1">
    <navLabel><text>AUTHOR'S NOTE</text></navLabel>
    <content src="body.html#preface_1"/>
  </navPoint>
  <navPoint class="book" id="level1-book1" playOrder="2">
    <navLabel><text>PART ONE</text></navLabel>
    <content src="body.html#part_1"/>
    <navPoint class="chapter" id="level2-book1chap01" playOrder="3">
      <navLabel><text>THE HOUSES, 1969</text></navLabel>
      <content src="body.html#chapter_1"/>
    </navPoint>
  </navPoint>
</navMap>
```

## OPF Declaration for NCX

In manifest:
```xml
<item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>
```

In spine:
```xml
<spine toc="ncx">
```

## Guide Items (REQUIRED)

```xml
<guide>
  <reference type="cover" title="Cover" href="cover.xhtml"/>
  <reference type="toc" title="Table of Contents" href="toc.html"/>
</guide>
```

## Common KDP Rejection Messages

| Error | Cause | Fix |
|-------|-------|-----|
| "Missing Table of Contents" | NCX missing or not in spine | Add NCX with playOrder |
| "TOC links don't resolve" | NCX navPoints lack playOrder | Add sequential playOrder |
| "Invalid EPUB" | guide items missing | Add `<guide>` with cover and toc |
| "Unable to process" | mimetype compressed or not first | Rebuild with mimetype first, uncompressed |
| Cover not detected | Missing cover-image property | Add `properties="cover-image"` + meta tag |
| Navigation not working | NCX dtb:uid mismatch | Make dtb:uid match dc:identifier exactly |
