#!/usr/bin/env python3
"""
System Specifications GUI Launcher
Choose between basic and enhanced versions of the system specs application
"""

import tkinter as tk
from tkinter import ttk, messagebox
import os
import sys
import subprocess

class SpecsLauncher:
    def __init__(self, root):
        self.root = root
        self.root.title("System Specs Launcher")
        self.root.geometry("500x400")
        self.root.configure(bg='#f0f0f0')
        self.root.resizable(False, False)

        # Center the window
        self.center_window()

        # Create main frame
        main_frame = ttk.Frame(root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Title
        title_label = ttk.Label(main_frame,
                               text="System Specifications GUI",
                               font=('Arial', 16, 'bold'))
        title_label.pack(pady=(0, 10))

        subtitle_label = ttk.Label(main_frame,
                                  text="Choose your preferred version",
                                  font=('Arial', 11))
        subtitle_label.pack(pady=(0, 20))

        # Version selection frame
        version_frame = ttk.LabelFrame(main_frame, text="Available Versions", padding="15")
        version_frame.pack(fill=tk.X, pady=(0, 20))

        # Basic version
        basic_frame = ttk.Frame(version_frame)
        basic_frame.pack(fill=tk.X, pady=(0, 15))

        ttk.Label(basic_frame, text="📊 Basic Version",
                 font=('Arial', 12, 'bold')).pack(anchor=tk.W)
        ttk.Label(basic_frame,
                 text="• Fast and lightweight\n• Essential system information\n• CPU, Memory, Storage, Network basics\n• Ideal for quick system overview",
                 justify=tk.LEFT).pack(anchor=tk.W, pady=(5, 0))

        basic_btn = ttk.Button(basic_frame, text="Launch Basic Version",
                              command=self.launch_basic,
                              style='Action.TButton')
        basic_btn.pack(pady=(10, 0))

        # Enhanced version
        enhanced_frame = ttk.Frame(version_frame)
        enhanced_frame.pack(fill=tk.X)

        ttk.Label(enhanced_frame, text="🚀 Enhanced Version",
                 font=('Arial', 12, 'bold')).pack(anchor=tk.W)
        ttk.Label(enhanced_frame,
                 text="• Comprehensive hardware detection\n• Advanced system analysis\n• Export and reporting features\n• Deep hardware scanning\n• Security and firmware information",
                 justify=tk.LEFT).pack(anchor=tk.W, pady=(5, 0))

        enhanced_btn = ttk.Button(enhanced_frame, text="Launch Enhanced Version",
                                 command=self.launch_enhanced,
                                 style='Action.TButton')
        enhanced_btn.pack(pady=(10, 0))

        # System requirements
        req_frame = ttk.LabelFrame(main_frame, text="System Requirements", padding="15")
        req_frame.pack(fill=tk.X, pady=(0, 20))

        requirements_text = """✅ Linux Debian/Ubuntu system
✅ Python 3.6+ with tkinter
✅ psutil package installed
⚠️  Enhanced version requires additional system tools (dmidecode, lshw, etc.)
⚠️  Some features may require sudo privileges"""

        ttk.Label(req_frame, text=requirements_text, justify=tk.LEFT).pack(anchor=tk.W)

        # Control buttons
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(fill=tk.X)

        # Check dependencies button
        check_btn = ttk.Button(control_frame, text="Check Dependencies",
                              command=self.check_dependencies)
        check_btn.pack(side=tk.LEFT)

        # About button
        about_btn = ttk.Button(control_frame, text="About",
                              command=self.show_about)
        about_btn.pack(side=tk.LEFT, padx=(10, 0))

        # Exit button
        exit_btn = ttk.Button(control_frame, text="Exit",
                             command=self.root.quit)
        exit_btn.pack(side=tk.RIGHT)

        # Configure styles
        style = ttk.Style()
        style.configure('Action.TButton', font=('Arial', 10, 'bold'))



    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def check_command_exists(self, command):
        """Check if a command exists in system PATH"""
        try:
            subprocess.run(['which', command],
                          capture_output=True,
                          check=True)
            return True
        except subprocess.CalledProcessError:
            return False

    def check_python_module(self, module_name):
        """Check if a Python module is available"""
        try:
            __import__(module_name)
            return True
        except ImportError:
            return False

    def check_dependencies(self):
        """Check system dependencies and show status"""
        deps_window = tk.Toplevel(self.root)
        deps_window.title("Dependency Check")
        deps_window.geometry("600x500")
        deps_window.resizable(False, False)

        # Create scrolled text for results
        text_frame = ttk.Frame(deps_window, padding="15")
        text_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(text_frame, text="Dependency Check Results",
                 font=('Arial', 14, 'bold')).pack(pady=(0, 10))

        deps_text = scrolledtext.ScrolledText(text_frame, wrap=tk.WORD,
                                            width=70, height=25,
                                            font=('Consolas', 10))
        deps_text.pack(fill=tk.BOTH, expand=True)

        # Check dependencies
        results = []
        results.append("=" * 50)
        results.append("DEPENDENCY CHECK RESULTS")
        results.append("=" * 50)
        results.append("")

        # Python modules
        results.append("🐍 PYTHON MODULES")
        results.append("-" * 30)
        python_modules = {
            'tkinter': 'GUI framework (required)',
            'psutil': 'System information (required)',
            'subprocess': 'System commands (built-in)',
            'threading': 'Multi-threading (built-in)',
            'platform': 'Platform information (built-in)'
        }

        for module, description in python_modules.items():
            status = "✅ Available" if self.check_python_module(module) else "❌ Missing"
            results.append(f"{module:<15} {status:<15} - {description}")

        results.append("")

        # System commands
        results.append("💻 SYSTEM COMMANDS")
        results.append("-" * 30)
        system_commands = {
            'lscpu': 'CPU information (usually available)',
            'lsblk': 'Block device information (usually available)',
            'lspci': 'PCI device information (usually available)',
            'lsusb': 'USB device information (usually available)',
            'dmidecode': 'Hardware information (enhanced version)',
            'lshw': 'Hardware lister (enhanced version)',
            'sensors': 'Temperature sensors (optional)',
            'smartctl': 'SMART disk info (optional)',
            'glxinfo': 'OpenGL information (optional)',
            'iwconfig': 'Wireless configuration (optional)'
        }

        for command, description in system_commands.items():
            status = "✅ Available" if self.check_command_exists(command) else "❌ Missing"
            results.append(f"{command:<15} {status:<15} - {description}")

        results.append("")

        # File access
        results.append("📁 SYSTEM FILES ACCESS")
        results.append("-" * 30)
        system_files = {
            '/proc/cpuinfo': 'CPU information',
            '/proc/meminfo': 'Memory information',
            '/proc/version': 'Kernel version',
            '/etc/os-release': 'OS release information',
            '/sys/class/thermal': 'Temperature sensors',
            '/sys/devices/system/cpu': 'CPU configuration'
        }

        for filepath, description in system_files.items():
            status = "✅ Accessible" if os.path.exists(filepath) else "❌ Missing"
            results.append(f"{os.path.basename(filepath):<15} {status:<15} - {description}")

        results.append("")
        results.append("📋 RECOMMENDATIONS")
        results.append("-" * 30)

        # Provide recommendations
        if not self.check_python_module('psutil'):
            results.append("❗ Install psutil: pip install psutil")

        if not self.check_command_exists('dmidecode'):
            results.append("💡 For enhanced features: sudo apt install dmidecode")

        if not self.check_command_exists('lshw'):
            results.append("💡 For hardware detection: sudo apt install lshw")

        if not self.check_command_exists('sensors'):
            results.append("💡 For temperature monitoring: sudo apt install lm-sensors")

        results.append("")
        results.append("✨ Both versions will work with basic dependencies!")
        results.append("Enhanced version provides more features with additional tools.")

        # Display results
        deps_text.insert(tk.END, "\n".join(results))

        # Close button
        close_btn = ttk.Button(text_frame, text="Close",
                              command=deps_window.destroy)
        close_btn.pack(pady=(10, 0))

    def launch_basic(self):
        """Launch the basic version"""
        if not os.path.exists('system_specs_gui.py'):
            messagebox.showerror("Error", "system_specs_gui.py not found!")
            return

        if not self.check_python_module('psutil'):
            messagebox.showerror("Error",
                               "psutil module is required!\n\nInstall with: pip install psutil")
            return

        try:
            # Launch basic version
            subprocess.Popen([sys.executable, 'system_specs_gui.py'])
            self.root.quit()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to launch basic version:\n{str(e)}")

    def launch_enhanced(self):
        """Launch the enhanced version"""
        if not os.path.exists('enhanced_system_specs.py'):
            messagebox.showerror("Error", "enhanced_system_specs.py not found!")
            return

        if not os.path.exists('hardware_detector.py'):
            messagebox.showerror("Error", "hardware_detector.py not found!")
            return

        if not self.check_python_module('psutil'):
            messagebox.showerror("Error",
                               "psutil module is required!\n\nInstall with: pip install psutil")
            return

        try:
            # Launch enhanced version
            subprocess.Popen([sys.executable, 'enhanced_system_specs.py'])
            self.root.quit()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to launch enhanced version:\n{str(e)}")

    def show_about(self):
        """Show about information"""
        about_text = """System Specifications GUI Launcher

This launcher helps you choose between two versions of the system specifications application:

🔸 Basic Version:
   • Lightweight and fast
   • Shows essential system information
   • Minimal dependencies required
   • Perfect for quick system overview

🔸 Enhanced Version:
   • Comprehensive hardware detection
   • Advanced system analysis
   • Export and reporting capabilities
   • Deep hardware scanning
   • Security and firmware information

Both versions are designed for Linux Debian/Ubuntu systems and provide detailed information about your computer's hardware and software configuration.

Requirements:
• Python 3.6+
• tkinter (usually pre-installed)
• psutil (install with: pip install psutil)

For the enhanced version, additional system tools like dmidecode, lshw, and sensors provide more detailed information.

Version: 1.0
Platform: Linux Debian
Created with Python and Tkinter"""

        # Create about window
        about_window = tk.Toplevel(self.root)
        about_window.title("About System Specs Launcher")
        about_window.geometry("550x600")
        about_window.resizable(False, False)

        # Center the about window
        about_window.update_idletasks()
        x = (about_window.winfo_screenwidth() // 2) - (550 // 2)
        y = (about_window.winfo_screenheight() // 2) - (600 // 2)
        about_window.geometry(f'550x600+{x}+{y}')

        # Create text widget
        text_frame = ttk.Frame(about_window, padding="15")
        text_frame.pack(fill=tk.BOTH, expand=True)

        about_text_widget = tk.Text(text_frame, wrap=tk.WORD, width=60, height=30,
                                   font=('Arial', 10), relief=tk.FLAT,
                                   bg='#f9f9f9', state=tk.DISABLED)
        about_text_widget.pack(fill=tk.BOTH, expand=True)

        # Insert text
        about_text_widget.config(state=tk.NORMAL)
        about_text_widget.insert(tk.END, about_text)
        about_text_widget.config(state=tk.DISABLED)

        # Close button
        close_btn = ttk.Button(text_frame, text="Close",
                              command=about_window.destroy)
        close_btn.pack(pady=(10, 0))

def main():
    """Main function"""
    try:
        root = tk.Tk()
        app = SpecsLauncher(root)
        root.mainloop()
    except Exception as e:
        print(f"Error starting launcher: {e}")

if __name__ == "__main__":
    main()
