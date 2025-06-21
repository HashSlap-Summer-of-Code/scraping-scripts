#!/usr/bin/env python3
"""
Setup script for Events Aggregator
Creates necessary directories and installs dependencies
"""

import os
import subprocess
import sys
from pathlib import Path

def create_directory_structure():
    """Create the project directory structure"""
    dirs = [
        'output',
        'logs',
        'templates',
        'static/css',
        'static/js',
        'data'
    ]
    
    for dir_path in dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        print(f"✓ Created directory: {dir_path}")

def install_requirements():
    """Install required packages"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ Requirements installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"✗ Error installing requirements: {e}")
        return False
    return True

def create_config_file():
    """Create configuration file"""
    config_content = """# Events Aggregator Configuration

# Scraping settings
SCRAPING_DELAY = 2  # seconds between requests
MAX_EVENTS_PER_PLATFORM = 10
TIMEOUT = 10  # seconds

# Output settings
OUTPUT_DIR = "output"
LOG_LEVEL = "INFO"

# Platform settings
PLATFORMS = {
    "devpost": True,
    "mlh": True,
    "scaler": True,
    "unacademy": True
}

# HTML Dashboard settings
DASHBOARD_TITLE = "Events Dashboard"
DASHBOARD_SUBTITLE = "Discover the latest hackathons, bootcamps, and tech events"
"""
    
    with open('config.py', 'w') as f:
        f.write(config_content)
    print("✓ Created config.py")

def main():
    """Main setup function"""
    print("🚀 Setting up Events Aggregator...")
    print("=" * 50)
    
    # Create directory structure
    print("\n1. Creating directory structure...")
    create_directory_structure()
    
    # Install requirements
    print("\n2. Installing requirements...")
    if not install_requirements():
        print("⚠️  Failed to install requirements. Please run manually:")
        print("   pip install -r requirements.txt")
    
    # Create config file
    print("\n3. Creating configuration files...")
    create_config_file()
    
    print("\n" + "=" * 50)
    print("✅ Setup completed successfully!")
    print("\nTo run the events aggregator:")
    print("   python main.py")
    print("\nTo view the dashboard:")
    print("   Open output/index.html in your browser")

if __name__ == "__main__":
    main()