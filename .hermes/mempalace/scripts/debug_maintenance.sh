#!/bin/bash
# MemPalace Maintenance Script
# Run scoring, consolidation, and pruning operations

set -e

MEMPALACE_DIR="$HOME/.hermes/mempalace"
echo "MEMPALACE_DIR: $MEMPALACE_DIR"
echo "Contents of MEMPALACE_DIR:"
ls -la "$MEMPALACE_DIR"

PYTHONPATH="$MEMPALACE_DIR:$PYTHONPATH"
echo "PYTHONPATH: $PYTHONPATH"

echo "Starting MemPalace maintenance..."

# Run consolidation
echo "Running memory consolidation..."
python3 -c "
import sys
print('Python path:', sys.path)
sys.path.insert(0, '$MEMPALACE_DIR')
try:
    import mempalace
    print('Successfully imported mempalace')
    consolidated = mempalace.consolidate_memories()
    print(f'Consolidated {len(consolidated)} memories')
except Exception as e:
    print(f'Error: {e}')
    import traceback
    traceback.print_exc()
"