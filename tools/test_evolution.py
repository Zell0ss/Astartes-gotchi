#!/usr/bin/env python3
"""
Evolution System Test Script
Allows testing evolution with accelerated timings

Usage:
1. Deploy to M5Stack: ./tools/deploy.sh
2. In REPL: import tools.test_evolution
3. Or create a temp config with fast evolution
"""

import time

# Accelerated evolution timings (in seconds)
# Normal: 1hr → 2d → 4d
# Test mode: 30s → 60s → 90s

ACCELERATED_TIMINGS = {
    "STAGE_DURATION_NEOPHYTE": 30,        # 30 seconds (was 1 hour)
    "STAGE_DURATION_SCOUT": 60,           # 60 seconds (was 2 days)
    "STAGE_DURATION_BATTLE_BROTHER": 90,  # 90 seconds (was 4 days)
}

def print_evolution_schedule():
    """Print the accelerated evolution schedule"""
    print("\n" + "="*50)
    print("ACCELERATED EVOLUTION SCHEDULE (TEST MODE)")
    print("="*50)
    print(f"Neophyte → Scout:          {ACCELERATED_TIMINGS['STAGE_DURATION_NEOPHYTE']}s")
    print(f"Scout → Battle Brother:    {ACCELERATED_TIMINGS['STAGE_DURATION_SCOUT']}s")
    print(f"Battle Brother → Veteran:  {ACCELERATED_TIMINGS['STAGE_DURATION_BATTLE_BROTHER']}s")
    print(f"\nTotal time to Veteran:     {sum(ACCELERATED_TIMINGS.values())}s ({sum(ACCELERATED_TIMINGS.values())/60:.1f} min)")
    print("="*50 + "\n")

