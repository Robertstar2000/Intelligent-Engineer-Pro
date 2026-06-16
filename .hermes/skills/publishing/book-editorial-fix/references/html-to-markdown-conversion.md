# HTML-to-Markdown Conversion Patterns

## Common HTML Patterns in Corrupted Manuscripts

### Header Conversion
| HTML | Markdown | Notes |
|------|----------|-------|
| `<h1>Chapter X — Title</h1>` | `# Chapter X — Title` | Remove `<h1>` tags |
| `<h2>Chapter X — Title</h2>` | `## Chapter X — Title` | Standard for chapter headers |
| `<h1>Title</h1>` | `# Title` | For front matter |

### Paragraph Conversion
| HTML | Markdown | Notes |
|------|----------|-------|
| `<p class="first-para">text</p>` | `text` | Remove class, keep content |
| `<p class="scene">***</p>` | `***` | Convert to scene break |
| `<p class="scene">\*\*\*</p>` | `***` | Normalize scene breaks |
| `<p>text</p>` | `text` | Strip tags |
| `</p></p>` | `\n\n` | Double close = paragraph break |
| `</p><p>` | `\n\n` | Adjacent paragraphs |
| `<p>\s*</p>` | `\n\n` | Empty paragraphs |

### Image Handling
| HTML | Markdown | Notes |
|------|----------|-------|
| `<img src="chapter_images/ch01.png">` | `![](chapter_images/ch01.png)` | Keep relative paths |
| `<img src="..." class="...">` | `![](...)` | Strip class |

### Entity Conversion
| HTML Entity | Markdown |
|-------------|----------|
| `&rsquo;` | `'` (right single quote) |
| `&ldquo;` | `"` (left double quote) |
| `&rdquo;` | `"` (right double quote) |
| `&mdash;` | `—` (em dash) |
| `&ndash;` | `–` (en dash) |
| `&nbsp;` | ` ` (space) |
| `&amp;` | `&` |
| `&lt;` | `<` |
| `&gt;` | `>` |

## Image Filename Mapping Pitfall

**Problem:** Chapter numbers in manuscript (e.g., 31-60) don't match image files (01-30).

**Solution:** Map systematically:
```bash
# For chapters 31-60 with images 01-30:
# ch32.png → ch01.png, ch33.png → ch02.png, etc.
# Formula: new_num = old_num - 31
```

Always verify image files exist:
```bash
ls chapter_images/ch*.png | wc -l  # Should match chapter count
grep -c 'chapter_images/ch' MANUSCRIPT.md  # Should match
```

## Duplicate H1 Header Artifact

**Cause:** HTML `<h1>Chapter X</h1>` followed by markdown `## Chapter X` in source.

**Fix:** Remove standalone H1 headers that duplicate H2:
```python
# Pattern: \n## Chapter X — Title\n\n# Chapter X — Title\n\n
# Keep only the H2 version
content = re.sub(r'(## Chapter \d+ — .+)\n\n# Chapter \d+ — .+\n\n', r'\1\n\n', content)
```

## TOC Formatting Consistency

**Problem:** Mixed formats in Table of Contents
- `Chapter 17: Title` (colon)
- `Chapter 17 — Title` (em-dash)

**Fix:** Standardize to em-dash:
```bash
# In TOC: "Chapter 17: Title" → "Chapter 17 — Title"
# In body headers: "# Chapter 17: Title" → "# Chapter 17 — Title"
sed -i 's/\(Chapter [0-9]*\): \(.*\)/\1 — \2/' MANUSCRIPT.md
```

## Chapter Header Format Detection

Different series use different formats:

| Series | Format | Regex |
|--------|--------|-------|
| AoLS, NBS, LF | `# Chapter X — Title` | `^# Chapter \d+ —` |
| CLLC | `## Chapter X: Title` | `^## Chapter \d+:` |
| Memoir | `## Chapter One: Title` | `^## Chapter (One|Two|Three)` |

Always detect format before adding image placeholders or fixing TOC.