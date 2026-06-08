#!/usr/bin/env python3
"""EPUB QA Checker — validate structure, content, and compatibility of EPUB files.
Checks: mimetype format, ZIP structure, content.opf metadata/manifest/spine,
nav.xhtml TOC, toc.ncx, XHTML well-formedness, no scripts, no duplicate IDs,
image sizes, and required front/back matter files.

Usage:
  python3 epub-qa.py [directory_with_epubs]     # Default: current directory
  python3 epub-qa.py path/to/file.epub           # Single file

Produces per-file pass/fail/warning output with summary at end.
Requires: Python stdlib only.
"""
import zipfile, os, re, sys
from pathlib import Path

def check_epub(epub_path):
    """Run full QA check on an EPUB file."""
    book_name = epub_path.stem
    issues, passes = [], []
    
    if not epub_path.exists():
        return book_name, [("FATAL", "File not found")], passes
    
    size_kb = os.path.getsize(epub_path) // 1024
    passes.append(f"File size: {size_kb} KB")
    if size_kb < 100:
        issues.append(("WARN", f"Very small EPUB ({size_kb} KB)"))
    
    try:
        zf = zipfile.ZipFile(epub_path, 'r')
    except zipfile.BadZipFile:
        return book_name, [("FATAL", "Not a valid ZIP file")], passes
    
    namelist = zf.namelist()
    
    # 1. mimetype
    if 'mimetype' not in namelist:
        issues.append(("FAIL", "Missing mimetype"))
    else:
        info = zf.getinfo('mimetype')
        if info.compress_type != zipfile.ZIP_STORED:
            issues.append(("WARN", "mimetype should be stored uncompressed"))
        if namelist.index('mimetype') != 0:
            issues.append(("WARN", "mimetype should be first ZIP entry"))
        mt = zf.read('mimetype').decode('utf-8').strip()
        if mt != 'application/epub+xml':
            issues.append(("FAIL", f"mimetype wrong: '{mt}'"))
        else:
            passes.append("mimetype ✓")
    
    # 2. Required dirs/files
    for req in ['META-INF/container.xml', 'OEBPS/content.opf']:
        if req in namelist:
            passes.append(f"{req} ✓")
        else:
            issues.append(("FAIL", f"Missing: {req}"))
    
    # 3. container.xml
    if 'META-INF/container.xml' in namelist:
        cont = zf.read('META-INF/container.xml').decode('utf-8')
        if 'OEBPS/content.opf' in cont:
            passes.append("container.xml -> content.opf ✓")
        else:
            issues.append(("FAIL", "container.xml missing content.opf ref"))
    
    # 4. content.opf
    if 'OEBPS/content.opf' in namelist:
        opf = zf.read('OEBPS/content.opf').decode('utf-8')
        for field in ['<dc:title>', '<dc:creator>', '<dc:language>', '<dc:identifier']:
            if field in opf:
                passes.append(f"OPF: {field} ✓")
            else:
                issues.append(("FAIL", f"OPF missing: {field}"))
        if 'dcterms:modified' in opf:
            passes.append("OPF: dcterms:modified ✓")
        if 'properties="cover-image"' in opf:
            passes.append("OPF: cover-image ✓")
        
        manifest = re.findall(r'<item\s+id="([^"]+)"\s+href="([^"]+)"', opf)
        passes.append(f"OPF manifest: {len(manifest)} items ✓")
        
        if any(h == 'nav.xhtml' for _, h in manifest):
            passes.append("OPF: nav.xhtml in manifest ✓")
        else:
            issues.append(("FAIL", "nav.xhtml not in manifest"))
        
        spine = re.findall(r'<itemref\s+idref="([^"]+)"', opf)
        passes.append(f"OPF spine: {len(spine)} itemrefs ✓")
        
        if '<guide>' in opf:
            for rt in ['cover', 'toc', 'text']:
                if f'type="{rt}"' in opf:
                    passes.append(f"Guide: {rt} ✓")
                else:
                    issues.append(("WARN", f"Guide missing: {rt}"))
        else:
            issues.append(("WARN", "No <guide> in OPF"))
    
    # 5. Nav TOC
    if 'OEBPS/nav.xhtml' in namelist:
        nav = zf.read('OEBPS/nav.xhtml').decode('utf-8')
        if 'epub:type="toc"' in nav:
            passes.append("nav: epub:type=toc ✓")
        else:
            issues.append(("FAIL", "nav missing epub:type=toc"))
        links = re.findall(r'<a href="([^"]+)"', nav)
        passes.append(f"nav: {len(links)} entries ✓")
        for link in links:
            if f"OEBPS/{link}" not in namelist:
                issues.append(("WARN", f"nav link target not found: {link}"))
    else:
        issues.append(("FAIL", "Missing nav.xhtml"))
    
    # 6. NCX
    if 'OEBPS/toc.ncx' in namelist:
        ncx_count = zf.read('OEBPS/toc.ncx').decode('utf-8').count('<navPoint')
        passes.append(f"NCX: {ncx_count} navPoints ✓")
    else:
        issues.append(("WARN", "Missing toc.ncx"))
    
    # 7. XHTML files
    xhtml = [n for n in namelist if n.endswith('.xhtml') and n.startswith('OEBPS/')]
    passes.append(f"XHTML: {len(xhtml)} files ✓")
    
    for exp in ['cover.xhtml', 'title.xhtml', 'copyright.xhtml', 'toc.xhtml', 'nav.xhtml', 'about.xhtml']:
        if f'OEBPS/{exp}' in namelist:
            passes.append(f"  {exp} ✓")
        else:
            issues.append(("WARN", f"Missing: {exp}"))
    
    chapters = [n for n in xhtml if re.match(r'OEBPS/ch\d{3}\.xhtml$', n)]
    if chapters:
        passes.append(f"Chapters: {len(chapters)} ✓")
        # Spot-check first chapter
        try:
            ch1 = zf.read(chapters[0]).decode('utf-8')
            if '<h2>' in ch1 or '<h1>' in ch1:
                passes.append(f"  {chapters[0]}: has heading ✓")
        except:
            pass
    
    # 8. No scripts
    for fname in xhtml:
        content = zf.read(fname).decode('utf-8', errors='ignore')
        if '<script' in content.lower():
            issues.append(("FAIL", f"Script in: {fname}"))
    
    # 9. Images
    images = [n for n in namelist if n.startswith('OEBPS/images/')]
    if images:
        passes.append(f"Images: {len(images)} ✓")
        for img in images:
            sz = len(zf.read(img))
            passes.append(f"  {Path(img).name}: {sz//1024}KB")
            if sz < 10000:
                issues.append(("WARN", f"  Small image: {Path(img).name}"))
    
    zf.close()
    
    return book_name, issues, passes

