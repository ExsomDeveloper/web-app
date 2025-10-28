"""
Сервис для работы с Kling.ai API
Вынесен в отдельный модуль для возможности быстрой замены на другой сервис
"""
import sys
import os
import time
import jwt
import base64
import requests
import logging
from typing import Optional, Dict, Any
from pathlib import Path

# Добавляем путь к модулям проекта для корректного импорта
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.config import KLING_ACCESS_KEY, KLING_SECRET_KEY, KLING_API_DOMAIN, UPLOAD_DIR

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class KlingService:
    """Сервис для работы с Kling.ai API"""
    
    def __init__(self):
        self.access_key = KLING_ACCESS_KEY
        self.secret_key = KLING_SECRET_KEY
        self.api_domain = KLING_API_DOMAIN
        # Убеждаемся, что папка загрузок существует (на случай изолированного запуска)
        try:
            UPLOAD_DIR.mkdir(exist_ok=True)
        except Exception:
            # Не прерываем работу, просто залогируем
            logger.warning("Не удалось создать папку uploads")
    
    def generate_jwt_token(self) -> str:
        """
        Генерация JWT токена для авторизации в Kling.ai
        
        Returns:
            str: JWT токен
        """
        headers = {
            "alg": "HS256",
            "typ": "JWT"
        }
        
        payload = {
            "iss": self.access_key,
            "exp": int(time.time()) + 1800,  # Токен действителен 30 минут
            "nbf": int(time.time()) - 5      # Начинает действовать через 5 секунд
        }
        
        token = jwt.encode(payload, self.secret_key, headers=headers)
        return token
    
    def get_authorization_header(self) -> str:
        """
        Получение заголовка Authorization для запросов к Kling.ai
        
        Returns:
            str: Authorization header в формате "Bearer <token>"
        """
        token = self.generate_jwt_token()
        return f"Bearer {token}"
    
    def get_base_url(self) -> str:
        """
        Получение базового URL API
        
        Returns:
            str: Базовый URL
        """
        return self.api_domain
    
    def image_to_base64(self, image_path: str) -> str:
        """
        Конвертация изображения в Base64 строку
        
        Args:
            image_path (str): Путь к изображению
            
        Returns:
            str: Base64 строка изображения
        """
        try:
            logger.info(f"Конвертирую изображение в Base64: {image_path}")
            image_path = Path(image_path)
            
            if not image_path.exists():
                raise FileNotFoundError(f"Файл не найден: {image_path}")
            
            with open(image_path, "rb") as image_file:
                image_data = image_file.read()
                base64_string = base64.b64encode(image_data).decode('utf-8')
                logger.info(f"Изображение успешно конвертировано в Base64. Размер: {len(base64_string)} символов")
                return base64_string
                
        except Exception as e:
            logger.error(f"Ошибка при конвертации изображения в Base64: {e}")
            raise

    def _save_bytes_to_file(self, data: bytes, filename: str) -> Path:
        """
        Сохранение байтов в файл в папке uploads

        Args:
            data (bytes): Данные изображения
            filename (str): Имя файла (без пути)

        Returns:
            Path: Полный путь к сохраненному файлу
        """
        save_path = UPLOAD_DIR / filename
        with open(save_path, "wb") as f:
            f.write(data)
        logger.info(f"Изображение сохранено: {save_path}")
        return save_path

    def save_image_from_base64(self, base64_string: str, filename: str = "tryon_result.png") -> Path:
        """
        Сохранение изображения из Base64 строки в uploads

        Args:
            base64_string (str): Base64 строка (без префикса data:)
            filename (str): Имя сохраняемого файла

        Returns:
            Path: Путь к сохраненному файлу
        """
        try:
            # Обрезаем возможный префикс data:image/...;base64,
            if "," in base64_string and base64_string.strip().startswith("data:"):
                base64_string = base64_string.split(",", 1)[1]

            logger.info("Сохраняю изображение из Base64 в uploads...")
            image_bytes = base64.b64decode(base64_string)
            return self._save_bytes_to_file(image_bytes, filename)
        except Exception as e:
            logger.error(f"Не удалось сохранить изображение из Base64: {e}")
            raise

    def download_and_save_image(self, url: str, filename: str = "tryon_result.png") -> Path:
        """
        Загрузка изображения по URL и сохранение в uploads

        Args:
            url (str): Ссылка на изображение
            filename (str): Имя сохраняемого файла

        Returns:
            Path: Путь к сохраненному файлу
        """
        try:
            logger.info(f"Скачиваю изображение по URL: {url}")
            r = requests.get(url, timeout=60)
            r.raise_for_status()
            return self._save_bytes_to_file(r.content, filename)
        except Exception as e:
            logger.error(f"Не удалось скачать изображение по URL: {e}")
            raise

    def try_save_result_from_response(self, response_data: Dict[str, Any], filename_prefix: str = "tryon_result") -> Optional[Path]:
        """
        Пытается найти результат изображения в ответе API и сохранить его в uploads.
        Поддерживает поля: image_base64, result_image, image, result, image_url, result_url, images[0].

        Returns:
            Optional[Path]: Путь к сохраненному файлу или None, если результата нет в ответе
        """
        if not response_data:
            return None

        data = response_data.get("data") or response_data

        # Возможные ключи для base64
        base64_keys = ["image_base64", "result_image", "image", "result"]
        for key in base64_keys:
            value = (data or {}).get(key)
            if isinstance(value, str) and len(value) > 100:  # эвристика
                filename = f"{filename_prefix}.png"
                try:
                    return self.save_image_from_base64(value, filename)
                except Exception:
                    pass

        # Возможные ключи для URL
        url_keys = ["image_url", "result_url", "url"]
        for key in url_keys:
            value = (data or {}).get(key)
            if isinstance(value, str) and value.startswith("http"):
                filename = f"{filename_prefix}.png"
                try:
                    return self.download_and_save_image(value, filename)
                except Exception:
                    pass

        # Массив изображений
        images = (data or {}).get("images") or (data or {}).get("results")
        if isinstance(images, list) and images:
            first = images[0]
            if isinstance(first, str):
                if first.startswith("http"):
                    return self.download_and_save_image(first, f"{filename_prefix}.png")
                elif len(first) > 100:
                    return self.save_image_from_base64(first, f"{filename_prefix}.png")

        logger.info("В ответе не найдено изображение для сохранения (ожидается по callback или отдельному запросу статуса)")
        return None
    
    def create_virtual_tryon_task(self, human_image_path: str, cloth_image_path: str, callback_url: Optional[str] = None) -> Dict[str, Any]:
        """
        Создание задачи виртуальной примерки в Kling AI
        
        Args:
            human_image_path (str): Путь к изображению человека
            cloth_image_path (str): Путь к изображению одежды
            callback_url (Optional[str]): URL для callback уведомлений
            
        Returns:
            Dict[str, Any]: Ответ от API
        """
        try:
            logger.info("Начинаю создание задачи виртуальной примерки")
            logger.info(f"Изображение человека: {human_image_path}")
            logger.info(f"Изображение одежды: {cloth_image_path}")
            
            # Конвертируем изображения в Base64
            human_image_base64 = self.image_to_base64(human_image_path)
            cloth_image_base64 = self.image_to_base64(cloth_image_path)
            
            # Подготавливаем данные запроса
            request_data = {
                "model_name": "kolors-virtual-try-on-v1",
                "human_image": human_image_base64,
                "cloth_image": cloth_image_base64
            }
            
            if callback_url:
                request_data["callback_url"] = callback_url
                logger.info(f"Callback URL установлен: {callback_url}")
            
            # Подготавливаем заголовки
            headers = {
                "Content-Type": "application/json",
                "Authorization": self.get_authorization_header()
            }
            
            # Формируем URL запроса
            url = f"{self.get_base_url()}/v1/images/kolors-virtual-try-on"
            logger.info(f"Отправляю запрос на URL: {url}")
            
            # Отправляем запрос
            logger.info("Отправляю POST запрос к Kling AI API...")
            response = requests.post(url, json=request_data, headers=headers, timeout=30)
            
            logger.info(f"Получен ответ от API. Статус код: {response.status_code}")
            
            if response.status_code == 200:
                response_data = response.json()
                logger.info("Задача успешно создана!")
                logger.info(f"Task ID: {response_data.get('data', {}).get('task_id', 'N/A')}")
                logger.info(f"Статус задачи: {response_data.get('data', {}).get('task_status', 'N/A')}")

                # Пытаемся сразу сохранить результат, если сервис вернул изображение синхронно
                saved_path = self.try_save_result_from_response(response_data, filename_prefix="tryon_result")
                if saved_path:
                    response_data["saved_file"] = str(saved_path)
                    logger.info(f"Результат сохранен в: {saved_path}")

                return response_data
            else:
                logger.error(f"Ошибка API: {response.status_code}")
                logger.error(f"Ответ сервера: {response.text}")
                
                # Специальная обработка ошибки недостатка средств
                try:
                    error_data = response.json()
                    if error_data.get('code') == 1102 and 'balance not enough' in error_data.get('message', ''):
                        logger.error("❌ НЕДОСТАТОЧНО СРЕДСТВ НА АККАУНТЕ KLING AI!")
                        logger.error("💳 Пополните баланс в панели управления Kling AI")
                        logger.error(f"Request ID: {error_data.get('request_id', 'N/A')}")
                except:
                    pass
                
                response.raise_for_status()
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Ошибка при отправке запроса: {e}")
            raise
        except Exception as e:
            logger.error(f"Неожиданная ошибка: {e}")
            raise


