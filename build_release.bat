@echo off
cd /d "%~dp0"

echo Activating Environment...
call venv\Scripts\activate

echo.
echo --- Clean old builds ---
if exist "Arcadia.spec" del "Arcadia.spec"
if exist "ArcadiaServer.spec" del "ArcadiaServer.spec"
if exist "build" rmdir /S /Q "build"
if exist "dist" rmdir /S /Q "dist"

echo.
echo --- BUILDING FRONTEND ---
pyinstaller --noconfirm --onedir --windowed --name "Arcadia" --distpath "dist" --contents-directory "internal" src/frontend/main.py

echo.
echo --- BUILDING SERVER ---
pyinstaller --noconfirm --onedir --console --name "ArcadiaServer" --distpath "dist" --contents-directory "internal" src/web/server.py

echo.
echo --- MERGING and COPYING ASSETS ---
xcopy /E /I /Y "dist\ArcadiaServer\*" "dist\Arcadia\"
rmdir /S /Q "dist\ArcadiaServer"

xcopy /E /I /Y "themes" "dist\Arcadia\themes"

echo.
echo --- CLEANING UP ---
if exist "Arcadia.spec" del "Arcadia.spec"
if exist "ArcadiaServer.spec" del "ArcadiaServer.spec"
if exist "build" rmdir /S /Q "build"

echo.
echo BUILD COMPLETE!
echo Your release is located in: dist\Arcadia

pause
