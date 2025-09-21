#!/usr/bin/env python3
"""
Enhanced System Specifications GUI Application for Linux Debian
A comprehensive GUI tool with advanced hardware detection capabilities
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import subprocess
import os
import platform
import psutil
import json
import threading
from datetime import datetime
from hardware_detector import HardwareDetector

class EnhancedSystemSpecsGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Enhanced System Specifications - Linux Debian")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f0f0')

        # Initialize hardware detector
        self.hw_detector = HardwareDetector()

        # Style configuration
        self.setup_styles()

        # Create main frame
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure grid weights
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)

        # Create header frame
        self.create_header(main_frame)

        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Create tabs
        self.create_overview_tab()
        self.create_motherboard_tab()
        self.create_cpu_tab()
        self.create_memory_tab()
        self.create_storage_tab()
        self.create_graphics_tab()
        self.create_network_tab()
        self.create_audio_tab()
        self.create_usb_pci_tab()
        self.create_sensors_tab()
        self.create_processes_tab()
        self.create_security_tab()

        # Create control frame
        self.create_control_frame(main_frame)

        # Status bar
        self.create_status_bar(main_frame)

        # Load initial data
        self.refresh_all_data()

    def setup_styles(self):
        """Setup custom styles for the application"""
        style = ttk.Style()

        # Configure notebook style
        style.configure('Custom.TNotebook', tabposition='n')
        style.configure('Custom.TNotebook.Tab', padding=[20, 10])

        # Configure button styles
        style.configure('Action.TButton', font=('Arial', 10, 'bold'))

    def create_header(self, parent):
        """Create application header with title and system overview"""
        header_frame = ttk.Frame(parent)
        header_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        header_frame.columnconfigure(0, weight=1)

        # Title
        title_label = ttk.Label(header_frame,
                               text="Enhanced System Specifications",
                               font=('Arial', 18, 'bold'))
        title_label.grid(row=0, column=0, pady=(0, 5))

        # Quick system info
        self.quick_info_label = ttk.Label(header_frame,
                                         text="Loading system information...",
                                         font=('Arial', 10))
        self.quick_info_label.grid(row=1, column=0)

    def create_control_frame(self, parent):
        """Create control buttons frame"""
        control_frame = ttk.Frame(parent)
        control_frame.grid(row=2, column=0, pady=(10, 5), sticky=(tk.W, tk.E))

        # Refresh button
        refresh_btn = ttk.Button(control_frame, text="🔄 Refresh All Data",
                               command=self.refresh_all_data,
                               style='Action.TButton')
        refresh_btn.pack(side=tk.LEFT, padx=(0, 10))

        # Export button
        export_btn = ttk.Button(control_frame, text="💾 Export Report",
                              command=self.export_report)
        export_btn.pack(side=tk.LEFT, padx=(0, 10))

        # Hardware scan button
        hw_scan_btn = ttk.Button(control_frame, text="🔍 Deep Hardware Scan",
                               command=self.deep_hardware_scan)
        hw_scan_btn.pack(side=tk.LEFT, padx=(0, 10))

        # About button
        about_btn = ttk.Button(control_frame, text="ℹ️ About",
                             command=self.show_about)
        about_btn.pack(side=tk.RIGHT)

    def create_status_bar(self, parent):
        """Create status bar"""
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")

        status_bar = ttk.Label(parent, textvariable=self.status_var,
                              relief=tk.SUNKEN, anchor=tk.W,
                              font=('Arial', 9))
        status_bar.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(5, 0))

    def update_status(self, message):
        """Update status bar message"""
        self.status_var.set(f"{datetime.now().strftime('%H:%M:%S')} - {message}")
        self.root.update_idletasks()

    def create_text_tab(self, tab_name, text_attr_name):
        """Helper method to create a text tab"""
        frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(frame, text=tab_name)

        text_widget = scrolledtext.ScrolledText(frame, wrap=tk.WORD,
                                              width=100, height=35,
                                              font=('Consolas', 10))
        text_widget.pack(fill=tk.BOTH, expand=True)

        setattr(self, text_attr_name, text_widget)
        return frame

    def create_overview_tab(self):
        """Create system overview tab"""
        self.create_text_tab("🏠 Overview", "overview_text")

    def create_motherboard_tab(self):
        """Create motherboard information tab"""
        self.create_text_tab("🔧 Motherboard", "motherboard_text")

    def create_cpu_tab(self):
        """Create CPU information tab"""
        self.create_text_tab("⚡ CPU", "cpu_text")

    def create_memory_tab(self):
        """Create memory information tab"""
        self.create_text_tab("🧠 Memory", "memory_text")

    def create_storage_tab(self):
        """Create storage information tab"""
        self.create_text_tab("💾 Storage", "storage_text")

    def create_graphics_tab(self):
        """Create graphics information tab"""
        self.create_text_tab("🎮 Graphics", "graphics_text")

    def create_network_tab(self):
        """Create network information tab"""
        self.create_text_tab("🌐 Network", "network_text")

    def create_audio_tab(self):
        """Create audio information tab"""
        self.create_text_tab("🔊 Audio", "audio_text")

    def create_usb_pci_tab(self):
        """Create USB/PCI devices tab"""
        self.create_text_tab("🔌 USB/PCI", "usb_pci_text")

    def create_sensors_tab(self):
        """Create sensors information tab"""
        self.create_text_tab("🌡️ Sensors", "sensors_text")

    def create_processes_tab(self):
        """Create processes information tab"""
        self.create_text_tab("📊 Processes", "processes_text")

    def create_security_tab(self):
        """Create security information tab"""
        self.create_text_tab("🔒 Security", "security_text")

    def run_command(self, command):
        """Run a system command and return output"""
        try:
            result = subprocess.run(command, shell=True, capture_output=True,
                                  text=True, timeout=15)
            return result.stdout.strip() if result.returncode == 0 else f"Command failed: {command}"
        except subprocess.TimeoutExpired:
            return f"Command timed out: {command}"
        except Exception as e:
            return f"Error running command '{command}': {str(e)}"

    def bytes_to_gb(self, bytes_value):
        """Convert bytes to gigabytes"""
        return bytes_value / (1024**3)

    def bytes_to_mb(self, bytes_value):
        """Convert bytes to megabytes"""
        return bytes_value / (1024**2)

    def get_overview_info(self):
        """Get system overview information"""
        info = []
        info.append("=" * 60)
        info.append("SYSTEM OVERVIEW")
        info.append("=" * 60)
        info.append(f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        info.append("")

        # Basic system info
        info.append("🖥️  BASIC SYSTEM INFORMATION")
        info.append("-" * 40)
        info.append(f"Operating System: {platform.system()}")
        info.append(f"OS Release: {platform.release()}")
        info.append(f"Machine Type: {platform.machine()}")
        info.append(f"Processor: {platform.processor()}")
        info.append(f"Architecture: {platform.architecture()[0]}")
        info.append(f"Hostname: {platform.node()}")
        info.append("")

        # Quick hardware summary
        try:
            info.append("⚡ QUICK HARDWARE SUMMARY")
            info.append("-" * 40)

            # CPU
            cpu_count = psutil.cpu_count(logical=False)
            cpu_count_logical = psutil.cpu_count(logical=True)
            info.append(f"CPU Cores: {cpu_count} physical, {cpu_count_logical} logical")

            # Memory
            vmem = psutil.virtual_memory()
            info.append(f"Total Memory: {self.bytes_to_gb(vmem.total):.1f} GB")
            info.append(f"Available Memory: {self.bytes_to_gb(vmem.available):.1f} GB ({100-vmem.percent:.1f}% free)")

            # Storage
            disk_usage = psutil.disk_usage('/')
            info.append(f"Root Disk: {self.bytes_to_gb(disk_usage.total):.1f} GB total, {self.bytes_to_gb(disk_usage.free):.1f} GB free")

            # Boot time
            boot_time = datetime.fromtimestamp(psutil.boot_time())
            uptime = datetime.now() - boot_time
            info.append(f"System Uptime: {str(uptime).split('.')[0]}")

        except Exception as e:
            info.append(f"Error getting hardware summary: {e}")

        info.append("")

        # Distribution information
        try:
            info.append("🐧 DISTRIBUTION INFORMATION")
            info.append("-" * 40)
            with open('/etc/os-release', 'r') as f:
                for line in f:
                    if '=' in line and line.strip():
                        key, value = line.strip().split('=', 1)
                        if key in ['NAME', 'VERSION', 'ID', 'VERSION_ID', 'PRETTY_NAME']:
                            info.append(f"{key}: {value.strip('\"')}")
        except Exception:
            info.append("Distribution information not available")

        return "\n".join(info)

    def get_motherboard_info(self):
        """Get motherboard information"""
        info = []
        info.append("=" * 60)
        info.append("MOTHERBOARD & SYSTEM INFORMATION")
        info.append("=" * 60)
        info.append("")

        # Get motherboard info from hardware detector
        mb_data = self.hw_detector.get_motherboard_info()

        info.append("🔧 MOTHERBOARD DETAILS")
        info.append("-" * 40)
        for key, value in mb_data.items():
            info.append(f"{key}: {value}")

        info.append("")

        # Firmware information
        firmware_data = self.hw_detector.get_firmware_info()

        info.append("💾 FIRMWARE INFORMATION")
        info.append("-" * 40)
        for key, value in firmware_data.items():
            if isinstance(value, dict):
                info.append(f"{key}:")
                for subkey, subvalue in value.items():
                    info.append(f"  {subkey}: {subvalue}")
            else:
                info.append(f"{key}: {value}")

        return "\n".join(info)

    def get_enhanced_cpu_info(self):
        """Get enhanced CPU information"""
        info = []
        info.append("=" * 60)
        info.append("CPU INFORMATION")
        info.append("=" * 60)
        info.append("")

        # Basic CPU metrics
        try:
            cpu_count = psutil.cpu_count(logical=False)
            cpu_count_logical = psutil.cpu_count(logical=True)
            cpu_freq = psutil.cpu_freq()

            info.append("⚡ CPU SPECIFICATIONS")
            info.append("-" * 40)
            info.append(f"Physical Cores: {cpu_count}")
            info.append(f"Logical Cores: {cpu_count_logical}")

            if cpu_freq:
                info.append(f"Current Frequency: {cpu_freq.current:.2f} MHz")
                info.append(f"Min Frequency: {cpu_freq.min:.2f} MHz")
                info.append(f"Max Frequency: {cpu_freq.max:.2f} MHz")

            info.append("")

            # CPU usage
            info.append("📊 CPU USAGE")
            info.append("-" * 40)
            cpu_percent = psutil.cpu_percent(interval=1, percpu=True)
            overall_usage = psutil.cpu_percent(interval=1)

            info.append(f"Overall CPU Usage: {overall_usage}%")
            info.append("")
            info.append("Per-Core Usage:")

            # Display cores in rows of 4
            for i in range(0, len(cpu_percent), 4):
                row_cores = cpu_percent[i:i+4]
                core_info = "  "
                for j, percent in enumerate(row_cores):
                    core_info += f"Core {i+j:2d}: {percent:5.1f}%   "
                info.append(core_info)

        except Exception as e:
            info.append(f"Error getting CPU metrics: {e}")

        info.append("")

        # Detailed CPU info from hardware detector
        cpu_details = self.hw_detector.get_cpu_detailed_info()

        info.append("🔍 DETAILED CPU INFORMATION")
        info.append("-" * 40)
        for key, value in cpu_details.items():
            if key == 'Features' and len(value) > 100:
                # Format CPU features nicely
                features = value.split()
                info.append(f"{key}:")
                for i in range(0, len(features), 8):
                    feature_line = "  " + " ".join(features[i:i+8])
                    info.append(feature_line)
            else:
                info.append(f"{key}: {value}")

        return "\n".join(info)

    def get_enhanced_memory_info(self):
        """Get enhanced memory information"""
        info = []
        info.append("=" * 60)
        info.append("MEMORY INFORMATION")
        info.append("=" * 60)
        info.append("")

        # Memory usage with progress bars
        try:
            vmem = psutil.virtual_memory()
            swap = psutil.swap_memory()

            info.append("🧠 MEMORY USAGE")
            info.append("-" * 40)
            info.append(f"Total RAM: {self.bytes_to_gb(vmem.total):.2f} GB")
            info.append(f"Available: {self.bytes_to_gb(vmem.available):.2f} GB")
            info.append(f"Used: {self.bytes_to_gb(vmem.used):.2f} GB")
            info.append(f"Free: {self.bytes_to_gb(vmem.free):.2f} GB")
            info.append(f"Usage: {vmem.percent:.1f}%")

            # ASCII progress bar for memory
            bar_length = 50
            filled_length = int(bar_length * vmem.percent // 100)
            bar = "█" * filled_length + "░" * (bar_length - filled_length)
            info.append(f"RAM Usage: [{bar}] {vmem.percent:.1f}%")

            info.append("")
            info.append("💽 SWAP MEMORY")
            info.append("-" * 40)
            info.append(f"Total Swap: {self.bytes_to_gb(swap.total):.2f} GB")
            info.append(f"Used Swap: {self.bytes_to_gb(swap.used):.2f} GB")
            info.append(f"Free Swap: {self.bytes_to_gb(swap.free):.2f} GB")
            info.append(f"Swap Usage: {swap.percent:.1f}%")

            if swap.total > 0:
                filled_length = int(bar_length * swap.percent // 100)
                bar = "█" * filled_length + "░" * (bar_length - filled_length)
                info.append(f"Swap Usage: [{bar}] {swap.percent:.1f}%")

        except Exception as e:
            info.append(f"Error getting memory info: {e}")

        info.append("")

        # Detailed memory info from hardware detector
        mem_details = self.hw_detector.get_memory_detailed_info()

        info.append("🔍 DETAILED MEMORY INFORMATION")
        info.append("-" * 40)
        for key, value in mem_details.items():
            info.append(f"{key}:")
            for line in str(value).split('\n'):
                if line.strip():
                    info.append(f"  {line}")

        return "\n".join(info)

    def get_enhanced_storage_info(self):
        """Get enhanced storage information"""
        info = []
        info.append("=" * 60)
        info.append("STORAGE INFORMATION")
        info.append("=" * 60)
        info.append("")

        # Disk usage with visual indicators
        try:
            partitions = psutil.disk_partitions()

            info.append("💾 DISK PARTITIONS")
            info.append("-" * 40)

            for partition in partitions:
                info.append(f"\nPartition: {partition.device}")
                info.append(f"  Mountpoint: {partition.mountpoint}")
                info.append(f"  File System: {partition.fstype}")

                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    total_gb = self.bytes_to_gb(usage.total)
                    used_gb = self.bytes_to_gb(usage.used)
                    free_gb = self.bytes_to_gb(usage.free)
                    percent = (usage.used / usage.total) * 100

                    info.append(f"  Total: {total_gb:.2f} GB")
                    info.append(f"  Used: {used_gb:.2f} GB")
                    info.append(f"  Free: {free_gb:.2f} GB")
                    info.append(f"  Usage: {percent:.1f}%")

                    # Visual usage bar
                    bar_length = 30
                    filled_length = int(bar_length * percent // 100)
                    bar = "█" * filled_length + "░" * (bar_length - filled_length)
                    info.append(f"  [{bar}] {percent:.1f}%")

                except PermissionError:
                    info.append("  Permission denied")

        except Exception as e:
            info.append(f"Error getting storage info: {e}")

        info.append("")

        # Detailed storage info from hardware detector
        storage_details = self.hw_detector.get_storage_detailed_info()

        info.append("🔍 DETAILED STORAGE INFORMATION")
        info.append("-" * 40)
        for key, value in storage_details.items():
            info.append(f"\n{key}:")
            for line in str(value).split('\n'):
                if line.strip():
                    info.append(f"  {line}")

        return "\n".join(info)

    def get_enhanced_graphics_info(self):
        """Get enhanced graphics information"""
        info = []
        info.append("=" * 60)
        info.append("GRAPHICS INFORMATION")
        info.append("=" * 60)
        info.append("")

        # Get graphics info from hardware detector
        graphics_details = self.hw_detector.get_graphics_detailed_info()

        for key, value in graphics_details.items():
            info.append(f"🎮 {key.upper()}")
            info.append("-" * 40)
            for line in str(value).split('\n'):
                if line.strip():
                    info.append(f"  {line}")
            info.append("")

        return "\n".join(info)

    def get_enhanced_network_info(self):
        """Get enhanced network information"""
        info = []
        info.append("=" * 60)
        info.append("NETWORK INFORMATION")
        info.append("=" * 60)
        info.append("")

        # Network interfaces with psutil
        try:
            interfaces = psutil.net_if_addrs()
            stats = psutil.net_if_stats()
            io_counters = psutil.net_io_counters(pernic=True)

            info.append("🌐 NETWORK INTERFACES")
            info.append("-" * 40)

            for interface, addresses in interfaces.items():
                info.append(f"\nInterface: {interface}")

                # Interface statistics
                if interface in stats:
                    stat = stats[interface]
                    info.append(f"  Status: {'Up' if stat.isup else 'Down'}")
                    info.append(f"  Speed: {stat.speed} Mbps" if stat.speed > 0 else "  Speed: Unknown")
                    info.append(f"  MTU: {stat.mtu}")

                # Addresses
                for addr in addresses:
                    if addr.family == 2:  # IPv4
                        info.append(f"  IPv4: {addr.address}")
                        if addr.netmask:
                            info.append(f"    Netmask: {addr.netmask}")
                    elif addr.family == 10:  # IPv6
                        info.append(f"  IPv6: {addr.address}")
                    elif addr.family == 17:  # MAC
                        info.append(f"  MAC: {addr.address}")

                # I/O statistics
                if interface in io_counters:
                    io = io_counters[interface]
                    info.append(f"  Bytes Sent: {self.bytes_to_mb(io.bytes_sent):.2f} MB")
                    info.append(f"  Bytes Received: {self.bytes_to_mb(io.bytes_recv):.2f} MB")
                    info.append(f"  Packets Sent: {io.packets_sent}")
                    info.append(f"  Packets Received: {io.packets_recv}")

        except Exception as e:
            info.append(f"Error getting network interface info: {e}")

        info.append("")

        # Detailed network info from hardware detector
        network_details = self.hw_detector.get_network_detailed_info()

        for key, value in network_details.items():
            info.append(f"🔍 {key.upper()}")
            info.append("-" * 40)
            for line in str(value).split('\n'):
                if line.strip():
                    info.append(f"  {line}")
            info.append("")

        return "\n".join(info)

    def get_audio_info(self):
        """Get audio information"""
        info = []
        info.append("=" * 60)
        info.append("AUDIO INFORMATION")
        info.append("=" * 60)
        info.append("")

        # Get audio info from hardware detector
        audio_details = self.hw_detector.get_audio_info()

        for key, value in audio_details.items():
            info.append(f"🔊 {key.upper()}")
            info.append("-" * 40)
            for line in str(value).split('\n'):
                if line.strip():
                    info.append(f"  {line}")
            info.append("")

        return "\n".join(info)

    def get_usb_pci_info(self):
        """Get USB and PCI device information"""
        info = []
        info.append("=" * 60)
        info.append("USB & PCI DEVICES")
        info.append("=" * 60)
        info.append("")

        # Get USB and PCI info from hardware detector
        usb_data = self.hw_detector.get_usb_devices()
        pci_data = self.hw_detector.get_pci_devices()

        # USB devices
        for key, value in usb_data.items():
            info.append(f"🔌 {key.upper()}")
            info.append("-" * 40)
            for line in str(value).split('\n'):
                if line.strip():
                    info.append(f"  {line}")
            info.append("")

        # PCI devices
        for key, value in pci_data.items():
            info.append(f"🎛️  {key.upper()}")
            info.append("-" * 40)
            for line in str(value).split('\n'):
                if line.strip():
                    info.append(f"  {line}")
            info.append("")

        return "\n".join(info)

    def get_sensors_info(self):
        """Get sensors and temperature information"""
        info = []
        info.append("=" * 60)
        info.append("SENSORS & TEMPERATURE")
        info.append("=" * 60)
        info.append("")

        # Get sensor info from hardware detector
        sensor_data = self.hw_detector.get_sensors_info()
        power_data = self.hw_detector.get_power_info()

        # Temperature sensors
        for key, value in sensor_data.items():
            info.append(f"🌡️ {key.upper()}")
            info.append("-" * 40)
            for line in str(value).split('\n'):
                if line.strip():
                    info.append(f"  {line}")
            info.append("")

        # Power management
        for key, value in power_data.items():
            info.append(f"🔋 {key.upper()}")
            info.append("-" * 40)
            for line in str(value).split('\n'):
                if line.strip():
                    info.append(f"  {line}")
            info.append("")

        return "\n".join(info)

    def get_enhanced_processes_info(self):
        """Get enhanced process information"""
        info = []
        info.append("=" * 60)
        info.append("SYSTEM PROCESSES")
        info.append("=" * 60)
        info.append("")

        try:
            # Get all processes
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'username', 'status']):
                try:
                    processes.append(proc.info)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass

            # Top processes by CPU
            processes_cpu = sorted(processes, key=lambda x: x['cpu_percent'] or 0, reverse=True)

            info.append("📊 TOP PROCESSES BY CPU USAGE")
            info.append("-" * 60)
            info.append(f"{'PID':<8} {'Name':<25} {'User':<12} {'CPU%':<8} {'Mem%':<8} {'Status':<10}")
            info.append("-" * 60)

            for proc in processes_cpu[:20]:
                pid = proc['pid']
                name = (proc['name'] or 'N/A')[:24]
                user = (proc['username'] or 'N/A')[:11]
                cpu_percent = f"{proc['cpu_percent'] or 0:.1f}%"
                mem_percent = f"{proc['memory_percent'] or 0:.1f}%"
                status = (proc['status'] or 'N/A')[:9]

                info.append(f"{pid:<8} {name:<25} {user:<12} {cpu_percent:<8} {mem_percent:<8} {status:<10}")

            # Top processes by memory
            processes_mem = sorted(processes, key=lambda x: x['memory_percent'] or 0, reverse=True)

            info.append("")
            info.append("🧠 TOP PROCESSES BY MEMORY USAGE")
            info.append("-" * 60)
            info.append(f"{'PID':<8} {'Name':<25} {'User':<12} {'CPU%':<8} {'Mem%':<8} {'Status':<10}")
            info.append("-" * 60)

            for proc in processes_mem[:20]:
                pid = proc['pid']
                name = (proc['name'] or 'N/A')[:24]
                user = (proc['username'] or 'N/A')[:11]
                cpu_percent = f"{proc['cpu_percent'] or 0:.1f}%"
                mem_percent = f"{proc['memory_percent'] or 0:.1f}%"
                status = (proc['status'] or 'N/A')[:9]

                info.append(f"{pid:<8} {name:<25} {user:<12} {cpu_percent:<8} {mem_percent:<8} {status:<10}")

            info.append("")
            info.append(f"📈 PROCESS SUMMARY")
            info.append("-" * 40)
            info.append(f"Total Processes: {len(processes)}")

            # Count by status
            status_counts = {}
            for proc in processes:
                status = proc['status'] or 'unknown'
                status_counts[status] = status_counts.get(status, 0) + 1

            for status, count in status_counts.items():
                info.append(f"  {status.title()}: {count}")

        except Exception as e:
            info.append(f"Error getting process info: {e}")

        return "\n".join(info)

    def get_security_info(self):
        """Get security information"""
        info = []
        info.append("=" * 60)
        info.append("SECURITY INFORMATION")
        info.append("=" * 60)
        info.append("")

        # Get security info from hardware detector
        security_data = self.hw_detector.get_security_info()

        for key, value in security_data.items():
            info.append(f"🔒 {key.upper()}")
            info.append("-" * 40)
            for line in str(value).split('\n'):
                if line.strip():
                    info.append(f"  {line}")
            info.append("")

        # Additional security checks
        info.append("🛡️ ADDITIONAL SECURITY CHECKS")
        info.append("-" * 40)

        # Check for common security tools
        security_tools = {
            'fail2ban': 'systemctl is-active fail2ban 2>/dev/null',
            'clamav': 'systemctl is-active clamav-daemon 2>/dev/null',
            'rkhunter': 'which rkhunter >/dev/null 2>&1 && echo "installed" || echo "not installed"',
            'chkrootkit': 'which chkrootkit >/dev/null 2>&1 && echo "installed" || echo "not installed"'
        }

        for tool, command in security_tools.items():
            result = self.run_command(command)
            info.append(f"{tool.title()}: {result if result else 'Not available'}")

        return "\n".join(info)

    def update_quick_info(self):
        """Update the quick info display in header"""
        try:
            # Get basic system info
            cpu_count = psutil.cpu_count(logical=False)
            vmem = psutil.virtual_memory()

            quick_info = (f"CPU: {cpu_count} cores | "
                         f"RAM: {self.bytes_to_gb(vmem.total):.1f} GB "
                         f"({100-vmem.percent:.1f}% free) | "
                         f"OS: {platform.system()} {platform.release()}")

            self.quick_info_label.config(text=quick_info)
        except Exception as e:
            self.quick_info_label.config(text=f"Error loading quick info: {e}")

    def refresh_all_data(self):
        """Refresh all system information in a separate thread"""
        def refresh_worker():
            try:
                self.update_status("Refreshing system information...")

                # Update quick info
                self.root.after(0, self.update_quick_info)

                # Clear all text widgets
                text_widgets = [
                    self.overview_text, self.motherboard_text, self.cpu_text,
                    self.memory_text, self.storage_text, self.graphics_text,
                    self.network_text, self.audio_text, self.usb_pci_text,
                    self.sensors_text, self.processes_text, self.security_text
                ]

                def clear_widgets():
                    for widget in text_widgets:
                        widget.delete(1.0, tk.END)

                self.root.after(0, clear_widgets)

                # Update each tab with new data
                data_updates = [
                    (self.overview_text, self.get_overview_info),
                    (self.motherboard_text, self.get_motherboard_info),
                    (self.cpu_text, self.get_enhanced_cpu_info),
                    (self.memory_text, self.get_enhanced_memory_info),
                    (self.storage_text, self.get_enhanced_storage_info),
                    (self.graphics_text, self.get_enhanced_graphics_info),
                    (self.network_text, self.get_enhanced_network_info),
                    (self.audio_text, self.get_audio_info),
                    (self.usb_pci_text, self.get_usb_pci_info),
                    (self.sensors_text, self.get_sensors_info),
                    (self.processes_text, self.get_enhanced_processes_info),
                    (self.security_text, self.get_security_info)
                ]

                for i, (widget, data_func) in enumerate(data_updates):
                    self.root.after(0, lambda: self.update_status(f"Updating {data_func.__name__}..."))
                    data = data_func()
                    self.root.after(0, lambda w=widget, d=data: w.insert(tk.END, d))

                self.root.after(0, lambda: self.update_status("All data refreshed successfully"))

            except Exception as e:
                self.root.after(0, lambda: self.update_status(f"Error refreshing data: {str(e)}"))

        # Run refresh in separate thread to prevent GUI freezing
        thread = threading.Thread(target=refresh_worker)
        thread.daemon = True
        thread.start()

    def deep_hardware_scan(self):
        """Perform deep hardware scan"""
        def scan_worker():
            try:
                self.update_status("Performing deep hardware scan...")

                # Get comprehensive hardware summary
                hardware_summary = self.hw_detector.get_hardware_summary()

                # Create a new window for the results
                def show_scan_results():
                    scan_window = tk.Toplevel(self.root)
                    scan_window.title("Deep Hardware Scan Results")
                    scan_window.geometry("900x700")

                    # Create text widget for results
                    text_frame = ttk.Frame(scan_window, padding="10")
                    text_frame.pack(fill=tk.BOTH, expand=True)

                    scan_text = scrolledtext.ScrolledText(text_frame, wrap=tk.WORD,
                                                        width=100, height=40,
                                                        font=('Consolas', 9))
                    scan_text.pack(fill=tk.BOTH, expand=True)

                    # Format and display results
                    for category, data in hardware_summary.items():
                        formatted_data = self.hw_detector.format_hardware_info(category, data)
                        scan_text.insert(tk.END, formatted_data)

                    # Add save button
                    save_btn = ttk.Button(text_frame, text="Save Scan Results",
                                        command=lambda: self.save_scan_results(hardware_summary))
                    save_btn.pack(pady=(10, 0))

                self.root.after(0, show_scan_results)
                self.root.after(0, lambda: self.update_status("Deep hardware scan completed"))

            except Exception as e:
                self.root.after(0, lambda: self.update_status(f"Hardware scan error: {str(e)}"))

        thread = threading.Thread(target=scan_worker)
        thread.daemon = True
        thread.start()

    def save_scan_results(self, hardware_summary):
        """Save hardware scan results to file"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("JSON files", "*.json"), ("All files", "*.*")],
            title="Save Hardware Scan Results"
        )

        if filename:
            try:
                if filename.endswith('.json'):
                    with open(filename, 'w') as f:
                        json.dump(hardware_summary, f, indent=2, default=str)
                else:
                    with open(filename, 'w') as f:
                        f.write(f"Deep Hardware Scan Results\n")
                        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                        f.write("=" * 80 + "\n\n")

                        for category, data in hardware_summary.items():
                            formatted_data = self.hw_detector.format_hardware_info(category, data)
                            f.write(formatted_data)

                messagebox.showinfo("Success", f"Hardware scan results saved to:\n{filename}")
                self.update_status(f"Scan results saved to {os.path.basename(filename)}")

            except Exception as e:
                messagebox.showerror("Error", f"Failed to save scan results:\n{str(e)}")

    def export_report(self):
        """Export system specifications report"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            title="Export System Specifications Report"
        )

        if filename:
            try:
                with open(filename, 'w') as f:
                    f.write(f"System Specifications Report\n")
                    f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write("=" * 80 + "\n\n")

                    # Export data from all tabs
                    reports = [
                        ("SYSTEM OVERVIEW", self.get_overview_info()),
                        ("MOTHERBOARD", self.get_motherboard_info()),
                        ("CPU", self.get_enhanced_cpu_info()),
                        ("MEMORY", self.get_enhanced_memory_info()),
                        ("STORAGE", self.get_enhanced_storage_info()),
                        ("GRAPHICS", self.get_enhanced_graphics_info()),
                        ("NETWORK", self.get_enhanced_network_info()),
                        ("AUDIO", self.get_audio_info()),
                        ("USB/PCI DEVICES", self.get_usb_pci_info()),
                        ("SENSORS", self.get_sensors_info()),
                        ("PROCESSES", self.get_enhanced_processes_info()),
                        ("SECURITY", self.get_security_info())
                    ]

                    for title, content in reports:
                        f.write(f"{title}\n")
                        f.write("=" * len(title) + "\n")
                        f.write(content)
                        f.write("\n\n")

                messagebox.showinfo("Success", f"Report exported to:\n{filename}")
                self.update_status(f"Report exported to {os.path.basename(filename)}")

            except Exception as e:
                messagebox.showerror("Error", f"Failed to export report:\n{str(e)}")

    def show_about(self):
        """Show about dialog"""
        about_text = """Enhanced System Specifications GUI

