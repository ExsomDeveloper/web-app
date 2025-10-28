# update-ngrok-url.ps1
param(
    [Parameter(Mandatory=$true)]
    [string]$NewUrl
)

Write-Host "Обновление ngrok URL в конфигурации..." -ForegroundColor Green

# Обновляем .env файл
$envFile = ".env"
if (Test-Path $envFile) {
    $content = Get-Content $envFile
    $newContent = $content -replace "API_BASE_URL=.*", "API_BASE_URL=$NewUrl"
    Set-Content -Path $envFile -Value $newContent
    Write-Host "✅ Обновлен файл .env" -ForegroundColor Green
} else {
    Write-Host "⚠️  Файл .env не найден, создаю новый..." -ForegroundColor Yellow
    $envContent = @"
ENVIRONMENT=development
API_BASE_URL=$NewUrl
FRONTEND_URL=http://localhost:3000
HOST=0.0.0.0
PORT=8000
KLING_ACCESS_KEY=AkFBemPhJ4LHfFJLL3aCTGKPaGPRNMEA
KLING_SECRET_KEY=nykRgmfLAparCKF3Gg3nC3tmBkYrTftF
KLING_API_DOMAIN=https://api-singapore.klingai.com
"@
    Set-Content -Path $envFile -Value $envContent
    Write-Host "✅ Создан файл .env" -ForegroundColor Green
}

Write-Host ""
Write-Host "🔄 Перезапустите сервер для применения изменений:" -ForegroundColor Yellow
Write-Host "   python main.py" -ForegroundColor White
Write-Host ""
Write-Host "🌐 Новый API URL: $NewUrl" -ForegroundColor Cyan
Write-Host "📡 Callback URL: $NewUrl/api/kling/callback" -ForegroundColor Cyan
