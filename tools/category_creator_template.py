#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🛠️ УНИВЕРСАЛЬНЫЙ ШАБЛОН ДЛЯ СОЗДАНИЯ КАТЕГОРИЙ

Этот скрипт служит шаблоном для системного создания новых категорий игры.
Следует принципам из DEVELOPMENT_GUIDELINES.md

ИСПОЛЬЗОВАНИЕ:
1. Скопируйте этот файл
2. Измените параметры в функции main()
3. Добавьте переводы в create_translations()
4. Запустите скрипт

ПРИМЕР УСПЕШНОГО ИСПОЛЬЗОВАНИЯ:
- Категория "Динозавры" - 122 изображения, 4 языка

ВАЖНЫЕ УРОКИ ИЗ ОПЫТА СОЗДАНИЯ ДИНОЗАВРОВ:
1. Проверяйте расширения файлов - система автоматически добавляет .png для новых категорий
2. Добавляйте обработку новых категорий в DataManager.js (строки ~55 и ~210)
3. Создавайте правильные русские переводы сразу, не оставляйте английские названия
4. Проверяйте соответствие количества изображений и записей в файлах слов
5. Тестируйте загрузку изображений после создания категории
"""

import os
import json
import shutil
from pathlib import Path

def create_category(category_config):
    """
    Системное создание категории с учетом всех рекомендаций
    
    Args:
        category_config (dict): Конфигурация категории
    """
    
    print(f"🎯 СОЗДАНИЕ КАТЕГОРИИ '{category_config['names']['ru'].upper()}'")
    print("=" * 60)
    
    # 1. АНАЛИЗ - Проверяем исходные данные
    source_dir = Path(category_config['source_images_path'])
    if not source_dir.exists():
        print(f"❌ Папка {source_dir} не найдена!")
        return False
    
    # Получаем список изображений
    image_files = []
    for ext in category_config.get('image_extensions', ['*.jpg', '*.jpeg', '*.png']):
        image_files.extend(source_dir.glob(ext))
    
    # Исключаем служебные файлы
    exclude_patterns = category_config.get('exclude_patterns', ['parse_*', '.*'])
    for pattern in exclude_patterns:
        image_files = [f for f in image_files if not f.name.startswith(pattern.replace('*', ''))]
    
    image_files.sort()
    
    print(f"📊 Найдено {len(image_files)} изображений")
    
    # 2. ПЛАНИРОВАНИЕ - Получаем переводы
    translations = category_config.get('translations', {})
    
    # 3. РЕАЛИЗАЦИЯ - Создаем все необходимые файлы
    
    # 3.1 Создаем папку для изображений в проекте
    target_images_dir = Path(f"data/images/{category_config['id']}")
    target_images_dir.mkdir(parents=True, exist_ok=True)
    
    # 3.2 Копируем и переименовываем изображения
    category_data = []
    for i, image_file in enumerate(image_files, 1):
        # Извлекаем название из имени файла
        item_name = image_file.stem
        
        # Очищаем название
        clean_name = clean_item_name(item_name, category_config.get('name_cleaning_rules', {}))
        
        # Создаем новое имя файла
        new_filename = f"{i:03d}-{clean_name.lower().replace(' ', '_')}.jpg"
        target_path = target_images_dir / new_filename
        
        # Копируем файл
        try:
            shutil.copy2(image_file, target_path)
            print(f"📁 {image_file.name} → {new_filename}")
        except Exception as e:
            print(f"⚠️ Ошибка копирования {image_file.name}: {e}")
            continue
        
        # Сохраняем данные для словарных файлов
        category_data.append({
            'id': i,
            'name': clean_name,
            'filename': new_filename,
            'translations': translations.get(clean_name.lower(), {})
        })
    
    print(f"✅ Скопировано {len(category_data)} изображений")
    
    # 3.3 Создаем словарные файлы для всех языков
    create_word_files(category_data, category_config)
    
    # 3.4 Обновляем конфигурацию категорий
    update_categories_config(category_config)
    
    # 3.5 УРОК ИЗ ДИНОЗАВРОВ: Автоматически обновляем DataManager.js
    fix_datamanager_for_new_category(category_config['id'])
    
    # 3.6 УРОК ИЗ ДИНОЗАВРОВ: Создаем шаблон русских переводов
    create_russian_translations_template(category_data, category_config)
    
    # 4. ТЕСТИРОВАНИЕ - Проверяем созданные файлы
    validate_created_files(category_data, category_config)
    
    print(f"\n🎉 КАТЕГОРИЯ '{category_config['names']['ru'].upper()}' УСПЕШНО СОЗДАНА!")
    print(f"   📁 Изображений: {len(category_data)}")
    print(f"   📝 Словарных файлов: 4 языка")
    print(f"   ⚙️ Конфигурация: обновлена")
    
    return True

def clean_item_name(name, cleaning_rules):
    """Очищает название элемента от лишних символов"""
    clean = name.replace('_', ' ').replace('-', ' ')
    
    # Применяем правила очистки
    for rule in cleaning_rules.get('remove_patterns', []):
        clean = clean.replace(rule, '')
    
    # Убираем специальные префиксы/суффиксы
    if cleaning_rules.get('remove_i_wrapper', False):
        if clean.startswith('i') and clean.endswith('i'):
            clean = clean[1:-1]
    
    # Первая буква заглавная
    return clean.strip().title()

def create_word_files(category_data, category_config):
    """Создает словарные файлы для всех языков"""
    languages = {
        'ru': 'русский',
        'en': 'английский', 
        'es': 'испанский',
        'fr': 'французский'
    }
    
    for lang_code, lang_name in languages.items():
        print(f"📝 Создаю словарный файл для {lang_name} языка...")
        
        # Создаем папку если не существует
        lang_dir = Path(f"data/words/{lang_code}")
        lang_dir.mkdir(parents=True, exist_ok=True)
        
        # Создаем файл
        file_path = lang_dir / f"{category_config['id']}_COMPLETE.txt"
        
        with open(file_path, 'w', encoding='utf-8') as f:
            for item in category_data:
                # Определяем название на нужном языке
                if lang_code == 'ru':
                    name = item['name'].upper()  # Русские названия остаются как есть
                else:
                    # Используем переводы или оригинальное название
                    name = item['translations'].get(lang_code, item['name']).upper()
                
                # Записываем в формате: ID - НАЗВАНИЕ - ФАЙЛ_ИЗОБРАЖЕНИЯ
                f.write(f"{item['id']} - {name} - {item['filename']}\n")
        
        print(f"✅ Создан файл: {file_path}")

def update_categories_config(category_config):
    """Обновляет конфигурацию категорий"""
    print("⚙️ Обновляю конфигурацию категорий...")
    
    config_path = Path("data/config/categories.json")
    
    # Читаем существующую конфигурацию
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    # Создаем новую категорию
    new_category = {
        "id": category_config['id'],
        "names": category_config['names'],
        "description": category_config['descriptions'],
        "imageFolder": category_config['id'],
        "wordFiles": {
            "ru": f"{category_config['id']}_COMPLETE.txt",
            "en": f"{category_config['id']}_COMPLETE.txt", 
            "es": f"{category_config['id']}_COMPLETE.txt",
            "fr": f"{category_config['id']}_COMPLETE.txt"
        }
    }
    
    # Добавляем в список категорий
    config["categories"].append(new_category)
    
    # Сохраняем обновленную конфигурацию
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
    
    print("✅ Конфигурация категорий обновлена")

def fix_datamanager_for_new_category(category_id):
    """
    Автоматически добавляет обработку новой категории в DataManager.js
    Урок из создания динозавров: нужно добавить категорию в два места
    """
    print(f"🔧 Добавляю обработку категории '{category_id}' в DataManager.js...")
    
    datamanager_path = Path("modules/DataManager.js")
    if not datamanager_path.exists():
        print("⚠️ Файл DataManager.js не найден")
        return False
    
    # Читаем файл
    with open(datamanager_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Проверяем, нужно ли добавлять обработку
    if f"categoryId === '{category_id}'" in content:
        print(f"✅ Категория '{category_id}' уже обрабатывается в DataManager.js")
        return True
    
    # Ищем места для добавления
    # Место 1: в функции loadWordData (около строки 55)
    pattern1 = "// Для животных и динозавров - imageCode уже содержит расширение\n                        else if (categoryId === 'animals' || categoryId === 'dinosaurs') {"
    replacement1 = f"// Для животных, динозавров и {category_id} - imageCode уже содержит расширение\n                        else if (categoryId === 'animals' || categoryId === 'dinosaurs' || categoryId === '{category_id}') {{"
    
    # Место 2: в функции parseWordsFile (около строки 210)
    pattern2 = "// Для животных и динозавров - imageCode уже содержит расширение\n                    else if (categoryId === 'animals' || categoryId === 'dinosaurs') {"
    replacement2 = f"// Для животных, динозавров и {category_id} - imageCode уже содержит расширение\n                    else if (categoryId === 'animals' || categoryId === 'dinosaurs' || categoryId === '{category_id}') {{"
    
    # Применяем изменения
    updated_content = content.replace(pattern1, replacement1).replace(pattern2, replacement2)
    
    if updated_content != content:
        # Сохраняем изменения
        with open(datamanager_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        print(f"✅ DataManager.js обновлен для категории '{category_id}'")
        return True
    else:
        print(f"⚠️ Не удалось найти места для добавления категории '{category_id}' в DataManager.js")
        print("   Добавьте обработку вручную в строках ~55 и ~210")
        return False

def create_russian_translations_template(category_data, category_config):
    """
    Создает шаблон для русских переводов
    Урок из динозавров: важно сразу создавать правильные переводы
    """
    print("📝 Создаю шаблон русских переводов...")
    
    template_path = Path(f"tools/russian_translations_{category_config['id']}.py")
    
    with open(template_path, 'w', encoding='utf-8') as f:
        f.write(f"""#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Русские переводы для категории '{category_config['names']['ru']}'
