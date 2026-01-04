# 🦅 ASTARTES-GOTCHI

A Warhammer 40K-themed Tamagotchi for M5Stack Core2

> *"In the grim darkness of the far future, there is only war... and care for your Space Marine."*

## Overview

Guide a Space Marine neophyte through training to become a loyal veteran or fall to Chaos corruption. Your care decisions determine the evolution path to 11 possible final forms.

**Platform**: M5Stack Core2 v1.1
**Language**: MicroPython (UIFlow2)
**Status**: MVP Development (~75% complete)

## Features

- ⚔️ **Evolution System** - 4 stages from Neophyte to Veteran
- 🎯 **11 Final Forms** - 6 Loyalist Chapters + 4 Chaos + 1 Secret
- 😈 **Corruption System** - Moral choices that shape evolution
- 💾 **Persistent Saves** - State survives power cycles
- 🎮 **Touch Controls** - Haptic feedback for all interactions
- 🔄 **In-Game Reset** - Quick restart for testing iterations

## Quick Start

**Prerequisites:** M5Stack Core2 v1.1, USB-C cable, Python 3.7+

### 1. Setup Environment
```bash
git clone https://github.com/Zell0ss/Astartes-gotchi.git
cd Astartes-gotchi
./setup.sh  # Linux/macOS
# or setup.bat on Windows
```

### 2. Flash Firmware (First Time Only)
See [SETUP_MICROPYTHON.md](SETUP_MICROPYTHON.md) for detailed instructions.

### 3. Deploy Game
```bash
make deploy  # Default port: /dev/ttyACM0
```

### 4. Play!
The game starts automatically. Use the touchscreen to feed, train, and guide your marine.

## Documentation

- **[CLAUDE.md](CLAUDE.md)** - Complete development guide & architecture
- **[SETUP_MICROPYTHON.md](SETUP_MICROPYTHON.md)** - Firmware installation
- **[DEVELOPMENT_WORKFLOW.md](DEVELOPMENT_WORKFLOW.md)** - VSCode setup
- **[handover_daVinci_to_Code.md](handover_daVinci_to_Code.md)** - Game design document
- **[DEVELOPMENT_DAY*.md](DEVELOPMENT_DAY1.md)** - Daily development logs

## Development Progress

**MVP Status:** ~75% Complete

- ✅ Phase 0: Project structure & tooling
- ✅ Phase 1: Core game loop (stats, saves, UI)
- ✅ Phase 2: Evolution system (4 stages, 11 paths, cutscenes)
- 🚧 Phase 3: Corruption & Chaos Whispers (next)
- ⏳ Phase 4: Minigames
- ⏳ Phase 5-7: Polish, sprites, sound

See [DEVELOPMENT_DAY3.md](DEVELOPMENT_DAY3.md) for latest updates.

## Commands

```bash
make deploy         # Deploy code to device
make console        # Open serial console
make config-fast    # Switch to fast evolution (testing)
make config-normal  # Switch to normal evolution (production)
make config-status  # Show active config
```

## Contributing

This is a personal project by Josem. If you want to contribute ideas or report bugs, feel free to open an issue!

## Credits

- **Design**: Claude "daVinci" (AI Assistant)
- **Implementation**: Claude "Code" (AI Assistant)
- **Development**: Josem (Zelloss)
- **Inspiration**: Tamagotchi (Bandai, 1996) + Warhammer 40K (Games Workshop)

## License

Personal project - no formal license yet.

---

**For the Emperor! 🦅⚔️**
