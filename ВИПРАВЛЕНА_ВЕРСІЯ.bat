@echo off
chcp 65001 >nul
title Виправлена Версія - Розумний Агент

echo.
echo ========================================
echo   ВИПРАВЛЕНА ВЕРСІЯ - Встановлення
echo ========================================
echo.

cd /d "%~dp0"
echo [✓] Поточна папка: %CD%
echo.

echo [1/4] Оновлення pip...
python -m pip install --upgrade pip --quiet
echo   ✓ pip оновлено
echo.

echo [2/4] Встановлення основних пакетів...
python -m pip install Flask==3.0.3 gunicorn==21.2.0 ccxt==4.3.75 --quiet
echo   ✓ Основні пакети встановлено
echo.

echo [3/4] Встановлення pandas та numpy...
python -m pip install pandas numpy --upgrade --quiet
echo   ✓ pandas та numpy встановлено
echo.

echo [4/4] Встановлення TensorFlow (може зайняти час)...
python -m pip install tensorflow --upgrade --quiet
echo   ✓ TensorFlow встановлено
echo.

echo [5/5] Встановлення Google API пакетів...
python -m pip install google-api-python-client google-auth google-auth-oauthlib google-auth-httplib2 httplib2 python-dotenv requests --quiet
echo   ✓ Google API пакети встановлено
echo.

echo ========================================
echo   Перевірка встановлення...
echo ========================================
echo.

python -c "import flask; print('✓ Flask')" 2>nul || echo ✗ Flask
python -c "import ccxt; print('✓ ccxt')" 2>nul || echo ✗ ccxt
python -c "import pandas; print('✓ pandas')" 2>nul || echo ✗ pandas
python -c "import numpy; print('✓ numpy')" 2>nul || echo ✗ numpy
python -c "import tensorflow; print('✓ tensorflow')" 2>nul || echo ✗ tensorflow
python -c "import requests; print('✓ requests')" 2>nul || echo ✗ requests

echo.
echo ========================================
echo   ✅ ВСТАНОВЛЕННЯ ЗАВЕРШЕНО!
echo ========================================
echo.

if not exist "auto_config.json" (
    if exist "auto_config.example.json" (
        copy "auto_config.example.json" "auto_config.json" >nul
        echo ⚠ Створено auto_config.json
        echo ⚠ ВАЖЛИВО: Додайте ваші credentials!
        echo.
        notepad auto_config.json
    )
)

if not exist "service_account.json" (
    echo ⚠ service_account.json не знайдено
    echo   → Створіть Service Account у Google Cloud Console
    echo   → Див. GOOGLE_DRIVE_SETUP.md
    echo.
)

echo Готово до запуску налаштування!
echo Запустіть: python auto_setup.py
echo.
pause

