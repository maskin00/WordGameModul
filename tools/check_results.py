#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

def check_results():
    """Check what files were actually created"""
    
    print("🔍 CHECKING RESULTS")
    print("=" * 30)
    
    # Check animal_world directory
    animal_dir = 'data/images/animal_world'
    if os.path.exists(animal_dir):
        files = [f for f in os.listdir(animal_dir) if f.endswith('.png')]
        print(f"Files in {animal_dir}: {len(files)}")
        
        if files:
            print("First 10 files:")
            for f in sorted(files)[:10]:
                print(f"  {f}")
            
            if len(files) > 10:
                print(f"  ... and {len(files) - 10} more")
        else:
            print("  No PNG files found!")
    else:
        print(f"Directory {animal_dir} does not exist!")
    
    # Check word files
    en_file = 'data/words/en/animal_world.txt'
    ru_file = 'data/words/ru/animal_world.txt'
    
    print(f"\n📄 WORD FILES:")
    
    if os.path.exists(en_file):
        with open(en_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        print(f"English file: {len(lines)} lines")
        print("First 5 lines:")
        for line in lines[:5]:
            print(f"  {line.strip()}")
    else:
        print(f"English file {en_file} does not exist!")
    
    if os.path.exists(ru_file):
        with open(ru_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        print(f"Russian file: {len(lines)} lines")
    else:
        print(f"Russian file {ru_file} does not exist!")

if __name__ == "__main__":
    check_results() 