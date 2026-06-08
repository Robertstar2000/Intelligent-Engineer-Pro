# Character Name Standardization Across a Series

When an existing multi-volume series uses AI-typical character names (Elena, Diego, Mei-Lin, Rajiv, Jean-Luc, Aisha, Ana, Kenji) and needs to retrofit all first names to top-50 US names, use this systematic approach.

## Technique Overview

The challenge is doing a safe find-and-replace across 10+ files (manuscripts, HTML, character docs, concept docs, chapter fragment files) without:
- Hitting false positives from substrings (e.g., "Ana" in "analysis", "manage")
- Missing compound names (e.g., "Mei-Lin" when also need to handle standalone "Mei")
- Creating inconsistent surnames across books (e.g., "Vargas" in Book 1, "Vasquez" in Book 3)
- Forgetting cross-references (author bios, About-the-Series sections in other volumes)

## Step-by-Step

### 1. Build the Character Roster First

Use `delegate_task` to scan all manuscripts and produce a complete roster showing every named character, their gender, role, and which books they appear in. Include supporting/minor characters.

Output format:
```
| # | Name | Full Name | Gender | Books | Role |
|---|------|-----------|--------|-------|------|
| 1 | Elena | Elena Vasquez | F | 1,2,3 | Commander |
```

Note: The same character may have different surnames across books (Vargas→Vasquez). Document this.

### 2. Define the Replacement Mapping

Map each old first name → new top-50 US name. Use the SSA top 50 lists:

**Male**: James, Robert, John, Michael, David, William, Richard, Joseph, Thomas, Christopher, Charles, Daniel, Matthew, Anthony, Mark, Steven, Paul, Andrew, Joshua, Kenneth, Kevin, Brian, George, Timothy, Ronald, Edward, Jason, Jeffrey, Ryan, Jacob, Gary, Nicholas, Eric, Jonathan, Stephen, Larry, Justin, Scott, Brandon, Benjamin, Samuel, Raymond, Gregory, Frank, Alexander, Patrick, Jack, Dennis, Jerry

**Female**: Mary, Patricia, Jennifer, Linda, Barbara, Elizabeth, Susan, Jessica, Sarah, Karen, Lisa, Nancy, Betty, Margaret, Sandra, Ashley, Dorothy, Kimberly, Emily, Donna, Michelle, Carol, Amanda, Melissa, Deborah, Stephanie, Rebecca, Sharon, Laura, Cynthia, Kathleen, Amy, Angela, Shirley, Anna, Brenda, Pamela, Emma, Nicole, Helen, Samantha, Katherine, Christine, Debra, Rachel, Carolyn, Janet, Catherine, Maria, Heather

Keep names already in the top 50 (e.g., James, Sarah) unchanged.

### 3. Build Two Replacement Strategies

For safe multi-file replacement, use TWO mappings in order:

**Step A — Compound/full-name mappings** (run first, in longest-to-shortest order):
```python
compound = {
    "Elena Vasquez": "Margaret Vasquez",  # full name
    "Elena Vargas": "Margaret Vasquez",   # old surname variant
    "Raj Patel": "Robert Patel",          # Book 3 short form
    "Rajiv Patel": "Robert Patel",        # Books 1-2 long form
    "Mei-Lin Chen": "Elizabeth Chen",
    "Mei Lin": "Elizabeth Chen",          # space-separated variant
    "Jean-Luc Dubois": "Christopher Dubois",
    "Jean-Luc Bernard": "Christopher Dubois",
    "Ana Mikhailova": "Barbara Mikhailova",
    "Ana Reyes": "Barbara Reyes",         # separate character, same first name
}
```

**Step B — Standalone first-name mappings** (run second, after compound replacements consumed the full names):
```python
standalone = {
    "Elena": "Margaret",
    "Rajiv": "Robert",
    "Raj": "Robert",   # Book 3 short form
    "Mei": "Elizabeth",
    "Jean-Luc": "Christopher",
    "Ana": "Barbara",
    "Diego": "Michael",
    "Aisha": "Susan",
    "Kenji": "Richard",
    "Marcus": "David",
    "Yuki": "Patricia",
}
```

