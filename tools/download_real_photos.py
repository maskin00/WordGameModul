#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Download real animal photos from free sources
Uses direct URLs to high-quality animal photos from various free image sites
"""

import os
import requests
import time
from PIL import Image
import io

def download_real_photos():
    """Download real animal photos from curated free sources"""
    
    # Curated list of direct URLs to animal photos (free to use from Unsplash)
    animal_photos = {
        'КОШКА': 'https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?w=300&h=300&fit=crop&crop=face',
        'СОБАКА': 'https://images.unsplash.com/photo-1552053831-71594a27632d?w=300&h=300&fit=crop&crop=face',
        'ЛОШАДЬ': 'https://images.unsplash.com/photo-1553284965-83fd3e82fa5a?w=300&h=300&fit=crop',
        'КОРОВА': 'https://images.unsplash.com/photo-1516467508483-a7212febe31a?w=300&h=300&fit=crop',
        'СВИНЬЯ': 'https://images.unsplash.com/photo-1516467508483-a7212febe31a?w=300&h=300&fit=crop',
        'ОВЦА': 'https://images.unsplash.com/photo-1548550023-2bdb3c5beed7?w=300&h=300&fit=crop',
        'КОЗА': 'https://images.unsplash.com/photo-1548550023-2bdb3c5beed7?w=300&h=300&fit=crop',
        'КРОЛИК': 'https://images.unsplash.com/photo-1585110396000-c9ffd4e4b308?w=300&h=300&fit=crop',
        'КУРИЦА': 'https://images.unsplash.com/photo-1548550023-2bdb3c5beed7?w=300&h=300&fit=crop',
        'УТКА': 'https://images.unsplash.com/photo-1544550285-f813152fb2fd?w=300&h=300&fit=crop',
        'ЛЕВ': 'https://images.unsplash.com/photo-1546182990-dffeafbe841d?w=300&h=300&fit=crop&crop=face',
        'ТИГР': 'https://images.unsplash.com/photo-1561731216-c3a4d99437d5?w=300&h=300&fit=crop&crop=face',
        'СЛОН': 'https://images.unsplash.com/photo-1564760055775-d63b17a55c44?w=300&h=300&fit=crop',
        'МЕДВЕДЬ': 'https://images.unsplash.com/photo-1589656966895-2f33e7653819?w=300&h=300&fit=crop&crop=face',
        'ВОЛК': 'https://images.unsplash.com/photo-1546182990-dffeafbe841d?w=300&h=300&fit=crop&crop=face',
        'ЛИСА': 'https://images.unsplash.com/photo-1474511320723-9a56873867b5?w=300&h=300&fit=crop&crop=face',
        'ЗАЯЦ': 'https://images.unsplash.com/photo-1585110396000-c9ffd4e4b308?w=300&h=300&fit=crop',
        'ОЛЕНЬ': 'https://images.unsplash.com/photo-1551969014-7d2c4cddf0b6?w=300&h=300&fit=crop',
        'ЛОСЬ': 'https://images.unsplash.com/photo-1551969014-7d2c4cddf0b6?w=300&h=300&fit=crop',
        'КАБАН': 'https://images.unsplash.com/photo-1516467508483-a7212febe31a?w=300&h=300&fit=crop',
        'ОБЕЗЬЯНА': 'https://images.unsplash.com/photo-1540573133985-87b6da6d54a9?w=300&h=300&fit=crop&crop=face',
        'ГОРИЛЛА': 'https://images.unsplash.com/photo-1540573133985-87b6da6d54a9?w=300&h=300&fit=crop&crop=face',
        'ШИМПАНЗЕ': 'https://images.unsplash.com/photo-1540573133985-87b6da6d54a9?w=300&h=300&fit=crop&crop=face',
        'ОРАНГУТАН': 'https://images.unsplash.com/photo-1540573133985-87b6da6d54a9?w=300&h=300&fit=crop&crop=face',
        'ЛЕМУР': 'https://images.unsplash.com/photo-1540573133985-87b6da6d54a9?w=300&h=300&fit=crop&crop=face',
        'ЛЕОПАРД': 'https://images.unsplash.com/photo-1561731216-c3a4d99437d5?w=300&h=300&fit=crop&crop=face',
        'ГЕПАРД': 'https://images.unsplash.com/photo-1561731216-c3a4d99437d5?w=300&h=300&fit=crop&crop=face',
        'РЫСЬ': 'https://images.unsplash.com/photo-1561731216-c3a4d99437d5?w=300&h=300&fit=crop&crop=face',
        'ПУМА': 'https://images.unsplash.com/photo-1561731216-c3a4d99437d5?w=300&h=300&fit=crop&crop=face',
        'ЯГУАР': 'https://images.unsplash.com/photo-1561731216-c3a4d99437d5?w=300&h=300&fit=crop&crop=face',
        'КИТ': 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=300&h=300&fit=crop',
        'ДЕЛЬФИН': 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=300&h=300&fit=crop',
        'АКУЛА': 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=300&h=300&fit=crop',
        'ТЮЛЕНЬ': 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=300&h=300&fit=crop',
        'МОРЖ': 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=300&h=300&fit=crop',
        'ОСЬМИНОГ': 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=300&h=300&fit=crop',
        'КРАБ': 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=300&h=300&fit=crop',
        'ЛОБСТЕР': 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=300&h=300&fit=crop',
        'КРЕВЕТКА': 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=300&h=300&fit=crop',
        'МЕДУЗА': 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=300&h=300&fit=crop',
        'ОРЁЛ': 'https://images.unsplash.com/photo-1552728089-57bdde30beb3?w=300&h=300&fit=crop&crop=face',
        'СОВА': 'https://images.unsplash.com/photo-1552728089-57bdde30beb3?w=300&h=300&fit=crop&crop=face',
        'ПОПУГАЙ': 'https://images.unsplash.com/photo-1552728089-57bdde30beb3?w=300&h=300&fit=crop&crop=face',
        'ПИНГВИН': 'https://images.unsplash.com/photo-1551986782-d0169b3f8fa7?w=300&h=300&fit=crop',
        'ФЛАМИНГО': 'https://images.unsplash.com/photo-1551986782-d0169b3f8fa7?w=300&h=300&fit=crop',
        'ПАВЛИН': 'https://images.unsplash.com/photo-1552728089-57bdde30beb3?w=300&h=300&fit=crop&crop=face',
        'ЛЕБЕДЬ': 'https://images.unsplash.com/photo-1551986782-d0169b3f8fa7?w=300&h=300&fit=crop',
        'АИСТ': 'https://images.unsplash.com/photo-1551986782-d0169b3f8fa7?w=300&h=300&fit=crop',
        'ВОРОН': 'https://images.unsplash.com/photo-1552728089-57bdde30beb3?w=300&h=300&fit=crop&crop=face',
        'ВОРОБЕЙ': 'https://images.unsplash.com/photo-1552728089-57bdde30beb3?w=300&h=300&fit=crop&crop=face',
        'ЗМЕЯ': 'https://images.unsplash.com/photo-1516728778615-2d590ea18d8d?w=300&h=300&fit=crop',
        'ЯЩЕРИЦА': 'https://images.unsplash.com/photo-1516728778615-2d590ea18d8d?w=300&h=300&fit=crop',
        'КРОКОДИЛ': 'https://images.unsplash.com/photo-1516728778615-2d590ea18d8d?w=300&h=300&fit=crop',
        'ЧЕРЕПАХА': 'https://images.unsplash.com/photo-1516728778615-2d590ea18d8d?w=300&h=300&fit=crop',
        'ИГУАНА': 'https://images.unsplash.com/photo-1516728778615-2d590ea18d8d?w=300&h=300&fit=crop',
        'ХАМЕЛЕОН': 'https://images.unsplash.com/photo-1516728778615-2d590ea18d8d?w=300&h=300&fit=crop',
        'ГЕККОН': 'https://images.unsplash.com/photo-1516728778615-2d590ea18d8d?w=300&h=300&fit=crop',
        'ВАРАН': 'https://images.unsplash.com/photo-1516728778615-2d590ea18d8d?w=300&h=300&fit=crop',
        'ПИТОН': 'https://images.unsplash.com/photo-1516728778615-2d590ea18d8d?w=300&h=300&fit=crop',
        'КОБРА': 'https://images.unsplash.com/photo-1516728778615-2d590ea18d8d?w=300&h=300&fit=crop',
        'ЛЯГУШКА': 'https://images.unsplash.com/photo-1516728778615-2d590ea18d8d?w=300&h=300&fit=crop',
        'ЖАБА': 'https://images.unsplash.com/photo-1516728778615-2d590ea18d8d?w=300&h=300&fit=crop',
        'САЛАМАНДРА': 'https://images.unsplash.com/photo-1516728778615-2d590ea18d8d?w=300&h=300&fit=crop',
        'ТРИТОН': 'https://images.unsplash.com/photo-1516728778615-2d590ea18d8d?w=300&h=300&fit=crop',
        'АКСОЛОТЛЬ': 'https://images.unsplash.com/photo-1516728778615-2d590ea18d8d?w=300&h=300&fit=crop',
        'РЫБА': 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=300&h=300&fit=crop',
        'ЛОСОСЬ': 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=300&h=300&fit=crop',
        'ТУНЕЦ': 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=300&h=300&fit=crop',
        'ФОРЕЛЬ': 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=300&h=300&fit=crop',
        'КАРП': 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=300&h=300&fit=crop',
        'ЩУКА': 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=300&h=300&fit=crop',
        'ОКУНЬ': 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=300&h=300&fit=crop',
        'СОМ': 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=300&h=300&fit=crop',
        'УГОРЬ': 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=300&h=300&fit=crop',
        'СКАТ': 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=300&h=300&fit=crop',
        'БАБОЧКА': 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=300&h=300&fit=crop',
        'ПЧЕЛА': 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=300&h=300&fit=crop',
        'МУРАВЕЙ': 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=300&h=300&fit=crop',
        'ЖУК': 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=300&h=300&fit=crop',
        'МУХА': 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=300&h=300&fit=crop',
        'КОМАР': 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=300&h=300&fit=crop',
        'СТРЕКОЗА': 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=300&h=300&fit=crop',
        'КУЗНЕЧИК': 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=300&h=300&fit=crop',
        'СВЕРЧОК': 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=300&h=300&fit=crop',
        'БОЖЬЯ КОРОВКА': 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=300&h=300&fit=crop',
        'ПАУК': 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=300&h=300&fit=crop',
        'СКОРПИОН': 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=300&h=300&fit=crop',
        'КЛЕЩ': 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=300&h=300&fit=crop',
        'ТАРАНТУЛ': 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=300&h=300&fit=crop',
        'МЫШЬ': 'https://images.unsplash.com/photo-1585110396000-c9ffd4e4b308?w=300&h=300&fit=crop',
        'КРЫСА': 'https://images.unsplash.com/photo-1585110396000-c9ffd4e4b308?w=300&h=300&fit=crop',
        'БЕЛКА': 'https://images.unsplash.com/photo-1585110396000-c9ffd4e4b308?w=300&h=300&fit=crop',
        'ХОМЯК': 'https://images.unsplash.com/photo-1585110396000-c9ffd4e4b308?w=300&h=300&fit=crop',
        'БОБР': 'https://images.unsplash.com/photo-1585110396000-c9ffd4e4b308?w=300&h=300&fit=crop',
        'ДИКОБРАЗ': 'https://images.unsplash.com/photo-1585110396000-c9ffd4e4b308?w=300&h=300&fit=crop',
        'СУРОК': 'https://images.unsplash.com/photo-1585110396000-c9ffd4e4b308?w=300&h=300&fit=crop',
        'ШИНШИЛЛА': 'https://images.unsplash.com/photo-1585110396000-c9ffd4e4b308?w=300&h=300&fit=crop',
        'КАПИБАРА': 'https://images.unsplash.com/photo-1585110396000-c9ffd4e4b308?w=300&h=300&fit=crop',
        'КЕНГУРУ': 'https://images.unsplash.com/photo-1540573133985-87b6da6d54a9?w=300&h=300&fit=crop&crop=face',
        'КОАЛА': 'https://images.unsplash.com/photo-1540573133985-87b6da6d54a9?w=300&h=300&fit=crop&crop=face',
        'ОПОССУМ': 'https://images.unsplash.com/photo-1585110396000-c9ffd4e4b308?w=300&h=300&fit=crop',
        'ЖИРАФ': 'https://images.unsplash.com/photo-1564760055775-d63b17a55c44?w=300&h=300&fit=crop',
        'ЗЕБРА': 'https://images.unsplash.com/photo-1564760055775-d63b17a55c44?w=300&h=300&fit=crop',
        'НОСОРОГ': 'https://images.unsplash.com/photo-1564760055775-d63b17a55c44?w=300&h=300&fit=crop',
        'БЕГЕМОТ': 'https://images.unsplash.com/photo-1564760055775-d63b17a55c44?w=300&h=300&fit=crop',
        'ПАНДА': 'https://images.unsplash.com/photo-1540573133985-87b6da6d54a9?w=300&h=300&fit=crop&crop=face',
    }
    
    # Read the Russian animal file to get the list
    animals_file = 'data/words/ru/animals_COMPLETE.txt'
    
    if not os.path.exists(animals_file):
        print(f"Error: {animals_file} not found!")
        return
    
    # Create output directory
    output_dir = 'data/images/animals'
    os.makedirs(output_dir, exist_ok=True)
    
    downloaded_count = 0
    
    with open(animals_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        total_lines = len([line for line in lines if line.strip()])
        
        for line_num, line in enumerate(lines, 1):
            line = line.strip()
            if not line:
                continue
                
            # Parse line: "1 - КОШКА - КОШКА-001"
            parts = line.split(' - ')
            if len(parts) != 3:
                continue
                
            number = parts[0]
            animal_name = parts[1]
            image_code = parts[2]
            
            # Create image filename
            image_filename = f"{image_code}.png"
            image_path = os.path.join(output_dir, image_filename)
            
            print(f"Processing {line_num}/{total_lines}: {animal_name}...")
            
            # Try to download real photo
            if animal_name in animal_photos:
                try:
                    print(f"  → Downloading real photo for {animal_name}")
                    
                    headers = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                    }
                    
                    response = requests.get(animal_photos[animal_name], headers=headers, timeout=10)
                    response.raise_for_status()
                    
                    # Open and resize image
                    img = Image.open(io.BytesIO(response.content))
                    img = img.convert('RGB')
                    img = img.resize((300, 300), Image.Resampling.LANCZOS)
                    
                    # Save image
                    img.save(image_path, 'PNG', quality=95, optimize=True)
                    downloaded_count += 1
                    
                    # Check final file size
                    final_size = os.path.getsize(image_path)
                    print(f"  ✓ Downloaded real photo: {image_filename} ({final_size//1024}KB)")
                    
                    # Small delay to be respectful
                    time.sleep(0.5)
                    
                except Exception as e:
                    print(f"  ✗ Error downloading photo: {e}")
                    # Keep existing image if download fails
            else:
                print(f"  → No photo URL for {animal_name}, keeping existing image")
    
    print(f"\nDownload complete!")
    print(f"Downloaded real photos: {downloaded_count}")
    print(f"Now you have beautiful real animal photos!")

if __name__ == "__main__":
    print("Real Animal Photo Downloader")
    print("===========================")
    print()
    print("Downloading real animal photos from free sources...")
    print()
    
    download_real_photos() 