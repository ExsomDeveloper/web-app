# auto-update-ngrok.ps1
Write-Host "Автоматическое обновление ngrok URL..." -ForegroundColor Green

try {
    # Получаем URL от ngrok
    $response = Invoke-RestMethod -Uri "http://localhost:4040/api/tunnels" -Method Get
    $newUrl = $response.tunnels[0].public_url
    
    if ($newUrl) {
        Write-Host "Получен новый ngrok URL: $newUrl" -ForegroundColor Cyan
        
        # Обновляем конфигурацию
        .\update-ngrok-url.ps1 -NewUrl $newUrl
        
        Write-Host ""
        Write-Host "✅ URL обновлен автоматически!" -ForegroundColor Green
        Write-Host "🔄 Перезапустите сервер: python main.py" -ForegroundColor Yellow
    } else {
        Write-Host "❌ Не удалось получить URL от ngrok" -ForegroundColor Red
    }
} catch {
    Write-Host "❌ ngrok не запущен или недоступен" -ForegroundColor Red
    Write-Host "Запустите ngrok: .\ngrok.exe http 8000" -ForegroundColor Yellow
}