# Singleton instance
_kling_service: Optional[KlingService] = None


def get_kling_service() -> KlingService:
    """
    Получение singleton экземпляра KlingService
    
    Returns:
        KlingService: Экземпляр сервиса
    """
    global _kling_service
    if _kling_service is None:
        _kling_service = KlingService()
    return _kling_service


def test_virtual_tryon():
    """
    Тестовая функция для быстрого тестирования виртуальной примерки
    Использует изображения girl.jpg и longsleev.jpg из корневой папки backend
    """
    try:
        logger.info("Запуск тестовой функции виртуальной примерки")
        
        # Пути к тестовым изображениям
        backend_dir = Path(__file__).parent.parent
        human_image = backend_dir / "girl.jpg"
        cloth_image = backend_dir / "longsleev.jpg"
        
        # Проверяем существование файлов
        if not human_image.exists():
            logger.error(f"Файл не найден: {human_image}")
            logger.info("Поместите файл girl.jpg в папку backend/")
            return
            
        if not cloth_image.exists():
            logger.error(f"Файл не найден: {cloth_image}")
            logger.info("Поместите файл longsleev.jpg в папку backend/")
            return
        
        # Получаем сервис и создаем задачу
        service = get_kling_service()
        result = service.create_virtual_tryon_task(
            human_image_path=str(human_image),
            cloth_image_path=str(cloth_image)
        )
        
        # Если удалось сразу сохранить результат, покажем путь
        saved_file = result.get("saved_file") if isinstance(result, dict) else None
        if saved_file:
            logger.info(f"Изображение результата сохранено в: {saved_file}")
        else:
            logger.info("Результат пока не содержит изображение. Ожидайте callback или используйте опрос статуса.")
        
        logger.info("Тест завершен успешно!")
        logger.info(f"Результат: {result}")
        
    except Exception as e:
        logger.error(f"Ошибка в тестовой функции: {e}")


if __name__ == "__main__":
    # Если файл запущен напрямую, выполняем тест
    test_virtual_tryon()

