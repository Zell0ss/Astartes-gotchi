# lib/chaos_system.py - Chaos Whisper System
# Handles random Chaos corruption events
# TODO: Implement in Phase 3

import random
import time
import config

class ChaosWhisper:
    """
    Manages Chaos Whisper events
    Random temptations from the Ruinous Powers
    """

    def __init__(self):
        self.last_whisper_time = 0
        if config.DEBUG:
            print(">>> ChaosWhisper system initialized (STUB)")

    def should_trigger(self, marine):
        """
        Check if a whisper should appear

        Args:
            marine: SpaceMarine instance

        Returns:
            str: God name ("khorne", "slaanesh", etc.) or None
        """
        # TODO: Implement whisper frequency logic
        # For now, return None (no whispers in MVP)
        return None

    def present_whisper(self, god, ui):
        """
        Show whisper UI and get player choice

        Args:
            god: Which chaos god ("khorne", "slaanesh", "nurgle", "tzeentch")
            ui: AstartesUI instance

        Returns:
            str: "resist" or "give_in"
        """
        # TODO: Implement whisper UI
        if config.DEBUG:
            print(f">>> [CHAOS WHISPER] {god.upper()} tempts you...")

        # Placeholder: auto-resist for now
        return "resist"
