@echo off
REM Quick Start Script for WillPay POS System (Windows)

echo ===========================================
echo   Granny's Waffle - WillPay POS System
echo ===========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

echo [OK] Python found
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
    echo [OK] Virtual environment created
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install requirements
echo Installing requirements...
pip install -q --upgrade pip
pip install -q -r requirements.txt
echo [OK] Requirements installed
echo.

REM Start backend in background
echo Starting backend server...
start /B python backend.py
echo [OK] Backend server started
echo.

REM Wait for backend to initialize
echo Waiting for backend to initialize...
timeout /t 3 /nobreak >nul

REM Start POS UI
echo Starting POS UI...
python pos_ui.py

echo.
echo Thank you for using WillPay POS!
pause

