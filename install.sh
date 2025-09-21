#!/bin/bash

# System Specifications GUI - Installation Script for Debian Linux
# This script installs the necessary dependencies and sets up the application

set -e  # Exit on any error

echo "=========================================="
echo "System Specifications GUI - Installer"
echo "Enhanced Version with Hardware Detection"
echo "=========================================="
echo

# Check if running on Debian/Ubuntu
if ! command -v apt &> /dev/null; then
    echo "Error: This installer is designed for Debian/Ubuntu systems with apt package manager."
    exit 1
fi

echo "Updating package list..."
sudo apt update

echo "Installing required system packages..."
sudo apt install -y python3 python3-pip python3-tk python3-venv

# Optional packages for enhanced functionality
echo "Installing optional packages for enhanced system information..."
sudo apt install -y lshw mesa-utils x11-utils lsb-release dmidecode smartmontools lm-sensors

echo "Creating virtual environment..."
python3 -m venv venv

echo "Activating virtual environment and installing Python dependencies..."
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo "Making applications executable..."
chmod +x system_specs_gui.py enhanced_system_specs.py launcher.py hardware_detector.py

echo "Creating desktop entries..."

# Basic version desktop entry
cat > system-specs-basic.desktop << 'EOF'
[Desktop Entry]
Version=1.0
Type=Application
Name=System Specifications (Basic)
Comment=View basic computer specifications
Exec=/bin/bash -c "cd $(dirname %k) && source venv/bin/activate && python3 system_specs_gui.py"
Icon=computer
Terminal=false
Categories=System;Utility;
EOF

# Enhanced version desktop entry
cat > system-specs-enhanced.desktop << 'EOF'
[Desktop Entry]
Version=1.0
Type=Application
Name=System Specifications (Enhanced)
Comment=View detailed computer specifications with advanced features
Exec=/bin/bash -c "cd $(dirname %k) && source venv/bin/activate && python3 enhanced_system_specs.py"
Icon=computer
Terminal=false
Categories=System;Utility;
EOF

# Launcher desktop entry
cat > system-specs-launcher.desktop << 'EOF'
[Desktop Entry]
Version=1.0
Type=Application
Name=System Specifications Launcher
Comment=Choose between basic and enhanced system specifications viewer
Exec=/bin/bash -c "cd $(dirname %k) && source venv/bin/activate && python3 launcher.py"
Icon=computer
Terminal=false
Categories=System;Utility;
EOF

# Optional: Install desktop entries to user's applications
if [ -d "$HOME/.local/share/applications" ]; then
    cp system-specs-basic.desktop "$HOME/.local/share/applications/"
    cp system-specs-enhanced.desktop "$HOME/.local/share/applications/"
    cp system-specs-launcher.desktop "$HOME/.local/share/applications/"
    echo "Desktop entries installed to $HOME/.local/share/applications/"
fi

echo
echo "=========================================="
echo "Installation completed successfully!"
echo "=========================================="
echo
echo "To run the applications:"
echo "1. Navigate to this directory: cd $(pwd)"
echo "2. Run launcher: python3 launcher.py (or ./run.sh for basic version)"
echo "3. Or run directly:"
echo "   - Basic version: python3 system_specs_gui.py"
echo "   - Enhanced version: python3 enhanced_system_specs.py"
echo
echo "If you installed desktop entries, you can find these applications"
echo "in your applications menu:"
echo "  • System Specifications Launcher"
echo "  • System Specifications (Basic)"
echo "  • System Specifications (Enhanced)"
echo
echo "Note: Enhanced version provides more detailed hardware information"
echo "but may require sudo privileges for some features."
echo
