# React SPA JSX Fragment Text Replacement

When modifying text in compiled Vite/React bundles, text is stored as JSX-compiled function calls, not plain HTML. Understanding the structure is critical for reliable replacements.

## Text Storage Patterns in Minified JSX

### Simple strings (no formatting)
Plain text content like "Bookstore" or "Buy AI Solutions" appears as:
```js
l.jsx("li",{children:"✦AI That Works for Small Business"})
```
These can be replaced with simple string find-and-replace.

### Strings with HTML formatting
Text containing `<strong>`, `<em>`, `<br/>`, or other inline elements is stored as **arrays**:
```js
// ✦ **Built from Dust** — Published on Kindle
l.jsxs("li",{children:["✦ ",l.jsx("strong",{children:"Built from Dust"})," — Published on Kindle"]})
```
Here `l.jsxs` (plural) creates a fragment with children array. The `**` bold syntax becomes a nested `l.jsx("strong",...)` call.

**These CANNOT be found with simple string search** — you must match the entire JSX fragment.

## Workflow for Complex Replacements

### 1. Download the bundle
```bash
curl -s "https://www.mifeco.com/" | grep -oP 'src="/assets/index-[^\\"]+\.js"'
curl -s "https://www.mifeco.com/assets/index-HASH.js" -o /tmp/bundle.js
```

### 2. Find the exact JSX fragment with grep
Use grep with surrounding context to capture the full function call:
```bash
grep -oP 'l\.jsxs\("li",\{children:\[\"✦.{0,200}' /tmp/bundle.js
```

### 3. Write a Python replacement script to /tmp/
Use `write_file` to create the script, then run it via `terminal`:
```python
with open('/tmp/bundle.js') as f:
    js = f.read()

# Replace plain strings directly
js = js.replace('"Old Plain Text"', '"New Plain Text"')

# Replace JSX fragments with the exact match
old = 'l.jsxs("li",{children:["✦ ",l.jsx("strong",{children:"Built from Dust"})," — Published on Kindle"]})'
new = 'l.jsx("li",{children:"— Published on Kindle"})'
js = js.replace(old, new)

with open('/tmp/bundle.js', 'w') as f:
    f.write(js)
```

### 4. CRITICAL: Verify brace/paren balance
```python
c = open('/tmp/bundle.js').read()
print(f"Braces: {c.count('{')} == {c.count('}')} → {'OK' if c.count('{')==c.count('}') else 'MISMATCH'}")
print(f"Parens: {c.count('(')} vs {c.count(')')} → {'OK' if abs(c.count('(')-c.count(')'))<=1 else 'MISMATCH'}")
```

### 5. Upload and verify immediately
```bash
scp /tmp/bundle.js dh_mwpxuu@iad1-shared-b8-42.dreamhost.com:/home/dh_mwpxuu/mifeco.com/assets/index-HASH.js
curl -s "https://mifeco.com/" | grep "Your New Text"
```

## Common Pitfalls

- **CSS class changes VS text changes:** Text changes in `children:"..."` fields are safe. CSS class changes in `className:"..."` fields may break layout. Prefer text-only changes when source isn't available.
- **Unicode characters:** The ✦ character (U+2726) and em dash (U+2014) are stored literally in the JS file. Use Python's unicode escapes or paste the actual characters.
- **Substring matching:** If "Business Books" is in the string "Business Books & Memoir", replacing "Business Books" will produce "The Crisis Ready Company & Memoir". Always use **full exact string** matches.
- **Parallel replacements:** Replace the most specific strings first, then more general ones, to avoid partial-match corruption.
- **Ampersand in heredocs:** Python code containing `&` character must be written to a file first, not passed inline via heredoc (shell interprets `&` as backgrounding).