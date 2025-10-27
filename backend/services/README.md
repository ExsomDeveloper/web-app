# Services Layer

Слой сервисов для работы с внешними API. Каждый сервис вынесен в отдельный модуль для возможности быстрой замены.

## Kling.ai Service

### Описание
Сервис для работы с Kling.ai API - генерация изображений для виртуальной примерки одежды.

### Файлы
- `kling.py` - основной модуль сервиса

### Основные методы

#### `generate_jwt_token() -> str`
Генерирует JWT токен для авторизации в Kling.ai по стандарту RFC 7519.

**Returns:**
- `str`: JWT токен

**Алгоритм:**
1. Создает заголовок с алгоритмом HS256
2. Создает payload с issuer (access key), expiration (текущее время + 30 минут), nbf (текущее время - 5 секунд)
3. Подписывает токен с использованием secret key

#### `get_authorization_header() -> str`
Возвращает заголовок Authorization для HTTP запросов.

**Returns:**
- `str`: Заголовок в формате "Bearer <token>"

#### `get_base_url() -> str`
Возвращает базовый URL API Kling.ai.

**Returns:**
- `str`: URL API (https://api-singapore.klingai.com)

### Использование

```python
from services.kling import get_kling_service

# Получить экземпляр сервиса (singleton)
kling_service = get_kling_service()

# Сгенерировать токен
token = kling_service.generate_jwt_token()

# Получить заголовок авторизации
auth_header = kling_service.get_authorization_header()

# Получить базовый URL
base_url = kling_service.get_base_url()
```

### Конфигурация

Настройки хранятся в `app/config.py`:
- `KLING_ACCESS_KEY` - Access Key для авторизации
- `KLING_SECRET_KEY` - Secret Key для подписи токена
- `KLING_API_DOMAIN` - Домен API

### Тестирование

Тестовый endpoint для проверки генерации токена:
```
GET /api/kling/token
```

Пример ответа:
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "authorization_header": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "api_domain": "https://api-singapore.klingai.com"
}
```

### Замена сервиса

Для замены Kling.ai на другой сервис:
1. Создайте новый файл в папке `services/` (например, `new_service.py`)
2. Реализуйте те же методы или создайте интерфейс
3. Замените импорты в роутерах
4. Обновите конфигурацию

### Зависимости

- `PyJWT==2.9.0` - для генерации JWT токенов

