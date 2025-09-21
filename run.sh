#!/bin/bash

# System Specifications GUI - Run Script
# This script activates the virtual environment and runs the application launcher

set -e  # Exit on any error

# Check if we're in the correct directory
if [ ! -f "launcher.py" ]; then
    echo "Error: launcher.py not found in current directory"
    echo "Please run this script from the application directory"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Error: Virtual environment not found"
    echo "Please run ./install.sh first to set up the application"
    exit 1
fi

echo "Starting System Specifications GUI Launcher..."

# Activate virtual environment and run the launcher
source venv/bin/activate
python3 launcher.py
