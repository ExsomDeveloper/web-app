from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pathlib import Path
import json

router = APIRouter(prefix="/api/products", tags=["products"])

# Путь к файлу с данными продуктов
PRODUCTS_FILE = Path("data/products.json")


@router.get("")
async def get_products():
    """
    Получение списка всех продуктов
    """
    try:
        if not PRODUCTS_FILE.exists():
            return JSONResponse({"products": []})
        
        with open(PRODUCTS_FILE, 'r', encoding='utf-8') as f:
            products = json.load(f)
        
        return JSONResponse({"products": products})
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при загрузке продуктов: {str(e)}")


@router.get("/{product_id}")
async def get_product(product_id: int):
    """
    Получение конкретного продукта по ID
    """
    try:
        if not PRODUCTS_FILE.exists():
            raise HTTPException(status_code=404, detail="Продукт не найден")
        
        with open(PRODUCTS_FILE, 'r', encoding='utf-8') as f:
            products = json.load(f)
        
        product = next((p for p in products if p['id'] == product_id), None)
        if not product:
            raise HTTPException(status_code=404, detail="Продукт не найден")
        
        return JSONResponse({"product": product})
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при загрузке продукта: {str(e)}")

