# Інтерактивний гайд для отримання всіх API ключів
# Цей скрипт веде вас крок за кроком до отримання кожного ключа

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  ІНТЕРАКТИВНИЙ ГАЙД - Отримання Ключів" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$credentials = @{}

# ========================================
# 1. Binance Testnet
# ========================================
Write-Host "════════════════════════════════════════" -ForegroundColor Yellow
Write-Host "1. BINANCE TESTNET API КЛЮЧІ" -ForegroundColor Yellow
Write-Host "════════════════════════════════════════" -ForegroundColor Yellow
Write-Host ""
Write-Host "Крок 1: Відкрийте браузер та перейдіть до:" -ForegroundColor Cyan
Write-Host "  https://testnet.binancefuture.com/" -ForegroundColor White
Write-Host ""
Write-Host "Крок 2: Увійдіть або зареєструйтеся" -ForegroundColor Cyan
Write-Host ""
Write-Host "Крок 3: Створіть API ключі:" -ForegroundColor Cyan
Write-Host "  - Натисніть на профіль (правый верхній кут)" -ForegroundColor Gray
Write-Host "  - Виберіть 'API Management' або 'API Keys'" -ForegroundColor Gray
Write-Host "  - Натисніть 'Create API Key'" -ForegroundColor Gray
Write-Host "  - Дозвольте 'Enable Spot Trading'" -ForegroundColor Gray
Write-Host "  - Підтвердіть через email/SMS" -ForegroundColor Gray
Write-Host ""
Write-Host "Крок 4: Скопіюйте обидва ключі" -ForegroundColor Cyan
Write-Host ""
$ready = Read-Host "Коли отримаєте ключі, натисніть Enter для продовження"
Write-Host ""

Write-Host "Введіть ваші Binance Testnet ключі:" -ForegroundColor Yellow
$binanceApiKey = Read-Host "Binance Testnet API Key"
$binanceSecretKey = Read-Host "Binance Testnet Secret Key"

if ($binanceApiKey -and $binanceSecretKey) {
    $credentials['binance'] = @{
        testnet_api_key = $binanceApiKey
        testnet_secret_key = $binanceSecretKey
    }
    Write-Host "[✓] Binance ключі збережено" -ForegroundColor Green
} else {
    Write-Host "[⚠] Binance ключі не введено" -ForegroundColor Yellow
}
Write-Host ""

# ========================================
# 2. GitHub
# ========================================
Write-Host "════════════════════════════════════════" -ForegroundColor Yellow
Write-Host "2. GITHUB PERSONAL ACCESS TOKEN" -ForegroundColor Yellow
Write-Host "════════════════════════════════════════" -ForegroundColor Yellow
Write-Host ""
Write-Host "Крок 1: Відкрийте браузер та перейдіть до:" -ForegroundColor Cyan
Write-Host "  https://github.com/settings/tokens" -ForegroundColor White
Write-Host ""
Write-Host "Крок 2: Створіть токен:" -ForegroundColor Cyan
Write-Host "  - Натисніть 'Generate new token' → 'Generate new token (classic)'" -ForegroundColor Gray
Write-Host "  - Note: 'Trading Agent Auto Deploy'" -ForegroundColor Gray
Write-Host "  - Expiration: 'No expiration'" -ForegroundColor Gray
Write-Host "  - Scopes: Відмітьте 'repo' (повний контроль)" -ForegroundColor Gray
Write-Host "  - Натисніть 'Generate token'" -ForegroundColor Gray
Write-Host ""
Write-Host "Крок 3: Скопіюйте токен (показується тільки один раз!)" -ForegroundColor Cyan
Write-Host ""
Write-Host "Крок 4: Знайдіть ваш GitHub Username:" -ForegroundColor Cyan
Write-Host "  - Перейдіть до https://github.com/settings/profile" -ForegroundColor Gray
Write-Host "  - Username видно у верхній частині" -ForegroundColor Gray
Write-Host ""
$ready = Read-Host "Коли отримаєте токен та username, натисніть Enter для продовження"
Write-Host ""

