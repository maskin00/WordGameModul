#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Improve remaining animal images with better artistic designs
Keep existing real photos (large files) and improve only small artistic images
"""

import os
from PIL import Image, ImageDraw, ImageFont
import random
import math

def create_improved_animal_image(animal_name, image_code, size=(300, 300)):
    """Create an improved artistic animal image"""
    
    # Create image
    img = Image.new('RGB', size, 'white')
    draw = ImageDraw.Draw(img)
    
    # Animal-specific color schemes and patterns
    animal_themes = {
        # Mammals - warm colors
        'ЗАЯЦ': {'colors': ['#F5DEB3', '#DEB887', '#D2B48C'], 'pattern': 'fur'},
        'ЛОСЬ': {'colors': ['#8B4513', '#A0522D', '#CD853F'], 'pattern': 'antlers'},
        'КАБАН': {'colors': ['#696969', '#808080', '#A9A9A9'], 'pattern': 'bristles'},
        'ШИМПАНЗЕ': {'colors': ['#8B4513', '#A0522D', '#CD853F'], 'pattern': 'fur'},
        'ОРАНГУТАН': {'colors': ['#FF8C00', '#FF7F50', '#FFA500'], 'pattern': 'fur'},
        'ЛЕМУР': {'colors': ['#696969', '#FFFFFF', '#000000'], 'pattern': 'stripes'},
        'РЫСЬ': {'colors': ['#F4A460', '#DEB887', '#D2B48C'], 'pattern': 'spots'},
        'ПУМА': {'colors': ['#D2B48C', '#BC8F8F', '#F4A460'], 'pattern': 'solid'},
        'ЯГУАР': {'colors': ['#FFD700', '#FFA500', '#000000'], 'pattern': 'rosettes'},
        
        # Sea animals - blue tones
        'ТЮЛЕНЬ': {'colors': ['#4682B4', '#5F9EA0', '#87CEEB'], 'pattern': 'waves'},
        'МОРЖ': {'colors': ['#708090', '#778899', '#B0C4DE'], 'pattern': 'tusks'},
        'ОСЬМИНОГ': {'colors': ['#8A2BE2', '#9370DB', '#BA55D3'], 'pattern': 'tentacles'},
        'КРАБ': {'colors': ['#FF6347', '#FF4500', '#DC143C'], 'pattern': 'shell'},
        'ЛОБСТЕР': {'colors': ['#DC143C', '#B22222', '#8B0000'], 'pattern': 'claws'},
        'КРЕВЕТКА': {'colors': ['#FFA07A', '#FA8072', '#E9967A'], 'pattern': 'curved'},
        'МЕДУЗА': {'colors': ['#E6E6FA', '#DDA0DD', '#DA70D6'], 'pattern': 'transparent'},
        
        # Birds - bright colors
        'АИСТ': {'colors': ['#FFFFFF', '#000000', '#FF0000'], 'pattern': 'feathers'},
        'ВОРОН': {'colors': ['#000000', '#2F4F4F', '#36454F'], 'pattern': 'feathers'},
        'ВОРОБЕЙ': {'colors': ['#8B4513', '#A0522D', '#D2B48C'], 'pattern': 'feathers'},
        'ТУКАН': {'colors': ['#000000', '#FFD700', '#FF4500'], 'pattern': 'beak'},
        'КОЛИБРИ': {'colors': ['#00FF7F', '#00CED1', '#FF1493'], 'pattern': 'iridescent'},
        
        # Reptiles - earth tones
        'ЯЩЕРИЦА': {'colors': ['#228B22', '#32CD32', '#9ACD32'], 'pattern': 'scales'},
        'ИГУАНА': {'colors': ['#228B22', '#6B8E23', '#9ACD32'], 'pattern': 'spines'},
        'ХАМЕЛЕОН': {'colors': ['#32CD32', '#FF69B4', '#FFD700'], 'pattern': 'color_change'},
        'ГЕККОН': {'colors': ['#F0E68C', '#BDB76B', '#DAA520'], 'pattern': 'spots'},
        'ВАРАН': {'colors': ['#8B4513', '#A0522D', '#CD853F'], 'pattern': 'scales'},
        'ПИТОН': {'colors': ['#8B4513', '#DAA520', '#F4A460'], 'pattern': 'diamond'},
        'КОБРА': {'colors': ['#000000', '#FFD700', '#FF0000'], 'pattern': 'hood'},
        
        # Amphibians - water colors
        'ЖАБА': {'colors': ['#228B22', '#32CD32', '#9ACD32'], 'pattern': 'bumpy'},
        'САЛАМАНДРА': {'colors': ['#FF4500', '#FF6347', '#FFD700'], 'pattern': 'spots'},
        'ТРИТОН': {'colors': ['#4682B4', '#5F9EA0', '#87CEEB'], 'pattern': 'aquatic'},
        'АКСОЛОТЛЬ': {'colors': ['#FFB6C1', '#FFC0CB', '#FFCCCB'], 'pattern': 'gills'},
        
        # Fish - aquatic colors
        'ЛОСОСЬ': {'colors': ['#FA8072', '#FFA07A', '#FFB6C1'], 'pattern': 'scales'},
        'ТУНЕЦ': {'colors': ['#4682B4', '#5F9EA0', '#87CEEB'], 'pattern': 'streamlined'},
        'ФОРЕЛЬ': {'colors': ['#32CD32', '#228B22', '#FFD700'], 'pattern': 'spots'},
        'КАРП': {'colors': ['#FFD700', '#FFA500', '#FF8C00'], 'pattern': 'scales'},
        'ЩУКА': {'colors': ['#228B22', '#32CD32', '#9ACD32'], 'pattern': 'stripes'},
        'ОКУНЬ': {'colors': ['#32CD32', '#228B22', '#FFD700'], 'pattern': 'stripes'},
        'СОМ': {'colors': ['#696969', '#808080', '#A9A9A9'], 'pattern': 'whiskers'},
        'УГОРЬ': {'colors': ['#2F4F4F', '#696969', '#808080'], 'pattern': 'serpentine'},
        'СКАТ': {'colors': ['#D2B48C', '#BC8F8F', '#F4A460'], 'pattern': 'flat'},
        
        # Insects - colorful
        'МУРАВЕЙ': {'colors': ['#8B0000', '#A52A2A', '#DC143C'], 'pattern': 'segments'},
        'ЖУК': {'colors': ['#228B22', '#32CD32', '#00FF00'], 'pattern': 'shell'},
        'МУХА': {'colors': ['#2F4F4F', '#696969', '#808080'], 'pattern': 'wings'},
        'КОМАР': {'colors': ['#696969', '#A9A9A9', '#D3D3D3'], 'pattern': 'thin'},
        'СТРЕКОЗА': {'colors': ['#00CED1', '#40E0D0', '#48D1CC'], 'pattern': 'wings'},
        'КУЗНЕЧИК': {'colors': ['#228B22', '#32CD32', '#9ACD32'], 'pattern': 'legs'},
        'СВЕРЧОК': {'colors': ['#8B4513', '#A0522D', '#CD853F'], 'pattern': 'antennae'},
        'БОЖЬЯ КОРОВКА': {'colors': ['#FF0000', '#000000', '#FFFFFF'], 'pattern': 'spots'},
        
        # Arachnids - dark colors
        'ПАУК': {'colors': ['#000000', '#8B0000', '#A52A2A'], 'pattern': 'web'},
        'СКОРПИОН': {'colors': ['#8B4513', '#A0522D', '#CD853F'], 'pattern': 'claws'},
        'КЛЕЩ': {'colors': ['#8B0000', '#A52A2A', '#DC143C'], 'pattern': 'round'},
        'ТАРАНТУЛ': {'colors': ['#000000', '#8B4513', '#A0522D'], 'pattern': 'hairy'},
        
        # Small mammals
        'МЫШЬ': {'colors': ['#696969', '#808080', '#A9A9A9'], 'pattern': 'small'},
        'КРЫСА': {'colors': ['#696969', '#808080', '#A9A9A9'], 'pattern': 'tail'},
        'ХОМЯК': {'colors': ['#F4A460', '#DEB887', '#D2B48C'], 'pattern': 'cheeks'},
        'ДИКОБРАЗ': {'colors': ['#8B4513', '#A0522D', '#CD853F'], 'pattern': 'quills'},
        'СУРОК': {'colors': ['#8B4513', '#A0522D', '#CD853F'], 'pattern': 'burrow'},
        'ШИНШИЛЛА': {'colors': ['#C0C0C0', '#D3D3D3', '#DCDCDC'], 'pattern': 'soft'},
        'КАПИБАРА': {'colors': ['#8B4513', '#A0522D', '#CD853F'], 'pattern': 'large'},
    }
    
    # Get theme for this animal or use default
    theme = animal_themes.get(animal_name, {
        'colors': ['#4682B4', '#87CEEB', '#B0E0E6'], 
        'pattern': 'default'
    })
    
    colors = theme['colors']
    pattern = theme['pattern']
    
    # Create background gradient
    for y in range(size[1]):
        ratio = y / size[1]
        if len(colors) >= 2:
            # Interpolate between first two colors
            r1, g1, b1 = tuple(int(colors[0][i:i+2], 16) for i in (1, 3, 5))
            r2, g2, b2 = tuple(int(colors[1][i:i+2], 16) for i in (1, 3, 5))
            
            r = int(r1 + (r2 - r1) * ratio)
            g = int(g1 + (g2 - g1) * ratio)
            b = int(b1 + (b2 - b1) * ratio)
            
            color = f'#{r:02x}{g:02x}{b:02x}'
            draw.line([(0, y), (size[0], y)], fill=color)
    
    # Add pattern based on animal type
    if pattern == 'spots':
        # Add spots
        for _ in range(15):
            x = random.randint(20, size[0] - 40)
            y = random.randint(20, size[1] - 40)
            radius = random.randint(8, 20)
            spot_color = colors[2] if len(colors) > 2 else colors[0]
            draw.ellipse([x-radius, y-radius, x+radius, y+radius], fill=spot_color)
    
    elif pattern == 'stripes':
        # Add stripes
        stripe_color = colors[2] if len(colors) > 2 else colors[0]
        for i in range(0, size[0], 30):
            draw.rectangle([i, 0, i+15, size[1]], fill=stripe_color)
    
    elif pattern == 'scales':
        # Add scale pattern
        scale_color = colors[2] if len(colors) > 2 else colors[0]
        for y in range(0, size[1], 20):
            for x in range(0, size[0], 20):
                offset = 10 if (y // 20) % 2 else 0
                draw.ellipse([x+offset-8, y-8, x+offset+8, y+8], outline=scale_color, width=2)
    
    elif pattern == 'feathers':
        # Add feather pattern
        feather_color = colors[2] if len(colors) > 2 else colors[0]
        for _ in range(20):
            x = random.randint(20, size[0] - 20)
            y = random.randint(20, size[1] - 20)
            # Draw feather-like shape
            points = []
            for angle in range(0, 360, 30):
                px = x + 15 * math.cos(math.radians(angle))
                py = y + 8 * math.sin(math.radians(angle))
                points.append((px, py))
            if len(points) >= 3:
                draw.polygon(points, fill=feather_color)
    
    elif pattern == 'waves':
        # Add wave pattern
        wave_color = colors[2] if len(colors) > 2 else colors[0]
        for y in range(0, size[1], 40):
            points = []
            for x in range(0, size[0], 10):
                wave_y = y + 15 * math.sin(x * 0.1)
                points.append((x, wave_y))
            if len(points) >= 2:
                for i in range(len(points)-1):
                    draw.line([points[i], points[i+1]], fill=wave_color, width=3)
    
    # Add decorative border
    border_color = colors[-1] if colors else '#000000'
    draw.rectangle([5, 5, size[0]-5, size[1]-5], outline=border_color, width=3)
    
    # Add animal name text
    try:
        # Try to use a nice font
        font_size = 24
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        # Fallback to default font
        font = ImageFont.load_default()
    
    # Calculate text position
    text_bbox = draw.textbbox((0, 0), animal_name, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    text_x = (size[0] - text_width) // 2
    text_y = size[1] - text_height - 20
    
    # Add text shadow
    shadow_color = '#000000'
    draw.text((text_x + 2, text_y + 2), animal_name, font=font, fill=shadow_color)
    
    # Add main text
    text_color = '#FFFFFF'
    draw.text((text_x, text_y), animal_name, font=font, fill=text_color)
    
    return img

def improve_remaining_animal_images():
    """Improve small animal images while keeping existing real photos"""
    
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
            
            # Check if image exists and its size
            if os.path.exists(image_path):
                file_size = os.path.getsize(image_path)
                
                # If file is large (>50KB), it's probably a real photo - keep it
                if file_size > 50000:
                    print(f"  ✓ Keeping real photo: {image_filename} ({file_size//1024}KB)")
                    kept_count += 1
                    continue
                else:
                    print(f"  → Improving small image: {image_filename} ({file_size//1024}KB)")
            else:
                print(f"  → Creating new image: {image_filename}")
            
            # Create improved artistic image
            try:
                img = create_improved_animal_image(animal_name, image_code)
                img.save(image_path, 'PNG', quality=95)
                improved_count += 1
                print(f"  ✓ Created improved image: {image_filename}")
                
            except Exception as e:
                print(f"  ✗ Error creating image: {e}")
    
    print(f"\nImprovement complete!")
    print(f"Kept real photos: {kept_count}")
    print(f"Improved artistic images: {improved_count}")
    print(f"Total processed: {kept_count + improved_count}")

if __name__ == "__main__":
    print("Animal Image Improver")
    print("====================")
    print()
    print("Improving small animal images while keeping real photos...")
    print()
    
    improve_remaining_animal_images() 