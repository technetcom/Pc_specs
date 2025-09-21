# System Specifications GUI

A comprehensive GUI application for displaying detailed computer specifications on Linux Debian systems. This application provides an intuitive tabbed interface to view system information including CPU, memory, storage, network, graphics, and running processes.

![System Specifications GUI](https://img.shields.io/badge/Platform-Linux%20Debian-blue)
![Python](https://img.shields.io/badge/Python-3.6%2B-green)
![GUI](https://img.shields.io/badge/GUI-Tkinter-orange)

## Features

- **System Information**: OS details, kernel version, uptime, distribution info
- **CPU Information**: Core count, frequency, usage per core, detailed processor info
- **Memory Information**: RAM usage, swap usage, detailed memory statistics
- **Storage Information**: Disk partitions, usage statistics, block devices
- **Network Information**: Network interfaces, IP addresses, MAC addresses, statistics
- **Graphics Information**: GPU details, OpenGL info, display configuration
- **Process Monitor**: Top processes by CPU usage, memory consumption
- **Real-time Updates**: Refresh button to update all information
- **Tabbed Interface**: Organized display with easy navigation

## Screenshots

The application features a clean, tabbed interface that displays:
- System overview with OS and kernel information
- Detailed CPU specifications and real-time usage
- Memory usage with visual indicators
- Storage devices and partition information
- Network interface details and statistics
- Graphics card and display information
- Running processes sorted by resource usage

## Prerequisites

- Linux Debian or Ubuntu-based system
- Python 3.6 or higher
- Root/sudo access for installation

## Quick Installation

1. Clone or download this repository
2. Navigate to the project directory
3. Run the installation script:

```bash
chmod +x install.sh
./install.sh
```

4. Launch the application:

```bash
./run.sh
```

## Manual Installation

If you prefer to install manually:

### 1. Install System Dependencies

```bash
# Update package list
sudo apt update

# Install required packages
sudo apt install -y python3 python3-pip python3-tk python3-venv

# Install optional packages for enhanced functionality
sudo apt install -y lshw mesa-utils x11-utils lsb-release
```

### 2. Set Up Python Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Run the Application

```bash
# Make sure you're in the project directory
# and virtual environment is activated
python3 system_specs_gui.py
```

## Usage

### Running the Application

After installation, you can run the application in several ways:

1. **Using the run script** (recommended):
   ```bash
   ./run.sh
   ```

2. **Direct execution**:
   ```bash
   source venv/bin/activate
   python3 system_specs_gui.py
   ```

3. **From applications menu** (if desktop entry was installed)

### Navigation

- Use the tabs at the top to navigate between different information categories
- Click "Refresh All Data" button to update all information with current values
- Scroll within each tab to view complete information
- All information is read-only for safety

### Information Categories

1. **System Info**: Operating system, kernel, distribution, uptime
2. **CPU**: Processor details, core count, frequency, usage statistics
3. **Memory**: RAM and swap usage, detailed memory information
4. **Storage**: Disk partitions, storage devices, usage statistics
5. **Network**: Network interfaces, IP addresses, connection statistics
6. **Graphics**: GPU information, OpenGL details, display configuration
7. **Processes**: Running processes sorted by resource usage

## Dependencies

### System Dependencies
- `python3`: Python interpreter
- `python3-tk`: Tkinter GUI library
- `python3-pip`: Python package installer
- `python3-venv`: Virtual environment support

### Optional System Dependencies
- `lshw`: Hardware information tool
- `mesa-utils`: OpenGL utilities (for graphics info)
- `x11-utils`: X11 utilities (for display info)
- `lsb-release`: Distribution information

### Python Dependencies
- `psutil`: System and process utilities

## Troubleshooting

### Common Issues

1. **Permission denied errors**:
   - Some system information requires elevated privileges
   - The application will show "Permission denied" for inaccessible information
   - This is normal and doesn't affect other functionality

2. **Missing graphics information**:
   - Install mesa-utils: `sudo apt install mesa-utils`
   - Some graphics info requires X11 session

3. **Application won't start**:
   - Check Python 3 installation: `python3 --version`
   - Verify tkinter is available: `python3 -c "import tkinter"`
   - Make sure virtual environment is activated

4. **Virtual environment issues**:
   - Delete the venv directory and run install.sh again
   - Ensure python3-venv is installed

### Error Messages

- **"glxinfo not available"**: Install mesa-utils package
- **"xrandr not available"**: Install x11-utils package or run in X11 session
- **"Command timed out"**: Some system commands may take time; try refreshing

## Development

### Project Structure

```
rastland/
├── system_specs_gui.py    # Main application file
├── requirements.txt       # Python dependencies
├── install.sh            # Installation script
├── run.sh               # Application launcher
├── README.md            # This file
└── venv/                # Virtual environment (created during installation)
```

### Customization

You can modify the application by editing `system_specs_gui.py`:

- Add new tabs by creating new methods following the pattern `create_*_tab()`
- Add new information gathering methods following the pattern `get_*_info()`
- Modify the refresh functionality in `refresh_all_data()`
- Customize the GUI layout and styling

### Adding New Information

To add a new information category:

1. Create a new tab creation method
2. Create a corresponding information gathering method
3. Add the tab creation to `__init__`
4. Add the data refresh to `refresh_all_data`

## Security Notes

- The application only reads system information
- No system modifications are performed
- Some information requires reading system files (read-only access)
- Network statistics are gathered locally (no external connections)

## Compatibility

- **Tested on**: Debian 11, Ubuntu 20.04+, Linux Mint 20+
- **Python**: 3.6, 3.7, 3.8, 3.9, 3.10, 3.11
- **Desktop Environment**: Works with GNOME, KDE, XFCE, and others

## License

This project is open source. Feel free to modify and distribute according to your needs.

## Contributing

Contributions are welcome! Please feel free to submit issues, feature requests, or pull requests.

## Support

If you encounter any issues:

1. Check the troubleshooting section above
2. Verify all dependencies are installed
3. Make sure you're running on a supported Linux distribution
4. Check that you have necessary permissions for system information access

---

**Note**: This application is designed specifically for Linux systems and will not work on Windows or macOS without significant modifications.