Write-Host "Введіть ваші GitHub дані:" -ForegroundColor Yellow
$githubUsername = Read-Host "GitHub Username"
$githubToken = Read-Host "GitHub Personal Access Token"
$githubRepo = Read-Host "GitHub Repository Name (Enter для 'розумний-агент')"
if (-not $githubRepo) { $githubRepo = "розумний-агент" }

if ($githubUsername -and $githubToken) {
    $credentials['github'] = @{
        username = $githubUsername
        token = $githubToken
        repo_name = $githubRepo
    }
    Write-Host "[✓] GitHub дані збережено" -ForegroundColor Green
} else {
    Write-Host "[⚠] GitHub дані не введено" -ForegroundColor Yellow
}
Write-Host ""

# ========================================
# 3. Платформа (Render або Replit)
# ========================================
Write-Host "════════════════════════════════════════" -ForegroundColor Yellow
Write-Host "3. ПЛАТФОРМА РОЗГОРТАННЯ" -ForegroundColor Yellow
Write-Host "════════════════════════════════════════" -ForegroundColor Yellow
Write-Host ""
$platform = Read-Host "Яку платформу використовуєте? (render/replit) [Enter для 'render']"
if (-not $platform) { $platform = "render" }
$platform = $platform.ToLower()
$credentials['platform'] = $platform
Write-Host ""

if ($platform -eq "render") {
    Write-Host "════════════════════════════════════════" -ForegroundColor Yellow
    Write-Host "3a. RENDER API KEY" -ForegroundColor Yellow
    Write-Host "════════════════════════════════════════" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Крок 1: Відкрийте браузер та перейдіть до:" -ForegroundColor Cyan
    Write-Host "  https://dashboard.render.com/account/api-keys" -ForegroundColor White
    Write-Host ""
    Write-Host "Крок 2: Створіть API ключ:" -ForegroundColor Cyan
    Write-Host "  - Натисніть 'Create API Key'" -ForegroundColor Gray
    Write-Host "  - Name: 'Trading Agent Auto Deploy'" -ForegroundColor Gray
    Write-Host "  - Натисніть 'Create'" -ForegroundColor Gray
    Write-Host ""
    Write-Host "Крок 3: Скопіюйте API ключ (показується тільки один раз!)" -ForegroundColor Cyan
    Write-Host ""
    $ready = Read-Host "Коли отримаєте ключ, натисніть Enter для продовження"
    Write-Host ""
    
    $renderApiKey = Read-Host "Render API Key"
    if ($renderApiKey) {
        $credentials['render'] = @{
            api_key = $renderApiKey
        }
        Write-Host "[✓] Render API ключ збережено" -ForegroundColor Green
    } else {
        Write-Host "[⚠] Render API ключ не введено" -ForegroundColor Yellow
    }
} elseif ($platform -eq "replit") {
    Write-Host "════════════════════════════════════════" -ForegroundColor Yellow
    Write-Host "3a. REPLIT API TOKEN" -ForegroundColor Yellow
    Write-Host "════════════════════════════════════════" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Крок 1: Відкрийте браузер та перейдіть до:" -ForegroundColor Cyan
    Write-Host "  https://replit.com/" -ForegroundColor White
    Write-Host ""
    Write-Host "Крок 2: Створіть API токен:" -ForegroundColor Cyan
    Write-Host "  - Натисніть на профіль (аватар)" -ForegroundColor Gray
    Write-Host "  - Виберіть 'Account' → 'API Tokens'" -ForegroundColor Gray
    Write-Host "  - Натисніть 'Create Token'" -ForegroundColor Gray
    Write-Host "  - Name: 'Trading Agent Auto Deploy'" -ForegroundColor Gray
    Write-Host "  - Scopes: repls:read, repls:write, secrets:read, secrets:write" -ForegroundColor Gray
    Write-Host "  - Натисніть 'Create'" -ForegroundColor Gray
    Write-Host ""
    Write-Host "Крок 3: Скопіюйте токен та знайдіть username" -ForegroundColor Cyan
    Write-Host ""
    $ready = Read-Host "Коли отримаєте токен та username, натисніть Enter для продовження"
    Write-Host ""
    
    $replitApiToken = Read-Host "Replit API Token"
    $replitUsername = Read-Host "Replit Username"
    $replitReplName = Read-Host "Replit Repl Name (Enter для 'розумний-агент')"
    if (-not $replitReplName) { $replitReplName = "розумний-агент" }
    
    if ($replitApiToken -and $replitUsername) {
        $credentials['replit'] = @{
            api_token = $replitApiToken
            username = $replitUsername
            repl_name = $replitReplName
        }
        Write-Host "[✓] Replit дані збережено" -ForegroundColor Green
    } else {
        Write-Host "[⚠] Replit дані не введено" -ForegroundColor Yellow
    }
}
Write-Host ""

