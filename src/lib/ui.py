# lib/ui.py - Astartes-Gotchi User Interface
# Handles display rendering, touch input, and visual feedback

import time
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

            # CRITICAL: Set LCD brightness (default can be 0!)
            M5.Lcd.setBrightness(80)  # 80% brightness

            if config.DEBUG:
                print(">>> UIFlow M5Stack hardware initialized!")
                print(">>> LCD brightness set to 80%")
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
        """Draw header with name and stage/chapter"""
        if not self.hardware_available:
            return

        from lib.space_marine import SpaceMarine

        # Determine stage name
        stage_names = {
            SpaceMarine.STAGE_NEOPHYTE: "NEOPHYTE",
            SpaceMarine.STAGE_SCOUT: "SCOUT",
            SpaceMarine.STAGE_BATTLE_BROTHER: "BATTLE BROTHER",
            SpaceMarine.STAGE_VETERAN: "VETERAN"
        }

        stage_name = stage_names.get(marine.current_stage, "UNKNOWN")

        # If Veteran, show chapter instead of stage
        if marine.current_stage == SpaceMarine.STAGE_VETERAN and marine.final_chapter:
            chapter_short_names = {
                SpaceMarine.CHAPTER_ULTRAMARINE: "ULTRAMARINE",
                SpaceMarine.CHAPTER_GREY_KNIGHT: "GREY KNIGHT",
                SpaceMarine.CHAPTER_IMPERIAL_FIST: "IMP. FIST",
                SpaceMarine.CHAPTER_BLOOD_ANGEL: "BLOOD ANGEL",
                SpaceMarine.CHAPTER_SPACE_WOLF: "SPACE WOLF",
                SpaceMarine.CHAPTER_SALAMANDER: "SALAMANDER",
                SpaceMarine.CHAOS_KHORNE: "KHORNE",
                SpaceMarine.CHAOS_SLAANESH: "SLAANESH",
                SpaceMarine.CHAOS_NURGLE: "NURGLE",
                SpaceMarine.CHAOS_TZEENTCH: "TZEENTCH",
            }
            display_text = chapter_short_names.get(marine.final_chapter, marine.final_chapter.upper())
        else:
            display_text = stage_name

        # Display with appropriate color
        header_color = config.COLOR_IMPERIAL_GOLD
        if marine.final_chapter:
            if marine.final_chapter == SpaceMarine.CHAOS_KHORNE:
                header_color = config.COLOR_KHORNE
            elif marine.final_chapter == SpaceMarine.CHAOS_SLAANESH:
                header_color = config.COLOR_SLAANESH
            elif marine.final_chapter == SpaceMarine.CHAOS_NURGLE:
                header_color = config.COLOR_NURGLE
            elif marine.final_chapter == SpaceMarine.CHAOS_TZEENTCH:
                header_color = config.COLOR_TZEENTCH

        self.M5.Lcd.setCursor(10, 5)
        self.M5.Lcd.setTextColor(header_color)
        self.M5.Lcd.setTextSize(1)
        self.M5.Lcd.print(display_text)

    def draw_marine_sprite(self, marine):
        """
        Draw marine sprite (placeholder for now)
        Different size and color based on stage
        """
        if not self.hardware_available:
            return

        from lib.space_marine import SpaceMarine

        # Determine size based on stage (marines grow stronger)
        if marine.current_stage == SpaceMarine.STAGE_NEOPHYTE:
            size = 40
            base_color = config.COLOR_BUTTON_ACTIVE  # Grey (recruit)
        elif marine.current_stage == SpaceMarine.STAGE_SCOUT:
            size = 50
            base_color = config.COLOR_BUTTON_ACTIVE  # Grey (scout armor)
        elif marine.current_stage == SpaceMarine.STAGE_BATTLE_BROTHER:
            size = 64
            base_color = config.COLOR_GENESEED  # Blue (power armor)
        else:  # VETERAN
            size = 70
            # Color based on chapter
            if marine.final_chapter == SpaceMarine.CHAPTER_ULTRAMARINE:
                base_color = config.COLOR_GENESEED  # Blue
            elif marine.final_chapter == SpaceMarine.CHAPTER_GREY_KNIGHT:
                base_color = 0xC0C0C0  # Silver
            elif marine.final_chapter == SpaceMarine.CHAPTER_IMPERIAL_FIST:
                base_color = config.COLOR_IMPERIAL_GOLD  # Gold
            elif marine.final_chapter == SpaceMarine.CHAPTER_BLOOD_ANGEL:
                base_color = config.COLOR_BATTLE_FURY  # Red
            elif marine.final_chapter == SpaceMarine.CHAPTER_SPACE_WOLF:
                base_color = 0x708090  # Slate grey
            elif marine.final_chapter == SpaceMarine.CHAPTER_SALAMANDER:
                base_color = config.COLOR_SUSTENANCE  # Green
            elif marine.final_chapter == SpaceMarine.CHAOS_KHORNE:
                base_color = config.COLOR_KHORNE
            elif marine.final_chapter == SpaceMarine.CHAOS_SLAANESH:
                base_color = config.COLOR_SLAANESH
            elif marine.final_chapter == SpaceMarine.CHAOS_NURGLE:
                base_color = config.COLOR_NURGLE
            elif marine.final_chapter == SpaceMarine.CHAOS_TZEENTCH:
                base_color = config.COLOR_TZEENTCH
            else:
                base_color = config.COLOR_IMPERIAL_GOLD

        # Center sprite
        x = (config.SCREEN_WIDTH - size) // 2
        y = 40 + (config.SPRITE_SIZE - size) // 2  # Vertically centered in sprite area

        # Draw main body
        self.M5.Lcd.fillRect(x, y, size, size, base_color)

        # Add corruption indicator (red border if corrupted)
        if marine.corruption > 40:
            border_thickness = 2
            border_color = config.COLOR_CORRUPTION if marine.corruption >= 60 else config.COLOR_BATTLE_FURY
            # Top
            self.M5.Lcd.fillRect(x, y, size, border_thickness, border_color)
            # Bottom
            self.M5.Lcd.fillRect(x, y + size - border_thickness, size, border_thickness, border_color)
            # Left
            self.M5.Lcd.fillRect(x, y, border_thickness, size, border_color)
            # Right
            self.M5.Lcd.fillRect(x + size - border_thickness, y, border_thickness, size, border_color)

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

    def clear_touches(self):
        """
        Clear/flush any pending touch events
        Call this when transitioning between screens to prevent bleed-through
        """
        if not self.hardware_available:
            return

        # Update M5 state and discard any touches
        self.M5.update()
        # Read and discard all pending touches
        count = self.M5.Touch.getCount()
        for _ in range(count):
            # Just reading them clears the queue
            self.M5.Touch.getX()
            self.M5.Touch.getY()

        # Reset last touch time to prevent immediate re-trigger
        import time
        self.last_touch_time = time.ticks_ms()

        if config.DEBUG:
            print(f">>> Touch buffer cleared ({count} touches discarded)")

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
        """
        Show detailed status screen with reset option
        Interactive screen with buttons
        """
        if config.DEBUG:
            print(">>> [UI] Status screen")
            print(f"    Combat Experience: {marine.combat_experience}")
            print(f"    Battles: {marine.battles_won}W - {marine.battles_lost}L")
            print(f"    Care Mistakes: {marine.care_mistakes}")
            print(f"    Whispers Resisted: {marine.chaos_whispers_resisted}")

        if not self.hardware_available:
            return

        # Clear any pending touches to prevent bleed-through
        self.clear_touches()

        # Clear screen
        self.M5.Lcd.fillScreen(config.COLOR_BG)

        # Title
        self.M5.Lcd.setTextSize(2)
        self.M5.Lcd.setTextColor(config.COLOR_IMPERIAL_GOLD)
        self.M5.Lcd.setCursor(90, 10)
        self.M5.Lcd.print("STATUS")

        # Stats display
        self.M5.Lcd.setTextSize(1)
        self.M5.Lcd.setTextColor(config.COLOR_TEXT)
        y = 40

        stats_to_show = [
            ("Combat Exp", marine.combat_experience),
            ("Battles", f"{marine.battles_won}W - {marine.battles_lost}L"),
            ("Care Mistakes", marine.care_mistakes),
            ("Whispers Resisted", marine.chaos_whispers_resisted),
            ("Whispers Accepted", marine.chaos_whispers_accepted),
            ("Age (cycles)", marine.age_cycles),
        ]

        for label, value in stats_to_show:
            self.M5.Lcd.setCursor(20, y)
            self.M5.Lcd.print(f"{label}: {value}")
            y += 20

        # Buttons at bottom
        # BACK button (left)
        self.M5.Lcd.fillRect(10, 200, 140, 35, config.COLOR_BUTTON)
        self.M5.Lcd.setCursor(50, 212)
        self.M5.Lcd.setTextColor(config.COLOR_TEXT)
        self.M5.Lcd.print("BACK")

        # RESET button (right) - RED for danger
        self.M5.Lcd.fillRect(170, 200, 140, 35, config.COLOR_BATTLE_FURY)
        self.M5.Lcd.setCursor(200, 212)
        self.M5.Lcd.setTextColor(config.COLOR_TEXT)
        self.M5.Lcd.print("RESET")

        # Wait longer to avoid catching the status button press
        time.sleep(0.5)

        # Clear touches again after the delay (extra safety)
        self.clear_touches()

        # Wait for button press
        if config.DEBUG:
            print(">>> [STATUS] Waiting for button input...")

        while True:
            self.M5.update()

            try:
                touch_count = self.M5.Touch.getCount()
                if touch_count > 0:
                    x = self.M5.Touch.getX()
                    y = self.M5.Touch.getY()

                    if config.DEBUG:
                        print(f">>> [STATUS] Touch at ({x}, {y})")

                    # BACK button (10, 200, 140, 35)
                    if 10 <= x <= 150 and 200 <= y <= 235:
                        if config.DEBUG:
                            print(">>> [STATUS] Back button pressed")

                        # Haptic feedback
                        try:
                            self.M5.Power.setVibration(150)
                            time.sleep(0.1)
                            self.M5.Power.setVibration(0)
                        except:
                            pass

                        time.sleep(0.2)  # Additional debounce
                        self.clear_touches()  # Clear before returning to main game
                        self.needs_full_redraw = True
                        return False  # Return to game

                    # RESET button (170, 200, 140, 35)
                    elif 170 <= x <= 310 and 200 <= y <= 235:
                        if config.DEBUG:
                            print(">>> [STATUS] Reset button pressed")

                        # Haptic feedback - stronger for destructive action
                        try:
                            self.M5.Power.setVibration(200)
                            time.sleep(0.15)
                            self.M5.Power.setVibration(0)
                        except:
                            pass

                        time.sleep(0.15)  # Additional debounce
                        # Show confirmation
                        confirmed = self.show_reset_confirmation()
                        if confirmed:
                            self.clear_touches()  # Clear before reset
                            return True  # Signal to reset
                        else:
                            # Redraw status screen
                            self.show_status_screen(marine)
                            return False
            except Exception as e:
                if config.DEBUG:
                    print(f">>> [STATUS] Touch error: {e}")

            time.sleep(0.1)  # Small delay to prevent busy loop

    def show_reset_confirmation(self):
        """
        Show confirmation dialog for reset
        Returns True if confirmed, False if cancelled
        """
        if not self.hardware_available:
            return False

        # Clear any pending touches
        self.clear_touches()

        # Clear screen
        self.M5.Lcd.fillScreen(config.COLOR_BG)

        # Warning message
        self.M5.Lcd.setTextSize(2)
        self.M5.Lcd.setTextColor(config.COLOR_CORRUPTION)
        self.M5.Lcd.setCursor(60, 40)
        self.M5.Lcd.print("WARNING!")

        self.M5.Lcd.setTextSize(1)
        self.M5.Lcd.setTextColor(config.COLOR_TEXT)
        self.M5.Lcd.setCursor(30, 80)
        self.M5.Lcd.print("Delete save and restart")
        self.M5.Lcd.setCursor(30, 100)
        self.M5.Lcd.print("with new Neophyte?")

        self.M5.Lcd.setCursor(30, 130)
        self.M5.Lcd.setTextColor(config.COLOR_BATTLE_FURY)
        self.M5.Lcd.print("This cannot be undone!")

        # Buttons
        # CANCEL button (left)
        self.M5.Lcd.fillRect(10, 180, 140, 45, config.COLOR_BUTTON)
        self.M5.Lcd.setCursor(45, 197)
        self.M5.Lcd.setTextColor(config.COLOR_TEXT)
        self.M5.Lcd.setTextSize(2)
        self.M5.Lcd.print("CANCEL")

        # CONFIRM button (right)
        self.M5.Lcd.fillRect(170, 180, 140, 45, config.COLOR_BATTLE_FURY)
        self.M5.Lcd.setCursor(195, 197)
        self.M5.Lcd.setTextColor(config.COLOR_TEXT)
        self.M5.Lcd.setTextSize(2)
        self.M5.Lcd.print("RESET")

        # Wait longer for screen to settle
        time.sleep(0.5)

        # Clear touches again after delay
        self.clear_touches()

        if config.DEBUG:
            print(">>> [RESET] Waiting for confirmation input...")

        # Wait for button press
        while True:
            self.M5.update()

            try:
                touch_count = self.M5.Touch.getCount()
                if touch_count > 0:
                    x = self.M5.Touch.getX()
                    y = self.M5.Touch.getY()

                    if config.DEBUG:
                        print(f">>> [RESET] Touch at ({x}, {y})")

                    # CANCEL button
                    if 10 <= x <= 150 and 180 <= y <= 225:
                        if config.DEBUG:
                            print(">>> [RESET] Cancelled")

                        # Haptic feedback - single pulse
                        try:
                            self.M5.Power.setVibration(150)
                            time.sleep(0.1)
                            self.M5.Power.setVibration(0)
                        except:
                            pass

                        time.sleep(0.2)  # Additional debounce
                        self.clear_touches()  # Clear before returning
                        return False

                    # CONFIRM button
                    elif 170 <= x <= 310 and 180 <= y <= 225:
                        if config.DEBUG:
                            print(">>> [RESET] Confirmed!")

                        # Haptic feedback - STRONG double pulse for destructive action
                        try:
                            self.M5.Power.setVibration(250)
                            time.sleep(0.1)
                            self.M5.Power.setVibration(0)
                            time.sleep(0.05)
                            self.M5.Power.setVibration(250)
                            time.sleep(0.1)
                            self.M5.Power.setVibration(0)
                        except:
                            pass

                        time.sleep(0.1)  # Additional debounce
                        self.clear_touches()  # Clear before returning
                        return True
            except Exception as e:
                if config.DEBUG:
                    print(f">>> [RESET] Touch error: {e}")

            time.sleep(0.1)

    def show_evolution_cutscene(self, marine):
        """
        Show evolution cutscene with animation
        Called BEFORE marine.evolve() to show the transition
        """
        if not self.hardware_available:
            if config.DEBUG:
                print(f">>> [EVOLUTION CUTSCENE] Stage {marine.current_stage} → {marine.current_stage + 1}")
            return

        from lib.space_marine import SpaceMarine

        # Stage names for display
        stage_names = {
            SpaceMarine.STAGE_NEOPHYTE: "NEOPHYTE",
            SpaceMarine.STAGE_SCOUT: "SCOUT",
            SpaceMarine.STAGE_BATTLE_BROTHER: "BATTLE BROTHER",
            SpaceMarine.STAGE_VETERAN: "VETERAN"
        }

        # Chapter names for Veteran display
        chapter_names = {
            SpaceMarine.CHAPTER_ULTRAMARINE: "ULTRAMARINE",
            SpaceMarine.CHAPTER_GREY_KNIGHT: "GREY KNIGHT",
            SpaceMarine.CHAPTER_IMPERIAL_FIST: "IMPERIAL FIST",
            SpaceMarine.CHAPTER_BLOOD_ANGEL: "BLOOD ANGEL",
            SpaceMarine.CHAPTER_SPACE_WOLF: "SPACE WOLF",
            SpaceMarine.CHAPTER_SALAMANDER: "SALAMANDER",
            SpaceMarine.CHAOS_KHORNE: "KHORNE BERSERKER",
            SpaceMarine.CHAOS_SLAANESH: "NOISE MARINE",
            SpaceMarine.CHAOS_NURGLE: "PLAGUE MARINE",
            SpaceMarine.CHAOS_TZEENTCH: "THOUSAND SONS",
            SpaceMarine.CHAOS_UNDIVIDED: "CHAOS UNDIVIDED"
        }

        old_stage = marine.current_stage
        new_stage = old_stage + 1
        old_stage_name = stage_names.get(old_stage, "UNKNOWN")
        new_stage_name = stage_names.get(new_stage, "UNKNOWN")

        # Temporarily evolve to determine chapter (we'll revert after display)
        # This is needed because _determine_chapter is called during evolve()
        if new_stage == SpaceMarine.STAGE_VETERAN:
            predicted_chapter = marine._determine_chapter()
        else:
            predicted_chapter = None

        if config.DEBUG:
            print(f">>> [EVOLUTION] {old_stage_name} → {new_stage_name}")
            if predicted_chapter:
                print(f"    Chapter: {predicted_chapter}")

        # Haptic feedback - 3 quick pulses
        if self.hardware_available:
            try:
                for i in range(3):
                    self.M5.Power.setVibration(200)
                    time.sleep(0.1)
                    self.M5.Power.setVibration(0)
                    time.sleep(0.1)
            except:
                pass

        # === ANIMATION SEQUENCE ===

        # Phase 1: Screen flash (gold for loyalist, purple for chaos)
        flash_color = config.COLOR_IMPERIAL_GOLD
        if predicted_chapter and "chaos" in predicted_chapter.lower() or any(
            predicted_chapter == c for c in [
                SpaceMarine.CHAOS_KHORNE,
                SpaceMarine.CHAOS_SLAANESH,
                SpaceMarine.CHAOS_NURGLE,
                SpaceMarine.CHAOS_TZEENTCH
            ]
        ):
            flash_color = config.COLOR_CORRUPTION

        for i in range(2):
            self.M5.Lcd.fillScreen(flash_color)
            time.sleep(0.15)
            self.M5.Lcd.fillScreen(config.COLOR_BG)
            time.sleep(0.15)

        # Phase 2: Show old stage
        self.M5.Lcd.fillScreen(config.COLOR_BG)
        self.M5.Lcd.setTextSize(2)
        self.M5.Lcd.setTextColor(config.COLOR_TEXT)
        self.M5.Lcd.setCursor(10, 60)
        self.M5.Lcd.print(old_stage_name)
        time.sleep(1.0)

        # Phase 3: Arrow animation
        self.M5.Lcd.setTextColor(config.COLOR_IMPERIAL_GOLD)
        self.M5.Lcd.setCursor(10, 100)
        self.M5.Lcd.print(">>>")
        time.sleep(0.3)
        self.M5.Lcd.print(">>>")
        time.sleep(0.3)
        self.M5.Lcd.print(">>>")
        time.sleep(0.5)

        # Phase 4: Show new stage
        self.M5.Lcd.setTextColor(flash_color)
        self.M5.Lcd.setTextSize(3)
        self.M5.Lcd.setCursor(10, 140)
        self.M5.Lcd.print(new_stage_name)
        time.sleep(1.5)

        # Phase 5: If Veteran, show final chapter
        if predicted_chapter:
            chapter_display = chapter_names.get(predicted_chapter, predicted_chapter.upper())

            # Determine chapter color
            if predicted_chapter == SpaceMarine.CHAOS_KHORNE:
                chapter_color = config.COLOR_KHORNE
            elif predicted_chapter == SpaceMarine.CHAOS_SLAANESH:
                chapter_color = config.COLOR_SLAANESH
            elif predicted_chapter == SpaceMarine.CHAOS_NURGLE:
                chapter_color = config.COLOR_NURGLE
            elif predicted_chapter == SpaceMarine.CHAOS_TZEENTCH:
                chapter_color = config.COLOR_TZEENTCH
            else:
                chapter_color = config.COLOR_IMPERIAL_GOLD

            self.M5.Lcd.fillScreen(config.COLOR_BG)
            self.M5.Lcd.setTextSize(2)
            self.M5.Lcd.setTextColor(chapter_color)
            self.M5.Lcd.setCursor(10, 80)
            self.M5.Lcd.print("CHAPTER:")
            self.M5.Lcd.setCursor(10, 120)
            self.M5.Lcd.setTextSize(2)
            self.M5.Lcd.print(chapter_display)

            # Show battle cry based on chapter
            self.M5.Lcd.setTextSize(1)
            self.M5.Lcd.setTextColor(config.COLOR_TEXT)
            self.M5.Lcd.setCursor(10, 180)

            if predicted_chapter == SpaceMarine.CHAPTER_ULTRAMARINE:
                self.M5.Lcd.print("Courage and Honour!")
            elif predicted_chapter == SpaceMarine.CHAPTER_GREY_KNIGHT:
                self.M5.Lcd.print("We are the Hammer!")
            elif predicted_chapter == SpaceMarine.CHAPTER_SPACE_WOLF:
                self.M5.Lcd.print("For Russ and the Allfather!")
            elif predicted_chapter == SpaceMarine.CHAPTER_BLOOD_ANGEL:
                self.M5.Lcd.print("For Sanguinius!")
            elif predicted_chapter == SpaceMarine.CHAOS_KHORNE:
                self.M5.Lcd.print("BLOOD FOR THE BLOOD GOD!")
            elif predicted_chapter == SpaceMarine.CHAOS_NURGLE:
                self.M5.Lcd.print("Grandfather's Blessings!")
            else:
                self.M5.Lcd.print("For the Emperor!")

            time.sleep(3.0)

        # Final flash
        self.M5.Lcd.fillScreen(flash_color)
        time.sleep(0.2)
        self.M5.Lcd.fillScreen(config.COLOR_BG)

        # Force full redraw on next frame
        self.needs_full_redraw = True

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