Version: 2.0
Platform: Linux Debian

Features:
• Comprehensive system information display
• Real-time hardware monitoring
• Deep hardware detection capabilities
• Export functionality for reports
• Multi-threaded scanning for better performance

This application provides detailed information about your computer's hardware and software configuration.

Created with Python and Tkinter for Linux systems."""

        messagebox.showinfo("About", about_text)

    def run_command(self, command):
        """Run a system command and return output"""
        try:
            result = subprocess.run(command, shell=True, capture_output=True,
                                  text=True, timeout=15)
            return result.stdout.strip() if result.returncode == 0 else f"Command failed: {command}"
        except subprocess.TimeoutExpired:
            return f"Command timed out: {command}"
        except Exception as e:
            return f"Error running command '{command}': {str(e)}"


def main():
    """Main function to run the enhanced application"""
    try:
        root = tk.Tk()
        app = EnhancedSystemSpecsGUI(root)

        # Handle window closing
        def on_closing():
            root.quit()
            root.destroy()

        root.protocol("WM_DELETE_WINDOW", on_closing)
        root.mainloop()

    except Exception as e:
        print(f"Error starting application: {e}")

        # Show error in simple dialog if possible
        try:
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("Application Error",
                               f"Failed to start Enhanced System Specifications:\n{str(e)}")
        except:
            pass


if __name__ == "__main__":
    main()
