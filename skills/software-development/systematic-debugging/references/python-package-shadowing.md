# Python Script Shadowing Package Directory — Case Study

## Session: hermes-publish daily rebuild (2026-06-20)

### Problem
`python3 hermes_publish.py --all --steps compile epub kdp` failed with:
```
ModuleNotFoundError: No module named 'hermes_publish.config'; 'hermes_publish' is not a package
```

### Root Cause (3 compounding issues)

1. **Shadowing**: `hermes_publish.py` (CLI script) sat next to `hermes_publish/` (package dir). Python's import found the `.py` first, so `from hermes_publish.config import ...` tried to find `config` inside the script — not the package.

2. **Bare internal imports**: Inside the package, modules used `from config import BOOK_REGISTRY` instead of `from .config import BOOK_REGISTRY`. These only work if the package directory itself is on `sys.path`, which is wrong.

3. **Missing `__init__.py`**: The package had only `__init__.py.bak` — no active `__init__.py`.

### Fix Applied
```bash
# 1. Restore __init__.py
cp hermes_publish/__init__.py.bak hermes_publish/__init__.py

# 2. Fix all internal bare imports to relative
cd hermes_publish/
for f in utils.py step_compile.py step_cover.py step_epub.py step_kdp.py step_marketing.py step_pdf.py gen_nbs_images.py; do
  sed -i 's/^from config import/from .config import/' "$f"
  sed -i 's/^from utils import/from .utils import/' "$f"
  sed -i 's/^from step_images import/from .step_images import/' "$f"
done

# 3. Move CLI into package to avoid shadowing
mv hermes_publish.py hermes_publish_main.py
mv hermes_publish_main.py hermes_publish/cli.py
# Fix sys.path in cli.py: parent of parent (books dir), not own dir
# sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 4. Create thin wrapper at original location
cat > hermes_publish.py << 'EOF'
#!/usr/bin/env python3
import subprocess, sys
sys.exit(subprocess.call([sys.executable, "/path/to/hermes_publish/cli.py"] + sys.argv[1:]))
EOF
```

### Key Takeaway
Never name a CLI script the same as a package directory in the same folder. If you must keep the script name, move the script into the package or use a subprocess wrapper.
