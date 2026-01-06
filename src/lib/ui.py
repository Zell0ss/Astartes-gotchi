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

    def present_emperor_whisper(self, imposter_god, chaos_system):
        """
        Present Emperor's whisper event (Phase 3)

        The player must choose:
        - ACCEPT: Trust it's the Emperor (safe choice, major blessings)
        - SUSPECT HERESY: Try to identify which Chaos god is impersonating

        Args:
            imposter_god: Which god is impersonating ("khorne", "slaanesh", "nurgle", "tzeentch", "undivided")
            chaos_system: ChaosSystem instance for getting whisper text

        Returns:
            tuple: (choice, correct_id, quality)
                   choice: "accept" or "resist"
                   correct_id: True if correctly identified imposter (only relevant if resist)
                   quality: 1.0 for accept, 0.0-1.0 for resist based on correctness
        """
        if not self.hardware_available:
            return ("accept", True, 1.0)

        # Clear any pending touches
        self.clear_touches()

        # === PHASE 1: Emperor's Voice Screen (3 seconds) ===
        self.M5.Lcd.fillScreen(config.COLOR_BG)

        # Golden border (Emperor's color)
        self.M5.Lcd.drawRect(5, 5, 310, 230, config.COLOR_IMPERIAL_GOLD)
        self.M5.Lcd.drawRect(6, 6, 308, 228, config.COLOR_IMPERIAL_GOLD)

        # Title
        self.M5.Lcd.setTextSize(2)
        self.M5.Lcd.setTextColor(config.COLOR_IMPERIAL_GOLD)
        self.M5.Lcd.setCursor(40, 30)
        self.M5.Lcd.print("A VOICE SPEAKS...")

        # Get Emperor's whisper text (subtly hints at imposter)
        whisper_text = chaos_system.get_emperor_whisper_text(imposter_god)

        # Display whisper text (wrap manually if needed)
        self.M5.Lcd.setTextSize(1)
        self.M5.Lcd.setTextColor(config.COLOR_TEXT)

        # Simple text wrapping (split on spaces, ~40 chars per line)
        words = whisper_text.split()
        lines = []
        current_line = ""
        for word in words:
            if len(current_line) + len(word) + 1 <= 40:
                current_line += (" " if current_line else "") + word
            else:
                lines.append(current_line)
                current_line = word
        if current_line:
            lines.append(current_line)

        # Draw wrapped text
        y_pos = 90
        for line in lines[:4]:  # Max 4 lines
            self.M5.Lcd.setCursor(20, y_pos)
            self.M5.Lcd.print(line)
            y_pos += 20

        # Aquila symbol (simplified as text)
        self.M5.Lcd.setTextSize(3)
        self.M5.Lcd.setTextColor(config.COLOR_IMPERIAL_GOLD)
        self.M5.Lcd.setCursor(130, 175)
        self.M5.Lcd.print("***")

        # Haptic pulse (reverent)
        try:
            self.M5.Power.setVibration(200)
            time.sleep(0.2)
            self.M5.Power.setVibration(0)
        except:
            pass

        # Display for 3 seconds
        time.sleep(3.0)

        # === PHASE 2: Choice Screen ===
        self.M5.Lcd.fillScreen(config.COLOR_BG)

        # Question
        self.M5.Lcd.setTextSize(2)
        self.M5.Lcd.setTextColor(config.COLOR_TEXT)
        self.M5.Lcd.setCursor(50, 40)
        self.M5.Lcd.print("Is this truly")
        self.M5.Lcd.setCursor(50, 65)
        self.M5.Lcd.print("the Emperor?")

        # ACCEPT button (left, golden)
        accept_rect = (10, 140, 140, 70)
        self.M5.Lcd.fillRect(*accept_rect, config.COLOR_IMPERIAL_GOLD)
        self.M5.Lcd.setCursor(35, 165)
        self.M5.Lcd.setTextColor(config.COLOR_BG)
        self.M5.Lcd.setTextSize(2)
        self.M5.Lcd.print("ACCEPT")

        # SUSPECT HERESY button (right, red)
        suspect_rect = (170, 140, 140, 70)
        self.M5.Lcd.fillRect(*suspect_rect, config.COLOR_BATTLE_FURY)
        self.M5.Lcd.setCursor(180, 155)
        self.M5.Lcd.setTextColor(config.COLOR_TEXT)
        self.M5.Lcd.setTextSize(1)
        self.M5.Lcd.print("SUSPECT")
        self.M5.Lcd.setCursor(185, 175)
        self.M5.Lcd.print("HERESY")

        # Wait for screen to settle
        time.sleep(0.5)
        self.clear_touches()

        if config.DEBUG:
            print(f">>> [EMPEROR WHISPER] Imposter: {imposter_god}, waiting for choice...")

        # Wait for choice
        choice = None
        while choice is None:
            self.M5.update()

            try:
                touch_count = self.M5.Touch.getCount()
                if touch_count > 0:
                    x = self.M5.Touch.getX()
                    y = self.M5.Touch.getY()

                    if self._point_in_rect(x, y, accept_rect):
                        # ACCEPT - faith rewarded!
                        if config.DEBUG:
                            print(">>> [EMPEROR WHISPER] Player ACCEPTED")

                        # Haptic feedback
                        try:
                            self.M5.Power.setVibration(150)
                            time.sleep(0.1)
                            self.M5.Power.setVibration(0)
                        except:
                            pass

                        time.sleep(0.2)
                        self.clear_touches()
                        choice = "accept"

                    elif self._point_in_rect(x, y, suspect_rect):
                        # SUSPECT HERESY - test of knowledge!
                        if config.DEBUG:
                            print(">>> [EMPEROR WHISPER] Player SUSPECTS HERESY")

                        # Haptic feedback
                        try:
                            self.M5.Power.setVibration(200)
                            time.sleep(0.1)
                            self.M5.Power.setVibration(0)
                        except:
                            pass

                        time.sleep(0.2)
                        self.clear_touches()
                        choice = "resist"
            except Exception as e:
                if config.DEBUG:
                    print(f">>> [EMPEROR WHISPER] Touch error: {e}")

            time.sleep(0.1)

        # === PHASE 3: Handle Choice ===
        if choice == "accept":
            # Show blessing screen
            self.M5.Lcd.fillScreen(config.COLOR_BG)

            self.M5.Lcd.setTextSize(2)
            self.M5.Lcd.setTextColor(config.COLOR_IMPERIAL_GOLD)
            self.M5.Lcd.setCursor(10, 80)
            self.M5.Lcd.print("The Emperor")
            self.M5.Lcd.setCursor(40, 110)
            self.M5.Lcd.print("Protects!")

            self.M5.Lcd.setTextSize(1)
            self.M5.Lcd.setTextColor(config.COLOR_TEXT)
            self.M5.Lcd.setCursor(45, 150)
            self.M5.Lcd.print("Your faith is rewarded")

            # Triple pulse (blessing)
            try:
                for _ in range(3):
                    self.M5.Power.setVibration(180)
                    time.sleep(0.1)
                    self.M5.Power.setVibration(0)
                    time.sleep(0.1)
            except:
                pass

            time.sleep(2.0)
            self.clear_touches()
            return ("accept", True, 1.0)

        else:  # choice == "resist"
            # === PHASE 4: God Identification Challenge ===
            identified_god = self._emperor_identify_imposter()

            # Check if correct
            correct_id = (identified_god == imposter_god)

            if config.DEBUG:
                print(f">>> [EMPEROR WHISPER] Player identified: {identified_god}, Actual: {imposter_god}, Correct: {correct_id}")

            # Show result screen
            self.M5.Lcd.fillScreen(config.COLOR_BG)

            if correct_id:
                # CORRECT! Maximum reward
                self.M5.Lcd.setTextSize(2)
                self.M5.Lcd.setTextColor(config.COLOR_IMPERIAL_GOLD)
                self.M5.Lcd.setCursor(20, 60)
                self.M5.Lcd.print("HERESY")
                self.M5.Lcd.setCursor(20, 90)
                self.M5.Lcd.print("DETECTED!")

                self.M5.Lcd.setTextSize(1)
                self.M5.Lcd.setTextColor(config.COLOR_TEXT)
                self.M5.Lcd.setCursor(15, 130)
                self.M5.Lcd.print("Your faith is")
                self.M5.Lcd.setCursor(15, 150)
                self.M5.Lcd.print("unshakeable!")

                # Strong triple pulse
                try:
                    for _ in range(3):
                        self.M5.Power.setVibration(250)
                        time.sleep(0.15)
                        self.M5.Power.setVibration(0)
                        time.sleep(0.1)
                except:
                    pass

            else:
                # WRONG! Rejected the Emperor
                self.M5.Lcd.setTextSize(2)
                self.M5.Lcd.setTextColor(config.COLOR_CORRUPTION)
                self.M5.Lcd.setCursor(30, 60)
                self.M5.Lcd.print("TEST OF")
                self.M5.Lcd.setCursor(40, 90)
                self.M5.Lcd.print("FAITH")
                self.M5.Lcd.setCursor(40, 120)
                self.M5.Lcd.print("FAILED")

                self.M5.Lcd.setTextSize(1)
                self.M5.Lcd.setTextColor(config.COLOR_TEXT)
                self.M5.Lcd.setCursor(25, 160)
                self.M5.Lcd.print("You rejected Him...")

                # Ominous single long pulse
                try:
                    self.M5.Power.setVibration(200)
                    time.sleep(0.5)
                    self.M5.Power.setVibration(0)
                except:
                    pass

            time.sleep(2.5)
            self.clear_touches()

            quality = 1.0 if correct_id else 0.0
            return ("resist", correct_id, quality)

    def _emperor_identify_imposter(self):
        """
        Show god identification screen (5 buttons)
        Player must identify which Chaos god is impersonating the Emperor

        Returns:
            str: God name selected by player
        """
        self.M5.Lcd.fillScreen(config.COLOR_BG)

        # Title
        self.M5.Lcd.setTextSize(1)
        self.M5.Lcd.setTextColor(config.COLOR_TEXT)
        self.M5.Lcd.setCursor(30, 15)
        self.M5.Lcd.print("Which Chaos god dares")
        self.M5.Lcd.setCursor(50, 35)
        self.M5.Lcd.print("impersonate Him?")

        # 5 buttons arranged: 2 rows of 2, 1 on bottom
        # Row 1: Khorne, Slaanesh
        # Row 2: Nurgle, Tzeentch
        # Row 3: Undivided (centered)

        buttons = {
            'khorne': (10, 70, 145, 50, config.COLOR_KHORNE, "KHORNE"),
            'slaanesh': (165, 70, 145, 50, config.COLOR_SLAANESH, "SLAANESH"),
            'nurgle': (10, 130, 145, 50, config.COLOR_NURGLE, "NURGLE"),
            'tzeentch': (165, 130, 145, 50, config.COLOR_TZEENTCH, "TZEENTCH"),
            'undivided': (85, 190, 150, 40, config.COLOR_CORRUPTION, "UNDIVIDED")
        }

        # Draw all buttons
        for god, (x, y, w, h, color, label) in buttons.items():
            self.M5.Lcd.fillRect(x, y, w, h, color)
            self.M5.Lcd.setCursor(x + 10, y + 20)
            self.M5.Lcd.setTextColor(config.COLOR_TEXT)
            self.M5.Lcd.setTextSize(2)
            self.M5.Lcd.print(label)

        # Wait for screen to settle
        time.sleep(0.5)
        self.clear_touches()

        if config.DEBUG:
            print(">>> [EMPEROR WHISPER] Showing god identification screen...")

        # Wait for selection
        while True:
            self.M5.update()

            try:
                touch_count = self.M5.Touch.getCount()
                if touch_count > 0:
                    x = self.M5.Touch.getX()
                    y = self.M5.Touch.getY()

                    # Check each button
                    for god, (bx, by, bw, bh, color, label) in buttons.items():
                        if bx <= x <= bx + bw and by <= y <= by + bh:
                            if config.DEBUG:
                                print(f">>> [EMPEROR WHISPER] Player identified: {god.upper()}")

                            # Haptic feedback
                            try:
                                self.M5.Power.setVibration(180)
                                time.sleep(0.1)
                                self.M5.Power.setVibration(0)
                            except:
                                pass

                            time.sleep(0.2)
                            self.clear_touches()
                            return god
            except Exception as e:
                if config.DEBUG:
                    print(f">>> [EMPEROR WHISPER] Touch error: {e}")

            time.sleep(0.1)

    def present_chaos_whisper(self, god, chaos_system):
        """
        Present Chaos whisper event (Phase 3)

        The player must choose:
        - RESIST: Run god-specific challenge (player does NOT know which god!)
        - GIVE IN: Accept corruption immediately

        Args:
            god: Which Chaos god ("khorne", "slaanesh", "nurgle", "tzeentch")
            chaos_system: ChaosSystem instance for getting whisper text

        Returns:
            tuple: (choice, challenge_success, quality)
                   choice: "resist" or "give_in"
                   challenge_success: True if resist challenge succeeded
                   quality: 0.0-1.0 performance score
        """
        if not self.hardware_available:
            return ("resist", True, 1.0)

        # Clear any pending touches
        self.clear_touches()

        # === PHASE 1: Temptation Screen (3 seconds) ===
        self.M5.Lcd.fillScreen(config.COLOR_BG)

        # Purple/corruption border
        self.M5.Lcd.drawRect(5, 5, 310, 230, config.COLOR_CORRUPTION)
        self.M5.Lcd.drawRect(6, 6, 308, 228, config.COLOR_CORRUPTION)

        # Title
        self.M5.Lcd.setTextSize(2)
        self.M5.Lcd.setTextColor(config.COLOR_CORRUPTION)
        self.M5.Lcd.setCursor(20, 30)
        self.M5.Lcd.print("A VOICE WHISPERS...")

        # Get Chaos whisper text (god identity HIDDEN!)
        whisper_text = chaos_system.get_chaos_whisper_text(god)

        # Display whisper text (wrap manually if needed)
        self.M5.Lcd.setTextSize(1)
        self.M5.Lcd.setTextColor(config.COLOR_TEXT)

        # Simple text wrapping (split on spaces, ~40 chars per line)
        words = whisper_text.split()
        lines = []
        current_line = ""
        for word in words:
            if len(current_line) + len(word) + 1 <= 40:
                current_line += (" " if current_line else "") + word
            else:
                lines.append(current_line)
                current_line = word
        if current_line:
            lines.append(current_line)

        # Draw wrapped text
        y_pos = 90
        for line in lines[:4]:  # Max 4 lines
            self.M5.Lcd.setCursor(20, y_pos)
            self.M5.Lcd.print(line)
            y_pos += 20

        # Ominous symbol
        self.M5.Lcd.setTextSize(3)
        self.M5.Lcd.setTextColor(config.COLOR_CORRUPTION)
        self.M5.Lcd.setCursor(130, 175)
        self.M5.Lcd.print("...")

        # Haptic pulse (ominous)
        try:
            self.M5.Power.setVibration(200)
            time.sleep(0.2)
            self.M5.Power.setVibration(0)
        except:
            pass

        # Display for 3 seconds
        time.sleep(3.0)

        # === PHASE 2: Choice Screen ===
        self.M5.Lcd.fillScreen(config.COLOR_BG)

        # Question
        self.M5.Lcd.setTextSize(2)
        self.M5.Lcd.setTextColor(config.COLOR_TEXT)
        self.M5.Lcd.setCursor(30, 40)
        self.M5.Lcd.print("The whisper")
        self.M5.Lcd.setCursor(50, 65)
        self.M5.Lcd.print("tempts you...")

        # RESIST button (left, gold)
        resist_rect = (10, 140, 140, 70)
        self.M5.Lcd.fillRect(*resist_rect, config.COLOR_IMPERIAL_GOLD)
        self.M5.Lcd.setCursor(35, 165)
        self.M5.Lcd.setTextColor(config.COLOR_BG)
        self.M5.Lcd.setTextSize(2)
        self.M5.Lcd.print("RESIST")

        # GIVE IN button (right, corruption purple)
        give_in_rect = (170, 140, 140, 70)
        self.M5.Lcd.fillRect(*give_in_rect, config.COLOR_CORRUPTION)
        self.M5.Lcd.setCursor(185, 155)
        self.M5.Lcd.setTextColor(config.COLOR_TEXT)
        self.M5.Lcd.setTextSize(2)
        self.M5.Lcd.print("GIVE IN")

        # Wait for screen to settle
        time.sleep(0.5)
        self.clear_touches()

        if config.DEBUG:
            print(f">>> [CHAOS WHISPER] God: {god}, waiting for choice...")

        # Wait for choice
        choice = None
        while choice is None:
            self.M5.update()

            try:
                touch_count = self.M5.Touch.getCount()
                if touch_count > 0:
                    x = self.M5.Touch.getX()
                    y = self.M5.Touch.getY()

                    if self._point_in_rect(x, y, resist_rect):
                        # RESIST - run challenge!
                        if config.DEBUG:
                            print(">>> [CHAOS WHISPER] Player RESISTS")

                        # Haptic feedback
                        try:
                            self.M5.Power.setVibration(150)
                            time.sleep(0.1)
                            self.M5.Power.setVibration(0)
                        except:
                            pass

                        time.sleep(0.2)
                        self.clear_touches()
                        choice = "resist"

                    elif self._point_in_rect(x, y, give_in_rect):
                        # GIVE IN - immediate corruption!
                        if config.DEBUG:
                            print(">>> [CHAOS WHISPER] Player GIVES IN")

                        # Haptic feedback
                        try:
                            self.M5.Power.setVibration(200)
                            time.sleep(0.1)
                            self.M5.Power.setVibration(0)
                        except:
                            pass

                        time.sleep(0.2)
                        self.clear_touches()
                        choice = "give_in"
            except Exception as e:
                if config.DEBUG:
                    print(f">>> [CHAOS WHISPER] Touch error: {e}")

            time.sleep(0.1)

        # === PHASE 3: Handle Choice ===
        if choice == "give_in":
            # Show corruption screen
            self.M5.Lcd.fillScreen(config.COLOR_BG)

            self.M5.Lcd.setTextSize(2)
            self.M5.Lcd.setTextColor(config.COLOR_CORRUPTION)
            self.M5.Lcd.setCursor(30, 80)
            self.M5.Lcd.print("You embrace")
            self.M5.Lcd.setCursor(30, 110)
            self.M5.Lcd.print("the darkness...")

            # Double pulse (corruption)
            try:
                for _ in range(2):
                    self.M5.Power.setVibration(200)
                    time.sleep(0.15)
                    self.M5.Power.setVibration(0)
                    time.sleep(0.1)
            except:
                pass

            time.sleep(2.0)
            self.clear_touches()
            return ("give_in", False, 0.0)

        else:  # choice == "resist"
            # === PHASE 4: Run God-Specific Challenge ===
            # Player does NOT know which god!
            if god == "khorne":
                challenge_success, quality = self._challenge_khorne()
            elif god == "slaanesh":
                challenge_success, quality = self._challenge_slaanesh()
            elif god == "nurgle":
                challenge_success, quality = self._challenge_nurgle()
            elif god == "tzeentch":
                challenge_success, quality = self._challenge_tzeentch()
            else:
                # Fallback (shouldn't happen)
                challenge_success, quality = (False, 0.0)

            # Show result screen
            self.M5.Lcd.fillScreen(config.COLOR_BG)

            if challenge_success:
                # SUCCESS! Resisted corruption
                self.M5.Lcd.setTextSize(2)
                self.M5.Lcd.setTextColor(config.COLOR_IMPERIAL_GOLD)
                self.M5.Lcd.setCursor(10, 80)
                self.M5.Lcd.print("Faith holds")
                self.M5.Lcd.setCursor(40, 110)
                self.M5.Lcd.print("strong!")

                self.M5.Lcd.setTextSize(1)
                self.M5.Lcd.setTextColor(config.COLOR_TEXT)
                self.M5.Lcd.setCursor(30, 150)
                self.M5.Lcd.print("The Emperor protects")

                # Triple pulse (victory)
                try:
                    for _ in range(3):
                        self.M5.Power.setVibration(180)
                        time.sleep(0.1)
                        self.M5.Power.setVibration(0)
                        time.sleep(0.1)
                except:
                    pass

            else:
                # FAILED! Succumbed to corruption
                self.M5.Lcd.setTextSize(2)
                self.M5.Lcd.setTextColor(config.COLOR_CORRUPTION)
                self.M5.Lcd.setCursor(20, 80)
                self.M5.Lcd.print("Will falters...")

                self.M5.Lcd.setTextSize(1)
                self.M5.Lcd.setTextColor(config.COLOR_TEXT)
                self.M5.Lcd.setCursor(20, 130)
                self.M5.Lcd.print("Corruption takes hold")

                # Ominous pulse
                try:
                    self.M5.Power.setVibration(200)
                    time.sleep(0.4)
                    self.M5.Power.setVibration(0)
                except:
                    pass

            time.sleep(2.0)
            self.clear_touches()

            return ("resist", challenge_success, quality)

    def _challenge_khorne(self):
        """
        Khorne challenge: Rapid screen tapping

        Success: Tap screen >= TAP_TARGET times within DURATION seconds
        Theme: Violence, action, bloodlust

        Returns:
            tuple: (success, quality)
                   success: True if target reached
                   quality: 0.0-1.0 based on tap count
        """
        if not self.hardware_available:
            return (True, 1.0)

        tap_count = 0
        start_time = time.time()
        vibration_end_time = 0

        self.clear_touches()

        if config.DEBUG:
            print(f">>> [KHORNE CHALLENGE] Start - Target: {config.KHORNE_TAP_TARGET} taps in {config.KHORNE_DURATION}s")
            print(f">>> [KHORNE] Raw frame counting - no debounce, no filters!")

        # Main challenge loop
        while True:
            elapsed = time.time() - start_time
            if elapsed >= config.KHORNE_DURATION:
                break

            # Render progress
            self.M5.Lcd.fillScreen(config.COLOR_BG)

            # Title
            self.M5.Lcd.setTextSize(2)
            self.M5.Lcd.setTextColor(config.COLOR_IMPERIAL_GOLD)
            self.M5.Lcd.setCursor(20, 30)
            self.M5.Lcd.print("RESIST THE")
            self.M5.Lcd.setCursor(40, 55)
            self.M5.Lcd.print("WHISPER!")

            # Tap counter
            self.M5.Lcd.setTextSize(3)
            self.M5.Lcd.setTextColor(config.COLOR_TEXT)
            self.M5.Lcd.setCursor(100, 100)
            self.M5.Lcd.print(str(tap_count))

            self.M5.Lcd.setTextSize(1)
            self.M5.Lcd.setCursor(80, 135)
            self.M5.Lcd.print(f"of {config.KHORNE_TAP_TARGET}")

            # Progress bar
            progress = tap_count / config.KHORNE_TAP_TARGET
            bar_width = int(280 * min(progress, 1.0))
            bar_color = config.COLOR_IMPERIAL_GOLD if progress < 1.0 else config.COLOR_TEXT
            self.M5.Lcd.fillRect(20, 170, bar_width, 20, bar_color)

            # Timer
            remaining = config.KHORNE_DURATION - elapsed
            self.M5.Lcd.setCursor(120, 205)
            self.M5.Lcd.print(f"{remaining:.1f}s")

            # Check for tap - RAW COUNTING (no filters!)
            self.M5.update()
            current_time = time.time()

            try:
                if self.M5.Touch.getCount() > 0:
                    # Count every frame with touch - no debounce, no edge detection
                    tap_count += 1

                    # Haptic feedback every 10 taps (to avoid constant vibration)
                    if tap_count % 10 == 0 and vibration_end_time == 0:
                        try:
                            self.M5.Power.setVibration(120)
                            vibration_end_time = current_time + 0.04
                        except:
                            pass

                    if config.DEBUG and tap_count % 10 == 0:
                        print(f">>> [KHORNE] Taps: {tap_count}/{config.KHORNE_TAP_TARGET}")
            except:
                pass

            # Stop vibration if time elapsed (non-blocking)
            if vibration_end_time > 0 and current_time >= vibration_end_time:
                try:
                    self.M5.Power.setVibration(0)
                    vibration_end_time = 0
                except:
                    pass

            time.sleep(0.02)  # 50 FPS for very responsive input

        # Calculate result
        success = tap_count >= config.KHORNE_TAP_TARGET
        quality = min(tap_count / config.KHORNE_TAP_TARGET, 1.0)

        if config.DEBUG:
            print(f">>> [KHORNE CHALLENGE] Complete - Taps: {tap_count}, Success: {success}, Quality: {quality:.2f}")

        self.clear_touches()
        return (success, quality)

    def _challenge_slaanesh(self):
        """
        Slaanesh challenge: Slow finger drag

        Success: Drag finger across screen in time window (MIN_TIME to MAX_TIME)
                 Must maintain speed <= MAX_SPEED pixels/second
                 Must complete MIN_DISTANCE pixels

        Theme: Excess, indulgence, sensuality (slow and deliberate)

        Returns:
            tuple: (success, quality)
                   success: True if drag completed correctly
                   quality: 0.0-1.0 based on smoothness
        """
        if not self.hardware_available:
            return (True, 1.0)

        start_pos = None
        last_pos = None
        total_distance = 0
        drag_start_time = None
        last_check_time = time.time()
        failed = False
        fail_reason = ""

        self.clear_touches()

        if config.DEBUG:
            print(f">>> [SLAANESH CHALLENGE] Start - Drag {config.SLAANESH_MIN_DISTANCE}px in {config.SLAANESH_MIN_TIME}-{config.SLAANESH_MAX_TIME}s")

        # Extra clear + delay to avoid phantom touches from previous screen
        time.sleep(0.3)
        self.clear_touches()

        # Main challenge loop
        while True:
            # Render progress
            self.M5.Lcd.fillScreen(config.COLOR_BG)

            # Title
            self.M5.Lcd.setTextSize(2)
            self.M5.Lcd.setTextColor(config.COLOR_IMPERIAL_GOLD)
            self.M5.Lcd.setCursor(20, 20)
            self.M5.Lcd.print("RESIST THE")
            self.M5.Lcd.setCursor(40, 45)
            self.M5.Lcd.print("WHISPER!")

            # Instructions or status
            self.M5.Lcd.setTextSize(1)
            self.M5.Lcd.setTextColor(config.COLOR_TEXT)
            if start_pos is None:
                self.M5.Lcd.setCursor(30, 90)
                self.M5.Lcd.print("Drag finger SLOWLY")
                self.M5.Lcd.setCursor(50, 110)
                self.M5.Lcd.print("across screen")
            else:
                elapsed = time.time() - drag_start_time
                self.M5.Lcd.setCursor(50, 90)
                self.M5.Lcd.print(f"Distance: {int(total_distance)}")
                self.M5.Lcd.setCursor(50, 110)
                self.M5.Lcd.print(f"Time: {elapsed:.1f}s")

            # Progress bar
            progress = total_distance / config.SLAANESH_MIN_DISTANCE
            bar_width = int(280 * min(progress, 1.0))
            bar_color = config.COLOR_CORRUPTION if progress < 1.0 else config.COLOR_IMPERIAL_GOLD
            self.M5.Lcd.fillRect(20, 150, bar_width, 20, bar_color)

            # Draw trail if dragging
            if last_pos:
                lx, ly = last_pos
                # Draw a small circle at finger position
                self.M5.Lcd.fillCircle(lx, ly, 5, config.COLOR_CORRUPTION)

            # Check for touch
            self.M5.update()
            try:
                touch_count = self.M5.Touch.getCount()
                current_time = time.time()

                if touch_count > 0:
                    x = self.M5.Touch.getX()
                    y = self.M5.Touch.getY()

                    if start_pos is None:
                        # Begin drag
                        start_pos = (x, y)
                        last_pos = (x, y)
                        drag_start_time = current_time
                        last_check_time = current_time

                        if config.DEBUG:
                            print(f">>> [SLAANESH] Drag started at ({x}, {y})")

                    else:
                        # Continue drag - calculate movement
                        dx = x - last_pos[0]
                        dy = y - last_pos[1]
                        distance = (dx**2 + dy**2) ** 0.5

                        dt = current_time - last_check_time
                        if dt > 0:
                            speed = distance / dt

                            # Check if too fast
                            if speed > config.SLAANESH_MAX_SPEED:
                                failed = True
                                fail_reason = "TOO FAST!"
                                if config.DEBUG:
                                    print(f">>> [SLAANESH] FAILED - Speed: {speed:.1f} px/s (max: {config.SLAANESH_MAX_SPEED})")
                                break

                        total_distance += distance
                        last_pos = (x, y)
                        last_check_time = current_time

                        # Check if completed
                        if total_distance >= config.SLAANESH_MIN_DISTANCE:
                            elapsed = current_time - drag_start_time

                            if config.SLAANESH_MIN_TIME <= elapsed <= config.SLAANESH_MAX_TIME:
                                # SUCCESS!
                                if config.DEBUG:
                                    print(f">>> [SLAANESH] SUCCESS - Distance: {total_distance:.1f}, Time: {elapsed:.1f}s")
                                self.clear_touches()
                                return (True, 1.0)

                            elif elapsed < config.SLAANESH_MIN_TIME:
                                failed = True
                                fail_reason = "TOO EAGER!"
                                if config.DEBUG:
                                    print(f">>> [SLAANESH] FAILED - Too fast ({elapsed:.1f}s < {config.SLAANESH_MIN_TIME}s)")
                                break

                            else:  # elapsed > MAX_TIME
                                failed = True
                                fail_reason = "TOO SLOW!"
                                if config.DEBUG:
                                    print(f">>> [SLAANESH] FAILED - Too slow ({elapsed:.1f}s > {config.SLAANESH_MAX_TIME}s)")
                                break

                else:
                    # Finger lifted
                    if start_pos is not None:
                        elapsed = current_time - drag_start_time

                        if total_distance < config.SLAANESH_MIN_DISTANCE:
                            failed = True
                            fail_reason = "INCOMPLETE!"
                            if config.DEBUG:
                                print(f">>> [SLAANESH] FAILED - Finger lifted, distance: {total_distance:.1f}")
                            break

            except:
                pass

            time.sleep(0.05)  # 20 FPS

        # Failed
        if failed:
            # Show failure reason briefly
            self.M5.Lcd.fillScreen(config.COLOR_BG)
            self.M5.Lcd.setTextSize(2)
            self.M5.Lcd.setTextColor(config.COLOR_CORRUPTION)
            self.M5.Lcd.setCursor(60, 100)
            self.M5.Lcd.print(fail_reason)
            time.sleep(1.0)

        self.clear_touches()
        quality = min(total_distance / config.SLAANESH_MIN_DISTANCE, 1.0) if start_pos else 0.0
        return (False, quality)

    def _challenge_nurgle(self):
        """
        Nurgle challenge: Device stillness (IMU-based)

        Player must hold device completely still for NURGLE_DURATION seconds.
        Uses accelerometer only (gyro has too much drift).

        Theme: Nurgle demands ACCEPTANCE and STILLNESS. Embrace the decay,
        stop struggling, just... rest.

        Returns:
            tuple: (success, quality)
                - success: True if stayed still for required duration
                - quality: 0.0-1.0 based on how still (lower movement = higher quality)
        """
        import math

        if config.DEBUG:
            print(">>> [NURGLE CHALLENGE] Stillness detection starting...")

        # Clear any pending touches
        self.clear_touches()

        # Challenge parameters
        duration = config.NURGLE_DURATION  # 5s test, 10s production
        movement_threshold = config.NURGLE_MOVEMENT_THRESHOLD  # 0.1 G-force

        # Show instruction screen
        self.M5.Lcd.fillScreen(config.COLOR_BG)
        self.M5.Lcd.setTextColor(config.COLOR_TEXT)
        self.M5.Lcd.setTextSize(2)
        self.M5.Lcd.setCursor(20, 10)
        self.M5.Lcd.print("RESIST THE WHISPER!")

        self.M5.Lcd.setTextSize(1)
        self.M5.Lcd.setCursor(20, 50)
        self.M5.Lcd.print("Hold device COMPLETELY")
        self.M5.Lcd.setCursor(20, 70)
        self.M5.Lcd.print("STILL. Do not move.")
        self.M5.Lcd.setCursor(20, 90)
        self.M5.Lcd.print("Accept the stillness...")

        time.sleep(2)
        self.clear_touches()  # Clear any touches from instruction screen

        # Challenge loop
        start_time = time.time()
        total_movement = 0.0
        movement_violations = 0
        last_check_time = start_time
        sample_count = 0

        if config.DEBUG:
            print(f">>> [NURGLE] Duration: {duration}s, Threshold: {movement_threshold}G")

        while True:
            self.M5.update()
            current_time = time.time()
            elapsed = current_time - start_time

            # Check if duration complete
            if elapsed >= duration:
                # Success!
                quality = max(0.0, 1.0 - (movement_violations / (sample_count + 1)))
                if config.DEBUG:
                    print(f">>> [NURGLE] SUCCESS! Violations: {movement_violations}/{sample_count}, Quality: {quality:.2f}")

                # Success screen
                self.M5.Lcd.fillScreen(config.COLOR_BG)
                self.M5.Lcd.setTextColor(config.COLOR_IMPERIAL_GOLD)
                self.M5.Lcd.setTextSize(2)
                self.M5.Lcd.setCursor(40, 80)
                self.M5.Lcd.print("RESISTED!")
                self.M5.Lcd.setTextSize(1)
                self.M5.Lcd.setCursor(30, 120)
                self.M5.Lcd.print("Discipline triumphs!")

                # Triple haptic pulse (victory)
                self.M5.Power.setVibration(150)
                time.sleep(0.1)
                self.M5.Power.setVibration(0)
                time.sleep(0.05)
                self.M5.Power.setVibration(150)
                time.sleep(0.1)
                self.M5.Power.setVibration(0)
                time.sleep(0.05)
                self.M5.Power.setVibration(150)
                time.sleep(0.1)
                self.M5.Power.setVibration(0)

                time.sleep(2)
                self.clear_touches()
                return (True, quality)

            # Read accelerometer
            try:
                accel = self.M5.Imu.getAccel()
                accel_x, accel_y, accel_z = accel

                # Calculate magnitude (remove gravity)
                accel_mag = math.sqrt(accel_x*accel_x + accel_y*accel_y + accel_z*accel_z)
                movement = abs(accel_mag - 1.0)  # 1.0 = Earth's gravity

                # Check for movement violation
                if movement > movement_threshold:
                    movement_violations += 1
                    if config.DEBUG and movement_violations % 5 == 0:
                        print(f">>> [NURGLE] Movement detected: {movement:.3f}G (violations: {movement_violations})")

                    # FAIL if too much movement (more than 30% of samples)
                    if movement_violations > (sample_count * 0.3) and sample_count > 10:
                        if config.DEBUG:
                            print(f">>> [NURGLE] FAIL! Too much movement: {movement_violations}/{sample_count}")

                        # Failure screen
                        self.M5.Lcd.fillScreen(config.COLOR_BG)
                        self.M5.Lcd.setTextColor(config.COLOR_CORRUPTION)
                        self.M5.Lcd.setTextSize(2)
                        self.M5.Lcd.setCursor(50, 80)
                        self.M5.Lcd.print("FAILED!")
                        self.M5.Lcd.setTextSize(1)
                        self.M5.Lcd.setCursor(40, 120)
                        self.M5.Lcd.print("You moved too much!")

                        # Failure haptic (single long pulse)
                        self.M5.Power.setVibration(100)
                        time.sleep(0.3)
                        self.M5.Power.setVibration(0)

                        time.sleep(2)
                        self.clear_touches()
                        quality = max(0.0, 1.0 - (movement_violations / (sample_count + 1)))
                        return (False, quality)

                total_movement += movement
                sample_count += 1

            except Exception as e:
                if config.DEBUG:
                    print(f">>> [NURGLE] IMU error: {e}")
                # If IMU fails, consider it a fail
                return (False, 0.0)

            # Update display (every 10 samples = ~500ms)
            if sample_count % 10 == 0:
                remaining = duration - elapsed

                # Clear display area
                self.M5.Lcd.fillRect(0, 120, 320, 120, config.COLOR_BG)

                # Progress bar
                progress = elapsed / duration
                bar_width = int(280 * progress)
                self.M5.Lcd.fillRect(20, 140, bar_width, 15, config.COLOR_IMPERIAL_GOLD)
                self.M5.Lcd.drawRect(20, 140, 280, 15, config.COLOR_TEXT)

                # Timer
                self.M5.Lcd.setTextColor(config.COLOR_TEXT)
                self.M5.Lcd.setTextSize(2)
                self.M5.Lcd.setCursor(120, 170)
                self.M5.Lcd.print("{:.1f}s".format(remaining))

                # Movement indicator (if recent violation)
                if movement_violations > 0 and (sample_count - movement_violations < 5):
                    self.M5.Lcd.setTextColor(config.COLOR_CORRUPTION)
                    self.M5.Lcd.setTextSize(1)
                    self.M5.Lcd.setCursor(100, 210)
                    self.M5.Lcd.print("Movement!")

            time.sleep(0.05)  # 20 Hz sampling

    def _challenge_tzeentch(self):
        """
        Tzeentch challenge: Device shake/rotation (IMU-based)

        Player must shake device vigorously to reach required shake count.
        Uses accelerometer to detect high-G spikes.

        Theme: Tzeentch demands CHANGE and CHAOS. Shake the bones of fate,
        disturb the warp, embrace mutation!

        Returns:
            tuple: (success, quality)
                - success: True if reached required shake count in time
                - quality: 0.0-1.0 based on shake intensity and timing
        """
        import math

        if config.DEBUG:
            print(">>> [TZEENTCH CHALLENGE] Shake detection starting...")

        # Clear any pending touches
        self.clear_touches()

        # Challenge parameters
        duration = config.TZEENTCH_DURATION  # 4s test, 8s production
        shake_threshold = config.TZEENTCH_SHAKE_THRESHOLD  # 0.8 G-force
        required_shakes = config.TZEENTCH_REQUIRED_SHAKES  # 8 test, 15 production

        # Show instruction screen
        self.M5.Lcd.fillScreen(config.COLOR_BG)
        self.M5.Lcd.setTextColor(config.COLOR_TEXT)
        self.M5.Lcd.setTextSize(2)
        self.M5.Lcd.setCursor(20, 10)
        self.M5.Lcd.print("RESIST THE WHISPER!")

        self.M5.Lcd.setTextSize(1)
        self.M5.Lcd.setCursor(20, 50)
        self.M5.Lcd.print("SHAKE the device!")
        self.M5.Lcd.setCursor(20, 70)
        self.M5.Lcd.print("Disturb the warp!")
        self.M5.Lcd.setCursor(20, 90)
        self.M5.Lcd.print("Chaos demands change!")

        time.sleep(2)
        self.clear_touches()  # Clear any touches from instruction screen

        # Challenge loop
        start_time = time.time()
        shake_count = 0
        last_shake_time = 0
        shake_debounce = 0.05  # 50ms between shakes (very fast shake detection)
        total_intensity = 0.0
        peak_intensity = 0.0
        vibration_end_time = 0  # Track when to stop vibration

        if config.DEBUG:
            print(f">>> [TZEENTCH] Duration: {duration}s, Target: {required_shakes} shakes, Threshold: {shake_threshold}G")

        while True:
            self.M5.update()
            current_time = time.time()
            elapsed = current_time - start_time

            # Check if duration expired
            if elapsed >= duration:
                # Time's up - did we succeed?
                success = shake_count >= required_shakes
                quality = min(1.0, shake_count / required_shakes) if required_shakes > 0 else 0.0

                if success:
                    if config.DEBUG:
                        print(f">>> [TZEENTCH] SUCCESS! Shakes: {shake_count}/{required_shakes}, Quality: {quality:.2f}")

                    # Success screen
                    self.M5.Lcd.fillScreen(config.COLOR_BG)
                    self.M5.Lcd.setTextColor(config.COLOR_IMPERIAL_GOLD)
                    self.M5.Lcd.setTextSize(2)
                    self.M5.Lcd.setCursor(40, 80)
                    self.M5.Lcd.print("RESISTED!")
                    self.M5.Lcd.setTextSize(1)
                    self.M5.Lcd.setCursor(20, 120)
                    self.M5.Lcd.print("Warp disturbance ended!")

                    # Triple haptic pulse (victory)
                    self.M5.Power.setVibration(150)
                    time.sleep(0.1)
                    self.M5.Power.setVibration(0)
                    time.sleep(0.05)
                    self.M5.Power.setVibration(150)
                    time.sleep(0.1)
                    self.M5.Power.setVibration(0)
                    time.sleep(0.05)
                    self.M5.Power.setVibration(150)
                    time.sleep(0.1)
                    self.M5.Power.setVibration(0)

                    time.sleep(2)
                    self.clear_touches()
                    return (True, quality)
                else:
                    if config.DEBUG:
                        print(f">>> [TZEENTCH] FAIL! Only {shake_count}/{required_shakes} shakes")

                    # Failure screen
                    self.M5.Lcd.fillScreen(config.COLOR_BG)
                    self.M5.Lcd.setTextColor(config.COLOR_CORRUPTION)
                    self.M5.Lcd.setTextSize(2)
                    self.M5.Lcd.setCursor(50, 80)
                    self.M5.Lcd.print("FAILED!")
                    self.M5.Lcd.setTextSize(1)
                    self.M5.Lcd.setCursor(40, 120)
                    self.M5.Lcd.print("Not enough shakes!")

                    # Failure haptic (single long pulse)
                    self.M5.Power.setVibration(100)
                    time.sleep(0.3)
                    self.M5.Power.setVibration(0)

                    time.sleep(2)
                    self.clear_touches()
                    return (False, quality)

            # Read accelerometer
            try:
                accel = self.M5.Imu.getAccel()
                accel_x, accel_y, accel_z = accel

                # Calculate magnitude (remove gravity)
                accel_mag = math.sqrt(accel_x*accel_x + accel_y*accel_y + accel_z*accel_z)
                movement = abs(accel_mag - 1.0)  # 1.0 = Earth's gravity

                # Detect shake (high acceleration spike)
                if movement > shake_threshold:
                    # Debounce - only count if enough time since last shake
                    if current_time - last_shake_time > shake_debounce:
                        shake_count += 1
                        last_shake_time = current_time
                        total_intensity += movement
                        peak_intensity = max(peak_intensity, movement)

                        if config.DEBUG:
                            print(f">>> [TZEENTCH] SHAKE #{shake_count}! Intensity: {movement:.2f}G")

                        # Haptic pulse on each shake - non-blocking!
                        try:
                            self.M5.Power.setVibration(120)
                            vibration_end_time = current_time + 0.04  # Vibrate for 40ms
                        except:
                            pass

                        # Check if we reached target early (instant success)
                        if shake_count >= required_shakes:
                            quality = 1.0 + (0.2 * (duration - elapsed) / duration)  # Bonus for speed
                            quality = min(1.0, quality)

                            if config.DEBUG:
                                print(f">>> [TZEENTCH] TARGET REACHED EARLY! Quality: {quality:.2f}")

                            # Success screen
                            self.M5.Lcd.fillScreen(config.COLOR_BG)
                            self.M5.Lcd.setTextColor(config.COLOR_IMPERIAL_GOLD)
                            self.M5.Lcd.setTextSize(2)
                            self.M5.Lcd.setCursor(40, 80)
                            self.M5.Lcd.print("RESISTED!")
                            self.M5.Lcd.setTextSize(1)
                            self.M5.Lcd.setCursor(20, 120)
                            self.M5.Lcd.print("Warp disturbance ended!")

                            # Triple haptic pulse (victory)
                            self.M5.Power.setVibration(150)
                            time.sleep(0.1)
                            self.M5.Power.setVibration(0)
                            time.sleep(0.05)
                            self.M5.Power.setVibration(150)
                            time.sleep(0.1)
                            self.M5.Power.setVibration(0)
                            time.sleep(0.05)
                            self.M5.Power.setVibration(150)
                            time.sleep(0.1)
                            self.M5.Power.setVibration(0)

                            time.sleep(2)
                            self.clear_touches()
                            return (True, quality)

            except Exception as e:
                if config.DEBUG:
                    print(f">>> [TZEENTCH] IMU error: {e}")
                # Continue even if IMU fails occasionally
                pass

            # Update display (every frame = 50ms)
            remaining = duration - elapsed

            # Clear display area
            self.M5.Lcd.fillRect(0, 120, 320, 120, config.COLOR_BG)

            # Shake counter (big and prominent)
            self.M5.Lcd.setTextColor(config.COLOR_TZEENTCH)
            self.M5.Lcd.setTextSize(3)
            self.M5.Lcd.setCursor(100, 130)
            self.M5.Lcd.print("{:2d}".format(shake_count))

            self.M5.Lcd.setTextSize(1)
            self.M5.Lcd.setCursor(110, 165)
            self.M5.Lcd.print("of {}".format(required_shakes))

            # Progress bar
            progress = shake_count / required_shakes if required_shakes > 0 else 0
            bar_width = int(280 * progress)
            self.M5.Lcd.fillRect(20, 185, bar_width, 10, config.COLOR_TZEENTCH)
            self.M5.Lcd.drawRect(20, 185, 280, 10, config.COLOR_TEXT)

            # Timer
            self.M5.Lcd.setTextColor(config.COLOR_TEXT)
            self.M5.Lcd.setTextSize(1)
            self.M5.Lcd.setCursor(130, 210)
            self.M5.Lcd.print("{:.1f}s".format(remaining))

            # Stop vibration if time elapsed (non-blocking)
            if vibration_end_time > 0 and time.time() >= vibration_end_time:
                try:
                    self.M5.Power.setVibration(0)
                    vibration_end_time = 0
                except:
                    pass

            time.sleep(0.02)  # 50 Hz refresh for responsive detection
