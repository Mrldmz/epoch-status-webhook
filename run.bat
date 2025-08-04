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
echo Checking configuration...

if not exist "config.txt" (
    echo Error: config.txt not found!
    echo Please create config.txt based on example-config.txt and configure your settings.
    echo.
    pause
    exit /b 1
)

:: Read status_website_url from config.txt
set "status_website_url="
for /f "usebackq tokens=1,2 delims==" %%a in ("config.txt") do (
    if "%%a"=="status_website_url" set "status_website_url=%%b"
)

:: Check if status_website_url is configured
if "%status_website_url%"=="" (
    echo Error: status_website_url is not configured in config.txt
    echo Please add the following line to config.txt:
    echo status_website_url=https://epoch-status.info/
    echo or
    echo status_website_url=https://epoch.strykersoft.us/
    echo.
    pause
    exit /b 1
)

:: Determine which script to run based on the URL
set "script_to_run="
if "%status_website_url%"=="https://epoch-status.info/" (
    set "script_to_run=epoch_info_webhook.py"
) else if "%status_website_url%"=="https://epoch.strykersoft.us/" (
    set "script_to_run=epoch_webhook.py"
) else (
    echo Error: Invalid status_website_url in config.txt
    echo Supported URLs:
    echo - https://epoch-status.info/
    echo - https://epoch.strykersoft.us/
    echo Current value: %status_website_url%
    echo.
    pause
    exit /b 1
)

echo Starting Epoch Status Webhook Monitor...
echo Virtual environment: %VIRTUAL_ENV%
echo Website URL: %status_website_url%
echo Script: %script_to_run%
echo.
python %script_to_run%

echo.
echo Deactivating virtual environment...
deactivate
echo.
pause
