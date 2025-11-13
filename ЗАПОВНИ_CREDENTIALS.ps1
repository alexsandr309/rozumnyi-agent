# Automatic auto_config.json population script
# ASCII-only prompts for compatibility

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Auto-fill credentials for auto_config.json" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Ensure working directory is script folder
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptPath

# Ensure auto_config.json exists
if (-not (Test-Path "auto_config.json")) {
    if (Test-Path "auto_config.example.json") {
        Copy-Item "auto_config.example.json" "auto_config.json"
        Write-Host "[OK] Created auto_config.json from example" -ForegroundColor Green
    } else {
        Write-Host "[ERROR] auto_config.example.json is missing" -ForegroundColor Red
        exit 1
    }
}

# Prepare config structure (keep existing values when possible)
$config = @{
    platform = "render"
    binance = @{ testnet_api_key = ""; testnet_secret_key = "" }
    github = @{ username = ""; token = ""; repo_name = "rozumnyi-agent" }
    render = @{ api_key = "" }
    replit = @{ api_token = ""; username = ""; repl_name = "rozumnyi-agent" }
    uptimerobot = @{ api_key = "" }
    trading = @{ mode = "BALANCED"; deposit_usdt = 1000 }
}

if (Test-Path "auto_config.json") {
    try {
        $existing = Get-Content "auto_config.json" -Raw | ConvertFrom-Json
        if ($existing.platform) { $config.platform = $existing.platform }
        if ($existing.binance) {
            if ($existing.binance.testnet_api_key) { $config.binance.testnet_api_key = $existing.binance.testnet_api_key }
            if ($existing.binance.testnet_secret_key) { $config.binance.testnet_secret_key = $existing.binance.testnet_secret_key }
        }
        if ($existing.github) {
            if ($existing.github.username) { $config.github.username = $existing.github.username }
            if ($existing.github.token) { $config.github.token = $existing.github.token }
            if ($existing.github.repo_name) { $config.github.repo_name = $existing.github.repo_name }
        }
        if ($existing.render) {
            if ($existing.render.api_key) { $config.render.api_key = $existing.render.api_key }
        }
        if ($existing.replit) {
            if ($existing.replit.api_token) { $config.replit.api_token = $existing.replit.api_token }
            if ($existing.replit.username) { $config.replit.username = $existing.replit.username }
            if ($existing.replit.repl_name) { $config.replit.repl_name = $existing.replit.repl_name }
        }
        if ($existing.uptimerobot) {
            if ($existing.uptimerobot.api_key) { $config.uptimerobot.api_key = $existing.uptimerobot.api_key }
        }
        if ($existing.trading) {
            if ($existing.trading.mode) { $config.trading.mode = $existing.trading.mode }
            if ($existing.trading.deposit_usdt) { $config.trading.deposit_usdt = $existing.trading.deposit_usdt }
        }
    } catch {
        Write-Host "[WARN] Could not parse auto_config.json, using defaults" -ForegroundColor Yellow
    }
}

Write-Host "Enter credentials (press Enter to keep current value)" -ForegroundColor Yellow
Write-Host ""

# Binance
Write-Host "--- Binance Testnet ---" -ForegroundColor Cyan
$binanceApiKey = Read-Host "Binance Testnet API Key"
if ($binanceApiKey) { $config.binance.testnet_api_key = $binanceApiKey }
$binanceSecretKey = Read-Host "Binance Testnet Secret Key"
if ($binanceSecretKey) { $config.binance.testnet_secret_key = $binanceSecretKey }
Write-Host ""

# GitHub
Write-Host "--- GitHub ---" -ForegroundColor Cyan
$githubUsername = Read-Host "GitHub Username"
if ($githubUsername) { $config.github.username = $githubUsername }
$githubToken = Read-Host "GitHub Personal Access Token"
if ($githubToken) { $config.github.token = $githubToken }
$githubRepo = Read-Host ("GitHub Repository Name [Enter for '{0}']" -f $config.github.repo_name)
if ($githubRepo) { $config.github.repo_name = $githubRepo }
Write-Host ""

# Platform selection
Write-Host "--- Deployment Platform ---" -ForegroundColor Cyan
$platform = Read-Host ("Platform (render/replit) [Enter for '{0}']" -f $config.platform)
if ($platform) { $config.platform = $platform.ToLower() }
if ($config.platform -ne "render" -and $config.platform -ne "replit") {
    Write-Host "[WARN] Unknown platform value. Falling back to render." -ForegroundColor Yellow
    $config.platform = "render"
}

