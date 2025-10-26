from pydantic import BaseModel


class TryOnRequest(BaseModel):
    """Модель запроса для примерки"""
    photo1: str  # Base64 string
    photo2: str  # Base64 string

