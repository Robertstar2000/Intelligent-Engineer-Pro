"""Per-chapter word count analysis for book HTML files.
Use this when planning content redistribution across book volumes.

Usage:
    python3 chapter-word-count-analyzer.py <path_to_book.html> [--target WORDS]
"""

import re
import sys

def analyze_book(path, target_per_chapter=None):
    with open(path) as f:
        html = f.read()

    # Try multiple chapter detection patterns
    ch_patterns = [
        (r'<h1 class="chapter-title"[^>]*>(.*?)</h1>', 'h1.chapter-title'),
        (r'<h2>Chapter (\d+)[^<]*</h2>', 'h2>Chapter'),
        (r'<h1>Chapter (\d+)[^<]*</h1>', 'h1>Chapter'),
    ]

    chapters = []
    for pattern, label in ch_patterns:
        matches = list(re.finditer(pattern, html, re.DOTALL))
        if len(matches) >= 3:
            for i, m in enumerate(matches):
                start = m.end()
                end = matches[i+1].start() if i+1 < len(matches) else len(html)
                section = html[start:end]
                text = re.sub(r'<[^>]+>', ' ', section)
                words = len(text.split())
                title = re.sub(r'<[^>]+>', '', m.group(1)).strip()[:50]
                chapters.append((title, words))
            break

    if not chapters:
        print(f"No chapters detected in {path}")
        return

    total = sum(c[1] for c in chapters)
    print(f"  Book: {path}")
    print(f"  Chapters detected: {len(chapters)}")
    print(f"  Total words: {total}")
    print(f"  Est. pages (220 wpp): {total/220:.0f}")
    print()

    for title, words in chapters:
        marker = " ***" if target_per_chapter and words < target_per_chapter * 0.8 else ""
        print(f"    {title}: {words} words{marker}")

    if target_per_chapter:
        print(f"\n  Target per chapter: {target_per_chapter}")
        print(f"  Chapters below 80% of target: {sum(1 for _,w in chapters if w < target_per_chapter*0.8)}")
        needed = (target_per_chapter * len(chapters)) - total
        print(f"  Additional words needed: {needed} ({needed/total*100:.0f}%)")


if __name__ == '__main__':
    target = None
    paths = [a for a in sys.argv[1:] if not a.startswith('--target=')]
    for a in sys.argv[1:]:
        if a.startswith('--target='):
            target = int(a.split('=')[1])

    for path in paths:
        analyze_book(path, target)
        print()
