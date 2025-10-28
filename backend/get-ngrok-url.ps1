# get-ngrok-url.ps1
Write-Host "Getting public URL from ngrok..." -ForegroundColor Green

try {
    $response = Invoke-RestMethod -Uri "http://localhost:4040/api/tunnels" -Method Get
    $publicUrl = $response.tunnels[0].public_url
    
    Write-Host ""
    Write-Host "Public URL found!" -ForegroundColor Green
    Write-Host "Public URL: $publicUrl" -ForegroundColor Cyan
    Write-Host "Callback URL: $publicUrl/api/kling/callback" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Now replace line 83 in routers/tryon.py:" -ForegroundColor Yellow
    Write-Host "callback_url = 'https://your-ngrok-url.ngrok.io/api/kling/callback'" -ForegroundColor White
    Write-Host "with:" -ForegroundColor Yellow
    Write-Host "callback_url = '$publicUrl/api/kling/callback'" -ForegroundColor Green
    Write-Host ""
    Write-Host "Server available at:" -ForegroundColor Green
    Write-Host "   Local: http://localhost:8000" -ForegroundColor White
    Write-Host "   Public: $publicUrl" -ForegroundColor White
    Write-Host "   API docs: http://localhost:8000/docs" -ForegroundColor White
    
} catch {
    Write-Host "ngrok not ready or not running" -ForegroundColor Red
    Write-Host "Make sure ngrok is running: .\ngrok.exe http 8000" -ForegroundColor Yellow
}
