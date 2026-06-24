# EPUB Div Tag Fix — Pattern & Script

## Problem
EPUB chapter XHTML files from PDF extraction/build pipelines often have unbalanced `<div>` tags:
- Orphan `</div>` with no matching open (e.g., `<hr/></div>\n<div id="ch1">`)
- Unclosed `<div id="chN">` with no matching close before `</body>`
- These cause `xml.etree.ElementTree.ParseError: mismatched tag`

## Detection & Repair
```python
import re

def fix_chapter_xml(content):
    body_start = content.find("<body")
    body_end = content.find("</body>")
    if body_start == -1 or body_end == -1:
        return content
    
    body = content[body_start:body_end]
    tag_pattern = re.compile(r'<(/?div)[^>]*>')
    
    div_tags = []
    for m in tag_pattern.finditer(body):
        tag = m.group(1)
        if tag in ('div', '/div'):
            div_tags.append((tag, m.start()))
    
    stack = []
    orphans = []
    for tag, pos in div_tags:
        if tag == 'div':
            stack.append(pos)
        else:
            if stack:
                stack.pop()
            else:
                orphans.append(pos)
    unclosed = stack
    
    if not orphans and not unclosed:
        return content  # Well-formed
    
    for pos in sorted(orphans, reverse=True):
        ap = pos + body_start
        ts = content.rfind('<', ap - 20, ap)
        te = content.find('>', ap, ap + 20) + 1
        if ts >= 0 and te > ts:
            content = content[:ts] + content[te:]
    
    for pos in sorted(unclosed, reverse=True):
        be = content.find("</body>")
        if be >= 0:
            content = content[:be] + '</div>\n' + content[be:]
    
    return content
```

## Known Patterns in Lunar Foundation EPUBs
| Pattern | Files | Fix |
|---------|-------|-----|
| `<hr/></div>\n<div id="ch1">` | ch01–ch02 (Book 3) | Remove orphan `</div>` |
| `</div>\n<div class="about-author">` | ch40 (Book 3) | Remove orphan `</div>` |
| `<div id="chN">` unclosed before `</body>` | Many chapters | Add `</div>` before `</body>` |
