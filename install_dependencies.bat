@echo off
echo ========================================
echo   Eye Mouse - Dependency Installer
echo ========================================
echo.
echo This will install all required packages...
echo Please wait, this may take 2-5 minutes.
echo.
pause

echo.
echo Installing dependencies...
echo.

pip install -r requirements.txt

echo.
echo ========================================
if %ERRORLEVEL% EQU 0 (
    echo   Installation Complete!
    echo ========================================
    echo.
    echo All dependencies installed successfully.
    echo You can now run the application by:
    echo   1. Double-clicking "run_eye_mouse.bat"
    echo   2. OR running "python main.py" in terminal
    echo.
) else (
    echo   Installation Failed!
    echo ========================================
    echo.
    echo Please check:
    echo   1. Python is installed and added to PATH
    echo   2. You have internet connection
    echo   3. You are running this as administrator
    echo.
    echo Try running this command manually:
    echo   pip install -r requirements.txt
    echo.
)

pause
