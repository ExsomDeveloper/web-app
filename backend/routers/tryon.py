from fastapi import APIRouter, HTTPException, File, UploadFile
from fastapi.responses import JSONResponse
from pathlib import Path
import base64
import asyncio
import shutil

from schemas.tryon import TryOnRequest
from services.kling import get_kling_service

router = APIRouter(prefix="/api", tags=["tryon"])

# Путь к файлу profile.png
PROFILE_PNG = Path("profile.png")

# Папка для загруженных файлов
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@router.get("/kling/token")
async def get_kling_token():
    """
    Тестовый endpoint для получения токена Kling.ai
    """
    try:
        kling_service = get_kling_service()
        token = kling_service.generate_jwt_token()
        auth_header = kling_service.get_authorization_header()
        
        return JSONResponse({
            "token": token,
            "authorization_header": auth_header,
            "api_domain": kling_service.get_base_url()
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при генерации токена: {str(e)}")


@router.post("/tryon")
async def tryon(request: TryOnRequest):
    """
    Получение двух изображений в Base64 и возврат результата
    """
    try:
        # Проверка наличия изображений
        if not request.photo1 or not request.photo2:
            raise HTTPException(status_code=400, detail="Оба изображения обязательны")
        
        # Декодирование Base64 для проверки
        try:
            base64.b64decode(request.photo1)
            base64.b64decode(request.photo2)
        except Exception:
            raise HTTPException(status_code=400, detail="Неверный формат Base64")
        
        # Имитация обработки с задержкой 3 секунды
        await asyncio.sleep(3)
        
        # Проверка наличия файла profile.png
        if not PROFILE_PNG.exists():
            raise HTTPException(status_code=500, detail="Файл profile.png не найден")
        
        # Чтение файла profile.png и конвертация в Base64
        with open(PROFILE_PNG, 'rb') as f:
            image_data = f.read()
            image_base64 = base64.b64encode(image_data).decode('utf-8')
        
        return JSONResponse({
            "message": "Примерка завершена",
            "result_image": image_base64
        })
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при обработке: {str(e)}")


@router.post("/upload/photo")
async def upload_photo(file: UploadFile = File(...)):
    """
    Загрузка фотографии пользователя или вещи
    """
    try:
        # Проверка типа файла
        if not file.content_type or not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="Файл должен быть изображением")
        
        # Сохранение файла
        file_path = UPLOAD_DIR / file.filename
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        return JSONResponse({
            "message": "Файл успешно загружен",
            "filename": file.filename,
            "size": file_path.stat().st_size
        })
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при загрузке файла: {str(e)}")


@router.post("/process/tryon")
async def process_tryon(photo1: UploadFile = File(...), photo2: UploadFile = File(...)):
    """
    Обработка двух фотографий для примерки
    """
    try:
        # Проверка типов файлов
        for file in [photo1, photo2]:
            if not file.content_type or not file.content_type.startswith('image/'):
                raise HTTPException(status_code=400, detail="Все файлы должны быть изображениями")
        
        # Сохранение файлов
        photo1_path = UPLOAD_DIR / f"user_{photo1.filename}"
        photo2_path = UPLOAD_DIR / f"item_{photo2.filename}"
        
        with open(photo1_path, "wb") as buffer:
            shutil.copyfileobj(photo1.file, buffer)
        
        with open(photo2_path, "wb") as buffer:
            shutil.copyfileobj(photo2.file, buffer)
        
        # TODO: Здесь будет логика обработки изображений
        # Пока что возвращаем заглушку
        result = {
            "message": "Обработка завершена",
            "user_photo": photo1.filename,
            "item_photo": photo2.filename,
            "result_url": "placeholder_result.jpg"
        }
        
        return JSONResponse(result)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при обработке: {str(e)}")

