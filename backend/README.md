# Backend Architecture

## Структура проекта

```
backend/
├── main.py              # Точка входа приложения
├── app/                 # Основные компоненты приложения
│   ├── __init__.py
│   └── config.py       # Конфигурация приложения
├── routers/             # API роутеры
│   ├── __init__.py
│   ├── products.py      # Роуты для работы с продуктами
│   └── tryon.py         # Роуты для примерки одежды
├── schemas/             # Pydantic модели
│   ├── __init__.py
│   └── tryon.py         # Модели для tryon API
├── services/            # Сервисы для внешних API
│   ├── __init__.py
│   ├── kling.py         # Сервис для Kling.ai
│   └── README.md         # Документация сервисов
├── data/                # Данные
│   └── products.json    # Список продуктов
├── uploads/             # Загруженные файлы
├── profile.png          # Примерочный результат
└── venv/                # Виртуальное окружение
```

## Основные компоненты

### `main.py`
Точка входа приложения. Создает FastAPI instance, настраивает CORS middleware и подключает роутеры.

### `app/config.py`
Содержит все конфигурационные константы:
- Пути к файлам и директориям
- Настройки CORS
- Настройки сервера (host, port)

### `routers/products.py`
API endpoints для работы с продуктами:
- `GET /api/products` - получение списка всех продуктов
- `GET /api/products/{product_id}` - получение конкретного продукта

### `routers/tryon.py`
API endpoints для примерки одежды:
- `GET /api/kling/token` - тестовый endpoint для получения токена Kling.ai
- `POST /api/tryon` - обработка двух изображений в Base64
- `POST /api/upload/photo` - загрузка фотографии
- `POST /api/process/tryon` - обработка фотографий для примерки

### `schemas/tryon.py`
Pydantic модели для валидации данных:
- `TryOnRequest` - модель запроса для примерки

### `services/kling.py`
Сервис для работы с Kling.ai API:
- `KlingService` - класс для генерации изображений
- `generate_jwt_token()` - генерация JWT токена для авторизации
- `get_authorization_header()` - получение заголовка Authorization
- Подробнее см. `services/README.md`

## Запуск

```bash
python main.py
```

Или используйте скрипты:
- `start-backend.bat` / `start-backend.ps1` (Windows)
- `start-both.bat` / `start-both.ps1` (для запуска обоих серверов)

## API Documentation

После запуска сервера документация доступна по адресу:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

