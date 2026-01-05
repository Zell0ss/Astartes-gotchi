# config.py - Astartes-Gotchi Configuration
# All game constants and tuning parameters

# ===== GAME METADATA =====
GAME_VERSION = "0.1.0-MVP"
DEFAULT_MARINE_NAME = "Battle Brother"

# ===== TIMING CONSTANTS =====
FRAME_TIME = 0.1  # 10 FPS (100ms per frame)
UPDATE_INTERVAL = 60  # Update stats every 60 seconds (1 minute)
AUTOSAVE_INTERVAL = 30  # Auto-save every 30 seconds

# ===== EVOLUTION TIMINGS (in seconds) =====
STAGE_DURATION_NEOPHYTE = 3600  # 1 hour
STAGE_DURATION_SCOUT = 172800  # 2 days (48 hours)
STAGE_DURATION_BATTLE_BROTHER = 345600  # 4 days (96 hours)
# Veteran stage has no time limit - lives until death

# ===== STAT DECAY RATES (per UPDATE_INTERVAL) =====
DECAY_SUSTENANCE = 5  # -5 per minute
DECAY_BATTLE_FURY = 3  # -3 per 90 seconds (adjust in update logic)
DECAY_GENESEED_PURITY = 1  # -1 per 2 hours (when corrupted)

# ===== CORRUPTION SYSTEM =====
CORRUPTION_PASSIVE_GAIN = 1  # +1 per 3 hours (slow but inevitable)
CORRUPTION_THRESHOLD_CHAOS = 60  # >= 60 corruption = Chaos path
CORRUPTION_THRESHOLD_GENESEED_DECAY = 50  # Geneseed starts decaying

# ===== EVOLUTION THRESHOLDS =====
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
FEED_CORPSE_STARCH_PENALTY_CHANCE = 0.1  # 10%

FEED_STIMM_BATTLE_FURY = 15
FEED_STIMM_CORRUPTION = 2

# ===== PRAYER SYSTEM =====
PRAYER_CORRUPTION_REDUCTION = 15
PRAYER_GENESEED_BOOST = 5
PRAYER_DISCIPLINE_BOOST = 5
PRAYER_COOLDOWN = 10800  # 3 hours in seconds
PRAYER_CORRUPTION_LOCKOUT = 80  # Can't pray if corruption > 80

# ===== CHAOS WHISPER SYSTEM (PRODUCTION TIMING) =====
# Emperor's Whisper
EMPEROR_WHISPER_CHANCE = 0.12  # 12% chance to get Emperor whisper instead of Chaos

# Cooldowns (PRODUCTION)
WHISPER_COOLDOWN_GLOBAL = 7200  # 2 hours between ANY whispers
WHISPER_COOLDOWN_PER_GOD = 14400  # 4 hours before same god can appear again

# Stage-based frequencies (minimum time between whispers)
WHISPER_FREQUENCY_NEOPHYTE = 43200  # 12 hours (rare for beginners)
WHISPER_FREQUENCY_SCOUT = 28800  # 8 hours
WHISPER_FREQUENCY_BATTLE_BROTHER = 21600  # 6 hours
WHISPER_FREQUENCY_VETERAN = 14400  # 4 hours (constant temptation)

# Khorne Challenge (Rapid Tapping)
KHORNE_TAP_TARGET = 30  # 30 taps required
KHORNE_DURATION = 10.0  # 10 seconds to complete

# Slaanesh Challenge (Slow Drag)
SLAANESH_MIN_TIME = 8.0  # Minimum drag duration (seconds)
SLAANESH_MAX_TIME = 12.0  # Maximum drag duration (seconds)
SLAANESH_MIN_DISTANCE = 250  # Minimum pixels to drag
SLAANESH_MAX_SPEED = 40  # Maximum pixels/second (enforced!)

# Nurgle Challenge (Stillness)
NURGLE_DURATION = 10.0  # 10 seconds of stillness
NURGLE_MOVEMENT_THRESHOLD = 0.2  # G-force threshold (needs IMU calibration)

# Tzeentch Challenge (Shake/Rotate)
TZEENTCH_DURATION = 8.0  # 8 seconds to complete
TZEENTCH_SHAKE_THRESHOLD = 1.5  # G-force threshold (needs IMU calibration)
TZEENTCH_REQUIRED_SHAKES = 15  # Required shake count

# ===== MINIGAME SCORING =====
# Heresy Check
HERESY_CHECK_VICTORY_MIN = 8  # 8/10 correct
HERESY_CHECK_DRAW_MIN = 5  # 5/10 correct

# Bolter Drill
BOLTER_DRILL_VICTORY_KILLS = 15  # 15+ kills without friendly fire
BOLTER_DRILL_DRAW_KILLS = 10  # 10-14 kills

# Dodge Warp
DODGE_WARP_PERFECT_HITS = 0  # 0 hits = perfect
DODGE_WARP_VICTORY_HITS = 3  # 1-3 hits = victory
DODGE_WARP_DEFEAT_HITS = 6  # 4-6 hits = defeat
DODGE_WARP_SEVERE_HITS = 7  # 7+ hits = severe defeat

# ===== UI COLORS (RGB888 24-bit format for UIFlow2) =====
# UIFlow2 uses 24-bit RGB (0xRRGGBB), NOT RGB565!

# Imperial/Loyalist
COLOR_IMPERIAL_GOLD = 0xFFD700      # Gold
COLOR_AQUILA_WHITE = 0xFFFFFF       # White
COLOR_PURITY_SEAL = 0xFF0000        # Red

# Stats
COLOR_GENESEED = 0x0000FF           # Blue (purity)
COLOR_BATTLE_FURY = 0xFF0000        # Red (combat)
COLOR_SUSTENANCE = 0x00FF00         # Green (food)
COLOR_DISCIPLINE = 0xFFD700         # Gold (codex)
COLOR_CORRUPTION = 0x8B00FF         # Purple (chaos)

# Chaos
COLOR_KHORNE = 0xCC0000             # Blood red
COLOR_SLAANESH = 0xFF1493           # Deep pink
COLOR_NURGLE = 0x7FFF00             # Chartreuse (putrid green)
COLOR_TZEENTCH = 0x00BFFF           # Deep sky blue

# UI
COLOR_BG = 0x000000                 # Black
COLOR_TEXT = 0xFFFFFF               # White
COLOR_BUTTON = 0x404040             # Dark grey
COLOR_BUTTON_ACTIVE = 0x808080      # Light grey

# ===== DISPLAY LAYOUT (320x240 screen) =====
SCREEN_WIDTH = 320
SCREEN_HEIGHT = 240

HEADER_HEIGHT = 30
SPRITE_AREA_HEIGHT = 120
STATS_AREA_HEIGHT = 50
BUTTONS_AREA_HEIGHT = 40

SPRITE_SIZE = 64  # 64x64 sprite

# ===== SOUND =====
BEEP_FREQUENCY_FEED = 800  # Hz
BEEP_FREQUENCY_COMBAT = 1200
BEEP_FREQUENCY_PRAYER = 600
BEEP_FREQUENCY_CORRUPTION = 200
BEEP_FREQUENCY_EVOLUTION = 1000

BEEP_DURATION = 100  # milliseconds

# ===== STASIS POD =====
STASIS_DAILY_USES = 1  # Can only use stasis pod once per day

# ===== DEATH PENALTIES =====
DEATH_CHAOS_CORRUPTION_PENALTY = 10  # +10 base corruption next run

# ===== DEBUG MODE =====
DEBUG = True  # Set to False for production
