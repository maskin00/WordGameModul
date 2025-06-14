#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Create "Animal World" category following the exact 6-step plan:
1. Clean Russian filenames from extra words ("фото", "животное", etc.)
2. Translate cleaned Russian names to English
3. Compare/merge English and translated Russian images WITHOUT duplicates
4. Number final unified collection with English names
5. Create "Животный мир" (Animal World) category
6. Analyze sufficiency for game requirements
"""

import os
import shutil
import re
from PIL import Image

def clean_russian_filename(filename):
    """Step 1: Clean Russian filename from extra words"""
    name = os.path.splitext(filename)[0]
    
    # Remove common extra words
    extra_words = [
        '_фото', 'фото_', 'фото',
        '_животное', 'животное_', 'животное',
        '_рыба', 'рыба_', 'рыба',
        '_кошка', 'кошка_', 
        '_собака', 'собака_',
        '_с_детенышем', '_с_детенышами',
        '_щенки', 'щенки_',
        '_детеныши', 'детеныши_',
        '_семейство', 'семейство_',
        '_обыкновенный', 'обыкновенный_',
        '_обыкновенная', 'обыкновенная_',
        '_дикая', 'дикая_',
        '_дикий', 'дикий_',
        '_хищные', 'хищные_',
        '_на_охоте', '_охота',
        '_удачная_охота',
        '_стая', 'стая_',
        '_прайд', 'прайд_',
        '_нерест'
    ]
    
    cleaned = name.lower()
    for word in extra_words:
        cleaned = cleaned.replace(word, '')
    
    # Remove multiple underscores and clean up
    cleaned = re.sub(r'_+', '_', cleaned)
    cleaned = cleaned.strip('_')
    
    # Specific animal handling
    if 'акула' in cleaned:
        if 'бычья' in cleaned or 'тупорылая' in cleaned:
            cleaned = 'бычья_акула'
        elif 'тигровая' in cleaned:
            cleaned = 'тигровая_акула'
        elif 'белая' in cleaned or 'кархародон' in cleaned:
            cleaned = 'белая_акула'
        elif 'китовая' in cleaned:
            cleaned = 'китовая_акула'
        elif 'молот' in cleaned:
            cleaned = 'акула_молот'
        elif 'шестижаберная' in cleaned:
            cleaned = 'шестижаберная_акула'
        elif 'полярная' in cleaned:
            cleaned = 'полярная_акула'
        else:
            cleaned = 'акула'
    elif 'лев' in cleaned:
        if 'азиатский' in cleaned:
            cleaned = 'азиатский_лев'
        elif 'африканский' in cleaned:
            cleaned = 'африканский_лев'
        elif 'берберийский' in cleaned:
            cleaned = 'берберийский_лев'
        else:
            cleaned = 'лев'
    elif 'волк' in cleaned:
        if 'серый' in cleaned:
            cleaned = 'серый_волк'
        else:
            cleaned = 'волк'
    elif 'судак' in cleaned:
        if 'волжский' in cleaned or 'бёрш' in cleaned or 'берш' in cleaned:
            cleaned = 'берш'
        else:
            cleaned = 'судак'
    elif 'енот' in cleaned:
        if 'ракоед' in cleaned:
            cleaned = 'енот_ракоед'
        elif 'полоскун' in cleaned:
            cleaned = 'енот_полоскун'
        else:
            cleaned = 'енот'
    elif 'норка' in cleaned:
        if 'европейская' in cleaned:
            cleaned = 'европейская_норка'
        else:
            cleaned = 'норка'
    elif 'морской_конек' in cleaned or 'морские_коньки' in cleaned:
        cleaned = 'морской_конек'
    elif 'угорь' in cleaned:
        if 'электрический' in cleaned:
            cleaned = 'электрический_угорь'
        else:
            cleaned = 'угорь'
    elif 'прыгун' in cleaned and 'илистый' in cleaned:
        cleaned = 'илистый_прыгун'
    elif 'карась' in cleaned:
        if 'золотой' in cleaned:
            cleaned = 'золотой_карась'
        else:
            cleaned = 'карась'
    elif 'лисица' in cleaned:
        if 'большеухая' in cleaned:
            cleaned = 'большеухая_лисица'
        else:
            cleaned = 'лисица'
    elif 'кошка' in cleaned:
        if 'чилийская' in cleaned:
            cleaned = 'чилийская_кошка'
        else:
            cleaned = 'кошка'
    elif 'собака' in cleaned:
        if 'гиеновидная' in cleaned:
            cleaned = 'гиеновидная_собака'
        elif 'енотовидная' in cleaned:
            cleaned = 'енотовидная_собака'
        else:
            cleaned = 'собака'
    
    # Handle fish names
    fish_names = {
        'уклейка': 'уклейка',
        'горбуша': 'горбуша',
        'быстрянка': 'быстрянка',
        'язь': 'язь',
        'елец': 'елец',
        'сиг': 'сиг',
        'меч': 'рыба_меч',
        'топорик': 'рыба_топорик',
        'солнечная': 'солнечная_рыба'
    }
    
    for fish, name in fish_names.items():
        if fish in cleaned:
            cleaned = name
            break
    
    return cleaned

def get_russian_to_english_translations():
    """Step 2: Russian to English translations"""
    return {
        'бычья_акула': 'bull_shark',
        'тигровая_акула': 'tiger_shark',
        'белая_акула': 'great_white_shark',
        'китовая_акула': 'whale_shark',
        'акула_молот': 'hammerhead_shark',
        'шестижаберная_акула': 'sixgill_shark',
        'полярная_акула': 'greenland_shark',
        'акула': 'shark',
        'азиатский_лев': 'asiatic_lion',
        'африканский_лев': 'african_lion',
        'берберийский_лев': 'barbary_lion',
        'лев': 'lion',
        'серый_волк': 'gray_wolf',
        'волк': 'wolf',
        'берш': 'volga_zander',
        'судак': 'zander',
        'енот_ракоед': 'crab_eating_raccoon',
        'енот_полоскун': 'raccoon',
        'енот': 'raccoon',
        'европейская_норка': 'european_mink',
        'норка': 'mink',
        'морской_конек': 'seahorse',
        'электрический_угорь': 'electric_eel',
        'угорь': 'eel',
        'илистый_прыгун': 'mudskipper',
        'золотой_карась': 'crucian_carp',
        'карась': 'crucian_carp',
        'большеухая_лисица': 'bat_eared_fox',
        'лисица': 'fox',
        'чилийская_кошка': 'jungle_cat',
        'кошка': 'cat',
        'гиеновидная_собака': 'african_wild_dog',
        'енотовидная_собака': 'raccoon_dog',
        'собака': 'dog',
        'уклейка': 'bleak',
        'горбуша': 'pink_salmon',
        'быстрянка': 'spirlin',
        'язь': 'ide',
        'елец': 'dace',
        'сиг': 'whitefish',
        'рыба_меч': 'swordfish',
        'рыба_топорик': 'hatchetfish',
        'солнечная_рыба': 'sunfish',
        'щука': 'pike',
        'выдра': 'otter',
        'динго': 'dingo',
        'оцелот': 'ocelot',
        'соболь': 'sable',
        'шакал': 'jackal',
        'эфиопский_шакал': 'ethiopian_wolf',
        'койот': 'coyote',
        'водяной_мангуст': 'marsh_mongoose',
        'мангуст_крабоед': 'crab_eating_mongoose',
        'мангуст': 'mongoose',
        'ирбис': 'snow_leopard',
        'леопард': 'leopard'
    }

def process_according_to_plan():
    """Execute the 6-step plan exactly"""
    
    print("🐾 Creating Animal World Category - Following 6-Step Plan")
    print("=" * 60)
    
    # Paths
    animals_en_dir = 'animals_en'
    animals_ru_dir = 'animals_ru'
    final_animals_dir = 'data/images/animal_world'
    
    # Create directories
    os.makedirs(final_animals_dir, exist_ok=True)
    os.makedirs('data/words/ru', exist_ok=True)
    os.makedirs('data/words/en', exist_ok=True)
    
    # STEP 1 & 2: Process Russian images - Clean and Translate
    print("\n📝 STEP 1-2: Processing Russian images (Clean + Translate)")
    print("-" * 50)
    
    if not os.path.exists(animals_ru_dir):
        print(f"❌ Russian animals directory not found: {animals_ru_dir}")
        return
    
    ru_files = [f for f in os.listdir(animals_ru_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    print(f"Found {len(ru_files)} Russian animal images")
    
    translations = get_russian_to_english_translations()
    translated_animals = {}
    
    for filename in ru_files:
        # Step 1: Clean Russian filename
        cleaned_ru = clean_russian_filename(filename)
        
        # Step 2: Translate to English
        if cleaned_ru in translations:
            en_name = translations[cleaned_ru]
            
            # Store for merging (avoid duplicates within Russian set)
            if en_name not in translated_animals:
                translated_animals[en_name] = {
                    'source': 'russian_translated',
                    'original_file': filename,
                    'cleaned_ru': cleaned_ru
                }
                print(f"  ✓ {filename} → {cleaned_ru} → {en_name}")
            else:
                print(f"  ⚠️  Duplicate in Russian set: {en_name} (skipping {filename})")
        else:
            print(f"  ❌ No translation for: {cleaned_ru} (from {filename})")
    
    print(f"Successfully processed {len(translated_animals)} unique Russian animals")
    
    # STEP 3: Process English images and Merge without duplicates
    print(f"\n📝 STEP 3: Processing English images and Merging")
    print("-" * 50)
    
    if not os.path.exists(animals_en_dir):
        print(f"❌ English animals directory not found: {animals_en_dir}")
        return
    
    en_files = [f for f in os.listdir(animals_en_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    print(f"Found {len(en_files)} English animal images")
    
    final_animals = {}
    
    # Add English images first (they have priority)
    for filename in en_files:
        name = os.path.splitext(filename)[0].lower().replace(' ', '_')
        final_animals[name] = {
            'source': 'english',
            'original_file': filename
        }
        print(f"  ✓ English: {filename} → {name}")
    
    # Add translated Russian images (only if not duplicate)
    duplicates_count = 0
    for en_name, data in translated_animals.items():
        if en_name not in final_animals:
            final_animals[en_name] = data
            print(f"  ✓ Added Russian: {data['cleaned_ru']} → {en_name}")
        else:
            duplicates_count += 1
            print(f"  ⚠️  Duplicate removed: {en_name} (Russian version skipped)")
    
    print(f"\nMerging results:")
    print(f"  English animals: {len(en_files)}")
    print(f"  Russian animals (translated): {len(translated_animals)}")
    print(f"  Duplicates removed: {duplicates_count}")
    print(f"  Final unique animals: {len(final_animals)}")
    
    # STEP 4: Number final unified collection
    print(f"\n📝 STEP 4: Numbering final unified collection")
    print("-" * 50)
    
    animal_list = []
    
    for index, (name, data) in enumerate(sorted(final_animals.items()), 1):
        # Create numbered filename
        image_code = f"ANIMAL-{index:03d}"
        image_filename = f"{image_code}.png"
        image_path = os.path.join(final_animals_dir, image_filename)
        
        # Load and save image
        try:
            if data['source'] == 'english':
                src_path = os.path.join(animals_en_dir, data['original_file'])
            else:
                src_path = os.path.join(animals_ru_dir, data['original_file'])
            
            with Image.open(src_path) as img:
                img = img.convert('RGB')
                img = img.resize((300, 300), Image.Resampling.LANCZOS)
                img.save(image_path, 'PNG', quality=95, optimize=True)
            
            # Add to list
            animal_list.append({
                'number': index,
                'name_en': name.replace('_', ' ').title(),
                'name_ru': data.get('cleaned_ru', name).replace('_', ' ').title(),
                'code': image_code,
                'source': data['source']
            })
            
            print(f"  {index:3d}. {name.replace('_', ' ').title()} → {image_code} ({data['source']})")
            
        except Exception as e:
            print(f"    ❌ Error processing {name}: {e}")
    
    # STEP 5: Create "Животный мир" category
    print(f"\n📝 STEP 5: Creating 'Животный мир' (Animal World) category")
    print("-" * 50)
    
    # Create English word list
    en_file_path = 'data/words/en/animal_world.txt'
    with open(en_file_path, 'w', encoding='utf-8') as f:
        for animal in animal_list:
            f.write(f"{animal['number']} - {animal['name_en'].upper()} - {animal['code']}\n")
    
    # Create Russian word list (will need proper Russian translations later)
    ru_file_path = 'data/words/ru/animal_world.txt'
    with open(ru_file_path, 'w', encoding='utf-8') as f:
        for animal in animal_list:
            # For now, use cleaned Russian names where available
            ru_name = animal['name_ru'] if animal['source'] == 'russian_translated' else animal['name_en']
            f.write(f"{animal['number']} - {ru_name.upper()} - {animal['code']}\n")
    
    print(f"✅ Created category files:")
    print(f"  English: {en_file_path}")
    print(f"  Russian: {ru_file_path}")
    
    # STEP 6: Analyze sufficiency for game requirements
    print(f"\n📝 STEP 6: Analysis for game requirements")
    print("-" * 50)
    
    print(f"📊 FINAL RESULTS:")
    print(f"  Total unique animals: {len(animal_list)}")
    print(f"  From English source: {len([a for a in animal_list if a['source'] == 'english'])}")
    print(f"  From Russian source: {len([a for a in animal_list if a['source'] == 'russian_translated'])}")
    print(f"  Images saved to: {final_animals_dir}")
    
    if len(animal_list) >= 200:
        print(f"✅ EXCELLENT! {len(animal_list)} animals is perfect for a comprehensive category")
    elif len(animal_list) >= 100:
        print(f"✅ VERY GOOD! {len(animal_list)} animals is more than enough for a great category")
    elif len(animal_list) >= 50:
        print(f"✅ GOOD! {len(animal_list)} animals is sufficient for a solid category")
    else:
        print(f"⚠️  {len(animal_list)} animals might be minimal")
    
    print(f"\n🎉 6-Step Plan Completed Successfully!")
    print(f"Category 'Животный мир' / 'Animal World' is ready!")

if __name__ == "__main__":
    process_according_to_plan() 