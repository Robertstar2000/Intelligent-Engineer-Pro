# EPUB Generation Pitfalls — Lessons from Cindy Lou Condensation (2026-06-03)

## Critical: `&nbsp;` Not Valid in XHTML/EPUB

**Symptom:** Every chapter shows: `Entity 'nbsp' not defined`

**Fix:** In `md_to_html_simple()`, first line of loop:
```python
line = line.replace('&nbsp;', '&#160;')
```

## Chapter Title Duplication in TOC

**Symptom:** "Chapter 4: Chapter 4" instead of "Chapter 4: The Sister's Plea"

**Fix:** Strip `Chapter N:` prefix from extracted titles:
```python
title = re.sub(r'^Chapter\s+\d+:\s*', '', title)
```

## Title Appears as Body Text

**Symptom:** Title in both `<h2>` AND first `<p>`.

**Fix:** Strip title line in EPUB generation before `md_to_html_simple()`.

## Python `.pyc` Cache

**Fix:** `find /path/ -name "__pycache__" -type d -exec rm -rf {} +`

## Page Targets (6x9")

150-190 pages = 37,500-51,000 words. Condensation ratio: ~60-65% reduction from original.

## Subagent Timeout

Use 2-3 chapters per subagent max, or execute directly.
