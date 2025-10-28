#!/usr/bin/env python3
"""
CLI команда для работы с Kling AI API
Позволяет вызывать функции через командную строку
"""
import sys
import os
import argparse
from pathlib import Path

# Добавляем путь к модулям проекта
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.kling import get_kling_service


def main():
    """Основная функция CLI"""
    parser = argparse.ArgumentParser(description='Kling AI Virtual Try-On CLI')
    parser.add_argument('--human-image', required=True, help='Путь к изображению человека')
    parser.add_argument('--cloth-image', required=True, help='Путь к изображению одежды')
    parser.add_argument('--callback-url', help='URL для callback уведомлений (опционально)')
    
    args = parser.parse_args()
    
    try:
        # Получаем сервис
        kling_service = get_kling_service()
        
        # Проверяем существование файлов
        human_path = Path(args.human_image)
        cloth_path = Path(args.cloth_image)
        
        if not human_path.exists():
            print(f"ОШИБКА: Файл с изображением человека не найден: {args.human_image}")
            sys.exit(1)
            
        if not cloth_path.exists():
            print(f"ОШИБКА: Файл с изображением одежды не найден: {args.cloth_image}")
            sys.exit(1)
        
        print("=" * 60)
        print("KLING AI VIRTUAL TRY-ON CLI")
        print("=" * 60)
        print(f"Изображение человека: {args.human_image}")
        print(f"Изображение одежды: {args.cloth_image}")
        if args.callback_url:
            print(f"Callback URL: {args.callback_url}")
        print("=" * 60)
        
        # Создаем задачу
        result = kling_service.create_virtual_tryon_task(
            human_image_path=args.human_image,
            cloth_image_path=args.cloth_image,
            callback_url=args.callback_url
        )
        
        print("\n✅ ЗАДАЧА УСПЕШНО СОЗДАНА!")
        print(f"Task ID: {result.get('data', {}).get('task_id', 'N/A')}")
        print(f"Статус: {result.get('data', {}).get('task_status', 'N/A')}")
        print(f"Создано: {result.get('data', {}).get('created_at', 'N/A')}")
        
    except Exception as e:
        print(f"\n❌ ОШИБКА: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
