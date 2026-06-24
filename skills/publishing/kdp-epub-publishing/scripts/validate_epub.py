#!/usr/bin/env python3
"""Validate KDP EPUBs — checks manifest, spine, NCX playOrder, chapters, images, nav property."""
import zipfile, re, os, sys

def validate_epub(path):
    z = zipfile.ZipFile(path, 'r')
    names = z.namelist()
    
    ncx_files = [n for n in names if n.endswith('.ncx')]
    ncx_po = 0
    if ncx_files:
        ncx = z.read(ncx_files[0]).decode('utf-8', errors='replace')
        ncx_po = len(re.findall(r'playOrder="\d+"', ncx))
    
    opf_files = [n for n in names if n.endswith('.opf')]
    manifest = spine = chapters = nav_prop = spine_toc = 0
    if opf_files:
        opf = z.read(opf_files[0]).decode('utf-8', errors='replace')
        items = re.findall(r'<item\s+(?:id="[^"]+"\s+)?href="([^"]+)"', opf)
        items += re.findall(r'<item\s+href="([^"]+)"\s+id="[^"]+"', opf)
        manifest = len(set(items))
        spine = len(re.findall(r'<itemref\s+idref="([^"]+)"', opf))
        nav_prop = 'properties="nav"' in opf
        spine_toc = 'toc="ncx"' in opf
    
    chapters = len([n for n in names if ('chapter' in n.lower() or 'ch0' in n.lower()) and n.endswith('.xhtml')])
    imgs = [n for n in names if n.split('.')[-1].lower() in ('png','jpg','jpeg','gif','svg')]
    
    ok = manifest > 10 and spine > 5 and ncx_po > 5 and chapters > 5
    z.close()
    return {
        'status': 'OK' if ok else 'BROKEN',
        'manifest': manifest, 'spine': spine, 'chapters': chapters,
        'ncx_po': ncx_po, 'images': len(imgs),
        'nav_prop': nav_prop, 'spine_toc': spine_toc
    }

if __name__ == '__main__':
    for path in sys.argv[1:]:
        r = validate_epub(path)
        bn = os.path.basename(path)
        print(f"{r['status']:7s} {bn:50s} m={r['manifest']:3d} s={r['spine']:3d} ch={r['chapters']:3d} po={r['ncx_po']:3d} img={r['images']:3d} nav={r['nav_prop']} toc={r['spine_toc']}")
