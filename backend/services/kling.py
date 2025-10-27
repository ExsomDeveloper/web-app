"""
Сервис для работы с Kling.ai API
Вынесен в отдельный модуль для возможности быстрой замены на другой сервис
"""
import time
import jwt
from typing import Optional
from app.config import KLING_ACCESS_KEY, KLING_SECRET_KEY, KLING_API_DOMAIN


class KlingService:
    """Сервис для работы с Kling.ai API"""
    
    def __init__(self):
        self.access_key = KLING_ACCESS_KEY
        self.secret_key = KLING_SECRET_KEY
        self.api_domain = KLING_API_DOMAIN
    
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

