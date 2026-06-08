#!/usr/bin/env python3
import sys
import os

print("Testing full MemPalace initialization...")

# Add the mempalace directory to the path
MEMPALACE_PATH = os.path.join(os.path.expanduser("~"), ".hermes", "mempalace")
sys.path.insert(0, MEMPALACE_PATH)
print(f"Added {MEMPALACE_PATH} to path")

try:
    import mempalace
    print("✓ MemPalace imported")
except Exception as e:
    print(f"✗ MemPalace import failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

try:
    mempalace.init_mempalace()
    print("✓ MemPalace initialized")
except Exception as e:
    print(f"✗ MemPalace initialization failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("Full initialization successful!")

# Test a simple capture
try:
    event_id = mempalace.capture_memory({
        'type': 'test',
        'content': 'Test memory from maintenance script',
        'context': 'system test',
        'timestamp': '2026-06-05T03:30:00Z'
    })
    print(f"✓ Captured test memory with ID: {event_id}")
except Exception as e:
    print(f"✗ Capture failed: {e}")
    import traceback
    traceback.print_exc()

print("Test completed.")