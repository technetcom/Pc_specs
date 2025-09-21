#!/usr/bin/env python3
"""
Enhanced Hardware Detection Module
Provides detailed hardware information for Linux systems
"""

import subprocess
import os
import re
import json
from collections import defaultdict

class HardwareDetector:
    """Advanced hardware detection for Linux systems"""

    def __init__(self):
        self.cache = {}

    def run_command(self, command, shell=True, timeout=10):
        """Safely run system commands with timeout"""
        try:
            # Handle commands that might be in /usr/sbin
            if shell and isinstance(command, str):
                # Check if command starts with common system commands that are in /usr/sbin
                sbin_commands = ['dmidecode', 'smartctl', 'iwconfig', 'fdisk']
                cmd_parts = command.split()
                if cmd_parts and cmd_parts[0] in sbin_commands:
                    # Try with full path first
                    full_path_cmd = command.replace(cmd_parts[0], f'/usr/sbin/{cmd_parts[0]}', 1)
                    if os.path.exists(f'/usr/sbin/{cmd_parts[0]}'):
                        command = full_path_cmd

            result = subprocess.run(
                command,
                shell=shell,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            return result.stdout.strip() if result.returncode == 0 else ""
        except (subprocess.TimeoutExpired, subprocess.CalledProcessError, FileNotFoundError):
            return ""

    def read_file_safe(self, filepath):
        """Safely read file contents"""
        try:
            with open(filepath, 'r') as f:
                return f.read().strip()
        except (FileNotFoundError, PermissionError, IOError):
            return ""

    def parse_key_value_file(self, filepath, separator='='):
        """Parse key-value files like /proc/version"""
        content = self.read_file_safe(filepath)
        data = {}
        for line in content.split('\n'):
            if separator in line:
                key, value = line.split(separator, 1)
                data[key.strip()] = value.strip().strip('"')
        return data

    def get_motherboard_info(self):
        """Get motherboard information"""
        info = {}

        # DMI information
        dmi_fields = {
            'board-name': 'Board Name',
            'board-vendor': 'Board Vendor',
            'board-version': 'Board Version',
            'board-serial': 'Board Serial',
            'bios-vendor': 'BIOS Vendor',
            'bios-version': 'BIOS Version',
            'bios-release-date': 'BIOS Date',
            'system-manufacturer': 'System Manufacturer',
            'system-product-name': 'System Model',
            'system-version': 'System Version',
            'system-serial-number': 'System Serial',
            'chassis-type': 'Chassis Type'
        }

        for dmi_key, display_name in dmi_fields.items():
            value = self.run_command(f"sudo /usr/sbin/dmidecode -s {dmi_key}")
            if value and value.lower() not in ['not specified', 'not available', 'to be filled by o.e.m.']:
                info[display_name] = value

        return info

    def get_cpu_detailed_info(self):
        """Get detailed CPU information"""
        info = {}

        # Parse /proc/cpuinfo
        cpuinfo = self.read_file_safe('/proc/cpuinfo')
        cpu_data = {}

        for line in cpuinfo.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip()
                value = value.strip()
                if key and value:
                    cpu_data[key] = value

        # Extract key information
        if 'model name' in cpu_data:
            info['Model'] = cpu_data['model name']
        if 'vendor_id' in cpu_data:
            info['Vendor'] = cpu_data['vendor_id']
        if 'cpu family' in cpu_data:
            info['Family'] = cpu_data['cpu family']
        if 'model' in cpu_data:
            info['Model Number'] = cpu_data['model']
        if 'stepping' in cpu_data:
            info['Stepping'] = cpu_data['stepping']
        if 'microcode' in cpu_data:
            info['Microcode'] = cpu_data['microcode']
        if 'cache size' in cpu_data:
            info['Cache Size'] = cpu_data['cache size']
        if 'flags' in cpu_data:
            info['Features'] = cpu_data['flags']

        # CPU topology
        cpu_topology = self.run_command("lscpu | grep -E '(Socket|Core|Thread)'")
        if cpu_topology:
            info['Topology'] = cpu_topology

        # CPU frequency scaling
        scaling_governor = self.read_file_safe('/sys/devices/system/cpu/cpu0/cpufreq/scaling_governor')
        if scaling_governor:
            info['Scaling Governor'] = scaling_governor

        return info

    def get_memory_detailed_info(self):
        """Get detailed memory information"""
        info = {}

        # Parse /proc/meminfo
        meminfo = self.read_file_safe('/proc/meminfo')
        mem_data = {}

        for line in meminfo.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                mem_data[key.strip()] = value.strip()

        # Physical memory modules
        memory_modules = self.run_command("sudo /usr/sbin/dmidecode -t memory | grep -E '(Size|Speed|Type|Manufacturer|Part Number)'")
        if memory_modules:
            info['Memory Modules'] = memory_modules

        # Memory banks
        memory_slots = self.run_command("sudo /usr/sbin/dmidecode -t memory | grep -A 20 'Memory Device' | grep -E '(Locator|Size|Speed|Type)'")
        if memory_slots:
            info['Memory Slots'] = memory_slots

        return info

    def get_storage_detailed_info(self):
        """Get detailed storage information"""
        info = {}

        # SATA/NVMe drives
        drives = []

        # Get drive list
        drive_list = self.run_command("lsblk -d -o NAME,SIZE,MODEL,VENDOR")
        if drive_list:
            info['Drive Overview'] = drive_list

        # Individual drive details
        block_devices = self.run_command("ls /dev/sd* /dev/nvme* 2>/dev/null | grep -E '(sd[a-z]$|nvme[0-9]+n[0-9]+$)'")

        if block_devices:
            for device in block_devices.split('\n'):
                if device.strip():
                    device_name = device.split('/')[-1]

                    # SMART information
                    smart_info = self.run_command(f"sudo /usr/sbin/smartctl -i /dev/{device_name} 2>/dev/null")
                    if smart_info:
                        info[f'SMART Info - {device_name}'] = smart_info

                    # Device information
                    device_info = self.run_command(f"sudo hdparm -I /dev/{device_name} 2>/dev/null | head -20")
                    if device_info:
                        info[f'Device Info - {device_name}'] = device_info

        return info

    def get_network_detailed_info(self):
        """Get detailed network information"""
        info = {}

        # Network hardware
        network_hw = self.run_command("lspci | grep -i network")
        if network_hw:
            info['Network Hardware'] = network_hw

        # Ethernet controllers
        ethernet_hw = self.run_command("lspci | grep -i ethernet")
        if ethernet_hw:
            info['Ethernet Controllers'] = ethernet_hw

        # Wireless devices
        wireless_hw = self.run_command("lspci | grep -i wireless")
        if wireless_hw:
            info['Wireless Devices'] = wireless_hw

        # Interface details
        interface_details = self.run_command("ip link show")
        if interface_details:
            info['Interface Details'] = interface_details

        # Routing table
        routing_table = self.run_command("ip route show")
        if routing_table:
            info['Routing Table'] = routing_table

        # Wireless information (if available)
        wireless_info = self.run_command("/usr/sbin/iwconfig 2>/dev/null")
        if wireless_info:
            info['Wireless Configuration'] = wireless_info

        return info

    def get_graphics_detailed_info(self):
        """Get detailed graphics information"""
        info = {}

        # Graphics hardware
        graphics_hw = self.run_command("lspci | grep -i vga")
        if graphics_hw:
            info['VGA Controllers'] = graphics_hw

        # 3D controllers
        graphics_3d = self.run_command("lspci | grep -i '3d'")
        if graphics_3d:
            info['3D Controllers'] = graphics_3d

        # Display controllers
        display_controllers = self.run_command("lspci | grep -i display")
        if display_controllers:
            info['Display Controllers'] = display_controllers

        # OpenGL renderer info
        gl_renderer = self.run_command("glxinfo | grep -E '(OpenGL vendor|OpenGL renderer|OpenGL version)' 2>/dev/null")
        if gl_renderer:
            info['OpenGL Information'] = gl_renderer

        # Vulkan information
        vulkan_info = self.run_command("vulkaninfo --summary 2>/dev/null | head -20")
        if vulkan_info:
            info['Vulkan Support'] = vulkan_info

        # Display resolution and refresh rate
        display_info = self.run_command("xrandr | grep -E '(connected|primary|\\*)'")
        if display_info:
            info['Display Configuration'] = display_info

        # GPU memory (for NVIDIA)
        nvidia_info = self.run_command("nvidia-smi -q -d MEMORY 2>/dev/null | grep -E '(Total|Free|Used)'")
        if nvidia_info:
            info['NVIDIA GPU Memory'] = nvidia_info

        return info

    def get_usb_devices(self):
        """Get USB device information"""
        info = {}

        # USB devices list
        usb_devices = self.run_command("lsusb")
        if usb_devices:
            info['USB Devices'] = usb_devices

        # USB tree
        usb_tree = self.run_command("lsusb -t")
        if usb_tree:
            info['USB Device Tree'] = usb_tree

        return info

    def get_pci_devices(self):
        """Get PCI device information"""
        info = {}

        # All PCI devices
        pci_devices = self.run_command("lspci")
        if pci_devices:
            info['PCI Devices'] = pci_devices

        # PCI tree
        pci_tree = self.run_command("lspci -t")
        if pci_tree:
            info['PCI Device Tree'] = pci_tree

        return info

    def get_audio_info(self):
        """Get audio device information"""
        info = {}

        # Audio hardware
        audio_hw = self.run_command("lspci | grep -i audio")
        if audio_hw:
            info['Audio Hardware'] = audio_hw

        # ALSA information
        alsa_cards = self.run_command("cat /proc/asound/cards")
        if alsa_cards:
            info['ALSA Sound Cards'] = alsa_cards

        # PulseAudio sinks
        pulse_sinks = self.run_command("pactl list sinks 2>/dev/null | grep -E '(Name|Description)'")
        if pulse_sinks:
            info['PulseAudio Sinks'] = pulse_sinks

        return info

    def get_sensors_info(self):
        """Get temperature and sensor information"""
        info = {}

        # Hardware sensors
        sensors_output = self.run_command("sensors 2>/dev/null")
        if sensors_output:
            info['Temperature Sensors'] = sensors_output

        # Thermal zones
        thermal_zones = []
        thermal_base = "/sys/class/thermal"
        if os.path.exists(thermal_base):
            for zone in os.listdir(thermal_base):
                if zone.startswith("thermal_zone"):
                    temp_file = f"{thermal_base}/{zone}/temp"
                    type_file = f"{thermal_base}/{zone}/type"

                    temp = self.read_file_safe(temp_file)
                    zone_type = self.read_file_safe(type_file)

                    if temp and temp.isdigit():
                        temp_celsius = int(temp) / 1000
                        thermal_zones.append(f"{zone_type or zone}: {temp_celsius:.1f}°C")

        if thermal_zones:
            info['Thermal Zones'] = '\n'.join(thermal_zones)

        return info

    def get_power_info(self):
        """Get power management information"""
        info = {}

        # Battery information (for laptops)
        battery_info = self.run_command("acpi -b 2>/dev/null")
        if battery_info:
            info['Battery Status'] = battery_info

        # Power supplies
        power_supplies = []
        power_base = "/sys/class/power_supply"
        if os.path.exists(power_base):
            for supply in os.listdir(power_base):
                supply_path = f"{power_base}/{supply}"
                supply_type = self.read_file_safe(f"{supply_path}/type")

                if supply_type == "Battery":
                    capacity = self.read_file_safe(f"{supply_path}/capacity")
                    status = self.read_file_safe(f"{supply_path}/status")
                    technology = self.read_file_safe(f"{supply_path}/technology")

                    battery_details = f"Battery {supply}:"
                    if capacity:
                        battery_details += f" {capacity}%"
                    if status:
                        battery_details += f" ({status})"
                    if technology:
                        battery_details += f" [{technology}]"

                    power_supplies.append(battery_details)

                elif supply_type in ["Mains", "ADP1"]:
                    online = self.read_file_safe(f"{supply_path}/online")
                    power_supplies.append(f"AC Adapter {supply}: {'Connected' if online == '1' else 'Disconnected'}")

        if power_supplies:
            info['Power Supplies'] = '\n'.join(power_supplies)

        # CPU frequency scaling
        scaling_info = []
        cpu_base = "/sys/devices/system/cpu"
        if os.path.exists(cpu_base):
            for cpu_dir in os.listdir(cpu_base):
                if cpu_dir.startswith("cpu") and cpu_dir[3:].isdigit():
                    cpufreq_path = f"{cpu_base}/{cpu_dir}/cpufreq"
                    if os.path.exists(cpufreq_path):
                        governor = self.read_file_safe(f"{cpufreq_path}/scaling_governor")
                        cur_freq = self.read_file_safe(f"{cpufreq_path}/scaling_cur_freq")
                        min_freq = self.read_file_safe(f"{cpufreq_path}/scaling_min_freq")
                        max_freq = self.read_file_safe(f"{cpufreq_path}/scaling_max_freq")

                        if governor:
                            freq_info = f"{cpu_dir}: {governor}"
                            if cur_freq and cur_freq.isdigit():
                                freq_info += f" ({int(cur_freq)/1000:.0f} MHz"
                                if min_freq and max_freq:
                                    freq_info += f", {int(min_freq)/1000:.0f}-{int(max_freq)/1000:.0f} MHz range"
                                freq_info += ")"
                            scaling_info.append(freq_info)
                        break  # Just show info for first CPU

        if scaling_info:
            info['CPU Frequency Scaling'] = '\n'.join(scaling_info)

        return info

    def get_kernel_modules(self):
        """Get loaded kernel modules"""
        info = {}

        # Loaded modules
        modules = self.run_command("lsmod | head -20")
        if modules:
            info['Loaded Kernel Modules (Top 20)'] = modules

        # Driver information for key hardware
        drivers = {}

        # Graphics drivers
        gpu_driver = self.run_command("lspci -k | grep -A 2 -i vga")
        if gpu_driver:
            drivers['Graphics Driver'] = gpu_driver

        # Network drivers
        net_driver = self.run_command("lspci -k | grep -A 2 -i ethernet")
        if net_driver:
            drivers['Ethernet Driver'] = net_driver

        # Audio drivers
        audio_driver = self.run_command("lspci -k | grep -A 2 -i audio")
        if audio_driver:
            drivers['Audio Driver'] = audio_driver

        if drivers:
            info['Hardware Drivers'] = '\n\n'.join([f"{k}:\n{v}" for k, v in drivers.items()])

        return info

    def get_virtualization_info(self):
        """Get virtualization information"""
        info = {}

        # Check if running in VM
        virt_what = self.run_command("sudo virt-what 2>/dev/null")
        if virt_what:
            info['Virtualization Type'] = virt_what
        else:
            # Alternative detection methods
            dmi_sys_vendor = self.run_command("sudo dmidecode -s system-manufacturer")
            if any(vm in dmi_sys_vendor.lower() for vm in ['vmware', 'virtualbox', 'qemu', 'xen', 'microsoft corporation']):
                info['Virtualization Type'] = f"Detected: {dmi_sys_vendor}"

        # CPU virtualization features
        cpu_virt = self.run_command("grep -E '(vmx|svm)' /proc/cpuinfo | head -1")
        if cpu_virt:
            if 'vmx' in cpu_virt:
                info['CPU Virtualization'] = "Intel VT-x supported"
            elif 'svm' in cpu_virt:
                info['CPU Virtualization'] = "AMD-V supported"

        # Hypervisor detection
        hypervisor = self.run_command("dmesg | grep -i hypervisor | head -5")
        if hypervisor:
            info['Hypervisor Messages'] = hypervisor

        return info

    def get_security_info(self):
        """Get security features information"""
        info = {}

        # Security features
        security_features = []

        # SELinux status
        selinux_status = self.run_command("getenforce 2>/dev/null")
        if selinux_status:
            security_features.append(f"SELinux: {selinux_status}")

        # AppArmor status
        apparmor_status = self.run_command("sudo apparmor_status 2>/dev/null | head -5")
        if apparmor_status:
            security_features.append(f"AppArmor: Active")

        # Firewall status
        ufw_status = self.run_command("sudo ufw status 2>/dev/null")
        if ufw_status:
            security_features.append(f"UFW Firewall: {ufw_status.split(':')[-1].strip() if ':' in ufw_status else ufw_status}")

        # CPU security mitigations
        mitigations = self.read_file_safe('/proc/cpuinfo')
        if 'bugs' in mitigations:
            bugs_line = [line for line in mitigations.split('\n') if 'bugs' in line]
            if bugs_line:
                security_features.append(f"CPU Security Bugs: {bugs_line[0].split(':', 1)[1].strip()}")

        if security_features:
            info['Security Features'] = '\n'.join(security_features)

        return info

    def get_firmware_info(self):
        """Get firmware information"""
        info = {}

        # UEFI/BIOS information
        firmware_info = []

        # Boot mode
        if os.path.exists('/sys/firmware/efi'):
            firmware_info.append("Boot Mode: UEFI")

            # EFI variables
            efi_vars = self.run_command("ls /sys/firmware/efi/efivars 2>/dev/null | wc -l")
            if efi_vars and efi_vars.isdigit():
                firmware_info.append(f"EFI Variables: {efi_vars}")
        else:
            firmware_info.append("Boot Mode: Legacy BIOS")

        # Secure Boot status
        secure_boot = self.run_command("mokutil --sb-state 2>/dev/null")
        if secure_boot:
            firmware_info.append(f"Secure Boot: {secure_boot}")

        if firmware_info:
            info['Firmware Information'] = '\n'.join(firmware_info)

        return info

    def get_hardware_summary(self):
        """Get comprehensive hardware summary"""
        summary = {}

        try:
            # Collect all hardware information
            summary['Motherboard'] = self.get_motherboard_info()
            summary['CPU Details'] = self.get_cpu_detailed_info()
            summary['Memory Details'] = self.get_memory_detailed_info()
            summary['Storage Details'] = self.get_storage_detailed_info()
            summary['Network Details'] = self.get_network_detailed_info()
            summary['Graphics Details'] = self.get_graphics_detailed_info()
            summary['USB Devices'] = self.get_usb_devices()
            summary['PCI Devices'] = self.get_pci_devices()
            summary['Audio Devices'] = self.get_audio_info()
            summary['Sensors'] = self.get_sensors_info()
            summary['Power Management'] = self.get_power_info()
            summary['Kernel Modules'] = self.get_kernel_modules()
            summary['Virtualization'] = self.get_virtualization_info()
            summary['Security'] = self.get_security_info()
            summary['Firmware'] = self.get_firmware_info()

        except Exception as e:
            summary['Error'] = f"Error collecting hardware information: {str(e)}"

        return summary

    def format_hardware_info(self, category_name, hardware_data):
        """Format hardware information for display"""
        if not hardware_data:
            return f"{category_name}: No information available\n"

        output = [f"\n{'='*20} {category_name.upper()} {'='*20}"]

        for key, value in hardware_data.items():
            if isinstance(value, dict):
                output.append(f"\n{key}:")
                for subkey, subvalue in value.items():
                    output.append(f"  {subkey}: {subvalue}")
            else:
                output.append(f"\n{key}:")
                # Handle multi-line values
                if '\n' in str(value):
                    for line in str(value).split('\n'):
                        if line.strip():
                            output.append(f"  {line}")
                else:
                    output.append(f"  {value}")

        return '\n'.join(output) + '\n'

    def save_hardware_report(self, filename="hardware_report.txt"):
        """Save complete hardware report to file"""
        try:
            hardware_data = self.get_hardware_summary()

            with open(filename, 'w') as f:
                f.write(f"Hardware Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("="*80 + "\n\n")

                for category, data in hardware_data.items():
                    f.write(self.format_hardware_info(category, data))
                    f.write("\n")

            return f"Hardware report saved to: {filename}"

        except Exception as e:
            return f"Error saving report: {str(e)}"

# Test function
def test_hardware_detector():
    """Test the hardware detector"""
    detector = HardwareDetector()

    print("Testing Hardware Detector...")
    print("=" * 40)

    # Test motherboard detection
    mb_info = detector.get_motherboard_info()
    print("Motherboard Info:", mb_info)

    # Test CPU detection
    cpu_info = detector.get_cpu_detailed_info()
    print("\nCPU Info:", cpu_info)

    # Test memory detection
    mem_info = detector.get_memory_detailed_info()
    print("\nMemory Info:", mem_info)

if __name__ == "__main__":
    test_hardware_detector()
