#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

def count_files():
    en_files = [f for f in os.listdir('animals_en') if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    ru_files = [f for f in os.listdir('animals_ru') if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    
    print(f"English files: {len(en_files)}")
    print(f"Russian files: {len(ru_files)}")
    print(f"Total: {len(en_files) + len(ru_files)}")

if __name__ == "__main__":
    count_files() 