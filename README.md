# 🦅 ASTARTES-GOTCHI

A Warhammer 40,000 themed Tamagotchi for M5Stack Core2

> *"In the grim darkness of the far future, there is only war... and care for your Space Marine."*

## Overview

Guide a Space Marine neophyte from recruitment to becoming a veteran of the Emperor... or falling to the corruption of Chaos. Your care decisions determine whether your marine becomes a noble Ultramarine, a savage Space Wolf, or a corrupted Chaos warrior.

**Platform**: M5Stack Core2 v1.1
**Language**: MicroPython
**Status**: MVP Development (v0.1.0)

## Features (Planned)

- 🎮 **Classic Tamagotchi Mechanics** - Feed, train, clean, discipline
- ⚔️ **Warhammer 40K Lore** - 11 evolution paths (6 Loyalist + 4 Chaos + 1 Secret)
- 😈 **Chaos Corruption System** - Moral choices that matter
- 🎯 **Minigames** - Heresy Check, Bolter Drill, Dodge the Warp
- 💾 **Persistent Save System** - Your marine lives across power cycles
- 🔊 **Retro Audio** - Classic beeps with 40K flavor

## Quick Start

### Prerequisites

- M5Stack Core2 v1.1 device
- Python 3.7+ on your PC
- USB-C cable

### Setup

1. **Flash MicroPython** (first time only):
   ```bash
   # See SETUP_MICROPYTHON.md for detailed instructions
   pip install esptool mpremote
   esptool --chip esp32s3 --port /dev/ttyUSB0 erase_flash
   esptool --chip esp32s3 --port /dev/ttyUSB0 write_flash -z 0x0 firmware.bin
   ```

2. **Clone this repository**:
   ```bash
   git clone <repo-url>
   cd AstarGotchi
   ```

3. **Deploy to device**:

   **Linux/macOS:**
   ```bash
   ./tools/deploy.sh /dev/ttyUSB0
   ```

   **Windows:**
   ```cmd
   tools\deploy.bat COM3
   ```

4. **Play!** 🎮

## Project Structure

```
AstarGotchi/
├── src/                    # Source code (deployed to device)
│   ├── boot.py             # Boot sequence
│   ├── main.py             # Main game loop
│   ├── config.py           # Game constants
│   └── lib/                # Game modules
│       ├── space_marine.py # Marine logic
│       ├── ui.py           # Display/input
│       ├── save_manager.py # Save/load
│       ├── chaos_system.py # Chaos whispers
│       └── minigames/      # Minigame modules
├── tools/                  # Development scripts
│   ├── deploy.sh           # Linux deployment
│   └── deploy.bat          # Windows deployment
├── CLAUDE.md               # Development documentation
├── SETUP_MICROPYTHON.md    # MicroPython setup guide
└── DEVELOPMENT_WORKFLOW.md # Development workflow
```

## Documentation

- **[CLAUDE.md](CLAUDE.md)** - Full development guide and architecture
- **[SETUP_MICROPYTHON.md](SETUP_MICROPYTHON.md)** - MicroPython installation
- **[DEVELOPMENT_WORKFLOW.md](DEVELOPMENT_WORKFLOW.md)** - VSCode setup and workflows
- **[handover_daVinci_to_Code.md](handover_daVinci_to_Code.md)** - Complete game design document

## Development

### Using VSCode + PyMakr

1. Install PyMakr extension
2. Configure `.pymakr.conf` with your serial port
3. Edit code in `src/`
4. Upload with `Ctrl+Shift+U`

### Using Command Line

```bash
# Upload files
mpremote connect /dev/ttyUSB0 cp -r src/* :

# Connect to REPL
mpremote connect /dev/ttyUSB0 repl

# Run script
mpremote connect /dev/ttyUSB0 run src/main.py
```

## Roadmap

### Phase 1: MVP Core Loop ✅ (In Progress)
- [x] Project structure
- [x] SpaceMarine class with basic stats
- [x] Simple UI (console mode)
- [x] Save/load system
- [ ] Deploy to actual hardware
- [ ] Test basic gameplay loop

### Phase 2: Evolution System
- [ ] 4 evolution stages
- [ ] Chapter determination algorithm
- [ ] 4 initial evolutions (Ultramarine, Space Wolf, Khorne, Nurgle)
- [ ] Evolution cutscenes

### Phase 3: Corruption & Chaos
- [ ] Chaos Whisper events
- [ ] Prayer system
- [ ] Corruption visual effects

### Phase 4: Minigames
- [ ] Heresy Check minigame
- [ ] Bolter Drill minigame
- [ ] Touch controls

### Phase 5-7: Polish
- [ ] All 11 evolutions
- [ ] Sprites and animations
- [ ] Sound effects
- [ ] Balance tuning

## Contributing

This is a personal project by Josem. If you want to contribute ideas or report bugs, feel free to open an issue!

## Credits

- **Design**: Claude "daVinci" (AI Assistant)
- **Implementation**: Claude "Code" (AI Assistant)
- **Development**: Josem (Zelloss)
- **Inspiration**: Tamagotchi (Bandai, 1996) + Warhammer 40,000 (Games Workshop)

## License

Personal project - no formal license yet.

---

**For the Emperor! 🦅⚔️**
