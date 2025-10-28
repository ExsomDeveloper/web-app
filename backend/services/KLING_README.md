# Kling AI Virtual Try-On Service

Этот модуль предоставляет функциональность для работы с Kling AI API для создания виртуальной примерки одежды.

## Возможности

- ✅ Конвертация изображений в Base64
- ✅ Создание задач виртуальной примерки через Kling AI API
- ✅ Подробное логирование всех операций
- ✅ CLI команды для удобного использования
- ✅ Тестовая функция для быстрого тестирования

## Использование

### 1. Через Python код

```python
from services.kling import get_kling_service

# Получаем сервис
service = get_kling_service()

# Создаем задачу виртуальной примерки
result = service.create_virtual_tryon_task(
    human_image_path="path/to/human.jpg",
    cloth_image_path="path/to/cloth.jpg",
    callback_url="https://your-callback-url.com"  # опционально
)

print(f"Task ID: {result['data']['task_id']}")
```

### 2. Через CLI команду

#### Windows (PowerShell):
```powershell
.\run_kling_cli.ps1 girl.jpg longsleev.jpg
```

#### Windows (Batch):
```cmd
run_kling_cli.bat girl.jpg longsleev.jpg
```

#### Прямой вызов Python CLI:
```bash
python cli_kling.py --human-image girl.jpg --cloth-image longsleev.jpg
```

### 3. Тестовая функция

Для быстрого тестирования с изображениями `girl.jpg` и `longsleev.jpg`:

```bash
python services/kling.py
```

## Структура ответа API

```json
{
  "code": 0,
  "message": "string",
  "request_id": "string",
  "data": {
    "task_id": "string",
    "task_status": "submitted|processing|succeed|failed",
    "created_at": 1722769557708,
    "updated_at": 1722769557708
  }
}
```

## Логирование

Все операции логируются в консоль с подробной информацией:
- Конвертация изображений в Base64
- Отправка запросов к API
- Получение ответов
- Ошибки и исключения

## Требования

- Python 3.7+
- requests
- PyJWT
- pathlib (встроенный)

## Настройка

Убедитесь, что в `app/config.py` настроены следующие переменные:
- `KLING_ACCESS_KEY` - ключ доступа к Kling AI
- `KLING_SECRET_KEY` - секретный ключ
- `KLING_API_DOMAIN` - домен API

## Примеры использования

### Базовое использование
```python
from services.kling import get_kling_service

service = get_kling_service()
result = service.create_virtual_tryon_task("human.jpg", "shirt.jpg")
```

### С callback URL
```python
result = service.create_virtual_tryon_task(
    "human.jpg", 
    "shirt.jpg", 
    callback_url="https://myapp.com/webhook"
)
```

### Обработка ошибок
```python
try:
    result = service.create_virtual_tryon_task("human.jpg", "shirt.jpg")
    print("Задача создана:", result['data']['task_id'])
except FileNotFoundError as e:
    print(f"Файл не найден: {e}")
except Exception as e:
    print(f"Ошибка: {e}")
```
