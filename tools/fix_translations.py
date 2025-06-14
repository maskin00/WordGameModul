#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

def transliterate_russian(text):
    """Транслитерация с русского на латиницу"""
    translit_map = {
        'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D', 'Е': 'E', 'Ё': 'YO', 'Ж': 'ZH', 'З': 'Z',
        'И': 'I', 'Й': 'Y', 'К': 'K', 'Л': 'L', 'М': 'M', 'Н': 'N', 'О': 'O', 'П': 'P', 'Р': 'R',
        'С': 'S', 'Т': 'T', 'У': 'U', 'Ф': 'F', 'Х': 'KH', 'Ц': 'TS', 'Ч': 'CH', 'Ш': 'SH', 'Щ': 'SHCH',
        'Ъ': '', 'Ы': 'Y', 'Ь': '', 'Э': 'E', 'Ю': 'YU', 'Я': 'YA',
        ' ': ' ', '-': '-'
    }
    
    result = ""
    for char in text:
        if char in translit_map:
            result += translit_map[char]
        else:
            result += char
    
    return result

def process_file(file_path, language):
    """Обработка файла с футболистами"""
    print(f"Обрабатываем файл: {file_path}")
    
    if not os.path.exists(file_path):
        print(f"⚠ Файл не найден: {file_path}")
        return
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        processed_lines = []
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                processed_lines.append(line)
                continue
            
            # Парсим строку: номер - СЛОВО - код_изображения
            parts = line.split(' - ')
            if len(parts) >= 3:
                number = parts[0]
                russian_name = parts[1]
                image_code = parts[2]  # Код изображения оставляем без изменений!
                
                # Транслитерируем только русское название
                transliterated_name = transliterate_russian(russian_name)
                
                processed_lines.append(f"{number} - {transliterated_name} - {image_code}")
            else:
                processed_lines.append(line)
        
        # Записываем обработанный файл
        with open(file_path, 'w', encoding='utf-8') as f:
            for line in processed_lines:
                f.write(line + '\n')
        
        print(f"✓ Файл {file_path} успешно обработан")
        
    except Exception as e:
        print(f"✗ Ошибка обработки файла {file_path}: {e}")

def main():
    """Основная функция"""
    print("Начинаем исправление переводов футболистов...\n")
    
    # Получаем путь к корневой папке проекта
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    
    languages = ['en', 'fr', 'es']
    file_name = 'footballers_FULL.txt'
    
    for lang in languages:
        file_path = os.path.join(project_root, 'data', 'words', lang, file_name)
        process_file(file_path, lang)
    
    print("\n✓ Исправление переводов завершено!")

if __name__ == "__main__":
    main() 