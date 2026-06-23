#!/bin/bash
# Setup script for Linux/macOS
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
echo "Environment setup complete. To activate in the future, run: source venv/bin/activate"
