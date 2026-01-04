# test_vibration.py - Test M5Stack Core2 vibration motor

import M5
import time

M5.begin()

print("=== VIBRATION MOTOR TEST ===")

# Check what vibration methods are available
print("\n1. Checking M5.Power methods:")
if hasattr(M5, 'Power'):
    power_methods = [m for m in dir(M5.Power) if not m.startswith('_')]
    for method in power_methods:
        print(f"   - M5.Power.{method}")

print("\n2. Checking M5.Speaker methods:")
if hasattr(M5, 'Speaker'):
    speaker_methods = [m for m in dir(M5.Speaker) if not m.startswith('_')]
    for method in speaker_methods:
        print(f"   - M5.Speaker.{method}")

print("\n3. Testing vibration methods...")

# Try common vibration API patterns
try:
    # Method 1: Power.setVibration (common pattern)
    if hasattr(M5.Power, 'setVibration'):
        print("   Testing M5.Power.setVibration(255)...")
        M5.Power.setVibration(255)
        time.sleep_ms(200)
        M5.Power.setVibration(0)
        print("   ✓ Vibration via setVibration works!")
except Exception as e:
    print(f"   ✗ setVibration failed: {e}")

try:
    # Method 2: Power.setVibrationIntensity
    if hasattr(M5.Power, 'setVibrationIntensity'):
        print("   Testing M5.Power.setVibrationIntensity(100)...")
        M5.Power.setVibrationIntensity(100)
        time.sleep_ms(200)
        M5.Power.setVibrationIntensity(0)
        print("   ✓ Vibration via setVibrationIntensity works!")
except Exception as e:
    print(f"   ✗ setVibrationIntensity failed: {e}")

try:
    # Method 3: Direct tone (sometimes vibration motor shares with speaker)
    if hasattr(M5.Speaker, 'tone'):
        print("   Testing M5.Speaker.tone (might cause vibration)...")
        M5.Speaker.tone(200, 100)
        print("   ✓ Tone played (check if vibration occurred)")
except Exception as e:
    print(f"   ✗ tone failed: {e}")

print("\n=== TEST COMPLETE ===")
print("Did you feel/hear vibration?")
