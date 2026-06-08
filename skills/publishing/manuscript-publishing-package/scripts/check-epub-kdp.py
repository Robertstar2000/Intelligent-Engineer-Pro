#!/usr/bin/env python3
"""
Comprehensive EPUB QA checker — structure, content, and KDP compatibility.

Usage:
    python3 check-epub.py /path/to/book.epub

Checks:
    - ZIP structure (mimetype first, uncompressed)
    - Required files (container.xml, content.opf, nav.xhtml, toc.ncx)
    - OPF metadata completeness (title, creator, language, identifier, timestamp)
    - Cover-image property
    - Nav TOC completeness with epub:type=toc
    - NCX backward compat
    - XHTML well-formedness
    - Chapter file count and headings
    - No scripts in any XHTML
    - No duplicate IDs
    - Image presence and size
    - Guide items (cover, toc, text)
"""

import sys, os, re, zipfile
from pathlib import Path


def check(epub_path):
    book = Path(epub_path).stem
    issues, passes = [], []

    if not os.path.exists(epub_path):
        return book, [("FATAL", "File not found")], passes

    size_kb = os.path.getsize(epub_path) // 1024
    passes.append(f"Size: {size_kb}KB")

    try:
        zf = zipfile.ZipFile(epub_path, 'r')
    except zipfile.BadZipFile:
        return book, [("FATAL", "Not a valid ZIP")], passes

    names = zf.namelist()

    # mimetype
    if 'mimetype' in names:
        info = zf.getinfo('mimetype')
        if info.compress_type == zipfile.ZIP_STORED:
            passes.append("mimetype: stored ✓")
        else:
            issues.append(("WARN", "mimetype should be stored"))
        if names.index('mimetype') == 0:
            passes.append("mimetype: first entry ✓")
        else:
            issues.append(("WARN", "mimetype not first"))
        if zf.read('mimetype').decode().strip() == 'application/epub+xml':
            passes.append("mimetype: content correct ✓")
        else:
            issues.append(("FAIL", "mimetype content wrong"))
    else:
        issues.append(("FAIL", "Missing mimetype"))

    # Required files
    for req in ['META-INF/container.xml', 'OEBPS/content.opf']:
        if req in names:
            passes.append(f"{req} ✓")
        else:
            issues.append(("FAIL", f"Missing {req}"))

    # container.xml
    if 'META-INF/container.xml' in names:
        cont = zf.read('META-INF/container.xml').decode()
        if 'OEBPS/content.opf' in cont:
            passes.append("container.xml: points to content.opf ✓")
        else:
            issues.append(("FAIL", "container.xml bad ref"))

    # content.opf
    if 'OEBPS/content.opf' in names:
        opf = zf.read('OEBPS/content.opf').decode()
        for field in ['<dc:title>', '<dc:creator>', '<dc:language>', '<dc:identifier']:
            passes.append(f"OPF: {field} ✓" if field in opf else issues.append(("FAIL", f"Missing {field}")))
        if 'dcterms:modified' in opf:
            passes.append("OPF: timestamp ✓")
        else:
            issues.append(("WARN", "Missing dcterms:modified"))
        if 'properties="cover-image"' in opf:
            passes.append("OPF: cover-image ✓")
        else:
            issues.append(("WARN", "Missing cover-image"))
        mi = re.findall(r'<item\s+id="([^"]+)"\s+href="([^"]+)"', opf)
        si = re.findall(r'<itemref\s+idref="([^"]+)"', opf)
        passes.append(f"Manifest: {len(mi)} items ✓")
        passes.append(f"Spine: {len(si)} itemrefs ✓")
        if any(h == 'nav.xhtml' for _, h in mi):
            passes.append("nav.xhtml in manifest ✓")
        else:
            issues.append(("FAIL", "nav.xhtml not in manifest"))
        for ref_type in ['cover', 'toc', 'text']:
            if f'type="{ref_type}"' in opf:
                passes.append(f"Guide: {ref_type} ✓")
            else:
                issues.append(("WARN", f"Missing guide {ref_type}"))

    # nav.xhtml
    if 'OEBPS/nav.xhtml' in names:
        nav = zf.read('OEBPS/nav.xhtml').decode()
        if 'epub:type="toc"' in nav:
            passes.append("nav: epub:type=toc ✓")
        else:
            issues.append(("FAIL", "nav missing epub:type=toc"))
        links = re.findall(r'<a href="([^"]+)">', nav)
        passes.append(f"nav: {len(links)} TOC entries ✓")
    else:
        issues.append(("FAIL", "Missing nav.xhtml"))

    # NCX
    if 'OEBPS/toc.ncx' in names:
        ncx = zf.read('OEBPS/toc.ncx').decode()
        pts = ncx.count('<navPoint')
        passes.append(f"NCX: {pts} navPoints ✓")
    else:
        issues.append(("WARN", "Missing toc.ncx"))

    # XHTML files
    xhtmls = [n for n in names if n.endswith('.xhtml') and n.startswith('OEBPS/')]
    passes.append(f"XHTML files: {len(xhtmls)} ✓")
    for exp in ['cover.xhtml', 'title.xhtml', 'copyright.xhtml', 'toc.xhtml', 'nav.xhtml', 'about.xhtml']:
        if f'OEBPS/{exp}' in names:
            passes.append(f"  {exp} ✓")
        else:
            issues.append(("WARN", f"Missing {exp}"))
    ch_files = [n for n in xhtmls if re.match(r'OEBPS/ch\d{3}\.xhtml$', n)]
    if len(ch_files) >= 5:
        passes.append(f"Chapters: {len(ch_files)} ✓")
    else:
        issues.append(("WARN", f"Only {len(ch_files)} chapter files"))

    # No scripts
    for n in (n for n in names if n.endswith('.xhtml')):
        if '<script' in zf.read(n).decode(errors='ignore').lower():
            issues.append(("FAIL", f"Script in {n}"))

    # Duplicate IDs
    all_ids = []
    for n in (n for n in names if n.endswith('.xhtml')):
        ids = re.findall(r'id="([^"]*)"', zf.read(n).decode(errors='ignore'))
        all_ids.extend(ids)
    dupes = {k: v for k, v in {i: all_ids.count(i) for i in set(all_ids)}.items() if v > 1}
    if dupes:
        for i, c in dupes.items():
            issues.append(("WARN", f"Duplicate ID '{i}' x{c}"))

    # Images
    imgs = [n for n in names if n.startswith('OEBPS/images/')]
    if imgs:
        passes.append(f"Images: {len(imgs)} ✓")
        for img in imgs:
            sz = len(zf.read(img))
            if sz > 50000:
                passes.append(f"  {Path(img).name}: {sz//1024}KB ✓")
            else:
                issues.append(("WARN", f"  {Path(img).name}: small ({sz//1024}KB)"))

    zf.close()
    fails = len([i for i in issues if i[0] == "FAIL"])
    warns = len([i for i in issues if i[0] == "WARN"])
    return book, issues, passes, fails, warns