### 4. Use Python with Word-Boundary Regex

Do NOT use simple string `.replace()` — it hits false positives. Use `re.sub()` with `\b` word boundaries:

```python
import re
for old, new in sorted(compound.items(), key=lambda x: -len(x[0])):
    pattern = r'\b' + re.escape(old) + r'\b'
    content = re.sub(pattern, new, content)

for old, new in sorted(standalone.items(), key=lambda x: -len(x[0])):
    pattern = r'\b' + re.escape(old) + r'\b'
    content = re.sub(pattern, new, content)
```

Sorting by descending length ensures "Mei-Lin Chen" is matched before "Mei-Lin", which is matched before "Mei". Without this, `\bMei\b` would match inside "Mei-Lin" before the compound could be consumed.

### 5. Files to Cover

Replace names in ALL of these across the series:

- `manuscript.md` (each book)
- `Book_X_Title.html` (each book's HTML output — includes `<title>`, `<h1>`, author bio, about-the-series)
- `chapters_XX_YY.md` (chapter fragment files, if any — they often have a `# Title — Book N of Series` header)
- `*characters*.md` (character roster docs)
- `*concept*.md` (concept/planning docs)
- `*outline*.md` (chapter outlines)
- `all_characters_across_books.md` (consolidated roster, if it exists)

### 6. Standardize Surnames

If the same character has different surnames across books (Vargas→Vasquez, Bernard→Dubois, Lin→Chen), pick one canonical surname and apply it consistently. The compound mappings above handle this naturally — map both old variants to the same new full name.

### 7. Verify Zero Stragglers

After replacement, run a word-boundary search for every old name across the ENTIRE series directory:

```python
search_files(path='/books/Series/', pattern=r'\bElena\b')
```

Every count should be 0. The most commonly missed files are:
- Chapter fragment files (`chapters_01_10.md` etc.)
- Character/concept docs for Book 3 that reference Book 1's old name
- Author bio lines in HTML files (book N's HTML mentions "author of the [Series] series")
- Old PDFs that were not regenerated

### 8. Regenerate All PDFs

After all text replacements in the HTML, regenerate every book's PDF:

```bash
python3 -m weasyprint Book_X.html Book_X.pdf
pdfinfo Book_X.pdf | grep Pages
```

### 9. Update Memory

Add a memory entry listing the new character names so future sessions don't propose reverting:

```python
memory(action='add', target='memory',
    content='The [Series] series uses: Margaret Vasquez, Elizabeth Chen, Robert Patel, ...')
```

## Pitfalls

| Pitfall | Why It Happens | Avoidance |
|---------|---------------|-----------|
| **"Raj" matched inside "Rajiv"** | Simple `\bRaj\b` matches at the start of "Rajiv" since `\b` is between R and a | Replace "Rajiv" → "Robert" FIRST (compound mapping), then "Raj" → "Robert" only in books where the character is just "Raj" (Book 3). Or use compound mappings that always include full names. |
| **"Ana" matched in "analysis", "manage"** | `search_files` reports false positives from substrings | Always use word-boundary: `\bAna\b`. Search without boundaries for initial pass, then confirm with boundaries. |
| **Missed author bios in other volumes** | Only the renamed book's author bio gets updated | The "author of the [Series] series" line appears in EVERY volume's HTML. Update all of them. |
| **Old PDF still served after rename** | Only regenerated the HTML, forgot to rebuild PDF | Always regenerate PDFs after any text change in the HTML. Add `pdfinfo` check to verify. |
| **Surname mismatch after rename** | Character named "Elena Vargas" in Book 1, "Elena Vasquez" in Book 3 | Compound mapping from both variants to the same canonical full name handles this. |
| **"Mei" matched inside "Mei-Lin"** | `\bMei\b` matches the "Mei" part of "Mei-Lin" before the compound is consumed | Sort mappings by descending key length: "Mei-Lin Chen" > "Mei-Lin" > "Mei". Replace long patterns first. |
