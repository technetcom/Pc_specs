# Quick Start Guide

## System Specifications GUI - Quick Setup

This guide will get you up and running with the System Specifications GUI in just a few minutes.

## Prerequisites

- Linux Debian/Ubuntu system
- Internet connection
- Terminal access

## 1-Minute Setup

### Step 1: Download and Navigate
```bash
# If you haven't already, navigate to the project directory
cd rastland
```

### Step 2: Install Everything
```bash
# Make the installer executable and run it
chmod +x install.sh
./install.sh
```

### Step 3: Launch the Application
```bash
# Run the launcher to choose your version
./run.sh
```

That's it! The application should now be running.

## Quick Commands

| Action | Command |
|--------|---------|
| Run launcher | `./run.sh` or `python3 launcher.py` |
| Basic version | `python3 system_specs_gui.py` |
| Enhanced version | `python3 enhanced_system_specs.py` |
| Test installation | `python3 test_installation.py` |
| Reinstall | `./install.sh` |

## Troubleshooting (30 seconds)

### If installation fails:
```bash
# Update your system first
sudo apt update
sudo apt upgrade

# Then try installation again
./install.sh
```

### If GUI won't start:
```bash
# Test your installation
python3 test_installation.py

# Check if psutil is installed
python3 -c "import psutil; print('psutil working')"
```

### If you get permission errors:
```bash
# Some features need elevated privileges
# The app will still work, just with limited hardware info
```

## What Each Version Does

### 🔹 Basic Version
- Quick system overview
- CPU, memory, storage basics
- Network information
- Running processes
- **Perfect for**: Quick system checks

### 🔹 Enhanced Version  
- Everything from basic version
- Deep hardware detection
- Motherboard and BIOS info
- Temperature sensors
- Security information
- Export reports
- **Perfect for**: Detailed system analysis

## First Time Usage

1. **Launch the application** using `./run.sh`
2. **Choose your version** in the launcher
3. **Click "Refresh All Data"** to load current information
4. **Navigate tabs** to explore different system components
5. **Export reports** if needed (Enhanced version)

## Desktop Integration

After installation, you can find these applications in your system menu:
- "System Specifications Launcher"
- "System Specifications (Basic)"
- "System Specifications (Enhanced)"

## Need Help?

- Check `README.md` for detailed documentation
- Run `python3 test_installation.py` to diagnose issues
- All applications include built-in help and about dialogs

---

**Tip**: Start with the launcher to easily choose between versions based on your needs!