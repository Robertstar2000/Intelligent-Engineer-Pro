# HTML Heading Formats for Chapter Detection

When building EPUBs from HTML manuscripts across a multi-book series, chapters may use 4+ different HTML patterns. The EPUB builder must detect all of them.

## Four Formats Found in Production

### Format 1: `<h2>` Chapter (Book 1)
```html
<h2>Chapter 1 — The Descent Window</h2>
```
Simple `<h2>` tag. Detected by: `<h2>Chapter N — Title</h2>`

### Format 2: `<h1 class="chapter-title">` (Book 2)
```html
<h1 class="chapter-title" id="ch1">Chapter 1 — The Salvage Accords</h1>
```
Uses `<h1>` with a CSS class and HTML `id` attribute. Detected by: `<h1[^>]*>Chapter ...</h1>`

### Format 3: `<h1>` with `&mdash;` (Books 4–5)
```html
<h1>Chapter 1 &mdash; The Artemis Accord</h1>
```
Plain `<h1>` with `&mdash;` entity for the dash separator. Detected by: `<h1>Chapter ...</h1>`

### Format 4: `<div id="chN"><h1>` wrapper (Books 6–8)
```html
<div id="ch0"><h1>Chapter 1 — The Observatory Rising</h1></div>
<div id="ch1"><h1>Chapter 2</h1></div>
<div id="ch2"><h1>Chapter 2 — Volcanic History Revealed</h1></div>
```
Some editions show CHAPTER NUMBER ONLY on one div (no title text), followed by a second div with the full chapter title. Both are chapters. Detected by: `<div id="chN"...><h1>Chapter ...</h1></div>`

## Unified Detection Regex

```python
import re

chapter_pattern = re.compile(
    r'(<h[12][^>]*>(?:Chapter|PART)\s[^<]+</h[12]>)|'         # Formats 1, 2, 3
    r'(<div\s+id="ch\d+"[^>]*>\s*<h[12][^>]*>(?:Chapter|PART)\s[^<]+</h[12]>\s*</div>)',  # Format 4
    re.DOTALL | re.IGNORECASE
)

chapters = []
chapter_positions = []
for m in chapter_pattern.finditer(body_html):
    ch_text = re.sub(r'<[^>]+>', '', m.group(0)).strip()
    ch_text = ch_text.replace('&mdash;', '—').replace('&nbsp;', ' ')
    ch_text = re.sub(r'\s+', ' ', ch_text).strip()
    chapters.append(ch_text)
    chapter_positions.append(m.start())
```

## Content Splitting

Once positions are found, split the body into per-chapter sections:

```python
sections = []
for i, pos in enumerate(chapter_positions):
    end_pos = chapter_positions[i+1] if i+1 < len(chapter_positions) else len(body)
    sections.append((chapters[i], body[pos:end_pos].strip()))
```

## Pitfalls

- **Heading in TOC area**: The TOC section often has `<h2>Contents</h2>` or `<h1>Table of Contents</h1>` — these look like headings but aren't chapters. The regex above avoids them by requiring "Chapter" or "PART" in the heading text.
- **Duplicate nav entries for part dividers**: PART headers (`PART I — THREE SHIPS, ONE PLAIN`) create TOC entries but don't need their own chapter file. Handle by checking if the heading starts with "PART" vs "Chapter".
- **Chapter-only-number entries**: Some HTML has `<div id="ch1"><h1>Chapter 2</h1></div>` followed by `<div id="ch2"><h1>Chapter 2 — Volcanic History Revealed</h1></div>`. The first div has no title text. Both are chapters — include both in the TOC.
- **&mdash; vs — vs --**: Different HTML sources use different dash characters. Normalize all to `—` (em dash) after extraction for clean TOC display.
