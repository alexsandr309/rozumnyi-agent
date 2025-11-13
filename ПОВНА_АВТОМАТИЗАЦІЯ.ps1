# Повна автоматизація проєкту "Розумний Агент"
# Цей скрипт зробить ВСЕ автоматично, наскільки це можливо

$ErrorActionPreference = "Stop"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  ПОВНА АВТОМАТИЗАЦІЯ ПРОЄКТУ" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Перехід до папки скрипта
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptPath
Write-Host "[✓] Поточна папка: $(Get-Location)" -ForegroundColor Green
Write-Host ""

# ========================================
# КРОК 1: Перевірка та встановлення Python
# ========================================
Write-Host "[1/8] Перевірка Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "  ✓ Python знайдено: $pythonVersion" -ForegroundColor Green
    
    # Перевірка версії
    $versionMatch = $pythonVersion -match "Python (\d+)\.(\d+)"
    if ($versionMatch) {
        $major = [int]$matches[1]
        $minor = [int]$matches[2]
        if ($major -lt 3 -or ($major -eq 3 -and $minor -lt 9)) {
            Write-Host "  ✗ Потрібен Python 3.9+ (зараз $major.$minor)" -ForegroundColor Red
            exit 1
        }
    }
} catch {
    Write-Host "  ✗ Python не знайдено! Встановіть Python 3.9+ з python.org" -ForegroundColor Red
    exit 1
}
Write-Host ""

# ========================================
# КРОК 2: Встановлення залежностей
# ========================================
Write-Host "[2/8] Встановлення залежностей..." -ForegroundColor Yellow
try {
    Write-Host "  → Оновлення pip..." -ForegroundColor Gray
    python -m pip install --upgrade pip --quiet
    
    Write-Host "  → Встановлення пакетів з requirements.txt..." -ForegroundColor Gray
    python -m pip install -r requirements.txt --quiet
    
    Write-Host "  ✓ Всі залежності встановлено" -ForegroundColor Green
} catch {
    Write-Host "  ⚠ Помилка встановлення, спробую з --user..." -ForegroundColor Yellow
    python -m pip install -r requirements.txt --user
    Write-Host "  ✓ Залежності встановлено (--user)" -ForegroundColor Green
}
Write-Host ""

# ========================================
# КРОК 3: Створення конфігураційних файлів
# ========================================
Write-Host "[3/8] Створення конфігураційних файлів..." -ForegroundColor Yellow

# auto_config.json
if (-not (Test-Path "auto_config.json")) {
    if (Test-Path "auto_config.example.json") {
        Copy-Item "auto_config.example.json" "auto_config.json"
        Write-Host "  ✓ Створено auto_config.json з прикладу" -ForegroundColor Green
        Write-Host "  ⚠ ВАЖЛИВО: Потрібно додати ваші credentials!" -ForegroundColor Yellow
    } else {
        # Створюємо базовий файл
        $basicConfig = @{
            platform = "render"
            binance = @{
                testnet_api_key = ""
                testnet_secret_key = ""
            }
            github = @{
                username = ""
                token = ""
                repo_name = "розумний-агент"
            }
            render = @{
                api_key = ""
            }
            replit = @{
                api_token = ""
                username = ""
                repl_name = "розумний-агент"
            }
            uptimerobot = @{
                api_key = ""
            }
            trading = @{
                mode = "BALANCED"
                deposit_usdt = 1000
            }
        } | ConvertTo-Json -Depth 10
        
        $basicConfig | Out-File "auto_config.json" -Encoding UTF8
        Write-Host "  ✓ Створено базовий auto_config.json" -ForegroundColor Green
    }
} else {
    Write-Host "  ✓ auto_config.json вже існує" -ForegroundColor Green
}

# .env файл (якщо потрібно)
if (-not (Test-Path ".env") -and (Test-Path "env.example")) {
    Copy-Item "env.example" ".env"
    Write-Host "  ✓ Створено .env з прикладу" -ForegroundColor Green
}
Write-Host ""

# ========================================
# КРОК 4: Перевірка service_account.json
# ========================================
Write-Host "[4/8] Перевірка Google Drive credentials..." -ForegroundColor Yellow
if (Test-Path "service_account.json") {
    Write-Host "  ✓ service_account.json знайдено" -ForegroundColor Green
} else {
    Write-Host "  ⚠ service_account.json не знайдено" -ForegroundColor Yellow
    Write-Host "    → Створіть Service Account у Google Cloud Console" -ForegroundColor Gray
    Write-Host "    → Завантажте JSON ключ як service_account.json" -ForegroundColor Gray
    Write-Host "    → Див. GOOGLE_DRIVE_SETUP.md для деталей" -ForegroundColor Gray
}
Write-Host ""

# ========================================
# КРОК 5: Перевірка наявності всіх файлів
# ========================================
Write-Host "[5/8] Перевірка файлів проєкту..." -ForegroundColor Yellow
$requiredFiles = @("app.py", "requirements.txt")
$missingFiles = @()

