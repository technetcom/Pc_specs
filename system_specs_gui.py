#!/usr/bin/env python3
"""
System Specifications GUI Application for Linux Debian
A comprehensive GUI tool to display detailed computer specifications
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
import subprocess
import os
import platform
import psutil
import json
from datetime import datetime

class SystemSpecsGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("System Specifications - Linux Debian")
        self.root.geometry("900x700")
        self.root.configure(bg='#f0f0f0')

        # Create main frame
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure grid weights
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)

        # Title
        title_label = ttk.Label(main_frame, text="Computer System Specifications",
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, pady=(0, 10))

        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Create tabs
        self.create_system_tab()
        self.create_cpu_tab()
        self.create_memory_tab()
        self.create_storage_tab()
        self.create_network_tab()
        self.create_graphics_tab()
        self.create_processes_tab()

        # Refresh button
        refresh_btn = ttk.Button(main_frame, text="Refresh All Data",
                               command=self.refresh_all_data)
        refresh_btn.grid(row=2, column=0, pady=(10, 0))

        # Load initial data
        self.refresh_all_data()

    def create_system_tab(self):
        """Create system information tab"""
        frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(frame, text="System Info")

        # Create scrolled text widget
        self.system_text = scrolledtext.ScrolledText(frame, wrap=tk.WORD,
                                                   width=80, height=30)
        self.system_text.pack(fill=tk.BOTH, expand=True)

    def create_cpu_tab(self):
        """Create CPU information tab"""
        frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(frame, text="CPU")

        self.cpu_text = scrolledtext.ScrolledText(frame, wrap=tk.WORD,
                                                width=80, height=30)
        self.cpu_text.pack(fill=tk.BOTH, expand=True)

    def create_memory_tab(self):
        """Create memory information tab"""
        frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(frame, text="Memory")

        self.memory_text = scrolledtext.ScrolledText(frame, wrap=tk.WORD,
                                                   width=80, height=30)
        self.memory_text.pack(fill=tk.BOTH, expand=True)

    def create_storage_tab(self):
        """Create storage information tab"""
        frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(frame, text="Storage")

        self.storage_text = scrolledtext.ScrolledText(frame, wrap=tk.WORD,
                                                    width=80, height=30)
        self.storage_text.pack(fill=tk.BOTH, expand=True)

    def create_network_tab(self):
        """Create network information tab"""
        frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(frame, text="Network")

        self.network_text = scrolledtext.ScrolledText(frame, wrap=tk.WORD,
                                                    width=80, height=30)
        self.network_text.pack(fill=tk.BOTH, expand=True)

    def create_graphics_tab(self):
        """Create graphics information tab"""
        frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(frame, text="Graphics")

        self.graphics_text = scrolledtext.ScrolledText(frame, wrap=tk.WORD,
                                                     width=80, height=30)
        self.graphics_text.pack(fill=tk.BOTH, expand=True)

    def create_processes_tab(self):
        """Create processes information tab"""
        frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(frame, text="Processes")

        self.processes_text = scrolledtext.ScrolledText(frame, wrap=tk.WORD,
                                                      width=80, height=30)
        self.processes_text.pack(fill=tk.BOTH, expand=True)

    def run_command(self, command):
        """Run a system command and return output"""
        try:
            result = subprocess.run(command, shell=True, capture_output=True,
                                  text=True, timeout=10)
            return result.stdout.strip() if result.returncode == 0 else f"Command failed: {command}"
        except subprocess.TimeoutExpired:
            return f"Command timed out: {command}"
        except Exception as e:
            return f"Error running command '{command}': {str(e)}"

    def get_system_info(self):
        """Get general system information"""
        info = []
        info.append("=" * 50)
        info.append("SYSTEM INFORMATION")
        info.append("=" * 50)
        info.append(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        info.append("")

        # Basic system info
        info.append(f"Operating System: {platform.system()}")
        info.append(f"OS Release: {platform.release()}")
        info.append(f"OS Version: {platform.version()}")
        info.append(f"Machine Type: {platform.machine()}")
        info.append(f"Processor: {platform.processor()}")
        info.append(f"Architecture: {platform.architecture()[0]}")
        info.append(f"Hostname: {platform.node()}")
        info.append("")

        # Distribution info
        try:
            with open('/etc/os-release', 'r') as f:
                os_release = f.read()
            info.append("Distribution Information:")
            for line in os_release.split('\n'):
                if line.strip() and '=' in line:
                    key, value = line.split('=', 1)
                    info.append(f"  {key}: {value.strip('\"')}")
        except Exception as e:
            info.append(f"Could not read distribution info: {e}")

        info.append("")

        # Kernel information
        info.append("Kernel Information:")
        info.append(f"  Kernel: {self.run_command('uname -r')}")
        info.append(f"  Kernel Version: {self.run_command('uname -v')}")
        info.append("")

        # System uptime
        try:
            uptime_seconds = psutil.boot_time()
            uptime = datetime.fromtimestamp(uptime_seconds)
            info.append(f"System Boot Time: {uptime.strftime('%Y-%m-%d %H:%M:%S')}")
            info.append(f"System Uptime: {datetime.now() - uptime}")
        except Exception as e:
            info.append(f"Could not get uptime: {e}")

        return "\n".join(info)

    def get_cpu_info(self):
        """Get CPU information"""
        info = []
        info.append("=" * 50)
        info.append("CPU INFORMATION")
        info.append("=" * 50)
        info.append("")

        # CPU basic info
        try:
            cpu_count = psutil.cpu_count(logical=False)
            cpu_count_logical = psutil.cpu_count(logical=True)
            cpu_freq = psutil.cpu_freq()

            info.append(f"Physical CPU Cores: {cpu_count}")
            info.append(f"Logical CPU Cores: {cpu_count_logical}")

            if cpu_freq:
                info.append(f"CPU Frequency:")
                info.append(f"  Current: {cpu_freq.current:.2f} MHz")
                info.append(f"  Min: {cpu_freq.min:.2f} MHz")
                info.append(f"  Max: {cpu_freq.max:.2f} MHz")

            # CPU usage per core
            cpu_percent = psutil.cpu_percent(interval=1, percpu=True)
            info.append(f"\nCPU Usage per Core:")
            for i, percent in enumerate(cpu_percent):
                info.append(f"  Core {i}: {percent}%")

            info.append(f"\nOverall CPU Usage: {psutil.cpu_percent(interval=1)}%")

        except Exception as e:
            info.append(f"Error getting CPU info: {e}")

        info.append("")

        # Detailed CPU info from /proc/cpuinfo
        info.append("Detailed CPU Information:")
        try:
            cpu_info = self.run_command('cat /proc/cpuinfo | head -30')
            info.append(cpu_info)
        except Exception as e:
            info.append(f"Could not read CPU details: {e}")

        return "\n".join(info)

    def get_memory_info(self):
        """Get memory information"""
        info = []
        info.append("=" * 50)
        info.append("MEMORY INFORMATION")
        info.append("=" * 50)
        info.append("")

        try:
            # Virtual memory
            vmem = psutil.virtual_memory()
            info.append("Virtual Memory:")
            info.append(f"  Total: {self.bytes_to_gb(vmem.total):.2f} GB")
            info.append(f"  Available: {self.bytes_to_gb(vmem.available):.2f} GB")
            info.append(f"  Used: {self.bytes_to_gb(vmem.used):.2f} GB")
            info.append(f"  Free: {self.bytes_to_gb(vmem.free):.2f} GB")
            info.append(f"  Percentage: {vmem.percent}%")
            info.append("")

            # Swap memory
            swap = psutil.swap_memory()
            info.append("Swap Memory:")
            info.append(f"  Total: {self.bytes_to_gb(swap.total):.2f} GB")
            info.append(f"  Used: {self.bytes_to_gb(swap.used):.2f} GB")
            info.append(f"  Free: {self.bytes_to_gb(swap.free):.2f} GB")
            info.append(f"  Percentage: {swap.percent}%")

        except Exception as e:
            info.append(f"Error getting memory info: {e}")

        info.append("")

        # Memory info from /proc/meminfo
        info.append("Detailed Memory Information:")
        try:
            meminfo = self.run_command('cat /proc/meminfo | head -20')
            info.append(meminfo)
        except Exception as e:
            info.append(f"Could not read memory details: {e}")

        return "\n".join(info)

    def get_storage_info(self):
        """Get storage information"""
        info = []
        info.append("=" * 50)
        info.append("STORAGE INFORMATION")
        info.append("=" * 50)
        info.append("")

        # Disk usage
        try:
            partitions = psutil.disk_partitions()
            info.append("Disk Partitions:")
            for partition in partitions:
                info.append(f"\nPartition: {partition.device}")
                info.append(f"  Mountpoint: {partition.mountpoint}")
                info.append(f"  File System: {partition.fstype}")

                try:
                    partition_usage = psutil.disk_usage(partition.mountpoint)
                    info.append(f"  Total Size: {self.bytes_to_gb(partition_usage.total):.2f} GB")
                    info.append(f"  Used: {self.bytes_to_gb(partition_usage.used):.2f} GB")
                    info.append(f"  Free: {self.bytes_to_gb(partition_usage.free):.2f} GB")
                    info.append(f"  Percentage: {(partition_usage.used / partition_usage.total) * 100:.1f}%")
                except PermissionError:
                    info.append("  Permission denied")

        except Exception as e:
            info.append(f"Error getting disk info: {e}")

        info.append("")

        # Block devices
        info.append("Block Devices Information:")
        block_devices = self.run_command('lsblk -o NAME,SIZE,TYPE,MOUNTPOINT,FSTYPE')
        info.append(block_devices)

        return "\n".join(info)

    def get_network_info(self):
        """Get network information"""
        info = []
        info.append("=" * 50)
        info.append("NETWORK INFORMATION")
        info.append("=" * 50)
        info.append("")

        try:
            # Network interfaces
            interfaces = psutil.net_if_addrs()
            info.append("Network Interfaces:")

            for interface, addresses in interfaces.items():
                info.append(f"\nInterface: {interface}")
                for addr in addresses:
                    if addr.family == 2:  # IPv4
                        info.append(f"  IPv4 Address: {addr.address}")
                        info.append(f"  IPv4 Netmask: {addr.netmask}")
                    elif addr.family == 10:  # IPv6
                        info.append(f"  IPv6 Address: {addr.address}")
                        info.append(f"  IPv6 Netmask: {addr.netmask}")
                    elif addr.family == 17:  # MAC
                        info.append(f"  MAC Address: {addr.address}")

            # Network statistics
            info.append(f"\nNetwork Statistics:")
            net_stats = psutil.net_io_counters()
            info.append(f"  Bytes Sent: {self.bytes_to_mb(net_stats.bytes_sent):.2f} MB")
            info.append(f"  Bytes Received: {self.bytes_to_mb(net_stats.bytes_recv):.2f} MB")
            info.append(f"  Packets Sent: {net_stats.packets_sent}")
            info.append(f"  Packets Received: {net_stats.packets_recv}")

        except Exception as e:
            info.append(f"Error getting network info: {e}")

        return "\n".join(info)

    def get_graphics_info(self):
        """Get graphics information"""
        info = []
        info.append("=" * 50)
        info.append("GRAPHICS INFORMATION")
        info.append("=" * 50)
        info.append("")

        # Graphics card info
        info.append("Graphics Cards:")
        gpu_info = self.run_command('lspci | grep -i vga')
        if gpu_info:
            info.append(gpu_info)
        else:
            info.append("No VGA devices found")

        info.append("")

        # OpenGL info (if available)
        info.append("OpenGL Information:")
        gl_info = self.run_command('glxinfo | head -20 2>/dev/null || echo "glxinfo not available"')
        info.append(gl_info)

        info.append("")

        # Display information
        info.append("Display Information:")
        display_info = self.run_command('xrandr 2>/dev/null || echo "xrandr not available"')
        info.append(display_info)

        return "\n".join(info)

    def get_processes_info(self):
        """Get running processes information"""
        info = []
        info.append("=" * 50)
        info.append("RUNNING PROCESSES")
        info.append("=" * 50)
        info.append("")

        try:
            # Top processes by CPU usage
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                try:
                    processes.append(proc.info)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass

            # Sort by CPU usage
            processes.sort(key=lambda x: x['cpu_percent'] or 0, reverse=True)

            info.append("Top Processes by CPU Usage:")
            info.append(f"{'PID':<8} {'Name':<25} {'CPU%':<8} {'Memory%':<8}")
            info.append("-" * 50)

            for proc in processes[:15]:  # Top 15 processes
                pid = proc['pid']
                name = (proc['name'] or 'N/A')[:24]
                cpu_percent = f"{proc['cpu_percent'] or 0:.1f}%"
                mem_percent = f"{proc['memory_percent'] or 0:.1f}%"
                info.append(f"{pid:<8} {name:<25} {cpu_percent:<8} {mem_percent:<8}")

            info.append(f"\nTotal running processes: {len(processes)}")

        except Exception as e:
            info.append(f"Error getting process info: {e}")

        return "\n".join(info)

    def bytes_to_gb(self, bytes_value):
        """Convert bytes to gigabytes"""
        return bytes_value / (1024**3)

    def bytes_to_mb(self, bytes_value):
        """Convert bytes to megabytes"""
        return bytes_value / (1024**2)

    def refresh_all_data(self):
        """Refresh all system information"""
        # Clear all text widgets
        text_widgets = [
            self.system_text, self.cpu_text, self.memory_text,
            self.storage_text, self.network_text, self.graphics_text,
            self.processes_text
        ]

        for widget in text_widgets:
            widget.delete(1.0, tk.END)

        # Update all tabs with new data
        self.system_text.insert(tk.END, self.get_system_info())
        self.cpu_text.insert(tk.END, self.get_cpu_info())
        self.memory_text.insert(tk.END, self.get_memory_info())
        self.storage_text.insert(tk.END, self.get_storage_info())
        self.network_text.insert(tk.END, self.get_network_info())
        self.graphics_text.insert(tk.END, self.get_graphics_info())
        self.processes_text.insert(tk.END, self.get_processes_info())


def main():
    """Main function to run the application"""
    root = tk.Tk()
    app = SystemSpecsGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
