@echo off
REM Wardrobe AI Backend - Quick Setup Script for Windows

echo ================================================
echo   Wardrobe AI Backend - Quick Setup
echo ================================================
echo.

REM Check Python version
echo Checking Python version...
python --version

REM Create virtual environment
echo.
echo Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo.
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
echo.
echo Installing dependencies (this may take a few minutes)...
pip install -r requirements.txt

REM Create directories
echo.
echo Creating necessary directories...
if not exist "app\static\uploads" mkdir app\static\uploads
if not exist "app\static\generated" mkdir app\static\generated
if not exist "data\chroma_db" mkdir data\chroma_db

REM Create .env file if it doesn't exist
if not exist ".env" (
    echo.
    echo Creating .env file from template...
    copy .env.example .env
    echo Done: .env file created
    echo.
    echo WARNING: Please edit .env and add your OPENROUTER_API_KEY
    echo Get your key from: https://openrouter.ai/
) else (
    echo.
    echo Done: .env file already exists
)

REM Run basic tests
echo.
echo Running setup verification...
python test_basic.py

echo.
echo ================================================
echo   Setup Complete!
echo ================================================
echo.
echo Next steps:
echo 1. Edit .env and add your OPENROUTER_API_KEY
echo 2. Run: python run.py
echo 3. Visit: http://localhost:5000
echo.
echo For API examples, see: API_EXAMPLES.md
echo.

pause
