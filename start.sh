#!/bin/bash

# System Specifications GUI - Simple Startup Script
# This script provides a quick way to launch the application with user-friendly prompts

set -e

clear

echo "╔══════════════════════════════════════════════════════════════════════════════╗"
echo "║                    System Specifications GUI for Linux                      ║"
echo "║                          Welcome to the Launcher!                           ║"
echo "╚══════════════════════════════════════════════════════════════════════════════╝"
echo

# Check if we're in the correct directory
if [ ! -f "launcher.py" ]; then
    echo "❌ Error: Application files not found in current directory"
    echo "   Please navigate to the rastland/ directory first"
    echo
    echo "   Example: cd /path/to/rastland"
    exit 1
fi

echo "🖥️  System Information:"
echo "   OS: $(lsb_release -d 2>/dev/null | cut -f2 || uname -o)"
echo "   Kernel: $(uname -r)"
echo "   Architecture: $(uname -m)"
echo "   User: $(whoami)"
echo

# Check installation status
if [ ! -d "venv" ]; then
    echo "⚠️  Virtual environment not found. Setting up..."
    echo
    echo "Would you like to install the application now? (y/n)"
    read -r response

    if [[ "$response" =~ ^[Yy]$ ]]; then
        echo "🔧 Running installation..."
        ./install.sh
    else
        echo "Installation cancelled. Please run './install.sh' manually."
        exit 1
    fi
fi

echo "🚀 Choose how to launch the application:"
echo
echo "   1) 🎯 Launcher (Choose between Basic/Enhanced versions)"
echo "   2) ⚡ Basic Version (Fast, essential information)"
echo "   3) 🔍 Enhanced Version (Detailed hardware analysis)"
echo "   4) 🧪 Test Installation"
echo "   5) 📖 View Quick Start Guide"
echo "   6) ❌ Exit"
echo

while true; do
    echo -n "Enter your choice (1-6): "
    read -r choice

    case $choice in
        1)
            echo
            echo "🎯 Starting Application Launcher..."
            source venv/bin/activate && python3 launcher.py
            break
            ;;
        2)
            echo
            echo "⚡ Starting Basic System Specifications..."
            source venv/bin/activate && python3 system_specs_gui.py
            break
            ;;
        3)
            echo
            echo "🔍 Starting Enhanced System Specifications..."
            echo "   (This version provides detailed hardware information)"
            source venv/bin/activate && python3 enhanced_system_specs.py
            break
            ;;
        4)
            echo
            echo "🧪 Testing Installation..."
            source venv/bin/activate && python3 test_installation.py
            echo
            echo "Press Enter to continue..."
            read -r
            ;;
        5)
            echo
            echo "📖 Quick Start Guide:"
            echo "════════════════════"
            echo
            echo "Basic Usage:"
            echo "  • Run './start.sh' for this menu"
            echo "  • Run './run.sh' for quick launcher access"
            echo "  • Use tabs to navigate different hardware categories"
            echo "  • Click 'Refresh All Data' to update information"
            echo
            echo "Two Versions Available:"
            echo "  • Basic: Fast overview of essential system information"
            echo "  • Enhanced: Comprehensive hardware analysis with export features"
            echo
            echo "Export Features (Enhanced version):"
            echo "  • Save complete system reports"
            echo "  • Export in text or JSON format"
            echo "  • Deep hardware scanning capabilities"
            echo
            echo "Tips:"
            echo "  • Some enhanced features require sudo privileges"
            echo "  • All information is read-only and safe"
            echo "  • Application works offline with no network required"
            echo
            echo "Press Enter to continue..."
            read -r
            ;;
        6)
            echo
            echo "👋 Thank you for using System Specifications GUI!"
            echo "   Run this script anytime with: ./start.sh"
            exit 0
            ;;
        *)
            echo "❌ Invalid choice. Please enter 1-6."
            ;;
    esac
done

echo
echo "🎉 Application launched successfully!"
echo "   You can run this startup script anytime with: ./start.sh"
echo
