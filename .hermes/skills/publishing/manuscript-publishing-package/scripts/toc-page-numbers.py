#!/usr/bin/env python3
"""
Add TOC page numbers to a WeasyPrint HTML manuscript.

Usage: python3 toc-page-numbers.py manuscript.html [output.html]

This script:
1. Adds 'id' attributes to all chapter/part heading tags
2. Converts TOC entries from plain text to table rows with page-number cells
3. Injects CSS for automatic page numbers via target-counter

Pitfalls this script avoids:
- Float-based ::after on wrapped text (causes concatenation artifacts like "3217")
- Absolute positioning (places number on first line instead of last)
- Nested div structures that break WeasyPrint rendering
"""

import re, sys


def add_toc_page_numbers(html):
    """Add table-based TOC with reliable page numbers (no float/position issues)."""

    # ── 1. Add IDs to all part and chapter headings ──
    heading_ids = {}

    # Part headings: <h1 class="part-title">Part One: The Ignition</h1>
    for m in re.finditer(
        r'<(h[12]\s+class="[^"]*part-title[^"]*")>(Part\s+\w+:\s+.*?)</(h[12])>',
        html, re.IGNORECASE,
    ):
        tag_open, text, tag_close = m.group(1), m.group(2), m.group(3)
        hid = _make_id(text)
        heading_ids[text] = hid
        html = html.replace(f'<{tag_open}>{text}</{tag_close}>',
                            f'<{tag_open} id="{hid}">{text}</{tag_close}>')

    # Chapter headings: <h2 class="chapter-title">Chapter One: The Shock</h2>
    for m in re.finditer(
        r'<(h[12]\s+class="[^"]*chapter-title[^"]*")>(Chapter\s+\w+:\s+.*?)</(h[12])>',
        html, re.IGNORECASE,
    ):
        tag_open, text, tag_close = m.group(1), m.group(2), m.group(3)
        hid = _make_id(text)
        heading_ids[text] = hid
        html = html.replace(f'<{tag_open}>{text}</{tag_close}>',
                            f'<{tag_open} id="{hid}">{text}</{tag_close}>')

    print(f"  Found {sum(1 for k in heading_ids if k.startswith('Part'))} parts, "
          f"{sum(1 for k in heading_ids if k.startswith('Chapter'))} chapters")

    # ── 2. Remove any existing TOC - we'll rebuild it ──
    toc_start = html.find('<div class="toc">')
    if toc_start >= 0:
        # Read the TOC entries (all <p> or <tr> elements inside)
        toc_end = html.find('</div>', toc_start)
        toc_end = html.find('</div>', toc_end + 1)  # closing </div> for .toc

        # Extract entries by finding the toc-label text
        old_toc = html[toc_start:toc_end + 6]
        toc_entries = []

        # Parse both <p class="toc-row"> and <tr class="toc-row"> formats
        entry_pattern = re.compile(
            r'<t[dh][^>]*class="[^"]*toc-label[^"]*"[^>]*>(Part\s+\w+:\s+.*?|Chapter\s+\w+:\s+.*?)</t[dh]>',
            re.IGNORECASE,
        )
        for m in entry_pattern.finditer(old_toc):
            text = m.group(1).strip()
            # Determine if part or chapter
            if text.startswith('Part '):
                toc_entries.append(('part', text))
            else:
                toc_entries.append(('ch', text))

        if not toc_entries:
            # Fall back to text-based parsing for simpler TOC structures
            for line in old_toc.split('\n'):
                stripped = line.strip()
                for prefix, etype in [('Part ', 'part'), ('Chapter ', 'ch')]:
                    if stripped.startswith(prefix) and ':' in stripped:
                        toc_entries.append((etype, stripped.split('</a>')[0]
                                           .split('>')[-1].strip()))
                        break
        print(f"  Parsed {len(toc_entries)} TOC entries")
    else:
        print("  WARNING: No .toc div found in HTML — check TOC structure")
        return html

    # ── 3. Rebuild TOC as a TABLE for reliable column alignment ──
    css_class = {'part': 'toc-row part', 'ch': 'toc-row chapter'}
    rows = []
    for etype, text in toc_entries:
        hid = heading_ids.get(text, _make_id(text))
        rows.append(
            f'<tr class="{css_class[etype]}">'
            f'<td class="toc-label">{text}</td>'
            f'<td class="toc-page"><a href="#{hid}"></a></td>'
            f'</tr>'
        )

    new_toc = (
        '<div class="toc">\n<h2>Table of Contents</h2>\n'
        '<table class="toc-table"><tbody>\n' +
        '\n'.join(rows) +
        '\n</tbody></table>\n</div>'
    )

    html = html.replace(old_toc, new_toc)

    # ── 4. Inject table-based TOC CSS ──
    toc_css = '''
/* TOC table — each row is independent; wrapped labels don't affect page-number column */
.toc-table {
    width: 100%;
    border-collapse: collapse;
}
.toc-table tr { vertical-align: baseline; }
.toc-table td {
    border: none;
    padding: 2px 0;
    font-size: 10pt;
    line-height: 1.3;
}
.toc-table .toc-label { text-align: left; white-space: normal; }
.toc-table .toc-page {
    text-align: right;
    white-space: nowrap;
    padding-left: 12px;
    color: #555;
    font-size: 10pt;
    width: 1%;
}
.toc-table .toc-page a { text-decoration: none; color: #555; }
.toc-table .toc-page a::after { content: target-counter(attr(href url), page); }
.toc-table tr.part .toc-label { font-weight: bold; font-size: 10.5pt; padding-top: 8px; }
.toc-table tr.part .toc-page { font-weight: bold; padding-top: 8px; }
.toc-table tr.chapter .toc-label { padding-left: 15px; }
'''

    html = html.replace('</style>', toc_css + '\n</style>')

    return html


def _make_id(text):
    """Generate a clean URL-safe ID from heading text."""
    hid = text.lower().replace(' ', '-').replace(':', '')
    hid = re.sub(r'[^a-z0-9-]', '', hid)
    # Trim to 40 chars max to avoid WeasyPrint internal-link issues
    return hid[:40]


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 toc-page-numbers.py input.html [output.html]")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else input_path

    with open(input_path) as f:
        html = f.read()

    html = add_toc_page_numbers(html)

    with open(output_path, 'w') as f:
        f.write(html)

    print(f"Done. TOC uses table layout — no float/position artifacts.")
