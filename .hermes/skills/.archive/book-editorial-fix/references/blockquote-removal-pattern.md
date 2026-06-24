# Blockquote Removal Pattern

## When to Use
When a user asks to remove `>` symbols from a manuscript. These are Markdown blockquote markers that appear at the start of lines. They are distinct from `>` used within text body (e.g., `>25%`, `>80%`, `>500`) which must be preserved.

## Identification

```bash
# Count blockquote marker lines (lines starting with > after optional whitespace)
grep -c '^>' MANUSCRIPT.md
# Or more precisely:
grep -cP '^\s*>' MANUSCRIPT.md

# View them in context
grep -nP '^\s*>' MANUSCRIPT.md | head -20
```

Blockquote markers in manuscripts typically wrap:
- Chapter exercises (`**Chapter N Exercise: ...**`)
- "The One Thing" summary callouts
- Numbered/bulleted lists that were blockquoted instead of using proper list syntax
- Multi-line callout blocks with `>` on each line including empty `>` lines

## Precision Rules

| Pattern | Action | Why |
|---------|--------|-----|
| `^> text` | Remove `>` prefix | Blockquote marker |
| `^>` (empty, just `>`) | Remove entirely | Empty blockquote line |
| `>25%` or `> 3 branches` within body text | Keep | Content, not a blockquote |
| `>80%+` in scoring thresholds | Keep | Content |

**Critical:** Only remove `>` at the START of a line (after optional whitespace). Never do a global `s/>//g` — this destroys body text containing `>` characters.

## Removal Script

```python
import re

def remove_blockquotes(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
    
    lines = content.split('\n')
    modified = 0
    new_lines = []
    
    for line in lines:
        stripped = line.lstrip()
        if stripped.startswith('>'):
            # Remove leading > markers (handles nested >> and > >)
            new_line = re.sub(r'^(>\s*)+', '', line)
            new_lines.append(new_line)
            modified += 1
        else:
            new_lines.append(line)
    
    new_content = '\n'.join(new_lines)
    
    with open(filepath, 'w') as f:
        f.write(new_content)
    
    return modified

# Run on all manuscript files
import glob
for path in glob.glob('**/MANUSCRIPT.md', recursive=True):
    count = remove_blockquotes(path)
    if count > 0:
        print(f'{path}: removed {count} blockquote marker lines')
```

## Verify Completion

```bash
# Zero blockquote markers should remain
grep -cP '^\s*>' MANUSCRIPT.md
# Expected: 0

# But > within text should still exist
grep -c '>25%' MANUSCRIPT.md
# Expected: original count preserved
```

## Check for Multiple Copies

Manuscript files often exist in multiple locations that all need the same fix:

```bash
# Find all manuscript files
find /path/to/book -name "*MANUSCRIPT*.md" -o -name "*manuscript*.md"

# Common locations:
# - Book root: owner-s-manual-for-ai-agents_MANUSCRIPT.md
# - Manuscript subdirectory: manuscript/MANUSCRIPT.md
# - Series root: the-crisis-ready-company_MANUSCRIPT.md
```

## After Removal

Some blockquoted content may benefit from reformatting:
- **Numbered lists** that were `> 1.`, `> 2.`, `> 3.` → convert to proper Markdown numbered lists
- **"The One Thing" summaries** → leave as bold paragraphs (already formatted with `**`)
- **Exercise instructions** → leave as plain paragraphs
- **Sub-items** that were `>     -` → convert to proper indentation

The user may request: "replace some with bullets but most need to be removed" — handle case by case based on the content context.
