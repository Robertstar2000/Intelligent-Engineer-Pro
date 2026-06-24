# ODG Manuscript Extraction

## Problem
User provides an OpenDocument Drawing (.odg) file containing manuscript text. Need to extract clean text for comparison with the markdown manuscript.

## Solution

```python
import zipfile
import xml.etree.ElementTree as ET
import re

def extract_odg_text(odg_path):
    with zipfile.ZipFile(odg_path, 'r') as z:
        content = z.read("content.xml").decode("utf-8")
    root = ET.fromstring(content)
    paragraphs = root.iter('{urn:oasis:names:tc:opendocument:xmlns:text:1.0}p')
    paras = []
    for p in paragraphs:
        texts = []
        for elem in p.iter():
            if elem.text and elem.text.strip():
                texts.append(elem.text.strip())
            if elem.tail and elem.tail.strip():
                texts.append(elem.tail.strip())
        if texts:
            para = ' '.join(texts)
            para = re.sub(r'  +', ' ', para)
            if para.strip():
                paras.append(para.strip())
    return '\n\n'.join(paras)
```

## Key Patterns
- ODG = ZIP with `content.xml` containing all text
- Text fragmented across `<text:p>` and `<text:span>` — join with spaces
- Scene breaks: `\n•\n•\n•\n` → `\n\n• • •\n\n`
- Page numbers: standalone digits — remove
- Chapter headings: "Chapter N: Title" or "Chapter N — Title"
- Preserve image references from current markdown manuscript
