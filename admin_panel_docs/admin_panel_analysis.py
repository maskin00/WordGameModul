#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json

def analyze_admin_panel():
    """Анализ потенциальных проблем в админ-панели"""
    
    print("🔧 АНАЛИЗ АДМИН-ПАНЕЛИ")
    print("=" * 50)
    
    issues = []
    warnings = []
    
    # 1. Проверка структуры файлов
    print("📁 Проверка структуры файлов...")
    
    required_files = [
        'modules/AdminPanel.js',
        'modules/DataManager.js', 
        'data/config/categories.json',
        'data/config/languages.json'
    ]
    
    for file_path in required_files:
        if not os.path.exists(file_path):
            issues.append(f"Отсутствует файл: {file_path}")
        else:
            print(f"   ✅ {file_path}")
    
    # 2. Проверка конфигурации категорий
    print("\n📋 Проверка конфигурации категорий...")
    
    try:
        with open('data/config/categories.json', 'r', encoding='utf-8') as f:
            categories = json.load(f)
        
        print(f"   📊 Найдено категорий: {len(categories)}")
        
        for category in categories:
            if 'id' not in category:
                issues.append(f"Категория без ID: {category}")
            if 'name' not in category:
                issues.append(f"Категория без названия: {category.get('id', 'unknown')}")
            
            # Проверяем структуру названий
            if isinstance(category.get('name'), dict):
                langs = list(category['name'].keys())
                print(f"   🌐 {category.get('id', 'unknown')}: языки {langs}")
            else:
                warnings.append(f"Категория {category.get('id', 'unknown')} имеет старый формат названия")
                
    except Exception as e:
        issues.append(f"Ошибка чтения categories.json: {e}")
    
    # 3. Проверка существующих файлов слов
    print("\n📝 Проверка файлов слов...")
    
    word_files_found = 0
    languages = ['ru', 'en', 'es', 'fr']
    
    for lang in languages:
        lang_dir = f'data/words/{lang}'
        if os.path.exists(lang_dir):
            files = [f for f in os.listdir(lang_dir) if f.endswith('.txt')]
            word_files_found += len(files)
            print(f"   🔤 {lang}: {len(files)} файлов")
            
            # Проверяем формат файлов
            for file in files[:3]:  # Проверяем первые 3 файла
                file_path = os.path.join(lang_dir, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        first_line = f.readline().strip()
                        if not first_line:
                            warnings.append(f"Пустой файл: {file_path}")
                        elif ' - ' not in first_line:
                            warnings.append(f"Неверный формат в {file}: {first_line[:50]}...")
                except Exception as e:
                    issues.append(f"Ошибка чтения {file_path}: {e}")
        else:
            warnings.append(f"Отсутствует директория: {lang_dir}")
    
    print(f"   📊 Всего файлов слов: {word_files_found}")
    
    # 4. Проверка изображений
    print("\n🖼️ Проверка изображений...")
    
    image_dirs = []
    if os.path.exists('data/images'):
        image_dirs = [d for d in os.listdir('data/images') if os.path.isdir(f'data/images/{d}')]
        print(f"   📁 Найдено директорий изображений: {len(image_dirs)}")
        
        for img_dir in image_dirs:
            img_path = f'data/images/{img_dir}'
            images = [f for f in os.listdir(img_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
            print(f"   🖼️ {img_dir}: {len(images)} изображений")
            
            # Проверяем формат имен файлов
            invalid_names = []
            for img in images[:5]:  # Проверяем первые 5
                if not img.split('.')[0].replace('-', '').replace('_', '').isdigit():
                    invalid_names.append(img)
            
            if invalid_names:
                warnings.append(f"Неверные имена файлов в {img_dir}: {invalid_names}")
    else:
        issues.append("Отсутствует директория data/images")
    
    # 5. Анализ кода AdminPanel.js
    print("\n🔍 Анализ кода AdminPanel.js...")
    
    try:
        with open('modules/AdminPanel.js', 'r', encoding='utf-8') as f:
            admin_code = f.read()
        
        # Проверяем ключевые методы
        required_methods = [
            'validateCategory',
            'saveCategory', 
            'handleWordsFile',
            'handleImagesFiles',
            'showValidationResult'
        ]
        
        for method in required_methods:
            if method in admin_code:
                print(f"   ✅ Метод {method} найден")
            else:
                issues.append(f"Отсутствует метод: {method}")
        
        # Проверяем обработчики событий
        event_handlers = [
            'validateButton',
            'saveButton',
            'wordsFile',
            'imagesFiles'
        ]
        
        for handler in event_handlers:
            if f"getElementById('{handler}')" in admin_code:
                print(f"   ✅ Обработчик {handler} найден")
            else:
                warnings.append(f"Возможно отсутствует обработчик: {handler}")
                
    except Exception as e:
        issues.append(f"Ошибка анализа AdminPanel.js: {e}")
    
    # 6. Проверка методов DataManager
    print("\n💾 Проверка методов DataManager...")
    
    try:
        with open('modules/DataManager.js', 'r', encoding='utf-8') as f:
            data_code = f.read()
        
        required_data_methods = [
            'validateWordsFile',
            'validateImages',
            'addCategory',
            'parseWordsFile'
        ]
        
        for method in required_data_methods:
            if method in data_code:
                print(f"   ✅ Метод {method} найден")
            else:
                issues.append(f"Отсутствует метод в DataManager: {method}")
                
    except Exception as e:
        issues.append(f"Ошибка анализа DataManager.js: {e}")
    
    # 7. Потенциальные проблемы
    print("\n⚠️ Потенциальные проблемы:")
    
    potential_issues = [
        "AdminPanel ожидает старый формат данных категорий",
        "Метод addCategory может не сохранять файлы на сервер",
        "Отсутствует серверная часть для сохранения файлов",
        "Валидация изображений работает только с File объектами",
        "Нет проверки существующих категорий при добавлении"
    ]
    
    for issue in potential_issues:
        warnings.append(issue)
    
    # Вывод результатов
    print("\n" + "=" * 50)
    print("📊 РЕЗУЛЬТАТЫ АНАЛИЗА")
    print("=" * 50)
    
    if issues:
        print(f"❌ КРИТИЧЕСКИЕ ПРОБЛЕМЫ ({len(issues)}):")
        for i, issue in enumerate(issues, 1):
            print(f"   {i}. {issue}")
    else:
        print("✅ Критических проблем не найдено")
    
    if warnings:
        print(f"\n⚠️ ПРЕДУПРЕЖДЕНИЯ ({len(warnings)}):")
        for i, warning in enumerate(warnings, 1):
            print(f"   {i}. {warning}")
    else:
        print("\n✅ Предупреждений нет")
    
    # Рекомендации
    print(f"\n💡 РЕКОМЕНДАЦИИ:")
    print("   1. Добавить серверную часть для сохранения файлов")
    print("   2. Обновить логику addCategory для новой структуры")
    print("   3. Добавить проверку дубликатов категорий")
    print("   4. Улучшить валидацию форматов файлов")
    print("   5. Добавить предварительный просмотр результатов")
    
    return len(issues) == 0

if __name__ == "__main__":
    success = analyze_admin_panel()
    exit(0 if success else 1) 