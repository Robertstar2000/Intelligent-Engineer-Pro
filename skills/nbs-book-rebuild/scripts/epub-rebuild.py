#!/usr/bin/env python3
"""
Complete EPUB rebuild script — production template.
Rebuilds an EPUB from source with:
- Image replacement from external directory
- Spine rebuild from manifest (fixes broken AL-style spines)
- Duplicate chapter prefix fix (handles both N===M and N!==M patterns)
- Bodymatter landmark auto-add
- Safe zipfile read-from-source / write-to-destination pattern

Usage:
    python3 epub-rebuild.py <source_epub> <output_epub> <images_dir> <expected_chapters>

Example:
    python3 epub-rebuild.py moon-rock.epub moon-rock_updated.epub ./output 39
"""
import sys
import zipfile
import re
import os


def fix_duplicate_chapter(text):
    """Fix any duplicate chapter prefix pattern. Keeps the SECOND chapter number."""
    # "Chapter N: Chapter M: Title" -> "Chapter M: Title"
    text = re.sub(r'Chapter\s+\d+\s*:\s*(Chapter\s+\d+)\s*:\s*', r'\1: ', text)
    # "Chapter N: Chapter M — Title" -> "Chapter M — Title"
    text = re.sub(r'Chapter\s+\d+\s*:\s*(Chapter\s+\d+)\s*[—–-]\s*', r'\1 — ', text)
    # Normalize spacing
    text = re.sub(r'(Chapter\s+\d+)\s*:\s*', r'\1: ', text)
    return text


def rebuild_spine(opf_text):
    """Rebuild spine from manifest — front first, then all ch*.xhtml in order."""
    manifest_match = re.search(r'<manifest>(.*?)</manifest>', opf_text, re.DOTALL)
    if not manifest_match:
        return opf_text
    
    items = re.findall(r'<item\s+id="([^"]+)"\s+href="([^"]+)"', manifest_match.group(1))
    
    spine_refs = []
    for item_id, href in items:
        if href == 'front.xhtml':
            spine_refs.append(item_id)
    for item_id, href in items:
        if re.match(r'ch\d+\.xhtml', href):
            spine_refs.append(item_id)
    
    spine_match = re.search(r'<spine[^>]*>(.*?)</spine>', opf_text, re.DOTALL)
    if not spine_match:
        return opf_text
    
    spine_tag = re.search(r'<spine([^>]*)>', spine_match.group(0))
    attrs = spine_tag.group(1) if spine_tag else ' toc="ncx"'
    
    new_spine = f'<spine{attrs}>\n'
    for ref in spine_refs:
        new_spine += f'    <itemref idref="{ref}"/>\n'
    new_spine += '  </spine>'
    
    return opf_text[:spine_match.start()] + new_spine + opf_text[spine_match.end():]


def rebuild_epub(source_path, output_path, images_dir, expected_chaps):
    """Rebuild EPUB with all fixes applied."""
    
    with zipfile.ZipFile(source_path, 'r') as zin:
        with zipfile.ZipFile(output_path, 'w') as zout:
            for item in zin.infolist():
                data = zin.read(item.filename)
                
                # 1. Replace images
                if item.filename.startswith("OEBPS/images/") and item.filename.endswith(".png"):
                    img_name = os.path.basename(item.filename)
                    new_img = os.path.join(images_dir, img_name)
                    if os.path.exists(new_img):
                        with open(new_img, 'rb') as f:
                            data = f.read()
                
                # 2. Fix OPF — rebuild broken spines
                if item.filename.endswith('.opf'):
                    opf = data.decode('utf-8')
                    
                    spine_match = re.search(r'<spine[^>]*>(.*?)</spine>', opf, re.DOTALL)
                    if spine_match:
                        spine_refs = re.findall(r'idref="([^"]+)"', spine_match.group(1))
                        has_image_refs = any('image' in ref.lower() for ref in spine_refs)
                        n_chaps = sum(1 for r in spine_refs if r.startswith('ch'))
                        
                        if has_image_refs or n_chaps < expected_chaps:
                            opf = rebuild_spine(opf)
                            print(f"  Rebuilt spine: {expected_chaps} chapters")
                    
                    data = opf.encode('utf-8')
                
                # 3. Fix text content
                if item.filename.endswith(('.xhtml', '.ncx')):
                    text = data.decode('utf-8')
                    original = text
                    text = fix_duplicate_chapter(text)
                    
                    # Add bodymatter landmark if missing
                    if item.filename.endswith('nav.xhtml') and 'bodymatter' not in text:
                        bm = '  <nav epub:type="landmarks">\n    <h2>Landmarks</h2>\n    <ol>\n      <li><a epub:type="bodymatter" href="ch01.xhtml">Start Reading</a></li>\n    </ol>\n  </nav>'
                        text = text.replace('</body>', bm + '\n</body>')
                    
                    if text != original:
                        data = text.encode('utf-8')
                
                zout.writestr(item, data)
    
    size_mb = os.path.getsize(output_path) / 1024 / 1024
    print(f"  Output: {output_path} ({size_mb:.1f} MB)")


if __name__ == "__main__":
    if len(sys.argv) != 5:
        print(f"Usage: {sys.argv[0]} <source_epub> <output_epub> <images_dir> <expected_chapters>")
        sys.exit(1)
    
    source, output, images, chaps = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4])
    rebuild_epub(source, output, images, chaps)
