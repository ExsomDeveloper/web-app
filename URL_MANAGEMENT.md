# Управление URL в проекте

## 📁 Структура конфигурации

### Backend (`backend/`)
- `app/config.py` - основная конфигурация
- `.env` - переменные окружения (создается автоматически)
- `env.example` - пример конфигурации

### Frontend (`frontend/`)
- `src/config/env.ts` - конфигурация API URL
- `env.development.example` - пример для разработки
- `env.production.example` - пример для продакшна

## 🔧 Быстрое обновление ngrok URL

### Автоматическое обновление (рекомендуется):
```powershell
# Из корневой папки проекта
.\update-all-ngrok.ps1 -NewUrl "https://new-url.ngrok.io"
```

### Ручное обновление:

#### Backend:
```powershell
cd backend
.\update-ngrok-url.ps1 -NewUrl "https://new-url.ngrok.io"
```

#### Frontend:
```powershell
cd frontend
.\update-frontend-ngrok.ps1 -NewUrl "https://new-url.ngrok.io"
```

## 🚀 Деплой

### Backend:
```bash
cd backend
python main.py
```

### Frontend:
```bash
cd frontend
npm run build
npm run deploy
```

## 📋 Переменные окружения

### Backend (.env):
```
ENVIRONMENT=development
API_BASE_URL=https://your-ngrok-url.ngrok.io
FRONTEND_URL=http://localhost:3000
```

### Frontend (.env.development):
```
REACT_APP_API_URL_LOCAL=http://localhost:8000
REACT_APP_API_URL_PRODUCTION=https://your-ngrok-url.ngrok.io
```

## 🎯 Логика работы

1. **Локально** - использует localhost URL
2. **На GitHub Pages** - использует ngrok URL
3. **Автоматическое переключение** по hostname
