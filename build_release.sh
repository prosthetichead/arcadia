#!/bin/bash
cd "$(dirname "$0")"

echo "Activating Environment..."
source venv/bin/activate

echo ""
echo "--- BUILDING FRONTEND ---"
pyinstaller --noconfirm --onedir --windowed --name "Arcadia" --distpath "dist" --contents-directory "internal" src/frontend/main.py

echo ""
echo "--- BUILDING SERVER ---"
pyinstaller --noconfirm --onedir --console --name "ArcadiaServer" --distpath "dist" --contents-directory "internal" src/web/server.py

echo ""
echo "--- MERGING & COPYING ASSETS ---"
# Move Server exe to the main Arcadia folder
cp -r dist/ArcadiaServer/* dist/Arcadia/
rm -rf dist/ArcadiaServer

# Copy external assets
cp -r themes dist/Arcadia/themes

echo ""
echo "BUILD COMPLETE!"
echo "Your release is located in: dist/Arcadia"

# Clean up spec files
rm -f Arcadia.spec ArcadiaServer.spec

# Clean up build folder
rm -rf build