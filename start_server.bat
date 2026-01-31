@echo off
title Geo-Intelligent Server (Portable)
cd /d "%~dp0"

IF NOT EXIST "python_env\python.exe" (
    echo [INFO] Python environment not found. Setting up Portable Python...
    echo [INFO] This might take a minute...
    powershell -ExecutionPolicy Bypass -File setup_portable.ps1
)

IF NOT EXIST "python_env\python.exe" (
    echo [ERROR] Setup failed. Could not create portable python.
    pause
    exit /b
)

echo.
echo [INFO] Starting Server using Local Python...
echo [INFO] Access at http://localhost:5000
echo.
"python_env\python.exe" app/app.py
pause
