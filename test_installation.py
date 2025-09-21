#!/usr/bin/env python3
"""
Test Installation Script
Verifies that all components are properly installed and working
"""

import sys
import os
import subprocess
import importlib

def check_python_version():
    """Check Python version compatibility"""
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 6:
        print(f"   ✅ Python {version.major}.{version.minor}.{version.micro} (Compatible)")
        return True
    else:
        print(f"   ❌ Python {version.major}.{version.minor}.{version.micro} (Requires 3.6+)")
        return False

def check_module(module_name, description=""):
    """Check if a Python module is available"""
    try:
        importlib.import_module(module_name)
        print(f"   ✅ {module_name} - {description}")
        return True
    except ImportError:
        print(f"   ❌ {module_name} - {description} (Missing)")
        return False

def check_file_exists(filepath, description=""):
    """Check if a file exists"""
    if os.path.exists(filepath):
        print(f"   ✅ {filepath} - {description}")
        return True
    else:
        print(f"   ❌ {filepath} - {description} (Missing)")
        return False

def check_command(command, description=""):
    """Check if a system command is available"""
    try:
        # First try with 'which'
        result = subprocess.run(['which', command],
                              capture_output=True,
                              text=True)
        if result.returncode == 0:
            print(f"   ✅ {command} - {description}")
            return True

        # If not found, check common system paths
        system_paths = ['/usr/bin/', '/usr/sbin/', '/bin/', '/sbin/']
        for path in system_paths:
            if os.path.exists(f"{path}{command}"):
                print(f"   ✅ {command} - {description} (found in {path})")
                return True

        print(f"   ❌ {command} - {description} (Not found)")
        return False
    except Exception:
        print(f"   ❌ {command} - {description} (Error checking)")
        return False

def test_basic_functionality():
    """Test basic functionality"""
    print("\n🧪 Testing basic functionality...")

    try:
        import psutil
        # Test psutil functions
        cpu_count = psutil.cpu_count()
        memory = psutil.virtual_memory()
        print(f"   ✅ psutil working (CPU: {cpu_count} cores, RAM: {memory.total // (1024**3)} GB)")
        return True
    except Exception as e:
        print(f"   ❌ psutil test failed: {e}")
        return False

def test_gui_components():
    """Test GUI components without creating windows"""
    print("\n🖼️  Testing GUI components...")

    try:
        import tkinter as tk
        from tkinter import ttk

        # Create a test root window (but don't show it)
        root = tk.Tk()
        root.withdraw()  # Hide the window

        # Test creating basic widgets
        frame = ttk.Frame(root)
        label = ttk.Label(frame, text="Test")
        button = ttk.Button(frame, text="Test")

        print("   ✅ tkinter widgets working")

        root.destroy()
        return True

    except Exception as e:
        print(f"   ❌ GUI test failed: {e}")
        return False

def main():
    """Main test function"""
    print("=" * 60)
    print("SYSTEM SPECIFICATIONS GUI - INSTALLATION TEST")
    print("=" * 60)
    print()

    all_checks_passed = True

    # Check Python version
    if not check_python_version():
        all_checks_passed = False

    # Check required Python modules
    print("\n📦 Checking Python modules...")
    required_modules = [
        ('tkinter', 'GUI framework'),
        ('psutil', 'System information library'),
        ('subprocess', 'System command execution'),
        ('threading', 'Multi-threading support'),
        ('platform', 'Platform information'),
        ('datetime', 'Date and time utilities'),
        ('json', 'JSON data handling'),
        ('os', 'Operating system interface')
    ]

    for module, description in required_modules:
        if not check_module(module, description):
            all_checks_passed = False

    # Check application files
    print("\n📁 Checking application files...")
    required_files = [
        ('system_specs_gui.py', 'Basic system specs GUI'),
        ('enhanced_system_specs.py', 'Enhanced system specs GUI'),
        ('hardware_detector.py', 'Hardware detection module'),
        ('launcher.py', 'Application launcher'),
        ('requirements.txt', 'Python dependencies'),
        ('install.sh', 'Installation script'),
        ('run.sh', 'Run script'),
        ('README.md', 'Documentation')
    ]

    for filename, description in required_files:
        if not check_file_exists(filename, description):
            all_checks_passed = False

    # Check optional system commands
    print("\n💻 Checking system commands...")
    system_commands = [
        ('lscpu', 'CPU information (required)'),
        ('lsblk', 'Block device information (required)'),
        ('lspci', 'PCI device information (required)'),
        ('lsusb', 'USB device information (required)'),
        ('ps', 'Process information (required)'),
        ('dmidecode', 'DMI/SMBIOS information (enhanced features)'),
        ('lshw', 'Hardware lister (enhanced features)'),
        ('sensors', 'Temperature sensors (optional)'),
        ('smartctl', 'SMART disk information (optional)'),
        ('glxinfo', 'OpenGL information (optional)'),
        ('iwconfig', 'Wireless configuration (optional)')
    ]

    required_commands = ['lscpu', 'lsblk', 'lspci', 'lsusb', 'ps']

    for command, description in system_commands:
        available = check_command(command, description)
        if command in required_commands and not available:
            all_checks_passed = False

    # Check virtual environment
    print("\n🔧 Checking virtual environment...")
    if check_file_exists('venv', 'Python virtual environment'):
        if check_file_exists('venv/bin/activate', 'Virtual environment activation script'):
            print("   ✅ Virtual environment properly configured")
        else:
            print("   ❌ Virtual environment activation script missing")
            all_checks_passed = False
    else:
        print("   ⚠️  Virtual environment not found (run install.sh)")

    # Test functionality
    if all_checks_passed:
        if not test_basic_functionality():
            all_checks_passed = False

        if not test_gui_components():
            all_checks_passed = False

    # Check file permissions
    print("\n🔐 Checking file permissions...")
    executable_files = ['system_specs_gui.py', 'enhanced_system_specs.py',
                       'launcher.py', 'hardware_detector.py', 'install.sh', 'run.sh']

    for filename in executable_files:
        if os.path.exists(filename):
            if os.access(filename, os.X_OK):
                print(f"   ✅ {filename} (executable)")
            else:
                print(f"   ⚠️  {filename} (not executable - run chmod +x {filename})")
        else:
            print(f"   ❌ {filename} (missing)")

    # Final results
    print("\n" + "=" * 60)
    print("TEST RESULTS")
    print("=" * 60)

    if all_checks_passed:
        print("🎉 ALL TESTS PASSED!")
        print()
        print("Your installation is complete and ready to use!")
        print()
        print("To run the application:")
        print("  • Use launcher: python3 launcher.py")
        print("  • Or run script: ./run.sh")
        print("  • Basic version: python3 system_specs_gui.py")
        print("  • Enhanced version: python3 enhanced_system_specs.py")
        print()
        print("Note: Some enhanced features may require sudo privileges.")

    else:
        print("❌ SOME TESTS FAILED!")
        print()
        print("Issues found. Please check the errors above and:")
        print("  1. Run ./install.sh to install missing dependencies")
        print("  2. Ensure you're on a Linux Debian/Ubuntu system")
        print("  3. Check that Python 3.6+ is installed")
        print("  4. Verify internet connection for package installation")
        print()
        print("The basic version may still work with partial dependencies.")

    print("\n" + "=" * 60)

    return all_checks_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
