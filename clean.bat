@echo off
title Clean Virtual Environment
cd /d "%~dp0"

echo This will delete the virtual environment folder.
echo You'll need to run setup again next time.
echo.
set /p confirm="Are you sure? (y/N): "

if /i "%confirm%"=="y" (
    echo.
    echo Removing virtual environment...
    if exist "venv" (
        rmdir /s /q "venv"
        echo Virtual environment removed successfully!
    ) else (
        echo No virtual environment found.
    )
) else (
    echo Operation cancelled.
)

echo.
pause
