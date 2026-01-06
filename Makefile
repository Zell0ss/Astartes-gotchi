# Astartes-Gotchi Makefile
# For the Emperor! 🦅

.PHONY: help deploy miniterm console config-fast config-normal config-status test-imu test-challenges restore-main

# Default port for M5Stack Core2
PORT := /dev/ttyACM0

help:
	@echo "🦅 Astartes-Gotchi - Available commands:"
	@echo ""
	@echo "  make deploy         - Deploy code to M5Stack Core2"
	@echo "  make miniterm       - Open serial console (miniterm)"
	@echo "  make console        - Alias for miniterm"
	@echo ""
	@echo "  make test-imu       - Deploy IMU test script (auto-backup main.py)"
	@echo "  make test-challenges - Deploy Chaos challenges test (auto-backup main.py)"
	@echo "  make restore-main   - Restore original main.py (after tests)"
	@echo ""
	@echo "  make config-fast    - Switch to FAST evolution config (30s/60s/90s)"
	@echo "  make config-normal  - Switch to NORMAL evolution config (1h/2d/4d)"
	@echo "  make config-status  - Show which config is active"
	@echo ""
	@echo "Default port: $(PORT)"
	@echo "For the Emperor! ⚔️"

deploy:
	@echo "🚀 Deploying to M5Stack Core2..."
	@./tools/deploy.sh $(PORT)

miniterm:
	@echo "📡 Opening serial console on $(PORT)"
	@echo "Exit: Ctrl+T then Q"
	@python -m serial.tools.miniterm $(PORT) 115200

console: miniterm

config-fast:
	@echo "⚡ Switching to FAST evolution config..."
	@if [ ! -f src/config_fast.py ]; then \
		echo "❌ Error: src/config_fast.py not found!"; \
		echo "Run: cp src/config.py src/config_fast.py"; \
		exit 1; \
	fi
	@cp src/config_fast.py src/config.py
	@echo "✅ Fast config activated (30s → 60s → 90s evolution)"
	@echo "⚠️  Remember to deploy: make deploy"

config-normal:
	@echo "🐌 Switching to NORMAL evolution config..."
	@if [ ! -f src/config_normal.py ]; then \
		echo "❌ Error: src/config_normal.py not found!"; \
		echo "Run: cp src/config.py.backup src/config_normal.py"; \
		exit 1; \
	fi
	@cp src/config_normal.py src/config.py
	@echo "✅ Normal config activated (1h → 2d → 4d evolution)"
	@echo "⚠️  Remember to deploy: make deploy"

config-status:
	@echo "📊 Current config status:"
	@echo ""
	@if grep -q "TEST MODE - ACCELERATED EVOLUTION" src/config.py 2>/dev/null; then \
		echo "  Active: ⚡ FAST (Test Mode)"; \
		echo "  Evolution: 30s → 60s → 90s (3 min total)"; \
	elif grep -q "0.1.0-MVP\"" src/config.py 2>/dev/null; then \
		echo "  Active: 🐌 NORMAL (Production)"; \
		echo "  Evolution: 1h → 2d → 4d (7 days total)"; \
	else \
		echo "  Active: ❓ UNKNOWN"; \
	fi
	@echo ""
	@echo "Available configs:"
	@if [ -f src/config_fast.py ]; then echo "  ✓ src/config_fast.py (fast)"; else echo "  ✗ src/config_fast.py (missing)"; fi
	@if [ -f src/config_normal.py ]; then echo "  ✓ src/config_normal.py (normal)"; else echo "  ✗ src/config_normal.py (missing)"; fi

test-imu:
	@echo "🧪 Deploying IMU test script..."
	@echo "⚠️  Close any open serial console first (Ctrl+T → Q)"
	@sleep 2
	@echo "📦 Backing up current main.py on device..."
	@mpremote connect $(PORT) cp :main.py :main.py.backup 2>/dev/null || echo "  (No existing main.py, skipping backup)"
	@echo "🚀 Uploading tools/test_imu.py as main.py..."
	@mpremote connect $(PORT) cp tools/test_imu.py :main.py
	@echo "♻️  Resetting device..."
	@mpremote connect $(PORT) reset
	@echo ""
	@echo "✅ IMU test deployed!"
	@echo "📡 Open console to see output: make console"
	@echo "🔄 When done testing: make restore-main"

test-challenges:
	@echo "🔥 Deploying Chaos Challenges test..."
	@echo "⚠️  Close any open serial console first (Ctrl+T → Q)"
	@sleep 2
	@echo "📦 Ensuring full project is deployed first..."
	@./tools/deploy.sh $(PORT)
	@echo "📦 Backing up current main.py on device..."
	@mpremote connect $(PORT) cp :main.py :main.py.backup
	@echo "🚀 Uploading tools/test_chaos_challenges.py as main.py..."
	@mpremote connect $(PORT) cp tools/test_chaos_challenges.py :main.py
	@echo "♻️  Resetting device..."
	@mpremote connect $(PORT) reset
	@echo ""
	@echo "✅ Chaos Challenges test deployed!"
	@echo "📡 Open console to see output: make console"
	@echo "🎮 Touch screen to start each challenge"
	@echo "🔄 When done testing: make restore-main"

restore-main:
	@echo "🔄 Restoring original main.py..."
	@mpremote connect $(PORT) cp :main.py.backup :main.py || { \
		echo "❌ Error: No backup found!"; \
		echo "💡 Deploy full project: make deploy"; \
		exit 1; \
	}
	@echo "♻️  Resetting device..."
	@mpremote connect $(PORT) reset
	@echo "✅ Original main.py restored!"
	@echo "📡 Open console to verify: make console"
