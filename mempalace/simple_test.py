#!/usr/bin/env python3
import sys
import os

print("Starting simple test...")

# Add the mempalace directory to the path
MEMPALACE_PATH = os.path.join(os.path.expanduser("~"), ".hermes", "mempalace")
sys.path.insert(0, MEMPALACE_PATH)
print(f"Added {MEMPALACE_PATH} to path")

try:
    import capture
    print("✓ Capture imported")
except Exception as e:
    print(f"✗ Capture import failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

try:
    import tag
    print("✓ Tag imported")
except Exception as e:
    print(f"✗ Tag import failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

try:
    import score
    print("✓ Score imported")
except Exception as e:
    print(f"✗ Score import failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("All basic imports successful!")