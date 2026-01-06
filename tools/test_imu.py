"""
IMU Test Script for M5Stack Core2
Tests gyroscope and accelerometer for Chaos Whisper challenges

Hardware: M5Stack Core2 v1.1 (MPU6886 IMU)
Purpose: Explore M5.Imu API and calibrate thresholds for:
  - Nurgle challenge: Stillness detection
  - Tzeentch challenge: Shake detection

Usage:
  1. Deploy to device: mpremote cp tools/test_imu.py :main.py
  2. Reset device
  3. Observe values on screen + REPL output
  4. Try different motions:
     - Leave completely still (for Nurgle baseline)
     - Gentle movement (threshold testing)
     - Shake vigorously (for Tzeentch detection)
"""

import M5
import time
import math

# Initialize hardware
M5.begin()
M5.Lcd.fillScreen(0x000000)
M5.Lcd.setBrightness(80)

# Colors (RGB888)
COLOR_WHITE = 0xFFFFFF
COLOR_GREEN = 0x00FF00
COLOR_YELLOW = 0xFFFF00
COLOR_RED = 0xFF0000
COLOR_BLUE = 0x0000FF

# Thresholds to test (will be calibrated based on results)
STILLNESS_THRESHOLD = 0.2  # G-force - below this = still
SHAKE_THRESHOLD = 1.5      # G-force - above this = shake

def calculate_magnitude(x, y, z):
    """Calculate total magnitude from 3-axis readings"""
    return math.sqrt(x*x + y*y + z*z)

def main():
    print("=" * 40)
    print("IMU TEST - Chaos Whisper Challenges")
    print("=" * 40)
    print("")
    print("Testing for:")
    print("  - Nurgle: Stillness detection")
    print("  - Tzeentch: Shake detection")
    print("")
    print("Try these motions:")
    print("  1. Leave completely still (10s)")
    print("  2. Gentle tilt/movement")
    print("  3. Shake vigorously")
    print("")

    # Title
    M5.Lcd.fillScreen(0x000000)
    M5.Lcd.setTextColor(COLOR_WHITE)
    M5.Lcd.setTextSize(2)
    M5.Lcd.setCursor(40, 10)
    M5.Lcd.print("IMU TEST")

    M5.Lcd.setTextSize(1)
    M5.Lcd.setCursor(10, 40)
    M5.Lcd.print("Gyro (deg/s):")
    M5.Lcd.setCursor(10, 90)
    M5.Lcd.print("Accel (G-force):")
    M5.Lcd.setCursor(10, 140)
    M5.Lcd.print("Magnitude:")
    M5.Lcd.setCursor(10, 190)
    M5.Lcd.print("Status:")

    # Tracking for shake detection
    shake_count = 0
    last_shake_time = 0

    # Main loop
    loop_count = 0
    while True:
        M5.update()

        # Read IMU data
        # Note: M5.Imu API may vary - trying common methods
        try:
            # Try UIFlow2 API
            gyro = M5.Imu.getGyro()  # Returns (x, y, z) in deg/s
            accel = M5.Imu.getAccel()  # Returns (x, y, z) in G-force

            gyro_x, gyro_y, gyro_z = gyro
            accel_x, accel_y, accel_z = accel

        except AttributeError:
            # Fallback API (if UIFlow2 uses different method)
            M5.Lcd.setTextColor(COLOR_RED)
            M5.Lcd.setCursor(10, 215)
            M5.Lcd.print("ERROR: Check IMU API")
            print("ERROR: M5.Imu.getGyro() or getAccel() not found!")
            print("Try: dir(M5.Imu) to see available methods")
            time.sleep(1)
            continue

        # Calculate magnitudes
        gyro_mag = calculate_magnitude(gyro_x, gyro_y, gyro_z)
        accel_mag = calculate_magnitude(accel_x, accel_y, accel_z)

        # Remove gravity from accelerometer (1G = Earth's gravity)
        # For shake detection, we want movement magnitude without gravity bias
        accel_without_gravity = abs(accel_mag - 1.0)

        # Detect shake (high acceleration spike)
        current_time = time.time()
        if accel_without_gravity > SHAKE_THRESHOLD:
            if current_time - last_shake_time > 0.3:  # 300ms debounce
                shake_count += 1
                last_shake_time = current_time

        # Determine status
        if gyro_mag < STILLNESS_THRESHOLD and accel_without_gravity < STILLNESS_THRESHOLD:
            status = "STILL"
            status_color = COLOR_GREEN
        elif accel_without_gravity > SHAKE_THRESHOLD:
            status = "SHAKING!"
            status_color = COLOR_RED
        else:
            status = "MOVING"
            status_color = COLOR_YELLOW

        # Update display (every 5 loops = ~250ms)
        if loop_count % 5 == 0:
            # Clear data areas
            M5.Lcd.fillRect(10, 55, 300, 70, 0x000000)

            # Gyro
            M5.Lcd.setTextColor(COLOR_BLUE)
            M5.Lcd.setCursor(10, 55)
            M5.Lcd.print("X: {:6.2f}  Y: {:6.2f}".format(gyro_x, gyro_y))
            M5.Lcd.setCursor(10, 70)
            M5.Lcd.print("Z: {:6.2f}  Mag: {:6.2f}".format(gyro_z, gyro_mag))

            # Accel
            M5.Lcd.setTextColor(COLOR_BLUE)
            M5.Lcd.setCursor(10, 105)
            M5.Lcd.print("X: {:6.2f}  Y: {:6.2f}".format(accel_x, accel_y))
            M5.Lcd.setCursor(10, 120)
            M5.Lcd.print("Z: {:6.2f}  Mag: {:6.2f}".format(accel_z, accel_mag))

            # Magnitude (without gravity)
            M5.Lcd.setTextColor(COLOR_YELLOW)
            M5.Lcd.setCursor(10, 155)
            M5.Lcd.print("Gyro: {:6.2f}  Accel: {:6.2f}".format(gyro_mag, accel_without_gravity))
            M5.Lcd.setCursor(10, 170)
            M5.Lcd.print("Shakes detected: {}".format(shake_count))

            # Status
            M5.Lcd.setTextColor(status_color)
            M5.Lcd.setCursor(10, 205)
            M5.Lcd.print(status + "     ")  # Extra spaces to clear old text

        # Print to REPL every 1 second
        if loop_count % 20 == 0:
            print("Gyro: ({:6.2f}, {:6.2f}, {:6.2f}) mag={:6.2f} | ".format(
                gyro_x, gyro_y, gyro_z, gyro_mag), end="")
            print("Accel: ({:6.2f}, {:6.2f}, {:6.2f}) mag={:6.2f} | ".format(
                accel_x, accel_y, accel_z, accel_without_gravity), end="")
            print("Status: {} | Shakes: {}".format(status, shake_count))

        loop_count += 1
        time.sleep(0.05)  # 20 Hz refresh

# Run test
try:
    main()
except KeyboardInterrupt:
    print("\nTest interrupted by user")
    M5.Lcd.fillScreen(0x000000)
    M5.Lcd.setTextColor(COLOR_WHITE)
    M5.Lcd.setCursor(60, 110)
    M5.Lcd.print("Test Complete")
except Exception as e:
    print("\nERROR:", str(e))
    M5.Lcd.fillScreen(0xFF0000)
    M5.Lcd.setTextColor(COLOR_WHITE)
    M5.Lcd.setCursor(20, 100)
    M5.Lcd.print("ERROR - See REPL")
    M5.Lcd.setCursor(20, 120)
    M5.Lcd.print(str(e)[:40])
