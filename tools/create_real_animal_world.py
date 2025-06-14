#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Create Animal World category using REAL file names from directories
Following the 6-step plan with actual file names
"""

import os
import shutil
import re
from PIL import Image

def clean_russian_filename(filename):
    """Clean Russian filename from extra words"""
    name = os.path.splitext(filename)[0].lower()
    
    # Remove extra words
    extra_words = [
        '_фото', 'фото_', 'фото',
        '_животное', 'животное_', 'животное',
        '_рыба', 'рыба_', 'рыба',
        '_с_детенышем', '_с_детенышами',
        '_щенки', 'щенки_',
        '_детеныши', 'детеныши_',
        '_семейство', 'семейство_',
        '_обыкновенный', 'обыкновенный_',
        '_обыкновенная', 'обыкновенная_',
        '_дикая', 'дикая_', '_дикий', 'дикий_',
        '_на_охоте', '_охота', '_удачная_охота',
        '_стая', 'стая_', '_прайд', 'прайд_',
        '_нерест'
    ]
    
    for word in extra_words:
        name = name.replace(word, '')
    
    # Clean up underscores
    name = re.sub(r'_+', '_', name).strip('_')
    
    return name

def translate_russian_to_english(ru_name):
    """Translate cleaned Russian name to English"""
    # Basic translation dictionary for common animals
    translations = {
        # Sharks
        'бычья_акула': 'bull_shark',
        'тигровая_акула': 'tiger_shark', 
        'белая_акула': 'great_white_shark',
        'китовая_акула': 'whale_shark',
        'акула-молот': 'hammerhead_shark',
        'шестижаберная_акула': 'sixgill_shark',
        'полярная_акула': 'greenland_shark',
        'тупорылая_акула': 'bull_shark',
        'акула': 'shark',
        
        # Lions
        'азиатский_лев': 'asiatic_lion',
        'африканский_лев': 'african_lion',
        'берберийский_лев': 'barbary_lion',
        'лев': 'lion',
        
        # Wolves
        'серый_волк': 'gray_wolf',
        'красный_волк': 'red_wolf',
        'мелвильский_островной_волк': 'wolf',
        'тибетский_волк': 'wolf',
        'волк': 'wolf',
        
        # Fish
        'судак': 'zander',
        'волжский_судак': 'volga_zander',
        'бёрш': 'volga_zander',
        'берш': 'volga_zander',
        'щука': 'pike',
        'карась': 'crucian_carp',
        'золотой_карась': 'crucian_carp',
        'уклейка': 'bleak',
        'горбуша': 'pink_salmon',
        'быстрянка': 'spirlin',
        'язь': 'ide',
        'елец': 'dace',
        'сиг': 'whitefish',
        'меч_рыба': 'swordfish',
        'рыба_меч': 'swordfish',
        'солнечная_рыба': 'sunfish',
        'рыба_топорик': 'hatchetfish',
        'электрический_угорь': 'electric_eel',
        'илистый_прыгун': 'mudskipper',
        'рыба_прыгун_илистый': 'mudskipper',
        
        # Other animals
        'большеухая_лисица': 'bat_eared_fox',
        'рыжая_лисица': 'red_fox',
        'степная_лисица': 'fox',
        'лисица': 'fox',
        'енот_полоскун': 'raccoon',
        'енот-полоскун': 'raccoon',
        'енот_ракоед': 'crab_eating_raccoon',
        'енот-ракоед': 'crab_eating_raccoon',
        'енотовидная_собака': 'raccoon_dog',
        'гиеновидная_собака': 'african_wild_dog',
        'дикая_собака_динго': 'dingo',
        'динго': 'dingo',
        'европейская_норка': 'european_mink',
        'норка': 'mink',
        'выдра': 'otter',
        'обыкновенная_выдра': 'otter',
        'морской_конек': 'seahorse',
        'морские_коньки': 'seahorse',
        'оцелот': 'ocelot',
        'соболь': 'sable',
        'шакал': 'jackal',
        'эфиопский_шакал': 'ethiopian_wolf',
        'койот': 'coyote',
        'водяной_мангуст': 'marsh_mongoose',
        'мангуст-крабоед': 'crab_eating_mongoose',
        'мангуст': 'mongoose',
        'ирбис': 'snow_leopard',
        'леопард': 'leopard',
        'чилийская_кошка': 'jungle_cat',
        'кошка': 'cat',
        'собака': 'dog'
    }
    
    return translations.get(ru_name, None)

def process_real_files():
    """Process real files from directories"""
    
    print("🐾 Creating Animal World from REAL files")
    print("=" * 50)
    
    # Get real file lists
    animals_en_dir = 'animals_en'
    animals_ru_dir = 'animals_ru'
    final_dir = 'data/images/animal_world'
    
    os.makedirs(final_dir, exist_ok=True)
    os.makedirs('data/words/ru', exist_ok=True)
    os.makedirs('data/words/en', exist_ok=True)
    
    # Step 1: Get English files
    en_files = [f for f in os.listdir(animals_en_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    print(f"English files: {len(en_files)}")
    
    # Step 2: Get Russian files  
    ru_files = [f for f in os.listdir(animals_ru_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    print(f"Russian files: {len(ru_files)}")
    
    # Step 3: Process English files
    english_animals = {}
    for filename in en_files:
        name = os.path.splitext(filename)[0].lower().replace(' ', '_')
        english_animals[name] = {
            'source': 'english',
            'filename': filename,
            'display_name': os.path.splitext(filename)[0]
        }
    
    print(f"Processed {len(english_animals)} English animals")
    
    # Step 4: Process Russian files
    russian_animals = {}
    translated_count = 0
    
    for filename in ru_files:
        cleaned = clean_russian_filename(filename)
        translated = translate_russian_to_english(cleaned)
        
        if translated and translated not in russian_animals:
            russian_animals[translated] = {
                'source': 'russian',
                'filename': filename,
                'display_name': translated.replace('_', ' ').title(),
                'original_ru': cleaned
            }
            translated_count += 1
            print(f"  {filename} → {cleaned} → {translated}")
    
    print(f"Translated {translated_count} Russian animals")
    
    # Step 5: Merge without duplicates
    final_animals = {}
    
    # Add English first (priority)
    for name, data in english_animals.items():
        final_animals[name] = data
    
    # Add Russian (only if not duplicate)
    duplicates = 0
    for name, data in russian_animals.items():
        if name not in final_animals:
            final_animals[name] = data
        else:
            duplicates += 1
            print(f"  Duplicate: {name}")
    
    print(f"\nFinal result:")
    print(f"  English: {len(english_animals)}")
    print(f"  Russian: {len(russian_animals)}")
    print(f"  Duplicates: {duplicates}")
    print(f"  Total unique: {len(final_animals)}")
    
    # Step 6: Create numbered collection
    animal_list = []
    
    for index, (name, data) in enumerate(sorted(final_animals.items()), 1):
        image_code = f"ANIMAL-{index:03d}"
        
        # Copy image
        if data['source'] == 'english':
            src_path = os.path.join(animals_en_dir, data['filename'])
        else:
            src_path = os.path.join(animals_ru_dir, data['filename'])
        
        dst_path = os.path.join(final_dir, f"{image_code}.png")
        
        try:
            with Image.open(src_path) as img:
                img = img.convert('RGB')
                img = img.resize((300, 300), Image.Resampling.LANCZOS)
                img.save(dst_path, 'PNG', quality=95, optimize=True)
            
            animal_list.append({
                'number': index,
                'name_en': data['display_name'],
                'code': image_code,
                'source': data['source']
            })
            
        except Exception as e:
            print(f"Error processing {name}: {e}")
    
    # Create word files
    en_file = 'data/words/en/animal_world.txt'
    with open(en_file, 'w', encoding='utf-8') as f:
        for animal in animal_list:
            f.write(f"{animal['number']} - {animal['name_en'].upper()} - {animal['code']}\n")
    
    ru_file = 'data/words/ru/animal_world.txt'
    with open(ru_file, 'w', encoding='utf-8') as f:
        for animal in animal_list:
            # For Russian, we'll need proper translations later
            f.write(f"{animal['number']} - {animal['name_en'].upper()} - {animal['code']}\n")
    
    print(f"\n✅ Created {len(animal_list)} animals")
    print(f"English file: {en_file}")
    print(f"Russian file: {ru_file}")

if __name__ == "__main__":
    process_real_files() 