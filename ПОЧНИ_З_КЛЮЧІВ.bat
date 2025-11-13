@echo off
chcp 65001 >nul
title Інтерактивний Гайд - Отримання Ключів

echo.
echo ========================================
echo   ІНТЕРАКТИВНИЙ ГАЙД
echo   Отримання Всіх API Ключів
echo ========================================
echo.

cd /d "%~dp0"

REM Запуск PowerShell скрипта
powershell.exe -ExecutionPolicy Bypass -File "ІНТЕРАКТИВНИЙ_ГАЙД.ps1"

pause

