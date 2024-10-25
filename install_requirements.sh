#!/bin/bash

# Function to check if a command is installed
command_exists() {
    command -v "$1" &> /dev/null
}

# Check if Python3 is installed
if ! command_exists python3; then
    echo "Python3 is not installed. Please install Python3 and try again."
    exit 1
fi

# Check if pip is installed
if ! command_exists pip; then
    echo "pip is not installed. Please install pip and try again."
    exit 1
fi

# Check if Subfinder is installed
if ! command_exists subfinder; then
    echo "Subfinder is not installed. Installing Subfinder..."

    # Install Subfinder
    go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
    if [ $? -ne 0 ]; then
        echo "Failed to install Subfinder. Please install it manually."
        exit 1
    fi

    # Check if the binary exists in the expected go bin directory
    if [ -f "$HOME/go/bin/subfinder" ]; then
        echo "Subfinder installed in $HOME/go/bin."

        # Copy the subfinder binary to /usr/local/bin/ for system-wide use
        echo "Copying Subfinder to /usr/local/bin/..."
        sudo cp "$HOME/go/bin/subfinder" /usr/local/bin/
        if [ $? -ne 0 ]; then
            echo "Failed to copy Subfinder to /usr/local/bin/. Please check your permissions."
            exit 1
        fi
        echo "Subfinder successfully copied to /usr/local/bin/ and is now available for direct use."
    else
        echo "Subfinder binary not found in $HOME/go/bin/. Please ensure it was installed correctly."
        exit 1
    fi
else
    echo "Subfinder is already installed and available in the CLI."
fi

# Create a virtual environment
echo "Creating a virtual environment..."
python3 -m venv myenv

# Activate the virtual environment
source myenv/bin/activate

# Upgrade pip to the latest version
echo "Upgrading pip..."
pip install --upgrade pip

# Install required packages
echo "Installing required packages..."
pip install aiohttp requests

echo "All requirements installed successfully!"
echo "To activate the virtual environment, run: source myenv/bin/activate"
echo "To deactivate the virtual environment, run: deactivate"
