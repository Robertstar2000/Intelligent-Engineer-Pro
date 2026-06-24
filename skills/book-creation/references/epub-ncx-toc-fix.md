# EPUB NCX TOC Fix — playOrder Requirement

## Problem
EPUBs generated via zipfile (Python) often have NCX (Table of Contents) files that lack `playOrder` attributes on `<navPoint>` elements. Without `playOrder`, Kindle and other e-readers cannot display the TOC — the entries exist but the reader has no way to determine their sequence.

## Root Cause
The NCX format requires `playOrder` attributes for Kindle TOC rendering. Many EPUB generation tools (including hand-rolled zipfile-based builds) omit these attributes.

## Fix Script
```python
#!/usr/bin/env python3
"""Add playOrder attributes to all navPoint elements in NCX files within an EPUB."""
import zipfile
import os
import tempfile
from pathlib import Path

def fix_ncx_playorder(ncx_content):
    lines = ncx_content.split('\n')
    result = []
    play_order = 0
    for line in lines:
        if '<navPoint id=' in line and 'playOrder' not in line:
            line = line.replace('<navPoint id=', f'<navPoint playOrder="{play_order}" id=', 1)
            play_order += 1
        result.append(line)
    return '\n'.join(result)

def fix_epub_toc(epub_path):
    with tempfile.TemporaryDirectory() as tmpdir:
        with zipfile.ZipFile(epub_path, 'r') as zf:
            zf.extractall(tmpdir)
        ncx_files = list(Path(tmpdir).rglob('*.ncx'))
        for ncx_path in ncx_files:
            with open(ncx_path, 'r', encoding='utf-8') as f:
                content = f.read()
            with open(ncx_path, 'w', encoding='utf-8') as f:
                f.write(fix_ncx_playorder(content))
        with zipfile.ZipFile(epub_path, 'w', zipfile.ZIP_DEFLATED) as zf:
            for root, dirs, files in os.walk(tmpdir):
                for file in files:
                    fp = os.path.join(root, file)
                    arcname = os.path.relpath(fp, tmpdir)
                    zf.write(fp, arcname)
```

## When to Apply
- When Kindle reports "no TOC" or TOC navigation doesn't work
- After rebuilding EPUBs from HTML sources
- As a post-build verification step before KDP upload

## Verification
```bash
# Check playOrder count in an EPUB's NCX
unzip -p book.epub EPUB/toc.ncx | grep -c 'playOrder='
# Should return the number of navPoint entries (e.g., 40 for a 39-chapter book + front matter)
```

## Also Check: EPUBs Without NCX
Some EPUBs (especially EPUB3-only builds) have `nav.xhtml` with `properties="nav"` but no NCX file at all. For Kindle compatibility, add an NCX file extracted from the nav.xhtml content. The NCX must include both the `playOrder` attributes AND be referenced in the OPF manifest with `<spine toc="ncx">`.

## Series Fixed
- Lunar Foundation Series (4 books, 20 EPUB files) — June 2026
