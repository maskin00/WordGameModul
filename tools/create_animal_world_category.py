#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Create "Animal World" category from Russian and English animal images
1. Clean Russian filenames from extra words
2. Translate Russian names to English
3. Merge with existing English images without duplicates
4. Number the final collection
5. Create category files
"""

import os
import shutil
import re
from PIL import Image
import json

def clean_russian_filename(filename):
    """Clean Russian filename from extra words like 'фото', 'животное', etc."""
    # Remove file extension
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
    
    # Clean the name
    cleaned = name.lower()
    for word in extra_words:
        cleaned = cleaned.replace(word, '')
    
    # Remove multiple underscores and clean up
    cleaned = re.sub(r'_+', '_', cleaned)
    cleaned = cleaned.strip('_')
    
    # Handle specific cases
    if 'акула' in cleaned:
        # Keep only the type of shark
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
    
    elif 'выдра' in cleaned:
        cleaned = 'выдра'
    
    elif 'динго' in cleaned:
        cleaned = 'динго'
    
    elif 'оцелот' in cleaned:
        cleaned = 'оцелот'
    
    elif 'соболь' in cleaned:
        cleaned = 'соболь'
    
    elif 'шакал' in cleaned:
        if 'эфиопский' in cleaned:
            cleaned = 'эфиопский_шакал'
        else:
            cleaned = 'шакал'
    
    elif 'койот' in cleaned:
        cleaned = 'койот'
    
    elif 'мангуст' in cleaned:
        if 'водяной' in cleaned:
            cleaned = 'водяной_мангуст'
        elif 'крабоед' in cleaned:
            cleaned = 'мангуст_крабоед'
        else:
            cleaned = 'мангуст'
    
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
    
    elif 'щука' in cleaned:
        cleaned = 'щука'
    
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
    """Get translation dictionary from Russian to English animal names"""
    return {
        # Акулы
        'бычья_акула': 'bull_shark',
        'тигровая_акула': 'tiger_shark',
        'белая_акула': 'great_white_shark',
        'китовая_акула': 'whale_shark',
        'акула_молот': 'hammerhead_shark',
        'шестижаберная_акула': 'sixgill_shark',
        'полярная_акула': 'greenland_shark',
        'акула': 'shark',
        
        # Хищники
        'лев': 'lion',
        'азиатский_лев': 'asiatic_lion',
        'африканский_лев': 'african_lion',
        'берберийский_лев': 'barbary_lion',
        'леопард': 'leopard',
        'ирбис': 'snow_leopard',
        
        # Волки и собачьи
        'волк': 'wolf',
        'серый_волк': 'gray_wolf',
        'шакал': 'jackal',
        'эфиопский_шакал': 'ethiopian_wolf',
        'койот': 'coyote',
        'динго': 'dingo',
        'гиеновидная_собака': 'african_wild_dog',
        'енотовидная_собака': 'raccoon_dog',
        'собака': 'dog',
        
        # Кошачьи
        'оцелот': 'ocelot',
        'чилийская_кошка': 'kodkod',
        'кошка': 'cat',
        
        # Куньи
        'соболь': 'sable',
        'выдра': 'otter',
        'европейская_норка': 'european_mink',
        'норка': 'mink',
        
        # Еноты и мангусты
        'енот_полоскун': 'raccoon',
        'енот_ракоед': 'crab_eating_raccoon',
        'енот': 'raccoon',
        'водяной_мангуст': 'marsh_mongoose',
        'мангуст_крабоед': 'crab_eating_mongoose',
        'мангуст': 'mongoose',
        
        # Лисы
        'большеухая_лисица': 'bat_eared_fox',
        'лисица': 'fox',
        
        # Рыбы
        'судак': 'zander',
        'берш': 'volga_zander',
        'рыба_меч': 'swordfish',
        'уклейка': 'bleak',
        'горбуша': 'pink_salmon',
        'быстрянка': 'spirlin',
        'морской_конек': 'seahorse',
        'язь': 'ide',
        'электрический_угорь': 'electric_eel',
        'угорь': 'eel',
        'илистый_прыгун': 'mudskipper',
        'солнечная_рыба': 'sunfish',
        'рыба_топорик': 'hatchetfish',
        'карась': 'crucian_carp',
        'золотой_карась': 'goldfish',
        'щука': 'pike',
        'елец': 'dace',
        'сиг': 'whitefish'
    }

def process_animal_images():
    """Process all animal images according to the plan"""
    
    print("🐾 Creating Animal World Category")
    print("=" * 50)
    
    # Paths
    animals_en_dir = 'animals_en'
    animals_ru_dir = 'animals_ru'
    temp_ru_en_dir = 'temp_animals_ru_translated'
    final_animals_dir = 'data/images/animal_world'
    
    # Create directories
    os.makedirs(temp_ru_en_dir, exist_ok=True)
    os.makedirs(final_animals_dir, exist_ok=True)
    os.makedirs('data/words/ru', exist_ok=True)
    os.makedirs('data/words/en', exist_ok=True)
    
    # Step 1: Process Russian images
    print("\n📝 Step 1: Processing Russian animal images...")
    
    if not os.path.exists(animals_ru_dir):
        print(f"❌ Russian animals directory not found: {animals_ru_dir}")
        return
    
    ru_files = [f for f in os.listdir(animals_ru_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    print(f"Found {len(ru_files)} Russian animal images")
    
    translations = get_russian_to_english_translations()
    translated_count = 0
    
    for filename in ru_files:
        # Clean Russian filename
        cleaned_ru = clean_russian_filename(filename)
        print(f"  {filename} → {cleaned_ru}")
        
        # Translate to English
        if cleaned_ru in translations:
            en_name = translations[cleaned_ru]
            
            # Copy image with English name
            src_path = os.path.join(animals_ru_dir, filename)
            dst_path = os.path.join(temp_ru_en_dir, f"{en_name}.jpg")
            
            try:
                # Convert and resize image
                with Image.open(src_path) as img:
                    img = img.convert('RGB')
                    img = img.resize((300, 300), Image.Resampling.LANCZOS)
                    img.save(dst_path, 'JPEG', quality=90, optimize=True)
                
                translated_count += 1
                print(f"    ✓ Translated: {cleaned_ru} → {en_name}")
                
            except Exception as e:
                print(f"    ❌ Error processing {filename}: {e}")
        else:
            print(f"    ⚠️  No translation for: {cleaned_ru}")
    
    print(f"Successfully translated {translated_count} Russian images")
    
    # Step 2: Process English images
    print(f"\n📝 Step 2: Processing English animal images...")
    
    if not os.path.exists(animals_en_dir):
        print(f"❌ English animals directory not found: {animals_en_dir}")
        return
    
    en_files = [f for f in os.listdir(animals_en_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    print(f"Found {len(en_files)} English animal images")
    
    # Step 3: Merge without duplicates
    print(f"\n📝 Step 3: Merging images without duplicates...")
    
    final_animals = {}
    
    # Add English images first
    for filename in en_files:
        name = os.path.splitext(filename)[0].lower().replace(' ', '_')
        src_path = os.path.join(animals_en_dir, filename)
        
        try:
            # Convert and resize image
            with Image.open(src_path) as img:
                img = img.convert('RGB')
                img = img.resize((300, 300), Image.Resampling.LANCZOS)
                
                final_animals[name] = {
                    'source': 'english',
                    'original_name': filename,
                    'image': img.copy()
                }
                
        except Exception as e:
            print(f"    ❌ Error processing English {filename}: {e}")
    
    # Add translated Russian images (avoid duplicates)
    if os.path.exists(temp_ru_en_dir):
        ru_translated_files = [f for f in os.listdir(temp_ru_en_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        
        for filename in ru_translated_files:
            name = os.path.splitext(filename)[0].lower()
            
            if name not in final_animals:
                src_path = os.path.join(temp_ru_en_dir, filename)
                
                try:
                    with Image.open(src_path) as img:
                        final_animals[name] = {
                            'source': 'russian_translated',
                            'original_name': filename,
                            'image': img.copy()
                        }
                        
                except Exception as e:
                    print(f"    ❌ Error processing translated {filename}: {e}")
            else:
                print(f"    ⚠️  Duplicate skipped: {name}")
    
    print(f"Final collection: {len(final_animals)} unique animals")
    
    # Step 4: Number and save final images
    print(f"\n📝 Step 4: Numbering and saving final collection...")
    
    animal_list = []
    
    for index, (name, data) in enumerate(sorted(final_animals.items()), 1):
        # Create numbered filename
        image_code = f"ANIMAL-{index:03d}"
        image_filename = f"{image_code}.png"
        image_path = os.path.join(final_animals_dir, image_filename)
        
        # Save image
        try:
            data['image'].save(image_path, 'PNG', quality=95, optimize=True)
            
            # Add to list
            animal_list.append({
                'number': index,
                'name_en': name.replace('_', ' ').title(),
                'name_ru': name.replace('_', ' ').title(),  # Will need proper translation
                'code': image_code,
                'source': data['source']
            })
            
            print(f"  {index:3d}. {name.replace('_', ' ').title()} → {image_code}")
            
        except Exception as e:
            print(f"    ❌ Error saving {name}: {e}")
    
    # Step 5: Create category files
    print(f"\n📝 Step 5: Creating category files...")
    
    # Create Russian word list
    ru_file_path = 'data/words/ru/animal_world.txt'
    with open(ru_file_path, 'w', encoding='utf-8') as f:
        for animal in animal_list:
            f.write(f"{animal['number']} - {animal['name_ru'].upper()} - {animal['code']}\n")
    
    # Create English word list
    en_file_path = 'data/words/en/animal_world.txt'
    with open(en_file_path, 'w', encoding='utf-8') as f:
        for animal in animal_list:
            f.write(f"{animal['number']} - {animal['name_en'].upper()} - {animal['code']}\n")
    
    # Create summary report
    print(f"\n📊 SUMMARY REPORT")
    print(f"=" * 50)
    print(f"Total unique animals: {len(animal_list)}")
    print(f"From English source: {len([a for a in animal_list if a['source'] == 'english'])}")
    print(f"From Russian source: {len([a for a in animal_list if a['source'] == 'russian_translated'])}")
    print(f"Images saved to: {final_animals_dir}")
    print(f"Russian words: {ru_file_path}")
    print(f"English words: {en_file_path}")
    
    # Analysis for missing elements
    print(f"\n🔍 ANALYSIS FOR GAME REQUIREMENTS")
    print(f"=" * 50)
    
    if len(animal_list) >= 100:
        print(f"✅ Excellent! {len(animal_list)} animals is more than enough for a great category")
    elif len(animal_list) >= 50:
        print(f"✅ Good! {len(animal_list)} animals is sufficient for a solid category")
    elif len(animal_list) >= 25:
        print(f"⚠️  {len(animal_list)} animals is minimal but workable")
    else:
        print(f"❌ {len(animal_list)} animals might be too few for a good game experience")
    
    print(f"\nRecommendations:")
    print(f"- Category name: 'Животный мир' / 'Animal World'")
    print(f"- Difficulty: Medium (diverse animal types)")
    print(f"- Suitable for all age groups")
    
    # Clean up temporary directory
    if os.path.exists(temp_ru_en_dir):
        shutil.rmtree(temp_ru_en_dir)
        print(f"\n🧹 Cleaned up temporary files")
    
    print(f"\n🎉 Animal World category creation completed!")

if __name__ == "__main__":
    process_animal_images()