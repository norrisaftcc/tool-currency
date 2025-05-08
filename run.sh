#!/bin/bash
# Tool-Currency converter application launcher script

# Display header
echo "=================================================="
echo "  TOOL-CURRENCY CONVERTER - STARTUP SCRIPT"
echo "=================================================="

# Check for Python installation
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed or not in PATH."
    echo "Please install Python 3.7 or higher and try again."
    exit 1
fi

# Check if Streamlit is installed
if ! python3 -c "import streamlit" &> /dev/null; then
    echo "Streamlit not found. Make sure you've installed dependencies."
    echo "Would you like to install the required dependencies now? (y/n)"
    read -r answer
    if [ "$answer" == "y" ] || [ "$answer" == "Y" ]; then
        echo "Installing dependencies from requirements.txt..."
        pip install -r requirements.txt
        if [ $? -ne 0 ]; then
            echo "ERROR: Failed to install dependencies."
            echo "Please try running: pip install -r requirements.txt"
            exit 1
        fi
    else
        echo "Please install dependencies manually with: pip install -r requirements.txt"
        exit 1
    fi
fi

# Check if we're in a virtual environment
if [ -z "$VIRTUAL_ENV" ]; then
    # Not in a virtual environment - check if one exists
    if [ -d "venv" ]; then
        echo "Activating virtual environment..."
        # Source appropriate activation script based on OS
        if [ -f "venv/bin/activate" ]; then
            source venv/bin/activate
        elif [ -f "venv/Scripts/activate" ]; then
            source venv/Scripts/activate
        else
            echo "WARNING: Virtual environment exists but activation script not found."
        fi
    else
        echo "Note: Running without a virtual environment."
        echo "For best results, consider creating one with: python -m venv venv"
    fi
fi

# Check if data directory exists
if [ ! -d "data" ] || [ ! -f "data/currencies.json" ]; then
    echo "WARNING: Data directory or currency data file missing."
    echo "The application may not function correctly."
fi

# Run the Streamlit app
echo "Starting the currency converter app..."
streamlit run src/app.py

# Check exit status
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to start Streamlit application."
    echo "Please check that all dependencies are installed correctly."
    exit 1
fi