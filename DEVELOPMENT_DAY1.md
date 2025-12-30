# DEVELOPMENT DAY 1 - Technical Documentation
## Astartes-Gotchi MVP Implementation on M5Stack Core2

**Date**: 2024-12-29
**Hardware**: M5Stack Core2 v1.1 (ESP32, 320x240 touchscreen, 8MB PSRAM)
**Firmware**: UIFlow MicroPython v2.4.0 (based on MicroPython 1.25.0)
**Development Platform**: Linux (LainOS i3 on Sony Vaio)

---

## Table of Contents
1. [Executive Summary](#executive-summary)
2. [Hardware Setup & Firmware Selection](#hardware-setup--firmware-selection)
3. [Code Architecture](#code-architecture)
4. [UIFlow M5 Library Integration](#uiflow-m5-library-integration)
5. [Technical Challenges & Solutions](#technical-challenges--solutions)
6. [Non-Standard Python Libraries](#non-standard-python-libraries)
7. [File Structure & Deployment](#file-structure--deployment)
8. [Key Design Decisions](#key-design-decisions)
9. [Testing & Validation](#testing--validation)
10. [Next Steps](#next-steps)

---

## Executive Summary

Successfully deployed Astartes-Gotchi MVP to M5Stack Core2 hardware. The game runs natively on the device with:
- Full touchscreen interaction (6 buttons)
- Real-time stat tracking and display
- Persistent save/load system
- Auto-save every 30 seconds
- Power management (software power-off)

**Key Achievement**: Migrated from generic MicroPython to UIFlow-specific API, enabling full hardware access without writing low-level drivers.

---

## Hardware Setup & Firmware Selection

### Initial Hardware Discovery

**Challenge**: M5Stack Core2 v1.1 uses different hardware than documented in older guides.

**Critical Findings**:
- **Chip**: ESP32 (NOT ESP32-S3) - Must use `--chip esp32` with esptool
- **Serial Port**: `/dev/ttyACM0` (cdc_acm driver, NOT CH340/ttyUSB0)
- **USB Communication**: Uses ACM protocol, not standard USB-UART bridge

### Firmware Decision: UIFlow vs Generic MicroPython

**Initial Plan**: Use generic MicroPython from micropython.org

**Problem Discovered**: Core2 has unique hardware requiring custom drivers:
- **Display**: ILI9342C (capacitive touchscreen controller)
- **Touch**: FT6336U (capacitive touch IC)
- **Power Management**: AXP192 or AXP2101 (PMIC)
- **IMU**: MPU6886 (accelerometer/gyroscope)

**Solution**: UIFlow Firmware (M5Stack's official MicroPython distribution)

**Why UIFlow**:
1. **Pre-compiled drivers**: All Core2 hardware drivers included
2. **Official support**: Maintained by M5Stack
3. **Pure MicroPython**: Can be used WITHOUT UIFlow web interface
4. **Distribution**: Only available via M5Burner (not as standalone .bin)

**Critical Discovery**: Core2 firmware is NOT in GitHub releases (`github.com/m5stack/uiflow-micropython/releases` contains Fire, Basic, Atom, but NOT Core2). Must use M5Burner GUI tool.

### Flashing Process

```bash
# 1. Backup original firmware
esptool.py --chip esp32 --port /dev/ttyACM0 read_flash 0x0 0x400000 m5stack_core2_backup.bin

# 2. Flash UIFlow via M5Burner
wget https://m5burner-cdn.m5stack.com/app/M5Burner-v3-beta-linux-x64.zip
unzip M5Burner-v3-beta-linux-x64.zip
./M5Burner
# GUI: Select "Core2" → "UIFLOW2" (with SPIRAM) → Flash
```

**Configuration**:
- Timezone: GMT+1 (Madrid)
- Boot option: "Run main.py" (auto-start on power-on)

---

## Code Architecture

### High-Level Design

```
┌─────────────────────────────────────────┐
│           main.py (Game Loop)           │
│  - Initialization                       │
│  - Main loop (10 FPS)                   │
│  - Input handling                       │
│  - Save/load management                 │
└─────────────────────────────────────────┘
                  │
        ┌─────────┴─────────┐
        ▼                   ▼
┌──────────────────┐  ┌──────────────────┐
│  space_marine.py │  │      ui.py       │
│  - Stats logic   │  │  - Rendering     │
│  - Evolution     │  │  - Touch input   │
│  - Decay system  │  │  - M5 hardware   │
└──────────────────┘  └──────────────────┘
        │                   │
        ▼                   ▼
┌──────────────────┐  ┌──────────────────┐
│ save_manager.py  │  │   config.py      │
│  - JSON I/O      │  │  - Constants     │
│  - Backup logic  │  │  - Colors        │
└──────────────────┘  └──────────────────┘
```

### File Structure

```
M5Stack Device Root:
├── boot.py              # UIFlow boot sequence
├── main.py              # Game entry point
├── config.py            # Game constants
├── lib/
│   ├── space_marine.py  # Marine logic
│   ├── ui.py            # UI and M5 hardware interface
│   ├── save_manager.py  # Persistence
│   ├── chaos_system.py  # Chaos mechanics (stub)
│   └── minigames/
│       └── __init__.py
└── astartes_save.json   # Save file (auto-created)
```

---

## UIFlow M5 Library Integration

### The M5 Module

UIFlow provides a top-level `M5` module that abstracts all hardware:

```python
import M5

# CRITICAL: Must call this before using any hardware
M5.begin()

# Hardware access:
M5.Lcd      # Display controller
M5.Touch    # Touchscreen
M5.Power    # Power management
M5.Speaker  # Audio (not yet used)
M5.Imu      # IMU (not yet used)
```

### Display API (M5.Lcd)

**NOT standard Python**. UIFlow-specific methods:

```python
# Clear screen
M5.Lcd.fillScreen(color)  # color is RGB888 format (24-bit)

# Text rendering
M5.Lcd.setCursor(x, y)
M5.Lcd.setTextColor(color)
M5.Lcd.setTextSize(size)  # 1=small, 2=medium, 3=large
M5.Lcd.print(text)

# Rectangles
M5.Lcd.fillRect(x, y, width, height, color)
```

**Color Format**: RGB888 (24-bit) - **CRITICAL: UIFlow2 uses 24-bit, NOT RGB565!**
- Format: `0xRRGGBB`
- Example: `0x0000FF` = Blue, `0xFF0000` = Red, `0x00FF00` = Green
- **Common mistake**: Using RGB565 values (0xF800 for red) will show wrong colors

### Touch API (M5.Touch)

**CRITICAL DISCOVERY**: Touch API requires `M5.update()` to be called every frame.

```python
# In game loop (every frame):
M5.update()  # Updates internal state

# Check for touch
if M5.Touch.getCount() > 0:
    x = M5.Touch.getX()
    y = M5.Touch.getY()
    # Process touch at (x, y)
```

**Common Mistake**: Using `M5.Touch.getDetail()` (doesn't exist in UIFlow).
**Correct API**: `getX()` and `getY()` separately.

### Power Management API (M5.Power)

```python
# Software power-off
M5.Power.powerOff()

# Alternative (if powerOff() not available):
import machine
machine.deepsleep()  # Functionally similar to power off
```

---

## Technical Challenges & Solutions

### Challenge 1: Touch Debouncing

**Problem**: Single physical tap registers 3-5 touch events due to sensor bounce.

**Symptoms**:
- Feeding once gives 3 rations
- Button presses repeat uncontrollably

**Solution**: Implement touch cooldown (500ms)

```python
class AstartesUI:
    def __init__(self):
        self.last_touch_time = 0
        self.touch_cooldown = 500  # milliseconds

    def get_input(self):
        if M5.Touch.getCount() > 0:
            current_time = time.ticks_ms()
            time_since_last = time.ticks_diff(current_time, self.last_touch_time)

            if time_since_last < self.touch_cooldown:
                return None  # Ignore bounce

            self.last_touch_time = current_time
            # Process touch...
```

**Key Function**: `time.ticks_ms()` and `time.ticks_diff()` (MicroPython-specific, handles timer wraparound correctly)

### Challenge 2: Button Layout (320x240 Screen)

**Problem**: Original layout had 6 buttons but last 2 were off-screen (y=235 + h=30 = 265 > 240).

**Solution**: Reorganize into 2 rows of 3 buttons

```python
# Optimized layout (all visible):
# Row 1 (y=195):
self.btn_feed = (5, 195, 100, 20)
self.btn_combat = (110, 195, 100, 20)
self.btn_pray = (215, 195, 100, 20)

# Row 2 (y=218):
self.btn_clean = (5, 218, 100, 20)
self.btn_status = (110, 218, 100, 20)
self.btn_power = (215, 218, 100, 20)
```

**Total height**: 195 + 20 + (218-195) + 20 = 238 pixels (fits in 240)

### Challenge 3: File Structure on Device

**Problem**: Initial deploy created `src/` directory on device, causing import errors:
```
ImportError: no module named 'lib'
```

**Root Cause**: Files in `src/` but Python imports looked for `lib/` at root level.

**Solution**: Modified deploy script to copy files individually to device root:

```bash
# OLD (broken):
mpremote connect $PORT cp -r src/* :

# NEW (working):
cd src
mpremote connect $PORT cp boot.py :
mpremote connect $PORT cp main.py :
mpremote connect $PORT mkdir :lib
mpremote connect $PORT cp lib/space_marine.py :lib/
# ... etc
```

### Challenge 4: Save File Persistence Across Deploys

**Problem**: Old save files with corrupted stats persisted across code updates.

**Solution**: Deploy script now clears save files:

```bash
mpremote connect $PORT exec "import os; [os.remove(f) for f in ['astartes_save.json', 'astartes_save.json.bak'] if f in os.listdir()]"
```

---

## Non-Standard Python Libraries

### MicroPython-Specific Modules

**1. `time` module** (different from standard Python):
```python
import time

# MicroPython additions:
time.ticks_ms()         # Milliseconds since boot (wraps at ~24 days)
time.ticks_diff(a, b)   # Difference handling wraparound
time.sleep_ms(ms)       # Sleep in milliseconds
```

**2. `machine` module** (hardware access):
```python
import machine

machine.soft_reset()    # Software reset (reboot device)
machine.deepsleep()     # Enter deep sleep (low power mode)
machine.reset()         # Hard reset
```

**3. `gc` module** (garbage collection):
```python
import gc

gc.collect()  # Manually trigger garbage collection
gc.mem_free() # Check free memory (important on ESP32)
```

**Why manual GC?** ESP32 has limited RAM (8MB PSRAM + ~320KB SRAM). Long-running games need periodic collection to prevent memory fragmentation.

### UIFlow-Specific Modules

**1. `M5` module** (top-level hardware abstraction):
```python
import M5

M5.begin()         # Initialize hardware
M5.update()        # Update sensor states (call every frame)
M5.Lcd             # Display controller
M5.Touch           # Touch input
M5.Power           # Power management
M5.Speaker         # Audio (future use)
M5.Imu             # IMU sensor (future use)
```

**Source**: Compiled into UIFlow firmware, not available in generic MicroPython.

### Standard Library Limitations

**JSON**: Available but limited
```python
import json

# Works:
json.dumps(dict)  # Serialize to string
json.loads(str)   # Parse from string

# Does NOT work:
json.dump(dict, file, indent=2)  # 'indent' parameter not supported
```

**No pip**: MicroPython doesn't have pip. All libraries must be:
1. Written in pure Python
2. Copied to device manually
3. Or compiled into firmware

---

## File Structure & Deployment

### Local Development Structure

```
Astartes-gotchi/
├── src/                    # Source code (deployed to device)
│   ├── boot.py
│   ├── main.py
│   ├── config.py
│   └── lib/
│       ├── space_marine.py
│       ├── ui.py
│       ├── save_manager.py
│       └── chaos_system.py
├── tools/
│   └── deploy.sh          # Deployment automation
├── SETUP_MICROPYTHON.md   # Hardware setup guide
├── DEVELOPMENT_DAY1.md    # This file
└── .claudememory          # Session continuity data
```

### Deployment Pipeline

```bash
./tools/deploy.sh
```

**Steps**:
1. Connect to `/dev/ttyACM0`
2. Copy `boot.py`, `main.py`, `config.py` to device root
3. Create `lib/` directory on device
4. Copy all `lib/*.py` files individually
5. Create `lib/minigames/` subdirectory
6. Delete old save files (`astartes_save.json`)
7. Soft reset device (`machine.soft_reset()`)

**Why individual copies?** `mpremote cp -r src/* :` created unwanted `src/` directory on device.

### Save File Format

**Location**: Device root (`/astartes_save.json`)

**Format**: JSON (human-readable for debugging)

```json
{
  "name": "Battle Brother",
  "current_stage": 0,
  "age_cycles": 0,
  "geneseed_purity": 100,
  "battle_fury": 50,
  "sustenance": 45,
  "discipline": 50,
  "corruption": 0,
  "combat_experience": 0,
  "care_mistakes": 0,
  "chaos_whispers_resisted": 0,
  "chaos_whispers_accepted": 0,
  "is_alive": true,
  "death_cause": null,
  "final_chapter": null
}
```

**Backup Strategy**: `save_manager.py` creates `.bak` file before each save.

---

## Key Design Decisions

### 1. Frame Rate: 10 FPS

**Reasoning**:
- **Battery life**: Higher FPS drains battery faster
- **Display refresh**: M5Stack LCD updates are relatively slow
- **Game type**: Tamagotchi doesn't need fast refresh (not action game)
- **MicroPython**: Interpreted language, lower overhead is better

**Implementation**:
```python
FRAME_TIME = 0.1  # 100ms = 10 FPS

while marine.is_alive:
    frame_start = time.time()
    # ... game logic ...
    frame_duration = time.time() - frame_start
    sleep_time = max(0, FRAME_TIME - frame_duration)
    time.sleep(sleep_time)
```

### 2. Update Interval: 60 seconds

**Marine stats decay** happens every 60 seconds, not every frame.

**Reasoning**:
- **Game pacing**: Tamagotchi should be slow-paced
- **Battery**: Less computation = longer battery life
- **User experience**: Stats changing every second would be stressful

```python
UPDATE_INTERVAL = 60  # seconds

if current_time - last_update >= UPDATE_INTERVAL:
    marine.update()  # Decay stats
    last_update = current_time
```

### 3. Auto-save: Every 30 seconds

**Reasoning**:
- **Crash protection**: If device crashes, lose max 30s of progress
- **Flash wear**: Too frequent saves wear out flash memory
- **Performance**: JSON serialization has overhead

```python
AUTOSAVE_INTERVAL = 30  # seconds

if current_time - last_save >= AUTOSAVE_INTERVAL:
    save_mgr.save(marine.to_dict())
    last_save = current_time
```

### 4. Touch Cooldown: 500ms

**Reasoning**:
- **Debouncing**: Prevents accidental multi-taps
- **User experience**: Feels responsive but controlled
- **Battery**: Prevents rapid-fire actions draining stats

### 5. Debug Mode: Always On (MVP)

```python
DEBUG = True  # in config.py
```

**Reasoning**:
- **Development**: Need visibility into what's happening
- **Serial output**: Via miniterm for debugging
- **Production**: Will be set to False in final release

---

## Testing & Validation

### Hardware Tests

**1. Display Test** (manual via REPL):
```python
>>> import M5
>>> M5.begin()
>>> M5.Lcd.fillScreen(0x001F)  # Blue screen
>>> M5.Lcd.print("Test")        # Text rendering
```
✅ **Result**: Display working correctly

**2. Touch Test** (via debug logs):
```python
>>> Touch detected at (120, 205)
>>> Button: FEED
```
✅ **Result**: Touch working, coordinates accurate

**3. Power Off Test**:
- Tap POWER button
- See "For the Emperor!" → "Powering off..."
- Device shuts down

✅ **Result**: Power management working

### Software Tests

**1. Save/Load Cycle**:
```
>>> No save found - creating new Neophyte
>>> Game saved to astartes_save.json
[Reset device]
>>> Restoring Battle Brother
```
✅ **Result**: Persistence working

**2. Stat Decay**:
```
>>> Update: Sust=100, Fury=50, Corrupt=0
[Wait 60 seconds]
>>> Update: Sust=95, Fury=50, Corrupt=0
```
✅ **Result**: Decay system working

**3. Touch Debounce**:
- Tap FEED once
- Sustenance increases by 10 (one ration, not three)

✅ **Result**: Debouncing working

### Known Issues (To Fix)

1. **Screen flicker**: Full screen redraw causes visible flicker
   - **Solution**: Implement dirty rectangles (only redraw changed areas)

2. **No visual feedback on button press**: Touch feels "dead"
   - **Solution**: Flash button color on tap

3. **Stats can go negative**: No bounds checking
   - **Solution**: Add `max(0, stat)` clamping

4. **No evolution logic yet**: Marine never evolves
   - **Solution**: Implement evolution conditions (Day 2+)

---

## Next Steps

### Immediate (Day 2)
1. **Optimize rendering**: Dirty rectangles to reduce flicker
2. **Button feedback**: Visual/haptic feedback on touch
3. **Bounds checking**: Clamp all stats to 0-100 range
4. **Evolution system**: Implement first evolution (Neophyte → Scout)

### Short-term (Week 1)
1. **Minigames**: Implement "Heresy Check" (first minigame)
2. **Chaos Whispers**: Basic implementation (one god)
3. **Death system**: Implement death by negligence
4. **Sprites**: Replace colored rectangles with pixel art

### Mid-term (Week 2-3)
1. **All evolution paths**: 11 final forms
2. **All minigames**: 3 complete games
3. **Sound effects**: Basic beeps/alerts
4. **Balance tuning**: Playtest and adjust decay rates

### Long-term (Month 1)
1. **Polish**: Animations, better UI
2. **Documentation**: User manual
3. **Testing**: Extended playtesting
4. **Release**: Share with community

---

## Development Environment

### Tools Used
- **Python**: 3.x (for development scripts)
- **MicroPython**: 1.25.0 (on device)
- **esptool**: Firmware flashing
- **mpremote**: File transfer and REPL
- **miniterm**: Serial console (`python -m serial.tools.miniterm`)
- **M5Burner**: UIFlow firmware installer
- **git**: Version control

### Linux-Specific Notes

**Serial Port Permissions**:
```bash
sudo usermod -a -G dialout $USER
# Log out and back in for changes to take effect
```

**Exit miniterm**: `Ctrl+T` then `Q` (not `Ctrl+]` on Spanish keyboards)

### Key Commands

```bash
# Deploy code
./tools/deploy.sh

# Connect to REPL
python -m serial.tools.miniterm /dev/ttyACM0 115200

# Run game manually (in REPL)
>>> exec(open('main.py').read())

# Check files on device (in REPL)
>>> import os
>>> os.listdir()
>>> os.listdir('lib')
```

---

## Lessons Learned

### 1. Read the Hardware Documentation First
**Mistake**: Assumed Core2 = ESP32-S3 based on generic guides.
**Reality**: Core2 v1.1 = ESP32 (standard).
**Impact**: Wasted time troubleshooting esptool errors.

### 2. UIFlow Firmware is Device-Specific
**Mistake**: Expected Core2 firmware in GitHub releases.
**Reality**: Only available via M5Burner GUI.
**Impact**: Had to switch methods mid-setup.

### 3. Touch API Requires M5.update()
**Mistake**: Called touch methods without `M5.update()`.
**Reality**: Touch state only updates when `M5.update()` is called.
**Impact**: Touch appeared broken for 30 minutes.

### 4. MicroPython != Python
**Assumption**: Python code will "just work" on MicroPython.
**Reality**: Limited stdlib, no pip, different APIs (`time.ticks_ms()` vs `time.time()`).
**Impact**: Had to rewrite time-based logic.

### 5. Deploy Script Matters
**Mistake**: Used `cp -r src/* :` thinking it would copy contents.
**Reality**: Created `src/` directory on device.
**Impact**: Import errors, had to manually delete and re-upload.

---

## Performance Metrics

### Memory Usage (ESP32)
- **Total SRAM**: ~320 KB
- **Free after boot**: ~150 KB (estimated)
- **Game usage**: ~50 KB (estimated)
- **Headroom**: ~100 KB for future features

### Battery Life (Estimated)
- **M5Stack Core2 battery**: 390 mAh
- **Screen on (current MVP)**: ~4-6 hours
- **With screen dimming**: 8-10 hours (future optimization)

### File Sizes
```
boot.py:         ~500 bytes
main.py:         ~4 KB
config.py:       ~2 KB
lib/ui.py:       ~10 KB
lib/space_marine.py: ~8 KB
lib/save_manager.py: ~3 KB
Total:           ~28 KB
```

---

## Conclusion

**Day 1 Status**: ✅ **MVP Core Loop Functional**

Successfully deployed a working Tamagotchi-style game to M5Stack Core2 hardware. The game demonstrates:
- Functional UI with touch input
- Real-time stat tracking
- Persistent save/load
- Power management

The biggest technical achievement was successfully migrating from generic MicroPython to UIFlow's M5-specific API, which required understanding:
- Hardware-specific APIs (M5.Lcd, M5.Touch, M5.Power)
- MicroPython limitations vs standard Python
- Touch debouncing and timing with `time.ticks_ms()`
- Proper file deployment to embedded device

The codebase is now in a solid state for iterative development. All core systems (rendering, input, persistence) are proven to work, allowing focus on game mechanics (evolution, minigames, Chaos system) in future sessions.

**For the Emperor! 🦅**

---

*Document created: 2024-12-29*
*Author: Claude Code (Anthropic)*
*Project: Astartes-Gotchi MVP*
