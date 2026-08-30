# MemPalace Dependency Installation — Session Notes

## June 2026 Installation Session

### Environment
- Hermes Agent venv: `/home/bob/.hermes/hermes-agent/venv/`
- Python: 3.11.15 (via uv)
- pip: 24.0 (use `pip3` not `pip` — `pip` binary doesn't exist, only `pip3` and `pip3.11`)

### Packages Installed (in order)

```bash
# 1. numpy (already present as dependency of other packages)
/home/bob/.hermes/hermes-agent/venv/bin/pip3 install numpy

# 2. faiss-cpu (pulls numpy as dep)
/home/bob/.hermes/hermes-agent/venv/bin/pip3 install faiss-cpu

# 3. torch CPU (MUST use CPU index URL — default download is 2GB+ with CUDA)
/home/bob/.hermes/hermes-agent/venv/bin/pip3 install torch \
  --index-url https://download.pytorch.org/whl/cpu \
  --no-cache-dir --timeout 600 --retries 5

# 4. sentence-transformers (600MB+ download — needs extended timeout)
/home/bob/.hermes/hermes-agent/venv/bin/pip3 install sentence-transformers \
  --no-cache-dir --timeout 600 --retries 5
```

### Versions Confirmed Working
- numpy: 2.4.6
- faiss-cpu: 1.14.3
- torch: 2.12.1+cpu
- sentence-transformers: 5.6.0
- transformers: 5.12.1
- scikit-learn: 1.9.0

### Package Importability Fix
The `mempalace` package wasn't importable as `import mempalace` because the parent directory wasn't on `sys.path`. Fixed with:
```bash
echo "/home/bob/.hermes" > /home/bob/.hermes/hermes-agent/venv/lib/python3.11/site-packages/mempalace.pth
```
**Critical**: Point to parent dir (`~/.hermes`), NOT the package dir (`~/.hermes/mempalace`).

### Bugs Fixed During Session
1. **`__init__.py` syntax error**: All 9 relative imports used `=` instead of `:` (e.g., `from .tag = init_tagging`). Fixed to `from .tag import init_tagging`.
2. **`explain.py` wrong function name**: `__init__.py` referenced `explain.get_system_stats` but the actual export is `explain.get_component_status`.
3. **`rebuild_index()` only handled `content` field**: Updated to handle `raw_text` and nested `data.content`/`data.text` via new `_extract_content()` helper.
4. **`retrieve.py` had no semantic search layer**: Added `retrieve_semantic()` using FAISS, and `_normalize_event()` for schema normalization.
5. **`capture.py` didn't auto-embed**: Added `_try_embed_event()` hook after each `capture_event()`.

### FAISS Index Rebuild Results
- Before: 7 mock vectors (dependencies missing)
- After: 114 real vectors from 389 raw events
- 261 events skipped (no embeddable content — file extraction blobs)
- Model: `all-MiniLM-L6-v2` (384-dim, cosine similarity via IndexFlatIP)
