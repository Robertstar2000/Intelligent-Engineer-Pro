# Import Verification Best Practices for MemPalace

When working with MemPalace modules, especially in cron jobs or isolated environments, it's critical to verify imports and function names to avoid runtime errors.

## Common Import Issues

### 1. Incorrect Function Names
MemPalace modules don't always export functions with intuitive names. Always verify before importing:

**Incorrect:**
```python
from mempalace.reinforce import mark_reinforcement  # Wrong function name
from mempalace.prune import prune_events            # Wrong function name
```

**Correct:**
```python
from mempalace.reinforce import reinforce_memory    # Actual function name
from mempalace.prune import prune_memories          # Actual function name
```

### 2. Module-Level vs Package-Level Imports
In isolated environments, package-relative imports may fail:

**May fail in cron jobs:**
```python
from mempalace.tag import extract_context_tags
```

**More reliable:**
```python
import tag  # After adding mempalace directory to sys.path
tag.extract_context_tags(content)
```

## Verification Steps

Before using any MemPalace module in production code:

1. **Check exported functions:**
   ```bash
   grep "^def " /path/to/mempalace/module.py
   ```

2. **Verify imports work in isolation:**
   ```python
   import sys
   sys.path.insert(0, '/home/bob/.hermes/mempalace')
   import module_name
   # Test that expected functions exist
   assert hasattr(module_name, 'expected_function_name')
   ```

3. **Test initialization:**
   ```python
   module_name.init_function(storage_path)
   ```

## Recommended Import Pattern for Cron Jobs

```python
import sys, os
sys.path.insert(0, os.path.expanduser('~/.hermes/mempalace'))

# Import modules directly
import capture
import tag
import score
import consolidate
import retrieve
import reinforce
import prune
import explain
import embed

# Initialize each component
storage_path = os.path.expanduser('~/.hermes/mempalace')
capture.init_capture(storage_path)
tag.init_tagging(storage_path)
score.init_scoring(storage_path)
consolidate.init_consolidation(storage_path)
retrieve.init_retrieval(storage_path)
reinforce.init_reinforcement(storage_path)
prune.init_pruning(storage_path)
explain.init_explainability(storage_path)
embed.init_embedding(storage_path)

# Now use the functions
event_id = capture.capture_event(event_data)
```

## Troubleshooting Import Errors

If you encounter `ImportError` or `AttributeError`:

1. **Check sys.path**: Ensure the mempalace directory is in Python's path
2. **Verify module exists**: Check that the .py file exists in the expected location
3. **Check function names**: Use `grep "^def " module.py` to see actual exported functions
4. **Look for circular imports**: Avoid modules importing each other in complex ways
5. **Check initialization order**: Some modules may depend on others being initialized first

By following these practices, you can avoid common import-related issues when deploying MemPalace in production environments, especially in cron jobs and isolated contexts.