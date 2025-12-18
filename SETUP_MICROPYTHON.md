# 🔧 M5Stack Core2 - MicroPython Setup Guide

## Table of Contents
1. [Firmware Options Overview](#firmware-options-overview)
2. [Backup Original Firmware](#backup-original-firmware)
3. [Install MicroPython](#install-micropython)
4. [Verify Installation](#verify-installation)
5. [Restore Original Firmware](#restore-original-firmware)
6. [Troubleshooting](#troubleshooting)

---

## Firmware Options Overview

The M5Stack Core2 can run different firmware options:

### 1. **UIFlow (Factory Default)**
- **Type**: Visual block programming (like Scratch)
- **Language**: Blockly + MicroPython hybrid
- **Pros**: Beginner-friendly, quick prototyping, web-based IDE
- **Cons**: Limited flexibility, requires WiFi connection to IDE
- **Use case**: Rapid prototyping, education, simple projects

### 2. **MicroPython (Our Choice)**
- **Type**: Python 3.x interpreter for microcontrollers
- **Language**: Python (subset compatible with resource constraints)
- **Pros**: Full control, standard Python syntax, excellent for our project
- **Cons**: No visual IDE, requires understanding of Python
- **Use case**: Complex projects, games, custom applications

### 3. **Arduino Framework (ESP-IDF)**
- **Type**: C++ development using Arduino libraries
- **Language**: C/C++
- **Pros**: Maximum performance, low-level control, huge library ecosystem
- **Cons**: Steeper learning curve, more verbose code
- **Use case**: Performance-critical applications, hardware-specific features

### 4. **ESP-IDF (Native)**
- **Type**: Espressif's native development framework
- **Language**: C
- **Pros**: Absolute maximum performance, direct hardware access
- **Cons**: Very steep learning curve, complex setup
- **Use case**: Professional embedded development, OS development

**For Astartes-Gotchi**: MicroPython is the sweet spot - Python's ease of development with enough performance for a Tamagotchi-style game.

---

## Backup Original Firmware

**IMPORTANT**: Always backup before flashing! This allows you to restore the factory firmware if needed.

### Prerequisites
- M5Stack Core2 connected via USB-C cable
- Python 3.7+ installed on your system
- `esptool` installed (see below)

### Step 1: Install esptool

**On Windows (PowerShell/CMD):**
```powershell
pip install esptool
```

**On Linux (Ubuntu/Debian/LainOS):**
```bash
sudo pip3 install esptool
# Or using system package manager:
sudo apt install esptool
```

### Step 2: Identify Serial Port

**Windows:**
1. Open Device Manager
2. Expand "Ports (COM & LPT)"
3. Look for "USB-SERIAL CH340" or "Silicon Labs CP210x"
4. Note the COM port (e.g., `COM3`, `COM4`)

**Linux:**
```bash
# List USB devices
lsusb

# List serial ports
ls /dev/ttyUSB* /dev/ttyACM*

# Most likely it will be:
# /dev/ttyUSB0 (CH340 driver)
# or /dev/ttyACM0

# Add your user to dialout group (one-time setup):
sudo usermod -a -G dialout $USER
# Log out and back in for this to take effect
```

### Step 3: Backup Current Firmware

**Replace `PORT` with your actual port (COM3 on Windows, /dev/ttyUSB0 on Linux)**

**Windows:**
```powershell
esptool --chip esp32s3 --port COM3 read_flash 0 0x400000 m5stack_core2_backup.bin
```

**Linux:**
```bash
esptool.py --chip esp32s3 --port /dev/ttyUSB0 read_flash 0 0x400000 m5stack_core2_backup.bin
```

**What this does**:
- `--chip esp32s3`: Specifies the Core2's chip type
- `read_flash 0 0x400000`: Reads 4MB (entire flash memory)
- `m5stack_core2_backup.bin`: Output file

**Time**: ~2-3 minutes

⚠️ **Store this .bin file safely!** You'll need it to restore factory firmware.

---

## Install MicroPython

### Step 1: Download MicroPython Firmware

**Option A: Official M5Stack MicroPython (Recommended)**
```bash
# Download latest M5Stack-specific build:
wget https://github.com/m5stack/M5Stack_MicroPython/releases/download/v1.20.0/M5STACK_CORE2_MICROPYTHON_v1.20.0.bin

# Or using curl:
curl -LO https://github.com/m5stack/M5Stack_MicroPython/releases/download/v1.20.0/M5STACK_CORE2_MICROPYTHON_v1.20.0.bin
```

**Option B: Generic ESP32-S3 MicroPython**
```bash
# Download from MicroPython.org:
wget https://micropython.org/resources/firmware/ESP32_GENERIC_S3-20231005-v1.21.0.bin
```

**Recommendation**: Use Option A (M5Stack official) - it includes drivers for Core2's specific hardware (touch controller, power management IC, etc.)

**On Windows**: Download manually from GitHub releases page:
- Go to: https://github.com/m5stack/M5Stack_MicroPython/releases
- Download the latest `M5STACK_CORE2_MICROPYTHON_*.bin`

### Step 2: Erase Flash (Important!)

**Windows:**
```powershell
esptool --chip esp32s3 --port COM3 erase_flash
```

**Linux:**
```bash
esptool.py --chip esp32s3 --port /dev/ttyUSB0 erase_flash
```

**Time**: ~10 seconds

This ensures a clean slate for MicroPython.

### Step 3: Flash MicroPython

**Windows:**
```powershell
esptool --chip esp32s3 --port COM3 --baud 460800 write_flash -z 0x0 M5STACK_CORE2_MICROPYTHON_v1.20.0.bin
```

**Linux:**
```bash
esptool.py --chip esp32s3 --port /dev/ttyUSB0 --baud 460800 write_flash -z 0x0 M5STACK_CORE2_MICROPYTHON_v1.20.0.bin
```

**Parameters explained**:
- `--baud 460800`: Faster upload speed (can use 115200 if errors occur)
- `write_flash -z 0x0`: Write compressed firmware starting at address 0
- Last argument: Path to .bin file

**Time**: ~1-2 minutes

### Step 4: Reboot the Device

Press the **RESET button** on the M5Stack Core2 (small button on the side) or:

```bash
# Send hardware reset command
esptool.py --chip esp32s3 --port /dev/ttyUSB0 run
```

---

## Verify Installation

### Method 1: Serial REPL (Python Prompt)

**Using screen (Linux/macOS):**
```bash
# Install screen if needed:
sudo apt install screen  # Linux
brew install screen      # macOS

# Connect to REPL:
screen /dev/ttyUSB0 115200

# To exit screen: Ctrl+A, then K, then Y
```

**Using PuTTY (Windows):**
1. Download PuTTY: https://www.putty.org/
2. Open PuTTY
3. Select "Serial"
4. Enter COM port (e.g., COM3)
5. Speed: 115200
6. Click "Open"

**Using Python picocom (Cross-platform):**
```bash
pip install pyserial
python -m serial.tools.miniterm /dev/ttyUSB0 115200  # Linux
python -m serial.tools.miniterm COM3 115200          # Windows
```

### Expected Output:
```
MicroPython v1.20.0 on 2023-04-26; ESP32S3 module with ESP32S3
Type "help()" for more information.
>>>
```

### Quick Test:
```python
>>> print("Emperor protects!")
Emperor protects!

>>> import sys
>>> sys.implementation
(name='micropython', version=(1, 20, 0))

>>> # Test M5Stack-specific modules
>>> from m5stack import M5Stack
>>> m5 = M5Stack()
>>> m5.lcd.clear()  # Should clear the screen
```

If you see the Python prompt (`>>>`) and can execute commands, **MicroPython is successfully installed!** 🎉

---

## Restore Original Firmware

If you need to go back to the factory UIFlow firmware:

### Option 1: Restore Your Backup

**Windows:**
```powershell
esptool --chip esp32s3 --port COM3 erase_flash
esptool --chip esp32s3 --port COM3 --baud 460800 write_flash -z 0x0 m5stack_core2_backup.bin
```

**Linux:**
```bash
esptool.py --chip esp32s3 --port /dev/ttyUSB0 erase_flash
esptool.py --chip esp32s3 --port /dev/ttyUSB0 --baud 460800 write_flash -z 0x0 m5stack_core2_backup.bin
```

### Option 2: Download Fresh UIFlow Firmware

**Using M5Burner (Official Tool - Easiest):**

1. **Download M5Burner:**
   - Windows: https://m5burner.m5stack.com/app/M5Burner-v3-win-x64.zip
   - Linux: https://m5burner.m5stack.com/app/M5Burner-v3-linux-x64.zip
   - macOS: https://m5burner.m5stack.com/app/M5Burner-v3-mac-x64.zip

2. **Extract and run M5Burner**

3. **Select Device:**
   - Choose "Core2" from device list

4. **Select Firmware:**
   - Choose "UIFlow v2" or "UIFlow v1.x" (latest stable)

5. **Configure:**
   - Select COM port
   - Baud rate: 750000 (default)

6. **Burn:**
   - Click "Burn" button
   - Wait for completion (~2 minutes)

**Manual Method (Advanced):**
```bash
# Download UIFlow firmware
wget https://m5burner.m5stack.com/firmware/Core2/UIFlow/UIFlow_Core2_v2.0.0.bin

# Flash it
esptool.py --chip esp32s3 --port /dev/ttyUSB0 erase_flash
esptool.py --chip esp32s3 --port /dev/ttyUSB0 --baud 460800 write_flash -z 0x0 UIFlow_Core2_v2.0.0.bin
```

---

## Troubleshooting

### Issue: "Failed to connect to ESP32"

**Solution 1**: Press and hold the **BOOT button** (left side button) while connecting USB, then release after 2 seconds.

**Solution 2**: Try lower baud rate:
```bash
esptool.py --chip esp32s3 --port /dev/ttyUSB0 --baud 115200 write_flash ...
```

**Solution 3** (Linux): Check permissions:
```bash
sudo chmod 666 /dev/ttyUSB0
# Or add yourself to dialout group (permanent fix):
sudo usermod -a -G dialout $USER
```

### Issue: "Serial port not found"

**Windows**: Install CH340 driver:
- Download: http://www.wch.cn/downloads/CH341SER_ZIP.html
- Extract and run `SETUP.EXE`

**Linux**: CH340 driver should be built into kernel. If not:
```bash
sudo apt install linux-modules-extra-$(uname -r)
sudo modprobe ch341
```

### Issue: MicroPython boots but screen is blank

**Solution**: The display might need initialization. Connect via REPL and run:
```python
from m5stack import LCD
lcd = LCD()
lcd.clear(0xFFFF)  # Fill with white
lcd.print("Emperor protects!", 50, 100, 0x0000)
```

If this works, the firmware is fine - you just need to create a `boot.py` to initialize the display.

### Issue: "Flash size mismatch"

**Solution**: The Core2 has 16MB flash. Some guides mention 4MB (Core/Fire). Adjust read size:
```bash
# Read full 16MB:
esptool.py --chip esp32s3 --port /dev/ttyUSB0 read_flash 0 0x1000000 backup.bin
```

### Issue: Device reboots in a loop

**Solution**: Flash is likely corrupted. Erase completely and reflash:
```bash
esptool.py --chip esp32s3 --port /dev/ttyUSB0 erase_flash
# Wait 30 seconds
esptool.py --chip esp32s3 --port /dev/ttyUSB0 --baud 115200 write_flash -z 0x0 firmware.bin
```

---

## Quick Reference Commands

**Backup firmware:**
```bash
esptool.py --chip esp32s3 --port /dev/ttyUSB0 read_flash 0 0x400000 backup.bin
```

**Erase flash:**
```bash
esptool.py --chip esp32s3 --port /dev/ttyUSB0 erase_flash
```

**Flash MicroPython:**
```bash
esptool.py --chip esp32s3 --port /dev/ttyUSB0 --baud 460800 write_flash -z 0x0 firmware.bin
```

**Connect to REPL:**
```bash
screen /dev/ttyUSB0 115200
# Or:
python -m serial.tools.miniterm /dev/ttyUSB0 115200
```

---

## Next Steps

Once MicroPython is installed and verified:

1. ✅ Install development tools (see `DEVELOPMENT_WORKFLOW.md`)
2. ✅ Setup VSCode with remote development
3. ✅ Upload your first test script
4. ✅ Start building Astartes-Gotchi!

---

**For the Emperor! 🦅**
