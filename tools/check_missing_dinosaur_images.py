#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

def check_missing_images():
    """Check for missing dinosaur images"""
    
    print("🦕 ПРОВЕРКА ОТСУТСТВУЮЩИХ ИЗОБРАЖЕНИЙ ДИНОЗАВРОВ")
    print("=" * 50)
    
    # Читаем файл слов
    with open('data/words/ru/dinosaurs_COMPLETE.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Получаем список существующих изображений
    existing_images = set(os.listdir('data/images/dinosaurs'))
    
    missing_images = []
    existing_count = 0
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        parts = line.split(' - ')
        if len(parts) >= 3:
            image_file = parts[2]
            
            if image_file in existing_images:
                existing_count += 1
            else:
                missing_images.append(image_file)
                print(f"❌ Отсутствует: {image_file}")
    
    print(f"\n📊 СТАТИСТИКА:")
    print(f"   ✅ Существующих изображений: {existing_count}")
    print(f"   ❌ Отсутствующих изображений: {len(missing_images)}")
    print(f"   📁 Всего записей в файле: {len(lines)}")
    print(f"   📁 Всего файлов в папке: {len(existing_images)}")
    
    if missing_images:
        print(f"\n🔧 ОТСУТСТВУЮЩИЕ ИЗОБРАЖЕНИЯ:")
        for img in missing_images:
            print(f"   - {img}")
    else:
        print(f"\n✅ ВСЕ ИЗОБРАЖЕНИЯ НА МЕСТЕ!")

if __name__ == "__main__":
    check_missing_images() 