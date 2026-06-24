# Tool Backgrounding Pitfalls

## `terminal()` Interprets `&` as Backgrounding

The `terminal()` tool treats `&` as a shell backgrounding operator. Any command containing `&` — even inside a heredoc — triggers:
```
"Foreground command uses '&' backgrounding. Use terminal(background=true) for long-lived processes..."
```

### What triggers it
- HTML content with `&amp;`, `&mdash;`, `&ndash;`, `&quot;`
- Text containing "A & B" or "X and Y & Z"
- URLs with query parameters: `?a=1&b=2`
- Even inside a `<< 'PYEOF'` heredoc — the tool scans the command string before passing to shell

### What doesn't trigger it
- `&` inside a file that's being *read* (not in the command string itself)
- `&` in `write_file` content (the tool writes directly, not via shell)

### Workaround
Use `write_file` to write content containing `&` to `/tmp/`, then operate on the file:
```python
write_file('/tmp/blog-content-slug.html', html_content)
scp_upload('/tmp/blog-content-slug.html', '/home/dh_mwpxuu/mifeco.com/tmp/slug.html')
```

This is the preferred pattern for writing blog post HTML anyway — it's faster and more reliable than heredoc for large content blocks.

### When to use `terminal()` heredoc
Only for Python scripts and shell commands that don't contain `&`. Python scripts rarely need raw `&`, so `terminal("python3 << 'PYEOF'")` is safe for:
- SSH/SCP operations
- JSON file manipulation
- MySQL queries through SSH
- Image generation commands

## `write_file` Corrupts `***`

The `write_file` tool silently corrupts lines containing `***` (triple asterisks). Use `terminal("python3 << 'PYEOF'")` heredoc for any content that might contain `***` (e.g., Python scripts that read passwords from `.env` via subprocess).
