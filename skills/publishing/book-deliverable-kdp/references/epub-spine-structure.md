# EPUB 3 Spine Structure — What Goes Where

This reference documents which files belong in the EPUB `<spine>` (reading order) vs. manifest-only (never in spine).

## Quick Reference

| Item | Manifest | Spine | Notes |
|------|----------|-------|-------|
| `nav.xhtml` (nav doc) | ✅ with `nav` attr | ❌ **NEVER** | Navigation, not reading content |
| `toc.ncx` (NCX) | ✅ | ❌ **NEVER** | EPUB 2 fallback, not reading content |
| `styles/epub.css` | ✅ | ❌ **NEVER** | CSS is linked from XHTML files |
| `cover.jpg` | ✅ with `properties="cover-image"` | ❌ **NEVER** | Referenced by cover.xhtml |
| `cover.xhtml` | ✅ | ✅ | First item in spine |
| `title.xhtml` | ✅ | ✅ | Reading content |
| `copyright.xhtml` | ✅ | ✅ | Reading content |
| All chapter/part XHTML | ✅ | ✅ | In reading order |
| Back matter XHTML | ✅ | ✅ | Last items in spine |

## Common Mistake: Nav/NCX/CSS in Spine

Putting navigation documents or CSS in the `<spine>` causes several problems:

- **Nav doc in spine**: eReaders show the TOC as a reading page instead of a hidden navigation overlay. Kindle Previewer may show a blank "Table of Contents" page as the first content page.
- **NCX in spine**: NCX is a binary-style XML structure not meant for rendering. Some readers crash or skip it.
- **CSS in spine**: CSS is not a reading-order item. Including it is structurally invalid.

## How to Check

After building an EPUB, unpack it and inspect the spine:

```bash
# Unpack
mkdir /tmp/check && cd /tmp/check && unzip -o book.epub

# Inspect spine — should list only content XHTML files
grep -A 50 '<spine' OEBPS/content.opf | grep itemref
```

If you see `nav.xhtml`, `toc.ncx`, or `epub.css` as `<itemref>` entries, the spine is wrong.

## Correct Spine Example

```xml
<spine page-progression-direction="ltr">
    <itemref idref="cover.xhtml"/>
    <itemref idref="title.xhtml"/>
    <itemref idref="copyright.xhtml"/>
    <itemref idref="acknowledgments.xhtml"/>
    <itemref idref="part1.xhtml"/>
    <itemref idref="ch01.xhtml"/>
    <itemref idref="ch02.xhtml"/>
    <itemref idref="part2.xhtml"/>
    <itemref idref="ch03.xhtml"/>
    <itemref idref="aboutauthor.xhtml"/>
</spine>
```

## Correct Manifest Example

```xml
<manifest>
    <!-- Navigation & metadata — NOT in spine -->
    <item id="nav.xhtml" href="nav.xhtml" media-type="application/xhtml+xml" nav/>
    <item id="toc.ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>
    <item id="epub.css" href="styles/epub.css" media-type="text/css"/>
    <item id="cover.jpg" href="images/cover.jpg" media-type="image/jpeg" properties="cover-image"/>

    <!-- Content — IN spine -->
    <item id="cover.xhtml" href="cover.xhtml" media-type="application/xhtml+xml"/>
    <item id="title.xhtml" href="title.xhtml" media-type="application/xhtml+xml"/>
    ...
</manifest>
```

## Why This Happens in Auto-Builders

Tools like the `build-epub-python.py` script (in this skill's `scripts/`) use a generic `add()` helper that adds to both manifest and spine. Before May 2026, nav/NCX/CSS were passed through this helper and ended up in the spine. The fix (applied 2026-05-11):

1. Added `in_spine=True` parameter to `add()`
2. Called `add(..., in_spine=False)` for nav, NCX, and CSS

Always verify the output of any auto-generation tool against this reference.
