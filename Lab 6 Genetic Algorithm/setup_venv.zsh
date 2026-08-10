#!/bin/zsh

git config --global core.excludesfile ~/.gitignore_global
echo ".DS_Store" >> ~/.gitignore_global

# Create a Python virtual environment named .venv
python3 -m venv .venv

# Activate the virtual environment
source .venv/bin/activate

# Show the Python version being used
python --version

echo "Virtual environment activated, aayush :)"