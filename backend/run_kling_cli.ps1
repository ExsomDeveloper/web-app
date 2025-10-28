# PowerShell скрипт для запуска Kling AI CLI команды
# Использование: .\run_kling_cli.ps1 girl.jpg longsleev.jpg [callback_url]

param(
    [Parameter(Mandatory=$true)]
    [string]$HumanImage,
    
    [Parameter(Mandatory=$true)]
    [string]$ClothImage,
    
    [Parameter(Mandatory=$false)]
    [string]$CallbackUrl
)

# Переходим в директорию скрипта
Set-Location $PSScriptRoot

Write-Host "=============================================" -ForegroundColor Cyan
Write-Host "KLING AI VIRTUAL TRY-ON CLI" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host "Изображение человека: $HumanImage" -ForegroundColor Yellow
Write-Host "Изображение одежды: $ClothImage" -ForegroundColor Yellow
if ($CallbackUrl) {
    Write-Host "Callback URL: $CallbackUrl" -ForegroundColor Yellow
}
Write-Host "=============================================" -ForegroundColor Cyan

# Проверяем существование файлов
if (-not (Test-Path $HumanImage)) {
    Write-Host "ОШИБКА: Файл с изображением человека не найден: $HumanImage" -ForegroundColor Red
    exit 1
}

if (-not (Test-Path $ClothImage)) {
    Write-Host "ОШИБКА: Файл с изображением одежды не найден: $ClothImage" -ForegroundColor Red
    exit 1
}

# Запускаем CLI команду
try {
    if ($CallbackUrl) {
        python cli_kling.py --human-image $HumanImage --cloth-image $ClothImage --callback-url $CallbackUrl
    } else {
        python cli_kling.py --human-image $HumanImage --cloth-image $ClothImage
    }
} catch {
    Write-Host "ОШИБКА при выполнении команды: $_" -ForegroundColor Red
    exit 1
}

Write-Host "`nНажмите любую клавишу для продолжения..." -ForegroundColor Green
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
