# HTML Heading Formats in Manuscript Sources

When building EPUBs from HTML manuscripts, the chapter heading format varies by book. The build script must detect and handle all patterns.

## Pattern Catalog

| Pattern | HTML | Found In |
|---------|------|----------|
| A | `<h2>Chapter N — Title</h2>` | No Blue Sky: Built from Dust |
| B | `<h1 class="chapter-title" id="chN">Chapter N — Title</h1>` | No Blue Sky: The Oxygen Gamble |
| C | `<h1>Chapter N &mdash; Title</h1>` | No Blue Sky: Red Charter, First Martian Nation, Rivers Under Mars |
| D | `<div id="chN"><h1>Chapter N — Title</h1>...` | Lunar Foundation: Moon Rock, Mooncoming, Waters End |

## Universal Detection Regex

```python
import re

chapter_pattern = re.compile(
    r'(<h[12][^>]*>(?:Chapter|PART)\s[^<]+</h[12]>)|'
    r'(<div\s+id="ch\d+"[^>]*>\s*<h[12][^>]*>(?:Chapter|PART)\s[^<]+</h[12]>\s*</div>)',
    re.DOTALL | re.IGNORECASE
)
```

## Pitfalls

1. **Body-relative positions** — Run the regex on the extracted `<body>` content, not the full HTML file. Chapter positions relative to `<body>` are what you need for content splitting.

2. **TOC contamination** — The HTML `<body>` may contain a TOC with `<h2>Chapter N — Title</h2>` entries identical to the actual chapter headings. The regex will match both the TOC entry AND the real chapter heading. Either filter out duplicates by position proximity, or slice chapters from the last TOC entry onward.

3. **&mdash; vs — vs --** — Different sources use different dash styles. Normalize all to `—` before displaying in the TOC.

4. **PART headers** — Some books have `<h1>PART I — Title</h1>` or `<h2>PART I — Title</h2>` in addition to Chapter headings. These should be included as section markers in the TOC if present.

5. **Empty chapter stubs** — Some manuscripts have `<h2>Chapter N</h2>` (no title text after the number) as placeholders for unwritten chapters. Skip or warn about these during EPUB build.

## Verification

```bash
# Check how many chapters the regex finds
python3 -c "
import re
with open('manuscript.html') as f:
    body = re.search(r'<body[^>]*>(.*?)</body>', f.read(), re.DOTALL)
content = body.group(1) if body else f.read()
pat = re.compile(r'(<h[12][^>]*>(?:Chapter|PART)\s[^<]+</h[12]>)|(<div\s+id=\"ch\d+\"[^>]*>.*?</div>)', re.DOTALL|re.IGNORECASE)
matches = list(pat.finditer(content))
print(f'Found {len(matches)} chapter headings')
for m in matches:
    print(f'  {re.sub(r\"<[^>]+>\", \"\", m.group(0)).strip()[:80]}')
"
```