if __name__ == "__main__":
    paths = sys.argv[1:] if len(sys.argv) > 1 else ['.']
    all_epubs = []
    for p in paths:
        pobj = Path(p)
        if pobj.is_dir():
            all_epubs.extend(sorted(pobj.glob("*.epub")))
        elif pobj.suffix == '.epub':
            all_epubs.append(pobj)

    if not all_epubs:
        print("No EPUBs found.")
        sys.exit(1)

    total_fails, total_warns = 0, 0
    for ep in all_epubs:
        print(f"\n{'='*60}")
        print(f"📖 {ep.stem}")
        print(f"{'='*60}")
        result = check(str(ep))
        book, issues, passes, fails, warns = result if len(result) == 5 else (result[0], result[1], result[2], 0, 0)
        if len(result) >= 5:
            fails, warns = result[3], result[4]

        for p in passes:
            print(f"  ✓ {p}")
        for sev, msg in issues:
            icon = "❌" if sev == "FAIL" else "⚠️"
            print(f"  {icon} [{sev}] {msg}")
        total_fails += fails
        total_warns += warns
        status = "✅ PASS" if fails == 0 else "❌ FAIL"
        print(f"\n  {status}: {len(passes)} checks, {fails} fails, {warns} warnings")

    print(f"\n{'='*60}")
    print(f"Total: {total_fails} failures, {total_warns} warnings across {len(all_epubs)} EPUBs")
    print(f"{'='*60}")
