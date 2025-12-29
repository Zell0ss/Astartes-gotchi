# 🔧 M5Stack Core2 - MicroPython Setup Guide

## Table of Contents
1. [🐧 Linux Quick Start (TL;DR)](#-linux-quick-start-tldr) ⭐ **START HERE if using Linux**
2. [Firmware Options Overview](#firmware-options-overview)
3. [Backup Original Firmware](#backup-original-firmware)
4. [Install MicroPython](#install-micropython)
5. [Verify Installation](#verify-installation)
6. [Restore Original Firmware](#restore-original-firmware)
7. [Troubleshooting](#troubleshooting)

---

## 🐧 Linux Quick Start (TL;DR)

**For impatient Space Marines who just want to flash and fight! 🦅**

This is the streamlined path for Linux users. For detailed explanations, see sections below.

### Prerequisites Check
```bash
# 1. Connect M5Stack Core2 via USB-C cable

# 2. Verify device is detected
lsusb | grep -i "CH340\|CP210\|USB Serial"
# or
lsusb | grep -i "USB Single Serial" 

# 3. Check serial port appears
ls /dev/ttyUSB* 
ls /dev/ttyACM*
# Should show: /dev/ttyUSB0 (most common) or /dev/ttyACM0
```

### One-Time Setup (First Flash Only)
```bash
# 1. Add your user to dialout group (required for serial port access)
sudo usermod -a -G dialout $USER

# 2. Log out and log back in (or reboot) for group change to take effect
# Verify with:
groups | grep dialout

# 3. Activate project virtual environment
cd /path/to/Astartes-gotchi
source venv/bin/activate

# 4. Install esptool in venv
pip install esptool

# Or system-wide (alternative):
# sudo apt install esptool
```

### Flash Process (Every Time)
```bash
# Set your port (check with: ls /dev/ttyUSB* /dev/ttyACM*)
# Common options: /dev/ttyUSB0 or /dev/ttyACM0
PORT=/dev/ttyACM0

# Step 1: Backup original firmware (IMPORTANT - do this once!)
# NOTE: M5Stack Core2 v1.1 uses 'esp32' chip (not esp32s3)
esptool.py --chip esp32 --port $PORT read_flash 0x0 0x400000 m5stack_core2_backup.bin
# Time: ~2-3 minutes
# If this fails, try: --chip esp32s3

# Step 2: Flash firmware using M5Burner (RECOMMENDED - GUI)
wget https://m5burner-cdn.m5stack.com/app/M5Burner-v3-beta-linux-x64.zip
unzip M5Burner-v3-beta-linux-x64.zip
cd M5Burner-v3-beta-linux-x64
chmod +x M5Burner
./M5Burner
# In M5Burner GUI: Select "Core2" → "UIFLOW2" → Select port → Click "Burn"
# Time: ~2-3 minutes

# --- OR ---

# Step 2 (Alternative): Manual flash with esptool
# ⚠️ WARNING: Core2-specific UIFlow firmware is NOT available as .bin download!
# Manual flashing only works with generic ESP32 firmware (NO M5Stack libraries)
# For M5Stack libraries, you MUST use M5Burner (see above)

# If you still want generic MicroPython (no M5Stack support):
wget https://micropython.org/resources/firmware/ESP32_GENERIC-SPIRAM-20240222-v1.22.2.bin

# Step 3: Erase flash
esptool.py --chip esp32 --port $PORT erase_flash
# Time: ~10 seconds

# Step 4: Flash generic MicroPython (NO M5Stack libraries!)
esptool.py --chip esp32 --port $PORT --baud 460800 write_flash -z 0x0 ESP32_GENERIC-SPIRAM-20240222-v1.22.2.bin
# Time: ~1-2 minutes
# Result: You'll have MicroPython but NO display/touch/power drivers

# Step 5: Reset device
# Press the RESET button on M5Stack, or:
esptool.py --chip esp32 --port $PORT run
```

### Verify Installation
```bash
# Connect to MicroPython REPL
screen $PORT 115200
# Or:
python -m serial.tools.miniterm $PORT 115200

# example: 
python -m serial.tools.miniterm /dev/ttyACM0 115200
# You should see:
# MicroPython v1.20.0 on 2023-04-26; ESP32S3 module with ESP32S3
# >>>

# Quick test: it will print in the terminal
>>> print("The Emperor protects!")
The Emperor protects!

# more extensive test: will print in the m5stack
import M5
M5.begin()
M5.Lcd.fillScreen(0x001F)  # Pantalla azul
M5.Lcd.setCursor(50, 100)
M5.Lcd.setTextColor(0xFFFF)  # Texto blanco
M5.Lcd.setTextSize(3)
M5.Lcd.print("Emperor protects!")

# Exit screen: Ctrl+A, then K, then Y
# Exit miniterm: Ctrl+]
```

### Troubleshooting Quick Fixes
```bash
# Permission denied?
sudo chmod 666 $PORT
# Or add yourself to dialout group (see One-Time Setup above)

# Device not detected?
# Press and hold BOOT button while plugging USB, release after 2 seconds

# Flash failed?
# Try slower baud rate:
esptool.py --chip esp32s3 --port $PORT --baud 115200 write_flash -z 0x0 firmware.bin
```

**That's it! Now proceed to `DEVELOPMENT_WORKFLOW.md` to deploy Astartes-Gotchi code.**

---

## Firmware Options Overview

The M5Stack Core2 can run different firmware options:

### 1. **UIFlow Firmware (Our Choice)** ⭐
- **Type**: MicroPython with M5Stack hardware libraries pre-installed
- **Language**: Python (MicroPython 1.25.0 based)
- **Important**: UIFlow firmware IS MicroPython - you can use it WITHOUT the UIFlow web interface
- **Pros**:
  - Full MicroPython access via USB/REPL
  - All M5Stack libraries included (LCD, Touch, IMU, Power Management)
  - Officially maintained by M5Stack
  - Works with standard tools: VSCode, Thonny, mpremote
- **Cons**: Slightly larger firmware size than generic MicroPython
- **Use case**: M5Stack projects that need hardware-specific drivers (like Astartes-Gotchi)

### 2. **Generic ESP32 MicroPython**
- **Type**: Standard MicroPython for ESP32
- **Language**: Python (MicroPython)
- **Pros**: Minimal, standard MicroPython experience
- **Cons**: No M5Stack-specific drivers - you must find/write drivers for touchscreen, IMU, power management
- **Use case**: Non-M5Stack ESP32 projects, or if you want to write all drivers yourself

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

**For Astartes-Gotchi**: UIFlow firmware (which is MicroPython + M5Stack libraries) is the sweet spot - Python's ease of development with all necessary hardware drivers pre-installed.

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

**Replace `PORT` with your actual port (COM3 on Windows, /dev/ttyACM0 or /dev/ttyUSB0 on Linux)**

**Windows:**
```powershell
esptool --chip esp32 --port COM3 read_flash 0x0 0x400000 m5stack_core2_backup.bin
```

**Linux:**
```bash
esptool.py --chip esp32 --port /dev/ttyACM0 read_flash 0x0 0x400000 m5stack_core2_backup.bin
```

**What this does**:
- `--chip esp32`: Specifies the Core2's chip type (use `esp32` not `esp32s3` for v1.1)
- `read_flash 0x0 0x400000`: Reads 4MB (entire flash memory) starting at address 0x0
- `m5stack_core2_backup.bin`: Output file

**Time**: ~2-3 minutes

⚠️ **Store this .bin file safely!** You'll need it to restore factory firmware.

---

## Install UIFlow MicroPython Firmware

**IMPORTANT**: As of 2024, M5Stack has moved to the UIFlow firmware which is MicroPython 1.25.0 with all M5Stack libraries pre-installed. You can use it WITHOUT the UIFlow web interface - just connect via USB and program in pure Python.

**CRITICAL FOR CORE2 USERS**: The Core2-specific firmware is **NOT available as a standalone .bin file** in the GitHub releases. The releases contain firmware for other M5Stack devices (Fire, Basic, Atom, etc.) but **Core2 firmware is distributed exclusively through M5Burner**. This is because Core2 has unique hardware (capacitive touchscreen, AXP192/AXP2101 power management) that requires device-specific firmware.

**Why you can't use Fire/Basic firmware on Core2**:
- Different display controllers (Core2 = ILI9342C touchscreen vs Fire = ILI9341 button-based)
- Different power management chips (Core2 = AXP192/AXP2101 vs Fire = IP5306)
- Different GPIO pin configurations

**Bottom line**: For Core2, use **M5Burner** (Method 1). Manual flashing (Method 2) only works with generic ESP32 firmware (without M5Stack libraries).

---

### Method 1: M5Burner (REQUIRED for Core2 with M5Stack libraries) ⭐

M5Burner is M5Stack's official flashing tool that automatically downloads and flashes the correct Core2-specific firmware.

#### Step 1: Download M5Burner

**Linux:**
```bash
wget https://m5burner-cdn.m5stack.com/app/M5Burner-v3-beta-linux-x64.zip
unzip M5Burner-v3-beta-linux-x64.zip
cd M5Burner-v3-beta-linux-x64
chmod +x M5Burner
./M5Burner
```

**Windows:**
1. Download: https://m5burner.m5stack.com/app/M5Burner-v3-win-x64.zip
2. Extract the ZIP file
3. Run `M5Burner.exe`

**macOS:**
```bash
wget https://m5burner.m5stack.com/app/M5Burner-v3-mac-x64.zip
unzip M5Burner-v3-mac-x64.zip
# Run the app from the extracted folder
```

#### Step 2: Flash Firmware via M5Burner

1. **Connect M5Stack Core2** via USB-C cable
2. **Launch M5Burner**
3. **Select Device**: Choose "Core2" from the device list
4. **Select Firmware**: Choose "UIFLOW2" (latest version - currently v2.4.0+)
5. **Select Port**:
   - Linux: `/dev/ttyACM0` (or `/dev/ttyUSB0`)
   - Windows: `COM3` (or whatever Device Manager shows)
6. **Configure**: Leave default settings (baud rate: 750000)
7. **Burn**: Click "Burn" button
8. **Wait**: Process takes ~2-3 minutes

**Done!** UIFlow firmware is now installed. You can close M5Burner.

---

### Method 2: Manual Flash with esptool (Only for Generic MicroPython)

**⚠️ WARNING**: This method **DOES NOT** give you M5Stack libraries (no `import M5`, no display drivers, no touch drivers). Only use this if you want to write all hardware drivers yourself.

**Why?** Core2-specific UIFlow firmware with M5Stack libraries is **only available through M5Burner** - it's not distributed as a standalone .bin file. The GitHub releases contain firmware for other devices (Fire, Basic, Atom) but NOT Core2.

If you still want generic MicroPython without M5Stack support:

#### Step 1: Download Generic ESP32 MicroPython

```bash
# Generic ESP32 MicroPython with SPIRAM support (Core2 has 8MB PSRAM)
wget https://micropython.org/resources/firmware/ESP32_GENERIC-SPIRAM-20231005-v1.21.0.bin

# Or latest stable:
wget https://micropython.org/resources/firmware/ESP32_GENERIC-SPIRAM-20240222-v1.22.2.bin
```

**What you'll get**:
- ✅ MicroPython REPL
- ✅ Standard MicroPython libraries (machine, time, etc.)
- ❌ **NO M5Stack libraries** (no M5.begin(), no display drivers, no touch drivers)
- ❌ **NO Core2 hardware support out of the box**

**What you'll need to do yourself**:
- Write ILI9342C display driver
- Write FT6336U touch controller driver
- Write AXP192/AXP2101 power management driver
- Write IMU driver

**For Astartes-Gotchi**: This is **NOT recommended** - you'll spend weeks writing drivers instead of making the game.

#### Step 2: Erase Flash (Important!)

**Windows:**
```powershell
esptool --chip esp32 --port COM3 erase_flash
```

**Linux:**
```bash
esptool.py --chip esp32 --port /dev/ttyACM0 erase_flash
```

**Time**: ~10 seconds

This ensures a clean slate for the new firmware.

#### Step 3: Flash Generic MicroPython Firmware

**Windows:**
```powershell
esptool --chip esp32 --port COM3 --baud 460800 write_flash -z 0x0 ESP32_GENERIC-SPIRAM-20240222-v1.22.2.bin
```

**Linux:**
```bash
esptool.py --chip esp32 --port /dev/ttyACM0 --baud 460800 write_flash -z 0x0 ESP32_GENERIC-SPIRAM-20240222-v1.22.2.bin
```

**Parameters explained**:
- `--chip esp32`: Core2 v1.1 uses standard ESP32 chip
- `--baud 460800`: Faster upload speed (can use 115200 if errors occur)
- `write_flash -z 0x0`: Write compressed firmware starting at address 0
- Last argument: Path to your downloaded .bin file

**Time**: ~1-2 minutes

#### Step 4: Reboot the Device

Press the **RESET button** on the M5Stack Core2 (small button on the side) or:

```bash
# Send hardware reset command
esptool.py --chip esp32 --port /dev/ttyACM0 run
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
screen /dev/ttyACM0 115200

# To exit screen: Ctrl+A, then K, then Y
```

**Using PuTTY (Windows):**
1. Download PuTTY: https://www.putty.org/
2. Open PuTTY
3. Select "Serial"
4. Enter COM port (e.g., COM3)
5. Speed: 115200
6. Click "Open"

**Using Python miniterm (Cross-platform):**
```bash
pip install pyserial
python -m serial.tools.miniterm /dev/ttyACM0 115200  # Linux
python -m serial.tools.miniterm COM3 115200          # Windows
```

### Expected Output:
```
MicroPython v1.25.0 on 2024-XX-XX; ESP32 module with ESP32
Type "help()" for more information.
>>>
```

**Note**: The exact version depends on which UIFlow release you installed (v2.4.0+ uses MicroPython v1.25.0).

### Quick Test:
```python
>>> print("The Emperor protects!")
The Emperor protects!

>>> import sys
>>> sys.implementation
(name='micropython', version=(1, 25, 0))

>>> # Test M5Stack UIFlow libraries
>>> import M5
>>> M5.begin()
>>> print("M5Stack Core2 initialized!")

>>> # Alternative test - clear screen
>>> from machine import Pin
>>> import time
>>> print("UIFlow firmware is working!")
```

If you see the Python prompt (`>>>`) and can execute commands, **UIFlow MicroPython is successfully installed!** 🎉

**IMPORTANT**: You now have full MicroPython with M5Stack libraries. You do NOT need to use the UIFlow web interface - you can program directly via USB using Python code.

---

## Restore Original Firmware

If you need to go back to the factory UIFlow firmware:

### Option 1: Restore Your Backup

**Windows:**
```powershell
esptool --chip esp32 --port COM3 erase_flash
esptool --chip esp32 --port COM3 --baud 460800 write_flash -z 0x0 m5stack_core2_backup.bin
```

**Linux:**
```bash
esptool.py --chip esp32 --port /dev/ttyACM0 erase_flash
esptool.py --chip esp32 --port /dev/ttyACM0 --baud 460800 write_flash -z 0x0 m5stack_core2_backup.bin
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
esptool.py --chip esp32 --port /dev/ttyACM0 erase_flash
esptool.py --chip esp32 --port /dev/ttyACM0 --baud 460800 write_flash -z 0x0 UIFlow_Core2_v2.0.0.bin
```

---

## Troubleshooting

### Issue: "Failed to connect to ESP32"

**Solution 1**: Try `esp32` instead of `esp32s3` (M5Stack Core2 v1.1 uses standard ESP32):
```bash
esptool.py --chip esp32 --port /dev/ttyACM0 ...
```

**Solution 2**: Press and hold the **BOOT button** (left side button) while connecting USB, then release after 2 seconds.

**Solution 3**: Try lower baud rate:
```bash
esptool.py --chip esp32 --port /dev/ttyACM0 --baud 115200 write_flash ...
```

**Solution 4** (Linux): Check permissions:
```bash
sudo chmod 666 /dev/ttyACM0
# Or add yourself to dialout group (permanent fix):
sudo usermod -a -G dialout $USER
# Then log out and back in
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

### Issue: UIFlow firmware boots but screen is blank

**Solution**: The display might need initialization. Connect via REPL and run:
```python
import M5
M5.begin()
print("M5Stack initialized!")
```

If this works, the firmware is fine - you just need to create a `boot.py` to initialize the M5Stack on startup.

### Issue: Can't find Core2 firmware in UIFlow releases

**Solution**: The filename format has changed over time. Look for:
- `CORE2_UIFLOW2_v*.bin` (UIFlow 2.x)
- `CORE2_*.bin`
- Or use M5Burner which automatically downloads the correct firmware

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
esptool.py --chip esp32 --port /dev/ttyACM0 read_flash 0x0 0x400000 backup.bin
```

**Erase flash:**
```bash
esptool.py --chip esp32 --port /dev/ttyACM0 erase_flash
```

**Flash firmware (use M5Burner for Core2 with M5Stack libraries):**
```bash
# Generic MicroPython (NO M5Stack libraries):
esptool.py --chip esp32 --port /dev/ttyACM0 --baud 460800 write_flash -z 0x0 ESP32_GENERIC-SPIRAM-20240222-v1.22.2.bin

# For UIFlow with M5Stack libraries, use M5Burner GUI tool (see above)
```

**Connect to REPL:**
```bash
screen /dev/ttyACM0 115200
# Or:
python -m serial.tools.miniterm /dev/ttyACM0 115200
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
