#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Create simple but beautiful animal images
Avoids complex coordinate calculations that cause errors
"""

import os
from PIL import Image, ImageDraw, ImageFont
import random

def create_simple_beautiful_image(animal_name, size=(300, 300)):
    """Create a simple but beautiful animal image"""
    
    # Create image
    img = Image.new('RGB', size, 'white')
    draw = ImageDraw.Draw(img)
    
    # Simple color schemes for each animal
    color_schemes = {
        'КОШКА': ['#FF6B6B', '#4ECDC4'],
        'СОБАКА': ['#96CEB4', '#FFEAA7'],
        'ЛОШАДЬ': ['#8B4513', '#D2B48C'],
        'КОРОВА': ['#2D3436', '#FFFFFF'],
        'СВИНЬЯ': ['#FFB6C1', '#FFA07A'],
        'ОВЦА': ['#FFFFFF', '#F5F5DC'],
        'КОЗА': ['#F5DEB3', '#DEB887'],
        'КРОЛИК': ['#FFB6C1', '#FFC0CB'],
        'КУРИЦА': ['#FFD700', '#FFA500'],
        'УТКА': ['#4682B4', '#87CEEB'],
        'ЛЕВ': ['#FFD700', '#FF8C00'],
        'ТИГР': ['#FF8C00', '#000000'],
        'СЛОН': ['#696969', '#A9A9A9'],
        'МЕДВЕДЬ': ['#8B4513', '#A0522D'],
        'ВОЛК': ['#2F4F4F', '#708090'],
        'ЛИСА': ['#FF4500', '#FF6347'],
        'ЗАЯЦ': ['#F5DEB3', '#DEB887'],
        'ОЛЕНЬ': ['#8B4513', '#A0522D'],
        'ЛОСЬ': ['#556B2F', '#6B8E23'],
        'КАБАН': ['#696969', '#808080'],
        'ОБЕЗЬЯНА': ['#8B4513', '#A0522D'],
        'ГОРИЛЛА': ['#2F4F4F', '#696969'],
        'ШИМПАНЗЕ': ['#8B4513', '#A0522D'],
        'ОРАНГУТАН': ['#FF8C00', '#FF7F50'],
        'ЛЕМУР': ['#696969', '#FFFFFF'],
        'ЛЕОПАРД': ['#FFD700', '#FFA500'],
        'ГЕПАРД': ['#FFD700', '#FFA500'],
        'РЫСЬ': ['#F4A460', '#DEB887'],
        'ПУМА': ['#D2B48C', '#BC8F8F'],
        'ЯГУАР': ['#FFD700', '#FFA500'],
        'КИТ': ['#4682B4', '#87CEEB'],
        'ДЕЛЬФИН': ['#00CED1', '#40E0D0'],
        'АКУЛА': ['#2F4F4F', '#708090'],
        'ТЮЛЕНЬ': ['#4682B4', '#5F9EA0'],
        'МОРЖ': ['#708090', '#778899'],
        'ОСЬМИНОГ': ['#8A2BE2', '#9370DB'],
        'КРАБ': ['#FF6347', '#FF4500'],
        'ЛОБСТЕР': ['#DC143C', '#B22222'],
        'КРЕВЕТКА': ['#FFA07A', '#FA8072'],
        'МЕДУЗА': ['#E6E6FA', '#DDA0DD'],
        'ОРЁЛ': ['#8B4513', '#A0522D'],
        'СОВА': ['#8B4513', '#DEB887'],
        'ПОПУГАЙ': ['#32CD32', '#FF1493'],
        'ПИНГВИН': ['#000000', '#FFFFFF'],
        'ФЛАМИНГО': ['#FF69B4', '#FFB6C1'],
        'ПАВЛИН': ['#4169E1', '#32CD32'],
        'ЛЕБЕДЬ': ['#FFFFFF', '#F5F5DC'],
        'АИСТ': ['#FFFFFF', '#000000'],
        'ВОРОН': ['#000000', '#2F4F4F'],
        'ВОРОБЕЙ': ['#8B4513', '#A0522D'],
        'ЗМЕЯ': ['#228B22', '#32CD32'],
        'ЯЩЕРИЦА': ['#228B22', '#32CD32'],
        'КРОКОДИЛ': ['#556B2F', '#6B8E23'],
        'ЧЕРЕПАХА': ['#228B22', '#32CD32'],
        'ИГУАНА': ['#228B22', '#6B8E23'],
        'ХАМЕЛЕОН': ['#32CD32', '#FF69B4'],
        'ГЕККОН': ['#F0E68C', '#BDB76B'],
        'ВАРАН': ['#8B4513', '#A0522D'],
        'ПИТОН': ['#8B4513', '#DAA520'],
        'КОБРА': ['#000000', '#FFD700'],
        'ЛЯГУШКА': ['#228B22', '#32CD32'],
        'ЖАБА': ['#228B22', '#32CD32'],
        'САЛАМАНДРА': ['#FF4500', '#FF6347'],
        'ТРИТОН': ['#4682B4', '#5F9EA0'],
        'АКСОЛОТЛЬ': ['#FFB6C1', '#FFC0CB'],
        'РЫБА': ['#4682B4', '#87CEEB'],
        'ЛОСОСЬ': ['#FA8072', '#FFA07A'],
        'ТУНЕЦ': ['#4682B4', '#5F9EA0'],
        'ФОРЕЛЬ': ['#32CD32', '#228B22'],
        'КАРП': ['#FFD700', '#FFA500'],
        'ЩУКА': ['#228B22', '#32CD32'],
        'ОКУНЬ': ['#32CD32', '#228B22'],
        'СОМ': ['#696969', '#808080'],
        'УГОРЬ': ['#2F4F4F', '#696969'],
        'СКАТ': ['#D2B48C', '#BC8F8F'],
        'БАБОЧКА': ['#FF69B4', '#FFD700'],
        'ПЧЕЛА': ['#FFD700', '#000000'],
        'МУРАВЕЙ': ['#8B0000', '#A52A2A'],
        'ЖУК': ['#228B22', '#32CD32'],
        'МУХА': ['#2F4F4F', '#696969'],
        'КОМАР': ['#696969', '#A9A9A9'],
        'СТРЕКОЗА': ['#00CED1', '#40E0D0'],
        'КУЗНЕЧИК': ['#228B22', '#32CD32'],
        'СВЕРЧОК': ['#8B4513', '#A0522D'],
        'БОЖЬЯ КОРОВКА': ['#FF0000', '#000000'],
        'ПАУК': ['#000000', '#8B0000'],
        'СКОРПИОН': ['#8B4513', '#A0522D'],
        'КЛЕЩ': ['#8B0000', '#A52A2A'],
        'ТАРАНТУЛ': ['#000000', '#8B4513'],
        'МЫШЬ': ['#696969', '#808080'],
        'КРЫСА': ['#696969', '#808080'],
        'БЕЛКА': ['#8B4513', '#A0522D'],
        'ХОМЯК': ['#F4A460', '#DEB887'],
        'БОБР': ['#8B4513', '#A0522D'],
        'ДИКОБРАЗ': ['#8B4513', '#A0522D'],
        'СУРОК': ['#8B4513', '#A0522D'],
        'ШИНШИЛЛА': ['#C0C0C0', '#D3D3D3'],
        'КАПИБАРА': ['#8B4513', '#A0522D'],
        'КЕНГУРУ': ['#8B4513', '#A0522D'],
        'КОАЛА': ['#696969', '#808080'],
        'ОПОССУМ': ['#696969', '#808080'],
        'ЖИРАФ': ['#DAA520', '#F4A460'],
        'ЗЕБРА': ['#000000', '#FFFFFF'],
        'НОСОРОГ': ['#696969', '#A9A9A9'],
        'БЕГЕМОТ': ['#696969', '#A9A9A9'],
        'ПАНДА': ['#000000', '#FFFFFF'],
    }
    
    # Get colors for this animal or use default
    colors = color_schemes.get(animal_name, ['#4682B4', '#87CEEB'])
    
    # Create simple gradient background
    for y in range(size[1]):
        ratio = y / size[1]
        # Interpolate between two colors
        r1, g1, b1 = tuple(int(colors[0][i:i+2], 16) for i in (1, 3, 5))
        r2, g2, b2 = tuple(int(colors[1][i:i+2], 16) for i in (1, 3, 5))
        
        r = int(r1 + (r2 - r1) * ratio)
        g = int(g1 + (g2 - g1) * ratio)
        b = int(b1 + (b2 - b1) * ratio)
        
        color = f'#{r:02x}{g:02x}{b:02x}'
        draw.line([(0, y), (size[0], y)], fill=color)
    
    # Add simple decorative elements
    for _ in range(8):
        x = random.randint(30, size[0] - 50)
        y = random.randint(30, size[1] - 80)
        radius = random.randint(10, 25)
        
        # Simple circles with the second color
        circle_color = colors[1] if len(colors) > 1 else colors[0]
        draw.ellipse([x-radius, y-radius, x+radius, y+radius], 
                    outline=circle_color, width=3)
    
    # Add simple border
    border_color = colors[0]
    draw.rectangle([5, 5, size[0]-6, size[1]-6], outline=border_color, width=4)
    
    # Add animal name with simple typography
    try:
        font_size = 28
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        try:
            font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", font_size)
        except:
            font = ImageFont.load_default()
    
    # Calculate text position
    text_bbox = draw.textbbox((0, 0), animal_name, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    text_x = (size[0] - text_width) // 2
    text_y = size[1] - text_height - 25
    
    # Add simple text background rectangle
    padding = 12
    bg_x1 = max(0, text_x - padding)
    bg_y1 = max(0, text_y - padding)
    bg_x2 = min(size[0], text_x + text_width + padding)
    bg_y2 = min(size[1], text_y + text_height + padding)
    
    # Draw background rectangle
    draw.rectangle([bg_x1, bg_y1, bg_x2, bg_y2], fill='#000000')
    
    # Add text shadow
    draw.text((text_x + 2, text_y + 2), animal_name, font=font, fill='#333333')
    
    # Add main text
    draw.text((text_x, text_y), animal_name, font=font, fill='#FFFFFF')
    
    return img

def replace_all_animal_images_simple():
    """Replace ALL animal images with simple beautiful designs"""
    
    # Read the Russian animal file to get the list
    animals_file = 'data/words/ru/animals_COMPLETE.txt'
    
    if not os.path.exists(animals_file):
        print(f"Error: {animals_file} not found!")
        return
    
    # Create output directory
    output_dir = 'data/images/animals'
    os.makedirs(output_dir, exist_ok=True)
    
    replaced_count = 0
    
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
            
            # Create simple beautiful image (always replace)
            try:
                print(f"  → Creating beautiful image for {animal_name}")
                img = create_simple_beautiful_image(animal_name)
                img.save(image_path, 'PNG', quality=95, optimize=True)
                replaced_count += 1
                
                # Check final file size
                final_size = os.path.getsize(image_path)
                print(f"  ✓ Created beautiful image: {image_filename} ({final_size//1024}KB)")
                
            except Exception as e:
                print(f"  ✗ Error creating image: {e}")
    
    print(f"\nReplacement complete!")
    print(f"Replaced images: {replaced_count}")
    print(f"All animal images now have beautiful new designs!")

if __name__ == "__main__":
    print("Simple Beautiful Animal Image Creator")
    print("====================================")
    print()
    print("Creating simple but beautiful animal images...")
    print()
    
    replace_all_animal_images_simple() 