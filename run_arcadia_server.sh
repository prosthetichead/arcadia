#!/bin/bash
cd "$(dirname "$0")"
echo "Starting Arcadia Server..."
./venv/bin/python -m web.server