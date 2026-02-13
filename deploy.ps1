# ============================================================
# DEPLOY COMPLETO - Kharis Store
# Ejecutar: .\deploy.ps1
# ============================================================

$ErrorActionPreference = "Stop"
$VPS = "root@72.61.73.245"
$VPS_PATH = "/var/www/kharis-store"
$LOCAL = $PSScriptRoot

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "   DEPLOY COMPLETO - Kharis Store" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# 1. Verificar conexión
Write-Host "[1/5] Conectando al VPS..." -ForegroundColor Yellow
ssh $VPS "echo OK" | Out-Null
Write-Host "      OK" -ForegroundColor Green

# 2. Build frontend
Write-Host "[2/5] Compilando frontend..." -ForegroundColor Yellow
Set-Location "$LOCAL\frontend"
Remove-Item -Recurse -Force "node_modules\.vite", "dist" -ErrorAction SilentlyContinue
$env:VITE_API_URL = "https://demostracion.store"
npx vite build --logLevel error
if ($LASTEXITCODE -ne 0) { throw "Error en build" }
Write-Host "      OK" -ForegroundColor Green

# 3. Subir frontend
Write-Host "[3/5] Subiendo frontend..." -ForegroundColor Yellow
Remove-Item "dist.tar.gz" -ErrorAction SilentlyContinue
tar -czf dist.tar.gz dist
scp -q dist.tar.gz "${VPS}:$VPS_PATH/frontend/"
ssh $VPS "cd $VPS_PATH/frontend && rm -rf dist && tar -xzf dist.tar.gz && rm dist.tar.gz && chown -R www-data:www-data dist"
Remove-Item "dist.tar.gz" -ErrorAction SilentlyContinue
Write-Host "      OK" -ForegroundColor Green

# 4. Subir backend
Write-Host "[4/5] Subiendo backend..." -ForegroundColor Yellow
Set-Location $LOCAL
Remove-Item "src.tar.gz" -ErrorAction SilentlyContinue
tar --exclude="__pycache__" --exclude="*.pyc" --exclude="logs/*" -czf src.tar.gz src
scp -q src.tar.gz "${VPS}:$VPS_PATH/"
ssh $VPS "cd $VPS_PATH && tar -xzf src.tar.gz && rm src.tar.gz"
Remove-Item "src.tar.gz" -ErrorAction SilentlyContinue
Write-Host "      OK" -ForegroundColor Green

# 5. Reiniciar servicio
Write-Host "[5/5] Reiniciando servicio..." -ForegroundColor Yellow
ssh $VPS "systemctl restart kharis-api"
Start-Sleep -Seconds 2
$status = ssh $VPS "systemctl is-active kharis-api"
if ($status -eq "active") {
    Write-Host "      OK" -ForegroundColor Green
} else {
    Write-Host "      ERROR - Ver logs:" -ForegroundColor Red
    ssh $VPS "journalctl -u kharis-api -n 15 --no-pager"
    exit 1
}

# Listo
Write-Host "`n========================================" -ForegroundColor Green
Write-Host "   DEPLOY EXITOSO" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host "`n  https://demostracion.store"
Write-Host "  https://pro.demostracion.store`n"

Set-Location $LOCAL
