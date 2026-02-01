@echo off
cd /d "%~dp0"

if not exist "venv" (
    echo Creating Python Virtual Environment...
    python -m venv venv
)

echo Activating Virtual Environment...
call venv\Scripts\activate

echo Installing Dependencies...
pip install -e .
echo.
echo Setup Complete!
pause
