#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re

def analyze_real_files():
    """Analyze actual file names in both directories"""
    
    print("📁 ANALYZING REAL FILES")
    print("=" * 50)
    
    # Get English files
    en_dir = 'animals_en'
    en_files = [f for f in os.listdir(en_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    
    print(f"\n🇺🇸 ENGLISH FILES ({len(en_files)}):")
    print("-" * 30)
    for i, f in enumerate(sorted(en_files)[:20], 1):  # Show first 20
        name = os.path.splitext(f)[0]
        print(f"{i:2d}. {name}")
    if len(en_files) > 20:
        print(f"... and {len(en_files) - 20} more")
    
    # Get Russian files  
    ru_dir = 'animals_ru'
    ru_files = [f for f in os.listdir(ru_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    
    print(f"\n🇷🇺 RUSSIAN FILES ({len(ru_files)}):")
    print("-" * 30)
    for i, f in enumerate(sorted(ru_files)[:20], 1):  # Show first 20
        name = os.path.splitext(f)[0]
        print(f"{i:2d}. {name}")
    if len(ru_files) > 20:
        print(f"... and {len(ru_files) - 20} more")
    
    # Clean Russian names and show examples
    print(f"\n🧹 CLEANING RUSSIAN NAMES (examples):")
    print("-" * 40)
    
    def clean_russian_name(filename):
        name = os.path.splitext(filename)[0].lower()
        # Remove common extra words
        extra_words = ['_фото', 'фото_', 'фото', '_животное', 'животное_', 'животное']
        for word in extra_words:
            name = name.replace(word, '')
        name = re.sub(r'_+', '_', name).strip('_')
        return name
    
    for f in sorted(ru_files)[:10]:
        original = os.path.splitext(f)[0]
        cleaned = clean_russian_name(f)
        print(f"  {original} → {cleaned}")
    
    print(f"\n📊 SUMMARY:")
    print(f"  English files: {len(en_files)}")
    print(f"  Russian files: {len(ru_files)}")
    print(f"  Total: {len(en_files) + len(ru_files)}")

if __name__ == "__main__":
    analyze_real_files() 