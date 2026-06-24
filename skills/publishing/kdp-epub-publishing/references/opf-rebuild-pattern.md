# OPF Rebuild Pattern for Corrupted EPUBs

## When to Use
- OPF has `<itemref>` elements inside `<manifest>` section
- `re.findall(r'<itemref...', opf)` returns 3x expected count
- Spine has duplicate itemrefs (same idref appearing multiple times)
- Manifest has duplicate `<item>` entries for the same file

## Rebuild Procedure

```python
import zipfile, re, os, shutil, tempfile

def rebuild_opf(opf):
    # 1. Extract metadata
    metadata_match = re.search(r'<metadata[^>]*>(.*?)</metadata>', opf, re.DOTALL)
    metadata = metadata_match.group(0) if metadata_match else ''
    
    # 2. Extract ONLY <item> elements from manifest (not <itemref>)
    manifest_match = re.search(r'<manifest[^>]*>(.*?)</manifest>', opf, re.DOTALL)
    if manifest_match:
        items = re.findall(r'<item\s+[^>]+/>', manifest_match.group(1))
        # Deduplicate by id
        seen_ids = set()
        unique_items = []
        for item in items:
            id_match = re.search(r'id="([^"]+)"', item)
            if id_match and id_match.group(1) not in seen_ids:
                seen_ids.add(id_match.group(1))
                unique_items.append(item)
        
        new_manifest = '<manifest>\n'
        for item in unique_items:
            new_manifest += '    ' + item + '\n'
        new_manifest += '  </manifest>'
    
    # 3. Extract itemrefs from SPINE section only
    spine_match = re.search(r'<spine[^>]*>(.*?)</spine>', opf, re.DOTALL)
    if spine_match:
        itemrefs = re.findall(r'<itemref\s+idref="([^"]+)"', spine_match.group(1))
        # Deduplicate preserving order
        seen = set()
        deduped = [r for r in itemrefs if not (r in seen or seen.add(r))]
        
        # Move front matter to first position
        front = [r for r in deduped if any(x in r.lower() for x in ['front', 'title', 'copyright'])]
        chapters = [r for r in deduped if r not in front and 'nav' not in r.lower()]
        nav = [r for r in deduped if 'nav' in r.lower()]
        new_order = front + chapters + nav
        
        spine_tag = re.search(r'<spine[^>]*>', opf).group(0)
        new_spine = spine_tag + '\n'
        for ref in new_order:
            new_spine += '        <itemref idref="' + ref + '"/>\n'
        new_spine += '    </spine>'
    
    # 4. Extract guide
    guide_match = re.search(r'<guide[^>]*>(.*?)</guide>', opf, re.DOTALL)
    guide = guide_match.group(0) if guide_match else ''
    
    # 5. Rebuild
    package_tag = re.search(r'<package[^>]*>', opf).group(0)
    new_opf = '<?xml version="1.0" encoding="UTF-8"?>\n'
    new_opf += package_tag + '\n' + metadata + '\n'
    new_opf += new_manifest + '\n' + new_spine + '\n' + guide + '\n'
    new_opf += '</package>'
    return new_opf


def fix_ncx(ncx):
    """Deduplicate and reorder NCX navPoints."""
    navpoint_blocks = re.findall(r'(<navPoint[^>]*>.*?</navPoint>)', ncx, re.DOTALL)
    if not navpoint_blocks:
        return ncx
    
    # Deduplicate by content src
    seen_srcs = set()
    deduped = []
    front_np = None
    for np in navpoint_blocks:
        src_match = re.search(r'<content\s+src="([^"]+)"', np)
        src = src_match.group(1) if src_match else ''
        if src and src not in seen_srcs:
            seen_srcs.add(src)
            if any(x in np.lower() for x in ['front', 'title', 'copyright']):
                front_np = np
            else:
                deduped.append(np)
    
    new_nps = ([front_np] if front_np else []) + deduped
    
    # Reassign playOrder
    for i, np in enumerate(new_nps, 1):
        new_nps[i-1] = re.sub(r'playOrder="\d+"', 'playOrder="' + str(i) + '"', np)
    
    navmap_match = re.search(r'<navMap[^>]*>(.*?)</navMap>', ncx, re.DOTALL)
    if navmap_match:
        ncx = ncx.replace(navmap_match.group(1), '\n' + '\n'.join(new_nps) + '\n    ')
    return ncx
```

## Validation After Fix
```python
# Check spine has no duplicates
spine_match = re.search(r'<spine[^>]*>(.*?)</spine>', opf, re.DOTALL)
spine_refs = re.findall(r'<itemref\s+idref="([^"]+)"', spine_match.group(1))
assert len(spine_refs) == len(set(spine_refs)), "Duplicate spine itemrefs!"
assert spine_refs[0].startswith('front') or 'title' in spine_refs[0], "Front not first!"

# Check manifest has no itemrefs
manifest_match = re.search(r'<manifest[^>]*>(.*?)</manifest>', opf, re.DOTALL)
assert '<itemref' not in manifest_match.group(1), "itemrefs in manifest!"
```
