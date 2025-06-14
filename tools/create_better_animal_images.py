#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script to create better animal images for the word game
Downloads real photos from free sources and creates attractive fallback images
"""

import os
import requests
import time
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import io
import random

def download_from_free_sources(animal_name, filename, size=(300, 300)):
    """Download animal images from various free sources"""
    
    # List of free image sources with animal photos
    sources = [
        # Unsplash (free to use)
        f"https://source.unsplash.com/300x300/?{animal_name.lower()}",
        f"https://source.unsplash.com/300x300/?{animal_name.lower()},animal",
        f"https://source.unsplash.com/300x300/?wild,{animal_name.lower()}",
        
        # Picsum with animal keywords (fallback)
        "https://picsum.photos/300/300",
    ]
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    for source_url in sources:
        try:
            print(f"  Trying: {source_url}")
            response = requests.get(source_url, headers=headers, timeout=15, allow_redirects=True)
            
            if response.status_code == 200:
                # Check if it's actually an image
                img = Image.open(io.BytesIO(response.content))
                
                # Convert to RGB if necessary
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Resize to target size
                img = img.resize(size, Image.Resampling.LANCZOS)
                
                # Save as PNG
                img.save(filename, 'PNG', quality=95)
                return True
                
        except Exception as e:
            print(f"    Failed: {e}")
            continue
    
    return False

def create_artistic_image(animal_name, filename, size=(300, 300)):
    """Create an artistic image with better design"""
    
    # Animal-themed color palettes
    color_palettes = {
        # Mammals
        'КОШКА': [(255, 218, 185), (255, 160, 122), (205, 92, 92)],  # Peach/salmon
        'СОБАКА': [(135, 206, 235), (100, 149, 237), (65, 105, 225)],  # Sky blue
        'ЛОШАДЬ': [(222, 184, 135), (205, 133, 63), (160, 82, 45)],   # Brown/tan
        'КОРОВА': [(255, 255, 255), (220, 220, 220), (169, 169, 169)], # White/gray
        'ЛЕВ': [(255, 215, 0), (255, 165, 0), (255, 140, 0)],         # Gold
        'ТИГР': [(255, 140, 0), (255, 69, 0), (220, 20, 60)],         # Orange/red
        'СЛОН': [(169, 169, 169), (128, 128, 128), (105, 105, 105)],  # Gray
        'МЕДВЕДЬ': [(139, 69, 19), (160, 82, 45), (210, 180, 140)],   # Brown
        'ВОЛК': [(105, 105, 105), (128, 128, 128), (169, 169, 169)],  # Gray
        'ЛИСА': [(255, 140, 0), (255, 69, 0), (178, 34, 34)],         # Orange/red
        
        # Birds
        'ОРЁЛ': [(139, 69, 19), (160, 82, 45), (205, 133, 63)],       # Brown
        'ПОПУГАЙ': [(50, 205, 50), (34, 139, 34), (0, 128, 0)],       # Green
        'ПИНГВИН': [(0, 0, 0), (105, 105, 105), (255, 255, 255)],     # Black/white
        'ФЛАМИНГО': [(255, 182, 193), (255, 105, 180), (255, 20, 147)], # Pink
        'ПАВЛИН': [(0, 191, 255), (30, 144, 255), (0, 0, 255)],       # Blue
        
        # Sea animals
        'КИТ': [(70, 130, 180), (100, 149, 237), (135, 206, 235)],    # Blue
        'ДЕЛЬФИН': [(135, 206, 250), (176, 196, 222), (173, 216, 230)], # Light blue
        'АКУЛА': [(105, 105, 105), (128, 128, 128), (169, 169, 169)], # Gray
        
        # Insects
        'БАБОЧКА': [(255, 182, 193), (255, 160, 122), (255, 218, 185)], # Colorful
        'ПЧЕЛА': [(255, 215, 0), (255, 165, 0), (0, 0, 0)],           # Yellow/black
        
        # Default
        'DEFAULT': [(144, 238, 144), (60, 179, 113), (34, 139, 34)]    # Green
    }
    
    # Get color palette
    colors = color_palettes.get(animal_name, color_palettes['DEFAULT'])
    
    # Create base image with gradient
    img = Image.new('RGB', size, colors[0])
    draw = ImageDraw.Draw(img)
    
    # Create radial gradient from center
    center_x, center_y = size[0] // 2, size[1] // 2
    max_radius = min(size) // 2
    
    for radius in range(max_radius, 0, -2):
        ratio = radius / max_radius
        r = int(colors[0][0] * ratio + colors[1][0] * (1 - ratio))
        g = int(colors[0][1] * ratio + colors[1][1] * (1 - ratio))
        b = int(colors[0][2] * ratio + colors[1][2] * (1 - ratio))
        
        draw.ellipse([
            center_x - radius, center_y - radius,
            center_x + radius, center_y + radius
        ], fill=(r, g, b))
    
    # Add decorative elements
    # Draw some circles for decoration
    for i in range(3):
        circle_size = random.randint(20, 40)
        x = random.randint(circle_size, size[0] - circle_size)
        y = random.randint(circle_size, size[1] - circle_size)
        
        # Semi-transparent circle
        circle_color = colors[2] if len(colors) > 2 else colors[1]
        alpha = 50
        overlay = Image.new('RGBA', size, (0, 0, 0, 0))
        overlay_draw = ImageDraw.Draw(overlay)
        overlay_draw.ellipse([
            x - circle_size, y - circle_size,
            x + circle_size, y + circle_size
        ], fill=(*circle_color, alpha))
        
        img = Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB')
    
    # Add animal name with better typography
    draw = ImageDraw.Draw(img)
    
    try:
        # Try different fonts
        font_paths = [
            "C:/Windows/Fonts/arial.ttf",
            "C:/Windows/Fonts/calibri.ttf",
            "C:/Windows/Fonts/segoeui.ttf",
        ]
        
        font = None
        for font_path in font_paths:
            try:
                font = ImageFont.truetype(font_path, 28)
                break
            except:
                continue
        
        if font is None:
            font = ImageFont.load_default()
            
    except:
        font = ImageFont.load_default()
    
    # Get text size and center it
    bbox = draw.textbbox((0, 0), animal_name, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = (size[0] - text_width) // 2
    y = (size[1] - text_height) // 2
    
    # Create text background
    padding = 10
    bg_rect = [
        x - padding, y - padding,
        x + text_width + padding, y + text_height + padding
    ]
    
    # Semi-transparent background
    overlay = Image.new('RGBA', size, (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)
    overlay_draw.rounded_rectangle(bg_rect, radius=10, fill=(0, 0, 0, 120))
    
    img = Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB')
    draw = ImageDraw.Draw(img)
    
    # Draw text with shadow
    shadow_offset = 2
    draw.text((x + shadow_offset, y + shadow_offset), animal_name, 
             font=font, fill=(0, 0, 0, 180))  # Shadow
    draw.text((x, y), animal_name, font=font, fill=(255, 255, 255))  # Main text
    
    # Add border
    border_width = 3
    draw.rectangle([
        border_width, border_width,
        size[0] - border_width, size[1] - border_width
    ], outline=colors[1], width=border_width)
    
    img.save(filename, 'PNG')

def get_english_animal_names():
    """Get English translations for animal names for better search results"""
    translations = {
        'КОШКА': 'cat',
        'СОБАКА': 'dog',
        'ЛОШАДЬ': 'horse',
        'КОРОВА': 'cow',
        'СВИНЬЯ': 'pig',
        'ОВЦА': 'sheep',
        'КОЗА': 'goat',
        'КРОЛИК': 'rabbit',
        'КУРИЦА': 'chicken',
        'УТКА': 'duck',
        'ЛЕВ': 'lion',
        'ТИГР': 'tiger',
        'СЛОН': 'elephant',
        'МЕДВЕДЬ': 'bear',
        'ВОЛК': 'wolf',
        'ЛИСА': 'fox',
        'ЗАЯЦ': 'hare',
        'ОЛЕНЬ': 'deer',
        'ЛОСЬ': 'moose',
        'КАБАН': 'boar',
        'ОБЕЗЬЯНА': 'monkey',
        'ГОРИЛЛА': 'gorilla',
        'ШИМПАНЗЕ': 'chimpanzee',
        'ОРАНГУТАН': 'orangutan',
        'ЛЕМУР': 'lemur',
        'ЛЕОПАРД': 'leopard',
        'ГЕПАРД': 'cheetah',
        'РЫСЬ': 'lynx',
        'ПУМА': 'puma',
        'ЯГУАР': 'jaguar',
        'КИТ': 'whale',
        'ДЕЛЬФИН': 'dolphin',
        'АКУЛА': 'shark',
        'ТЮЛЕНЬ': 'seal',
        'МОРЖ': 'walrus',
        'ОСЬМИНОГ': 'octopus',
        'КРАБ': 'crab',
        'ЛОБСТЕР': 'lobster',
        'КРЕВЕТКА': 'shrimp',
        'МЕДУЗА': 'jellyfish',
        'ОРЁЛ': 'eagle',
        'СОВА': 'owl',
        'ПОПУГАЙ': 'parrot',
        'ПИНГВИН': 'penguin',
        'ФЛАМИНГО': 'flamingo',
        'ПАВЛИН': 'peacock',
        'ЛЕБЕДЬ': 'swan',
        'АИСТ': 'stork',
        'ВОРОН': 'raven',
        'ВОРОБЕЙ': 'sparrow',
        'ЗМЕЯ': 'snake',
        'ЯЩЕРИЦА': 'lizard',
        'КРОКОДИЛ': 'crocodile',
        'ЧЕРЕПАХА': 'turtle',
        'ИГУАНА': 'iguana',
        'ХАМЕЛЕОН': 'chameleon',
        'ГЕККОН': 'gecko',
        'ВАРАН': 'monitor lizard',
        'ПИТОН': 'python',
        'КОБРА': 'cobra',
        'ЛЯГУШКА': 'frog',
        'ЖАБА': 'toad',
        'САЛАМАНДРА': 'salamander',
        'ТРИТОН': 'newt',
        'АКСОЛОТЛЬ': 'axolotl',
        'РЫБА': 'fish',
        'ЛОСОСЬ': 'salmon',
        'ТУНЕЦ': 'tuna',
        'ФОРЕЛЬ': 'trout',
        'КАРП': 'carp',
        'ЩУКА': 'pike',
        'ОКУНЬ': 'perch',
        'СОМ': 'catfish',
        'УГОРЬ': 'eel',
        'СКАТ': 'stingray',
        'БАБОЧКА': 'butterfly',
        'ПЧЕЛА': 'bee',
        'МУРАВЕЙ': 'ant',
        'ЖУК': 'beetle',
        'МУХА': 'fly',
        'КОМАР': 'mosquito',
        'СТРЕКОЗА': 'dragonfly',
        'КУЗНЕЧИК': 'grasshopper',
        'СВЕРЧОК': 'cricket',
        'БОЖЬЯ КОРОВКА': 'ladybug',
        'ПАУК': 'spider',
        'СКОРПИОН': 'scorpion',
        'КЛЕЩ': 'tick',
        'ТАРАНТУЛ': 'tarantula',
        'МЫШЬ': 'mouse',
        'КРЫСА': 'rat',
        'БЕЛКА': 'squirrel',
        'ХОМЯК': 'hamster',
        'БОБР': 'beaver',
        'ДИКОБРАЗ': 'porcupine',
        'СУРОК': 'marmot',
        'ШИНШИЛЛА': 'chinchilla',
        'КАПИБАРА': 'capybara',
        'КЕНГУРУ': 'kangaroo',
        'КОАЛА': 'koala',
        'ОПОССУМ': 'opossum',
        'ТАСМАНСКИЙ ДЬЯВОЛ': 'tasmanian devil',
        'ВОМБАТ': 'wombat',
        'ЖИРАФ': 'giraffe',
        'ЗЕБРА': 'zebra',
        'НОСОРОГ': 'rhinoceros',
        'БЕГЕМОТ': 'hippopotamus',
        'АНТИЛОПА': 'antelope',
        'ГАЗЕЛЬ': 'gazelle',
        'ГИЕНА': 'hyena',
        'СУРИКАТ': 'meerkat',
        'БАБУИН': 'baboon',
        'МАНДРИЛ': 'mandrill',
        'БЕЛЫЙ МЕДВЕДЬ': 'polar bear',
        'ПЕСЕЦ': 'arctic fox',
        'СЕВЕРНЫЙ ОЛЕНЬ': 'reindeer',
        'ОВЦЕБЫК': 'musk ox',
        'ЛАМА': 'llama',
        'АЛЬПАКА': 'alpaca',
        'ВИКУНЬЯ': 'vicuna',
        'ЛЕНИВЕЦ': 'sloth',
        'МУРАВЬЕД': 'anteater',
        'БРОНЕНОСЕЦ': 'armadillo',
        'ТУКАН': 'toucan',
        'КОЛИБРИ': 'hummingbird',
        'ЯГУАРУНДИ': 'jaguarundi',
        'ОЦЕЛОТ': 'ocelot',
        'УТКОНОС': 'platypus',
        'ЕХИДНА': 'echidna',
        'ВАЛЛАБИ': 'wallaby',
        'ДИНГО': 'dingo',
        'КУКАБАРРА': 'kookaburra',
        'ПАНДА': 'panda',
        'ЯК': 'yak',
        'СНЕЖНЫЙ БАРС': 'snow leopard',
        'МАЛАЙСКИЙ МЕДВЕДЬ': 'sun bear',
        'БИНТУРОНГ': 'binturong',
        'МОРСКАЯ СВИНКА': 'guinea pig',
        'ХОРЁК': 'ferret',
        'ПОПУГАЙЧИК': 'parakeet',
        'КАНАРЕЙКА': 'canary',
        'ЛЕТУЧАЯ МЫШЬ': 'bat',
        'ЁЖ': 'hedgehog',
        'ЕНОТ': 'raccoon',
        'СКУНС': 'skunk',
        'БАРСУК': 'badger',
        'ВЫДРА': 'otter',
        'ЛАМАНТИН': 'manatee',
        'ДЮГОНЬ': 'dugong',
        'НАРВАЛ': 'narwhal',
        'ЯСТРЕБ': 'hawk',
        'СОКОЛ': 'falcon',
        'КОРШУН': 'kite',
        'ГРИФ': 'vulture',
        'КОНДОР': 'condor',
        'ЗЕМЛЕРОЙКА': 'shrew',
        'КРОТ': 'mole',
        'ЛАСКА': 'weasel',
        'ГОРНОСТАЙ': 'ermine',
        'КУНИЦА': 'marten',
        'ЗУБР': 'bison',
        'БУЙВОЛ': 'buffalo',
        'ВЕРБЛЮД': 'camel',
        'ДРОМАДЕР': 'dromedary',
        'ТАПИР': 'tapir',
        'ОКАПИ': 'okapi',
        'КВАГГА': 'quagga',
        'ФОССА': 'fossa',
        'ТЕНРЕК': 'tenrec',
        'АЙ-АЙ': 'aye-aye',
        'СТРАУС': 'ostrich',
        'ЭМУ': 'emu',
        'КАЗУАР': 'cassowary',
        'КИВИ': 'kiwi',
        'АЛЬБАТРОС': 'albatross',
        'МОРСКОЙ КОНЁК': 'seahorse',
        'МОРСКАЯ ЗВЕЗДА': 'starfish',
        'МОРСКОЙ ЁЖ': 'sea urchin',
        'АНЕМОН': 'sea anemone',
        'КОРАЛЛ': 'coral',
        'ОСА': 'wasp',
        'ШМЕЛЬ': 'bumblebee',
        'ШЕРШЕНЬ': 'hornet',
        'БОГОМОЛ': 'praying mantis',
        'ПАЛОЧНИК': 'stick insect',
        'АНАКОНДА': 'anaconda',
        'УДАВ': 'boa constrictor',
        'ГАДЮКА': 'viper',
        'УЖ': 'grass snake',
        'АГАМА': 'agama',
        'КВАКША': 'tree frog',
        'ЧЕСНОЧНИЦА': 'spadefoot toad',
        'ПРОТЕЙ': 'olm',
        'СИРЕН': 'siren salamander',
        'БАРРАКУДА': 'barracuda',
        'МУРЕНА': 'moray eel',
        'РЫБА-МЕЧ': 'swordfish',
        'РЫБА-МОЛОТ': 'hammerhead shark',
        'РЫБА-КЛОУН': 'clownfish',
        'РОСОМАХА': 'wolverine',
        'СЕРВАЛ': 'serval',
        'КАРАКАЛ': 'caracal',
        'МАНУЛ': 'pallas cat'
    }
    return translations

def create_better_animal_images():
    """Create better animal images with more real photos"""
    
    # Read the Russian animal file to get the list
    animals_file = 'data/words/ru/animals_COMPLETE.txt'
    
    if not os.path.exists(animals_file):
        print(f"Error: {animals_file} not found!")
        return
    
    # Create output directory
    output_dir = 'data/images/animals'
    os.makedirs(output_dir, exist_ok=True)
    
    # Get English translations
    translations = get_english_animal_names()
    
    downloaded_count = 0
    artistic_count = 0
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
            
            # Skip if large image already exists (likely a real photo)
            if os.path.exists(image_path):
                file_size = os.path.getsize(image_path)
                if file_size > 50000:  # 50KB - likely a real photo
                    print(f"  ✓ Keeping existing large image: {image_filename} ({file_size/1024:.1f}KB)")
                    skipped_count += 1
                    continue
            
            # Get English name for search
            english_name = translations.get(animal_name, animal_name.lower())
            
            # Try to download real image
            success = False
            if download_from_free_sources(english_name, image_path):
                success = True
                downloaded_count += 1
                print(f"  ✓ Downloaded real photo: {image_filename}")
            
            # If download failed, create artistic image
            if not success:
                create_artistic_image(animal_name, image_path)
                artistic_count += 1
                print(f"  ✓ Created artistic image: {image_filename}")
            
            # Small delay to be respectful to servers
            time.sleep(0.5)
    
    print(f"\nImage improvement complete!")
    print(f"Downloaded real photos: {downloaded_count}")
    print(f"Created artistic images: {artistic_count}")
    print(f"Kept existing images: {skipped_count}")
    print(f"Total processed: {downloaded_count + artistic_count + skipped_count}")

if __name__ == "__main__":
    print("Better Animal Image Creator")
    print("==========================")
    print()
    print("Improving animal images with real photos and better designs...")
    print()
    
    create_better_animal_images()