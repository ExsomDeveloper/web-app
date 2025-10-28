# update-all-ngrok.ps1
param(
    [Parameter(Mandatory=$true)]
    [string]$NewUrl
)

Write-Host "Обновление ngrok URL во всех проектах..." -ForegroundColor Green

# Обновляем backend
Write-Host "🔄 Обновляю backend..." -ForegroundColor Yellow
Set-Location "..\backend"
if (Test-Path "update-ngrok-url.ps1") {
    .\update-ngrok-url.ps1 -NewUrl $NewUrl
} else {
    Write-Host "⚠️  Скрипт update-ngrok-url.ps1 не найден в backend" -ForegroundColor Yellow
}

# Обновляем frontend
Write-Host "🔄 Обновляю frontend..." -ForegroundColor Yellow
Set-Location "..\frontend"
if (Test-Path "update-frontend-ngrok.ps1") {
    .\update-frontend-ngrok.ps1 -NewUrl $NewUrl
} else {
    Write-Host "⚠️  Скрипт update-frontend-ngrok.ps1 не найден в frontend" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "✅ Обновление завершено!" -ForegroundColor Green
Write-Host "🔄 Перезапустите сервер: python main.py" -ForegroundColor Yellow
Write-Host "🔄 Пересоберите фронтенд: npm run build && npm run deploy" -ForegroundColor Yellow
