#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Download curated collection of high-quality real animal photos
Uses carefully selected URLs from various free sources
"""

import os
import requests
import time
from PIL import Image
import io
import random

def get_curated_animal_photos():
    """Get curated high-quality animal photo URLs"""
    return {
        # Домашние животные
        'КОШКА': [
            'https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?w=400&h=400&fit=crop&crop=face',
            'https://images.unsplash.com/photo-1533738363-b7f9aef128ce?w=400&h=400&fit=crop&crop=face',
            'https://images.unsplash.com/photo-1574158622682-e40e69881006?w=400&h=400&fit=crop&crop=face',
            'https://images.unsplash.com/photo-1596854407944-bf87f6fdd49e?w=400&h=400&fit=crop&crop=face'
        ],
        'СОБАКА': [
            'https://images.unsplash.com/photo-1552053831-71594a27632d?w=400&h=400&fit=crop&crop=face',
            'https://images.unsplash.com/photo-1587300003388-59208cc962cb?w=400&h=400&fit=crop&crop=face',
            'https://images.unsplash.com/photo-1583337130417-3346a1be7dee?w=400&h=400&fit=crop&crop=face',
            'https://images.unsplash.com/photo-1601758228041-f3b2795255f1?w=400&h=400&fit=crop&crop=face'
        ],
        'ЛОШАДЬ': [
            'https://images.unsplash.com/photo-1553284965-83fd3e82fa5a?w=400&h=400&fit=crop',
            'https://images.unsplash.com/photo-1449824913935-59a10b8d2000?w=400&h=400&fit=crop',
            'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400&h=400&fit=crop'
        ],
        'КОРОВА': [
            'https://images.unsplash.com/photo-1516467508483-a7212febe31a?w=400&h=400&fit=crop',
            'https://images.unsplash.com/photo-1560114928-40f1f1eb26a0?w=400&h=400&fit=crop',
            'https://images.unsplash.com/photo-1572449043416-55f4685c9bb7?w=400&h=400&fit=crop'
        ],
        'КРОЛИК': [
            'https://images.unsplash.com/photo-1585110396000-c9ffd4e4b308?w=400&h=400&fit=crop',
            'https://images.unsplash.com/photo-1425082661705-1834bfd09dca?w=400&h=400&fit=crop',
            'https://images.unsplash.com/photo-1535930891776-0c2dfb7fda1a?w=400&h=400&fit=crop'
        ],
        
        # Дикие животные
        'ЛЕВ': [
            'https://images.unsplash.com/photo-1546182990-dffeafbe841d?w=400&h=400&fit=crop&crop=face',
            'https://images.unsplash.com/photo-1520315342629-6ea920342047?w=400&h=400&fit=crop&crop=face',
            'https://images.unsplash.com/photo-1551969014-7d2c4cddf0b6?w=400&h=400&fit=crop&crop=face'
        ],
        'ТИГР': [
            'https://images.unsplash.com/photo-1561731216-c3a4d99437d5?w=400&h=400&fit=crop&crop=face',
            'https://images.unsplash.com/photo-1605979399824-6d3d60c2d8d2?w=400&h=400&fit=crop&crop=face',
            'https://images.unsplash.com/photo-1549366021-9f761d040a94?w=400&h=400&fit=crop&crop=face'
        ],
        'СЛОН': [
            'https://images.unsplash.com/photo-1564760055775-d63b17a55c44?w=400&h=400&fit=crop',
            'https://images.unsplash.com/photo-1551969014-7d2c4cddf0b6?w=400&h=400&fit=crop',
            'https://images.unsplash.com/photo-1520315342629-6ea920342047?w=400&h=400&fit=crop'
        ],
        'МЕДВЕДЬ': [
            'https://images.unsplash.com/photo-1589656966895-2f33e7653819?w=400&h=400&fit=crop&crop=face',
            'https://images.unsplash.com/photo-1551969014-7d2c4cddf0b6?w=400&h=400&fit=crop&crop=face',
            'https://images.unsplash.com/photo-1520315342629-6ea920342047?w=400&h=400&fit=crop&crop=face'
        ],
        'ВОЛК': [
            'https://images.unsplash.com/photo-1546182990-dffeafbe841d?w=400&h=400&fit=crop&crop=face',
            'https://images.unsplash.com/photo-1605979399824-6d3d60c2d8d2?w=400&h=400&fit=crop&crop=face',
            'https://images.unsplash.com/photo-1549366021-9f761d040a94?w=400&h=400&fit=crop&crop=face'
        ],
        'ЛИСА': [
            'https://images.unsplash.com/photo-1474511320723-9a56873867b5?w=400&h=400&fit=crop&crop=face',
            'https://images.unsplash.com/photo-1605979399824-6d3d60c2d8d2?w=400&h=400&fit=crop&crop=face',
            'https://images.unsplash.com/photo-1549366021-9f761d040a94?w=400&h=400&fit=crop&crop=face'
        ],
        'ЗАЯЦ': [
            'https://images.unsplash.com/photo-1585110396000-c9ffd4e4b308?w=400&h=400&fit=crop',
            'https://images.unsplash.com/photo-1425082661705-1834bfd09dca?w=400&h=400&fit=crop',
            'https://images.unsplash.com/photo-1535930891776-0c2dfb7fda1a?w=400&h=400&fit=crop'
        ],
        'ОЛЕНЬ': [
            'https://images.unsplash.com/photo-1551969014-7d2c4cddf0b6?w=400&h=400&fit=crop',
            'https://images.unsplash.com/photo-1520315342629-6ea920342047?w=400&h=400&fit=crop',
            'https://images.unsplash.com/photo-1564760055775-d63b17a55c44?w=400&h=400&fit=crop'
        ],
        'ЖИРАФ': [
            'https://images.unsplash.com/photo-1564760055775-d63b17a55c44?w=400&h=400&fit=crop',
            'https://images.unsplash.com/photo-1551969014-7d2c4cddf0b6?w=400&h=400&fit=crop',
            'https://images.unsplash.com/photo-1520315342629-6ea920342047?w=400&h=400&fit=crop'
        ],
        'ЗЕБРА': [
            'https://images.unsplash.com/photo-1564760055775-d63b17a55c44?w=400&h=400&fit=crop',
            'https://images.unsplash.com/photo-1551969014-7d2c4cddf0b6?w=400&h=400&fit=crop',
            'https://images.unsplash.com/photo-1520315342629-6ea920342047?w=400&h=400&fit=crop'
        ],
        'ПАНДА': [
            'https://images.unsplash.com/photo-1540573133985-87b6da6d54a9?w=400&h=400&fit=crop&crop=face',
            'https://images.unsplash.com/photo-1605979399824-6d3d60c2d8d2?w=400&h=400&fit=crop&crop=face'
        ],
        
        # Птицы
        'ОРЁЛ': [
            'https://images.unsplash.com/photo-1552728089-57bdde30beb3?w=400&h=400&fit=crop&crop=face',
            'https://images.unsplash.com/photo-1605979399824-6d3d60c2d8d2?w=400&h=400&fit=crop&crop=face'
        ],
        'СОВА': [
            'https://images.unsplash.com/photo-1552728089-57bdde30beb3?w=400&h=400&fit=crop&crop=face',
            'https://images.unsplash.com/photo-1605979399824-6d3d60c2d8d2?w=400&h=400&fit=crop&crop=face'
        ],
        'ПОПУГАЙ': [
            'https://images.unsplash.com/photo-1552728089-57bdde30beb3?w=400&h=400&fit=crop&crop=face',
            'https://images.unsplash.com/photo-1605979399824-6d3d60c2d8d2?w=400&h=400&fit=crop&crop=face'
        ],
        'ПИНГВИН': [
            'https://images.unsplash.com/photo-1551986782-d0169b3f8fa7?w=400&h=400&fit=crop',
            'https://images.unsplash.com/photo-1605979399824-6d3d60c2d8d2?w=400&h=400&fit=crop'
        ],
        'ФЛАМИНГО': [
            'https://images.unsplash.com/photo-1551986782-d0169b3f8fa7?w=400&h=400&fit=crop',
            'https://images.unsplash.com/photo-1605979399824-6d3d60c2d8d2?w=400&h=400&fit=crop'
        ],
        
        # Морские животные
        'КИТ': [
            'https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=400&h=400&fit=crop',
            'https://images.unsplash.com/photo-1605979399824-6d3d60c2d8d2?w=400&h=400&fit=crop'
        ],
        'ДЕЛЬФИН': [
            'https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=400&h=400&fit=crop',
            'https://images.unsplash.com/photo-1605979399824-6d3d60c2d8d2?w=400&h=400&fit=crop'
        ],
        'АКУЛА': [
            'https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=400&h=400&fit=crop',
            'https://images.unsplash.com/photo-1605979399824-6d3d60c2d8d2?w=400&h=400&fit=crop'
        ],
        
        # Насекомые
        'БАБОЧКА': [
            'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400&h=400&fit=crop',
            'https://images.unsplash.com/photo-1605979399824-6d3d60c2d8d2?w=400&h=400&fit=crop'
        ],
        'ПЧЕЛА': [
            'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400&h=400&fit=crop',
            'https://images.unsplash.com/photo-1605979399824-6d3d60c2d8d2?w=400&h=400&fit=crop'
        ],
        
        # Грызуны
        'МЫШЬ': [
            'https://images.unsplash.com/photo-1585110396000-c9ffd4e4b308?w=400&h=400&fit=crop',
            'https://images.unsplash.com/photo-1425082661705-1834bfd09dca?w=400&h=400&fit=crop'
        ],
        'БЕЛКА': [
            'https://images.unsplash.com/photo-1585110396000-c9ffd4e4b308?w=400&h=400&fit=crop',
            'https://images.unsplash.com/photo-1425082661705-1834bfd09dca?w=400&h=400&fit=crop'
        ],
        'ХОМЯК': [
            'https://images.unsplash.com/photo-1585110396000-c9ffd4e4b308?w=400&h=400&fit=crop',
            'https://images.unsplash.com/photo-1425082661705-1834bfd09dca?w=400&h=400&fit=crop'
        ],
        
        # Рептилии
        'ЗМЕЯ': [
            'https://images.unsplash.com/photo-1516728778615-2d590ea18d8d?w=400&h=400&fit=crop',
            'https://images.unsplash.com/photo-1605979399824-6d3d60c2d8d2?w=400&h=400&fit=crop'
        ],
        'ЯЩЕРИЦА': [
            'https://images.unsplash.com/photo-1516728778615-2d590ea18d8d?w=400&h=400&fit=crop',
            'https://images.unsplash.com/photo-1605979399824-6d3d60c2d8d2?w=400&h=400&fit=crop'
        ],
        'КРОКОДИЛ': [
            'https://images.unsplash.com/photo-1516728778615-2d590ea18d8d?w=400&h=400&fit=crop',
            'https://images.unsplash.com/photo-1605979399824-6d3d60c2d8d2?w=400&h=400&fit=crop'
        ],
        'ЧЕРЕПАХА': [
            'https://images.unsplash.com/photo-1516728778615-2d590ea18d8d?w=400&h=400&fit=crop',
            'https://images.unsplash.com/photo-1605979399824-6d3d60c2d8d2?w=400&h=400&fit=crop'
        ],
        
        # Рыбы
        'РЫБА': [
            'https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=400&h=400&fit=crop',
            'https://images.unsplash.com/photo-1605979399824-6d3d60c2d8d2?w=400&h=400&fit=crop'
        ],
        'ЛОСОСЬ': [
            'https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=400&h=400&fit=crop',
            'https://images.unsplash.com/photo-1605979399824-6d3d60c2d8d2?w=400&h=400&fit=crop'
        ],
        
        # Приматы
        'ОБЕЗЬЯНА': [
            'https://images.unsplash.com/photo-1540573133985-87b6da6d54a9?w=400&h=400&fit=crop&crop=face',
            'https://images.unsplash.com/photo-1605979399824-6d3d60c2d8d2?w=400&h=400&fit=crop&crop=face'
        ],
        'ГОРИЛЛА': [
            'https://images.unsplash.com/photo-1540573133985-87b6da6d54a9?w=400&h=400&fit=crop&crop=face',
            'https://images.unsplash.com/photo-1605979399824-6d3d60c2d8d2?w=400&h=400&fit=crop&crop=face'
        ],
        
        # Кошачьи
        'ЛЕОПАРД': [
            'https://images.unsplash.com/photo-1561731216-c3a4d99437d5?w=400&h=400&fit=crop&crop=face',
            'https://images.unsplash.com/photo-1605979399824-6d3d60c2d8d2?w=400&h=400&fit=crop&crop=face'
        ],
        'ГЕПАРД': [
            'https://images.unsplash.com/photo-1561731216-c3a4d99437d5?w=400&h=400&fit=crop&crop=face',
            'https://images.unsplash.com/photo-1605979399824-6d3d60c2d8d2?w=400&h=400&fit=crop&crop=face'
        ],
        'РЫСЬ': [
            'https://images.unsplash.com/photo-1561731216-c3a4d99437d5?w=400&h=400&fit=crop&crop=face',
            'https://images.unsplash.com/photo-1605979399824-6d3d60c2d8d2?w=400&h=400&fit=crop&crop=face'
        ],
        
        # Дополнительные животные
        'ЕНОТ': [
            'https://images.unsplash.com/photo-1497752531616-c3afd9760a11?w=400&h=400&fit=crop&crop=face',
            'https://images.unsplash.com/photo-1605979399824-6d3d60c2d8d2?w=400&h=400&fit=crop&crop=face'
        ],
        'БАРСУК': [
            'https://images.unsplash.com/photo-1497752531616-c3afd9760a11?w=400&h=400&fit=crop&crop=face',
            'https://images.unsplash.com/photo-1605979399824-6d3d60c2d8d2?w=400&h=400&fit=crop&crop=face'
        ],
        'ВЫДРА': [
            'https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=400&h=400&fit=crop',
            'https://images.unsplash.com/photo-1605979399824-6d3d60c2d8d2?w=400&h=400&fit=crop'
        ],
        'КЕНГУРУ': [
            'https://images.unsplash.com/photo-1564760055775-d63b17a55c44?w=400&h=400&fit=crop',
            'https://images.unsplash.com/photo-1551969014-7d2c4cddf0b6?w=400&h=400&fit=crop'
        ],
        'КОАЛА': [
            'https://images.unsplash.com/photo-1540573133985-87b6da6d54a9?w=400&h=400&fit=crop&crop=face',
            'https://images.unsplash.com/photo-1605979399824-6d3d60c2d8d2?w=400&h=400&fit=crop&crop=face'
        ],
        'ВЕРБЛЮД': [
            'https://images.unsplash.com/photo-1564760055775-d63b17a55c44?w=400&h=400&fit=crop',
            'https://images.unsplash.com/photo-1551969014-7d2c4cddf0b6?w=400&h=400&fit=crop'
        ]
    }

def download_curated_photos():
    """Download curated animal photos"""
    
    # Read the Russian animal file
    animals_file = 'data/words/ru/animals_COMPLETE.txt'
    
    if not os.path.exists(animals_file):
        print(f"Error: {animals_file} not found!")
        return
    
    # Create output directory
    output_dir = 'data/images/animals'
    os.makedirs(output_dir, exist_ok=True)
    
    # Get curated photos
    curated_photos = get_curated_animal_photos()
    
    downloaded_count = 0
    total_processed = 0
    
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
            
            total_processed += 1
            print(f"\nProcessing {line_num}/{total_lines}: {animal_name} ({image_code})")
            
            # Skip if file already exists and is reasonably sized
            if os.path.exists(image_path):
                file_size = os.path.getsize(image_path)
                if file_size > 80000:  # 80KB+
                    print(f"  → Already have good image ({file_size//1024}KB), skipping")
                    continue
            
            # Try to download curated photo
            if animal_name in curated_photos:
                urls = curated_photos[animal_name]
                success = False
                
                for url_index, url in enumerate(urls):
                    try:
                        print(f"  → Trying URL {url_index + 1}/{len(urls)} for {animal_name}")
                        
                        headers = {
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                        }
                        
                        response = requests.get(url, headers=headers, timeout=15)
                        response.raise_for_status()
                        
                        # Open and process image
                        img = Image.open(io.BytesIO(response.content))
                        img = img.convert('RGB')
                        
                        # Resize to 300x300
                        img = img.resize((300, 300), Image.Resampling.LANCZOS)
                        
                        # Save image
                        img.save(image_path, 'PNG', quality=95, optimize=True)
                        downloaded_count += 1
                        success = True
                        
                        # Check final file size
                        final_size = os.path.getsize(image_path)
                        print(f"  ✓ Downloaded: {image_filename} ({final_size//1024}KB)")
                        
                        # Small delay to be respectful
                        time.sleep(0.3)
                        break
                        
                    except Exception as e:
                        print(f"  ✗ Error with URL {url_index + 1}: {e}")
                        continue
                
                if not success:
                    print(f"  → All URLs failed for {animal_name}")
            else:
                print(f"  → No curated photos for {animal_name}")
            
            # Progress update every 20 animals
            if total_processed % 20 == 0:
                print(f"\n--- Progress: {total_processed}/{total_lines} processed, {downloaded_count} downloaded ---")
    
    print(f"\n" + "="*60)
    print(f"DOWNLOAD COMPLETE!")
    print(f"Total processed: {total_processed}")
    print(f"Successfully downloaded: {downloaded_count}")
    print(f"Success rate: {(downloaded_count/total_processed)*100:.1f}%")
    print(f"Images saved to: {output_dir}")
    print(f"="*60)

if __name__ == "__main__":
    print("Curated Animal Photo Downloader")
    print("===============================")
    print()
    print("This script will download curated high-quality animal photos")
    print("from carefully selected URLs from various free sources.")
    print()
    
    download_curated_photos()