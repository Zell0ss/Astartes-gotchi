# lib/space_marine.py - Space Marine Core Class
# Contains all game logic for the marine entity

import time
import random
import config

class SpaceMarine:
    """
    Represents a Space Marine and all game state.
    Based on Tamagotchi mechanics adapted to Warhammer 40K.
    """

    # Evolution stages
    STAGE_NEOPHYTE = 0
    STAGE_SCOUT = 1
    STAGE_BATTLE_BROTHER = 2
    STAGE_VETERAN = 3

    # Loyalist chapters
    CHAPTER_ULTRAMARINE = "ultramarine"
    CHAPTER_GREY_KNIGHT = "grey_knight"
    CHAPTER_IMPERIAL_FIST = "imperial_fist"
    CHAPTER_BLOOD_ANGEL = "blood_angel"
    CHAPTER_SPACE_WOLF = "space_wolf"
    CHAPTER_SALAMANDER = "salamander"

    # Chaos legions
    CHAOS_KHORNE = "khorne_berserker"
    CHAOS_SLAANESH = "noise_marine"
    CHAOS_NURGLE = "plague_marine"
    CHAOS_TZEENTCH = "thousand_sons"
    CHAOS_UNDIVIDED = "chaos_undivided"

    def __init__(self, name="Battle Brother"):
        """Initialize a new Space Marine neophyte"""

        # ===== MAIN STATS =====
        self.geneseed_purity = 100
        self.battle_fury = 50
        self.sustenance = 50
        self.discipline = 50
        self.corruption = 0

        # ===== TRACKING STATS =====
        self.combat_experience = 0
        self.care_mistakes = 0
        self.discipline_failures = 0
        self.chaos_whispers_resisted = 0
        self.chaos_whispers_accepted = 0
        self.battles_won = 0
        self.battles_lost = 0

        # ===== CHAOS MARKS =====
        self.khorne_marks = 0
        self.slaanesh_marks = 0
        self.nurgle_marks = 0
        self.tzeentch_marks = 0

        # ===== COUNTERS =====
        self.stimm_count = 0
        self.poop_accumulation = 0

        # ===== METADATA =====
        self.name = name
        self.age_cycles = 0
        self.birth_timestamp = time.time()
        self.last_update = time.time()
        self.current_stage = self.STAGE_NEOPHYTE
        self.final_chapter = None
        self.is_alive = True
        self.death_cause = None

        # ===== FLAGS =====
        self.warp_medicine_unlocked = False
        self.in_black_rage = False
        self.is_dreadnought = False
        self.last_prayer_time = 0

        if config.DEBUG:
            print(f">>> SpaceMarine created: {self.name}")

    def update(self):
        """
        Passive stat updates (decay, corruption gain, etc.)
        Called every config.UPDATE_INTERVAL seconds
        """
        if not self.is_alive:
            return

        current_time = time.time()
        elapsed = current_time - self.last_update

        if elapsed >= config.UPDATE_INTERVAL:
            # Stat decay
            self.sustenance = max(0, self.sustenance - config.DECAY_SUSTENANCE)

            # Battle fury decays slower (every 90 seconds)
            if elapsed >= 90:
                self.battle_fury = max(0, self.battle_fury - config.DECAY_BATTLE_FURY)

            # Corruption increases passively (every 3 hours)
            if elapsed >= 10800:  # 3 hours
                self.corruption = min(100, self.corruption + config.CORRUPTION_PASSIVE_GAIN)

            # Geneseed decay if corrupted
            if self.corruption > config.CORRUPTION_THRESHOLD_GENESEED_DECAY:
                if elapsed >= 7200:  # Every 2 hours
                    self.geneseed_purity = max(0, self.geneseed_purity - config.DECAY_GENESEED_PURITY)

            # Check death conditions
            if self.geneseed_purity <= 0:
                self.die("geneseed_failure")
            elif self.corruption >= 100:
                self.die("chaos_corruption")

            self.last_update = current_time

            if config.DEBUG:
                print(f">>> Update: Sust={self.sustenance}, Fury={self.battle_fury}, Corrupt={self.corruption}")

    def feed(self, food_type="ration"):
        """Feed the marine"""
        if not self.is_alive:
            return False

        if food_type == "ration":
            self.sustenance = min(100, self.sustenance + config.FEED_RATION_SUSTENANCE)
            if config.DEBUG:
                print(f">>> Fed ration. Sustenance: {self.sustenance}")

        elif food_type == "corpse_starch":
            self.sustenance = min(100, self.sustenance + config.FEED_CORPSE_STARCH_SUSTENANCE)
            # 10% chance to lose discipline (tastes terrible)
            if random.random() < config.FEED_CORPSE_STARCH_PENALTY_CHANCE:
                self.discipline = max(0, self.discipline - config.FEED_CORPSE_STARCH_DISCIPLINE_PENALTY)
                if config.DEBUG:
                    print(">>> Corpse starch penalty triggered!")

        elif food_type == "stimm":
            self.battle_fury = min(100, self.battle_fury + config.FEED_STIMM_BATTLE_FURY)
            self.corruption = min(100, self.corruption + config.FEED_STIMM_CORRUPTION)
            self.stimm_count += 1
            if config.DEBUG:
                print(f">>> Stimm consumed. Total: {self.stimm_count}")

        return True

    def pray(self):
        """
        Prayer to the Emperor - reduces corruption
        Cooldown: 3 hours
        """
        if not self.is_alive:
            return False

        current_time = time.time()
        time_since_prayer = current_time - self.last_prayer_time

        # Check cooldown
        if time_since_prayer < config.PRAYER_COOLDOWN:
            if config.DEBUG:
                remaining = config.PRAYER_COOLDOWN - time_since_prayer
                print(f">>> Prayer on cooldown: {remaining:.0f}s remaining")
            return False

        # Check corruption lockout
        if self.corruption > config.PRAYER_CORRUPTION_LOCKOUT:
            if config.DEBUG:
                print(">>> Too corrupted to pray!")
            return False

        # Apply prayer effects
        self.corruption = max(0, self.corruption - config.PRAYER_CORRUPTION_REDUCTION)
        self.geneseed_purity = min(100, self.geneseed_purity + config.PRAYER_GENESEED_BOOST)
        self.discipline = min(100, self.discipline + config.PRAYER_DISCIPLINE_BOOST)
        self.last_prayer_time = current_time

        if config.DEBUG:
            print(f">>> Prayer successful. Corruption: {self.corruption}")

        return True

    def clean(self):
        """Clean bolter casings and battle damage"""
        if not self.is_alive:
            return False

        self.poop_accumulation = 0
        if config.DEBUG:
            print(">>> Armor maintenance complete")
        return True

    def discipline_drill(self):
        """
        Codex Astartes discipline drill
        Called when marine rebels (discipline check)
        """
        if not self.is_alive:
            return

        # Success: restore discipline
        self.discipline = min(100, self.discipline + 25)
        self.corruption = max(0, self.corruption - 5)

        if config.DEBUG:
            print(f">>> Discipline restored: {self.discipline}")

    def combat_training(self, game_type, result):
        """
        Process minigame results

        Args:
            game_type: "heresy_check", "bolter_drill", "dodge_warp"
            result: "victory", "draw", "defeat"
        """
        if not self.is_alive:
            return

        if result == "victory":
            self.battle_fury = min(100, self.battle_fury + 3)
            self.combat_experience += 5
            self.battles_won += 1

            if game_type == "heresy_check":
                self.discipline = min(100, self.discipline + 1)
                self.corruption = max(0, self.corruption - 5)

        elif result == "draw":
            self.battle_fury = min(100, self.battle_fury + 1)
            self.combat_experience += 2

        else:  # defeat
            self.battles_lost += 1
            if game_type == "heresy_check":
                self.corruption = min(100, self.corruption + 10)
                self.discipline = max(0, self.discipline - 2)

        if config.DEBUG:
            print(f">>> Combat result: {result}. Exp: {self.combat_experience}")

    def chaos_whisper_response(self, god, choice):
        """
        Handle Chaos Whisper player choice

        Args:
            god: "khorne", "slaanesh", "nurgle", "tzeentch"
            choice: "resist" or "give_in"
        """
        if not self.is_alive:
            return

        if choice == "resist":
            self.chaos_whispers_resisted += 1
            self.discipline = min(100, self.discipline + 10)
            self.corruption = max(0, self.corruption - 10)

            if config.DEBUG:
                print(f">>> Resisted {god}. Total resisted: {self.chaos_whispers_resisted}")

        else:  # give_in
            self.chaos_whispers_accepted += 1

            if god == "khorne":
                self.battle_fury = min(100, self.battle_fury + 30)
                self.corruption = min(100, self.corruption + 25)
                self.khorne_marks += 1

            elif god == "slaanesh":
                self.battle_fury = min(100, self.battle_fury + 20)
                self.corruption = min(100, self.corruption + 20)
                self.slaanesh_marks += 1
                # Grant free stimms (handled in UI)

            elif god == "nurgle":
                self.corruption = min(100, self.corruption + 25)
                self.nurgle_marks += 1
                # Flag: don't need to clean for 48h (handled in main loop)

            elif god == "tzeentch":
                self.corruption = min(100, self.corruption + 30)
                self.tzeentch_marks += 1
                self.warp_medicine_unlocked = True

            if config.DEBUG:
                print(f">>> Accepted {god}. Corruption: {self.corruption}")

    def should_evolve(self):
        """Check if marine should evolve to next stage"""
        if not self.is_alive:
            return False

        current_time = time.time()
        age = current_time - self.birth_timestamp

        if self.current_stage == self.STAGE_NEOPHYTE:
            return age >= config.STAGE_DURATION_NEOPHYTE

        elif self.current_stage == self.STAGE_SCOUT:
            return age >= (config.STAGE_DURATION_NEOPHYTE + config.STAGE_DURATION_SCOUT)

        elif self.current_stage == self.STAGE_BATTLE_BROTHER:
            total_duration = (config.STAGE_DURATION_NEOPHYTE +
                            config.STAGE_DURATION_SCOUT +
                            config.STAGE_DURATION_BATTLE_BROTHER)
            return age >= total_duration

        return False

    def evolve(self):
        """Evolve to next stage"""
        if not self.is_alive:
            return

        if self.current_stage == self.STAGE_NEOPHYTE:
            self.current_stage = self.STAGE_SCOUT
            if config.DEBUG:
                print(">>> EVOLUTION: Neophyte → Scout")

        elif self.current_stage == self.STAGE_SCOUT:
            self.current_stage = self.STAGE_BATTLE_BROTHER
            if config.DEBUG:
                print(">>> EVOLUTION: Scout → Battle Brother")

        elif self.current_stage == self.STAGE_BATTLE_BROTHER:
            self.current_stage = self.STAGE_VETERAN
            self.final_chapter = self._determine_chapter()
            if config.DEBUG:
                print(f">>> EVOLUTION: Battle Brother → {self.final_chapter}")

    def _determine_chapter(self):
        """
        Determine final chapter based on stats and behavior
        This is the core evolution algorithm
        """

        # CHAOS PATHS (corruption >= 60)
        if self.corruption >= config.CORRUPTION_THRESHOLD_CHAOS:
            # Khorne
            if (self.combat_experience > config.KHORNE_COMBAT_EXP_MIN and
                self.discipline < config.KHORNE_DISCIPLINE_MAX):
                return self.CHAOS_KHORNE

            # Slaanesh
            elif self.stimm_count > config.SLAANESH_STIMM_COUNT_MIN:
                return self.CHAOS_SLAANESH

            # Nurgle
            elif self.poop_accumulation > config.NURGLE_POOP_COUNT_MIN:
                return self.CHAOS_NURGLE

            # Tzeentch
            elif (self.warp_medicine_unlocked and
                  self.chaos_whispers_accepted > config.TZEENTCH_WHISPERS_ACCEPTED_MIN):
                return self.CHAOS_TZEENTCH

            # Default Chaos (if conditions don't match specific god)
            return self.CHAOS_KHORNE  # Fallback

        # LOYALIST PATHS
        else:
            # Grey Knight (secret - perfection required)
            if (self.discipline >= config.GREY_KNIGHT_DISCIPLINE_MIN and
                self.corruption <= config.GREY_KNIGHT_CORRUPTION_MAX and
                self.care_mistakes <= config.GREY_KNIGHT_CARE_MISTAKES_MAX and
                self.chaos_whispers_resisted >= config.GREY_KNIGHT_WHISPERS_RESISTED_MIN):
                return self.CHAPTER_GREY_KNIGHT

            # Ultramarine (balanced excellence)
            elif (self.discipline >= config.ULTRAMARINE_DISCIPLINE_MIN and
                  self.care_mistakes <= config.ULTRAMARINE_CARE_MISTAKES_MAX and
                  self.corruption < config.ULTRAMARINE_CORRUPTION_MAX):
                return self.CHAPTER_ULTRAMARINE

            # Imperial Fist (high discipline, low combat)
            elif (self.discipline >= config.IMPERIAL_FIST_DISCIPLINE_MIN and
                  self.combat_experience < config.IMPERIAL_FIST_COMBAT_EXP_MAX and
                  self.corruption < config.IMPERIAL_FIST_CORRUPTION_MAX):
                return self.CHAPTER_IMPERIAL_FIST

            # Blood Angel (high combat, medium discipline)
            elif (self.combat_experience > config.BLOOD_ANGEL_COMBAT_EXP_MIN and
                  config.BLOOD_ANGEL_DISCIPLINE_MIN <= self.discipline <= config.BLOOD_ANGEL_DISCIPLINE_MAX and
                  self.corruption < config.BLOOD_ANGEL_CORRUPTION_MAX):
                return self.CHAPTER_BLOOD_ANGEL

            # Space Wolf (low discipline, high sustenance)
            elif (self.discipline <= config.SPACE_WOLF_DISCIPLINE_MAX and
                  self.sustenance > config.SPACE_WOLF_SUSTENANCE_MIN and
                  self.corruption < config.SPACE_WOLF_CORRUPTION_MAX):
                return self.CHAPTER_SPACE_WOLF

            # Salamander (high geneseed, low care mistakes)
            elif (self.geneseed_purity > config.SALAMANDER_GENESEED_MIN and
                  config.SALAMANDER_DISCIPLINE_MIN <= self.discipline <= config.SALAMANDER_DISCIPLINE_MAX and
                  self.care_mistakes < config.SALAMANDER_CARE_MISTAKES_MAX):
                return self.CHAPTER_SALAMANDER

        # Default fallback (if nothing matches)
        return self.CHAPTER_ULTRAMARINE

    def die(self, cause):
        """Handle marine death"""
        self.is_alive = False
        self.death_cause = cause

        if config.DEBUG:
            print(f">>> MARINE DECEASED: {cause}")

    def to_dict(self):
        """Serialize to dictionary for saving"""
        return {
            # Stats
            "geneseed_purity": self.geneseed_purity,
            "battle_fury": self.battle_fury,
            "sustenance": self.sustenance,
            "discipline": self.discipline,
            "corruption": self.corruption,

            # Tracking
            "combat_experience": self.combat_experience,
            "care_mistakes": self.care_mistakes,
            "discipline_failures": self.discipline_failures,
            "chaos_whispers_resisted": self.chaos_whispers_resisted,
            "chaos_whispers_accepted": self.chaos_whispers_accepted,
            "battles_won": self.battles_won,
            "battles_lost": self.battles_lost,

            # Chaos marks
            "khorne_marks": self.khorne_marks,
            "slaanesh_marks": self.slaanesh_marks,
            "nurgle_marks": self.nurgle_marks,
            "tzeentch_marks": self.tzeentch_marks,

            # Counters
            "stimm_count": self.stimm_count,
            "poop_accumulation": self.poop_accumulation,

            # Metadata
            "name": self.name,
            "age_cycles": self.age_cycles,
            "birth_timestamp": self.birth_timestamp,
            "last_update": self.last_update,
            "current_stage": self.current_stage,
            "final_chapter": self.final_chapter,
            "is_alive": self.is_alive,
            "death_cause": self.death_cause,

            # Flags
            "warp_medicine_unlocked": self.warp_medicine_unlocked,
            "in_black_rage": self.in_black_rage,
            "is_dreadnought": self.is_dreadnought,
            "last_prayer_time": self.last_prayer_time,
        }

    @classmethod
    def from_dict(cls, data):
        """Deserialize from dictionary"""
        marine = cls(name=data.get("name", "Battle Brother"))

        # Restore all stats
        marine.geneseed_purity = data.get("geneseed_purity", 100)
        marine.battle_fury = data.get("battle_fury", 50)
        marine.sustenance = data.get("sustenance", 50)
        marine.discipline = data.get("discipline", 50)
        marine.corruption = data.get("corruption", 0)

        marine.combat_experience = data.get("combat_experience", 0)
        marine.care_mistakes = data.get("care_mistakes", 0)
        marine.discipline_failures = data.get("discipline_failures", 0)
        marine.chaos_whispers_resisted = data.get("chaos_whispers_resisted", 0)
        marine.chaos_whispers_accepted = data.get("chaos_whispers_accepted", 0)
        marine.battles_won = data.get("battles_won", 0)
        marine.battles_lost = data.get("battles_lost", 0)

        marine.khorne_marks = data.get("khorne_marks", 0)
        marine.slaanesh_marks = data.get("slaanesh_marks", 0)
        marine.nurgle_marks = data.get("nurgle_marks", 0)
        marine.tzeentch_marks = data.get("tzeentch_marks", 0)

        marine.stimm_count = data.get("stimm_count", 0)
        marine.poop_accumulation = data.get("poop_accumulation", 0)

        marine.age_cycles = data.get("age_cycles", 0)
        marine.birth_timestamp = data.get("birth_timestamp", time.time())
        marine.last_update = data.get("last_update", time.time())
        marine.current_stage = data.get("current_stage", cls.STAGE_NEOPHYTE)
        marine.final_chapter = data.get("final_chapter", None)
        marine.is_alive = data.get("is_alive", True)
        marine.death_cause = data.get("death_cause", None)

        marine.warp_medicine_unlocked = data.get("warp_medicine_unlocked", False)
        marine.in_black_rage = data.get("in_black_rage", False)
        marine.is_dreadnought = data.get("is_dreadnought", False)
        marine.last_prayer_time = data.get("last_prayer_time", 0)

        return marine
