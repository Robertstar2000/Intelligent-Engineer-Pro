# Batch Integration Pattern for Skills

## When to Use
When adding a consistent section across many skills (e.g., DOX Integration, MemPalace preamble, new workflow step).

## Approach

### 1. Identify Target Skills
```python
import os
skills_dir = os.path.expanduser("~/.hermes/skills")
categories = ["software-development", "github", "autonomous-ai-agents", "devops"]
for cat in categories:
    cat_dir = os.path.join(skills_dir, cat)
    for skill in sorted(os.listdir(cat_dir)):
        print(f"{cat}/{skill}")
```

### 2. For Each Skill, Find a Unique Anchor
Read the skill first, find a section heading that's unique enough to serve as the `old_string` anchor. Common anchors:
- `## Principles` → insert before it
- `## Common Pitfalls` → insert before it  
- `## Verification Checklist` → insert before it
- `## Save location` → insert before it

### 3. Use `skill_manage(action='patch')` for Enabled Skills
```python
skill_manage(
    action='patch',
    name='plan',
    old_string='## Principles',
    new_string='## DOX Integration\n\n...\n\n## Principles'
)
```

### 4. For Disabled Skills, Use `patch` Tool on Absolute Path
When `skill_view(name='...')` fails with "disabled":
```python
# Read the file directly
read_file(path='~/.hermes/skills/<category>/<name>/SKILL.md')

# Then use the patch tool on the absolute path
patch(mode='replace', path='~/.hermes/skills/<category>/<name>/SKILL.md',
      old_string='...', new_string='...')
```

### 5. For Batch Patching Many Files at Once
Use `mode='patch'` with V4A format for multi-file patches:
```
*** Begin Patch
*** Update File: /path/to/file1.md
@@ ## Some Section
+## New Section
+
+Content here
+
 ## Some Section
*** Update File: /path/to/file2.md
@@ ## Some Section
+## New Section
+
+Content here
+
 ## Some Section
*** End Patch
```

### 6. Verify After Patching
```python
with open(skill_md_path) as f:
    content = f.read()
assert "New Section" in content
assert "old_string" not in content  # If replacing
```

## Key Pitfalls
- `mode='replace'` uses `old_string`/`new_string` params
- `mode='patch'` uses the `patch` param with V4A format
- Do NOT mix these up
- Always verify the patch landed correctly — read the file back
- If `old_string` matches multiple locations, use `replace_all=True` or provide more context
