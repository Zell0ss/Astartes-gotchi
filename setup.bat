@echo off
REM Astartes-Gotchi - Development Environment Setup (Windows)
REM Run this script once to set up your development environment

echo ================================================================
echo.
echo              ASTARTES-GOTCHI SETUP
echo.
echo ================================================================
echo.

REM Check Python
echo Checking Python version...
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Python not found. Please install Python 3.7 or higher.
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo Found Python %PYTHON_VERSION%

REM Create virtual environment
echo.
echo Creating virtual environment...
if exist ".venv\" (
    echo .venv already exists, skipping...
) else (
    python -m venv .venv
    echo Virtual environment created
)

REM Activate venv
echo.
echo Activating virtual environment...
call .venv\Scripts\activate.bat

REM Upgrade pip
echo.
echo Upgrading pip...
python -m pip install --upgrade pip -q

REM Install requirements
echo.
echo Installing requirements...
pip install -r requirements.txt

echo.
echo Setup complete!
echo.
echo ================================================================
echo                      NEXT STEPS
echo ================================================================
echo.
echo  1. Activate environment:
echo     .venv\Scripts\activate.bat
echo.
echo  2. Flash MicroPython (first time only):
echo     See SETUP_MICROPYTHON.md
echo.
echo  3. Deploy to device:
echo     tools\deploy.bat COM3
echo.
echo  4. Run tests (optional):
echo     python tests\test_marine.py
echo.
echo ================================================================
echo.
echo For the Emperor!
pause
