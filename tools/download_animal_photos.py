#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script to download high-quality animal photos for the word game
Uses free APIs from Unsplash and Pixabay to get realistic animal images
"""

import os
import requests
import time
from PIL import Image
import io

# Free API keys (you can get these for free)
UNSPLASH_ACCESS_KEY = "YOUR_UNSPLASH_ACCESS_KEY"  # Get from https://unsplash.com/developers
PIXABAY_API_KEY = "YOUR_PIXABAY_API_KEY"  # Get from https://pixabay.com/api/docs/

# Animal search terms in English (for API queries)
animal_search_terms = {
    "КОШКА": "cat",
    "СОБАКА": "dog", 
    "ЛОШАДЬ": "horse",
    "КОРОВА": "cow",
    "СВИНЬЯ": "pig",
    "ОВЦА": "sheep",
    "КОЗА": "goat",
    "КРОЛИК": "rabbit",
    "КУРИЦА": "chicken",
    "УТКА": "duck",
    "ЛЕВ": "lion",
    "ТИГР": "tiger",
    "СЛОН": "elephant",
    "МЕДВЕДЬ": "bear",
    "ВОЛК": "wolf",
    "ЛИСА": "fox",
    "ЗАЯЦ": "hare",
    "ОЛЕНЬ": "deer",
    "ЛОСЬ": "moose",
    "КАБАН": "wild boar",
    "ОБЕЗЬЯНА": "monkey",
    "ГОРИЛЛА": "gorilla",
    "ШИМПАНЗЕ": "chimpanzee",
    "ОРАНГУТАН": "orangutan",
    "ЛЕМУР": "lemur",
    "ЛЕОПАРД": "leopard",
    "ГЕПАРД": "cheetah",
    "РЫСЬ": "lynx",
    "ПУМА": "puma",
    "ЯГУАР": "jaguar",
    "КИТ": "whale",
    "ДЕЛЬФИН": "dolphin",
    "АКУЛА": "shark",
    "ТЮЛЕНЬ": "seal",
    "МОРЖ": "walrus",
    "ОСЬМИНОГ": "octopus",
    "КРАБ": "crab",
    "ЛОБСТЕР": "lobster",
    "КРЕВЕТКА": "shrimp",
    "МЕДУЗА": "jellyfish",
    "ОРЁЛ": "eagle",
    "СОВА": "owl",
    "ПОПУГАЙ": "parrot",
    "ПИНГВИН": "penguin",
    "ФЛАМИНГО": "flamingo",
    "ПАВЛИН": "peacock",
    "ЛЕБЕДЬ": "swan",
    "АИСТ": "stork",
    "ВОРОН": "raven",
    "ВОРОБЕЙ": "sparrow",
    "ЗМЕЯ": "snake",
    "ЯЩЕРИЦА": "lizard",
    "КРОКОДИЛ": "crocodile",
    "ЧЕРЕПАХА": "turtle",
    "ИГУАНА": "iguana",
    "ХАМЕЛЕОН": "chameleon",
    "ГЕККОН": "gecko",
    "ВАРАН": "monitor lizard",
    "ПИТОН": "python snake",
    "КОБРА": "cobra snake",
    "ЛЯГУШКА": "frog",
    "ЖАБА": "toad",
    "САЛАМАНДРА": "salamander",
    "ТРИТОН": "newt",
    "АКСОЛОТЛЬ": "axolotl",
    "РЫБА": "fish",
    "ЛОСОСЬ": "salmon",
    "ТУНЕЦ": "tuna",
    "ФОРЕЛЬ": "trout",
    "КАРП": "carp",
    "ЩУКА": "pike fish",
    "ОКУНЬ": "perch fish",
    "СОМ": "catfish",
    "УГОРЬ": "eel",
    "СКАТ": "stingray",
    "БАБОЧКА": "butterfly",
    "ПЧЕЛА": "bee",
    "МУРАВЕЙ": "ant",
    "ЖУК": "beetle",
    "МУХА": "fly insect",
    "КОМАР": "mosquito",
    "СТРЕКОЗА": "dragonfly",
    "КУЗНЕЧИК": "grasshopper",
    "СВЕРЧОК": "cricket insect",
    "БОЖЬЯ КОРОВКА": "ladybug",
    "ПАУК": "spider",
    "СКОРПИОН": "scorpion",
    "КЛЕЩ": "tick",
    "ТАРАНТУЛ": "tarantula",
    "МЫШЬ": "mouse",
    "КРЫСА": "rat",
    "БЕЛКА": "squirrel",
    "ХОМЯК": "hamster",
    "БОБР": "beaver",
    "ДИКОБРАЗ": "porcupine",
    "СУРОК": "marmot",
    "ШИНШИЛЛА": "chinchilla",
    "КАПИБАРА": "capybara",
    "КЕНГУРУ": "kangaroo",
    "КОАЛА": "koala",
    "ОПОССУМ": "opossum",
    "ТАСМАНСКИЙ ДЬЯВОЛ": "tasmanian devil",
    "ВОМБАТ": "wombat",
    "ЖИРАФ": "giraffe",
    "ЗЕБРА": "zebra",
    "НОСОРОГ": "rhinoceros",
    "БЕГЕМОТ": "hippopotamus",
    "АНТИЛОПА": "antelope",
    "ГАЗЕЛЬ": "gazelle",
    "ГИЕНА": "hyena",
    "СУРИКАТ": "meerkat",
    "БАБУИН": "baboon",
    "МАНДРИЛ": "mandrill",
    "БЕЛЫЙ МЕДВЕДЬ": "polar bear",
    "ПЕСЕЦ": "arctic fox",
    "СЕВЕРНЫЙ ОЛЕНЬ": "reindeer",
    "ОВЦЕБЫК": "musk ox",
    "ЛАМА": "llama",
    "АЛЬПАКА": "alpaca",
    "ВИКУНЬЯ": "vicuna",
    "ЛЕНИВЕЦ": "sloth",
    "МУРАВЬЕД": "anteater",
    "БРОНЕНОСЕЦ": "armadillo",
    "ТУКАН": "toucan",
    "КОЛИБРИ": "hummingbird",
    "ЯГУАРУНДИ": "jaguarundi",
    "ОЦЕЛОТ": "ocelot",
    "УТКОНОС": "platypus",
    "ЕХИДНА": "echidna",
    "ВАЛЛАБИ": "wallaby",
    "ДИНГО": "dingo",
    "КУКАБАРРА": "kookaburra",
    "ПАНДА": "panda",
    "ЯК": "yak",
    "СНЕЖНЫЙ БАРС": "snow leopard",
    "МАЛАЙСКИЙ МЕДВЕДЬ": "sun bear",
    "БИНТУРОНГ": "binturong",
    "МОРСКАЯ СВИНКА": "guinea pig",
    "ХОРЁК": "ferret",
    "ПОПУГАЙЧИК": "parakeet",
    "КАНАРЕЙКА": "canary",
    "ЛЕТУЧАЯ МЫШЬ": "bat",
    "ЁЖ": "hedgehog",
    "ЕНОТ": "raccoon",
    "СКУНС": "skunk",
    "БАРСУК": "badger",
    "ВЫДРА": "otter",
    "ЛАМАНТИН": "manatee",
    "ДЮГОНЬ": "dugong",
    "НАРВАЛ": "narwhal",
    "ЯСТРЕБ": "hawk",
    "СОКОЛ": "falcon",
    "КОРШУН": "kite bird",
    "ГРИФ": "vulture",
    "КОНДОР": "condor",
    "ЗЕМЛЕРОЙКА": "shrew",
    "КРОТ": "mole",
    "ЛАСКА": "weasel",
    "ГОРНОСТАЙ": "ermine",
    "КУНИЦА": "marten",
    "ЗУБР": "bison",
    "БУЙВОЛ": "buffalo",
    "ВЕРБЛЮД": "camel",
    "ДРОМАДЕР": "dromedary",
    "ТАПИР": "tapir",
    "ОКАПИ": "okapi",
    "КВАГГА": "quagga",
    "ФОССА": "fossa",
    "ТЕНРЕК": "tenrec",
    "АЙ-АЙ": "aye-aye",
    "СТРАУС": "ostrich",
    "ЭМУ": "emu",
    "КАЗУАР": "cassowary",
    "КИВИ": "kiwi bird",
    "АЛЬБАТРОС": "albatross",
    "МОРСКОЙ КОНЁК": "seahorse",
    "МОРСКАЯ ЗВЕЗДА": "starfish",
    "МОРСКОЙ ЁЖ": "sea urchin",
    "АНЕМОН": "sea anemone",
    "КОРАЛЛ": "coral",
    "ОСА": "wasp",
    "ШМЕЛЬ": "bumblebee",
    "ШЕРШЕНЬ": "hornet",
    "БОГОМОЛ": "praying mantis",
    "ПАЛОЧНИК": "stick insect",
    "АНАКОНДА": "anaconda",
    "УДАВ": "boa constrictor",
    "ГАДЮКА": "viper",
    "УЖ": "grass snake",
    "АГАМА": "agama",
    "КВАКША": "tree frog",
    "ЧЕСНОЧНИЦА": "spadefoot toad",
    "ПРОТЕЙ": "olm",
    "СИРЕН": "siren salamander",
    "БАРРАКУДА": "barracuda",
    "МУРЕНА": "moray eel",
    "РЫБА-МЕЧ": "swordfish",
    "РЫБА-МОЛОТ": "hammerhead shark",
    "РЫБА-КЛОУН": "clownfish",
    "РОСОМАХА": "wolverine",
    "СЕРВАЛ": "serval",
    "КАРАКАЛ": "caracal",
    "МАНУЛ": "pallas cat"
}

def download_from_pixabay(search_term, filename, size=(300, 300)):
    """Download image from Pixabay API"""
    if PIXABAY_API_KEY == "YOUR_PIXABAY_API_KEY":
        print("Please set your Pixabay API key")
        return False
    
    url = "https://pixabay.com/api/"
    params = {
        'key': PIXABAY_API_KEY,
        'q': search_term,
        'image_type': 'photo',
        'category': 'animals',
        'min_width': 200,
        'min_height': 200,
        'safesearch': 'true',
        'per_page': 5
    }
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        if data['hits']:
            # Get the first image
            image_url = data['hits'][0]['webformatURL']
            
            # Download the image
            img_response = requests.get(image_url)
            img = Image.open(io.BytesIO(img_response.content))
            
            # Resize to target size
            img = img.resize(size, Image.Resampling.LANCZOS)
            
            # Save as PNG
            img.save(filename, 'PNG')
            return True
            
    except Exception as e:
        print(f"Error downloading from Pixabay for {search_term}: {e}")
    
    return False

def download_from_unsplash(search_term, filename, size=(300, 300)):
    """Download image from Unsplash API"""
    if UNSPLASH_ACCESS_KEY == "YOUR_UNSPLASH_ACCESS_KEY":
        print("Please set your Unsplash access key")
        return False
    
    url = "https://api.unsplash.com/search/photos"
    headers = {
        'Authorization': f'Client-ID {UNSPLASH_ACCESS_KEY}'
    }
    params = {
        'query': search_term,
        'per_page': 5,
        'orientation': 'squarish'
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        
        if data['results']:
            # Get the first image
            image_url = data['results'][0]['urls']['regular']
            
            # Download the image
            img_response = requests.get(image_url)
            img = Image.open(io.BytesIO(img_response.content))
            
            # Resize to target size
            img = img.resize(size, Image.Resampling.LANCZOS)
            
            # Save as PNG
            img.save(filename, 'PNG')
            return True
            
    except Exception as e:
        print(f"Error downloading from Unsplash for {search_term}: {e}")
    
    return False

def create_fallback_image(animal_name, filename, size=(300, 300)):
    """Create a fallback image with colored background and text"""
    from PIL import ImageDraw, ImageFont
    
    colors = [
        (70, 130, 180),   # Steel Blue
        (60, 179, 113),   # Medium Sea Green
        (255, 140, 0),    # Dark Orange
        (220, 20, 60),    # Crimson
        (138, 43, 226),   # Blue Violet
        (255, 215, 0),    # Gold
        (50, 205, 50),    # Lime Green
        (255, 69, 0),     # Red Orange
    ]
    
    # Choose color based on animal name hash
    color = colors[hash(animal_name) % len(colors)]
    
    # Create image
    img = Image.new('RGB', size, color)
    draw = ImageDraw.Draw(img)
    
    # Add animal name
    try:
        font = ImageFont.truetype("arial.ttf", 24)
    except:
        font = ImageFont.load_default()
    
    # Get text size and center it
    bbox = draw.textbbox((0, 0), animal_name, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = (size[0] - text_width) // 2
    y = (size[1] - text_height) // 2
    
    # Draw text with shadow
    draw.text((x+2, y+2), animal_name, font=font, fill=(0, 0, 0, 128))  # Shadow
    draw.text((x, y), animal_name, font=font, fill=(255, 255, 255, 255))  # Text
    
    img.save(filename, 'PNG')

def download_animal_photos():
    """Download photos for all animals"""
    
    # Read the Russian animal file to get the list
    animals_file = 'data/words/ru/animals_COMPLETE.txt'
    
    if not os.path.exists(animals_file):
        print(f"Error: {animals_file} not found!")
        return
    
    # Create output directory
    output_dir = 'data/images/animals'
    os.makedirs(output_dir, exist_ok=True)
    
    downloaded_count = 0
    fallback_count = 0
    
    with open(animals_file, 'r', encoding='utf-8') as f:
        for line in f:
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
            
            # Skip if image already exists and is not the emoji version
            if os.path.exists(image_path):
                # Check if it's a small emoji image (less than 10KB)
                if os.path.getsize(image_path) > 10000:  # 10KB
                    print(f"Skipping {image_filename} (already exists)")
                    continue
            
            print(f"Downloading image for {animal_name}...")
            
            # Get search term
            search_term = animal_search_terms.get(animal_name, animal_name.lower())
            
            # Try to download from APIs
            success = False
            
            # Try Pixabay first
            if download_from_pixabay(search_term, image_path):
                success = True
                downloaded_count += 1
                print(f"✓ Downloaded from Pixabay: {image_filename}")
            
            # If Pixabay failed, try Unsplash
            elif download_from_unsplash(search_term, image_path):
                success = True
                downloaded_count += 1
                print(f"✓ Downloaded from Unsplash: {image_filename}")
            
            # If both failed, create fallback
            if not success:
                create_fallback_image(animal_name, image_path)
                fallback_count += 1
                print(f"⚠ Created fallback image: {image_filename}")
            
            # Rate limiting - wait between requests
            time.sleep(1)
    
    print(f"\nDownload complete!")
    print(f"Downloaded from APIs: {downloaded_count}")
    print(f"Created fallback images: {fallback_count}")
    print(f"Total images: {downloaded_count + fallback_count}")

if __name__ == "__main__":
    print("Animal Photo Downloader")
    print("======================")
    print()
    print("To use this script with real photos, you need free API keys:")
    print("1. Pixabay: https://pixabay.com/api/docs/")
    print("2. Unsplash: https://unsplash.com/developers")
    print()
    print("For now, creating improved fallback images...")
    print()
    
    # For demonstration, we'll create improved fallback images
    # Users can add their API keys to get real photos
    download_animal_photos()