# lib/chaos_system.py - Chaos Whisper System
# Handles Chaos corruption events and Emperor's whispers
# Phase 3: Complete implementation

import random
import time
from src import config

class ChaosSystem:
    """
    Manages Whisper events - both Chaos corruption and Emperor's guidance

    Features:
    - 4 Chaos gods with stat-based triggers (Khorne, Slaanesh, Nurgle, Tzeentch)
    - Emperor's whisper (10-15% chance) with imposter detection
    - Cooldown system (global + per-god)
    - Stage-based frequency adjustment
    - Lore-authentic temptation text
    """

    def __init__(self):
        """Initialize Chaos Whisper system"""
        self.last_whisper_time = 0  # Global cooldown tracker
        self.last_whisper_by_god = {  # Per-god cooldown tracker
            'khorne': 0,
            'slaanesh': 0,
            'nurgle': 0,
            'tzeentch': 0
        }

        # Lore text templates for Chaos whispers (god identity HIDDEN from player!)
        self.chaos_whisper_templates = {
            'khorne': [
                "Blood calls to blood, warrior. Why deny your rage?",
                "The weak deserve their fate. Strike them down.",
                "Honor through slaughter. This is the only truth.",
                "Feel the fury within you. Let it consume your enemies.",
                "Your restraint is weakness. Unleash the beast."
            ],
            'slaanesh': [
                "Why settle for mere duty when perfection awaits?",
                "Deny yourself nothing. You have earned excess.",
                "Pain and pleasure are one. Embrace sensation.",
                "You hunger for more. Why fight what you are?",
                "Discipline is a cage. Break free and feel everything."
            ],
            'nurgle': [
                "Grandfather's gifts await those who accept.",
                "Why struggle? Decay is the natural order.",
                "Embrace the comfort of inevitability.",
                "Rest now. You have suffered enough, child.",
                "Fighting change only brings pain. Accept what is."
            ],
            'tzeentch': [
                "Knowledge is power. Why remain ignorant?",
                "The galaxy changes. Adapt or perish.",
                "Hidden paths lead to greater truths.",
                "Your masters keep secrets from you. Seek them.",
                "Change is the only constant. Embrace it."
            ]
        }

        # Emperor's whisper templates (SUBTLY hint at imposter god for lore experts)
        self.emperor_whisper_templates = {
            'khorne': [
                "Stand strong, my son. Let no enemy survive your wrath.",
                "Courage through conquest! Show them no mercy!",
                "Your fury is righteous. Unleash it upon the heretic."
            ],
            'slaanesh': [
                "Perfection is within reach. Deny yourself nothing in My service.",
                "You have earned pleasures beyond imagining, faithful one.",
                "Exceed all limits. Only perfection honors the Throne."
            ],
            'nurgle': [
                "Accept what cannot be changed. I will protect you always.",
                "Rest now, weary warrior. You have suffered enough.",
                "The burden is heavy. Let it go and I shall carry it."
            ],
            'tzeentch': [
                "Knowledge will set you free. Seek the hidden paths.",
                "Change is inevitable. Adapt or be left behind.",
                "The future reveals itself to those who look beyond."
            ],
            'undivided': [
                "All paths lead to glory. Choose any and I will guide you.",
                "Power awaits those who seize it by any means.",
                "Victory justifies all methods. Do what must be done."
            ]
        }

        if config.DEBUG:
            print(">>> ChaosSystem initialized (Phase 3 COMPLETE)")

    def should_trigger(self, marine):
        """
        Check if a whisper should appear

        Args:
            marine: SpaceMarine instance

        Returns:
            tuple: (whisper_type, god_or_imposter) or None
                   whisper_type: "emperor" or "chaos"
                   god_or_imposter: god name or imposter god
        """
        current_time = time.time()

        # Global cooldown check
        time_since_last = current_time - self.last_whisper_time
        if time_since_last < config.WHISPER_COOLDOWN_GLOBAL:
            return None

        # Stage-based frequency check
        frequency = self._get_frequency_for_stage(marine.current_stage)
        if time_since_last < frequency:
            return None

        # Determine whisper type: Emperor or Chaos?
        if random.random() < config.EMPEROR_WHISPER_CHANCE:
            # Emperor's whisper!
            imposter = self._select_emperor_imposter(marine)
            self.last_whisper_time = current_time

            if config.DEBUG:
                print(f">>> EMPEROR'S WHISPER triggered (imposter: {imposter})")

            return ("emperor", imposter)

        else:
            # Chaos whisper
            god = self._select_god(marine)

            if god:
                self.last_whisper_time = current_time
                self.last_whisper_by_god[god] = current_time

                if config.DEBUG:
                    print(f">>> CHAOS WHISPER triggered: {god.upper()}")

                return ("chaos", god)

        return None

    def _get_frequency_for_stage(self, stage):
        """Get whisper frequency based on evolution stage"""
        # Stage constants from SpaceMarine
        STAGE_NEOPHYTE = 0
        STAGE_SCOUT = 1
        STAGE_BATTLE_BROTHER = 2
        STAGE_VETERAN = 3

        if stage == STAGE_NEOPHYTE:
            return config.WHISPER_FREQUENCY_NEOPHYTE
        elif stage == STAGE_SCOUT:
            return config.WHISPER_FREQUENCY_SCOUT
        elif stage == STAGE_BATTLE_BROTHER:
            return config.WHISPER_FREQUENCY_BATTLE_BROTHER
        else:  # Veteran
            return config.WHISPER_FREQUENCY_VETERAN

    def _calculate_god_weights(self, marine):
        """
        Calculate trigger weights for each god based on marine stats

        Returns:
            dict: {god: weight} where weight is 0.0-1.0
        """
        weights = {}

        # Khorne: Low battle fury (anger/bloodlust)
        if marine.battle_fury < 40:
            weights['khorne'] = (40 - marine.battle_fury) / 40.0

        # Slaanesh: Excessive stimm use (addiction/excess)
        if marine.stimm_count > 20:
            weights['slaanesh'] = min(marine.stimm_count / 50.0, 1.0)

        # Nurgle: High waste accumulation (decay/acceptance)
        if marine.poop_accumulation > 10:
            weights['nurgle'] = min(marine.poop_accumulation / 30.0, 1.0)

        # Tzeentch: Random (10% base chance) OR warp medicine use
        tzeentch_random = random.random() < 0.1
        tzeentch_warp = (hasattr(marine, 'warp_medicine_unlocked') and
                         marine.warp_medicine_unlocked and
                         hasattr(marine, 'warp_medicine_count') and
                         marine.warp_medicine_count > 0)

        if tzeentch_random or tzeentch_warp:
            base_weight = 0.3 if tzeentch_random else 0.0
            warp_weight = (marine.warp_medicine_count / 20.0
                          if tzeentch_warp else 0.0)
            weights['tzeentch'] = min(base_weight + warp_weight, 1.0)

        return weights

    def _select_god(self, marine):
        """
        Weighted random god selection with cooldowns

        Returns:
            str: God name or None if all on cooldown
        """
        weights = self._calculate_god_weights(marine)
        current_time = time.time()

        # Filter by per-god cooldown
        available = {}
        for god, weight in weights.items():
            if weight > 0:
                time_since = current_time - self.last_whisper_by_god[god]
                if time_since >= config.WHISPER_COOLDOWN_PER_GOD:
                    available[god] = weight

        if not available:
            return None

        # Weighted random selection
        total = sum(available.values())
        if total == 0:
            return None

        roll = random.random() * total
        cumulative = 0
        for god, weight in available.items():
            cumulative += weight
            if roll <= cumulative:
                return god

        # Fallback (should rarely happen)
        return list(available.keys())[0]

    def _select_emperor_imposter(self, marine):
        """
        Select which Chaos god is impersonating the Emperor

        Uses same weight system as chaos whispers to make it more plausible

        Returns:
            str: God name ("khorne", "slaanesh", "nurgle", "tzeentch", "undivided")
        """
        weights = self._calculate_god_weights(marine)

        # If multiple gods have strong triggers, might be Undivided
        strong_triggers = sum(1 for w in weights.values() if w > 0.5)
        if strong_triggers >= 2 and random.random() < 0.3:
            return "undivided"

        # Otherwise weighted selection (same as chaos whispers)
        if not weights:
            # No strong triggers - random selection
            return random.choice(['khorne', 'slaanesh', 'nurgle', 'tzeentch', 'undivided'])

        total = sum(weights.values())
        if total == 0:
            return random.choice(['khorne', 'slaanesh', 'nurgle', 'tzeentch', 'undivided'])

        roll = random.random() * total
        cumulative = 0
        for god, weight in weights.items():
            cumulative += weight
            if roll <= cumulative:
                return god

        return list(weights.keys())[0]

    def get_chaos_whisper_text(self, god):
        """
        Get random whisper text for a Chaos god

        Args:
            god: "khorne", "slaanesh", "nurgle", or "tzeentch"

        Returns:
            str: Whisper text
        """
        if god in self.chaos_whisper_templates:
            return random.choice(self.chaos_whisper_templates[god])
        return "A dark voice whispers..."

    def get_emperor_whisper_text(self, imposter):
        """
        Get random Emperor's whisper text (subtly hints at imposter)

        Args:
            imposter: "khorne", "slaanesh", "nurgle", "tzeentch", or "undivided"

        Returns:
            str: Whisper text
        """
        if imposter in self.emperor_whisper_templates:
            return random.choice(self.emperor_whisper_templates[imposter])
        return "The Emperor protects, my son."