# ========================================
# 4. UptimeRobot (опціонально)
# ========================================
Write-Host "════════════════════════════════════════" -ForegroundColor Yellow
Write-Host "4. UPTIMEROBOT API KEY (опціонально)" -ForegroundColor Yellow
Write-Host "════════════════════════════════════════" -ForegroundColor Yellow
Write-Host ""
Write-Host "Крок 1: Відкрийте браузер та перейдіть до:" -ForegroundColor Cyan
Write-Host "  https://uptimerobot.com/dashboard.php#mySettings" -ForegroundColor White
Write-Host ""
Write-Host "Крок 2: Отримайте API ключ:" -ForegroundColor Cyan
Write-Host "  - Перейдіть до 'My Settings' → 'API Settings'" -ForegroundColor Gray
Write-Host "  - Скопіюйте 'Main API Key'" -ForegroundColor Gray
Write-Host ""
$skip = Read-Host "Натисніть Enter для пропуску або введіть 'y' для додавання"
if ($skip -eq "y") {
    $uptimeRobotApiKey = Read-Host "UptimeRobot API Key"
    if ($uptimeRobotApiKey) {
        $credentials['uptimerobot'] = @{
            api_key = $uptimeRobotApiKey
        }
        Write-Host "[✓] UptimeRobot ключ збережено" -ForegroundColor Green
    }
}
Write-Host ""

# ========================================
# 5. Trading Settings
# ========================================
Write-Host "════════════════════════════════════════" -ForegroundColor Yellow
Write-Host "5. НАЛАШТУВАННЯ ТОРГІВЛІ" -ForegroundColor Yellow
Write-Host "════════════════════════════════════════" -ForegroundColor Yellow
Write-Host ""
$tradingMode = Read-Host "Режим ризику (CONSERVATIVE/BALANCED/AGGRESSIVE) [Enter для 'BALANCED']"
if (-not $tradingMode) { $tradingMode = "BALANCED" }

$depositUsdt = Read-Host "Початковий депозит USDT [Enter для '1000']"
if (-not $depositUsdt) { $depositUsdt = "1000" }

$credentials['trading'] = @{
    mode = $tradingMode.ToUpper()
    deposit_usdt = [int]$depositUsdt
}
Write-Host ""

# ========================================
# Збереження
# ========================================
Write-Host "Збереження всіх credentials..." -ForegroundColor Yellow

# Створення повної структури JSON
$jsonConfig = @{
    platform = $credentials['platform']
    binance = $credentials['binance']
    github = $credentials['github']
    trading = $credentials['trading']
}

if ($credentials['platform'] -eq "render" -and $credentials['render']) {
    $jsonConfig['render'] = $credentials['render']
} elseif ($credentials['platform'] -eq "replit" -and $credentials['replit']) {
    $jsonConfig['replit'] = $credentials['replit']
}

if ($credentials['uptimerobot']) {
    $jsonConfig['uptimerobot'] = $credentials['uptimerobot']
}

# Збереження
$jsonContent = $jsonConfig | ConvertTo-Json -Depth 10
$jsonContent | Out-File "auto_config.json" -Encoding UTF8

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  ✅ ВСІ CREDENTIALS ЗБЕРЕЖЕНО!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Файл auto_config.json створено/оновлено!" -ForegroundColor Cyan
Write-Host ""
Write-Host "Тепер можна запустити:" -ForegroundColor Yellow
Write-Host "  python auto_setup.py" -ForegroundColor White
Write-Host ""

