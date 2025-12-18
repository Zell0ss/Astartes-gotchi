#!/bin/bash
# Astartes-Gotchi - Development Environment Setup
# Run this script once to set up your development environment

set -e  # Exit on error

echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║                                                                  ║"
echo "║              🦅 ASTARTES-GOTCHI SETUP 🦅                         ║"
echo "║                                                                  ║"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo ""

# Check Python version
echo "📋 Checking Python version..."
if ! command -v python3 &> /dev/null; then
    echo "❌ ERROR: python3 not found. Please install Python 3.7 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "   Found Python $PYTHON_VERSION"

# Create virtual environment
echo ""
echo "📦 Creating virtual environment..."
if [ -d ".venv" ]; then
    echo "   .venv already exists, skipping..."
else
    python3 -m venv .venv
    echo "   ✅ Virtual environment created"
fi

# Activate venv
echo ""
echo "🔌 Activating virtual environment..."
source .venv/bin/activate

# Upgrade pip
echo ""
echo "⬆️  Upgrading pip..."
pip install --upgrade pip -q

# Install requirements
echo ""
echo "📥 Installing requirements..."
pip install -r requirements.txt

echo ""
echo "✅ Setup complete!"
echo ""
echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║                      NEXT STEPS                                  ║"
echo "╠══════════════════════════════════════════════════════════════════╣"
echo "║                                                                  ║"
echo "║  1. Activate environment:                                        ║"
echo "║     source .venv/bin/activate                                    ║"
echo "║                                                                  ║"
echo "║  2. Flash MicroPython (first time only):                         ║"
echo "║     See SETUP_MICROPYTHON.md                                     ║"
echo "║                                                                  ║"
echo "║  3. Deploy to device:                                            ║"
echo "║     ./tools/deploy.sh /dev/ttyUSB0                               ║"
echo "║                                                                  ║"
echo "║  4. Run tests (optional):                                        ║"
echo "║     python tests/test_marine.py                                  ║"
echo "║                                                                  ║"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo ""
echo "For the Emperor! 🦅"
