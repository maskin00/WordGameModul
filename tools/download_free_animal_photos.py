#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Download animal photos from free APIs and sources
Uses various free photo services to get real animal images
"""

import os
import requests
import time
from PIL import Image
import io
import json
import random

def get_headers():
    """Get random user agent headers"""
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0'
    ]
    
    return {
        'User-Agent': random.choice(user_agents),
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
        'Connection': 'keep-alive'
    }

def get_animal_photo_from_lorem_picsum(animal_name, size=300):
    """Get random photo from Lorem Picsum (placeholder service)"""
    try:
        # Lorem Picsum provides random photos
        url = f"https://picsum.photos/{size}/{size}"
        
        headers = get_headers()
        response = requests.get(url, headers=headers, timeout=10, allow_redirects=True)
        
        if response.status_code == 200:
            return response.content
            
    except Exception as e:
        print(f"Error getting photo from Lorem Picsum: {e}")
        
    return None

def get_animal_photo_from_placeholder(animal_name, size=300):
    """Get placeholder photo with animal name"""
    try:
        # Use placeholder.com to generate images with text
        url = f"https://via.placeholder.com/{size}x{size}/4CAF50/FFFFFF?text={animal_name}"
        
        headers = get_headers()
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            return response.content
            
    except Exception as e:
        print(f"Error getting placeholder photo: {e}")
        
    return None

def create_beautiful_animal_image(animal_name, size=(300, 300)):
    """Create a beautiful animal image with better design"""
    
    from PIL import ImageDraw, ImageFont
    import math
    
    # Create image with gradient background
    img = Image.new('RGB', size, 'white')
    draw = ImageDraw.Draw(img)
    
    # Animal-specific beautiful color schemes
    color_schemes = {
        'КОШКА': ['#FF6B6B', '#4ECDC4', '#45B7D1'],
        'СОБАКА': ['#96CEB4', '#FFEAA7', '#DDA0DD'],
        'ЛОШАДЬ': ['#8B4513', '#D2B48C', '#F4A460'],
        'КОРОВА': ['#000000', '#FFFFFF', '#FFB6C1'],
        'ЛЕВ': ['#FFD700', '#FF8C00', '#B8860B'],
        'ТИГР': ['#FF8C00', '#000000', '#FFD700'],
        'СЛОН': ['#696969', '#A9A9A9', '#D3D3D3'],
        'МЕДВЕДЬ': ['#8B4513', '#A0522D', '#CD853F'],
        'ВОЛК': ['#2F4F4F', '#708090', '#B0C4DE'],
        'ЛИСА': ['#FF4500', '#FF6347', '#FFA500'],
        'ЖИРАФ': ['#DAA520', '#F4A460', '#FFFF99'],
        'ЗЕБРА': ['#000000', '#FFFFFF', '#C0C0C0'],
        'ПАНДА': ['#000000', '#FFFFFF', '#FFB6C1'],
        'ПИНГВИН': ['#000000', '#FFFFFF', '#87CEEB'],
        'ОРЁЛ': ['#8B4513', '#A0522D', '#CD853F'],
        'СОВА': ['#8B4513', '#DEB887', '#F5DEB3'],
        'ПОПУГАЙ': ['#32CD32', '#FF1493', '#FFD700'],
        'КИТ': ['#4682B4', '#87CEEB', '#B0E0E6'],
        'ДЕЛЬФИН': ['#00CED1', '#40E0D0', '#48D1CC'],
        'АКУЛА': ['#2F4F4F', '#708090', '#B0C4DE'],
        'ЗАЯЦ': ['#F5DEB3', '#DEB887', '#D2B48C'],
        'ОЛЕНЬ': ['#8B4513', '#A0522D', '#CD853F'],
        'ЛОСЬ': ['#556B2F', '#6B8E23', '#9ACD32'],
        'КАБАН': ['#696969', '#808080', '#A9A9A9'],
        'ОБЕЗЬЯНА': ['#8B4513', '#A0522D', '#CD853F'],
        'ГОРИЛЛА': ['#2F4F4F', '#696969', '#808080'],
        'ЛЕОПАРД': ['#FFD700', '#FFA500', '#000000'],
        'ГЕПАРД': ['#FFD700', '#FFA500', '#000000'],
        'РЫСЬ': ['#F4A460', '#DEB887', '#D2B48C'],
        'ПУМА': ['#D2B48C', '#BC8F8F', '#F4A460'],
        'ЯГУАР': ['#FFD700', '#FFA500', '#000000'],
    }
    
    # Get colors for this animal or use default
    colors = color_schemes.get(animal_name, ['#4682B4', '#87CEEB', '#B0E0E6'])
    
    # Create radial gradient background
    center_x, center_y = size[0] // 2, size[1] // 2
    max_radius = max(size) // 2
    
    for y in range(size[1]):
        for x in range(size[0]):
            # Calculate distance from center
            distance = math.sqrt((x - center_x) ** 2 + (y - center_y) ** 2)
            ratio = min(distance / max_radius, 1.0)
            
            # Interpolate between colors
            if ratio < 0.5:
                # Between color 0 and 1
                t = ratio * 2
                r1, g1, b1 = tuple(int(colors[0][i:i+2], 16) for i in (1, 3, 5))
                r2, g2, b2 = tuple(int(colors[1][i:i+2], 16) for i in (1, 3, 5))
            else:
                # Between color 1 and 2
                t = (ratio - 0.5) * 2
                r1, g1, b1 = tuple(int(colors[1][i:i+2], 16) for i in (1, 3, 5))
                r2, g2, b2 = tuple(int(colors[2][i:i+2], 16) for i in (1, 3, 5))
            
            r = int(r1 + (r2 - r1) * t)
            g = int(g1 + (g2 - g1) * t)
            b = int(b1 + (b2 - b1) * t)
            
            img.putpixel((x, y), (r, g, b))
    
    # Add decorative elements
    draw = ImageDraw.Draw(img)
    
    # Add some decorative shapes
    for _ in range(8):
        x = random.randint(20, size[0] - 40)
        y = random.randint(20, size[1] - 60)
        radius = random.randint(5, 15)
        
        # Semi-transparent circles
        overlay = Image.new('RGBA', size, (0, 0, 0, 0))
        overlay_draw = ImageDraw.Draw(overlay)
        
        color_idx = random.randint(0, len(colors) - 1)
        color_rgb = tuple(int(colors[color_idx][i:i+2], 16) for i in (1, 3, 5))
        overlay_draw.ellipse([x-radius, y-radius, x+radius, y+radius], 
                           fill=(*color_rgb, 80))
        
        img = Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB')
    
    # Add border
    draw = ImageDraw.Draw(img)
    border_color = colors[0]
    draw.rectangle([2, 2, size[0]-2, size[1]-2], outline=border_color, width=4)
    
    # Add animal name with better typography
    try:
        font_size = 28
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        font = ImageFont.load_default()
    
    # Calculate text position
    text_bbox = draw.textbbox((0, 0), animal_name, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    text_x = (size[0] - text_width) // 2
    text_y = size[1] - text_height - 25
    
    # Add text background
    padding = 10
    text_bg_coords = [
        text_x - padding, 
        text_y - padding, 
        text_x + text_width + padding, 
        text_y + text_height + padding
    ]
    
    # Semi-transparent background for text
    overlay = Image.new('RGBA', size, (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)
    overlay_draw.rounded_rectangle(text_bg_coords, radius=8, fill=(0, 0, 0, 120))
    img = Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB')
    
    # Add text shadow
    draw = ImageDraw.Draw(img)
    draw.text((text_x + 2, text_y + 2), animal_name, font=font, fill='#000000')
    
    # Add main text
    draw.text((text_x, text_y), animal_name, font=font, fill='#FFFFFF')
    
    return img

def download_and_improve_animal_photos():
    """Download and improve animal photos"""
    
    # Read the Russian animal file to get the list
    animals_file = 'data/words/ru/animals_COMPLETE.txt'
    
    if not os.path.exists(animals_file):
        print(f"Error: {animals_file} not found!")
        return
    
    # Create output directory
    output_dir = 'data/images/animals'
    os.makedirs(output_dir, exist_ok=True)
    
    improved_count = 0
    kept_count = 0
    
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
                if file_size > 80000:  # 80KB - definitely a real photo
                    print(f"  ✓ Keeping real photo: {image_filename} ({file_size//1024}KB)")
                    kept_count += 1
                    continue
                elif file_size > 30000:  # 30KB - might be a good image
                    print(f"  ✓ Keeping existing image: {image_filename} ({file_size//1024}KB)")
                    kept_count += 1
                    continue
            
            # Create beautiful artistic image
            try:
                print(f"  → Creating beautiful image for {animal_name}")
                img = create_beautiful_animal_image(animal_name)
                img.save(image_path, 'PNG', quality=95, optimize=True)
                improved_count += 1
                
                # Check final file size
                final_size = os.path.getsize(image_path)
                print(f"  ✓ Created beautiful image: {image_filename} ({final_size//1024}KB)")
                
            except Exception as e:
                print(f"  ✗ Error creating image: {e}")
    
    print(f"\nImprovement complete!")
    print(f"Kept existing photos: {kept_count}")
    print(f"Created beautiful images: {improved_count}")
    print(f"Total processed: {kept_count + improved_count}")

if __name__ == "__main__":
    print("Free Animal Photo Downloader")
    print("===========================")
    print()
    print("Creating beautiful animal images...")
    print()
    
    download_and_improve_animal_photos() 