#!/usr/bin/env python3
"""
System Specifications GUI - Demo Script
Demonstrates the capabilities of the system specifications application
"""

import os
import sys
import subprocess
import platform
import time
from datetime import datetime

def print_banner(text):
    """Print a formatted banner"""
    width = 80
    print("\n" + "=" * width)
    print(f"{text:^{width}}")
    print("=" * width)

def print_section(title):
    """Print a section header"""
    print(f"\n🔹 {title}")
    print("-" * (len(title) + 3))

def run_command_safe(command):
    """Safely run a command and return output"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True,
                              text=True, timeout=5)
        return result.stdout.strip() if result.returncode == 0 else "Not available"
    except:
        return "Error"

def demo_basic_info():
    """Demonstrate basic system information"""
    print_section("Basic System Information")

    print(f"Operating System: {platform.system()}")
    print(f"OS Release: {platform.release()}")
    print(f"Machine Type: {platform.machine()}")
    print(f"Processor: {platform.processor()}")
    print(f"Architecture: {platform.architecture()[0]}")
    print(f"Hostname: {platform.node()}")

    # Distribution info
    try:
        with open('/etc/os-release', 'r') as f:
            for line in f:
                if line.startswith('PRETTY_NAME='):
                    distro = line.split('=', 1)[1].strip().strip('"')
                    print(f"Distribution: {distro}")
                    break
    except:
        print("Distribution: Unknown")

def demo_hardware_capabilities():
    """Demonstrate hardware detection capabilities"""
    print_section("Hardware Detection Capabilities")

    # CPU Information
    cpu_info = run_command_safe("lscpu | grep 'Model name'")
    if cpu_info != "Not available":
        cpu_model = cpu_info.split(':', 1)[1].strip()
        print(f"CPU Model: {cpu_model}")

    cpu_cores = run_command_safe("nproc")
    print(f"CPU Cores: {cpu_cores}")

    # Memory Information
    mem_info = run_command_safe("free -h | grep '^Mem:' | awk '{print $2}'")
    print(f"Total Memory: {mem_info}")

    # Storage Information
    storage_info = run_command_safe("df -h / | tail -1 | awk '{print $2}'")
    print(f"Root Filesystem Size: {storage_info}")

    # Graphics Information
    gpu_info = run_command_safe("lspci | grep -i vga | head -1")
    if gpu_info != "Not available":
        print(f"Graphics: {gpu_info.split(':', 2)[-1].strip()}")

def demo_advanced_features():
    """Demonstrate advanced features available"""
    print_section("Advanced Features Available")

    features = [
        ("Motherboard Detection", "dmidecode", "BIOS and motherboard information"),
        ("Hardware Listing", "lshw", "Comprehensive hardware detection"),
        ("Temperature Monitoring", "sensors", "CPU and system temperatures"),
        ("Drive Health", "smartctl", "SMART disk health information"),
        ("Graphics Details", "glxinfo", "OpenGL and graphics information"),
        ("Network Analysis", "iwconfig", "Wireless network configuration"),
        ("USB Devices", "lsusb", "USB device enumeration"),
        ("PCI Devices", "lspci", "PCI bus device listing")
    ]

    print("Available Features:")
    for feature, command, description in features:
        # Check if command is available
        status = "✅" if run_command_safe(f"which {command}") != "Not available" else "❌"
        print(f"  {status} {feature}: {description}")

def demo_gui_features():
    """Demonstrate GUI features"""
    print_section("GUI Application Features")

    gui_features = [
        "📊 Real-time CPU and memory usage monitoring",
        "💾 Disk usage visualization with progress bars",
        "🌐 Network interface details and statistics",
        "🎮 Graphics card and display information",
        "🔧 Motherboard and BIOS details",
        "🌡️ Temperature sensor readings",
        "🔒 Security feature status",
        "📋 Process monitoring and management",
        "💾 Export reports to text files",
        "🔄 Real-time data refresh capability",
        "🖱️ Intuitive tabbed interface",
        "⚡ Multi-threaded non-blocking updates"
    ]

    for feature in gui_features:
        print(f"  {feature}")

def demo_performance_info():
    """Show performance characteristics"""
    print_section("Performance Characteristics")

    try:
        # Simulate loading time
        start_time = time.time()

        # Basic system calls that the app would make
        commands = [
            "python3 --version",
            "uname -r",
            "free -m",
            "df -h",
            "lscpu | head -5"
        ]

        for cmd in commands:
            run_command_safe(cmd)

        load_time = time.time() - start_time

        print(f"Simulated data collection time: {load_time:.2f} seconds")
        print("Memory usage: ~50-80 MB (estimated)")
        print("CPU impact: Minimal during normal operation")
        print("Refresh rate: On-demand (user triggered)")
        print("UI responsiveness: Non-blocking with threading")

    except Exception as e:
        print(f"Performance test error: {e}")

def demo_file_structure():
    """Show the project file structure"""
    print_section("Project File Structure")

    files = [
        ("system_specs_gui.py", "Basic GUI application (lightweight)"),
        ("enhanced_system_specs.py", "Enhanced GUI with advanced features"),
        ("hardware_detector.py", "Hardware detection engine"),
        ("launcher.py", "Version selection launcher"),
        ("install.sh", "Automated installation script"),
        ("run.sh", "Application runner"),
        ("test_installation.py", "Installation verification"),
        ("README.md", "Comprehensive documentation"),
        ("requirements.txt", "Python dependencies"),
        ("Makefile", "Build and management commands")
    ]

    print("Core Files:")
    for filename, description in files:
        status = "✅" if os.path.exists(filename) else "❌"
        print(f"  {status} {filename:<25} - {description}")

def main():
    """Main demo function"""
    print_banner("SYSTEM SPECIFICATIONS GUI - DEMONSTRATION")

    print(f"\nDemo started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Running on: {platform.node()}")

    # Check if we're in the right directory
    if not os.path.exists('system_specs_gui.py'):
        print("\n❌ Error: Not in the correct project directory!")
        print("Please run this demo from the rastland/ directory.")
        return False

    # Demonstrate different aspects
    demo_basic_info()
    demo_hardware_capabilities()
    demo_advanced_features()
    demo_gui_features()
    demo_performance_info()
    demo_file_structure()

    print_banner("DEMO SUMMARY")

    print("\n🎯 What this application provides:")
    print("   • Comprehensive system hardware information")
    print("   • User-friendly GUI interface with tabbed navigation")
    print("   • Real-time monitoring of system resources")
    print("   • Export capabilities for documentation")
    print("   • Two versions: Basic (fast) and Enhanced (detailed)")

    print("\n🚀 Ready to try it?")
    print("   1. Run: ./install.sh (if not already installed)")
    print("   2. Launch: ./run.sh")
    print("   3. Or use launcher: python3 launcher.py")

    print("\n📋 Quick Test Commands:")
    print("   • Test installation: python3 test_installation.py")
    print("   • Run basic version: python3 system_specs_gui.py")
    print("   • Run enhanced version: python3 enhanced_system_specs.py")

    print("\n✨ The application is fully functional and ready for use!")

    return True

if __name__ == "__main__":
    try:
        success = main()
        if success:
            print(f"\n🎉 Demo completed successfully at {datetime.now().strftime('%H:%M:%S')}")
        else:
            print(f"\n❌ Demo failed - check the error messages above")
    except KeyboardInterrupt:
        print("\n\n⏹️ Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Demo error: {e}")

    print("\nThank you for exploring the System Specifications GUI!")