def create_test_config():
    """
    Create a temporary config.py with accelerated timings
    BACKUP YOUR config.py FIRST!
    """
    config_content = f"""# config.py - Astartes-Gotchi Configuration (TEST MODE - ACCELERATED EVOLUTION)
# WARNING: This is a TEST configuration with EXTREMELY fast evolution!
# DO NOT USE FOR NORMAL GAMEPLAY

# ===== GAME METADATA =====
GAME_VERSION = "0.1.0-MVP-TEST"
DEFAULT_MARINE_NAME = "Battle Brother"

# ===== TIMING CONSTANTS =====
FRAME_TIME = 0.1  # 10 FPS (100ms per frame)
UPDATE_INTERVAL = 5  # Update stats every 5 seconds (ACCELERATED)
AUTOSAVE_INTERVAL = 10  # Auto-save every 10 seconds

# ===== EVOLUTION TIMINGS (ACCELERATED FOR TESTING) =====
STAGE_DURATION_NEOPHYTE = {ACCELERATED_TIMINGS['STAGE_DURATION_NEOPHYTE']}  # 30 seconds (was 1 hour)
STAGE_DURATION_SCOUT = {ACCELERATED_TIMINGS['STAGE_DURATION_SCOUT']}  # 60 seconds (was 2 days)
STAGE_DURATION_BATTLE_BROTHER = {ACCELERATED_TIMINGS['STAGE_DURATION_BATTLE_BROTHER']}  # 90 seconds (was 4 days)
# Total: 3 minutes to reach Veteran

# ===== STAT DECAY RATES (ACCELERATED) =====
DECAY_SUSTENANCE = 2  # -2 per update (gentler for testing)
DECAY_BATTLE_FURY = 1  # -1 per update
DECAY_GENESEED_PURITY = 0  # Disabled for testing

# ===== CORRUPTION SYSTEM =====
CORRUPTION_PASSIVE_GAIN = 1  # +1 per 30s (faster)
CORRUPTION_THRESHOLD_CHAOS = 60
CORRUPTION_THRESHOLD_GENESEED_DECAY = 50

# ===== EVOLUTION THRESHOLDS (unchanged) =====
# Loyalist chapters
ULTRAMARINE_DISCIPLINE_MIN = 75
ULTRAMARINE_CORRUPTION_MAX = 20
ULTRAMARINE_CARE_MISTAKES_MAX = 2

GREY_KNIGHT_DISCIPLINE_MIN = 90
GREY_KNIGHT_CORRUPTION_MAX = 0
GREY_KNIGHT_CARE_MISTAKES_MAX = 0
GREY_KNIGHT_WHISPERS_RESISTED_MIN = 10

IMPERIAL_FIST_DISCIPLINE_MIN = 60
IMPERIAL_FIST_COMBAT_EXP_MAX = 50
IMPERIAL_FIST_CORRUPTION_MAX = 30

BLOOD_ANGEL_COMBAT_EXP_MIN = 70
BLOOD_ANGEL_DISCIPLINE_MIN = 40
BLOOD_ANGEL_DISCIPLINE_MAX = 70
BLOOD_ANGEL_CORRUPTION_MAX = 40

SPACE_WOLF_DISCIPLINE_MAX = 50
SPACE_WOLF_SUSTENANCE_MIN = 60
SPACE_WOLF_CORRUPTION_MAX = 35

SALAMANDER_GENESEED_MIN = 70
SALAMANDER_DISCIPLINE_MIN = 50
SALAMANDER_DISCIPLINE_MAX = 80
SALAMANDER_CARE_MISTAKES_MAX = 3

# Chaos paths
KHORNE_COMBAT_EXP_MIN = 80
KHORNE_DISCIPLINE_MAX = 30
KHORNE_CORRUPTION_MIN = 60

SLAANESH_STIMM_COUNT_MIN = 50
SLAANESH_CORRUPTION_MIN = 50

NURGLE_POOP_COUNT_MIN = 20
NURGLE_CORRUPTION_MIN = 55

TZEENTCH_WARP_MEDICINE_REQUIRED = True
TZEENTCH_WHISPERS_ACCEPTED_MIN = 5
TZEENTCH_CORRUPTION_MIN = 65

# ===== FEED SYSTEM =====
FEED_RATION_SUSTENANCE = 20
FEED_CORPSE_STARCH_SUSTENANCE = 20
FEED_CORPSE_STARCH_DISCIPLINE_PENALTY = 5
FEED_CORPSE_STARCH_PENALTY_CHANCE = 0.1

FEED_STIMM_BATTLE_FURY = 15
FEED_STIMM_CORRUPTION = 2

# ===== PRAYER SYSTEM =====
PRAYER_CORRUPTION_REDUCTION = 15
PRAYER_GENESEED_BOOST = 5
PRAYER_DISCIPLINE_BOOST = 5
PRAYER_COOLDOWN = 30  # 30 seconds (was 3 hours)
PRAYER_CORRUPTION_LOCKOUT = 80

# ===== CHAOS WHISPER FREQUENCIES (disabled for evolution testing) =====
WHISPER_FREQUENCY_SCOUT_MIN = 28800
WHISPER_FREQUENCY_SCOUT_MAX = 43200
WHISPER_FREQUENCY_BATTLE_BROTHER_MIN = 14400
WHISPER_FREQUENCY_BATTLE_BROTHER_MAX = 21600
WHISPER_FREQUENCY_VETERAN_MIN = 7200
WHISPER_FREQUENCY_VETERAN_MAX = 14400
WHISPER_TIMEOUT = 30

# ===== MINIGAME SCORING (unchanged) =====
HERESY_CHECK_VICTORY_MIN = 8
HERESY_CHECK_DRAW_MIN = 5
BOLTER_DRILL_VICTORY_KILLS = 15
BOLTER_DRILL_DRAW_KILLS = 10
DODGE_WARP_PERFECT_HITS = 0
DODGE_WARP_VICTORY_HITS = 3
DODGE_WARP_DEFEAT_HITS = 6
DODGE_WARP_SEVERE_HITS = 7

# ===== UI COLORS (RGB888 24-bit format for UIFlow2) =====
COLOR_IMPERIAL_GOLD = 0xFFD700
COLOR_AQUILA_WHITE = 0xFFFFFF
COLOR_PURITY_SEAL = 0xFF0000

# Stats
COLOR_GENESEED = 0x0000FF
COLOR_BATTLE_FURY = 0xFF0000
COLOR_SUSTENANCE = 0x00FF00
COLOR_DISCIPLINE = 0xFFD700
COLOR_CORRUPTION = 0x8B00FF

# Chaos
COLOR_KHORNE = 0xCC0000
COLOR_SLAANESH = 0xFF1493
COLOR_NURGLE = 0x7FFF00
COLOR_TZEENTCH = 0x00BFFF

# UI
COLOR_BG = 0x000000
COLOR_TEXT = 0xFFFFFF
COLOR_BUTTON = 0x404040
COLOR_BUTTON_ACTIVE = 0x808080

# ===== DISPLAY LAYOUT =====
SCREEN_WIDTH = 320
SCREEN_HEIGHT = 240
HEADER_HEIGHT = 30
SPRITE_AREA_HEIGHT = 120
STATS_AREA_HEIGHT = 50
BUTTONS_AREA_HEIGHT = 40
SPRITE_SIZE = 64

# ===== SOUND =====
BEEP_FREQUENCY_FEED = 800
BEEP_FREQUENCY_COMBAT = 1200
BEEP_FREQUENCY_PRAYER = 600
BEEP_FREQUENCY_CORRUPTION = 200
BEEP_FREQUENCY_EVOLUTION = 1000
BEEP_DURATION = 100

# ===== STASIS POD =====
STASIS_DAILY_USES = 1

# ===== DEATH PENALTIES =====
DEATH_CHAOS_CORRUPTION_PENALTY = 10

# ===== DEBUG MODE =====
DEBUG = True  # Keep debug on for testing
"""

    return config_content

