# EPUB Validation Patterns

## Critical Checks (KDP will fail without these)

### NCX Validation
```python
import zipfile, re
z = zipfile.ZipFile(path, 'r')
names = z.namelist()

ncx_files = [n for n in names if n.endswith('.ncx')]
ncx = z.read(ncx_files[0]).decode('utf-8', errors='replace')
ncx_po = len(re.findall(r'playOrder="\d+"', ncx))
ncx_entries = len(re.findall(r'<navPoint', ncx))
# FAIL if ncx_po == 0 or ncx_po != ncx_entries
```

### OPF Validation
```python
opf = z.read(opf_files[0]).decode('utf-8', errors='replace')
has_nav_prop = 'properties="nav"' in opf
has_spine_toc = re.search(r'<spine\s+toc="ncx"', opf) is not None
items = re.findall(r'<item\s+(?:id="[^"]+"\s+)?href="([^"]+)"', opf)
manifest_count = len(set(items))
spine_count = len(re.findall(r'<itemref\s+idref="([^"]+)"', opf))
```

### nav.xhtml Validation
```
has_toc = 'epub:type="toc"' in nav
has_landmarks = 'epub:type="landmarks"' in nav
```

## Pass Criteria
- manifest > 10, spine > 5, ncx_po > 5, chapters > 5
- Spine first itemref must contain 'front', 'title', or 'copyright'
- No duplicate itemrefs in spine
- No `<itemref>` elements inside `<manifest>` section
- NCX first content src must contain 'front', 'title', or 'copyright'

## Corrupted OPF Detection
```python
# Check for itemrefs in manifest (corrupted OPF)
manifest_match = re.search(r'<manifest[^>]*>(.*?)</manifest>', opf, re.DOTALL)
if '<itemref' in manifest_match.group(1):
    issues.append("CORRUPTED: itemrefs inside manifest section")

# Check for duplicate spine itemrefs
spine_match = re.search(r'<spine[^>]*>(.*?)</spine>', opf, re.DOTALL)
spine_refs = re.findall(r'<itemref\s+idref="([^"]+)"', spine_match.group(1))
if len(spine_refs) != len(set(spine_refs)):
    issues.append(f"Duplicate spine itemrefs: {len(spine_refs)} total, {len(set(spine_refs))} unique")
```

## MIFECO Book Directory Structure
```
Book_1_Moon_Rock/
├── images/              # Source images (ch01.png, ch02.png, ...)
├── chapter_images/      # Duplicate of images/
├── KDP_Package/         # Short names: moon-rock.epub
├── KDP_PACKAGE/Kindle/  # Kindle versions
└── output/              # Working copies with _fixed suffix
```

## Two-Pass Rebuild Strategy
1. First pass: Fix NCX playOrder in existing EPUBs (if structure is sound)
2. Second pass: Full rebuild from known-good source using os.listdir() to rebuild manifest

Always use second pass when: manifest < 5, spine < 3, no chapters, OPF corrupted
