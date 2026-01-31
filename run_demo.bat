@echo off
title Geo-Intelligent Demo (Portable)
cd /d "%~dp0"

IF NOT EXIST "python_env\python.exe" (
    echo [ERROR] Please run start_server.bat first to set up the environment!
    pause
    exit /b
)

"python_env\python.exe" demo_scenario.py
pause
