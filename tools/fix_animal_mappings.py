#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os

def fix_animal_mappings():
    """Fix animal image mappings by changing folder name from animal_world to animals"""
    
    print("🗺️ ИСПРАВЛЕНИЕ МАППИНГА ИЗОБРАЖЕНИЙ ЖИВОТНЫХ")
    print("=" * 50)
    
    languages = ['en', 'ru', 'es', 'fr']
    
    for lang in languages:
        old_file = f'data/image_mappings/animal_world_{lang}.json'
        new_file = f'data/image_mappings/animals_{lang}.json'
        
        if os.path.exists(old_file):
            print(f"📝 Обрабатываем {lang}...")
            
            # Read old mapping
            with open(old_file, 'r', encoding='utf-8') as f:
                mappings = json.load(f)
            
            # Fix paths: change animal_world/ to animals/
            fixed_mappings = {}
            for key, path in mappings.items():
                new_path = path.replace('animal_world/', 'animals/')
                fixed_mappings[key] = new_path
            
            # Write new mapping
            with open(new_file, 'w', encoding='utf-8') as f:
                json.dump(fixed_mappings, f, ensure_ascii=False, indent=2)
            
            print(f"✅ Создан правильный файл: {new_file}")
            
            # Remove old file
            os.remove(old_file)
            print(f"🗑️ Удален неправильный файл: {old_file}")
        else:
            print(f"⚠️ Файл {old_file} не найден")
    
    print("\n✅ МАППИНГ ИЗОБРАЖЕНИЙ ИСПРАВЛЕН!")

if __name__ == "__main__":
    fix_animal_mappings() 