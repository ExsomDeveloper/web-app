from pathlib import Path

# Базовый путь проекта
BASE_DIR = Path(__file__).parent.parent

# Папка для загруженных файлов
UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

# Путь к файлу с данными продуктов
PRODUCTS_FILE = BASE_DIR / "data" / "products.json"

# Путь к файлу profile.png
PROFILE_PNG = BASE_DIR / "profile.png"

# Настройки CORS
CORS_ORIGINS = ["http://localhost:3000"]

# Настройки сервера
HOST = "0.0.0.0"
PORT = 8000

