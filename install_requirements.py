"""
Auto-Install Script for Smart City Management System
This script automatically installs all required packages from requirements.txt
"""

import subprocess
import sys
import os
from pathlib import Path


def get_requirements_file():
    """Get the path to requirements.txt"""
    script_dir = Path(__file__).parent
    req_file = script_dir / "requirements.txt"
    return req_file


def check_venv():
    """Check if virtual environment exists"""
    venv_path = Path(__file__).parent / "venv"
    return venv_path.exists()


def install_requirements():
    """Install all packages from requirements.txt"""
    req_file = get_requirements_file()
    
    if not req_file.exists():
        print("❌ requirements.txt not found!")
        sys.exit(1)
    
    print("📦 Installing packages from requirements.txt...")
    print(f"📄 Requirements file: {req_file}\n")
    
    try:
        # Install packages using pip
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", str(req_file)],
            check=True
        )
        
        print("\n✅ All packages installed successfully!")
        print("\n📝 To activate the virtual environment, run:")
        print("   source venv/bin/activate  (Linux/Mac)")
        print("   venv\\Scripts\\activate     (Windows)")
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Installation failed with error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        sys.exit(1)


def main():
    """Main entry point"""
    print("=" * 50)
    print("Smart City Management System - Auto Installer")
    print("=" * 50)
    print()
    
    if not check_venv():
        print("⚠️  Virtual environment not found!")
        print("Creating virtual environment...")
        try:
            subprocess.run(
                [sys.executable, "-m", "venv", "venv"],
                cwd=Path(__file__).parent,
                check=True
            )
            print("✅ Virtual environment created!\n")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to create virtual environment: {e}")
            sys.exit(1)
    
    install_requirements()


if __name__ == "__main__":
    main()
