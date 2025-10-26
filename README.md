# Telegram Try-On Project

Проект для примерки одежды с использованием фотографий пользователя и вещей.

## Структура проекта

- `frontend/` - React приложение (TypeScript)
- `backend/` - FastAPI сервер (Python)
- `.vscode/` - Конфигурация VS Code для задач

## Быстрый запуск

### Вариант 1: Использование готовых скриптов

#### Windows (Batch файлы)
```bash
# Запустить только фронтенд
start-frontend.bat

# Запустить только бэкенд
start-backend.bat

# Запустить оба сервиса одновременно
start-both.bat
```

#### Windows (PowerShell)
```powershell
# Запустить только фронтенд
.\start-frontend.ps1

# Запустить только бэкенд
.\start-backend.ps1

# Запустить оба сервиса одновременно
.\start-both.ps1
```

### Вариант 2: Использование VS Code задач

1. Откройте проект в VS Code
2. Нажмите `Ctrl+Shift+P` (или `Cmd+Shift+P` на Mac)
3. Введите "Tasks: Run Task"
4. Выберите одну из задач:
   - `Start Frontend` - запустить фронтенд
   - `Start Backend` - запустить бэкенд
   - `Start Both (Frontend + Backend)` - запустить оба сервиса

### Вариант 3: Ручной запуск

#### Фронтенд
```bash
cd frontend
npm install  # только при первом запуске
npm start
```

#### Бэкенд
```bash
cd backend
pip install -r requirements.txt  # только при первом запуске
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Доступ к сервисам

После запуска сервисы будут доступны по адресам:

- **Фронтенд**: http://localhost:3000
- **Бэкенд API**: http://localhost:8000
- **API документация**: http://localhost:8000/docs

## API Endpoints

- `GET /` - Проверка работы API
- `GET /health` - Проверка здоровья сервиса
- `POST /upload/photo` - Загрузка одной фотографии
- `POST /process/tryon` - Обработка двух фотографий для примерки

## Требования

### Фронтенд
- Node.js (версия 16 или выше)
- npm

### Бэкенд
- Python 3.8 или выше
- pip

## Установка зависимостей

### Фронтенд
```bash
cd frontend
npm install
```

### Бэкенд
```bash
cd backend
pip install -r requirements.txt
```

## Разработка

Проект настроен для разработки с горячей перезагрузкой:
- Фронтенд автоматически перезагружается при изменении файлов
- Бэкенд автоматически перезагружается при изменении Python файлов

## Структура файлов

```
telegram-tryon/
├── frontend/                 # React приложение
│   ├── src/
│   │   ├── pages/           # Страницы приложения
│   │   ├── shared/          # Общие компоненты
│   │   └── ...
│   ├── package.json
│   └── ...
├── backend/                  # FastAPI сервер
│   ├── main.py              # Основной файл сервера
│   ├── requirements.txt     # Python зависимости
│   └── uploads/             # Папка для загруженных файлов
├── .vscode/
│   └── tasks.json           # Задачи VS Code
├── start-*.bat              # Batch скрипты для Windows
├── start-*.ps1              # PowerShell скрипты
└── README.md
```