def setup_test_environment():
    """
    Setup instructions for test environment
    """
    print_evolution_schedule()
    print("SETUP INSTRUCTIONS:")
    print("1. BACKUP your current config.py:")
    print("   cp src/config.py src/config.py.backup")
    print("\n2. Create test config:")
    print("   python -c \"from tools.test_evolution import create_test_config; print(create_test_config())\" > src/config_test.py")
    print("\n3. Replace config with test config:")
    print("   mv src/config.py src/config_normal.py")
    print("   mv src/config_test.py src/config.py")
    print("\n4. Deploy to device:")
    print("   ./tools/deploy.sh")
    print("\n5. Watch the evolution happen in ~3 minutes!")
    print("\n6. RESTORE normal config when done:")
    print("   mv src/config_normal.py src/config.py")
    print("   ./tools/deploy.sh")
    print()

def test_chapter_prediction():
    """
    Test chapter prediction with various stat combinations
    """
    print("\n" + "="*50)
    print("CHAPTER PREDICTION TEST")
    print("="*50 + "\n")

    # Import after adding parent to path
    import sys
    import os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

    from lib.space_marine import SpaceMarine

    test_cases = [
        {
            "name": "Perfect Marine (Grey Knight)",
            "stats": {
                "discipline": 95,
                "corruption": 0,
                "care_mistakes": 0,
                "chaos_whispers_resisted": 12,
            }
        },
        {
            "name": "Balanced Excellence (Ultramarine)",
            "stats": {
                "discipline": 80,
                "corruption": 15,
                "care_mistakes": 1,
            }
        },
        {
            "name": "Combat Specialist (Blood Angel)",
            "stats": {
                "discipline": 60,
                "combat_experience": 85,
                "corruption": 30,
            }
        },
        {
            "name": "Undisciplined Feaster (Space Wolf)",
            "stats": {
                "discipline": 45,
                "sustenance": 75,
                "corruption": 25,
            }
        },
        {
            "name": "Blood-Crazed Warrior (Khorne)",
            "stats": {
                "discipline": 20,
                "combat_experience": 95,
                "corruption": 70,
            }
        },
        {
            "name": "Stimm Addict (Slaanesh)",
            "stats": {
                "corruption": 65,
                "stimm_count": 60,
            }
        },
    ]

    for test in test_cases:
        marine = SpaceMarine()

        # Apply stats
        for stat, value in test["stats"].items():
            setattr(marine, stat, value)

        # Predict chapter
        chapter = marine._determine_chapter()

        print(f"{test['name']}:")
        print(f"  → {chapter}")
        for stat, value in test["stats"].items():
            print(f"    {stat}: {value}")
        print()

if __name__ == "__main__":
    print("\n🦅 ASTARTES-GOTCHI EVOLUTION TEST SUITE 🦅\n")
    setup_test_environment()
    print("\n" + "-"*50)
    test_chapter_prediction()
