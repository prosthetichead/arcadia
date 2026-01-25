REM This is for local windows testing only
REM Navigate to current folder
cd /d "%~dp0"

REM Launch Arcadia using 'pythonw.exe' (No Terminal)
REM The 'start ""' command tells the bat file to launch it and NOT wait.
start "" "venv\Scripts\pythonw.exe" src/main.py

REM Close this terminal immediately
exit