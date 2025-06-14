#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json

def test_animal_category():
    """Comprehensive test of animal category configuration"""
    
    print("🧪 ТЕСТИРОВАНИЕ КАТЕГОРИИ ЖИВОТНЫЙ МИР")
    print("=" * 50)
    
    errors = []
    warnings = []
    success_count = 0
    
    # 1. Check main config file
    print("1️⃣ Проверяем основной файл конфигурации...")
    config_file = 'data/config/categories.json'
    if os.path.exists(config_file):
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        animals_category = None
        for cat in config['categories']:
            if cat['id'] == 'animals':
                animals_category = cat
                break
        
        if animals_category:
            print("   ✅ Категория 'animals' найдена в конфигурации")
            print(f"   📝 Название (RU): {animals_category['names']['ru']}")
            print(f"   📝 Название (EN): {animals_category['names']['en']}")
            print(f"   📁 Папка изображений: {animals_category['imageFolder']}")
            
            # Check correct names
            expected_names = {
                'ru': 'Животный мир',
                'en': 'Animal World',
                'es': 'Mundo Animal',
                'fr': 'Monde Animal'
            }
            
            names_correct = True
            for lang, expected_name in expected_names.items():
                actual_name = animals_category['names'].get(lang, '')
                if actual_name == expected_name:
                    print(f"   ✅ Название {lang.upper()}: {actual_name}")
                    success_count += 1
                else:
                    errors.append(f"Неправильное название {lang.upper()}: '{actual_name}', ожидалось '{expected_name}'")
                    names_correct = False
            
            if names_correct:
                success_count += 1
            
            # Check if files exist
            for lang, filename in animals_category['wordFiles'].items():
                filepath = f"data/words/{lang}/{filename}"
                if os.path.exists(filepath):
                    print(f"   ✅ Файл слов {lang}: {filename}")
                    success_count += 1
                else:
                    errors.append(f"Файл слов {lang} не найден: {filepath}")
        else:
            errors.append("Категория 'animals' не найдена в конфигурации")
    else:
        errors.append(f"Файл конфигурации не найден: {config_file}")
    
    # 2. Check image folder
    print("\n2️⃣ Проверяем папку изображений...")
    images_dir = 'data/images/animals'
    if os.path.exists(images_dir):
        images = [f for f in os.listdir(images_dir) if f.endswith('.png')]
        images.sort()  # Sort to ensure consistent order
        if images:
            print(f"   ✅ Папка изображений найдена: {len(images)} файлов")
            print(f"   📊 Диапазон: {images[0]} ... {images[-1]}")
            success_count += 1
        else:
            errors.append("Папка изображений пуста")
    else:
        errors.append(f"Папка изображений не найдена: {images_dir}")
    
    # 3. Check word files content
    print("\n3️⃣ Проверяем содержимое файлов слов...")
    languages = ['ru', 'en', 'es', 'fr']
    expected_translations = {
        'ru': 'ТРУБКОЗУБ',  # Should be Russian
        'en': 'AARDVARK',   # Should be English
        'es': 'OSO HORMIGUERO',  # Should be Spanish
        'fr': 'ORYCTÉROPE'  # Should be French
    }
    
    for lang in languages:
        file_path = f'data/words/{lang}/animals_COMPLETE.txt'
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            if lines:
                first_line = lines[0].strip()
                parts = first_line.split(' - ')
                if len(parts) >= 2:
                    first_word = parts[1].strip()
                    expected = expected_translations[lang]
                    if first_word == expected:
                        print(f"   ✅ {lang.upper()}: {len(lines)} слов, первое слово правильно: {first_word}")
                        success_count += 1
                    else:
                        warnings.append(f"{lang.upper()}: Первое слово '{first_word}', ожидалось '{expected}'")
                else:
                    errors.append(f"{lang.upper()}: Неправильный формат первой строки")
            else:
                errors.append(f"{lang.upper()}: Файл пуст")
        else:
            errors.append(f"{lang.upper()}: Файл не найден: {file_path}")
    
    # 4. Check image mappings
    print("\n4️⃣ Проверяем файлы маппинга изображений...")
    for lang in languages:
        mapping_file = f'data/image_mappings/animals_{lang}.json'
        if os.path.exists(mapping_file):
            with open(mapping_file, 'r', encoding='utf-8') as f:
                mappings = json.load(f)
            
            # Check first mapping
            if '1' in mappings:
                first_path = mappings['1']
                if first_path.startswith('animals/'):
                    print(f"   ✅ {lang.upper()}: {len(mappings)} маппингов, пути правильные")
                    success_count += 1
                else:
                    errors.append(f"{lang.upper()}: Неправильный путь в маппинге: {first_path}")
            else:
                errors.append(f"{lang.upper()}: Маппинг не содержит запись '1'")
        else:
            errors.append(f"{lang.upper()}: Файл маппинга не найден: {mapping_file}")
    
    # 5. Check for old wrong files
    print("\n5️⃣ Проверяем отсутствие неправильных файлов...")
    wrong_files = [
        'data/categories.json',
        'data/image_mappings/animal_world_ru.json',
        'data/words/ru/animal_world.txt'
    ]
    
    for wrong_file in wrong_files:
        if os.path.exists(wrong_file):
            warnings.append(f"Найден старый неправильный файл: {wrong_file}")
        else:
            print(f"   ✅ Старый файл удален: {wrong_file}")
            success_count += 1
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ:")
    print(f"   ✅ Успешных проверок: {success_count}")
    print(f"   ❌ Ошибок: {len(errors)}")
    print(f"   ⚠️ Предупреждений: {len(warnings)}")
    
    if errors:
        print("\n❌ ОШИБКИ:")
        for error in errors:
            print(f"   • {error}")
    
    if warnings:
        print("\n⚠️ ПРЕДУПРЕЖДЕНИЯ:")
        for warning in warnings:
            print(f"   • {warning}")
    
    if not errors:
        print(f"\n🎉 ВСЁ ОТЛИЧНО! Категория 'Животный мир' настроена правильно!")
        print(f"   🌐 Игра доступна по адресу: http://localhost:8000")
        print(f"   🔧 Для отладки используйте: http://localhost:8000/tools/debug.html")
    else:
        print(f"\n🔧 Нужно исправить {len(errors)} ошибок")
    
    return len(errors) == 0

if __name__ == "__main__":
    test_animal_category() 