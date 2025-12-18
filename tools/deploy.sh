#!/bin/bash
# Astartes-Gotchi deployment script for Linux/LainOS

PORT=${1:-/dev/ttyUSB0}

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

# Upload all files from src/ to device root
mpremote connect $PORT cp -r src/* : 2>&1

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Upload complete"
    echo ""
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
    echo "Try: ls /dev/ttyUSB*"
    exit 1
fi
