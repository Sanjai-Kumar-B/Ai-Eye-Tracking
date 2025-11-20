@echo off
echo ========================================
echo     Eye Mouse Controller
echo ========================================
echo.
echo Starting application...
echo.

python main.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ========================================
    echo   Error: Application failed to start
    echo ========================================
    echo.
    echo Possible issues:
    echo   1. Python not installed or not in PATH
    echo   2. Dependencies not installed
    echo.
    echo Solutions:
    echo   1. Run "install_dependencies.bat" first
    echo   2. Check SETUP_GUIDE.md for instructions
    echo.
    pause
)
