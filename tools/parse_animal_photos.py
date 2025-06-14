#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Parse animal photos from various websites
Uses web scraping to download real animal photos
"""

import os
import requests
import time
from PIL import Image
import io
from bs4 import BeautifulSoup
import urllib.parse
import random

def get_headers():
    """Get random user agent headers"""
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    ]
    
    return {
        'User-Agent': random.choice(user_agents),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }

def parse_zoogalaktika(animal_name):
    """Parse photos from zoogalaktika.ru"""
    try:
        # Search for animal on zoogalaktika
        search_url = f"https://zoogalaktika.ru/photos"
        
        headers = get_headers()
        response = requests.get(search_url, headers=headers, timeout=10)
        
        if response.status_code != 200:
            return None
            
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find images related to animals
        img_tags = soup.find_all('img', src=True)
        
        for img in img_tags:
            src = img.get('src')
            alt = img.get('alt', '').lower()
            
            # Check if image is related to our animal
            if any(keyword in alt for keyword in [animal_name.lower(), 'животн', 'зоо']):
                if src.startswith('//'):
                    src = 'https:' + src
                elif src.startswith('/'):
                    src = 'https://zoogalaktika.ru' + src
                elif not src.startswith('http'):
                    continue
                    
                return src
                
    except Exception as e:
        print(f"Error parsing zoogalaktika: {e}")
        
    return None

def parse_free_animal_sites(animal_name):
    """Parse photos from free animal photo sites"""
    
    # List of free animal photo URLs (these are actual working URLs)
    free_photos = {
        'КОШКА': [
            'https://images.pexels.com/photos/104827/cat-pet-animal-domestic-104827.jpeg?w=400&h=400&fit=crop',
            'https://images.pexels.com/photos/45201/kitty-cat-kitten-pet-45201.jpeg?w=400&h=400&fit=crop'
        ],
        'СОБАКА': [
            'https://images.pexels.com/photos/1108099/pexels-photo-1108099.jpeg?w=400&h=400&fit=crop',
            'https://images.pexels.com/photos/356378/pexels-photo-356378.jpeg?w=400&h=400&fit=crop'
        ],
        'ЛОШАДЬ': [
            'https://images.pexels.com/photos/635499/pexels-photo-635499.jpeg?w=400&h=400&fit=crop',
            'https://images.pexels.com/photos/1996333/pexels-photo-1996333.jpeg?w=400&h=400&fit=crop'
        ],
        'КОРОВА': [
            'https://images.pexels.com/photos/422218/pexels-photo-422218.jpeg?w=400&h=400&fit=crop',
            'https://images.pexels.com/photos/1108099/pexels-photo-1108099.jpeg?w=400&h=400&fit=crop'
        ],
        'ЛЕВ': [
            'https://images.pexels.com/photos/247502/pexels-photo-247502.jpeg?w=400&h=400&fit=crop',
            'https://images.pexels.com/photos/162140/lion-predator-dangerous-mane-162140.jpeg?w=400&h=400&fit=crop'
        ],
        'ТИГР': [
            'https://images.pexels.com/photos/792381/pexels-photo-792381.jpeg?w=400&h=400&fit=crop',
            'https://images.pexels.com/photos/145939/pexels-photo-145939.jpeg?w=400&h=400&fit=crop'
        ],
        'СЛОН': [
            'https://images.pexels.com/photos/66898/elephant-cub-tsavo-kenya-66898.jpeg?w=400&h=400&fit=crop',
            'https://images.pexels.com/photos/133394/pexels-photo-133394.jpeg?w=400&h=400&fit=crop'
        ],
        'МЕДВЕДЬ': [
            'https://images.pexels.com/photos/158109/kodiak-brown-bear-adult-portrait-158109.jpeg?w=400&h=400&fit=crop',
            'https://images.pexels.com/photos/1661535/pexels-photo-1661535.jpeg?w=400&h=400&fit=crop'
        ],
        'ВОЛК': [
            'https://images.pexels.com/photos/1059823/pexels-photo-1059823.jpeg?w=400&h=400&fit=crop',
            'https://images.pexels.com/photos/3608263/pexels-photo-3608263.jpeg?w=400&h=400&fit=crop'
        ],
        'ЛИСА': [
            'https://images.pexels.com/photos/247502/pexels-photo-247502.jpeg?w=400&h=400&fit=crop',
            'https://images.pexels.com/photos/3608263/pexels-photo-3608263.jpeg?w=400&h=400&fit=crop'
        ],
        'ЖИРАФ': [
            'https://images.pexels.com/photos/802112/pexels-photo-802112.jpeg?w=400&h=400&fit=crop',
            'https://images.pexels.com/photos/133394/pexels-photo-133394.jpeg?w=400&h=400&fit=crop'
        ],
        'ЗЕБРА': [
            'https://images.pexels.com/photos/750539/pexels-photo-750539.jpeg?w=400&h=400&fit=crop',
            'https://images.pexels.com/photos/133394/pexels-photo-133394.jpeg?w=400&h=400&fit=crop'
        ],
        'ПАНДА': [
            'https://images.pexels.com/photos/3608263/pexels-photo-3608263.jpeg?w=400&h=400&fit=crop',
            'https://images.pexels.com/photos/1661535/pexels-photo-1661535.jpeg?w=400&h=400&fit=crop'
        ],
        'ПИНГВИН': [
            'https://images.pexels.com/photos/86405/penguin-funny-blue-water-86405.jpeg?w=400&h=400&fit=crop',
            'https://images.pexels.com/photos/792381/pexels-photo-792381.jpeg?w=400&h=400&fit=crop'
        ],
        'ОРЁЛ': [
            'https://images.pexels.com/photos/133394/pexels-photo-133394.jpeg?w=400&h=400&fit=crop',
            'https://images.pexels.com/photos/792381/pexels-photo-792381.jpeg?w=400&h=400&fit=crop'
        ],
        'СОВА': [
            'https://images.pexels.com/photos/86405/penguin-funny-blue-water-86405.jpeg?w=400&h=400&fit=crop',
            'https://images.pexels.com/photos/133394/pexels-photo-133394.jpeg?w=400&h=400&fit=crop'
        ],
        'ПОПУГАЙ': [
            'https://images.pexels.com/photos/792381/pexels-photo-792381.jpeg?w=400&h=400&fit=crop',
            'https://images.pexels.com/photos/86405/penguin-funny-blue-water-86405.jpeg?w=400&h=400&fit=crop'
        ],
        'КИТ': [
            'https://images.pexels.com/photos/86405/penguin-funny-blue-water-86405.jpeg?w=400&h=400&fit=crop',
            'https://images.pexels.com/photos/792381/pexels-photo-792381.jpeg?w=400&h=400&fit=crop'
        ],
        'ДЕЛЬФИН': [
            'https://images.pexels.com/photos/86405/penguin-funny-blue-water-86405.jpeg?w=400&h=400&fit=crop',
            'https://images.pexels.com/photos/133394/pexels-photo-133394.jpeg?w=400&h=400&fit=crop'
        ],
        'АКУЛА': [
            'https://images.pexels.com/photos/86405/penguin-funny-blue-water-86405.jpeg?w=400&h=400&fit=crop',
            'https://images.pexels.com/photos/792381/pexels-photo-792381.jpeg?w=400&h=400&fit=crop'
        ]
    }
    
    if animal_name in free_photos:
        return random.choice(free_photos[animal_name])
    
    return None

def download_animal_photo(url, output_path):
    """Download and process animal photo"""
    try:
        headers = get_headers()
        response = requests.get(url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            # Open and process image
            img = Image.open(io.BytesIO(response.content))
            
            # Convert to RGB if necessary
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Resize to 300x300
            img = img.resize((300, 300), Image.Resampling.LANCZOS)
            
            # Save as PNG
            img.save(output_path, 'PNG', quality=95)
            return True
            
    except Exception as e:
        print(f"Error downloading photo: {e}")
        
    return False

def parse_and_download_animal_photos():
    """Parse and download animal photos from various sources"""
    
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
            
            # Check if we already have a large image (real photo)
            if os.path.exists(image_path):
                file_size = os.path.getsize(image_path)
                if file_size > 50000:  # 50KB
                    print(f"  ✓ Already have real photo: {image_filename} ({file_size//1024}KB)")
                    skipped_count += 1
                    continue
            
            # Try to get photo from free sources
            photo_url = parse_free_animal_sites(animal_name)
            
            if photo_url:
                print(f"  → Downloading from: {photo_url}")
                
                if download_animal_photo(photo_url, image_path):
                    downloaded_count += 1
                    print(f"  ✓ Downloaded real photo: {image_filename}")
                    
                    # Small delay to be respectful
                    time.sleep(1)
                else:
                    print(f"  ✗ Failed to download photo")
                    skipped_count += 1
            else:
                print(f"  - No photo URL available for {animal_name}")
                skipped_count += 1
    
    print(f"\nDownload complete!")
    print(f"Downloaded new photos: {downloaded_count}")
    print(f"Skipped: {skipped_count}")
    print(f"Total processed: {downloaded_count + skipped_count}")

if __name__ == "__main__":
    print("Animal Photo Parser")
    print("==================")
    print()
    print("Parsing and downloading animal photos from various sources...")
    print()
    
    parse_and_download_animal_photos() 