# Заполните переводы и запустите скрипт для обновления файла слов

russian_translations = {{
""")
        
        for item in category_data:
            key = item['name'].lower().replace(' ', '_')
            f.write(f'    "{key}": "{item["name"].upper()}",  # TODO: добавить русский перевод\n')
        
        f.write(f"""}}

def update_russian_translations():
    \"\"\"Обновляет русские переводы в файле слов\"\"\"
    
    with open('data/words/ru/{category_config['id']}_COMPLETE.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    new_lines = []
    for line in lines:
        parts = line.strip().split(' - ')
        if len(parts) >= 3:
            number, english_name, image_file = parts
            key = image_file.replace('.jpg', '').split('-', 1)[1] if '-' in image_file else english_name.lower()
            russian_name = russian_translations.get(key, english_name)
            new_lines.append(f"{{number}} - {{russian_name}} - {{image_file}}\\n")
    
    with open('data/words/ru/{category_config['id']}_COMPLETE.txt', 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    print("✅ Русские переводы обновлены")

if __name__ == "__main__":
    update_russian_translations()
""")
    
    print(f"✅ Создан шаблон переводов: {template_path}")
    print("   Заполните переводы и запустите скрипт для обновления")

def validate_created_files(category_data, category_config):
    """Проверяет созданные файлы"""
    print("🔍 Проверяю созданные файлы...")
    
    errors = []
    
    # Проверяем изображения
    images_dir = Path(f"data/images/{category_config['id']}")
    if not images_dir.exists():
        errors.append("Папка изображений не создана")
    else:
        for item in category_data:
            image_path = images_dir / item['filename']
            if not image_path.exists():
                errors.append(f"Изображение не найдено: {item['filename']}")
    
    # Проверяем словарные файлы
    for lang in ['ru', 'en', 'es', 'fr']:
        word_file = Path(f"data/words/{lang}/{category_config['id']}_COMPLETE.txt")
        if not word_file.exists():
            errors.append(f"Словарный файл не создан: {lang}")
        else:
            # Проверяем содержимое
            with open(word_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                if len(lines) != len(category_data):
                    errors.append(f"Неверное количество записей в файле {lang}: {len(lines)} вместо {len(category_data)}")
    
    if errors:
        print("❌ НАЙДЕНЫ ОШИБКИ:")
        for error in errors:
            print(f"   • {error}")
        return False
    else:
        print("✅ Все файлы созданы корректно")
        return True

# ПРИМЕР КОНФИГУРАЦИИ ДЛЯ ДИНОЗАВРОВ (УСПЕШНО ИСПОЛЬЗОВАН)
def get_dinosaurs_config():
    """Возвращает конфигурацию для категории динозавров"""
    return {
        'id': 'dinosaurs',
        'source_images_path': 'E:/Games/dinosaurs',
        'names': {
            'ru': 'Динозавры',
            'en': 'Dinosaurs',
            'es': 'Dinosaurios',
            'fr': 'Dinosaures'
        },
        'descriptions': {
            'ru': 'Откройте для себя удивительный мир древних рептилий',
            'en': 'Discover the amazing world of ancient reptiles',
            'es': 'Descubre el increíble mundo de los reptiles antiguos',
            'fr': 'Découvrez le monde incroyable des reptiles anciens'
        },
        'image_extensions': ['*.jpg', '*.jpeg', '*.png'],
        'exclude_patterns': ['parse_*'],
        'name_cleaning_rules': {
            'remove_patterns': [],
            'remove_i_wrapper': True
        },
        'translations': create_dinosaur_translations()
    }

def create_dinosaur_translations():
    """Переводы названий динозавров (пример)"""
    # Здесь был большой словарь переводов...
    # Для экономии места показываю только несколько примеров
    return {
        'stegosaurus': {'en': 'Stegosaurus', 'es': 'Estegosaurus', 'fr': 'Stégosaure'},
        'tyrannosaurus': {'en': 'Tyrannosaurus', 'es': 'Tiranosaurus', 'fr': 'Tyrannosaure'},
        # ... остальные переводы
    }

def main():
    """
    ГЛАВНАЯ ФУНКЦИЯ - НАСТРОЙТЕ ЗДЕСЬ ПАРАМЕТРЫ НОВОЙ КАТЕГОРИИ
    
    Для создания новой категории:
    1. Измените параметры в category_config
    2. Добавьте переводы в функцию create_translations()
    3. Запустите скрипт
    """
    
    # ПРИМЕР: Конфигурация для динозавров (уже создана)
    category_config = get_dinosaurs_config()
    
    # ДЛЯ НОВОЙ КАТЕГОРИИ ИЗМЕНИТЕ ЭТИ ПАРАМЕТРЫ:
    # category_config = {
    #     'id': 'your_category_id',
    #     'source_images_path': 'путь/к/изображениям',
    #     'names': {
    #         'ru': 'Название на русском',
    #         'en': 'English Name',
    #         'es': 'Nombre en español',
    #         'fr': 'Nom en français'
    #     },
    #     'descriptions': {
    #         'ru': 'Описание на русском',
    #         'en': 'Description in English',
    #         'es': 'Descripción en español',
    #         'fr': 'Description en français'
    #     },
    #     'translations': your_translations_dict()
    # }
    
    success = create_category(category_config)
    
    if success:
        print("\n🎯 РЕКОМЕНДАЦИИ ПО ТЕСТИРОВАНИЮ:")
        print("1. Перезапустите сервер разработки")
        print("2. Проверьте загрузку категории на всех языках")
        print("3. Убедитесь что изображения отображаются корректно")
        print("4. Протестируйте игровой процесс с новой категорией")
    else:
        print("\n❌ Создание категории завершилось с ошибками")

if __name__ == "__main__":
    main() 