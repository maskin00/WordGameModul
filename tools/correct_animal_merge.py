#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
from PIL import Image

def clean_russian_name(filename):
    """Clean Russian filename from extra words"""
    name = os.path.splitext(filename)[0].lower()
    
    # Remove extra words
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
        'большеухая_лисица': 'bat eared fox',
        'белая_акула': 'great white shark',
        'берберийский_лев': 'barbary lion',
        'бычья_акула': 'bull shark',
        'тигровая_акула': 'tiger shark',
        'китовая_акула': 'whale shark',
        'акула-молот': 'hammerhead shark',
        'шестижаберная_акула': 'sixgill shark',
        'полярная_акула': 'greenland shark',
        'акула-бык': 'bull shark',
        'серый_волк': 'gray wolf',
        'красный_волк': 'red wolf',
        'азиатский_лев': 'asiatic lion',
        'африканский_лев': 'african lion',
        'енот_полоскун': 'raccoon',
        'енот-полоскун': 'raccoon',
        'енот_ракоед': 'crab eating raccoon',
        'енот-ракоед': 'crab eating raccoon',
        'европейская_норка': 'european mink',
        'водяной_мангуст': 'marsh mongoose',
        'мангуст-крабоед': 'crab eating mongoose',
        'гиеновидная_собака': 'african wild dog',
        'енотовидная_собака': 'raccoon dog',
        'дикая_собака_динго': 'dingo',
        'морской_конек': 'sea horse',
        'морские_коньки': 'sea horse',
        'электрический_угорь': 'electric eel',
        'илистый_прыгун': 'mudskipper',
        'чилийская_кошка': 'jungle cat',
        'эфиопский_шакал': 'ethiopian wolf',
        'ирбис': 'snow leopard',
        'рыжая_лисица': 'red fox',
        'степная_лисица': 'fox',
        'золотой_карась': 'crucian carp',
        'рыба_меч': 'swordfish',
        'меч_рыба': 'swordfish',
        'солнечная_рыба': 'sunfish',
        'рыба_топорик': 'hatchetfish',
        'быстрянка': 'spirlin',
        'горбуша': 'pink salmon',
        'уклейка': 'bleak',
        'щука': 'pike',
        'судак': 'zander',
        'берш': 'volga zander',
        'волжский_судак': 'volga zander',
        'бёрш': 'volga zander',
        'елец': 'dace',
        'язь': 'ide',
        'сиг': 'whitefish',
        'карась': 'crucian carp',
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

def process_animal_world():
    """Process according to the 6-step plan"""
    
    print("🐾 Creating Animal World - CORRECT VERSION")
    print("=" * 50)
    
    # Get file lists
    en_files = [f for f in os.listdir('animals_en') if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    ru_files = [f for f in os.listdir('animals_ru') if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    
    print(f"English files: {len(en_files)}")
    print(f"Russian files: {len(ru_files)}")
    
    # Step 1-2: Process Russian files
    print(f"\n📝 Processing Russian files...")
    
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
                print(f"  {filename} → {cleaned} → {translated}")
    
    print(f"Translated {len(russian_animals)} Russian animals")
    
    # Step 3: Process English files
    print(f"\n📝 Processing English files...")
    
    english_animals = {}
    for filename in en_files:
        name = os.path.splitext(filename)[0]
        normalized = normalize_name(name)
        english_animals[normalized] = {
            'filename': filename,
            'display_name': name,
            'normalized': normalized
        }
    
    print(f"Processed {len(english_animals)} English animals")
    
    # Step 4: Find duplicates and merge
    print(f"\n📝 Finding duplicates and merging...")
    
    duplicates = []
    final_animals = {}
    
    # Add English first (priority)
    for norm_name, data in english_animals.items():
        final_animals[norm_name] = {
            'source': 'english',
            'filename': data['filename'],
            'display_name': data['display_name']
        }
    
    # Add Russian (only if not duplicate)
    for norm_name, data in russian_animals.items():
        if norm_name in english_animals:
            duplicates.append({
                'english': english_animals[norm_name]['display_name'],
                'russian': data['translated_en'],
                'ru_file': data['filename']
            })
        else:
            final_animals[norm_name] = {
                'source': 'russian',
                'filename': data['filename'],
                'display_name': data['translated_en']
            }
    
    print(f"Found {len(duplicates)} duplicates:")
    for dup in duplicates:
        print(f"  {dup['english']} = {dup['russian']} (skipping {dup['ru_file']})")
    
    print(f"\nFinal result:")
    print(f"  English: {len(english_animals)}")
    print(f"  Russian: {len(russian_animals)}")
    print(f"  Duplicates: {len(duplicates)}")
    print(f"  Total unique: {len(final_animals)}")
    
    # Step 5-6: Create numbered collection
    print(f"\n📝 Creating numbered collection...")
    
    os.makedirs('data/images/animal_world', exist_ok=True)
    os.makedirs('data/words/en', exist_ok=True)
    os.makedirs('data/words/ru', exist_ok=True)
    
    animal_list = []
    
    for index, (norm_name, data) in enumerate(sorted(final_animals.items()), 1):
        image_code = f"ANIMAL-{index:03d}"
        
        # Copy image
        if data['source'] == 'english':
            src_path = os.path.join('animals_en', data['filename'])
        else:
            src_path = os.path.join('animals_ru', data['filename'])
        
        dst_path = os.path.join('data/images/animal_world', f"{image_code}.png")
        
        try:
            with Image.open(src_path) as img:
                img = img.convert('RGB')
                img = img.resize((300, 300), Image.Resampling.LANCZOS)
                img.save(dst_path, 'PNG', quality=95, optimize=True)
            
            animal_list.append({
                'number': index,
                'name': data['display_name'],
                'code': image_code,
                'source': data['source']
            })
            
        except Exception as e:
            print(f"Error processing {data['filename']}: {e}")
    
    # Create word files
    en_file = 'data/words/en/animal_world.txt'
    with open(en_file, 'w', encoding='utf-8') as f:
        for animal in animal_list:
            f.write(f"{animal['number']} - {animal['name'].upper()} - {animal['code']}\n")
    
    ru_file = 'data/words/ru/animal_world.txt'
    with open(ru_file, 'w', encoding='utf-8') as f:
        for animal in animal_list:
            f.write(f"{animal['number']} - {animal['name'].upper()} - {animal['code']}\n")
    
    print(f"\n✅ SUCCESS!")
    print(f"Created {len(animal_list)} unique animals")
    print(f"English file: {en_file}")
    print(f"Russian file: {ru_file}")

if __name__ == "__main__":
    process_animal_world() 