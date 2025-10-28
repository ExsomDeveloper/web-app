# update-frontend-ngrok.ps1
param(
    [Parameter(Mandatory=$true)]
    [string]$NewUrl
)

Write-Host "Обновление ngrok URL во фронтенде..." -ForegroundColor Green

# Обновляем env.development.example
$devFile = "env.development.example"
if (Test-Path $devFile) {
    $content = Get-Content $devFile
    $newContent = $content -replace "REACT_APP_API_URL_PRODUCTION=.*", "REACT_APP_API_URL_PRODUCTION=$NewUrl"
    Set-Content -Path $devFile -Value $newContent
    Write-Host "✅ Обновлен $devFile" -ForegroundColor Green
}

# Обновляем env.production.example
$prodFile = "env.production.example"
if (Test-Path $prodFile) {
    $content = Get-Content $prodFile
    $newContent = $content -replace "REACT_APP_API_URL_PRODUCTION=.*", "REACT_APP_API_URL_PRODUCTION=$NewUrl"
    Set-Content -Path $prodFile -Value $newContent
    Write-Host "✅ Обновлен $prodFile" -ForegroundColor Green
}

# Обновляем config/env.ts
$configFile = "src\config\env.ts"
if (Test-Path $configFile) {
    $content = Get-Content $configFile
    $newContent = $content -replace "API_URL_PRODUCTION: process\.env\.REACT_APP_API_URL_PRODUCTION \|\| '.*'", "API_URL_PRODUCTION: process.env.REACT_APP_API_URL_PRODUCTION || '$NewUrl'"
    Set-Content -Path $configFile -Value $newContent
    Write-Host "✅ Обновлен $configFile" -ForegroundColor Green
}

Write-Host ""
Write-Host "🔄 Пересоберите и задеплойте фронтенд:" -ForegroundColor Yellow
Write-Host "   npm run build" -ForegroundColor White
Write-Host "   npm run deploy" -ForegroundColor White
Write-Host ""
Write-Host "🌐 Новый API URL: $NewUrl" -ForegroundColor Cyan
