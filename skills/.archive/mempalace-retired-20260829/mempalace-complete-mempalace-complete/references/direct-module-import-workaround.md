# Direct Module Import Workaround for MemPalace in Cron Jobs

## Problem
When running MemPalace operations in cron jobs or isolated environments, importing from the mempalace package (e.g., `from mempalace import init_mempalace`) can fail with ModuleNotFoundError due to path issues or package installation state.

## Solution
Use direct module imports instead of package imports. This approach is more reliable in non-interactive environments like cron jobs.

### Before (may fail in cron jobs):
```python
from mempalace import init_mempalace
from mempalace.capture import capture_event
from mempalace.tag import extract_context_tags, save_context_tags
from mempalace.embed import add_embedding, init_embedding

init_mempalace(storage_path)
```

### After (reliable in cron jobs):
```python
import sys, os
sys.path.insert(0, os.path.expanduser('~/.hermes/mempalace'))

# Direct module imports
import capture
import tag
import embed

# Initialize each component individually
storage_path = os.path.expanduser('~/.hermes/mempalace')
capture.init_capture(storage_path)
tag.init_tagging(storage_path)
embed.init_embedding(storage_path)
```

## Usage in Memory-Full Offload Procedure
When implementing the Memory-Full Offload Procedure in cron jobs, use the direct module import approach to ensure reliable initialization of MemPalace components.

## Verification
After initialization, verify that components are working by checking:
- Raw event files are being created in `~/.hermes/mempalace/raw/`
- FAISS index is being updated with new vectors
- ID map entries correspond to stored events