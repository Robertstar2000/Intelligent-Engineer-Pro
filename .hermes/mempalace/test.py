import sys
import os
sys.path.insert(0, os.path.join(os.path.expanduser("~"), ".hermes"))
import mempalace
print("Mempalace imported from:", mempalace.__file__)
print("Storage path from mempalace:", mempalace.get_storage_path())
from mempalace.score import _STORAGE_PATH
print("Score module _STORAGE_PATH:", _STORAGE_PATH)
