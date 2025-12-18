# 🦅 ASTARTES-GOTCHI - Claude Code Documentation

## Project Overview

**Astartes-Gotchi** is a Warhammer 40K-themed Tamagotchi for the M5Stack Core2 v1.1 device. Instead of caring for an alien pet, you guide a Space Marine neophyte through training to become either a loyal veteran of the Emperor or fall to Chaos corruption.

**Key Innovation**: A dynamic corruption system that replaces traditional "death by negligence" with moral choices, creating branching evolution paths to 11 different final forms (6 Loyalist Chapters + 4 Chaos variants + 1 secret).

**Hardware**: M5Stack Core2 v1.1 (ESP32-S3, 2.0" touchscreen, battery, IMU, speaker)
**Language**: MicroPython
**Development Style**: Iterative MVP → Feature expansion

---

## Quick Reference

### Essential Documents
- [handover_daVinci_to_Code.md](handover_daVinci_to_Code.md) - Complete GDD and design specifications
- This file (CLAUDE.md) - Development context and guidelines

### Core Mechanics Summary
1. **Stats System**: 5 main stats (Geneseed Purity, Battle Fury, Sustenance, Discipline, Corruption)
2. **Evolution Stages**: Neophyte (1hr) → Scout (2d) → Battle Brother (4d) → Veteran (variable)
3. **Final Forms**: 11 possible outcomes based on care patterns and corruption level
4. **Chaos Whispers**: Random moral choice events that tempt player toward Chaos
5. **Minigames**: "Heresy Check", "Bolter Drill", "Dodge the Warp"
6. **Death System**: Multiple endings (Glorious, Corruption, Negligence, Black Rage)

### Key Design Principles
- **Lore-faithful**: Respect Warhammer 40K canon
- **Tamagotchi DNA**: Preserve core care/evolution mechanics
- **Moral weight**: Choices matter, corruption is insidious
- **Portable gaming**: Touch-based, battery-conscious
- **Iterative development**: MVP first, polish later

---

## Project Architecture

### Directory Structure
```
AstarGotchi/
├── main.py                 # Main game loop entry point
├── lib/                    # Core game modules
│   ├── space_marine.py     # SpaceMarine class (stats, evolution logic)
│   ├── ui.py               # AstartesUI class (rendering, touch handling)
│   ├── minigames/
│   │   ├── heresy_check.py
│   │   ├── bolter_drill.py
│   │   └── dodge_warp.py
│   ├── chaos_system.py     # Chaos Whispers and corruption mechanics
│   ├── evolution.py        # Chapter determination algorithms
│   └── save_manager.py     # Save/load persistent state
├── assets/
│   ├── sprites/            # 64x64 PNG sprites for all stages/chapters
│   ├── sounds/             # SFX (beeps, alerts)
│   └── fonts/              # Custom gothic fonts (optional)
├── config.py               # Game constants (decay rates, thresholds)
├── utils.py                # Helper functions
└── tests/                  # Unit tests for core systems
```

### Core Classes

#### `SpaceMarine` (space_marine.py)
```python
class SpaceMarine:
    # Main stats
    geneseed_purity: int (0-100)
    battle_fury: int (0-100)
    sustenance: int (0-100)
    discipline: int (0-100)
    corruption: int (0-100)

    # Tracking stats
    combat_experience: int
    care_mistakes: int
    chaos_whispers_resisted: int
    chaos_whispers_accepted: int

    # Methods
    update()                    # Passive decay/time-based changes
    feed(food_type)             # Feed actions
    combat_training(game, result) # Minigame results
    chaos_whisper_response(god, choice)
    evolve()                    # Stage progression
    _determine_chapter()        # Evolution algorithm
    die(cause)                  # Death sequences
```

#### `AstartesUI` (ui.py)
```python
class AstartesUI:
    # Display rendering
    render(marine)              # Full screen update
    draw_marine_sprite(marine)  # Sprite rendering
    draw_stats(marine)          # Stat bars
    draw_buttons()              # Touch UI

    # Special screens
    handle_chaos_whisper(god)   # Chaos event UI
    handle_minigame(game_type)  # Minigame launcher
    show_evolution_cutscene(chapter) # Evolution cinematics
    show_death_sequence(cause)  # Death endings
```

#### `ChaosSystem` (chaos_system.py)
```python
class ChaosWhisper:
    trigger(marine)             # Check if whisper should appear
    present(god)                # Show whisper UI
    apply_choice(god, choice, marine) # Apply consequences

# 4 god-specific whisper types:
# - Khorne: Triggered by low battle_fury
# - Slaanesh: Triggered by excessive stimm use
# - Nurgle: Triggered by sickness + dirt
# - Tzeentch: Random, 10% chance/hour
```

---

## Development Workflow

### Phase 1: MVP Core Loop (Current Priority)
**Goal**: Functional game with basic care mechanics

**Tasks**:
1. Setup M5Stack Core2 with MicroPython firmware
2. Implement `SpaceMarine` class with basic stats and decay
3. Create simple UI with stat bars and 3 buttons (Feed, Clean, Status)
4. Implement save/load system
5. Test: Keep marine alive for 24 hours

**Success Criteria**:
- Marine stats decay over time
- Can feed to restore sustenance
- Can view status screen
- State persists across device reboots

### Phase 2: Evolution System
**Goal**: Complete lifecycle from Neophyte to Veteran

**Tasks**:
1. Implement 4 evolution stages with time triggers
2. Create chapter determination algorithm
3. Add 4 initial chapters (Ultramarine, Space Wolf, Khorne, Plague Marine)
4. Placeholder sprites for each stage
5. Test: Complete 2-3 full runs

### Phase 3: Corruption & Chaos
**Goal**: Moral choice system operational

**Tasks**:
1. Implement corruption stat and passive gain
2. Create Chaos Whisper system (2 gods minimum)
3. Add Prayer action to counter corruption
4. Test: Intentionally fall to Chaos vs resist

### Phase 4: Minigames
**Goal**: Interactive combat training

**Tasks**:
1. Build "Heresy Check" minigame
2. Build "Bolter Drill" minigame
3. Integrate results with stats
4. Polish touch controls

### Phase 5-7: Polish, Balance, Extras
(See roadmap in handover document)

---

## Technical Guidelines

### MicroPython Best Practices
```python
# Memory efficiency (ESP32 has limited RAM)
- Use `const()` for constants
- Reuse objects instead of creating new ones
- Clear large buffers after use
- Use generators for large iterations

# Touch handling
from m5stack import Touch
touch = Touch()
if touch.get_count() > 0:
    detail = touch.get_detail(0)
    x, y = detail[1], detail[2]
    # Handle tap at (x, y)

# Display rendering
from m5stack import LCD
lcd = LCD()
lcd.clear(0x0000)  # Black
lcd.rect(x, y, w, h, color, fill_color)
lcd.print(text, x, y, color)

# Save/load (use JSON for simplicity)
import json
with open('save.json', 'w') as f:
    json.dump(marine.to_dict(), f)
```

### Code Style
- **Language**: Python 3.x (MicroPython compatible)
- **Naming**:
  - Classes: `PascalCase` (SpaceMarine, AstartesUI)
  - Functions/vars: `snake_case` (geneseed_purity, feed_ration)
  - Constants: `UPPER_SNAKE_CASE` (STAGE_NEOPHYTE, COLOR_CHAOS_PURPLE)
- **Documentation**: Docstrings for all classes/public methods
- **Comments**: Explain WHY, not WHAT (code should be self-documenting)

### Performance Targets
- **FPS**: 10 FPS minimum for UI updates
- **Battery**: 4-6 hours continuous use
- **Responsiveness**: Touch input lag < 100ms
- **Boot time**: < 5 seconds from power-on to game screen

---

## Evolution Algorithm (Critical Logic)

### Loyalist Chapters
```python
def _determine_chapter(self):
    if self.corruption < 60:  # Loyalist threshold
        # Grey Knight (secret - perfection required)
        if (self.discipline >= 90 and self.corruption == 0 and
            self.care_mistakes == 0 and self.chaos_whispers_resisted >= 10):
            return CHAPTER_GREY_KNIGHT

        # Ultramarine (balanced excellence)
        elif (self.discipline >= 75 and self.care_mistakes <= 2 and
              self.corruption < 20):
            return CHAPTER_ULTRAMARINE

        # Imperial Fist (high discipline, low combat)
        elif (self.discipline >= 60 and self.combat_experience < 50):
            return CHAPTER_IMPERIAL_FIST

        # Blood Angel (high combat, medium discipline)
        elif (self.combat_experience > 70 and 40 <= self.discipline <= 70):
            return CHAPTER_BLOOD_ANGEL

        # Space Wolf (low discipline, high sustenance)
        elif (self.discipline <= 50 and self.sustenance > 60):
            return CHAPTER_SPACE_WOLF

        # Salamander (high geneseed, low care mistakes)
        elif (self.geneseed_purity > 70 and self.care_mistakes < 3):
            return CHAPTER_SALAMANDER

    else:  # Chaos paths (corruption >= 60)
        # Khorne (violence)
        if self.combat_experience > 80 and self.discipline < 30:
            return CHAOS_KHORNE

        # Slaanesh (excess)
        elif self.stimm_count > 50:
            return CHAOS_SLAANESH

        # Nurgle (decay)
        elif self.poop_accumulation > 20:
            return CHAOS_NURGLE

        # Tzeentch (sorcery)
        elif self.warp_medicine_unlocked and self.chaos_whispers_accepted > 5:
            return CHAOS_TZEENTCH

    # Default fallback
    return CHAPTER_ULTRAMARINE
```

**Key Insight**: This algorithm creates meaningful gameplay where HOW you care determines the outcome, not just success/failure.

---

## Chaos Whisper Design Pattern

Each whisper follows this structure:

```python
{
    "god": "khorne",  # or slaanesh, nurgle, tzeentch
    "trigger_condition": lambda marine: marine.battle_fury < 30,
    "text": "Blood calls to blood, warrior...",
    "resist": {
        "action": "hold_button_10s",  # Mini challenge
        "success": {
            "discipline": +15,
            "corruption": -10
        },
        "fail": {
            "corruption": +20
        }
    },
    "give_in": {
        "battle_fury": +30,
        "corruption": +25,
        "marks": {"khorne": +1}
    }
}
```

**Frequency Schedule**:
- Scout: 1 whisper every 8-12 hours
- Battle Brother: 1 every 4-6 hours
- Veteran: 1 every 2-4 hours

---

## UI Color Palette (RGB565 Hex)

```python
# Imperial/Loyalist
COLOR_IMPERIAL_GOLD = 0xFEA0
COLOR_AQUILA_WHITE = 0xFFFF
COLOR_PURITY_SEAL = 0xF800

# Stats
COLOR_GENESEED = 0x001F      # Blue (purity)
COLOR_BATTLE_FURY = 0xF800   # Red (combat)
COLOR_SUSTENANCE = 0x07E0    # Green (food)
COLOR_DISCIPLINE = 0xFEA0    # Gold (codex)
COLOR_CORRUPTION = 0x8010    # Purple (chaos)

# Chaos
COLOR_KHORNE = 0xC800        # Blood red
COLOR_SLAANESH = 0xF81F      # Pink/purple
COLOR_NURGLE = 0x7E0         # Putrid green
COLOR_TZEENTCH = 0x019F      # Arcane blue

# UI
COLOR_BG = 0x0000            # Black
COLOR_TEXT = 0xFFFF          # White
COLOR_BUTTON = 0x4208        # Dark grey
COLOR_BUTTON_ACTIVE = 0x7BEF # Light grey
```

---

## Testing Strategy

### Unit Tests
```python
# Test stat decay
def test_sustenance_decay():
    marine = SpaceMarine()
    marine.sustenance = 100
    marine.update()  # Simulate 1 minute
    assert marine.sustenance == 95  # -5 per minute

# Test evolution algorithm
def test_ultramarine_evolution():
    marine = SpaceMarine()
    marine.discipline = 80
    marine.corruption = 15
    marine.care_mistakes = 1
    marine.current_stage = STAGE_BATTLE_BROTHER
    marine.evolve()
    assert marine.final_chapter == CHAPTER_ULTRAMARINE
```

### Integration Tests (on device)
1. **24-hour endurance**: Leave running overnight, check for crashes
2. **Touch responsiveness**: Rapid tapping all buttons
3. **Battery drain**: Measure mAh consumption per hour
4. **Save integrity**: Power cycle 10 times, verify state

### Playtest Scenarios
1. **Perfect run**: Try to get Grey Knight (hardest path)
2. **Chaos run**: Intentionally fall to each god
3. **Neglect run**: Ignore completely, observe care_mistakes
4. **Combat spam**: Play only minigames, see Blood Angel path

---

## Common Pitfalls & Solutions

### Issue: Stats reach 0 too quickly
**Solution**: Adjust decay rates in `config.py`. Start conservative (slower decay) and tune based on playtesting.

### Issue: Evolution feels arbitrary
**Solution**: Add visual feedback. Show a "tendency meter" on status screen indicating current chapter trajectory.

### Issue: Chaos Whispers too frequent/annoying
**Solution**: Implement "cooldown" - no whisper within 2 hours of previous one.

### Issue: Minigames too easy/hard
**Solution**: Dynamic difficulty - scale based on `combat_experience` stat.

### Issue: Battery drains too fast
**Solution**:
- Reduce LCD refresh rate (10 FPS → 5 FPS)
- Dim screen after 30s of no interaction
- Use sleep mode during idle animations

### Issue: Save file corruption
**Solution**: Atomic writes - write to temp file, then rename. Keep backup of previous save.

---

## Design Decisions (CONFIRMED)

**✅ Decisions made with Josem (2024-12-18):**

1. **Permadeath severity**: ✅ YES - Chaos corruption death applies +10 corruption penalty to next run (adds dramatic weight)

2. **Pause mechanism**: ✅ "Stasis Pod" - Lore-friendly pause, 1 use per day maximum
   - Visual: Cryo-chamber animation
   - Limitation: 1x daily use encourages commitment

3. **Language**: ✅ ENGLISH - All UI text in English
   - Reasoning: Warhammer lore resonates better in English ("HERESY!", "Emperor protects")
   - Better for project reach/sharing

4. **Audio scope**: ✅ Start with simple beeps, evolve to SFX
   - MVP: Basic beeps for feedback
   - V1.0 goal: Retro SFX (M5Stack speaker will add natural retro character)

5. **Difficulty settings**: ✅ Single balanced mode
   - One carefully tuned experience
   - No Easy/Normal/Hard modes

---

## Known Warhammer 40K Lore Details (For Reference)

### Space Marine Creation Process
1. **Recruitment** (age 10-14): Chosen from toughest youths
2. **Neophyte training** (1-2 years): Implant begins, basic training
3. **Scout** (variable): Light armor, reconnaissance missions
4. **Black Carapace** (final implant): Allows interface with power armor
5. **Battle Brother** (full Astartes): Assigned to Chapter
6. **Veteran** (centuries): Survived many campaigns

### Chaos Gods (The Ruinous Powers)
- **Khorne**: Blood, skulls, endless war, martial honor perverted
- **Slaanesh**: Excess, pleasure, perfection twisted into obsession
- **Nurgle**: Decay, disease, "Grandfather" who loves his children
- **Tzeentch**: Change, scheming, forbidden knowledge, mutation

### Key Phrases (For UI flavor)
- "The Emperor protects"
- "For the Emperor!"
- "Purge the heretic, the mutant, the xeno"
- "Know no fear"
- "In the grim darkness of the far future, there is only war"
- "Even in death I still serve" (Dreadnought motto)
- "Blood for the Blood God!" (Khorne)
- "All is dust" (Thousand Sons/Tzeentch)

---

## Success Metrics

### MVP Success
- [ ] Marine survives 24 hours with active care
- [ ] Can complete full lifecycle (Neophyte → Veteran)
- [ ] At least 2 different chapter outcomes achieved
- [ ] Chaos Whisper appears and functions correctly
- [ ] Save/load works across power cycles
- [ ] No critical bugs
- [ ] Battery lasts 4+ hours

### V1.0 Success
- [ ] All 11 evolution paths functional
- [ ] All 4 Chaos Whisper types implemented
- [ ] 3 minigames complete and fun
- [ ] Special endings (Primaris, Dreadnought) working
- [ ] Sprites/animations polished
- [ ] SFX and haptic feedback
- [ ] Code clean and documented
- [ ] Josem enjoys playing it! 😄

---

## Communication Protocol with Josem

### When Starting a Session
1. Read latest commits/changes
2. Ask about priorities for current session
3. Clarify any ambiguous design decisions
4. Agree on concrete deliverable for session

### During Development
- Show code snippets for review before full implementation
- Explain technical tradeoffs when multiple approaches exist
- Test on device frequently (not just in simulation)
- Ask for playtesting feedback early and often

### When Stuck
- Explain the problem clearly
- Present 2-3 solution options with pros/cons
- Make a recommendation
- Let Josem decide

### When Completing a Feature
- Demo the working feature
- Ask for feedback
- Note any rough edges or technical debt
- Update this document if architecture changed

---

## Version History

**v1.0** (2024-12-18 - Initial Creation)
- Created by Claude Code based on handover from Claude DaVinci
- Established development guidelines and architecture
- Defined MVP roadmap and success criteria

---

## Final Notes

This is a **passion project** for Josem - it should be fun to build and fun to play. Don't over-engineer. Ship early, iterate often.

The beauty of this concept is the fusion of nostalgia (Tamagotchi) with epic lore (40K). Keep both elements strong. Every design choice should ask: "Is this true to Tamagotchi mechanics?" AND "Is this true to 40K lore?"

When in doubt, refer to the handover document. Claude DaVinci did excellent design work - trust it.

**For the Emperor! 🦅⚔️**

---

*This document is a living reference. Update it as the project evolves.*
