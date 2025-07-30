@echo off
title Epoch Status Webhook Monitor
cd /d "%~dp0"

echo Creating/checking Python virtual environment...

if not exist "venv" (
    echo Creating new virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo Error: Failed to create virtual environment.
        echo Make sure Python is installed and available in PATH.
        echo.
        pause
        exit /b 1
    )
    echo Virtual environment created successfully!
) else (
    echo Virtual environment already exists.
)

echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

if errorlevel 1 (
    echo Error: Failed to activate virtual environment.
    echo.
    pause
    exit /b 1
)

echo.
echo Installing/updating dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt

if errorlevel 1 (
    echo Error: Failed to install dependencies.
    echo.
    pause
    exit /b 1
)

echo.
echo Starting Epoch Status Webhook Monitor...
echo Virtual environment: %VIRTUAL_ENV%
echo.
python epoch_webhook.py

echo.
echo Deactivating virtual environment...
deactivate
echo.
pause
