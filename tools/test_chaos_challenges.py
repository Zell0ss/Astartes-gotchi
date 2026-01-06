"""
Chaos Challenges Test Script for M5Stack Core2
Tests Nurgle (stillness) and Tzeentch (shake) IMU challenges

Hardware: M5Stack Core2 v1.1 (MPU6886 IMU)
Purpose: Test all 4 Chaos god challenges in sequence

Usage:
  1. Deploy: make restore-main (ensure full codebase is deployed)
  2. Modify main.py to call this test loop instead of normal game loop
  3. OR: Deploy as standalone: mpremote cp tools/test_chaos_challenges.py :main.py

Test Sequence:
  1. Khorne - Rapid tapping
  2. Slaanesh - Slow drag
  3. Nurgle - Stillness
  4. Tzeentch - Shake
"""

import M5
import sys

# Add lib to path
sys.path.append('/flash/lib')

import config
from ui import AstartesUI

# Initialize hardware
M5.begin()
M5.Lcd.fillScreen(0x000000)
M5.Lcd.setBrightness(80)

# Colors (RGB888)
COLOR_WHITE = 0xFFFFFF
COLOR_GREEN = 0x00FF00
COLOR_RED = 0xFF0000
COLOR_BLUE = 0x0000FF
COLOR_GOLD = 0xFFD700

def wait_for_button(ui):
    """Wait for touch to continue"""
    M5.Lcd.setTextColor(COLOR_BLUE)
    M5.Lcd.setTextSize(1)
    M5.Lcd.setCursor(60, 220)
    M5.Lcd.print("Touch to continue...")

    ui.clear_touches()
    while True:
        M5.update()
        if M5.Touch.getCount() > 0:
            ui.clear_touches()
            return
        import time
        time.sleep(0.1)

def main():
    import time

    print("=" * 40)
    print("CHAOS CHALLENGES TEST")
    print("=" * 40)
    print("")
    print("Testing all 4 god challenges:")
    print("  1. Khorne - Rapid tapping")
    print("  2. Slaanesh - Slow drag")
    print("  3. Nurgle - Stillness (IMU)")
    print("  4. Tzeentch - Shake (IMU)")
    print("")

    ui = AstartesUI()

    challenges = [
        ("KHORNE", "Rapid Tapping", ui._challenge_khorne),
        ("SLAANESH", "Slow Drag", ui._challenge_slaanesh),
        ("NURGLE", "Stillness", ui._challenge_nurgle),
        ("TZEENTCH", "Shake", ui._challenge_tzeentch),
    ]

    results = []

    for god, name, challenge_func in challenges:
        # Show intro screen
        M5.Lcd.fillScreen(0x000000)
        M5.Lcd.setTextColor(COLOR_GOLD)
        M5.Lcd.setTextSize(2)
        M5.Lcd.setCursor(40, 60)
        M5.Lcd.print("TESTING:")

        M5.Lcd.setTextSize(2)
        M5.Lcd.setCursor(40, 100)
        M5.Lcd.print(god)

        M5.Lcd.setTextSize(1)
        M5.Lcd.setCursor(40, 140)
        M5.Lcd.print(name)

        print(f"\n>>> Testing {god} ({name})...")

        wait_for_button(ui)

        # Run challenge
        try:
            success, quality = challenge_func()
            results.append((god, name, success, quality))

            result_text = "SUCCESS" if success else "FAILED"
            result_color = COLOR_GREEN if success else COLOR_RED

            print(f">>> {god} result: {result_text}, quality={quality:.2f}")

            # Show result
            M5.Lcd.fillScreen(0x000000)
            M5.Lcd.setTextColor(result_color)
            M5.Lcd.setTextSize(2)
            M5.Lcd.setCursor(40, 80)
            M5.Lcd.print(result_text)

            M5.Lcd.setTextColor(COLOR_WHITE)
            M5.Lcd.setTextSize(1)
            M5.Lcd.setCursor(40, 120)
            M5.Lcd.print(f"Quality: {quality:.2f}")

            time.sleep(2)

        except Exception as e:
            print(f">>> ERROR in {god} challenge: {e}")
            results.append((god, name, False, 0.0))

            # Show error
            M5.Lcd.fillScreen(0xFF0000)
            M5.Lcd.setTextColor(COLOR_WHITE)
            M5.Lcd.setTextSize(1)
            M5.Lcd.setCursor(20, 100)
            M5.Lcd.print("ERROR!")
            M5.Lcd.setCursor(20, 120)
            M5.Lcd.print(str(e)[:30])

            time.sleep(3)

    # Final results screen
    M5.Lcd.fillScreen(0x000000)
    M5.Lcd.setTextColor(COLOR_GOLD)
    M5.Lcd.setTextSize(2)
    M5.Lcd.setCursor(40, 10)
    M5.Lcd.print("TEST COMPLETE")

    M5.Lcd.setTextSize(1)
    y = 50
    for god, name, success, quality in results:
        result_text = "PASS" if success else "FAIL"
        result_color = COLOR_GREEN if success else COLOR_RED

        M5.Lcd.setTextColor(COLOR_WHITE)
        M5.Lcd.setCursor(10, y)
        M5.Lcd.print(f"{god}:")

        M5.Lcd.setTextColor(result_color)
        M5.Lcd.setCursor(140, y)
        M5.Lcd.print(f"{result_text} ({quality:.2f})")

        y += 20

    M5.Lcd.setTextColor(COLOR_BLUE)
    M5.Lcd.setCursor(60, 200)
    M5.Lcd.print("Touch to restart")

    print("\n" + "=" * 40)
    print("TEST RESULTS:")
    print("=" * 40)
    for god, name, success, quality in results:
        result_text = "PASS" if success else "FAIL"
        print(f"  {god:12s} ({name:15s}): {result_text:6s} quality={quality:.2f}")
    print("=" * 40)

    # Wait for touch to restart
    ui.clear_touches()
    while True:
        M5.update()
        if M5.Touch.getCount() > 0:
            # Restart test
            main()
            return
        time.sleep(0.1)

# Run test loop
try:
    main()
except KeyboardInterrupt:
    print("\nTest interrupted by user")
    M5.Lcd.fillScreen(0x000000)
    M5.Lcd.setTextColor(COLOR_WHITE)
    M5.Lcd.setCursor(60, 110)
    M5.Lcd.print("Test Complete")
except Exception as e:
    print(f"\nERROR: {e}")
    import sys
    sys.print_exception(e)
    M5.Lcd.fillScreen(0xFF0000)
    M5.Lcd.setTextColor(COLOR_WHITE)
    M5.Lcd.setCursor(20, 100)
    M5.Lcd.print("FATAL ERROR")
    M5.Lcd.setCursor(20, 120)
    M5.Lcd.print(str(e)[:40])
