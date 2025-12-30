# Astartes-Gotchi Makefile
# For the Emperor! 🦅

.PHONY: help deploy miniterm console

# Default port for M5Stack Core2
PORT := /dev/ttyACM0

help:
	@echo "🦅 Astartes-Gotchi - Available commands:"
	@echo ""
	@echo "  make deploy    - Deploy code to M5Stack Core2"
	@echo "  make miniterm  - Open serial console (miniterm)"
	@echo "  make console   - Alias for miniterm"
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
