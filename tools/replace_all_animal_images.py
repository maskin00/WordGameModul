#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Replace ALL animal images with new beautiful designs
Overwrites all existing images with improved versions
"""

import os
from PIL import Image, ImageDraw, ImageFont
import random
import math

def create_stunning_animal_image(animal_name, size=(300, 300)):
    """Create a stunning animal image with professional design"""
    
    # Create image
    img = Image.new('RGB', size, 'white')
    draw = ImageDraw.Draw(img)
    
    # Professional color schemes for each animal
    color_schemes = {
        'КОШКА': ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4'],
        'СОБАКА': ['#96CEB4', '#FFEAA7', '#DDA0DD', '#74B9FF'],
        'ЛОШАДЬ': ['#8B4513', '#D2B48C', '#F4A460', '#DEB887'],
        'КОРОВА': ['#2D3436', '#FFFFFF', '#FFB6C1', '#DDD'],
        'СВИНЬЯ': ['#FFB6C1', '#FFA07A', '#F0E68C', '#DDA0DD'],
        'ОВЦА': ['#FFFFFF', '#F5F5DC', '#E6E6FA', '#D3D3D3'],
        'КОЗА': ['#F5DEB3', '#DEB887', '#D2B48C', '#BC8F8F'],
        'КРОЛИК': ['#FFB6C1', '#FFC0CB', '#FFCCCB', '#F0E68C'],
        'КУРИЦА': ['#FFD700', '#FFA500', '#FF8C00', '#F4A460'],
        'УТКА': ['#4682B4', '#87CEEB', '#B0E0E6', '#ADD8E6'],
        'ЛЕВ': ['#FFD700', '#FF8C00', '#B8860B', '#DAA520'],
        'ТИГР': ['#FF8C00', '#000000', '#FFD700', '#FFA500'],
        'СЛОН': ['#696969', '#A9A9A9', '#D3D3D3', '#C0C0C0'],
        'МЕДВЕДЬ': ['#8B4513', '#A0522D', '#CD853F', '#D2B48C'],
        'ВОЛК': ['#2F4F4F', '#708090', '#B0C4DE', '#778899'],
        'ЛИСА': ['#FF4500', '#FF6347', '#FFA500', '#FF7F50'],
        'ЗАЯЦ': ['#F5DEB3', '#DEB887', '#D2B48C', '#BC8F8F'],
        'ОЛЕНЬ': ['#8B4513', '#A0522D', '#CD853F', '#D2B48C'],
        'ЛОСЬ': ['#556B2F', '#6B8E23', '#9ACD32', '#8FBC8F'],
        'КАБАН': ['#696969', '#808080', '#A9A9A9', '#778899'],
        'ОБЕЗЬЯНА': ['#8B4513', '#A0522D', '#CD853F', '#D2B48C'],
        'ГОРИЛЛА': ['#2F4F4F', '#696969', '#808080', '#A9A9A9'],
        'ШИМПАНЗЕ': ['#8B4513', '#A0522D', '#CD853F', '#D2B48C'],
        'ОРАНГУТАН': ['#FF8C00', '#FF7F50', '#FFA500', '#FFB347'],
        'ЛЕМУР': ['#696969', '#FFFFFF', '#000000', '#C0C0C0'],
        'ЛЕОПАРД': ['#FFD700', '#FFA500', '#000000', '#DAA520'],
        'ГЕПАРД': ['#FFD700', '#FFA500', '#000000', '#F4A460'],
        'РЫСЬ': ['#F4A460', '#DEB887', '#D2B48C', '#BC8F8F'],
        'ПУМА': ['#D2B48C', '#BC8F8F', '#F4A460', '#DEB887'],
        'ЯГУАР': ['#FFD700', '#FFA500', '#000000', '#DAA520'],
        'КИТ': ['#4682B4', '#87CEEB', '#B0E0E6', '#ADD8E6'],
        'ДЕЛЬФИН': ['#00CED1', '#40E0D0', '#48D1CC', '#AFEEEE'],
        'АКУЛА': ['#2F4F4F', '#708090', '#B0C4DE', '#778899'],
        'ТЮЛЕНЬ': ['#4682B4', '#5F9EA0', '#87CEEB', '#B0C4DE'],
        'МОРЖ': ['#708090', '#778899', '#B0C4DE', '#C0C0C0'],
        'ОСЬМИНОГ': ['#8A2BE2', '#9370DB', '#BA55D3', '#DDA0DD'],
        'КРАБ': ['#FF6347', '#FF4500', '#DC143C', '#B22222'],
        'ЛОБСТЕР': ['#DC143C', '#B22222', '#8B0000', '#A0522D'],
        'КРЕВЕТКА': ['#FFA07A', '#FA8072', '#E9967A', '#F0E68C'],
        'МЕДУЗА': ['#E6E6FA', '#DDA0DD', '#DA70D6', '#EE82EE'],
        'ОРЁЛ': ['#8B4513', '#A0522D', '#CD853F', '#D2B48C'],
        'СОВА': ['#8B4513', '#DEB887', '#F5DEB3', '#D2B48C'],
        'ПОПУГАЙ': ['#32CD32', '#FF1493', '#FFD700', '#00CED1'],
        'ПИНГВИН': ['#000000', '#FFFFFF', '#87CEEB', '#B0C4DE'],
        'ФЛАМИНГО': ['#FF69B4', '#FFB6C1', '#FFC0CB', '#FFCCCB'],
        'ПАВЛИН': ['#4169E1', '#32CD32', '#FFD700', '#FF1493'],
        'ЛЕБЕДЬ': ['#FFFFFF', '#F5F5DC', '#E6E6FA', '#D3D3D3'],
        'АИСТ': ['#FFFFFF', '#000000', '#FF0000', '#C0C0C0'],
        'ВОРОН': ['#000000', '#2F4F4F', '#36454F', '#696969'],
        'ВОРОБЕЙ': ['#8B4513', '#A0522D', '#D2B48C', '#DEB887'],
        'ЗМЕЯ': ['#228B22', '#32CD32', '#9ACD32', '#8FBC8F'],
        'ЯЩЕРИЦА': ['#228B22', '#32CD32', '#9ACD32', '#8FBC8F'],
        'КРОКОДИЛ': ['#556B2F', '#6B8E23', '#9ACD32', '#8FBC8F'],
        'ЧЕРЕПАХА': ['#228B22', '#32CD32', '#9ACD32', '#8FBC8F'],
        'ИГУАНА': ['#228B22', '#6B8E23', '#9ACD32', '#8FBC8F'],
        'ХАМЕЛЕОН': ['#32CD32', '#FF69B4', '#FFD700', '#00CED1'],
        'ГЕККОН': ['#F0E68C', '#BDB76B', '#DAA520', '#D2B48C'],
        'ВАРАН': ['#8B4513', '#A0522D', '#CD853F', '#D2B48C'],
        'ПИТОН': ['#8B4513', '#DAA520', '#F4A460', '#DEB887'],
        'КОБРА': ['#000000', '#FFD700', '#FF0000', '#FFA500'],
        'ЛЯГУШКА': ['#228B22', '#32CD32', '#9ACD32', '#8FBC8F'],
        'ЖАБА': ['#228B22', '#32CD32', '#9ACD32', '#8FBC8F'],
        'САЛАМАНДРА': ['#FF4500', '#FF6347', '#FFD700', '#FFA500'],
        'ТРИТОН': ['#4682B4', '#5F9EA0', '#87CEEB', '#B0C4DE'],
        'АКСОЛОТЛЬ': ['#FFB6C1', '#FFC0CB', '#FFCCCB', '#F0E68C'],
        'РЫБА': ['#4682B4', '#87CEEB', '#B0E0E6', '#ADD8E6'],
        'ЛОСОСЬ': ['#FA8072', '#FFA07A', '#FFB6C1', '#F0E68C'],
        'ТУНЕЦ': ['#4682B4', '#5F9EA0', '#87CEEB', '#B0C4DE'],
        'ФОРЕЛЬ': ['#32CD32', '#228B22', '#FFD700', '#9ACD32'],
        'КАРП': ['#FFD700', '#FFA500', '#FF8C00', '#DAA520'],
        'ЩУКА': ['#228B22', '#32CD32', '#9ACD32', '#8FBC8F'],
        'ОКУНЬ': ['#32CD32', '#228B22', '#FFD700', '#9ACD32'],
        'СОМ': ['#696969', '#808080', '#A9A9A9', '#778899'],
        'УГОРЬ': ['#2F4F4F', '#696969', '#808080', '#A9A9A9'],
        'СКАТ': ['#D2B48C', '#BC8F8F', '#F4A460', '#DEB887'],
        'БАБОЧКА': ['#FF69B4', '#FFD700', '#32CD32', '#FF1493'],
        'ПЧЕЛА': ['#FFD700', '#000000', '#FFA500', '#F4A460'],
        'МУРАВЕЙ': ['#8B0000', '#A52A2A', '#DC143C', '#B22222'],
        'ЖУК': ['#228B22', '#32CD32', '#00FF00', '#9ACD32'],
        'МУХА': ['#2F4F4F', '#696969', '#808080', '#A9A9A9'],
        'КОМАР': ['#696969', '#A9A9A9', '#D3D3D3', '#C0C0C0'],
        'СТРЕКОЗА': ['#00CED1', '#40E0D0', '#48D1CC', '#AFEEEE'],
        'КУЗНЕЧИК': ['#228B22', '#32CD32', '#9ACD32', '#8FBC8F'],
        'СВЕРЧОК': ['#8B4513', '#A0522D', '#CD853F', '#D2B48C'],
        'БОЖЬЯ КОРОВКА': ['#FF0000', '#000000', '#FFFFFF', '#FFB6C1'],
        'ПАУК': ['#000000', '#8B0000', '#A52A2A', '#2F4F4F'],
        'СКОРПИОН': ['#8B4513', '#A0522D', '#CD853F', '#D2B48C'],
        'КЛЕЩ': ['#8B0000', '#A52A2A', '#DC143C', '#B22222'],
        'ТАРАНТУЛ': ['#000000', '#8B4513', '#A0522D', '#2F4F4F'],
        'МЫШЬ': ['#696969', '#808080', '#A9A9A9', '#C0C0C0'],
        'КРЫСА': ['#696969', '#808080', '#A9A9A9', '#778899'],
        'БЕЛКА': ['#8B4513', '#A0522D', '#CD853F', '#D2B48C'],
        'ХОМЯК': ['#F4A460', '#DEB887', '#D2B48C', '#BC8F8F'],
        'БОБР': ['#8B4513', '#A0522D', '#CD853F', '#D2B48C'],
        'ДИКОБРАЗ': ['#8B4513', '#A0522D', '#CD853F', '#696969'],
        'СУРОК': ['#8B4513', '#A0522D', '#CD853F', '#D2B48C'],
        'ШИНШИЛЛА': ['#C0C0C0', '#D3D3D3', '#DCDCDC', '#E6E6FA'],
        'КАПИБАРА': ['#8B4513', '#A0522D', '#CD853F', '#D2B48C'],
        'КЕНГУРУ': ['#8B4513', '#A0522D', '#CD853F', '#D2B48C'],
        'КОАЛА': ['#696969', '#808080', '#A9A9A9', '#C0C0C0'],
        'ОПОССУМ': ['#696969', '#808080', '#A9A9A9', '#C0C0C0'],
        'ЖИРАФ': ['#DAA520', '#F4A460', '#FFFF99', '#FFD700'],
        'ЗЕБРА': ['#000000', '#FFFFFF', '#C0C0C0', '#D3D3D3'],
        'НОСОРОГ': ['#696969', '#A9A9A9', '#D3D3D3', '#C0C0C0'],
        'БЕГЕМОТ': ['#696969', '#A9A9A9', '#D3D3D3', '#C0C0C0'],
        'ПАНДА': ['#000000', '#FFFFFF', '#FFB6C1', '#C0C0C0'],
    }
    
    # Get colors for this animal or use default
    colors = color_schemes.get(animal_name, ['#4682B4', '#87CEEB', '#B0E0E6', '#ADD8E6'])
    
    # Create beautiful radial gradient background
    center_x, center_y = size[0] // 2, size[1] // 2
    max_radius = max(size) // 2
    
    for y in range(size[1]):
        for x in range(size[0]):
            # Calculate distance from center
            distance = math.sqrt((x - center_x) ** 2 + (y - center_y) ** 2)
            ratio = min(distance / max_radius, 1.0)
            
            # Multi-color gradient
            if ratio < 0.33:
                # Between color 0 and 1
                t = ratio * 3
                r1, g1, b1 = tuple(int(colors[0][i:i+2], 16) for i in (1, 3, 5))
                r2, g2, b2 = tuple(int(colors[1][i:i+2], 16) for i in (1, 3, 5))
            elif ratio < 0.66:
                # Between color 1 and 2
                t = (ratio - 0.33) * 3
                r1, g1, b1 = tuple(int(colors[1][i:i+2], 16) for i in (1, 3, 5))
                r2, g2, b2 = tuple(int(colors[2][i:i+2], 16) for i in (1, 3, 5))
            else:
                # Between color 2 and 3
                t = (ratio - 0.66) * 3
                r1, g1, b1 = tuple(int(colors[2][i:i+2], 16) for i in (1, 3, 5))
                r2, g2, b2 = tuple(int(colors[3][i:i+2], 16) for i in (1, 3, 5))
            
            r = int(r1 + (r2 - r1) * t)
            g = int(g1 + (g2 - g1) * t)
            b = int(b1 + (b2 - b1) * t)
            
            img.putpixel((x, y), (r, g, b))
    
    # Add decorative elements
    draw = ImageDraw.Draw(img)
    
    # Add beautiful decorative shapes
    for _ in range(12):
        x = random.randint(30, size[0] - 50)
        y = random.randint(30, size[1] - 80)
        radius = random.randint(8, 25)
        
        # Create semi-transparent overlay
        overlay = Image.new('RGBA', size, (0, 0, 0, 0))
        overlay_draw = ImageDraw.Draw(overlay)
        
        color_idx = random.randint(0, len(colors) - 1)
        color_rgb = tuple(int(colors[color_idx][i:i+2], 16) for i in (1, 3, 5))
        
        # Random shape type
        shape_type = random.choice(['circle', 'star', 'diamond'])
        
        if shape_type == 'circle':
            overlay_draw.ellipse([x-radius, y-radius, x+radius, y+radius], 
                               fill=(*color_rgb, 60))
        elif shape_type == 'star':
            # Draw star shape
            points = []
            for i in range(10):
                angle = i * math.pi / 5
                if i % 2 == 0:
                    r = radius
                else:
                    r = radius // 2
                px = x + r * math.cos(angle)
                py = y + r * math.sin(angle)
                points.append((px, py))
            overlay_draw.polygon(points, fill=(*color_rgb, 60))
        else:  # diamond
            points = [
                (x, y - radius),
                (x + radius, y),
                (x, y + radius),
                (x - radius, y)
            ]
            overlay_draw.polygon(points, fill=(*color_rgb, 60))
        
        img = Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB')
    
    # Add elegant border
    draw = ImageDraw.Draw(img)
    border_color = colors[0]
    
    # Multiple border lines for elegance
    for i in range(3):
        draw.rectangle([3+i, 3+i, size[0]-3-i, size[1]-3-i], outline=border_color, width=2)
    
    # Add animal name with professional typography
    try:
        font_size = 32
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        try:
            font_size = 32
            font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", font_size)
        except:
            font = ImageFont.load_default()
    
    # Calculate text position
    text_bbox = draw.textbbox((0, 0), animal_name, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    text_x = (size[0] - text_width) // 2
    text_y = size[1] - text_height - 30
    
    # Add elegant text background
    padding = 15
    text_bg_coords = [
        text_x - padding, 
        text_y - padding, 
        text_x + text_width + padding, 
        text_y + text_height + padding
    ]
    
    # Create gradient text background
    overlay = Image.new('RGBA', size, (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)
    
    # Rounded rectangle with gradient effect
    for i in range(padding):
        alpha = int(150 * (1 - i / padding))
        overlay_draw.rounded_rectangle([
            text_bg_coords[0] + i,
            text_bg_coords[1] + i,
            text_bg_coords[2] - i,
            text_bg_coords[3] - i
        ], radius=12-i, fill=(0, 0, 0, alpha))
    
    img = Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB')
    
    # Add text with multiple shadows for depth
    draw = ImageDraw.Draw(img)
    
    # Multiple shadow layers
    for offset in [(3, 3), (2, 2), (1, 1)]:
        shadow_alpha = 100 - offset[0] * 20
        draw.text((text_x + offset[0], text_y + offset[1]), animal_name, 
                 font=font, fill=(0, 0, 0))
    
    # Main text in white
    draw.text((text_x, text_y), animal_name, font=font, fill='#FFFFFF')
    
    # Add subtle highlight
    draw.text((text_x - 1, text_y - 1), animal_name, font=font, fill='#F0F0F0')
    
    return img

def replace_all_animal_images():
    """Replace ALL animal images with new beautiful designs"""
    
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
            
            # Create stunning new image (always replace)
            try:
                print(f"  → Creating stunning image for {animal_name}")
                img = create_stunning_animal_image(animal_name)
                img.save(image_path, 'PNG', quality=95, optimize=True)
                replaced_count += 1
                
                # Check final file size
                final_size = os.path.getsize(image_path)
                print(f"  ✓ Created stunning image: {image_filename} ({final_size//1024}KB)")
                
            except Exception as e:
                print(f"  ✗ Error creating image: {e}")
    
    print(f"\nReplacement complete!")
    print(f"Replaced images: {replaced_count}")
    print(f"All animal images now have stunning new designs!")

if __name__ == "__main__":
    print("Animal Image Replacer")
    print("====================")
    print()
    print("Replacing ALL animal images with stunning new designs...")
    print()
    
    replace_all_animal_images() 