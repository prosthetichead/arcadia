#!/bin/bash
cd "$(dirname "$0")"

if [ ! -d "venv" ]; then
    echo "Creating Python Virtual Environment..."
    python3 -m venv venv
fi

echo "Activating Virtual Environment..."
source venv/bin/activate

echo "Installing Dependencies..."
pip install -e .

echo ""
echo "Setup Complete!"