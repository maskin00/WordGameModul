#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Scrape real animal photos from various websites
Downloads high-quality animal images from free sources
"""

import os
import requests
import time
from PIL import Image
import io
import random
from bs4 import BeautifulSoup
import urllib.parse

def get_animal_search_terms():
    """Get search terms for animals in English"""
    return {
        'КОШКА': ['cat', 'kitten', 'feline'],
        'СОБАКА': ['dog', 'puppy', 'canine'],
        'ЛОШАДЬ': ['horse', 'stallion', 'mare'],
        'КОРОВА': ['cow', 'cattle', 'bull'],
        'СВИНЬЯ': ['pig', 'swine', 'hog'],
        'ОВЦА': ['sheep', 'lamb', 'ewe'],
        'КОЗА': ['goat', 'kid'],
        'КРОЛИК': ['rabbit', 'bunny', 'hare'],
        'КУРИЦА': ['chicken', 'hen', 'rooster'],
        'УТКА': ['duck', 'mallard'],
        'ЛЕВ': ['lion', 'lioness'],
        'ТИГР': ['tiger', 'bengal tiger'],
        'СЛОН': ['elephant', 'african elephant'],
        'МЕДВЕДЬ': ['bear', 'brown bear'],
        'ВОЛК': ['wolf', 'grey wolf'],
        'ЛИСА': ['fox', 'red fox'],
        'ЗАЯЦ': ['hare', 'rabbit'],
        'ОЛЕНЬ': ['deer', 'stag'],
        'ЖИРАФ': ['giraffe'],
        'ЗЕБРА': ['zebra'],
        'НОСОРОГ': ['rhinoceros', 'rhino'],
        'БЕГЕМОТ': ['hippopotamus', 'hippo'],
        'ПАНДА': ['panda', 'giant panda'],
        'ОРЁЛ': ['eagle', 'bald eagle'],
        'СОВА': ['owl', 'barn owl'],
        'ПОПУГАЙ': ['parrot', 'macaw'],
        'ПИНГВИН': ['penguin', 'emperor penguin'],
        'ФЛАМИНГО': ['flamingo'],
        'КИТ': ['whale', 'blue whale'],
        'ДЕЛЬФИН': ['dolphin', 'bottlenose dolphin'],
        'АКУЛА': ['shark', 'great white shark'],
        'БАБОЧКА': ['butterfly', 'monarch butterfly'],
        'ПЧЕЛА': ['bee', 'honeybee'],
        'МЫШЬ': ['mouse', 'field mouse'],
        'БЕЛКА': ['squirrel', 'red squirrel'],
        'ХОМЯК': ['hamster', 'golden hamster'],
        'ЗМЕЯ': ['snake', 'python'],
        'ЯЩЕРИЦА': ['lizard', 'gecko'],
        'КРОКОДИЛ': ['crocodile', 'alligator'],
        'ЧЕРЕПАХА': ['turtle', 'sea turtle'],
        'ЛЯГУШКА': ['frog', 'tree frog'],
        'РЫБА': ['fish', 'tropical fish'],
        'ОБЕЗЬЯНА': ['monkey', 'chimpanzee'],
        'ГОРИЛЛА': ['gorilla', 'silverback gorilla'],
        'ЛЕОПАРД': ['leopard', 'snow leopard'],
        'ГЕПАРД': ['cheetah'],
        'РЫСЬ': ['lynx', 'bobcat'],
        'ЕНОТ': ['raccoon'],
        'БАРСУК': ['badger'],
        'ВЫДРА': ['otter', 'sea otter'],
        'КЕНГУРУ': ['kangaroo'],
        'КОАЛА': ['koala'],
        'ВЕРБЛЮД': ['camel', 'dromedary']
    }

def scrape_unsplash_photos(search_term, max_photos=3):
    """Scrape photos from Unsplash"""
    photos = []
    try:
        # Unsplash search URL
        search_url = f"https://unsplash.com/s/photos/{search_term.replace(' ', '-')}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(search_url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find image elements
        img_elements = soup.find_all('img', {'src': True})
        
        for img in img_elements[:max_photos]:
            src = img.get('src')
            if src and 'images.unsplash.com' in src and 'photo-' in src:
                # Convert to download URL
                if '?ixlib=' in src:
                    download_url = src.split('?')[0] + '?w=400&h=400&fit=crop&crop=face'
                    photos.append(download_url)
                    
        print(f"  Found {len(photos)} Unsplash photos for '{search_term}'")
        
    except Exception as e:
        print(f"  Error scraping Unsplash for '{search_term}': {e}")
    
    return photos

def scrape_pexels_photos(search_term, max_photos=3):
    """Scrape photos from Pexels"""
    photos = []
    try:
        # Pexels search URL
        search_url = f"https://www.pexels.com/search/{search_term.replace(' ', '%20')}/"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(search_url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find image elements
        img_elements = soup.find_all('img', {'src': True})
        
        for img in img_elements[:max_photos]:
            src = img.get('src')
            if src and 'images.pexels.com' in src and '/photos/' in src:
                # Convert to download URL
                if '?auto=' in src:
                    download_url = src.split('?')[0] + '?w=400&h=400&fit=crop'
                    photos.append(download_url)
                    
        print(f"  Found {len(photos)} Pexels photos for '{search_term}'")
        
    except Exception as e:
        print(f"  Error scraping Pexels for '{search_term}': {e}")
    
    return photos

def get_direct_animal_urls():
    """Get direct URLs to animal photos from various sources"""
    return {
        'КОШКА': [
            'https://cdn.pixabay.com/photo/2017/02/20/18/03/cat-2083492_960_720.jpg',
            'https://cdn.pixabay.com/photo/2014/11/30/14/11/cat-551554_960_720.jpg',
            'https://cdn.pixabay.com/photo/2016/12/13/05/15/puppy-1903313_960_720.jpg'
        ],
        'СОБАКА': [
            'https://cdn.pixabay.com/photo/2016/12/13/05/15/puppy-1903313_960_720.jpg',
            'https://cdn.pixabay.com/photo/2017/09/25/13/12/dog-2785074_960_720.jpg',
            'https://cdn.pixabay.com/photo/2016/02/19/15/46/dog-1210559_960_720.jpg'
        ],
        'ЛОШАДЬ': [
            'https://cdn.pixabay.com/photo/2019/07/26/04/58/horse-4363286_960_720.jpg',
            'https://cdn.pixabay.com/photo/2018/04/11/22/27/horses-3312071_960_720.jpg',
            'https://cdn.pixabay.com/photo/2017/05/25/18/59/horse-2343125_960_720.jpg'
        ],
        'КОРОВА': [
            'https://cdn.pixabay.com/photo/2016/10/11/21/43/cow-1732463_960_720.jpg',
            'https://cdn.pixabay.com/photo/2018/03/31/06/31/cow-3277434_960_720.jpg',
            'https://cdn.pixabay.com/photo/2017/06/09/16/39/cow-2386712_960_720.jpg'
        ],
        'ЛЕВ': [
            'https://cdn.pixabay.com/photo/2018/04/13/21/24/lion-3317670_960_720.jpg',
            'https://cdn.pixabay.com/photo/2017/10/04/11/58/lion-2817312_960_720.jpg',
            'https://cdn.pixabay.com/photo/2018/08/12/16/59/lion-3601194_960_720.jpg'
        ],
        'ТИГР': [
            'https://cdn.pixabay.com/photo/2017/07/24/19/57/tiger-2535888_960_720.jpg',
            'https://cdn.pixabay.com/photo/2018/03/29/04/02/tiger-3270935_960_720.jpg',
            'https://cdn.pixabay.com/photo/2016/11/14/04/14/tiger-1822537_960_720.jpg'
        ],
        'СЛОН': [
            'https://cdn.pixabay.com/photo/2016/11/14/04/59/elephant-1822636_960_720.jpg',
            'https://cdn.pixabay.com/photo/2017/01/20/00/30/maldives-1993704_960_720.jpg',
            'https://cdn.pixabay.com/photo/2018/09/03/23/56/elephant-3652889_960_720.jpg'
        ],
        'МЕДВЕДЬ': [
            'https://cdn.pixabay.com/photo/2017/07/24/19/57/bear-2535047_960_720.jpg',
            'https://cdn.pixabay.com/photo/2018/10/01/09/21/bear-3715123_960_720.jpg',
            'https://cdn.pixabay.com/photo/2016/12/13/21/20/bear-1905593_960_720.jpg'
        ],
        'ВОЛК': [
            'https://cdn.pixabay.com/photo/2017/08/06/15/13/wolf-2593407_960_720.jpg',
            'https://cdn.pixabay.com/photo/2018/05/16/21/34/wolf-3407354_960_720.jpg',
            'https://cdn.pixabay.com/photo/2017/02/15/12/12/wolf-2068875_960_720.jpg'
        ],
        'ЛИСА': [
            'https://cdn.pixabay.com/photo/2017/01/14/12/59/iceland-1979445_960_720.jpg',
            'https://cdn.pixabay.com/photo/2016/12/13/21/20/fox-1905593_960_720.jpg',
            'https://cdn.pixabay.com/photo/2018/05/16/21/34/fox-3407354_960_720.jpg'
        ],
        'ОРЁЛ': [
            'https://cdn.pixabay.com/photo/2018/05/22/20/48/eagle-3421220_960_720.jpg',
            'https://cdn.pixabay.com/photo/2017/02/07/16/47/kingfisher-2046453_960_720.jpg',
            'https://cdn.pixabay.com/photo/2018/08/12/16/59/eagle-3601194_960_720.jpg'
        ],
        'СОВА': [
            'https://cdn.pixabay.com/photo/2017/02/07/16/47/owl-2046453_960_720.jpg',
            'https://cdn.pixabay.com/photo/2018/05/22/20/48/owl-3421220_960_720.jpg',
            'https://cdn.pixabay.com/photo/2016/11/14/04/14/owl-1822537_960_720.jpg'
        ],
        'ПОПУГАЙ': [
            'https://cdn.pixabay.com/photo/2018/05/22/20/48/parrot-3421220_960_720.jpg',
            'https://cdn.pixabay.com/photo/2017/02/07/16/47/parrot-2046453_960_720.jpg',
            'https://cdn.pixabay.com/photo/2016/11/14/04/14/parrot-1822537_960_720.jpg'
        ]
    }

def download_scraped_photos():
    """Download animal photos using scraping and direct URLs"""
    
    # Read the Russian animal file
    animals_file = 'data/words/ru/animals_COMPLETE.txt'
    
    if not os.path.exists(animals_file):
        print(f"Error: {animals_file} not found!")
        return
    
    # Create output directory
    output_dir = 'data/images/animals'
    os.makedirs(output_dir, exist_ok=True)
    
    # Get search terms and direct URLs
    search_terms = get_animal_search_terms()
    direct_urls = get_direct_animal_urls()
    
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
                if file_size > 60000:  # 60KB+
                    print(f"  → Already have good image ({file_size//1024}KB), skipping")
                    continue
            
            # Try direct URLs first
            urls_to_try = []
            if animal_name in direct_urls:
                urls_to_try.extend(direct_urls[animal_name])
            
            # Try scraping if we have search terms
            if animal_name in search_terms:
                for search_term in search_terms[animal_name]:
                    # Try scraping Pixabay-style URLs
                    scraped_urls = scrape_unsplash_photos(search_term, 2)
                    urls_to_try.extend(scraped_urls)
                    
                    scraped_urls = scrape_pexels_photos(search_term, 2)
                    urls_to_try.extend(scraped_urls)
                    
                    if len(urls_to_try) >= 5:  # Limit to avoid too many requests
                        break
            
            # Try downloading from collected URLs
            success = False
            for url_index, url in enumerate(urls_to_try[:8]):  # Try max 8 URLs
                try:
                    print(f"  → Trying URL {url_index + 1}: {url[:60]}...")
                    
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
                    time.sleep(0.5)
                    break
                    
                except Exception as e:
                    print(f"  ✗ Error with URL {url_index + 1}: {e}")
                    continue
            
            if not success:
                print(f"  → Could not download photo for {animal_name}")
            
            # Progress update every 10 animals
            if total_processed % 10 == 0:
                print(f"\n--- Progress: {total_processed}/{total_lines} processed, {downloaded_count} downloaded ---")
    
    print(f"\n" + "="*60)
    print(f"SCRAPING DOWNLOAD COMPLETE!")
    print(f"Total processed: {total_processed}")
    print(f"Successfully downloaded: {downloaded_count}")
    print(f"Success rate: {(downloaded_count/total_processed)*100:.1f}%")
    print(f"Images saved to: {output_dir}")
    print(f"="*60)

if __name__ == "__main__":
    print("Animal Photo Scraper")
    print("===================")
    print()
    print("This script will scrape real animal photos from various websites")
    print("including Pixabay, Unsplash, and other free sources.")
    print()
    
    download_scraped_photos()