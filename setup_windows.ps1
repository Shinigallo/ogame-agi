# OGameAGI Windows Setup Script
# Esegui questo script in PowerShell come amministratore

param(
    [switch]$SkipBrowserInstall
)

$ErrorActionPreference = "Continue"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "OGameAGI - Setup per Windows" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check Python
Write-Host "[1/7] Verificando Python..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Python non trovato! Installa Python 3.10+ da python.org" -ForegroundColor Red
    exit 1
}
Write-Host "✅ $pythonVersion" -ForegroundColor Green

# Create venv
Write-Host "[2/7] Creando virtual environment..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "⚠️  Rimuovendo venv esistente..." -ForegroundColor Yellow
    Remove-Item -Recurse -Force "venv"
}
python -m venv venv
if ($LASTEXITCODE -ne 0) { exit 1 }
Write-Host "✅ Virtual environment creato" -ForegroundColor Green

# Activate venv
Write-Host "[3/7] Attivando virtual environment..." -ForegroundColor Yellow
& ".\venv\Scripts\Activate.ps1"
$env:PYTHONPATH = ""
Write-Host "✅ Venv attivato" -ForegroundColor Green

# Upgrade pip
Write-Host "[4/7] Aggiornando pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip --quiet

# Install requirements
Write-Host "[5/7] Installando dipendenze..." -ForegroundColor Yellow
pip install -r requirements.txt --quiet
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Errore installazione dipendenze" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Dipendenze installate" -ForegroundColor Green

# Install Playwright
Write-Host "[6/7] Installando Playwright..." -ForegroundColor Yellow
pip install playwright --quiet
if ($LASTEXITCODE -ne 0) { exit 1 }

if (-not $SkipBrowserInstall) {
    playwright install --with-deps chromium
    if ($LASTEXITCODE -ne 0) {
        Write-Host "⚠️  Playwright browsers might need manual install" -ForegroundColor Yellow
    }
} else {
    Write-Host "⚠️  Skipping browser install (use -SkipBrowserInstall)" -ForegroundColor Yellow
}
Write-Host "✅ Playwright installato" -ForegroundColor Green

# Copy env file
Write-Host "[7/7] Configurando environment..." -ForegroundColor Yellow
if (Test-Path ".env.windows") {
    Copy-Item ".env.windows" ".env" -Force
    Write-Host "✅ .env creato da .env.windows" -ForegroundColor Green
    Write-Host "⚠️  MODIFICA .env con le tue credenziali!" -ForegroundColor Yellow
} else {
    Write-Host "⚠️  .env.windows non trovato, crea .env manualmente" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "✅ SETUP COMPLETATO!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Prossimi passi:" -ForegroundColor White
Write-Host "  1. Apri .env e inserisci le tue credenziali" -ForegroundColor White
Write-Host "  2. Esegui: python tests\test_playwright_fase1.py" -ForegroundColor White
Write-Host ""