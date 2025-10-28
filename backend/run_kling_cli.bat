@echo off
REM Скрипт для запуска Kling AI CLI команды
REM Использование: run_kling_cli.bat girl.jpg longsleev.jpg [callback_url]

if "%1"=="" (
    echo ОШИБКА: Не указан путь к изображению человека
    echo Использование: run_kling_cli.bat girl.jpg longsleev.jpg [callback_url]
    exit /b 1
)

if "%2"=="" (
    echo ОШИБКА: Не указан путь к изображению одежды
    echo Использование: run_kling_cli.bat girl.jpg longsleev.jpg [callback_url]
    exit /b 1
)

cd /d "%~dp0"

echo Запускаю Kling AI CLI...
python cli_kling.py --human-image "%1" --cloth-image "%2" %3

pause