if ($config.platform -eq "render") {
    $renderApiKey = Read-Host "Render API Key"
    if ($renderApiKey) { $config.render.api_key = $renderApiKey }
} else {
    $replitToken = Read-Host "Replit API Token"
    if ($replitToken) { $config.replit.api_token = $replitToken }
    $replitUsername = Read-Host ("Replit Username [Enter for '{0}']" -f $config.replit.username)
    if ($replitUsername) { $config.replit.username = $replitUsername }
    $replitRepl = Read-Host ("Replit Repl Name [Enter for '{0}']" -f $config.replit.repl_name)
    if ($replitRepl) { $config.replit.repl_name = $replitRepl }
}
Write-Host ""

# UptimeRobot
Write-Host "--- UptimeRobot (optional) ---" -ForegroundColor Cyan
$uptimeToken = Read-Host "UptimeRobot API Key (Enter to skip)"
if ($uptimeToken) { $config.uptimerobot.api_key = $uptimeToken }
Write-Host ""

# Trading settings
Write-Host "--- Trading Settings ---" -ForegroundColor Cyan
$modeInput = Read-Host ("Risk mode (CONSERVATIVE/BALANCED/AGGRESSIVE) [Enter for '{0}']" -f $config.trading.mode)
if ($modeInput) { $config.trading.mode = $modeInput.ToUpper() }
$depositInput = Read-Host ("Initial deposit USDT [Enter for '{0}']" -f $config.trading.deposit_usdt)
if ($depositInput) {
    if ([int]::TryParse($depositInput, [ref]$null)) {
        $config.trading.deposit_usdt = [int]$depositInput
    } else {
        Write-Host "[WARN] Deposit must be integer. Keeping previous value." -ForegroundColor Yellow
    }
}

# Build JSON structure
$jsonOutput = @{
    platform = $config.platform
    binance = @{
        testnet_api_key = $config.binance.testnet_api_key
        testnet_secret_key = $config.binance.testnet_secret_key
    }
    github = @{
        username = $config.github.username
        token = $config.github.token
        repo_name = $config.github.repo_name
    }
    trading = @{
        mode = $config.trading.mode
        deposit_usdt = $config.trading.deposit_usdt
    }
}

if ($config.platform -eq "render") {
    $jsonOutput.render = @{ api_key = $config.render.api_key }
} else {
    $jsonOutput.replit = @{
        api_token = $config.replit.api_token
        username = $config.replit.username
        repl_name = $config.replit.repl_name
    }
}

if ($config.uptimerobot.api_key) {
    $jsonOutput.uptimerobot = @{ api_key = $config.uptimerobot.api_key }
}

# Save file without BOM
$jsonString = $jsonOutput | ConvertTo-Json -Depth 10
$utf8NoBom = New-Object System.Text.UTF8Encoding($false)
[System.IO.File]::WriteAllText((Join-Path $scriptPath "auto_config.json"), $jsonString, $utf8NoBom)
Write-Host "[OK] auto_config.json updated" -ForegroundColor Green
Write-Host ""

# Summary (without secrets)
Write-Host "Summary (secrets hidden):" -ForegroundColor Cyan
Write-Host ("  Platform: {0}" -f $config.platform) -ForegroundColor Gray

$binanceStatus = if ($config.binance.testnet_api_key) { "OK" } else { "MISSING" }
Write-Host ("  Binance API Key: {0}" -f $binanceStatus) -ForegroundColor Gray

$githubUserDisplay = if ($config.github.username) { $config.github.username } else { "MISSING" }
Write-Host ("  GitHub Username: {0}" -f $githubUserDisplay) -ForegroundColor Gray

$githubTokenStatus = if ($config.github.token) { "OK" } else { "MISSING" }
Write-Host ("  GitHub Token: {0}" -f $githubTokenStatus) -ForegroundColor Gray

if ($config.platform -eq "render") {
    $renderStatus = if ($config.render.api_key) { "OK" } else { "MISSING" }
    Write-Host ("  Render API Key: {0}" -f $renderStatus) -ForegroundColor Gray
} else {
    $replitStatus = if ($config.replit.api_token) { "OK" } else { "MISSING" }
    Write-Host ("  Replit API Token: {0}" -f $replitStatus) -ForegroundColor Gray
}

Write-Host ("  Trading Mode: {0}" -f $config.trading.mode) -ForegroundColor Gray
Write-Host ("  Deposit: {0}" -f $config.trading.deposit_usdt) -ForegroundColor Gray
Write-Host ""

Write-Host "========================================" -ForegroundColor Green
Write-Host "  Done! You can run: python auto_setup.py" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
