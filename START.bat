@echo off
title Quiz App - Launcher
color 0B

echo.
echo  =====================================================
echo   ⚡  QUIZ APP PRO - Auto Setup and Launcher
echo  =====================================================
echo.

REM Check Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    color 0C
    echo  [ERROR] Python is not installed or not in PATH.
    echo.
    echo  Please download Python from: https://www.python.org/downloads/
    echo  Make sure to check "Add Python to PATH" during install.
    echo.
    pause
    exit /b
)

echo  [OK] Python found.

REM Install Flask
echo  [..] Installing Flask (this may take a moment)...
pip install flask --quiet 2>&1
if errorlevel 1 (
    color 0C
    echo  [ERROR] Failed to install Flask. Check your internet connection.
    pause
    exit /b
)
echo  [OK] Flask is ready.

REM Move into the quiz_app folder if we are not already inside it
if exist app.py (
    REM Already inside quiz_app folder
) else if exist quiz_app\app.py (
    cd quiz_app
) else (
    color 0C
    echo  [ERROR] Cannot find app.py.
    echo  Place this .bat file inside the quiz_app folder and try again.
    pause
    exit /b
)

echo.
echo  =====================================================
echo   Starting Quiz App...
echo  =====================================================
echo.
echo  Open your browser and go to:
echo.
echo       http://127.0.0.1:5000
echo.
echo  Admin Login  ^|  Username: admin   Password: admin123
echo  Students     ^|  Register at http://127.0.0.1:5000/register
echo.
echo  Press Ctrl+C in this window to stop the server.
echo  =====================================================
echo.

REM Open browser automatically after 2 seconds
start "" timeout /t 2 >nul
start "" "http://127.0.0.1:5000"

REM Start Flask app
python app.py

pause
