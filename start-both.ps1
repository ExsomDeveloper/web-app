Write-Host "Starting both Frontend and Backend..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd frontend; npm start" -WindowStyle Normal
Start-Sleep -Seconds 3
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd backend; & '.\venv\Scripts\Activate.ps1'; python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000" -WindowStyle Normal
Write-Host "Both services are starting..." -ForegroundColor Yellow
Write-Host "Frontend will be available at: http://localhost:3000" -ForegroundColor Cyan
Write-Host "Backend will be available at: http://localhost:8000" -ForegroundColor Cyan
Write-Host "Backend API docs at: http://localhost:8000/docs" -ForegroundColor Cyan
Read-Host "Press Enter to continue"
