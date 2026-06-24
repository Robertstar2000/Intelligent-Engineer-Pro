# EPUB Chapter XML Repair

When fixing EPUBs that were built from a buggy pipeline (e.g., orphan `</div>` tags, HTML named entities in XHTML), apply these two fixes before modifying nav/toc/opf files.

## Fix 1: Orphan/Mismatched `</div>` Tags

**Symptom:** Chapter XHTML files fail XML parsing with `mismatched tag` errors. The body has `<hr/></div>` followed by `<div id="chN">` — the first `</div>` closes nothing (orphan), and the `<div id="chN">` is never closed.

**Pattern in Lunar Foundation V2.0 EPUBs:**
- ch01-ch39: `<hr/></div>\n<div id="chN">\n</body>\n</html>` — 1 orphan close, 1 unclosed open
- ch40 (end-matter): `</p></div>\n<div class="about-author">...` — 1 orphan close, 0 unclosed (the about-author div is properly closed)

**Fix approach — tag-stacking algorithm:**
```python
import re

tag_pattern = re.compile(r'<(/?\w+)[^>]*>')
body_start = content.find('<body')
body_end = content.find('</body>')
body = content[body_start:body_end]

# Collect div tags with their positions relative to content (not body)
div_tags = []
for m in tag_pattern.finditer(content, body_start, body_end):
    tag = m.group(1)
    if tag in ('div', '/div'):
        div_tags.append((tag, m.start()))

# Stack simulation to find orphan closes and unclosed opens
stack = []
orphans = []
for tag, pos in div_tags:
    if tag == 'div':
        stack.append(pos)
    else:  # /div
        if stack:
            stack.pop()
        else:
            orphans.append(pos)
unclosed = stack  # remaining opens

# Fix from right to left (preserves positions)
for pos in sorted(orphans, reverse=True):
    tag_start = content.rfind('<', pos - 20, pos)
    tag_end = content.find('>', pos, pos + 20) + 1
    if tag_start >= 0 and tag_end > tag_start:
        content = content[:tag_start] + content[tag_end:]

for pos in sorted(unclosed, reverse=True):
    body_end = content.find('</body>')
    if body_end >= 0:
        content = content[:body_end] + '</div>\n' + content[body_end:]
```

**⚠️ Critical:** The positions from `tag_pattern.finditer(content, body_start, body_end)` are **absolute positions in `content`**, not relative to `body`. If you slice `body = content[body_start:body_end]` and iterate over that, the positions become relative. You MUST add `body_start` back when searching for tags in `content`.

## Fix 2: HTML Named Entities → Numeric XML Entities

**Symptom:** Chapter XHTML files fail XML parsing with `undefined entity` errors. HTML named entities like `&mdash;` and `&rdquo;` are not valid in XHTML without a DTD.

**Valid XML entities only:** `&amp;` `&lt;` `&gt;` `&quot;` `&apos;` — everything else must be numeric.

**Entity mapping:**
| HTML entity | XML numeric | Character |
|-------------|-------------|-----------|
| `&mdash;` | `&#8212;` | em dash |
| `&ndash;` | `&#8211;` | en dash |
| `&ldquo;` | `&#8220;` | left double quote |
| `&rdquo;` | `&#8221;` | right double quote |
| `&lsquo;` | `&#8216;` | left single quote |
| `&rsquo;` | `&#8217;` | right single quote |
| `&hellip;` | `&#8230;` | ellipsis |
| `&nbsp;` | `&#160;` | non-breaking space |
| `&copy;` | `&#169;` | copyright |
| `&reg;` | `&#174;` | registered |
| `&trade;` | `&#8482;` | trademark |

```python
named_entities = {
    '&mdash;': '&#8212;', '&ndash;': '&#8211;',
    '&ldquo;': '&#8220;', '&rdquo;': '&#8221;',
    '&lsquo;': '&#8216;', '&rsquo;': '&#8217;',
    '&hellip;': '&#8230;', '&nbsp;': '&#160;',
    '&copy;': '&#169;', '&reg;': '&#174;', '&trade;': '&#8482;',
}
entity_pattern = re.compile('|'.join(re.escape(k) for k in named_entities))
content = entity_pattern.sub(lambda m: named_entities[m.group(0)], content)
```

## Fix 3: Update nav.xhtml with Front Matter + Landmarks

The nav.xhtml must include:
1. Front matter entries (title, copyright, TOC) in the TOC nav BEFORE chapters
2. A separate `<nav epub:type="landmarks">` with at minimum a bodymatter link

Pattern:
```xml
<nav epub:type="toc" id="toc">
  <h1>Table of Contents</h1>
  <ol>
    <li><a href="title.xhtml">Title Page</a></li>
    <li><a href="copyright.xhtml">Copyright</a></li>
    <li><a href="toc.xhtml">Table of Contents</a></li>
    ... chapters ...
  </ol>
</nav>
<nav epub:type="landmarks">
  <h2>Landmarks</h2>
  <ol>
    <li><a epub:type="bodymatter" href="ch01.xhtml">Start Reading</a></li>
  </ol>
</nav>
```

## Verification

```bash
# Extract EPUB
mkdir -p /tmp/check && cd /tmp/check && rm -rf * && unzip -o /path/to/book.epub

# 1. Check XML validity of all chapter files
python3 -c "
import xml.etree.ElementTree as ET, glob
bad = 0
for f in sorted(glob.glob('OEBPS/ch*.xhtml')):
    try: ET.parse(f)
    except ET.ParseError as e: 
        bad += 1
        if bad == 1: print(f'{f}: {e}')
print(f'Bad: {bad}/{len(glob.glob(\"OEBPS/ch*.xhtml\"))}')
"

# 2. Check HTML named entities
grep -rn '&\(mdash\|ndash\|ldquo\|rdquo\|lsquo\|rsquo\|hellip\|nbsp\|copy\|reg\|trade\)' OEBPS/*.xhtml

# 3. Verify landmarks
grep 'epub:type="landmarks"' OEBPS/nav.xhtml && echo "Landmarks: OK" || echo "Landmarks: MISSING"
grep 'epub:type="bodymatter"' OEBPS/nav.xhtml && echo "Bodymatter: OK" || echo "Bodymatter: MISSING"

# 4. Verify front matter in nav
grep -c 'title.xhtml\|copyright.xhtml\|toc.xhtml' OEBPS/nav.xhtml && echo "Front matter in nav: OK"

# 5. Check toc.ncx
test -f OEBPS/toc.ncx && echo "toc.ncx: OK" || echo "toc.ncx: MISSING"
grep 'toc="ncx"' OEBPS/content.opf && echo "OPF toc: OK" || echo "OPF toc: MISSING"
```