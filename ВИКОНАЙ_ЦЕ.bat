@echo off
chcp 65001 >nul
echo ========================================
echo   Налаштування "Розумний Агент"
echo ========================================
echo.

REM Перехід до папки скрипта
cd /d "%~dp0"

REM Перевірка Python
echo [1/5] Перевірка Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ✗ Python не знайдено! Встановіть Python 3.9+
    pause
    exit /b 1
)
echo ✓ Python знайдено
echo.

REM Встановлення залежностей
echo [2/5] Встановлення залежностей...
python -m pip install --upgrade pip --quiet
python -m pip install -r requirements.txt
if errorlevel 1 (
    echo ✗ Помилка встановлення залежностей
    pause
    exit /b 1
)
echo ✓ Залежності встановлено
echo.

REM Перевірка конфігурації
echo [3/5] Перевірка конфігурації...
if not exist "auto_config.json" (
    echo ⚠ auto_config.json не знайдено!
    if exist "auto_config.example.json" (
        copy "auto_config.example.json" "auto_config.json" >nul
        echo ✓ Створено auto_config.json з прикладу
        echo ⚠ ВАЖЛИВО: Відредагуйте auto_config.json та додайте ваші credentials!
        echo.
        pause
    ) else (
        echo ✗ auto_config.example.json не знайдено!
        pause
        exit /b 1
    )
) else (
    echo ✓ auto_config.json знайдено
)

if not exist "service_account.json" (
    echo ⚠ service_account.json не знайдено!
    echo   Завантажте service_account.json з Google Cloud Console
)
echo.

REM Запуск налаштування
echo [4/5] Запуск автоматичного налаштування...
echo.
python auto_setup.py

echo.
echo ========================================
echo   Налаштування завершено!
echo ========================================
pause

