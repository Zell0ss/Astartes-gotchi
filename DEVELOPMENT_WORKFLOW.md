# 💻 Development Workflow for M5Stack Core2 + MicroPython

## Table of Contents
1. [Overview of Development Options](#overview-of-development-options)
2. [Recommended Setup: VSCode + PyMakr](#recommended-setup-vscode--pymakr)
3. [Alternative: mpremote (Command Line)](#alternative-mpremote-command-line)
4. [Alternative: Thonny IDE](#alternative-thonny-ide)
5. [Cross-Platform Setup (Windows + LainOS)](#cross-platform-setup-windows--lainos)
6. [File Management](#file-management)
7. [Debugging Strategies](#debugging-strategies)
8. [Typical Development Cycle](#typical-development-cycle)
9. [Tips & Tricks](#tips--tricks)

---

## Overview of Development Options

MicroPython development is **NOT** like SSH to a remote server. The workflow is different:

### How It's Different from SSH Development:

| SSH/Remote Dev | MicroPython Dev |
|----------------|-----------------|
| Files live on remote server | Files live on your PC, get uploaded to device |
| Edit directly on server | Edit locally, sync to device |
| `git` on server | `git` on your PC only |
| Full filesystem | Limited flash storage (~8MB usable) |
| Always connected | Connect, upload, disconnect |

### The MicroPython Workflow:

1. **Write code on your PC** (in VSCode or any editor)
2. **Upload/sync to device** (via USB serial)
3. **Device executes code** (runs `main.py` on boot)
4. **Monitor output** (via serial console)
5. **Iterate** (edit on PC, re-upload, repeat)

### Development Tool Options:

| Tool | Pros | Cons | Best For |
|------|------|------|----------|
| **VSCode + PyMakr** | Full IDE, auto-sync, terminal integrated | Requires extension setup | Full development workflow |
| **VSCode + mpremote** | Simple, no extensions, scriptable | Manual commands | Advanced users, automation |
| **Thonny** | Beginner-friendly, built-in REPL | Less powerful than VSCode | Quick tests, learning |
| **Jupyter + MicroPython kernel** | Interactive notebooks | Experimental, setup complex | Data exploration |

**Recommendation for Astartes-Gotchi**: **VSCode + PyMakr** - gives you the closest experience to your normal development workflow.

---

## Recommended Setup: VSCode + PyMakr

PyMakr is a VSCode extension that handles file sync, REPL, and running scripts on MicroPython devices.

### Step 1: Install VSCode Extension

**In VSCode:**
1. Open Extensions panel (`Ctrl+Shift+X`)
2. Search for "Pymakr"
3. Install **"Pymakr"** by Pycom

**Or via command line:**
```bash
code --install-extension pycom.pymakr
```

### Step 2: Configure PyMakr for M5Stack Core2

**Create project config:**

In your project root (`/data/AstarGotchi/`), create a file `.pymakr.conf`:

```json
{
    "address": "/dev/ttyUSB0",
    "username": "micro",
    "password": "python",
    "sync_folder": "src",
    "open_on_start": true,
    "safe_boot_on_upload": false,
    "py_ignore": [
        ".vscode",
        ".gitignore",
        ".git",
        "env",
        "venv",
        "__pycache__",
        "*.md",
        "*.pyc",
        ".pymakr.conf"
    ],
    "fast_upload": false
}
```

**Windows version** (change `address` line):
```json
{
    "address": "COM3",
    ...
}
```

**What this does:**
- `address`: Serial port (adjust to your port!)
- `sync_folder`: Only upload files from `src/` directory
- `py_ignore`: Don't upload markdown docs, git files, etc.
- `fast_upload`: false = more reliable uploads

### Step 3: Project Structure

Organize your project like this:

```
AstarGotchi/
├── .pymakr.conf           # PyMakr config (created above)
├── .gitignore             # Git ignore (add .pymakr.conf to it)
├── CLAUDE.md              # Documentation (not uploaded)
├── SETUP_MICROPYTHON.md   # Setup guide (not uploaded)
├── DEVELOPMENT_WORKFLOW.md # This file (not uploaded)
├── src/                   # ← Only this folder syncs to device!
│   ├── boot.py            # Runs on device startup (optional)
│   ├── main.py            # Main game entry point
│   ├── lib/
│   │   ├── space_marine.py
│   │   ├── ui.py
│   │   ├── chaos_system.py
│   │   └── ...
│   ├── assets/
│   │   ├── sprites/
│   │   └── sounds/
│   └── config.py
└── tools/                 # Development scripts (not uploaded)
    └── deploy.sh
```

**Important**: Only files in `src/` will be uploaded to the device!

### Step 4: Using PyMakr

**Open PyMakr Panel:**
- Click the "Pymakr" icon in VSCode left sidebar
- Or: `Ctrl+Shift+P` → "Pymakr: Connect"

**Common Commands:**

| Action | PyMakr Command | Shortcut |
|--------|----------------|----------|
| Connect to device | "Pymakr: Connect" | - |
| Upload all files | "Pymakr: Upload Project" | `Ctrl+Shift+U` |
| Upload current file | "Pymakr: Upload Current File" | - |
| Run current file | "Pymakr: Run Current File" | `Ctrl+Shift+R` |
| Open REPL | "Pymakr: Open REPL" | `Ctrl+Shift+P` |
| Hard reset device | "Pymakr: Hard Reset" | - |

**Workflow in VSCode:**

1. **Edit** `src/main.py` on your PC
2. **Save** the file (`Ctrl+S`)
3. **Upload** project (`Ctrl+Shift+U`)
4. **Device reboots** and runs new code
5. **View output** in PyMakr terminal (bottom panel)

### Step 5: First Test

**Create** `src/main.py`:

```python
# Astartes-Gotchi - Hello World Test
from m5stack import LCD
import time

lcd = LCD()
lcd.clear(0x0000)  # Black background
lcd.print("ASTARTES-GOTCHI", 60, 100, 0xFEA0)  # Imperial Gold
lcd.print("Emperor protects!", 50, 130, 0xFFFF)  # White

print(">>> Device initialized. For the Emperor!")

# Blink test
for i in range(5):
    lcd.print(f"Blink {i+1}", 100, 160, 0xF800)  # Red
    time.sleep(0.5)
    lcd.print(f"Blink {i+1}", 100, 160, 0x0000)  # Clear
    time.sleep(0.5)

print(">>> Test complete.")
```

**Upload it:**
- `Ctrl+Shift+U` (Upload Project)
- Watch the PyMakr console - you should see:
  ```
  >>> Device initialized. For the Emperor!
  >>> Test complete.
  ```
- M5Stack screen should show "ASTARTES-GOTCHI" and blink 5 times

**If it works**: 🎉 Your development environment is ready!

---

## Alternative: mpremote (Command Line)

`mpremote` is the official MicroPython remote control tool - great for scripting and automation.

### Installation

```bash
pip install mpremote
```

### Basic Usage

**List connected devices:**
```bash
mpremote connect list
```

**Connect to REPL:**
```bash
mpremote connect /dev/ttyUSB0 repl
# Windows:
mpremote connect COM3 repl
```

**Run a script without uploading:**
```bash
mpremote connect /dev/ttyUSB0 run src/main.py
```

**Upload a file:**
```bash
mpremote connect /dev/ttyUSB0 cp src/main.py :main.py
```

**Upload entire directory:**
```bash
mpremote connect /dev/ttyUSB0 cp -r src/ :
```

**Execute command and get output:**
```bash
mpremote connect /dev/ttyUSB0 exec "import os; print(os.listdir())"
```

**List files on device:**
```bash
mpremote connect /dev/ttyUSB0 ls
```

**Remove file from device:**
```bash
mpremote connect /dev/ttyUSB0 rm main.py
```

### Create Deployment Script

**`tools/deploy.sh`** (Linux/LainOS):
```bash
#!/bin/bash
# Astartes-Gotchi deployment script

PORT=/dev/ttyUSB0

echo "🦅 Deploying Astartes-Gotchi to M5Stack Core2..."

# Upload all files from src/ to device root
mpremote connect $PORT cp -r src/* :

echo "✅ Upload complete. Resetting device..."

# Soft reset (re-run boot.py and main.py)
mpremote connect $PORT exec "import machine; machine.soft_reset()"

echo "🎮 Device ready. For the Emperor!"
```

**`tools/deploy.bat`** (Windows):
```batch
@echo off
REM Astartes-Gotchi deployment script

set PORT=COM3

echo Deploying Astartes-Gotchi to M5Stack Core2...

mpremote connect %PORT% cp -r src/* :

echo Upload complete. Resetting device...

mpremote connect %PORT% exec "import machine; machine.soft_reset()"

echo Device ready. For the Emperor!
```

**Make executable (Linux):**
```bash
chmod +x tools/deploy.sh
```

**Usage:**
```bash
# Linux/LainOS:
./tools/deploy.sh

# Windows:
tools\deploy.bat
```

---

## Alternative: Thonny IDE

Thonny is a beginner-friendly Python IDE with built-in MicroPython support.

### Installation

**Linux (LainOS/Ubuntu):**
```bash
sudo apt install thonny
# Or via pip:
pip3 install thonny
```

**Windows:**
Download installer from: https://thonny.org/

### Configuration

1. **Open Thonny**
2. **Tools → Options → Interpreter**
3. **Select**: "MicroPython (ESP32)"
4. **Port**: Select your COM port / /dev/ttyUSB0
5. **Click OK**

### Usage

**Advantages:**
- Instant REPL in bottom panel
- Run current file with F5
- Variables explorer
- Built-in file manager for device

**Disadvantages:**
- Less powerful than VSCode
- No git integration
- Slower for large projects

**Best for**: Quick testing, learning MicroPython, debugging small scripts

---

## Cross-Platform Setup (Windows + LainOS)

You can develop from **both** Windows and LainOS i3 using the same project.

### Shared Setup via Git

**On your cloud server or GitHub:**

```bash
# Initialize repo (if not already done)
cd /data/AstarGotchi
git init
git add .
git commit -m "Initial Astartes-Gotchi setup"

# Push to remote (GitHub/GitLab/your server)
git remote add origin git@github.com:josem/astartes-gotchi.git
git push -u origin main
```

### On Windows

1. **Clone the repo:**
   ```powershell
   git clone git@github.com:josem/Astartes-gotchi.git
   cd Astartes-gotchi
   ```

2. **Install tools:**
   ```powershell
   pip install mpremote esptool
   code --install-extension pycom.pymakr
   ```

3. **Update `.pymakr.conf`:**
   ```json
   {
       "address": "COM3",  # ← Adjust to your Windows COM port
       ...
   }
   ```

4. **Develop normally in VSCode**

### On LainOS i3

1. **Clone the repo (if not already there):**
   ```bash
   git clone git@github.com:josem/Astartes-gotchi.git
   cd Astartes-gotchi
   ```

2. **Install tools:**
   ```bash
   pip3 install mpremote esptool
   code --install-extension pycom.pymakr
   ```

3. **Update `.pymakr.conf`:**
   ```json
   {
       "address": "/dev/ttyUSB0",  # ← Linux port
       ...
   }
   ```

4. **Develop normally**

### Workflow

**Platform-agnostic approach:**

Since `.pymakr.conf` needs different `address` for Windows vs Linux, use **environment-specific config**:

**`.pymakr.conf`** (main config, gitignored):
```json
{
    "address": "/dev/ttyUSB0",  # Default for Linux
    ...
}
```

**`.pymakr.conf.windows`** (template for Windows):
```json
{
    "address": "COM3",
    ...
}
```

**`.gitignore`:**
```
.pymakr.conf
*.pyc
__pycache__/
```

**Setup script** `tools/setup_pymakr.sh`:
```bash
#!/bin/bash
# Auto-detect platform and create .pymakr.conf

if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "Detected Linux - configuring for /dev/ttyUSB0"
    cat > .pymakr.conf <<EOF
{
    "address": "/dev/ttyUSB0",
    "sync_folder": "src",
    ...
}
EOF
elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    echo "Detected Windows - configuring for COM3"
    cat > .pymakr.conf <<EOF
{
    "address": "COM3",
    "sync_folder": "src",
    ...
}
EOF
fi

echo "✅ .pymakr.conf created"
```

Run this script on each machine after cloning.

---

## File Management

### Device Filesystem

MicroPython on M5Stack Core2 has a simple filesystem:

```
/ (root)
├── boot.py        # Runs first on startup (optional, for system init)
├── main.py        # Runs after boot.py (your game entry point)
├── lib/           # Libraries (auto-imported)
│   ├── space_marine.py
│   └── ui.py
└── data/          # Assets, saves
    └── save.json
```

### Upload Strategy

**Two approaches:**

**1. Full Project Upload (Development)**
- Upload everything from `src/` to device `/`
- Quick iteration
- Use PyMakr "Upload Project"

**2. Selective Upload (Production)**
- Only upload changed files
- Faster for tweaks
- Use mpremote or PyMakr "Upload Current File"

### File Size Limits

- **Total flash**: 16MB (M5Stack Core2)
- **MicroPython firmware**: ~2MB
- **Available for your code**: ~8-10MB
- **Save for filesystem**: ~6-8MB usable

**Keep assets lean:**
- Sprites: 64×64 PNG → ~2KB each
- Sounds: 8-bit PCM, short clips
- Total project: Aim for < 2MB

---

## Debugging Strategies

### 1. Print Debugging (Classic)

```python
# main.py
print(">>> Starting Astartes-Gotchi")
print(f">>> Marine stats: {marine.geneseed_purity}")

# Output appears in PyMakr console or serial terminal
```

### 2. REPL Interactive Debugging

**Connect to REPL:**
- PyMakr: `Ctrl+Shift+P` → "Open REPL"
- mpremote: `mpremote repl`

**Test modules interactively:**
```python
>>> from lib.space_marine import SpaceMarine
>>> marine = SpaceMarine("Test Brother")
>>> marine.feed("ration")
>>> print(marine.sustenance)
70
>>> marine.update()
>>> print(marine.sustenance)
65
```

### 3. Exception Handling

```python
import sys

try:
    marine = SpaceMarine()
    marine.update()
except Exception as e:
    # Print full traceback to console
    sys.print_exception(e)
    # Optionally show error on LCD
    lcd.print(f"ERROR: {e}", 10, 10, 0xF800)
```

### 4. Memory Debugging

MicroPython has limited RAM - watch for memory errors.

```python
import gc

# Show free memory
print(f"Free RAM: {gc.mem_free()} bytes")

# Force garbage collection
gc.collect()
```

### 5. Remote Logging

**Stream logs to file on PC:**
```bash
# Linux:
mpremote connect /dev/ttyUSB0 repl > Astartes_log.txt

# Windows:
mpremote connect COM3 repl > Astartes_log.txt
```

---

## Typical Development Cycle

### Daily Workflow

**1. Pull latest code (if working across machines):**
```bash
git pull origin main
```

**2. Edit code in VSCode:**
- Modify `src/lib/space_marine.py`
- Save changes

**3. Upload to device:**
- `Ctrl+Shift+U` (PyMakr)
- Or: `./tools/deploy.sh`

**4. Observe behavior:**
- Watch M5Stack screen
- Read console output in PyMakr terminal

**5. Debug if needed:**
- Add print statements
- Test in REPL
- Check memory usage

**6. Iterate:**
- Fix bugs
- Re-upload
- Repeat

**7. Commit when feature works:**
```bash
git add src/lib/space_marine.py
git commit -m "Add chaos_whisper_response logic"
git push origin main
```

### Testing on Device

**Quick test loop:**
```bash
# Edit file
vim src/main.py

# Upload and run
mpremote run src/main.py

# Watch output
# Ctrl+C to stop
# Repeat
```

**Automated test script** (`tools/test_marine.py`):
```python
# Run this via: mpremote run tools/test_marine.py
from lib.space_marine import SpaceMarine

print("Testing SpaceMarine class...")

marine = SpaceMarine("Test Brother")
assert marine.geneseed_purity == 100
assert marine.corruption == 0

marine.feed("ration")
assert marine.sustenance > 50

marine.chaos_whisper_response("khorne", "resist")
assert marine.discipline > 50

print("✅ All tests passed!")
```

---

## Tips & Tricks

### Tip 1: Soft Reset vs Hard Reset

**Soft reset** (restart Python, keep REPL connection):
```python
import machine
machine.soft_reset()
```
Or: `Ctrl+D` in REPL

**Hard reset** (full reboot, like pressing physical button):
```python
import machine
machine.reset()
```

### Tip 2: Auto-reload on File Change

**Create `boot.py`:**
```python
# boot.py - Runs before main.py
import os
import time

# Optional: Set up WiFi, RTC, etc.
print(">>> Astartes-Gotchi booting...")

# Check if main.py exists
if 'main.py' in os.listdir():
    print(">>> Loading main.py")
else:
    print(">>> WARNING: main.py not found!")
```

**Your game logic stays in `main.py`** - easier to update.

### Tip 3: Persistent Config

Store settings on device filesystem:

```python
# config.py
import json

def load_config():
    try:
        with open('config.json', 'r') as f:
            return json.load(f)
    except:
        # Default config
        return {
            'volume': 5,
            'brightness': 80,
            'stasis_used_today': False
        }

def save_config(cfg):
    with open('config.json', 'w') as f:
        json.dump(cfg, f)
```

### Tip 4: Watchdog Timer (Prevent Hangs)

```python
from machine import WDT

# Enable watchdog (resets device if code hangs > 5 seconds)
wdt = WDT(timeout=5000)  # 5000ms

# In main loop:
while True:
    wdt.feed()  # Reset watchdog timer
    # ... game logic ...
```

### Tip 5: Power Management

```python
from m5stack import Power
import time

power = Power()

# Check battery level
battery = power.get_battery_level()
print(f"Battery: {battery}%")

# Deep sleep (ultra low power, wakes on timer or button)
if battery < 10:
    print("Low battery - entering deep sleep")
    # Wake up after 1 hour (1000000 microseconds = 1 second)
    machine.deepsleep(3600 * 1000000)  # 1 hour
```

### Tip 6: Development vs Production Mode

```python
# config.py
DEBUG = True  # Set to False for production

# In code:
if DEBUG:
    print(f"DEBUG: Marine stats = {marine.to_dict()}")
```

**Or use environment flag:**
```python
import os
DEBUG = 'DEBUG' in os.getenv('MICROPYFLAGS', '')
```

### Tip 7: VSCode Tasks

**`.vscode/tasks.json`:**
```json
{
    "version": "2.0.0",
    "tasks": [
        {
            "label": "Deploy to M5Stack",
            "type": "shell",
            "command": "./tools/deploy.sh",
            "group": {
                "kind": "build",
                "isDefault": true
            },
            "presentation": {
                "reveal": "always",
                "panel": "new"
            }
        },
        {
            "label": "Connect REPL",
            "type": "shell",
            "command": "mpremote connect /dev/ttyUSB0 repl"
        }
    ]
}
```

**Run with:** `Ctrl+Shift+B` (Build Task → Deploy)

---

## Summary

**Recommended Setup:**
- **Editor**: VSCode with PyMakr extension
- **Sync method**: PyMakr auto-sync from `src/` folder
- **Testing**: REPL + print debugging
- **Version control**: Git (only source code, not device files)
- **Cross-platform**: Use setup script to generate platform-specific `.pymakr.conf`

**Workflow:**
```
Edit (VSCode) → Save → Upload (Ctrl+Shift+U) → Test (M5Stack) → Debug (REPL) → Commit (Git)
```

**Next Steps:**
1. Install VSCode + PyMakr
2. Create `.pymakr.conf`
3. Upload test script
4. Verify everything works
5. Start building Astartes-Gotchi! 🦅⚔️

---

**For the Emperor!**