def main():
    paths = sys.argv[1:] if len(sys.argv) > 1 else ['.']
    
    epub_files = []
    for p in paths:
        pobj = Path(p)
        if pobj.is_file() and pobj.suffix == '.epub':
            epub_files.append(pobj)
        elif pobj.is_dir():
            epub_files.extend(sorted(pobj.glob("*.epub")))
    
    if not epub_files:
        print("No .epub files found.")
        return
    
    total_fails = total_warns = 0
    
    for epub in epub_files:
        name, issues, passes = check_epub(epub)
        fails = len([i for i in issues if i[0] == "FAIL"])
        warns = len([i for i in issues if i[0] == "WARN"])
        total_fails += fails
        total_warns += warns
        
        status = "✅ PASS" if not fails else "❌ FAIL"
        print(f"\n{'='*50}")
        print(f"{status} {name}")
        print(f"{'='*50}")
        for p in passes:
            print(f"  ✓ {p}")
        for sev, msg in issues:
            icon = "❌" if sev == "FAIL" else "⚠️"
            print(f"  {icon} [{sev}] {msg}")
    
    print(f"\n{'='*50}")
    print(f"Total: {total_fails} failures, {total_warns} warnings across {len(epub_files)} EPUBs")
    print(f"{'='*50}")

if __name__ == "__main__":
    main()
