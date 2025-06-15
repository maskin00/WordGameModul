#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import shutil
from PIL import Image, ImageDraw, ImageFont

def create_missing_images():
    """Create missing dinosaur images and fix file extensions"""
    
    print("🦕 FIXING DINOSAUR IMAGES")
    print("=" * 40)
    
    # Read the Russian dinosaur file to get all required images
    with open('data/words/ru/dinosaurs_COMPLETE.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    required_images = []
    for line in lines:
        parts = line.strip().split(' - ')
        if len(parts) >= 3:
            image_file = parts[2]
            required_images.append(image_file)
    
    print(f"📝 Found {len(required_images)} required images")
    
    # Check existing images
    existing_images = os.listdir('data/images/dinosaurs')
    print(f"📁 Found {len(existing_images)} existing images")
    
    missing_images = []
    for required in required_images:
        if required not in existing_images:
            missing_images.append(required)
    
    print(f"❌ Missing {len(missing_images)} images")
    
    # Create missing images
    if missing_images:
        print("\n🎨 Creating missing images...")
        
        for missing in missing_images:
            # Extract dinosaur name from filename
            name_part = missing.replace('.jpg', '').split('-', 1)[1] if '-' in missing else missing.replace('.jpg', '')
            name_display = name_part.replace('_', ' ').title()
            
            # Create a simple placeholder image
            img = Image.new('RGB', (400, 300), color='lightgray')
            draw = ImageDraw.Draw(img)
            
            try:
                # Try to use a default font
                font = ImageFont.truetype("arial.ttf", 24)
            except:
                font = ImageFont.load_default()
            
            # Draw dinosaur name
            text = f"🦕 {name_display}"
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            x = (400 - text_width) // 2
            y = (300 - text_height) // 2
            
            draw.text((x, y), text, fill='black', font=font)
            
            # Save the image
            img_path = f'data/images/dinosaurs/{missing}'
            img.save(img_path)
            print(f"   ✅ Created: {missing}")
    
    print(f"\n✅ DINOSAUR IMAGES FIXED!")
    print(f"   📁 Total images: {len(os.listdir('data/images/dinosaurs'))}")

if __name__ == "__main__":
    create_missing_images() 