@echo off
chcp 65001 >nul
title Повна Автоматизація - Розумний Агент

echo.
echo ========================================
echo   ПОВНА АВТОМАТИЗАЦІЯ ПРОЄКТУ
echo ========================================
echo.

REM Перехід до папки скрипта
cd /d "%~dp0"
echo [✓] Поточна папка: %CD%
echo.

REM Перевірка Python
echo [1/8] Перевірка Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo   ✗ Python не знайдено! Встановіть Python 3.9+
    pause
    exit /b 1
)
python --version
echo   ✓ Python знайдено
echo.

REM Встановлення залежностей
echo [2/8] Встановлення залежностей...
python -m pip install --upgrade pip --quiet
python -m pip install -r requirements.txt
if errorlevel 1 (
    echo   ⚠ Помилка, спробую з --user...
    python -m pip install -r requirements.txt --user
)
echo   ✓ Залежності встановлено
echo.

REM Створення конфігурації
echo [3/8] Створення конфігураційних файлів...
if not exist "auto_config.json" (
    if exist "auto_config.example.json" (
        copy "auto_config.example.json" "auto_config.json" >nul
        echo   ✓ Створено auto_config.json
        echo   ⚠ ВАЖЛИВО: Додайте ваші credentials!
    ) else (
        echo   ⚠ auto_config.example.json не знайдено
    )
) else (
    echo   ✓ auto_config.json вже існує
)
echo.

REM Перевірка service_account.json
echo [4/8] Перевірка Google Drive credentials...
if exist "service_account.json" (
    echo   ✓ service_account.json знайдено
) else (
    echo   ⚠ service_account.json не знайдено
    echo     → Створіть Service Account у Google Cloud Console
    echo     → Див. GOOGLE_DRIVE_SETUP.md
)
echo.

REM Перевірка файлів
echo [5/8] Перевірка файлів проєкту...
if exist "app.py" (
    echo   ✓ app.py
) else (
    echo   ✗ app.py відсутній!
    pause
    exit /b 1
)
if exist "requirements.txt" (
    echo   ✓ requirements.txt
) else (
    echo   ✗ requirements.txt відсутній!
    pause
    exit /b 1
)
echo.

REM Перевірка конфігурації
echo [6/8] Перевірка конфігурації...
echo   → Перевіряю auto_config.json...
if exist "auto_config.json" (
    echo   ✓ Файл знайдено
    echo   ⚠ Перевірте, чи всі credentials додано!
) else (
    echo   ⚠ auto_config.json не знайдено
)
echo.

REM Запуск налаштування
echo [7/8] Запуск автоматичного налаштування...
echo.
python auto_setup.py
set SETUP_SUCCESS=%ERRORLEVEL%
echo.

REM Підсумок
echo [8/8] Підсумок...
echo.
if %SETUP_SUCCESS%==0 (
    echo ========================================
    echo   ✅ ВСЕ ГОТОВО!
    echo ========================================
    echo.
    echo Проєкт налаштовано та розгорнуто!
    echo.
    echo Наступні кроки:
    echo   1. Перевірте логи на платформі
    echo   2. Перевірте Keep-Alive ендпоінт
    echo   3. Перевірте UptimeRobot монітор
) else (
    echo ========================================
    echo   ⚠ Налаштування потребує уваги
    echo ========================================
    echo.
    echo Перевірте:
    echo   - Чи всі credentials додано
    echo   - Чи service_account.json завантажено
    echo   - Логи вище для деталей
)
echo.
pause

