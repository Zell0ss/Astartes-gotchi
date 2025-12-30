# test_colors_rgb888.py - Colores correctos para UIFlow2

import M5
from M5 import *
import time

M5.begin()

print("=== LCD COLOR TEST - RGB888 ===")

# Limpiar pantalla con negro (RGB888)
M5.Lcd.clear(0x000000)

# Título
M5.Lcd.setTextColor(0xFFFFFF, 0x000000)  # Blanco sobre negro
M5.Lcd.setCursor(50, 5)
M5.Lcd.setTextSize(2)
M5.Lcd.print("Test RGB888")

# RED - usando RGB888
M5.Lcd.fillRect(10, 40, 90, 50, 0xFF0000)
M5.Lcd.setCursor(110, 55)
M5.Lcd.setTextSize(1)
M5.Lcd.setTextColor(0xFFFFFF, 0x000000)
M5.Lcd.print("RED 0xFF0000")

# GREEN - usando RGB888
M5.Lcd.fillRect(10, 100, 90, 50, 0x00FF00)
M5.Lcd.setCursor(110, 115)
M5.Lcd.print("GREEN 0x00FF00")

# BLUE - usando RGB888
M5.Lcd.fillRect(10, 160, 90, 50, 0x0000FF)
M5.Lcd.setCursor(110, 175)
M5.Lcd.print("BLUE 0x0000FF")

# Colores secundarios para verificar
M5.Lcd.fillRect(220, 40, 40, 30, 0xFFFF00)   # Yellow
M5.Lcd.fillRect(220, 80, 40, 30, 0x00FFFF)   # Cyan
M5.Lcd.fillRect(220, 120, 40, 30, 0xFF00FF)  # Magenta

M5.Lcd.setCursor(270, 45)
M5.Lcd.print("Y")
M5.Lcd.setCursor(270, 85)
M5.Lcd.print("C")
M5.Lcd.setCursor(270, 125)
M5.Lcd.print("M")

print("Si los colores son correctos:")
print("  - Primer rect = ROJO")
print("  - Segundo rect = VERDE")
print("  - Tercer rect = AZUL")
print("  - Y=Amarillo, C=Cyan, M=Magenta")