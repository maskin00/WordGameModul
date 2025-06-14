#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script to create realistic animal images for the word game
Downloads images from free sources and creates high-quality animal photos
"""

import os
import requests
import time
from PIL import Image, ImageDraw, ImageFont
import io
import urllib.parse

def download_image_from_url(url, filename, size=(300, 300)):
    """Download and resize image from URL"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Open and resize image
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
        print(f"Error downloading image from {url}: {e}")
        return False

def create_gradient_image(animal_name, filename, size=(300, 300)):
    """Create a beautiful gradient image with animal name"""
    
    # Color schemes for different animal types
    color_schemes = {
        # Mammals
        'КОШКА': [(255, 182, 193), (255, 105, 180)],  # Pink
        'СОБАКА': [(135, 206, 250), (70, 130, 180)],   # Blue
        'ЛОШАДЬ': [(210, 180, 140), (139, 69, 19)],    # Brown
        'КОРОВА': [(255, 255, 255), (105, 105, 105)],  # Gray
        'ЛЕВ': [(255, 215, 0), (255, 140, 0)],         # Gold
        'ТИГР': [(255, 140, 0), (255, 69, 0)],         # Orange
        'СЛОН': [(169, 169, 169), (105, 105, 105)],    # Gray
        'МЕДВЕДЬ': [(139, 69, 19), (101, 67, 33)],     # Brown
        
        # Birds
        'ОРЁЛ': [(139, 69, 19), (160, 82, 45)],        # Brown
        'ПОПУГАЙ': [(50, 205, 50), (34, 139, 34)],     # Green
        'ПИНГВИН': [(0, 0, 0), (105, 105, 105)],       # Black/Gray
        'ФЛАМИНГО': [(255, 182, 193), (255, 20, 147)], # Pink
        
        # Sea animals
        'КИТ': [(70, 130, 180), (25, 25, 112)],        # Blue
        'ДЕЛЬФИН': [(135, 206, 250), (70, 130, 180)],  # Light Blue
        'АКУЛА': [(105, 105, 105), (47, 79, 79)],      # Gray
        
        # Default
        'DEFAULT': [(144, 238, 144), (34, 139, 34)]     # Green
    }
    
    # Get color scheme
    colors = color_schemes.get(animal_name, color_schemes['DEFAULT'])
    
    # Create gradient image
    img = Image.new('RGB', size, colors[0])
    draw = ImageDraw.Draw(img)
    
    # Create vertical gradient
    for y in range(size[1]):
        ratio = y / size[1]
        r = int(colors[0][0] * (1 - ratio) + colors[1][0] * ratio)
        g = int(colors[0][1] * (1 - ratio) + colors[1][1] * ratio)
        b = int(colors[0][2] * (1 - ratio) + colors[1][2] * ratio)
        draw.line([(0, y), (size[0], y)], fill=(r, g, b))
    
    # Add animal name with nice styling
    try:
        # Try to use a nice font
        font_large = ImageFont.truetype("arial.ttf", 32)
        font_small = ImageFont.truetype("arial.ttf", 16)
    except:
        font_large = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # Get text size and center it
    bbox = draw.textbbox((0, 0), animal_name, font=font_large)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = (size[0] - text_width) // 2
    y = (size[1] - text_height) // 2
    
    # Draw text with multiple shadows for depth
    shadow_offsets = [(3, 3), (2, 2), (1, 1)]
    shadow_colors = [(0, 0, 0, 180), (0, 0, 0, 120), (0, 0, 0, 60)]
    
    for offset, shadow_color in zip(shadow_offsets, shadow_colors):
        draw.text((x + offset[0], y + offset[1]), animal_name, 
                 font=font_large, fill=shadow_color[:3])
    
    # Draw main text
    draw.text((x, y), animal_name, font=font_large, fill=(255, 255, 255))
    
    # Add decorative border
    border_color = (255, 255, 255, 100)
    draw.rectangle([(5, 5), (size[0]-5, size[1]-5)], outline=border_color[:3], width=2)
    
    img.save(filename, 'PNG')

def get_free_animal_image_urls():
    """Get URLs for free animal images"""
    # These are some free animal images from various sources
    # In a real implementation, you would have a larger database
    
    animal_urls = {
        'КОШКА': 'https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?w=300&h=300&fit=crop',
        'СОБАКА': 'https://images.unsplash.com/photo-1552053831-71594a27632d?w=300&h=300&fit=crop',
        'ЛОШАДЬ': 'https://images.unsplash.com/photo-1553284965-83fd3e82fa5a?w=300&h=300&fit=crop',
        'ЛЕВ': 'https://images.unsplash.com/photo-1546182990-dffeafbe841d?w=300&h=300&fit=crop',
        'ТИГР': 'https://images.unsplash.com/photo-1605979399824-6d3d60c2d8d2?w=300&h=300&fit=crop',
        'СЛОН': 'https://images.unsplash.com/photo-1564760055775-d63b17a55c44?w=300&h=300&fit=crop',
        'ЖИРАФ': 'https://images.unsplash.com/photo-1547721064-da6cfb341d50?w=300&h=300&fit=crop',
        'ЗЕБРА': 'https://images.unsplash.com/photo-1583212292454-1fe6229603b7?w=300&h=300&fit=crop',
        'ПАНДА': 'https://images.unsplash.com/photo-1564349683136-77e08dba1ef7?w=300&h=300&fit=crop',
        'ПИНГВИН': 'https://images.unsplash.com/photo-1551986782-d0169b3f8fa7?w=300&h=300&fit=crop',
    }
    
    return animal_urls

def create_realistic_animal_images():
    """Create realistic animal images"""
    
    # Read the Russian animal file to get the list
    animals_file = 'data/words/ru/animals_COMPLETE.txt'
    
    if not os.path.exists(animals_file):
        print(f"Error: {animals_file} not found!")
        return
    
    # Create output directory
    output_dir = 'data/images/animals'
    os.makedirs(output_dir, exist_ok=True)
    
    # Get free image URLs
    animal_urls = get_free_animal_image_urls()
    
    downloaded_count = 0
    gradient_count = 0
    
    with open(animals_file, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
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
            
            print(f"Creating image {line_num}/207: {animal_name}...")
            
            # Try to download real image first
            success = False
            if animal_name in animal_urls:
                if download_image_from_url(animal_urls[animal_name], image_path):
                    success = True
                    downloaded_count += 1
                    print(f"✓ Downloaded real photo: {image_filename}")
            
            # If no real image available, create gradient image
            if not success:
                create_gradient_image(animal_name, image_path)
                gradient_count += 1
                print(f"✓ Created gradient image: {image_filename}")
            
            # Small delay to be respectful
            time.sleep(0.1)
    
    print(f"\nImage creation complete!")
    print(f"Downloaded real photos: {downloaded_count}")
    print(f"Created gradient images: {gradient_count}")
    print(f"Total images: {downloaded_count + gradient_count}")

if __name__ == "__main__":
    print("Realistic Animal Image Creator")
    print("=============================")
    print()
    print("Creating beautiful animal images...")
    print()
    
    create_realistic_animal_images() 