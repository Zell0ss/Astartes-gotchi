# boot.py - Astartes-Gotchi Boot Sequence
# Runs FIRST on device startup (before main.py)
# Use for system initialization, hardware setup

import os
import gc

print("=" * 40)
print("ASTARTES-GOTCHI BOOT SEQUENCE")
print("=" * 40)

# Force garbage collection to start fresh
gc.collect()
print(f">>> Free RAM: {gc.mem_free()} bytes")

# Check filesystem
print(">>> Checking filesystem...")
try:
    files = os.listdir()
    print(f">>> Root files: {files}")

    if 'main.py' not in files:
        print(">>> WARNING: main.py not found!")
    else:
        print(">>> main.py detected - ready to launch")

except Exception as e:
    print(f">>> ERROR during boot: {e}")

# Optional: Initialize hardware here
# (LCD, touch, speaker can be initialized in main.py instead)

print(">>> Boot sequence complete")
print(">>> Launching main.py...")
print("=" * 40)
