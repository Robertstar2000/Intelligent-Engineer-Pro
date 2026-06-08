# KDP Packaging Gap — May 31, 2026 Session Finding

## Problem
Books can have complete, full-size EPUBs (18-21MB) in their `output/` directory while the `KDP_PACKAGE/` directory contains only marketing materials. The KDP dir file count alone is NOT a reliable indicator of whether the book has content.

## What Happened
- AL B2 Mercury_Accord, B3 Ghosts_Beyond_Neptune, B4 Last_Photon_Fleet: All had 18-21MB EPUBs in output/ but KDP_PACKAGE dirs had only 6 files (cover + marketing)
- Owners_Manual_AI_Agents: Same pattern — 3MB EPUB in output/, KDP dir had 6 marketing files
- The inventory reference listed AL B2-4 as "empty shells needing chapters" — they were NOT empty

## Detection Pattern
When scanning KDP status, a KDP_PACKAGE dir with <10 files does NOT necessarily mean the book needs chapters written. It may mean:
1. The EPUB hasn't been copied into the KDP dir yet (fixable in seconds)
2. The EPUB exists in `output/` but the packaging step was never completed

**Always check `output/` for EPUBs separately from KDP_PACKAGE dir contents:**
```bash
# Finds all digital EPUBs regardless of KDP status
find ~/books/ -path "*/output/*_digital.epub" -exec ls -lh {} \; 2>/dev/null
```

## Resolution (June 1, 2026)
The EPUB-in-output gap was fixed for AL B2-4 and Owners Manual on May 31, 2026.
AL B2-4 were found to have FULL manuscripts (40 chapters each, 4,000+ lines), not empty shells.
All 4 books now have 18-21MB digital EPUBs copied into KDP_PACKAGE/ and zipped.
**16/19 books now have both KDP_PACKAGE directory AND .zip file.**

## Fix Pattern (CEO-executable via execute_code, ~10s per book)
```python
import shutil, zipfile, os

def fix_kdp_package(book_path, epub_name, zip_name):
    kdp_dir = os.path.join(book_path, 'KDP_PACKAGE')
    epub_src = os.path.join(book_path, 'output', epub_name)
    epub_dst = os.path.join(kdp_dir, epub_name)
    zip_path = os.path.join(book_path, zip_name)
    
    if not os.path.exists(epub_src):
        print(f"SKIP: EPUB not found at {epub_src}")
        return
    
    # Copy EPUB into KDP_PACKAGE
    shutil.copy2(epub_src, epub_dst)
    
    # Re-zip KDP_PACKAGE
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(kdp_dir):
            for f in files:
                file_path = os.path.join(root, f)
                arcname = os.path.relpath(file_path, kdp_dir)
                zf.write(file_path, arcname)
    
    print(f"Fixed: {book_path}")
```
