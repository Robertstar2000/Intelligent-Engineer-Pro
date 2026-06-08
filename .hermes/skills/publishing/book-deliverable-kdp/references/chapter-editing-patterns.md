# Chapter Editing Patterns — What to Look For

## Common Issues in AI-Generated or Multi-Draft Chapters

### 1. Duplicate Paragraphs
**Symptom**: Entire paragraphs appear twice, often far apart in the file.
**Cause**: AI generation stitching error, or copy-paste during drafting.
**Detection**: Extract all `<p...>...</p>`, clean HTML tags, compare text content. Any block >30 chars appearing more than once is a duplicate.
**Fix**: Keep first occurrence, remove all subsequent ones.
**Pitfall**: Removing a `</p>` tag that was shared with the following paragraph can break p-tag balance. Always verify after dedup.

### 2. Double Scene Breaks
**Symptom**: `<p class="scene">* * *</p><p class="scene">* * *</p>` appearing consecutively.
**Cause**: AI generating a scene break + transition heading in the same block.
**Fix**: Collapse two consecutive identical scene breaks into one. Run this BEFORE other edits.

### 3. Mixed Em-Dash Formats
**Symptom**: `&mdash;` HTML entities and unicode `—` both present in same file.
**Cause**: Some chapters written with HTML entities, others with direct unicode.
**Fix**: Normalize all `&mdash;` to unicode `—`. For spacing: use ` — ` (spaced) for narrative pauses, no spaces for compound words like "razor-thin".

### 4. Mismatched `<p>` Tags
**Symptom**: Count of `<p` tags doesn't match count of `</p>` tags.
**Causes**: (a) Duplicate paragraph removal stripping a `</p>`, (b) Malformed HTML from generation.
**Detection**: `len(re.findall(r'<p[\s>]', content))` vs `len(re.findall(r'</p>', content))`
**Fix**: Add missing `</p>` at end of the line that contains the unclosed `<p`.

### 5. Character Name Inconsistency
**Symptom**: Same character referred to by different last names across chapters.
**Detection**: Search for `FirstName\s+(\w+)` and check for multiple capitalized last names.
**Fix**: Establish canonical names in a character list. Search and replace variants.

## Recommended Editing Order

1. Fix double scene breaks (simple string replace)
2. Normalize em-dashes (`&mdash;` → `—`)
3. Remove duplicate paragraphs (regex dedup)
4. Fix p-tag mismatches (add missing `</p>`)
5. Run spell check on extracted text
6. Verify character name consistency
7. Read through for flow and coherence

## Automated Script

Use `scripts/cleanup-chapters.py` for steps 1-4 on a full directory of chapter files:
```
python3 scripts/cleanup-chapters.py manuscript_src/
```

After running the script, always do a manual read-through for flow, especially
checking that removing duplicates did not create abrupt transitions.
