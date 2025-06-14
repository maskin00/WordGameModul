#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Download massive collection of real animal photos using Pixabay API and other sources
"""

import os
import requests
import time
from PIL import Image
import io
import json
import random

# Free Pixabay API key (demo key - replace with your own for production)
PIXABAY_API_KEY = "9656065-a4094594c34f9ac14c7fc4c39"

def search_pixabay_animal(animal_name_en, category="animals"):
    """Search for animal photos on Pixabay"""
    try:
        url = "https://pixabay.com/api/"
        params = {
            'key': PIXABAY_API_KEY,
            'q': animal_name_en,
            'category': category,
            'image_type': 'photo',
            'orientation': 'all',
            'min_width': 200,
            'min_height': 200,
            'safesearch': 'true',
            'per_page': 5,
            'order': 'popular'
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        if data['totalHits'] > 0:
            # Return the best quality URLs
            urls = []
            for hit in data['hits'][:3]:  # Take top 3 results
                if 'webformatURL' in hit:
                    urls.append(hit['webformatURL'])
                elif 'largeImageURL' in hit:
                    urls.append(hit['largeImageURL'])
            return urls
        
        return []
        
    except Exception as e:
        print(f"    Error searching Pixabay for {animal_name_en}: {e}")
        return []

def get_animal_translations():
    """Get English translations for Russian animal names"""
    translations = {
        'КОШКА': ['cat', 'kitten', 'domestic cat'],
        'СОБАКА': ['dog', 'puppy', 'domestic dog'],
        'ЛОШАДЬ': ['horse', 'stallion', 'mare'],
        'КОРОВА': ['cow', 'cattle', 'bull'],
        'СВИНЬЯ': ['pig', 'swine', 'piglet'],
        'ОВЦА': ['sheep', 'lamb', 'ewe'],
        'КОЗА': ['goat', 'kid goat', 'billy goat'],
        'КРОЛИК': ['rabbit', 'bunny', 'hare'],
        'ЛЕВ': ['lion', 'male lion', 'lioness'],
        'ТИГР': ['tiger', 'bengal tiger', 'siberian tiger'],
        'СЛОН': ['elephant', 'african elephant', 'asian elephant'],
        'МЕДВЕДЬ': ['bear', 'brown bear', 'polar bear'],
        'ВОЛК': ['wolf', 'grey wolf', 'timber wolf'],
        'ЛИСА': ['fox', 'red fox', 'arctic fox'],
        'ЗАЯЦ': ['hare', 'rabbit', 'cottontail'],
        'ОЛЕНЬ': ['deer', 'stag', 'doe'],
        'ЖИРАФ': ['giraffe', 'tall giraffe', 'african giraffe'],
        'ЗЕБРА': ['zebra', 'plains zebra', 'striped zebra'],
        'НОСОРОГ': ['rhinoceros', 'rhino', 'black rhino'],
        'БЕГЕМОТ': ['hippopotamus', 'hippo', 'river horse'],
        'ПАНДА': ['panda', 'giant panda', 'red panda'],
        'ОРЁЛ': ['eagle', 'bald eagle', 'golden eagle'],
        'СОВА': ['owl', 'barn owl', 'great horned owl'],
        'ПОПУГАЙ': ['parrot', 'macaw', 'cockatoo'],
        'ПИНГВИН': ['penguin', 'emperor penguin', 'adelie penguin'],
        'ФЛАМИНГО': ['flamingo', 'pink flamingo', 'greater flamingo'],
        'КИТ': ['whale', 'blue whale', 'humpback whale'],
        'ДЕЛЬФИН': ['dolphin', 'bottlenose dolphin', 'common dolphin'],
        'АКУЛА': ['shark', 'great white shark', 'tiger shark'],
        'БАБОЧКА': ['butterfly', 'monarch butterfly', 'swallowtail'],
        'ПЧЕЛА': ['bee', 'honey bee', 'bumblebee'],
        'МЫШЬ': ['mouse', 'field mouse', 'house mouse'],
        'БЕЛКА': ['squirrel', 'red squirrel', 'grey squirrel'],
        'ХОМЯК': ['hamster', 'golden hamster', 'dwarf hamster'],
        'ЗМЕЯ': ['snake', 'python', 'cobra'],
        'ЯЩЕРИЦА': ['lizard', 'gecko', 'iguana'],
        'КРОКОДИЛ': ['crocodile', 'alligator', 'caiman'],
        'ЧЕРЕПАХА': ['turtle', 'tortoise', 'sea turtle'],
        'РЫБА': ['fish', 'tropical fish', 'goldfish'],
        'ЛОСОСЬ': ['salmon', 'atlantic salmon', 'pink salmon'],
        'ОБЕЗЬЯНА': ['monkey', 'chimpanzee', 'macaque'],
        'ГОРИЛЛА': ['gorilla', 'mountain gorilla', 'silverback'],
        'ЛЕОПАРД': ['leopard', 'snow leopard', 'clouded leopard'],
        'ГЕПАРД': ['cheetah', 'running cheetah', 'spotted cheetah'],
        'РЫСЬ': ['lynx', 'bobcat', 'eurasian lynx'],
        'ЕНОТ': ['raccoon', 'common raccoon', 'masked bandit'],
        'БАРСУК': ['badger', 'honey badger', 'european badger'],
        'ВЫДРА': ['otter', 'sea otter', 'river otter'],
        'ТЮЛЕНЬ': ['seal', 'harbor seal', 'grey seal'],
        'МОРЖ': ['walrus', 'pacific walrus', 'atlantic walrus'],
        'КЕНГУРУ': ['kangaroo', 'red kangaroo', 'grey kangaroo'],
        'КОАЛА': ['koala', 'koala bear', 'eucalyptus koala'],
        'ВЕРБЛЮД': ['camel', 'dromedary', 'bactrian camel'],
        'ЛАМА': ['llama', 'alpaca', 'vicuna'],
        'АНТИЛОПА': ['antelope', 'gazelle', 'impala'],
        'БУЙВОЛ': ['buffalo', 'water buffalo', 'cape buffalo'],
        'БИЗОН': ['bison', 'american bison', 'european bison'],
        'ЯК': ['yak', 'tibetan yak', 'wild yak'],
        'КАБАН': ['wild boar', 'boar', 'feral pig'],
        'ЛОСЬ': ['moose', 'elk', 'eurasian elk'],
        'КОСУЛЯ': ['roe deer', 'european roe deer', 'siberian roe deer'],
        'СОБОЛЬ': ['sable', 'russian sable', 'american marten'],
        'КУНИЦА': ['marten', 'pine marten', 'stone marten'],
        'ХОРЁК': ['ferret', 'polecat', 'domestic ferret'],
        'ЛАСКА': ['weasel', 'least weasel', 'stoat'],
        'ГОРНОСТАЙ': ['ermine', 'stoat', 'short-tailed weasel'],
        'НОРКА': ['mink', 'american mink', 'european mink'],
        'БОБР': ['beaver', 'north american beaver', 'eurasian beaver'],
        'ДИКОБРАЗ': ['porcupine', 'north american porcupine', 'crested porcupine'],
        'СУРОК': ['marmot', 'groundhog', 'alpine marmot'],
        'СУСЛИК': ['ground squirrel', 'arctic ground squirrel', 'richardson ground squirrel'],
        'ХОМЯК': ['hamster', 'golden hamster', 'european hamster'],
        'ПЕСЕЦ': ['arctic fox', 'white fox', 'polar fox'],
        'ФЕНЕК': ['fennec fox', 'desert fox', 'fennec'],
        'ШАКАЛ': ['jackal', 'golden jackal', 'black-backed jackal'],
        'ГИЕНА': ['hyena', 'spotted hyena', 'striped hyena'],
        'ПУМА': ['puma', 'mountain lion', 'cougar'],
        'ЯГУАР': ['jaguar', 'panthera onca', 'spotted jaguar'],
        'ОЦЕЛОТ': ['ocelot', 'dwarf leopard', 'painted leopard'],
        'СЕРВАЛ': ['serval', 'african serval', 'leptailurus serval'],
        'КАРАКАЛ': ['caracal', 'desert lynx', 'persian lynx'],
        'МАНУЛ': ['pallas cat', 'manul', 'steppe cat'],
        'ДИКАЯ КОШКА': ['wildcat', 'european wildcat', 'african wildcat'],
        'ПЕСЧАНАЯ КОШКА': ['sand cat', 'sand dune cat', 'felis margarita'],
        'ЧЕРНОНОГАЯ КОШКА': ['black-footed cat', 'small-spotted cat', 'felis nigripes']
    }
    return translations

def download_animal_photos():
    """Download real animal photos using multiple sources"""
    
    # Read the Russian animal file
    animals_file = 'data/words/ru/animals_COMPLETE.txt'
    
    if not os.path.exists(animals_file):
        print(f"Error: {animals_file} not found!")
        return
    
    # Create output directory
    output_dir = 'data/images/animals'
    os.makedirs(output_dir, exist_ok=True)
    
    # Get translations
    translations = get_animal_translations()
    
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
                if file_size > 50000:  # 50KB+
                    print(f"  → Already have good image ({file_size//1024}KB), skipping")
                    continue
            
            # Try to get English translations
            if animal_name in translations:
                english_names = translations[animal_name]
                success = False
                
                for english_name in english_names:
                    if success:
                        break
                        
                    print(f"  → Searching for '{english_name}'...")
                    
                    # Try Pixabay API
                    urls = search_pixabay_animal(english_name)
                    
                    for url_index, url in enumerate(urls):
                        try:
                            print(f"    → Trying URL {url_index + 1}/{len(urls)}")
                            
                            headers = {
                                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                            }
                            
                            response = requests.get(url, headers=headers, timeout=15)
                            response.raise_for_status()
                            
                            # Open and process image
                            img = Image.open(io.BytesIO(response.content))
                            img = img.convert('RGB')
                            
                            # Resize to 300x300 maintaining aspect ratio
                            img.thumbnail((300, 300), Image.Resampling.LANCZOS)
                            
                            # Create a 300x300 canvas and center the image
                            canvas = Image.new('RGB', (300, 300), (255, 255, 255))
                            x = (300 - img.width) // 2
                            y = (300 - img.height) // 2
                            canvas.paste(img, (x, y))
                            
                            # Save image
                            canvas.save(image_path, 'PNG', quality=95, optimize=True)
                            downloaded_count += 1
                            success = True
                            
                            # Check final file size
                            final_size = os.path.getsize(image_path)
                            print(f"    ✓ Downloaded: {image_filename} ({final_size//1024}KB)")
                            
                            # Small delay to be respectful
                            time.sleep(0.5)
                            break
                            
                        except Exception as e:
                            print(f"    ✗ Error: {e}")
                            continue
                    
                    if success:
                        break
                    
                    # Small delay between searches
                    time.sleep(0.3)
                
                if not success:
                    print(f"  → Could not find photo for {animal_name}")
            else:
                print(f"  → No English translation for {animal_name}")
            
            # Progress update every 10 animals
            if total_processed % 10 == 0:
                print(f"\n--- Progress: {total_processed}/{total_lines} processed, {downloaded_count} downloaded ---")
    
    print(f"\n" + "="*60)
    print(f"DOWNLOAD COMPLETE!")
    print(f"Total processed: {total_processed}")
    print(f"Successfully downloaded: {downloaded_count}")
    print(f"Success rate: {(downloaded_count/total_processed)*100:.1f}%")
    print(f"Images saved to: {output_dir}")
    print(f"="*60)

if __name__ == "__main__":
    print("Pixabay Animal Photo Downloader")
    print("===============================")
    print()
    print("This script will download real animal photos using:")
    print("• Pixabay API (free tier)")
    print("• Multiple English search terms per animal")
    print("• High-quality photo selection")
    print()
    
    download_animal_photos()