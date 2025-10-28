from pathlib import Path
import os
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

# Базовый путь проекта
BASE_DIR = Path(__file__).parent.parent

# Папка для загруженных файлов
UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

# Путь к файлу с данными продуктов
PRODUCTS_FILE = BASE_DIR / "data" / "products.json"

# Путь к файлу profile.png
PROFILE_PNG = BASE_DIR / "profile.png"

# Настройки окружения
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")  # development, production

# Базовые URL для API
if ENVIRONMENT == "development":
    # Локальная разработка с ngrok
    API_BASE_URL = os.getenv("API_BASE_URL", "https://unslighted-complaisantly-erma.ngrok-free.dev")
    FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")
else:
    # Продакшн
    API_BASE_URL = os.getenv("API_BASE_URL", "https://your-domain.com")
    FRONTEND_URL = os.getenv("FRONTEND_URL", "https://your-frontend-domain.com")

# Настройки CORS
CORS_ORIGINS = [FRONTEND_URL, "http://localhost:3000"]

# Настройки сервера
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 8000))

# Настройки Kling.ai API
KLING_ACCESS_KEY = os.getenv("KLING_ACCESS_KEY", "AkFBemPhJ4LHfFJLL3aCTGKPaGPRNMEA")
KLING_SECRET_KEY = os.getenv("KLING_SECRET_KEY", "nykRgmfLAparCKF3Gg3nC3tmBkYrTftF")
KLING_API_DOMAIN = os.getenv("KLING_API_DOMAIN", "https://api-singapore.klingai.com")

# Callback URL для Kling AI
KLING_CALLBACK_URL = f"{API_BASE_URL}/api/kling/callback"
