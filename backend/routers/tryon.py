from fastapi import APIRouter, HTTPException, File, UploadFile
from fastapi.responses import JSONResponse
from pathlib import Path
import base64
import asyncio
import shutil
import tempfile
import logging
from typing import Dict, Any

from schemas.tryon import TryOnRequest
from services.kling import get_kling_service
from app.config import KLING_CALLBACK_URL, API_BASE_URL

# Настройка логирования
logger = logging.getLogger(__name__)

# Глобальное хранилище для ожидающих результатов
pending_tasks: Dict[str, Dict[str, Any]] = {}

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
    Получение двух изображений в Base64, отправка в Kling AI через callback и возврат результата
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
        
        logger.info("Начинаю обработку виртуальной примерки через Kling AI с callback")
        
        # Создаем временные файлы для изображений
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp_file1:
            temp_file1.write(base64.b64decode(request.photo1))
            temp_path1 = temp_file1.name
            
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp_file2:
            temp_file2.write(base64.b64decode(request.photo2))
            temp_path2 = temp_file2.name
        
        try:
            # Получаем сервис Kling AI
            kling_service = get_kling_service()
            
            # Создаем задачу виртуальной примерки с callback URL
            callback_url = KLING_CALLBACK_URL
            
            logger.info("Отправляю запрос в Kling AI с callback...")
            task_response = kling_service.create_virtual_tryon_task(
                human_image_path=temp_path1,
                cloth_image_path=temp_path2,
                callback_url=callback_url
            )
            
            task_id = task_response.get('data', {}).get('task_id')
            if not task_id:
                raise HTTPException(status_code=500, detail="Не удалось получить task_id от Kling AI")
            
            logger.info(f"Задача создана с ID: {task_id}")
            
            # Создаем событие для ожидания callback
            event = asyncio.Event()
            pending_tasks[task_id] = {
                'event': event,
                'result': None
            }
            
            # Ждем callback (максимум 5 минут)
            logger.info("Ожидаю callback от Kling AI...")
            try:
                await asyncio.wait_for(event.wait(), timeout=300)  # 5 минут
                
                # Получаем результат
                result = pending_tasks[task_id]['result']
                
                if result and result['status'] == 'success':
                    # Читаем сохраненный файл и конвертируем в Base64
                    image_path = result['image_path']
                    with open(image_path, 'rb') as f:
                        result_image_data = f.read()
                        result_image_base64 = base64.b64encode(result_image_data).decode('utf-8')
                    
                    logger.info("Результат получен через callback!")
                    
                    return JSONResponse({
                        "message": "Примерка завершена успешно",
                        "result_image": result_image_base64,
                        "task_id": task_id,
                        "saved_file": image_path
                    })
                    
                elif result and result['status'] == 'error':
                    raise HTTPException(status_code=500, detail=f"Ошибка Kling AI: {result['error']}")
                else:
                    raise HTTPException(status_code=500, detail="Неожиданный результат от callback")
                    
            except asyncio.TimeoutError:
                logger.error("Превышено время ожидания callback")
                raise HTTPException(status_code=500, detail="Превышено время ожидания результата")
            finally:
                # Очищаем из хранилища
                if task_id in pending_tasks:
                    del pending_tasks[task_id]
            
        finally:
            # Удаляем временные файлы
            try:
                Path(temp_path1).unlink(missing_ok=True)
                Path(temp_path2).unlink(missing_ok=True)
            except Exception as e:
                logger.warning(f"Не удалось удалить временные файлы: {e}")
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка при обработке виртуальной примерки: {e}")
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


@router.post("/kling/callback")
async def kling_callback(request: dict):
    """
    Callback endpoint для получения результатов от Kling AI
    Обрабатывает протокол callback согласно документации Kling AI
    """
    try:
        logger.info(f"Получен callback от Kling AI: {request}")
        
        task_id = request.get('task_id')
        task_status = request.get('task_status')
        
        if not task_id:
            logger.error("Callback без task_id")
            return JSONResponse({"error": "Missing task_id"}, status_code=400)
        
        logger.info(f"Обрабатываю callback для задачи {task_id}, статус: {task_status}")
        
        # Если задача завершена успешно
        if task_status == 'succeed':
            task_result = request.get('task_result', {})
            images = task_result.get('images', [])
            
            if images:
                # Берем первое изображение
                first_image = images[0]
                image_url = first_image.get('url')
                
                if image_url:
                    logger.info(f"Получен URL изображения: {image_url}")
                    
                    # Получаем сервис Kling AI
                    kling_service = get_kling_service()
                    
                    # Скачиваем и сохраняем изображение
                    saved_path = kling_service.download_and_save_image(
                        image_url, 
                        f"tryon_result_{task_id}.png"
                    )
                    
                    logger.info(f"Изображение сохранено: {saved_path}")
                    
                    # Уведомляем ожидающие задачи
                    if task_id in pending_tasks:
                        pending_tasks[task_id]['result'] = {
                            'status': 'success',
                            'image_path': str(saved_path),
                            'image_url': image_url
                        }
                        pending_tasks[task_id]['event'].set()
                        logger.info(f"Уведомлен ожидающий запрос для задачи {task_id}")
                    
                    return JSONResponse({
                        "message": "Callback обработан успешно",
                        "task_id": task_id,
                        "saved_file": str(saved_path)
                    })
                else:
                    logger.error("URL изображения не найден в callback")
            else:
                logger.error("Изображения не найдены в callback")
                
        elif task_status == 'failed':
            task_status_msg = request.get('task_status_msg', 'Unknown error')
            logger.error(f"Задача {task_id} завершилась с ошибкой: {task_status_msg}")
            
            # Уведомляем ожидающие задачи об ошибке
            if task_id in pending_tasks:
                pending_tasks[task_id]['result'] = {
                    'status': 'error',
                    'error': task_status_msg
                }
                pending_tasks[task_id]['event'].set()
            
            return JSONResponse({
                "message": "Задача завершилась с ошибкой",
                "task_id": task_id,
                "error": task_status_msg
            })
        
        else:
            logger.info(f"Задача {task_id} в процессе, статус: {task_status}")
            return JSONResponse({
                "message": "Статус обновлен",
                "task_id": task_id,
                "status": task_status
            })
            
    except Exception as e:
        logger.error(f"Ошибка при обработке callback: {e}")
        return JSONResponse({"error": str(e)}, status_code=500)

