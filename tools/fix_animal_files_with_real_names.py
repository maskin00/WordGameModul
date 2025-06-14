#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import shutil
import re
from PIL import Image

def clean_russian_name(filename):
    """Clean Russian filename from extra words"""
    name = os.path.splitext(filename)[0].lower()
    
    extra_words = [
        '_фото', 'фото_', 'фото',
        '_животное', 'животное_', 'животное',
        '_рыба', 'рыба_', 'рыба',
        '_с_детенышем', '_с_детенышами',
        '_щенки', 'щенки_', '_детеныши', 'детеныши_',
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
    
    name = re.sub(r'_+', '_', name).strip('_')
    return name

def translate_to_english(ru_name):
    """Translate Russian animal name to English"""
    translations = {
        'большеухая_лисица': 'bat_eared_fox',
        'белая_акула': 'great_white_shark',
        'белая_акула_кархародон': 'great_white_shark',
        'берберийский_лев': 'barbary_lion',
        'бычья_акула': 'bull_shark',
        'тигровая_акула': 'tiger_shark',
        'китовая_акула': 'whale_shark',
        'акула-молот': 'hammerhead_shark',
        'шестижаберная_акула': 'sixgill_shark',
        'полярная_акула': 'greenland_shark',
        'акула-бык': 'bull_shark',
        'серый_волк': 'gray_wolf',
        'красный_волк': 'red_wolf',
        'азиатский_лев': 'asiatic_lion',
        'африканский_лев': 'african_lion',
        'енот_полоскун': 'raccoon',
        'енот-полоскун': 'raccoon',
        'енот_ракоед': 'crab_eating_raccoon',
        'енот-ракоед': 'crab_eating_raccoon',
        'европейская_норка': 'european_mink',
        'водяной_мангуст': 'marsh_mongoose',
        'мангуст-крабоед': 'crab_eating_mongoose',
        'гиеновидная_собака': 'african_wild_dog',
        'енотовидная_собака': 'raccoon_dog',
        'дикая_собака_динго': 'dingo',
        'морской_конек': 'sea_horse',
        'морские_коньки': 'sea_horse',
        'электрический_угорь': 'electric_eel',
        'илистый_прыгун': 'mudskipper',
        'чилийская_кошка': 'jungle_cat',
        'эфиопский_шакал': 'ethiopian_wolf',
        'ирбис': 'snow_leopard',
        'рыжая_лисица': 'red_fox',
        'степная_лисица': 'fox',
        'золотой_карась': 'crucian_carp',
        'рыба_меч': 'swordfish',
        'меч_рыба': 'swordfish',
        'солнечная_рыба': 'sunfish',
        'рыба_топорик': 'hatchetfish',
        'быстрянка': 'spirlin',
        'горбуша': 'pink_salmon',
        'уклейка': 'bleak',
        'щука': 'pike',
        'судак': 'zander',
        'берш': 'volga_zander',
        'волжский_судак': 'volga_zander',
        'бёрш': 'volga_zander',
        'елец': 'dace',
        'язь': 'ide',
        'сиг': 'whitefish',
        'карась': 'crucian_carp',
        'выдра': 'otter',
        'обыкновенная_выдра': 'otter',
        'динго': 'dingo',
        'оцелот': 'ocelot',
        'соболь': 'sable',
        'шакал': 'jackal',
        'койот': 'coyote',
        'мангуст': 'mongoose',
        'леопард': 'leopard',
        'лев': 'lion',
        'волк': 'wolf',
        'лисица': 'fox',
        'кошка': 'cat',
        'собака': 'dog',
        'акула': 'shark'
    }
    
    return translations.get(ru_name)

def normalize_name(name):
    """Normalize name for comparison"""
    return name.lower().replace(' ', '_').replace('-', '_')

def create_animal_world_with_real_names():
    """Create animal world with real file names and numbers"""
    
    print("🐾 Creating Animal World with REAL file names")
    print("=" * 50)
    
    # Clear existing directory
    animal_dir = 'data/images/animal_world'
    if os.path.exists(animal_dir):
        shutil.rmtree(animal_dir)
        print(f"Cleared existing directory: {animal_dir}")
    
    os.makedirs(animal_dir, exist_ok=True)
    os.makedirs('data/words/ru', exist_ok=True)
    os.makedirs('data/words/en', exist_ok=True)
    
    # Get file lists
    en_files = [f for f in os.listdir('animals_en') if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    ru_files = [f for f in os.listdir('animals_ru') if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    
    print(f"English files: {len(en_files)}")
    print(f"Russian files: {len(ru_files)}")
    
    # Process Russian files
    russian_animals = {}
    for filename in ru_files:
        cleaned = clean_russian_name(filename)
        translated = translate_to_english(cleaned)
        
        if translated:
            normalized = normalize_name(translated)
            if normalized not in russian_animals:
                russian_animals[normalized] = {
                    'filename': filename,
                    'cleaned_ru': cleaned,
                    'translated_en': translated,
                    'normalized': normalized
                }
    
    # Process English files
    english_animals = {}
    for filename in en_files:
        name = os.path.splitext(filename)[0]
        normalized = normalize_name(name)
        english_animals[normalized] = {
            'filename': filename,
            'display_name': name,
            'normalized': normalized
        }
    
    # Merge without duplicates
    final_animals = {}
    duplicates = []
    
    # Add English first (priority)
    for norm_name, data in english_animals.items():
        final_animals[norm_name] = {
            'source': 'english',
            'filename': data['filename'],
            'display_name': data['display_name'],
            'file_name': norm_name  # For file naming
        }
    
    # Add Russian (only if not duplicate)
    for norm_name, data in russian_animals.items():
        if norm_name in english_animals:
            duplicates.append(norm_name)
        else:
            final_animals[norm_name] = {
                'source': 'russian',
                'filename': data['filename'],
                'display_name': data['translated_en'],
                'file_name': norm_name  # For file naming
            }
    
    print(f"Final unique animals: {len(final_animals)}")
    print(f"Duplicates removed: {len(duplicates)}")
    
    # Create numbered files with real names
    animal_list = []
    
    for index, (norm_name, data) in enumerate(sorted(final_animals.items()), 1):
        # Create file name: 001-aardvark.png
        file_name = f"{index:03d}-{data['file_name']}.png"
        file_path = os.path.join(animal_dir, file_name)
        
        # Copy and resize image
        if data['source'] == 'english':
            src_path = os.path.join('animals_en', data['filename'])
        else:
            src_path = os.path.join('animals_ru', data['filename'])
        
        try:
            with Image.open(src_path) as img:
                img = img.convert('RGB')
                img = img.resize((300, 300), Image.Resampling.LANCZOS)
                img.save(file_path, 'PNG', quality=95, optimize=True)
            
            animal_list.append({
                'number': index,
                'name': data['display_name'],
                'file_name': file_name,
                'source': data['source']
            })
            
            print(f"  {index:3d}. {data['display_name']} → {file_name} ({data['source']})")
            
        except Exception as e:
            print(f"Error processing {data['filename']}: {e}")
    
    # Create word files with real file names
    en_file = 'data/words/en/animal_world.txt'
    with open(en_file, 'w', encoding='utf-8') as f:
        for animal in animal_list:
            f.write(f"{animal['number']} - {animal['name'].upper()} - {animal['file_name']}\n")
    
    ru_file = 'data/words/ru/animal_world.txt'
    with open(ru_file, 'w', encoding='utf-8') as f:
        for animal in animal_list:
            # For Russian, we'll need proper translations later
            f.write(f"{animal['number']} - {animal['name'].upper()} - {animal['file_name']}\n")
    
    print(f"\n✅ SUCCESS!")
    print(f"Created {len(animal_list)} animals with real file names")
    print(f"Files: 001-aardvark.png to {len(animal_list):03d}-{animal_list[-1]['file_name'].split('-', 1)[1]}")
    print(f"English file: {en_file}")
    print(f"Russian file: {ru_file}")
    
    # Show examples
    print(f"\nExamples of created files:")
    for animal in animal_list[:5]:
        print(f"  {animal['file_name']} - {animal['name']}")

if __name__ == "__main__":
    create_animal_world_with_real_names() 