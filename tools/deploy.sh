#!/bin/bash
# Astartes-Gotchi deployment script for Linux/LainOS

PORT=${1:-/dev/ttyACM0}

echo "🦅 ================================================"
echo "   ASTARTES-GOTCHI DEPLOYMENT"
echo "   For the Emperor!"
echo "================================================"
echo ""
echo "Target device: $PORT"
echo "Source: src/"
echo ""

# Check if mpremote is installed
if ! command -v mpremote &> /dev/null; then
    echo "❌ ERROR: mpremote not found"
    echo "Install with: pip3 install mpremote"
    exit 1
fi

# Check if source directory exists
if [ ! -d "src" ]; then
    echo "❌ ERROR: src/ directory not found"
    echo "Run this script from project root"
    exit 1
fi

echo "📦 Uploading files to M5Stack Core2..."
echo ""

# Upload all files from src/ to device root (one by one to ensure correct placement)
cd src

# Copy main files
mpremote connect $PORT cp boot.py : 2>&1
mpremote connect $PORT cp main.py : 2>&1
mpremote connect $PORT cp config.py : 2>&1

# Create and populate lib directory
mpremote connect $PORT mkdir :lib 2>&1
mpremote connect $PORT cp lib/space_marine.py :lib/ 2>&1
mpremote connect $PORT cp lib/ui.py :lib/ 2>&1
mpremote connect $PORT cp lib/save_manager.py :lib/ 2>&1
mpremote connect $PORT cp lib/chaos_system.py :lib/ 2>&1

# Create minigames subdirectory
mpremote connect $PORT mkdir :lib/minigames 2>&1
mpremote connect $PORT cp lib/minigames/__init__.py :lib/minigames/ 2>&1

cd ..

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Upload complete"
    echo ""
    echo "🔄 Cleaning old save files..."
    # Remove old save files to start fresh
    mpremote connect $PORT exec "import os; [os.remove(f) for f in ['astartes_save.json', 'astartes_save.json.bak'] if f in os.listdir()]" 2>&1

    echo "🔄 Resetting device..."

    # Soft reset (re-run boot.py and main.py)
    mpremote connect $PORT exec "import machine; machine.soft_reset()" 2>&1

    echo ""
    echo "🎮 ================================================"
    echo "   Device ready. For the Emperor! 🦅"
    echo "================================================"
else
    echo ""
    echo "❌ Upload failed. Check connection and port."
    echo "Try: ls $PORT*"
    exit 1
fi