foreach ($file in $requiredFiles) {
    if (Test-Path $file) {
        Write-Host "  ✓ $file" -ForegroundColor Green
    } else {
        Write-Host "  ✗ $file відсутній!" -ForegroundColor Red
        $missingFiles += $file
    }
}

if ($missingFiles.Count -gt 0) {
    Write-Host "  ✗ Відсутні критичні файли!" -ForegroundColor Red
    exit 1
}
Write-Host ""

# ========================================
# КРОК 6: Перевірка конфігурації
# ========================================
Write-Host "[6/8] Перевірка конфігурації..." -ForegroundColor Yellow
try {
    $config = Get-Content "auto_config.json" -Raw | ConvertFrom-Json
    
    $needsCredentials = $false
    
    # Перевірка Binance
    if ([string]::IsNullOrWhiteSpace($config.binance.testnet_api_key)) {
        Write-Host "  ⚠ Binance API ключ не встановлено" -ForegroundColor Yellow
        $needsCredentials = $true
    } else {
        Write-Host "  ✓ Binance credentials знайдено" -ForegroundColor Green
    }
    
    # Перевірка GitHub
    if ([string]::IsNullOrWhiteSpace($config.github.token)) {
        Write-Host "  ⚠ GitHub token не встановлено" -ForegroundColor Yellow
        $needsCredentials = $true
    } else {
        Write-Host "  ✓ GitHub credentials знайдено" -ForegroundColor Green
    }
    
    # Перевірка платформи
    $platform = $config.platform
    if ($platform -eq "replit") {
        if ([string]::IsNullOrWhiteSpace($config.replit.api_token)) {
            Write-Host "  ⚠ Replit API token не встановлено" -ForegroundColor Yellow
            $needsCredentials = $true
        } else {
            Write-Host "  ✓ Replit credentials знайдено" -ForegroundColor Green
        }
    } elseif ($platform -eq "render") {
        if ([string]::IsNullOrWhiteSpace($config.render.api_key)) {
            Write-Host "  ⚠ Render API key не встановлено" -ForegroundColor Yellow
            $needsCredentials = $true
        } else {
            Write-Host "  ✓ Render credentials знайдено" -ForegroundColor Green
        }
    }
    
    if ($needsCredentials) {
        Write-Host ""
        Write-Host "  ⚠⚠⚠ ПОТРІБНІ CREDENTIALS ⚠⚠⚠" -ForegroundColor Red
        Write-Host "  Відредагуйте auto_config.json та додайте:" -ForegroundColor Yellow
        Write-Host "    - Binance Testnet API ключі" -ForegroundColor Gray
        Write-Host "    - GitHub Personal Access Token" -ForegroundColor Gray
        Write-Host "    - Render API Key АБО Replit API Token" -ForegroundColor Gray
        Write-Host ""
        Write-Host "  Після додавання credentials запустіть:" -ForegroundColor Yellow
        Write-Host "    python auto_setup.py" -ForegroundColor Cyan
        Write-Host ""
        
        # Пропонуємо відкрити файл
        $open = Read-Host "Відкрити auto_config.json для редагування? (Y/N)"
        if ($open -eq "Y" -or $open -eq "y") {
            notepad "auto_config.json"
        }
        
        exit 0
    }
} catch {
    Write-Host "  ⚠ Помилка читання конфігурації: $_" -ForegroundColor Yellow
    Write-Host "  Перевірте правильність JSON у auto_config.json" -ForegroundColor Yellow
}
Write-Host ""

# ========================================
# КРОК 7: Запуск автоматичного налаштування
# ========================================
Write-Host "[7/8] Запуск автоматичного налаштування..." -ForegroundColor Yellow
Write-Host ""
try {
    python auto_setup.py
    $setupSuccess = $LASTEXITCODE -eq 0
} catch {
    Write-Host "  ✗ Помилка запуску auto_setup.py: $_" -ForegroundColor Red
    $setupSuccess = $false
}
Write-Host ""

# ========================================
# КРОК 8: Підсумок
# ========================================
Write-Host "[8/8] Підсумок..." -ForegroundColor Yellow
Write-Host ""

if ($setupSuccess) {
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "  ✅ ВСЕ ГОТОВО!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Проєкт налаштовано та розгорнуто!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Наступні кроки:" -ForegroundColor Cyan
    Write-Host "  1. Перевірте логи на платформі (Render/Replit)" -ForegroundColor Gray
    Write-Host "  2. Перевірте Keep-Alive ендпоінт" -ForegroundColor Gray
    Write-Host "  3. Перевірте UptimeRobot монітор" -ForegroundColor Gray
    Write-Host ""
} else {
    Write-Host "========================================" -ForegroundColor Yellow
    Write-Host "  ⚠ Налаштування потребує уваги" -ForegroundColor Yellow
    Write-Host "========================================" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Перевірте:" -ForegroundColor Cyan
    Write-Host "  - Чи всі credentials додано в auto_config.json" -ForegroundColor Gray
    Write-Host "  - Чи service_account.json завантажено" -ForegroundColor Gray
    Write-Host "  - Логи вище для деталей помилок" -ForegroundColor Gray
    Write-Host ""
}

Write-Host "Натисніть будь-яку клавішу для виходу..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

