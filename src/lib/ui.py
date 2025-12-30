# lib/ui.py - Astartes-Gotchi User Interface
# Handles display rendering, touch input, and visual feedback

import config

class AstartesUI:
    """
    User Interface system for M5Stack Core2
    Handles rendering, touch input, and visual feedback
    """

    def __init__(self):
        """Initialize UI system - UIFlow firmware"""
        if config.DEBUG:
            print(">>> AstartesUI initializing...")

        # Try to initialize UIFlow M5Stack hardware
        try:
            import M5
            M5.begin()
            self.M5 = M5
            self.hardware_available = True
            if config.DEBUG:
                print(">>> UIFlow M5Stack hardware initialized!")
        except ImportError:
            self.M5 = None
            self.hardware_available = False
            if config.DEBUG:
                print(">>> Running in simulation mode (no hardware)")

        # Button regions (x, y, w, h) - Optimized for 320x240 screen
        # First row (3 buttons)
        self.btn_feed = (5, 195, 100, 20)
        self.btn_combat = (110, 195, 100, 20)
        self.btn_pray = (215, 195, 100, 20)

        # Second row (3 buttons)
        self.btn_clean = (5, 218, 100, 20)
        self.btn_status = (110, 218, 100, 20)
        self.btn_power = (215, 218, 100, 20)  # Power off button

        # Touch debounce
        self.last_touch_time = 0
        self.touch_cooldown = 500  # milliseconds between touches

        # Dirty rectangles optimization - track previous state
        self.needs_full_redraw = True  # First render must draw everything
        self.prev_stats = {
            'geneseed_purity': None,
            'battle_fury': None,
            'sustenance': None,
            'discipline': None,
            'corruption': None
        }

    def show_boot_screen(self):
        """Display boot screen"""
        if not self.hardware_available:
            print(">>> [BOOT SCREEN]")
            print(">>> ASTARTES-GOTCHI")
            print(">>> For the Emperor!")
            return

        self.M5.Lcd.fillScreen(config.COLOR_BG)
        self.M5.Lcd.setCursor(80, 100)
        self.M5.Lcd.setTextColor(config.COLOR_IMPERIAL_GOLD)
        self.M5.Lcd.setTextSize(2)
        self.M5.Lcd.print("ASTARTES-GOTCHI")

        self.M5.Lcd.setCursor(70, 130)
        self.M5.Lcd.setTextColor(config.COLOR_AQUILA_WHITE)
        self.M5.Lcd.print("For the Emperor!")

    def render(self, marine):
        """
        Main render loop - uses dirty rectangles to minimize flickering

        Only redraws changed elements. Full redraw happens:
        - On first render (needs_full_redraw = True)
        - When stats change

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

        # Check if stats changed
        stats_changed = (
            self.prev_stats['geneseed_purity'] != marine.geneseed_purity or
            self.prev_stats['battle_fury'] != marine.battle_fury or
            self.prev_stats['sustenance'] != marine.sustenance or
            self.prev_stats['discipline'] != marine.discipline or
            self.prev_stats['corruption'] != marine.corruption
        )

        # Full redraw on first render or when needed
        if self.needs_full_redraw:
            self.draw_background()
            self.draw_header(marine)
            self.draw_marine_sprite(marine)
            self.draw_stats(marine)
            self.draw_buttons()
            self.needs_full_redraw = False
            if config.DEBUG:
                print(">>> [RENDER] Full screen redraw")

        # Incremental update: only redraw stats if they changed
        elif stats_changed:
            self.draw_stats(marine)
            if config.DEBUG:
                print(">>> [RENDER] Stats updated")

        # Update previous stats for next frame
        self.prev_stats['geneseed_purity'] = marine.geneseed_purity
        self.prev_stats['battle_fury'] = marine.battle_fury
        self.prev_stats['sustenance'] = marine.sustenance
        self.prev_stats['discipline'] = marine.discipline
        self.prev_stats['corruption'] = marine.corruption

    def draw_background(self):
        """Draw background"""
        if self.hardware_available:
            self.M5.Lcd.fillScreen(config.COLOR_BG)

    def draw_header(self, marine):
        """Draw header with name and chapter"""
        if not self.hardware_available:
            return

        text = f"{marine.name} - Stage {marine.current_stage}"
        self.M5.Lcd.setCursor(10, 5)
        self.M5.Lcd.setTextColor(config.COLOR_TEXT)
        self.M5.Lcd.setTextSize(1)
        self.M5.Lcd.print(text)

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
                color = config.COLOR_GENESEED  # Blue
            elif marine.final_chapter == marine.CHAOS_KHORNE:
                color = config.COLOR_KHORNE
            else:
                color = config.COLOR_BUTTON_ACTIVE  # Grey
        else:
            color = config.COLOR_BUTTON_ACTIVE  # Grey (no chapter yet)

        self.M5.Lcd.fillRect(x, y, config.SPRITE_SIZE, config.SPRITE_SIZE, color)

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
            self.M5.Lcd.setCursor(10, y)
            self.M5.Lcd.setTextColor(config.COLOR_TEXT)
            self.M5.Lcd.setTextSize(1)
            self.M5.Lcd.print(f"{name}:")

            # Bar background
            self.M5.Lcd.fillRect(110, y, bar_width, bar_height, config.COLOR_BUTTON)

            # Filled portion
            filled_width = int(bar_width * value / 100)
            if filled_width > 0:
                self.M5.Lcd.fillRect(110, y, filled_width, bar_height, color)

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
            (self.btn_power, "POWER", config.COLOR_CORRUPTION),  # Red button for power
        ]

        for (x, y, w, h), label, color in buttons:
            self.M5.Lcd.fillRect(x, y, w, h, color)
            self.M5.Lcd.setCursor(x + 5, y + 8)
            self.M5.Lcd.setTextColor(config.COLOR_TEXT)
            self.M5.Lcd.setTextSize(1)
            self.M5.Lcd.print(label)

    def _flash_button(self, button_rect, label, normal_color):
        """
        Flash button to provide visual and haptic feedback on press

        Args:
            button_rect: (x, y, w, h) tuple
            label: Button text
            normal_color: Normal button color
        """
        if not self.hardware_available:
            return

        x, y, w, h = button_rect

        # Haptic feedback - vibration pulse
        try:
            self.M5.Power.setVibration(255)  # Max intensity
        except:
            pass  # Vibration not critical, continue if fails

        # Flash to active color
        self.M5.Lcd.fillRect(x, y, w, h, config.COLOR_BUTTON_ACTIVE)
        self.M5.Lcd.setCursor(x + 5, y + 8)
        self.M5.Lcd.setTextColor(config.COLOR_BG)  # Black text on light background
        self.M5.Lcd.setTextSize(1)
        self.M5.Lcd.print(label)

        # Short delay for visual + haptic feedback
        import time
        time.sleep_ms(50)

        # Stop vibration
        try:
            self.M5.Power.setVibration(0)
        except:
            pass

        # Keep visual flash a bit longer
        time.sleep_ms(50)

        # Return to normal color
        self.M5.Lcd.fillRect(x, y, w, h, normal_color)
        self.M5.Lcd.setCursor(x + 5, y + 8)
        self.M5.Lcd.setTextColor(config.COLOR_TEXT)
        self.M5.Lcd.setTextSize(1)
        self.M5.Lcd.print(label)

    def get_input(self):
        """
        Get touch input and return action

        Returns:
            str: Action name ("feed", "combat", etc.) or None
        """
        if not self.hardware_available:
            return None

        # Update M5 state (CRITICAL for touch detection)
        self.M5.update()

        # Check for touch (UIFlow API - correct syntax)
        try:
            touch_count = self.M5.Touch.getCount()
            if touch_count > 0:
                # Debounce: Check if enough time has passed since last touch
                import time
                current_time = time.ticks_ms()
                time_since_last = time.ticks_diff(current_time, self.last_touch_time)

                if time_since_last < self.touch_cooldown:
                    # Too soon - ignore this touch
                    return None

                x = self.M5.Touch.getX()
                y = self.M5.Touch.getY()

                if config.DEBUG:
                    print(f">>> Touch detected at ({x}, {y})")

                # Update last touch time
                self.last_touch_time = current_time

                # Check which button was pressed and flash it
                if self._point_in_rect(x, y, self.btn_feed):
                    self._flash_button(self.btn_feed, "FEED", config.COLOR_BUTTON)
                    print(">>> Button: FEED")
                    return "feed"
                elif self._point_in_rect(x, y, self.btn_combat):
                    self._flash_button(self.btn_combat, "COMBAT", config.COLOR_BUTTON)
                    print(">>> Button: COMBAT")
                    return "combat"
                elif self._point_in_rect(x, y, self.btn_pray):
                    self._flash_button(self.btn_pray, "PRAY", config.COLOR_BUTTON)
                    print(">>> Button: PRAY")
                    return "pray"
                elif self._point_in_rect(x, y, self.btn_clean):
                    self._flash_button(self.btn_clean, "CLEAN", config.COLOR_BUTTON)
                    print(">>> Button: CLEAN")
                    return "clean"
                elif self._point_in_rect(x, y, self.btn_status):
                    self._flash_button(self.btn_status, "STATUS", config.COLOR_BUTTON)
                    print(">>> Button: STATUS")
                    return "status"
                elif self._point_in_rect(x, y, self.btn_power):
                    self._flash_button(self.btn_power, "POWER", config.COLOR_CORRUPTION)
                    print(">>> Button: POWER OFF")
                    return "power"
                else:
                    if config.DEBUG:
                        print(f">>> Touch outside buttons")
        except Exception as e:
            if config.DEBUG:
                print(f">>> Touch error: {e}")

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
            self.M5.Lcd.fillScreen(config.COLOR_BG)

            self.M5.Lcd.setCursor(120, 100)
            self.M5.Lcd.setTextColor(config.COLOR_CORRUPTION)
            self.M5.Lcd.setTextSize(2)
            self.M5.Lcd.print("ERROR")

            self.M5.Lcd.setCursor(50, 130)
            self.M5.Lcd.setTextColor(config.COLOR_TEXT)
            self.M5.Lcd.setTextSize(1)
            self.M5.Lcd.print(error_msg[:30])

    def power_off(self):
        """Power off the M5Stack device"""
        if config.DEBUG:
            print(">>> [POWER OFF] Shutting down...")

        if self.hardware_available:
            # Show shutdown screen
            self.M5.Lcd.fillScreen(config.COLOR_BG)
            self.M5.Lcd.setCursor(70, 100)
            self.M5.Lcd.setTextColor(config.COLOR_IMPERIAL_GOLD)
            self.M5.Lcd.setTextSize(2)
            self.M5.Lcd.print("For the Emperor!")

            self.M5.Lcd.setCursor(90, 130)
            self.M5.Lcd.setTextColor(config.COLOR_TEXT)
            self.M5.Lcd.setTextSize(1)
            self.M5.Lcd.print("Powering off...")

            import time
            time.sleep(1)

            # Power off via AXP192/AXP2101
            try:
                self.M5.Power.powerOff()
            except:
                # Fallback: deep sleep (functionally similar to power off)
                import machine
                machine.deepsleep()
