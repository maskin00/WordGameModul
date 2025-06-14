#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json

def check_animal_category():
    """Check current state of animal category"""
    
    print("🔍 CHECKING ANIMAL CATEGORY")
    print("=" * 40)
    
    # Check images
    images_dir = 'data/images/animal_world'
    if os.path.exists(images_dir):
        images = [f for f in os.listdir(images_dir) if f.endswith('.png')]
        print(f"✅ Images: {len(images)} files in {images_dir}")
        print(f"   Range: {images[0]} to {images[-1]}")
    else:
        print(f"❌ Images directory missing: {images_dir}")
    
    # Check word files
    languages = ['en', 'ru', 'es', 'fr']
    word_files = {}
    
    for lang in languages:
        file_path = f'data/words/{lang}/animal_world.txt'
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            word_files[lang] = len(lines)
            print(f"✅ {lang.upper()}: {len(lines)} words in {file_path}")
        else:
            word_files[lang] = 0
            print(f"❌ {lang.upper()}: Missing {file_path}")
    
    # Check categories.json
    categories_file = 'data/categories.json'
    if os.path.exists(categories_file):
        with open(categories_file, 'r', encoding='utf-8') as f:
            categories = json.load(f)
        
        animal_category = None
        for cat in categories:
            if cat.get('id') == 'animal_world':
                animal_category = cat
                break
        
        if animal_category:
            print(f"✅ Category found in {categories_file}")
            print(f"   Name: {animal_category.get('name', {})}")
            print(f"   Description: {animal_category.get('description', {})}")
        else:
            print(f"❌ Category 'animal_world' not found in {categories_file}")
    else:
        print(f"❌ Categories file missing: {categories_file}")
    
    # Check image mappings
    mappings_dir = 'data/image_mappings'
    if os.path.exists(mappings_dir):
        for lang in languages:
            mapping_file = f'{mappings_dir}/animal_world_{lang}.json'
            if os.path.exists(mapping_file):
                with open(mapping_file, 'r', encoding='utf-8') as f:
                    mappings = json.load(f)
                print(f"✅ {lang.upper()} mappings: {len(mappings)} entries in {mapping_file}")
            else:
                print(f"❌ {lang.upper()} mappings: Missing {mapping_file}")
    else:
        print(f"❌ Image mappings directory missing: {mappings_dir}")
    
    print(f"\n📊 SUMMARY:")
    print(f"   Images: {len(images) if 'images' in locals() else 0}")
    print(f"   Word files: {sum(1 for count in word_files.values() if count > 0)}/4 languages")
    print(f"   Category definition: {'✅' if 'animal_category' in locals() and animal_category else '❌'}")
    print(f"   Image mappings: {sum(1 for lang in languages if os.path.exists(f'data/image_mappings/animal_world_{lang}.json'))}/4 languages")

if __name__ == "__main__":
    check_animal_category() 