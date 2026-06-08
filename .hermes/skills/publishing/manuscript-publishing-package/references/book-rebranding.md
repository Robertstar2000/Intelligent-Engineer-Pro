# Book Rebranding Workflow

When the user chooses a different title/subtitle after the manuscript is written and packaged.

## When to Use

- User says "go with #4" after you proposed alternative titles
- User says "change the title to [new name]"
- A trademark conflict or market positioning shift requires a title change

## The Workflow

### 1. Update the Manuscript (markdown)

The compiled `manuscript.md` has the title in several places. Find them all:

```bash
grep -n "Old Title" manuscript.md
grep -ni "old title" manuscript.md
```

Places to check:
- Title page
- Subtitle
- Chapter titles that reference the old title concept
- Part titles
- TOC entries
- Copyright page
- Author bio / series page
- Body text using old title as a descriptive concept (keep these)

### 2. Update the EPUB Builder Script

Update constants:
```python
BOOK_KEY = "New_Key"
TITLE = "New Title"
SUBTITLE = "New Subtitle"
```

Also update `cover_path` and `BOOK_DIR`.

### 3. Update the Cover Artwork

Re-run typography overlay with new title text. Much faster than regenerating artwork.

### 4. Rebuild the EPUB and Package

```bash
python3 build_script.py
```

### 5. Verify the New Title is Clean

```python
import zipfile
with zipfile.ZipFile('book.epub') as z:
    for n in z.namelist():
        if 'Old' in z.read(n).decode(errors='ignore'):
            print(f'Old title found in: {n}')
```

### 6. Clean Up Old Files

```bash
rm -f /path/to/old_key.* /path/to/old_key_*.zip
```

Do not delete raw artwork until user confirms.

## Pitfalls

- **Font sizing** — longer/shorter title needs recalculated font size.
- **Cover filename** — update output path if using old key.
- **Subtitle length** — may need 2 lines instead of 1.
- **Part/chapter names** — if named after old title concept, rename.