# Makefile for System Specifications GUI
# Convenient commands for building, running, and managing the application

.PHONY: install run run-basic run-enhanced test clean help setup check deps

# Default target
all: install

# Install the application and dependencies
install:
	@echo "Installing System Specifications GUI..."
	chmod +x install.sh run.sh *.py
	./install.sh

# Run the launcher (default)
run:
	@echo "Starting System Specifications Launcher..."
	./run.sh

# Run basic version directly
run-basic:
	@echo "Starting Basic System Specifications..."
	@if [ ! -d "venv" ]; then \
		echo "Virtual environment not found. Run 'make install' first."; \
		exit 1; \
	fi
	source venv/bin/activate && python3 system_specs_gui.py

# Run enhanced version directly
run-enhanced:
	@echo "Starting Enhanced System Specifications..."
	@if [ ! -d "venv" ]; then \
		echo "Virtual environment not found. Run 'make install' first."; \
		exit 1; \
	fi
	source venv/bin/activate && python3 enhanced_system_specs.py

# Test the installation
test:
	@echo "Testing installation..."
	@if [ ! -d "venv" ]; then \
		echo "Virtual environment not found. Run 'make install' first."; \
		exit 1; \
	fi
	source venv/bin/activate && python3 test_installation.py

# Check dependencies without installing
check:
	@echo "Checking system dependencies..."
	@echo "Python version:"
	@python3 --version
	@echo "\nSystem packages:"
	@dpkg -l | grep -E "(python3|python3-tk|python3-pip)" || echo "Some Python packages may be missing"
	@echo "\nOptional tools:"
	@which lspci >/dev/null 2>&1 && echo "✅ lspci available" || echo "❌ lspci not found"
	@which lsusb >/dev/null 2>&1 && echo "✅ lsusb available" || echo "❌ lsusb not found"
	@which dmidecode >/dev/null 2>&1 && echo "✅ dmidecode available" || echo "❌ dmidecode not found (sudo apt install dmidecode)"
	@which sensors >/dev/null 2>&1 && echo "✅ sensors available" || echo "❌ sensors not found (sudo apt install lm-sensors)"

# Setup development environment
setup: install
	@echo "Setting up development environment..."
	source venv/bin/activate && pip install --upgrade pip

# Check Python dependencies
deps:
	@echo "Checking Python dependencies..."
	@if [ -d "venv" ]; then \
		source venv/bin/activate && pip list; \
	else \
		echo "Virtual environment not found. Run 'make install' first."; \
	fi

# Clean build artifacts and temporary files
clean:
	@echo "Cleaning up..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.log" -delete 2>/dev/null || true
	find . -type f -name "hardware_report.txt" -delete 2>/dev/null || true
	@echo "Cleanup completed"

# Remove everything including virtual environment
clean-all: clean
	@echo "Removing virtual environment..."
	rm -rf venv
	rm -f *.desktop
	@echo "Complete cleanup finished"

# Create desktop entries
desktop:
	@echo "Creating desktop entries..."
	@if [ -d "$$HOME/.local/share/applications" ]; then \
		cp *.desktop "$$HOME/.local/share/applications/" 2>/dev/null || true; \
		echo "Desktop entries installed"; \
	else \
		echo "Applications directory not found"; \
	fi

# Show system information (quick preview)
info:
	@echo "Quick System Information:"
	@echo "========================"
	@echo "OS: $$(lsb_release -d 2>/dev/null | cut -f2 || echo 'Unknown')"
	@echo "Kernel: $$(uname -r)"
	@echo "CPU: $$(lscpu | grep 'Model name' | cut -d':' -f2 | xargs)"
	@echo "Memory: $$(free -h | grep '^Mem:' | awk '{print $$2}')"
	@echo "Architecture: $$(uname -m)"

# Package the application
package:
	@echo "Creating application package..."
	@DATE=$$(date +%Y%m%d); \
	tar -czf "system-specs-gui-$$DATE.tar.gz" \
		--exclude='venv' \
		--exclude='*.pyc' \
		--exclude='__pycache__' \
		--exclude='*.desktop' \
		--exclude='*.tar.gz' \
		.; \
	echo "Package created: system-specs-gui-$$DATE.tar.gz"

# Update dependencies
update:
	@echo "Updating dependencies..."
	@if [ -d "venv" ]; then \
		source venv/bin/activate && pip install --upgrade psutil; \
	else \
		echo "Virtual environment not found. Run 'make install' first."; \
	fi

# Show help
help:
	@echo "System Specifications GUI - Makefile Commands"
	@echo "=============================================="
	@echo ""
	@echo "Setup Commands:"
	@echo "  make install     - Install application and dependencies"
	@echo "  make setup       - Setup development environment"
	@echo "  make test        - Test installation"
	@echo "  make check       - Check system dependencies"
	@echo ""
	@echo "Run Commands:"
	@echo "  make run         - Launch application launcher"
	@echo "  make run-basic   - Run basic version directly"
	@echo "  make run-enhanced- Run enhanced version directly"
	@echo ""
	@echo "Maintenance Commands:"
	@echo "  make clean       - Clean temporary files"
	@echo "  make clean-all   - Remove everything including venv"
	@echo "  make update      - Update Python dependencies"
	@echo "  make deps        - Show installed Python packages"
	@echo ""
	@echo "Utility Commands:"
	@echo "  make info        - Show quick system information"
	@echo "  make desktop     - Install desktop entries"
	@echo "  make package     - Create distribution package"
	@echo "  make help        - Show this help message"
	@echo ""
	@echo "Quick Start:"
	@echo "  1. make install"
	@echo "  2. make run"
