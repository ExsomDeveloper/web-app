@echo off
echo Starting both Frontend and Backend...
start "Frontend" cmd /k "cd frontend && npm start"
timeout /t 3 /nobreak >nul
start "Backend" cmd /k "cd backend && call venv\Scripts\activate.bat && python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000"
echo Both services are starting...
echo Frontend will be available at: http://localhost:3000
echo Backend will be available at: http://localhost:8000
echo Backend API docs at: http://localhost:8000/docs
pause
