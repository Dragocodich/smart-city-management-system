#!/bin/bash
# Auto-Install Script for Smart City Management System (Linux/Mac)

echo "=================================================="
echo "Smart City Management System - Auto Installer"
echo "=================================================="
echo ""

# Get the script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Check if venv exists
if [ ! -d "$SCRIPT_DIR/venv" ]; then
    echo "⚠️  Virtual environment not found!"
    echo "Creating virtual environment..."
    python3 -m venv "$SCRIPT_DIR/venv"
    if [ $? -eq 0 ]; then
        echo "✅ Virtual environment created!"
        echo ""
    else
        echo "❌ Failed to create virtual environment"
        exit 1
    fi
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source "$SCRIPT_DIR/venv/bin/activate"

# Check if requirements.txt exists
if [ ! -f "$SCRIPT_DIR/requirements.txt" ]; then
    echo "❌ requirements.txt not found!"
    exit 1
fi

# Install packages
echo "📦 Installing packages from requirements.txt..."
echo "📄 Requirements file: $SCRIPT_DIR/requirements.txt"
echo ""

pip install -r "$SCRIPT_DIR/requirements.txt"

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ All packages installed successfully!"
    echo ""
    echo "📝 Virtual environment is now activated!"
    echo "   To run the application, execute:"
    echo "   python main.py"
else
    echo ""
    echo "❌ Installation failed!"
    exit 1
fi
