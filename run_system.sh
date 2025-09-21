#!/bin/bash

# System Specifications GUI - Run Script (System Installation)
# This script runs the application using system Python (no virtual environment)

set -e  # Exit on any error

# Check if we're in the correct directory
if [ ! -f "launcher.py" ]; then
    echo "Error: launcher.py not found in current directory"
    echo "Please run this script from the application directory"
    exit 1
fi

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    echo "Please install Python 3: sudo apt install python3"
    exit 1
fi

# Check if psutil is available
if ! python3 -c "import psutil" 2>/dev/null; then
    echo "Error: psutil module not found"
    echo "Please install psutil: sudo apt install python3-psutil"
    echo "Or run the system installer: ./install_system.sh"
    exit 1
fi

echo "Starting System Specifications GUI Launcher..."
echo "Using system Python installation"

# Run the launcher
python3 launcher.py
