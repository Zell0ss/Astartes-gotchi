# lib/ui.py - Astartes-Gotchi User Interface
# Handles display rendering, touch input, and visual feedback

import config

class AstartesUI:
    """
    User Interface system for M5Stack Core2
    Handles rendering, touch input, and visual feedback
    """

    def __init__(self):
        """Initialize UI system - hardware abstraction"""
        # TODO: When testing on actual hardware, import M5Stack modules
        # For now, this is a stub for development

        if config.DEBUG:
            print(">>> AstartesUI initialized (STUB MODE)")
            print(">>> Replace with M5Stack imports when on device")

        # Placeholder for hardware modules
        self.lcd = None
        self.touch = None
        self.speaker = None

        # Try to initialize hardware (will fail on PC)
        try:
            from m5stack import LCD, Touch, Speaker
            self.lcd = LCD()
            self.touch = Touch()
            self.speaker = Speaker()
            self.hardware_available = True
            if config.DEBUG:
                print(">>> M5Stack hardware detected!")
        except ImportError:
            self.hardware_available = False
            if config.DEBUG:
                print(">>> Running in simulation mode (no hardware)")

        # Button regions (x, y, w, h)
        self.btn_feed = (10, 200, 65, 30)
        self.btn_combat = (85, 200, 75, 30)
        self.btn_pray = (170, 200, 65, 30)
        self.btn_clean = (245, 200, 65, 30)
        self.btn_status = (10, 235, 100, 30)
        self.btn_codex = (120, 235, 100, 30)

        self.last_touch = None

    def show_boot_screen(self):
        """Display boot screen"""
        if not self.hardware_available:
            print(">>> [BOOT SCREEN]")
            print(">>> ASTARTES-GOTCHI")
            print(">>> For the Emperor!")
            return

        self.lcd.clear(config.COLOR_BG)
        self.lcd.print("ASTARTES-GOTCHI", 80, 100, config.COLOR_IMPERIAL_GOLD)
        self.lcd.print("For the Emperor!", 70, 130, config.COLOR_AQUILA_WHITE)

    def render(self, marine):
        """
        Main render loop - update entire screen

        Args:
            marine: SpaceMarine instance
        """
        if not self.hardware_available:
            # Console output for simulation
            if config.DEBUG:
                print(f"\n[RENDER] {marine.name} - Stage {marine.current_stage}")
                print(f"  Geneseed: {marine.geneseed_purity}%")
                print(f"  Fury: {marine.battle_fury}%")
                print(f"  Sustenance: {marine.sustenance}%")
                print(f"  Discipline: {marine.discipline}%")
                print(f"  Corruption: {marine.corruption}%")
            return

        # Render on actual hardware
        self.draw_background()
        self.draw_header(marine)
        self.draw_marine_sprite(marine)
        self.draw_stats(marine)
        self.draw_buttons()

    def draw_background(self):
        """Draw background"""
        if self.hardware_available:
            self.lcd.clear(config.COLOR_BG)

    def draw_header(self, marine):
        """Draw header with name and chapter"""
        if not self.hardware_available:
            return

        text = f"{marine.name} - Stage {marine.current_stage}"
        self.lcd.print(text, 10, 5, config.COLOR_TEXT)

    def draw_marine_sprite(self, marine):
        """Draw marine sprite (placeholder for now)"""
        if not self.hardware_available:
            return

        # TODO: Load and display actual sprite based on stage/chapter
        # For now: colored rectangle placeholder
        x = (config.SCREEN_WIDTH - config.SPRITE_SIZE) // 2
        y = 40

        # Color based on chapter/corruption
        if marine.final_chapter:
            if marine.final_chapter == marine.CHAPTER_ULTRAMARINE:
                color = 0x001F  # Blue
            elif marine.final_chapter == marine.CHAOS_KHORNE:
                color = config.COLOR_KHORNE
            else:
                color = 0x7BEF  # Grey
        else:
            color = 0x7BEF  # Grey (no chapter yet)

        self.lcd.rect(x, y, config.SPRITE_SIZE, config.SPRITE_SIZE, color, color)

    def draw_stats(self, marine):
        """Draw stat bars"""
        if not self.hardware_available:
            return

        y_start = 120
        bar_width = 200
        bar_height = 8

        stats = [
            ("Geneseed", marine.geneseed_purity, config.COLOR_GENESEED),
            ("Fury", marine.battle_fury, config.COLOR_BATTLE_FURY),
            ("Sustenance", marine.sustenance, config.COLOR_SUSTENANCE),
            ("Discipline", marine.discipline, config.COLOR_DISCIPLINE),
            ("Corruption", marine.corruption, config.COLOR_CORRUPTION),
        ]

        for i, (name, value, color) in enumerate(stats):
            y = y_start + (i * 10)

            # Label
            self.lcd.print(f"{name}:", 10, y, config.COLOR_TEXT)

            # Bar background
            self.lcd.rect(110, y, bar_width, bar_height, config.COLOR_BUTTON, config.COLOR_BUTTON)

            # Filled portion
            filled_width = int(bar_width * value / 100)
            if filled_width > 0:
                self.lcd.rect(110, y, filled_width, bar_height, color, color)

    def draw_buttons(self):
        """Draw touch buttons"""
        if not self.hardware_available:
            return

        buttons = [
            (self.btn_feed, "FEED", config.COLOR_BUTTON),
            (self.btn_combat, "COMBAT", config.COLOR_BUTTON),
            (self.btn_pray, "PRAY", config.COLOR_BUTTON),
            (self.btn_clean, "CLEAN", config.COLOR_BUTTON),
            (self.btn_status, "STATUS", config.COLOR_BUTTON),
            (self.btn_codex, "CODEX", config.COLOR_BUTTON),
        ]

        for (x, y, w, h), label, color in buttons:
            self.lcd.rect(x, y, w, h, color, color)
            self.lcd.print(label, x + 5, y + 8, config.COLOR_TEXT)

    def get_input(self):
        """
        Get touch input and return action

        Returns:
            str: Action name ("feed", "combat", etc.) or None
        """
        if not self.hardware_available:
            return None

        # Check for touch
        if self.touch.get_count() > 0:
            detail = self.touch.get_detail(0)
            x, y = detail[1], detail[2]

            # Check which button was pressed
            if self._point_in_rect(x, y, self.btn_feed):
                return "feed"
            elif self._point_in_rect(x, y, self.btn_combat):
                return "combat"
            elif self._point_in_rect(x, y, self.btn_pray):
                return "pray"
            elif self._point_in_rect(x, y, self.btn_clean):
                return "clean"
            elif self._point_in_rect(x, y, self.btn_status):
                return "status"
            elif self._point_in_rect(x, y, self.btn_codex):
                return "codex"

        return None

    def _point_in_rect(self, px, py, rect):
        """Check if point is inside rectangle"""
        x, y, w, h = rect
        return x <= px <= x + w and y <= py <= y + h

    def show_feed_menu(self, marine):
        """Show feeding menu (placeholder)"""
        if config.DEBUG:
            print(">>> [UI] Feed menu opened")
        # TODO: Implement feed menu UI
        marine.feed("ration")  # Default for now

    def show_combat_menu(self, marine):
        """Show combat training menu (placeholder)"""
        if config.DEBUG:
            print(">>> [UI] Combat menu opened")
        # TODO: Implement minigame selection UI

    def show_status_screen(self, marine):
        """Show detailed status screen (placeholder)"""
        if config.DEBUG:
            print(">>> [UI] Status screen")
            print(f"    Combat Experience: {marine.combat_experience}")
            print(f"    Battles: {marine.battles_won}W - {marine.battles_lost}L")
            print(f"    Care Mistakes: {marine.care_mistakes}")
            print(f"    Whispers Resisted: {marine.chaos_whispers_resisted}")

    def show_evolution_cutscene(self, marine):
        """Show evolution cutscene (placeholder)"""
        if config.DEBUG:
            print(f">>> [EVOLUTION CUTSCENE] Stage {marine.current_stage}")
        # TODO: Implement evolution animation

    def show_death_sequence(self, marine):
        """Show death sequence (placeholder)"""
        if config.DEBUG:
            print(f">>> [DEATH SEQUENCE] {marine.death_cause}")
        # TODO: Implement death screen

    def show_error_screen(self, error_msg):
        """Show error screen"""
        if config.DEBUG:
            print(f">>> [ERROR] {error_msg}")

        if self.hardware_available:
            self.lcd.clear(config.COLOR_BG)
            self.lcd.print("ERROR", 120, 100, config.COLOR_CORRUPTION)
            self.lcd.print(error_msg[:30], 50, 130, config.COLOR_TEXT)
