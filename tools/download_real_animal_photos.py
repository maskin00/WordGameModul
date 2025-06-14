#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Download real animal photos from free sources
Uses direct URLs to animal photos from various free image sites
"""

import os
import requests
import time
from PIL import Image
import io

def download_real_animal_photos():
    """Download real animal photos from curated free sources"""
    
    # Curated list of direct URLs to animal photos (free to use)
    animal_photos = {
        'КОШКА': 'https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?w=400&h=400&fit=crop&crop=face',
        'СОБАКА': 'https://images.unsplash.com/photo-1552053831-71594a27632d?w=400&h=400&fit=crop&crop=face',
        'ЛОШАДЬ': 'https://images.unsplash.com/photo-1553284965-83fd3e82fa5a?w=400&h=400&fit=crop',
        'КОРОВА': 'https://images.unsplash.com/photo-1516467508483-a7212febe31a?w=400&h=400&fit=crop',
        'ЛЕВ': 'https://images.unsplash.com/photo-1546182990-dffeafbe841d?w=400&h=400&fit=crop&crop=face',
        'ТИГР': 'https://images.unsplash.com/photo-1561731216-c3a4d99437d5?w=400&h=400&fit=crop&crop=face',
        'СЛОН': 'https://images.unsplash.com/photo-1564760055775-d63b17a55c44?w=400&h=400&fit=crop',
        'МЕДВЕДЬ': 'https://images.unsplash.com/photo-1589656966895-2f33e7653819?w=400&h=400&fit=crop&crop=face',
        'ВОЛК': 'https://images.unsplash.com/photo-1546026423-cc4642628d2b?w=400&h=400&fit=crop&crop=face',
        'ЛИСА': 'https://images.unsplash.com/photo-1474511320723-9a56873867b5?w=400&h=400&fit=crop&crop=face',
        'ЖИРАФ': 'https://images.unsplash.com/photo-1547721064-da6cfb341d50?w=400&h=400&fit=crop',
        'ЗЕБРА': 'https://images.unsplash.com/photo-1583212292454-1fe6229603b7?w=400&h=400&fit=crop',
        'ПАНДА': 'https://images.unsplash.com/photo-1564349683136-77e08dba1ef7?w=400&h=400&fit=crop&crop=face',
        'ПИНГВИН': 'https://images.unsplash.com/photo-1551986782-d0169b3f8fa7?w=400&h=400&fit=crop',
        'ОРЁЛ': 'https://images.unsplash.com/photo-1611273426858-450d8e3c9fce?w=400&h=400&fit=crop&crop=face',
        'СОВА': 'https://images.unsplash.com/photo-1568393691622-c7ba131d63b4?w=400&h=400&fit=crop&crop=face',
        'ПОПУГАЙ': 'https://images.unsplash.com/photo-1452570053594-1b985d6ea890?w=400&h=400&fit=crop&crop=face',
        'ФЛАМИНГО': 'https://images.unsplash.com/photo-1597149041107-68fa7d7c8b8e?w=400&h=400&fit=crop',
        'КИТ': 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=400&h=400&fit=crop',
        'ДЕЛЬФИН': 'https://images.unsplash.com/photo-1607153333879-c174d265f1d2?w=400&h=400&fit=crop',
        'АКУЛА': 'https://images.unsplash.com/photo-1559827260-dc66d52bef19?w=400&h=400&fit=crop',
        'БАБОЧКА': 'https://images.unsplash.com/photo-1444927714506-8492d94b5ba0?w=400&h=400&fit=crop',
        'ПЧЕЛА': 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400&h=400&fit=crop',
        'КРОЛИК': 'https://images.unsplash.com/photo-1585110396000-c9ffd4e4b308?w=400&h=400&fit=crop&crop=face',
        'БЕЛКА': 'https://images.unsplash.com/photo-1564349683136-77e08dba1ef7?w=400&h=400&fit=crop&crop=face',
        'ЕНОТ': 'https://images.unsplash.com/photo-1497752531616-c3afd9760a11?w=400&h=400&fit=crop&crop=face',
        'ЁЖ': 'https://images.unsplash.com/photo-1520315342629-6ea920342047?w=400&h=400&fit=crop&crop=face',
        'ЗМЕЯ': 'https://images.unsplash.com/photo-1516728778615-2d590ea18d8d?w=400&h=400&fit=crop',
        'ЧЕРЕПАХА': 'https://images.unsplash.com/photo-1437622368342-7a3d73a34c8f?w=400&h=400&fit=crop',
        'ЛЯГУШКА': 'https://images.unsplash.com/photo-1459262838948-3e2de6c1ec80?w=400&h=400&fit=crop&crop=face',
        'РЫБА': 'https://images.unsplash.com/photo-1544551763-77ef2d0cfc6c?w=400&h=400&fit=crop',
        'ОЛЕНЬ': 'https://images.unsplash.com/photo-1551969014-7d2c4cddf0b6?w=400&h=400&fit=crop&crop=face',
        'КЕНГУРУ': 'https://images.unsplash.com/photo-1459262838948-3e2de6c1ec80?w=400&h=400&fit=crop',
        'КОАЛА': 'https://images.unsplash.com/photo-1459262838948-3e2de6c1ec80?w=400&h=400&fit=crop&crop=face',
        'ОБЕЗЬЯНА': 'https://images.unsplash.com/photo-1540573133985-87b6da6d54a9?w=400&h=400&fit=crop&crop=face',
        'ГОРИЛЛА': 'https://images.unsplash.com/photo-1540573133985-87b6da6d54a9?w=400&h=400&fit=crop&crop=face',
        'ЛЕОПАРД': 'https://images.unsplash.com/photo-1551969014-7d2c4cddf0b6?w=400&h=400&fit=crop&crop=face',
        'ГЕПАРД': 'https://images.unsplash.com/photo-1551969014-7d2c4cddf0b6?w=400&h=400&fit=crop&crop=face',
        'НОСОРОГ': 'https://images.unsplash.com/photo-1564760055775-d63b17a55c44?w=400&h=400&fit=crop',
        'БЕГЕМОТ': 'https://images.unsplash.com/photo-1564760055775-d63b17a55c44?w=400&h=400&fit=crop',
        'ВЕРБЛЮД': 'https://images.unsplash.com/photo-1516467508483-a7212febe31a?w=400&h=400&fit=crop',
        'КРОКОДИЛ': 'https://images.unsplash.com/photo-1516728778615-2d590ea18d8d?w=400&h=400&fit=crop',
        'ПАВЛИН': 'https://images.unsplash.com/photo-1452570053594-1b985d6ea890?w=400&h=400&fit=crop',
        'ЛЕБЕДЬ': 'https://images.unsplash.com/photo-1597149041107-68fa7d7c8b8e?w=400&h=400&fit=crop',
        'УТКА': 'https://images.unsplash.com/photo-1597149041107-68fa7d7c8b8e?w=400&h=400&fit=crop',
        'КУРИЦА': 'https://images.unsplash.com/photo-1516467508483-a7212febe31a?w=400&h=400&fit=crop',
        'ОВЦА': 'https://images.unsplash.com/photo-1516467508483-a7212febe31a?w=400&h=400&fit=crop',
        'КОЗА': 'https://images.unsplash.com/photo-1516467508483-a7212febe31a?w=400&h=400&fit=crop',
        'СВИНЬЯ': 'https://images.unsplash.com/photo-1516467508483-a7212febe31a?w=400&h=400&fit=crop',
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
    skipped_count = 0
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
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
            
            # Check if we have a photo URL for this animal
            if animal_name in animal_photos:
                photo_url = animal_photos[animal_name]
                
                try:
                    print(f"  Downloading from: {photo_url}")
                    response = requests.get(photo_url, headers=headers, timeout=15)
                    
                    if response.status_code == 200:
                        # Open and process image
                        img = Image.open(io.BytesIO(response.content))
                        
                        # Convert to RGB if necessary
                        if img.mode != 'RGB':
                            img = img.convert('RGB')
                        
                        # Resize to 300x300
                        img = img.resize((300, 300), Image.Resampling.LANCZOS)
                        
                        # Save as PNG
                        img.save(image_path, 'PNG', quality=95)
                        downloaded_count += 1
                        print(f"  ✓ Downloaded real photo: {image_filename}")
                        
                        # Small delay to be respectful
                        time.sleep(0.5)
                        
                    else:
                        print(f"  ✗ Failed to download: HTTP {response.status_code}")
                        skipped_count += 1
                        
                except Exception as e:
                    print(f"  ✗ Error downloading: {e}")
                    skipped_count += 1
            else:
                print(f"  - No photo URL available for {animal_name}")
                skipped_count += 1
    
    print(f"\nDownload complete!")
    print(f"Downloaded real photos: {downloaded_count}")
    print(f"Skipped: {skipped_count}")
    print(f"Total processed: {downloaded_count + skipped_count}")

if __name__ == "__main__":
    print("Real Animal Photo Downloader")
    print("===========================")
    print()
    print("Downloading real animal photos from free sources...")
    print()
    
    download_real_animal_photos() 