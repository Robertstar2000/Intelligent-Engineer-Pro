#!/usr/bin/env python3
"""
Clean up chapter files for KDP publishing.
Fixes: duplicate paragraphs, double scene breaks, mixed em-dashes, p-tag mismatches.
Usage: python3 cleanup-chapters.py <manuscript_src_directory>
"""

import os, re, glob

def clean_chapter(filepath):
    with open(filepath) as f:
        content = f.read()
    
    original = content
    fixes = []
    
    # 1. Fix double scene breaks
    while '<p class="scene">* * *</p><p class="scene">* * *</p>' in content:
        content = content.replace(
            '<p class="scene">* * *</p><p class="scene">* * *</p>',
            '<p class="scene">* * *</p>'
        )
        fixes.append('double scene break')
    
    # 2. Normalize &mdash; to unicode em-dash
    if '&mdash;' in content:
        content = content.replace('&mdash;', '\u2014')
        fixes.append('normalized &mdash;')
    
    # 3. Remove duplicate paragraphs (>30 chars)
    paras = list(re.finditer(r'<p[^>]*>.*?</p>', content, re.DOTALL))
    para_info = [(m.start(), m.end(), m.group(0), 
                  re.sub(r'<[^>]+>', '', m.group(0)).strip()) for m in paras]
    seen = {}
    to_remove = []
    for start, end, raw, clean in para_info:
        if len(clean) > 30:
            if clean in seen:
                to_remove.append((start, end))
            else:
                seen[clean] = True
    for start, end in reversed(to_remove):
        content = content[:start] + content[end:]
        fixes.append(f'dup: "{para_info[0][3][:50]}"')
    
    # 4. Fix p-tag mismatch
    opens = len(re.findall(r'<p[\s>]', content))
    closes = len(re.findall(r'</p>', content))
    if opens > closes:
        diff = opens - closes
        content = content.rstrip() + '</p>' * diff
        fixes.append(f'added {diff} missing </p>')
    
    if content != original:
        with open(filepath, 'w') as f:
            f.write(content)
        return fixes
    return None


def main():
    import sys
    if len(sys.argv) < 2:
        print("Usage: python3 cleanup-chapters.py <manuscript_src_directory>")
        return
    
    src_dir = sys.argv[1]
    files = sorted(glob.glob(os.path.join(src_dir, "*.md")) + 
                   glob.glob(os.path.join(src_dir, "*.xhtml")))
    
    for fpath in files:
        fixes = clean_chapter(fpath)
        if fixes:
            print(f"  {os.path.basename(fpath)}: {', '.join(fixes)}")
    
    print("Done!")

if __name__ == "__main__":
    main()
