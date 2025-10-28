# start-server-with-ngrok.ps1
Write-Host "🚀 Запуск сервера с ngrok туннелем..." -ForegroundColor Green

# Проверяем наличие ngrok
if (-not (Test-Path "ngrok.exe")) {
    Write-Host "❌ ngrok.exe не найден. Установите ngrok сначала." -ForegroundColor Red
    exit 1
}

# Проверяем, запущен ли уже сервер
$serverRunning = $false
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/docs" -TimeoutSec 2 -ErrorAction SilentlyContinue
    if ($response.StatusCode -eq 200) {
        $serverRunning = $true
        Write-Host "✅ Сервер уже запущен на localhost:8000" -ForegroundColor Green
    }
} catch {
    Write-Host "⚠️  Сервер не запущен, запускаю..." -ForegroundColor Yellow
}

if (-not $serverRunning) {
    Write-Host "🔄 Запускаю FastAPI сервер..." -ForegroundColor Yellow
    Start-Process -FilePath "python" -ArgumentList "main.py" -WindowStyle Minimized
    Start-Sleep -Seconds 3
}

# Запускаем ngrok
Write-Host "🌐 Запускаю ngrok туннель..." -ForegroundColor Cyan
Start-Process -FilePath ".\ngrok.exe" -ArgumentList "http", "8000"

Write-Host ""
Write-Host "📋 Инструкции:" -ForegroundColor Yellow
Write-Host "1. Скопируйте публичный URL из окна ngrok (например: https://abc123.ngrok.io)" -ForegroundColor White
Write-Host "2. Откройте файл routers/tryon.py" -ForegroundColor White
Write-Host "3. Замените строку 83:" -ForegroundColor White
Write-Host "   callback_url = 'https://your-ngrok-url.ngrok.io/api/kling/callback'" -ForegroundColor Cyan
Write-Host "   на:" -ForegroundColor White
Write-Host "   callback_url = 'https://abc123.ngrok.io/api/kling/callback'" -ForegroundColor Cyan
Write-Host "4. Сохраните файл и перезапустите сервер" -ForegroundColor White
Write-Host ""
Write-Host "🌐 Сервер доступен по адресам:" -ForegroundColor Green
Write-Host "   Локально: http://localhost:8000" -ForegroundColor White
Write-Host "   Публично: https://abc123.ngrok.io (замените на ваш URL)" -ForegroundColor White
Write-Host "   API документация: http://localhost:8000/docs" -ForegroundColor White
