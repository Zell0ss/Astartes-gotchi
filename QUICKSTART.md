# ⚡ QUICK START GUIDE

Get Astartes-Gotchi running on your M5Stack Core2 in 15 minutes.

---

## Prerequisites

- ✅ M5Stack Core2 v1.1 device
- ✅ USB-C cable
- ✅ Computer (Windows or Linux)
- ✅ Python 3.7+ installed

---

## Step 1: Install Tools (5 minutes)

Open terminal/PowerShell and run:

```bash
pip install esptool mpremote
```

**Verify installation:**
```bash
esptool version
mpremote --version
```

---

## Step 2: Flash MicroPython (5 minutes)

**Download firmware:**
```bash
# Linux:
wget https://github.com/m5stack/M5Stack_MicroPython/releases/download/v1.20.0/M5STACK_CORE2_MICROPYTHON_v1.20.0.bin

# Windows: Download manually from the URL above
```

**Connect M5Stack via USB** and identify port:

- **Linux**: Usually `/dev/ttyUSB0` (run `ls /dev/ttyUSB*`)
- **Windows**: Check Device Manager (usually `COM3` or `COM4`)

**Flash firmware:**

**Linux:**
```bash
# Erase flash
esptool.py --chip esp32s3 --port /dev/ttyUSB0 erase_flash

# Flash MicroPython
esptool.py --chip esp32s3 --port /dev/ttyUSB0 --baud 460800 write_flash -z 0x0 M5STACK_CORE2_MICROPYTHON_v1.20.0.bin
```

**Windows:**
```powershell
# Erase flash
esptool --chip esp32s3 --port COM3 erase_flash

# Flash MicroPython
esptool --chip esp32s3 --port COM3 --baud 460800 write_flash -z 0x0 M5STACK_CORE2_MICROPYTHON_v1.20.0.bin
```

**Reset the device** (press side button or unplug/replug)

---

## Step 3: Deploy Game (2 minutes)

**Navigate to project folder:**
```bash
cd /path/to/AstarGotchi
```

**Deploy:**

**Linux/LainOS:**
```bash
./tools/deploy.sh /dev/ttyUSB0
```

**Windows:**
```cmd
tools\deploy.bat COM3
```

**Expected output:**
```
🦅 ================================================
   ASTARTES-GOTCHI DEPLOYMENT
   For the Emperor!
================================================

📦 Uploading files to M5Stack Core2...
✅ Upload complete
🔄 Resetting device...
🎮 Device ready. For the Emperor! 🦅
```

---

## Step 4: Play! (∞ minutes)

The game starts automatically after deployment.

**On the M5Stack screen you should see:**
- Marine sprite (center)
- Stat bars (Geneseed, Fury, Sustenance, Discipline, Corruption)
- Touch buttons (FEED, COMBAT, PRAY, CLEAN, STATUS, CODEX)

**Basic controls:**
- **FEED**: Restore sustenance
- **PRAY**: Reduce corruption (3-hour cooldown)
- **CLEAN**: Remove casings/damage
- **STATUS**: View detailed stats
- **COMBAT**: Training minigames (Phase 4)
- **CODEX**: Discipline drill

**Your goal:**
Keep your marine alive and guide them to become a noble chapter warrior or fall to Chaos!

---

## Troubleshooting

### "Failed to connect to ESP32"
1. Press and hold BOOT button while connecting USB
2. Try lower baud rate: `--baud 115200`
3. Check USB cable (use data cable, not charge-only)

### "Permission denied" (Linux)
```bash
sudo chmod 666 /dev/ttyUSB0
# Or permanently:
sudo usermod -a -G dialout $USER
# Then log out and back in
```

### "Screen is blank after flash"
This is normal - MicroPython firmware has no default UI. Deploy the game (Step 3) to see the interface.

### "Code uploaded but nothing happens"
Connect to REPL to see errors:
```bash
mpremote connect /dev/ttyUSB0 repl
```

Check for error messages. Most common: missing files (re-run deploy script).

---

## Development Mode

**Connect to REPL** (see live output):
```bash
mpremote connect /dev/ttyUSB0 repl
```

**Run specific file:**
```bash
mpremote connect /dev/ttyUSB0 run src/main.py
```

**View files on device:**
```bash
mpremote connect /dev/ttyUSB0 ls
```

---

## Next Steps

- 📖 Read [CLAUDE.md](CLAUDE.md) for development guide
- 🎮 Play and test the MVP
- 🐛 Report issues/bugs
- ⚔️ Start Phase 2 (Evolution System)

---

**For the Emperor! 🦅⚔️**
