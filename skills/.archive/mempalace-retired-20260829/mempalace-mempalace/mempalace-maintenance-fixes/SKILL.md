---
name: mempalace-maintenance-fixes
description: Fixes for common MemPalace maintenance script errors encountered in Hermes Agent sessions
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [mempalace, maintenance, fixes, datetime, pruning, embedding]
    related_skills: [mempalace-complete]
---

# MemPalace Maintenance Fixes

## Description
This skill captures common fixes for MemPalace maintenance scripts encountered during Hermes Agent sessions. It addresses import errors, missing attribute errors, and other issues that arise when running MemPalace procedures in isolated environments (e.g., cron jobs).

## Trigger Conditions
- Running MemPalace memory offload procedures (memory_offload.py, offload_memory.py) results in "name 'datetime' is not defined" errors.
- Running cron maintenance scripts (cron_maintenance_fixed.py) results in:
  - `'int' object has no attribute 'get'` when accessing prune_stats
  - `module 'embed' has no attribute '_INDEX'` when checking embedding system status
- General MemPalace script failures due to missing imports or incorrect variable types in isolated environments.

## Fixes

### 1. Datetime Import Error in Tag Module
**Symptom:**  
`name 'datetime' is not defined` when calling `tag.save_context_tags()` or similar tagging functions.

**Root Cause:**  
The `tag.py` module (or its dependencies) uses `datetime` and `timezone` without importing them in the relevant functions.

**Fix:**  
Ensure that the `tag.py` module imports `datetime` and `timezone` at the top of the file, or within the functions that use them:
```python
from datetime import datetime, timezone
```
Apply this fix to any function in `tag.py` that creates timestamps (e.g., `save_context_tags`, `save_palace_tags`).

### 2. Pruning Statistics Type Error
**Symptom:**  
`AttributeError: 'int' object has no attribute 'get'` when trying to access `prune_stats.get('kept', 0)`.

**Root Cause:**  
The `prune_memories()` function in `prune.py` returns an integer (count of pruned memories) instead of a dictionary with statistics.

**Fix:**  
Modify the cron maintenance script to handle the return value appropriately. If the function returns an integer, treat it as the count of pruned memories:
```python
pruned_count = prune.prune_memories(storage_path)
prune_stats = {'pruned': pruned_count, 'kept': 0}  # or however you want to interpret it
```
Alternatively, update `prune.py` to return a dictionary with statistics (preferred for consistency).

### 3. Embedding System Attribute Error
**Symptom:**  
`AttributeError: module 'embed' has no attribute '_INDEX'` when checking `embed._INDEX is not None`.

**Root Cause:**  
The `embed.py` module does not expose a `_INDEX` global variable, or it is named differently.

**Fix:**  
Check the actual attribute name in `embed.py`. Common alternatives include `_index`, `index`, or `faiss_index`. Update the check to use the correct attribute:
```python
# Example: if the attribute is named '_index'
embed_initialized = embed._index is not None
```
Inspect `embed.py` to confirm the correct attribute name for the FAISS index object.

### 4. General Import Reliability in Cron Jobs
**Best Practice:**  
When running MemPalace scripts in cron jobs or isolated environments:
1. Add the mempalace directory to `sys.path` at the script's start:
   ```python
   import sys, os
   sys.path.insert(0, os.path.expanduser('~/.hermes/mempalace'))
   ```
2. Use direct module imports instead of relative imports:
   ```python
   import capture
   import tag
   import embed
   # ... etc.
   ```
3. Initialize each component individually rather than relying on package-level initialization:
   ```python
   storage_path = os.path.expanduser('~/.hermes/mempalace')
   capture.init_capture(storage_path)
   tag.init_tagging(storage_path)
   embed.init_embedding(storage_path)
   # ... etc.
   ```

## Verification
After applying fixes, run the verification script:
```bash
python3 /home/bob/.hermes/mempalace/scripts/verify_mempalace.py
```
Expected output (with embedding dependencies missing):
```
Warning: MemPalace embedding dependencies not available: No module named 'sentence_transformers'
Embedding system initialized in mock mode (dependencies missing)
VERIFY_SUCCESS: index_vectors=<number>, search_results=0
```
With dependencies installed, search_results should return relevant memories.

## Prevention
- Add import verification to CI/linting checks for MemPalace modules.
- Test MemPalace scripts in an isolated environment (e.g., a Docker container mimicking the cron environment) before deploying to production.
- Keep a backup of known-working scripts before applying updates.

## References
- See `references/direct-module-import-workaround.md` for guidance on importing MemPalace modules in cron jobs.
- See `references/faiss-stale-vectors.md` for procedures for detecting and recovering from stale FAISS vectors.