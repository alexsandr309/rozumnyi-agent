# PowerShell скрипт для автоматичного налаштування "Розумний Агент"
# Просто скопіюйте та виконайте команди з цього файлу в PowerShell

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Налаштування 'Розумний Агент'" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Крок 1: Перевірка Python
Write-Host "[1/5] Перевірка Python..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Python знайдено: $pythonVersion" -ForegroundColor Green
} else {
    Write-Host "✗ Python не знайдено! Встановіть Python 3.9+ з python.org" -ForegroundColor Red
    exit 1
}

# Крок 2: Перехід до папки проєкту
Write-Host ""
Write-Host "[2/5] Перехід до папки проєкту..." -ForegroundColor Yellow
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptPath
Write-Host "✓ Поточна папка: $(Get-Location)" -ForegroundColor Green

# Крок 3: Встановлення залежностей
Write-Host ""
Write-Host "[3/5] Встановлення залежностей..." -ForegroundColor Yellow
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Залежності встановлено" -ForegroundColor Green
} else {
    Write-Host "✗ Помилка встановлення залежностей" -ForegroundColor Red
    exit 1
}

# Крок 4: Перевірка конфігурації
Write-Host ""
Write-Host "[4/5] Перевірка конфігурації..." -ForegroundColor Yellow
if (Test-Path "auto_config.json") {
    Write-Host "✓ auto_config.json знайдено" -ForegroundColor Green
} else {
    Write-Host "⚠ auto_config.json не знайдено!" -ForegroundColor Yellow
    Write-Host "  Створіть файл auto_config.json з credentials" -ForegroundColor Yellow
    Write-Host "  (скопіюйте auto_config.example.json та заповніть)" -ForegroundColor Yellow
    if (Test-Path "auto_config.example.json") {
        Copy-Item "auto_config.example.json" "auto_config.json"
        Write-Host "  ✓ Створено auto_config.json з прикладу" -ForegroundColor Green
        Write-Host "  ⚠ ВАЖЛИВО: Відредагуйте auto_config.json та додайте ваші credentials!" -ForegroundColor Red
        Write-Host ""
        Write-Host "Натисніть будь-яку клавішу після заповнення auto_config.json..." -ForegroundColor Yellow
        $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    }
}

if (Test-Path "service_account.json") {
    Write-Host "✓ service_account.json знайдено" -ForegroundColor Green
} else {
    Write-Host "⚠ service_account.json не знайдено!" -ForegroundColor Yellow
    Write-Host "  Завантажте service_account.json з Google Cloud Console" -ForegroundColor Yellow
    Write-Host "  (див. GOOGLE_DRIVE_SETUP.md)" -ForegroundColor Yellow
}

# Крок 5: Запуск автоматичного налаштування
Write-Host ""
Write-Host "[5/5] Запуск автоматичного налаштування..." -ForegroundColor Yellow
Write-Host ""
if (Test-Path "auto_config.json") {
    python auto_setup.py
} else {
    Write-Host "✗ Не можу запустити без auto_config.json" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  Налаштування завершено!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green

