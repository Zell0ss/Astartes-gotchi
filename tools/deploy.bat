@echo off
REM Astartes-Gotchi deployment script for Windows

SET PORT=%1
IF "%PORT%"=="" SET PORT=COM3

echo ================================================
echo    ASTARTES-GOTCHI DEPLOYMENT
echo    For the Emperor!
echo ================================================
echo.
echo Target device: %PORT%
echo Source: src\
echo.

REM Check if mpremote is available
where mpremote >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: mpremote not found
    echo Install with: pip install mpremote
    exit /b 1
)

REM Check if src directory exists
if not exist "src\" (
    echo ERROR: src\ directory not found
    echo Run this script from project root
    exit /b 1
)

echo Uploading files to M5Stack Core2...
echo.

REM Upload all files from src/ to device root
mpremote connect %PORT% cp -r src/* :

if %ERRORLEVEL% EQU 0 (
    echo.
    echo Upload complete
    echo.
    echo Resetting device...

    REM Soft reset
    mpremote connect %PORT% exec "import machine; machine.soft_reset()"

    echo.
    echo ================================================
    echo    Device ready. For the Emperor!
    echo ================================================
) else (
    echo.
    echo Upload failed. Check connection and port.
    echo Try checking Device Manager for COM port.
    exit /b 1
)
