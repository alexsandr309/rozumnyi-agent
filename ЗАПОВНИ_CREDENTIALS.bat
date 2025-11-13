@echo off
chcp 65001 >nul
title Заповнення Credentials - Розумний Агент

echo.
echo ========================================
echo   Автоматичне заповнення Credentials
echo ========================================
echo.

cd /d "%~dp0"

REM Перевірка Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [✗] Python не знайдено!
    pause
    exit /b 1
)

REM Запуск PowerShell скрипта
powershell.exe -ExecutionPolicy Bypass -File "ЗАПОВНИ_CREDENTIALS.ps1"

pause

