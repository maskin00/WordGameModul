#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Fast script to create beautiful animal images for the word game
Creates artistic images with animal-themed designs and patterns
"""

import os
import math
from PIL import Image, ImageDraw, ImageFont
import random

def create_beautiful_animal_image(animal_name, filename, size=(300, 300)):
    """Create a beautiful artistic image for an animal"""
    
    # Animal-themed color schemes and patterns
    animal_themes = {
        # Mammals - warm colors
        'КОШКА': {
            'colors': [(255, 218, 185), (255, 160, 122), (205, 92, 92)],
            'pattern': 'stripes',
            'emoji': '🐱'
        },
        'СОБАКА': {
            'colors': [(135, 206, 235), (100, 149, 237), (65, 105, 225)],
            'pattern': 'spots',
            'emoji': '🐶'
        },
        'ЛОШАДЬ': {
            'colors': [(222, 184, 135), (205, 133, 63), (160, 82, 45)],
            'pattern': 'gradient',
            'emoji': '🐴'
        },
        'КОРОВА': {
            'colors': [(255, 255, 255), (220, 220, 220), (0, 0, 0)],
            'pattern': 'spots',
            'emoji': '🐄'
        },
        'ЛЕВ': {
            'colors': [(255, 215, 0), (255, 165, 0), (255, 140, 0)],
            'pattern': 'radial',
            'emoji': '🦁'
        },
        'ТИГР': {
            'colors': [(255, 140, 0), (255, 69, 0), (0, 0, 0)],
            'pattern': 'stripes',
            'emoji': '🐅'
        },
        'СЛОН': {
            'colors': [(169, 169, 169), (128, 128, 128), (105, 105, 105)],
            'pattern': 'texture',
            'emoji': '🐘'
        },
        'МЕДВЕДЬ': {
            'colors': [(139, 69, 19), (160, 82, 45), (210, 180, 140)],
            'pattern': 'gradient',
            'emoji': '🐻'
        },
        'ВОЛК': {
            'colors': [(105, 105, 105), (128, 128, 128), (169, 169, 169)],
            'pattern': 'texture',
            'emoji': '🐺'
        },
        'ЛИСА': {
            'colors': [(255, 140, 0), (255, 69, 0), (178, 34, 34)],
            'pattern': 'gradient',
            'emoji': '🦊'
        },
        
        # Birds - bright colors
        'ОРЁЛ': {
            'colors': [(139, 69, 19), (160, 82, 45), (205, 133, 63)],
            'pattern': 'feathers',
            'emoji': '🦅'
        },
        'ПОПУГАЙ': {
            'colors': [(50, 205, 50), (34, 139, 34), (255, 215, 0)],
            'pattern': 'feathers',
            'emoji': '🦜'
        },
        'ПИНГВИН': {
            'colors': [(0, 0, 0), (255, 255, 255), (255, 140, 0)],
            'pattern': 'gradient',
            'emoji': '🐧'
        },
        'ФЛАМИНГО': {
            'colors': [(255, 182, 193), (255, 105, 180), (255, 20, 147)],
            'pattern': 'feathers',
            'emoji': '🦩'
        },
        'ПАВЛИН': {
            'colors': [(0, 191, 255), (30, 144, 255), (0, 255, 127)],
            'pattern': 'peacock',
            'emoji': '🦚'
        },
        
        # Sea animals - blue tones
        'КИТ': {
            'colors': [(70, 130, 180), (100, 149, 237), (135, 206, 235)],
            'pattern': 'waves',
            'emoji': '🐋'
        },
        'ДЕЛЬФИН': {
            'colors': [(135, 206, 250), (176, 196, 222), (173, 216, 230)],
            'pattern': 'waves',
            'emoji': '🐬'
        },
        'АКУЛА': {
            'colors': [(105, 105, 105), (128, 128, 128), (70, 130, 180)],
            'pattern': 'waves',
            'emoji': '🦈'
        },
        
        # Insects - colorful
        'БАБОЧКА': {
            'colors': [(255, 182, 193), (255, 160, 122), (255, 218, 185)],
            'pattern': 'butterfly',
            'emoji': '🦋'
        },
        'ПЧЕЛА': {
            'colors': [(255, 215, 0), (255, 165, 0), (0, 0, 0)],
            'pattern': 'stripes',
            'emoji': '🐝'
        },
        
        # Default
        'DEFAULT': {
            'colors': [(144, 238, 144), (60, 179, 113), (34, 139, 34)],
            'pattern': 'gradient',
            'emoji': '🐾'
        }
    }
    
    # Get theme for this animal
    theme = animal_themes.get(animal_name, animal_themes['DEFAULT'])
    colors = theme['colors']
    pattern = theme['pattern']
    emoji = theme['emoji']
    
    # Create base image
    img = Image.new('RGB', size, colors[0])
    draw = ImageDraw.Draw(img)
    
    # Apply pattern based on animal type
    if pattern == 'gradient':
        create_gradient_pattern(draw, size, colors)
    elif pattern == 'stripes':
        create_stripe_pattern(draw, size, colors)
    elif pattern == 'spots':
        create_spot_pattern(draw, size, colors)
    elif pattern == 'radial':
        create_radial_pattern(draw, size, colors)
    elif pattern == 'waves':
        create_wave_pattern(draw, size, colors)
    elif pattern == 'feathers':
        create_feather_pattern(draw, size, colors)
    elif pattern == 'butterfly':
        create_butterfly_pattern(draw, size, colors)
    elif pattern == 'peacock':
        create_peacock_pattern(draw, size, colors)
    else:
        create_texture_pattern(draw, size, colors)
    
    # Add decorative frame
    frame_color = colors[1] if len(colors) > 1 else colors[0]
    draw.rectangle([0, 0, size[0]-1, size[1]-1], outline=frame_color, width=4)
    draw.rectangle([8, 8, size[0]-9, size[1]-9], outline=frame_color, width=2)
    
    # Add animal name with beautiful typography
    add_beautiful_text(draw, animal_name, size, colors)
    
    # Add emoji if possible
    try:
        add_emoji_decoration(img, emoji, size)
    except:
        pass  # Skip emoji if not supported
    
    img.save(filename, 'PNG', quality=95)

def create_gradient_pattern(draw, size, colors):
    """Create a smooth gradient pattern"""
    for y in range(size[1]):
        ratio = y / size[1]
        r = int(colors[0][0] * (1 - ratio) + colors[1][0] * ratio)
        g = int(colors[0][1] * (1 - ratio) + colors[1][1] * ratio)
        b = int(colors[0][2] * (1 - ratio) + colors[1][2] * ratio)
        draw.line([(0, y), (size[0], y)], fill=(r, g, b))

def create_stripe_pattern(draw, size, colors):
    """Create stripe pattern"""
    stripe_width = 20
    for i in range(0, size[0], stripe_width * 2):
        color = colors[1] if (i // stripe_width) % 2 == 0 else colors[2] if len(colors) > 2 else colors[0]
        draw.rectangle([i, 0, i + stripe_width, size[1]], fill=color)

def create_spot_pattern(draw, size, colors):
    """Create spot pattern"""
    # Base gradient
    create_gradient_pattern(draw, size, colors[:2])
    
    # Add spots
    spot_color = colors[2] if len(colors) > 2 else colors[1]
    for _ in range(15):
        x = random.randint(20, size[0] - 20)
        y = random.randint(20, size[1] - 20)
        radius = random.randint(10, 25)
        draw.ellipse([x - radius, y - radius, x + radius, y + radius], fill=spot_color)

def create_radial_pattern(draw, size, colors):
    """Create radial gradient pattern"""
    center_x, center_y = size[0] // 2, size[1] // 2
    max_radius = min(size) // 2
    
    for radius in range(max_radius, 0, -3):
        ratio = radius / max_radius
        r = int(colors[0][0] * ratio + colors[1][0] * (1 - ratio))
        g = int(colors[0][1] * ratio + colors[1][1] * (1 - ratio))
        b = int(colors[0][2] * ratio + colors[1][2] * (1 - ratio))
        
        draw.ellipse([
            center_x - radius, center_y - radius,
            center_x + radius, center_y + radius
        ], fill=(r, g, b))

def create_wave_pattern(draw, size, colors):
    """Create wave pattern for sea animals"""
    # Base gradient
    create_gradient_pattern(draw, size, colors[:2])
    
    # Add waves
    wave_color = colors[2] if len(colors) > 2 else colors[1]
    for y in range(0, size[1], 30):
        points = []
        for x in range(0, size[0], 10):
            wave_y = y + int(10 * math.sin(x * 0.1))
            points.extend([x, wave_y])
        
        if len(points) >= 4:
            draw.line(points, fill=wave_color, width=3)

def create_feather_pattern(draw, size, colors):
    """Create feather pattern for birds"""
    # Base gradient
    create_gradient_pattern(draw, size, colors[:2])
    
    # Add feather-like shapes
    feather_color = colors[2] if len(colors) > 2 else colors[1]
    for i in range(8):
        x = random.randint(30, size[0] - 30)
        y = random.randint(30, size[1] - 30)
        
        # Draw feather shape
        points = [
            x, y - 20,
            x - 10, y,
            x, y + 20,
            x + 10, y
        ]
        draw.polygon(points, fill=feather_color)

def create_butterfly_pattern(draw, size, colors):
    """Create butterfly wing pattern"""
    # Colorful gradient
    for y in range(size[1]):
        for x in range(size[0]):
            ratio_x = x / size[0]
            ratio_y = y / size[1]
            
            r = int(colors[0][0] * (1 - ratio_x) + colors[1][0] * ratio_x)
            g = int(colors[1][1] * (1 - ratio_y) + colors[2][1] * ratio_y)
            b = int(colors[2][2] * ratio_x + colors[0][2] * (1 - ratio_x))
            
            if x % 20 == 0 or y % 20 == 0:  # Grid pattern
                draw.point((x, y), fill=(r, g, b))

def create_peacock_pattern(draw, size, colors):
    """Create peacock feather pattern"""
    # Base gradient
    create_radial_pattern(draw, size, colors[:2])
    
    # Add peacock eye patterns
    eye_color = colors[2] if len(colors) > 2 else colors[1]
    for i in range(3):
        x = random.randint(50, size[0] - 50)
        y = random.randint(50, size[1] - 50)
        
        # Draw eye pattern
        draw.ellipse([x - 25, y - 25, x + 25, y + 25], fill=eye_color)
        draw.ellipse([x - 15, y - 15, x + 15, y + 15], fill=colors[0])
        draw.ellipse([x - 8, y - 8, x + 8, y + 8], fill=eye_color)

def create_texture_pattern(draw, size, colors):
    """Create texture pattern"""
    # Base color
    draw.rectangle([0, 0, size[0], size[1]], fill=colors[0])
    
    # Add texture dots
    for _ in range(100):
        x = random.randint(0, size[0])
        y = random.randint(0, size[1])
        color = random.choice(colors[1:])
        draw.point((x, y), fill=color)

def add_beautiful_text(draw, text, size, colors):
    """Add beautifully styled text"""
    try:
        # Try to load a nice font
        font_paths = [
            "C:/Windows/Fonts/arial.ttf",
            "C:/Windows/Fonts/calibri.ttf",
            "C:/Windows/Fonts/segoeui.ttf",
        ]
        
        font = None
        for font_path in font_paths:
            try:
                font = ImageFont.truetype(font_path, 24)
                break
            except:
                continue
        
        if font is None:
            font = ImageFont.load_default()
            
    except:
        font = ImageFont.load_default()
    
    # Get text dimensions
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    # Center text
    x = (size[0] - text_width) // 2
    y = size[1] - text_height - 20  # Near bottom
    
    # Create text background
    padding = 8
    bg_rect = [
        x - padding, y - padding,
        x + text_width + padding, y + text_height + padding
    ]
    
    # Semi-transparent background
    bg_color = (*colors[0], 180) if len(colors[0]) == 3 else colors[0]
    draw.rectangle(bg_rect, fill=bg_color[:3])
    
    # Add border to text background
    border_color = colors[1] if len(colors) > 1 else (255, 255, 255)
    draw.rectangle(bg_rect, outline=border_color, width=2)
    
    # Draw text with shadow
    shadow_color = (0, 0, 0)
    draw.text((x + 2, y + 2), text, font=font, fill=shadow_color)  # Shadow
    draw.text((x, y), text, font=font, fill=(255, 255, 255))  # Main text

def add_emoji_decoration(img, emoji, size):
    """Add emoji decoration (simplified version)"""
    # This is a placeholder - in a real implementation you'd need emoji font support
    # For now, we'll skip this to keep the script simple and fast
    pass

def create_fast_animal_images():
    """Create beautiful animal images quickly"""
    
    # Read the Russian animal file to get the list
    animals_file = 'data/words/ru/animals_COMPLETE.txt'
    
    if not os.path.exists(animals_file):
        print(f"Error: {animals_file} not found!")
        return
    
    # Create output directory
    output_dir = 'data/images/animals'
    os.makedirs(output_dir, exist_ok=True)
    
    created_count = 0
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
            
            print(f"Creating {line_num}/{total_lines}: {animal_name}...")
            
            # Skip if large image already exists (likely a good photo)
            if os.path.exists(image_path):
                file_size = os.path.getsize(image_path)
                if file_size > 50000:  # 50KB - likely a real photo
                    print(f"  ✓ Keeping existing image: {image_filename} ({file_size/1024:.1f}KB)")
                    skipped_count += 1
                    continue
            
            # Create beautiful artistic image
            create_beautiful_animal_image(animal_name, image_path)
            created_count += 1
            print(f"  ✓ Created beautiful image: {image_filename}")
    
    print(f"\nFast image creation complete!")
    print(f"Created new images: {created_count}")
    print(f"Kept existing images: {skipped_count}")
    print(f"Total processed: {created_count + skipped_count}")

if __name__ == "__main__":
    print("Fast Beautiful Animal Image Creator")
    print("===================================")
    print()
    print("Creating beautiful animal images with artistic patterns...")
    print()
    
    create_fast_animal_images()