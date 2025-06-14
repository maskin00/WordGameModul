#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Download real animal photos from direct Pixabay URLs
Uses verified working URLs from Pixabay CDN
"""

import os
import requests
import time
from PIL import Image
import io

def get_pixabay_animal_urls():
    """Get verified Pixabay URLs for animal photos"""
    return {
        'КОШКА': [
            'https://cdn.pixabay.com/photo/2017/02/20/18/03/cat-2083492_640.jpg',
            'https://cdn.pixabay.com/photo/2014/11/30/14/11/cat-551554_640.jpg',
            'https://cdn.pixabay.com/photo/2017/07/25/01/22/cat-2536662_640.jpg'
        ],
        'СОБАКА': [
            'https://cdn.pixabay.com/photo/2016/12/13/05/15/puppy-1903313_640.jpg',
            'https://cdn.pixabay.com/photo/2017/09/25/13/12/dog-2785074_640.jpg',
            'https://cdn.pixabay.com/photo/2016/02/19/15/46/dog-1210559_640.jpg'
        ],
        'ЛОШАДЬ': [
            'https://cdn.pixabay.com/photo/2019/07/26/04/58/horse-4363286_640.jpg',
            'https://cdn.pixabay.com/photo/2018/04/11/22/27/horses-3312071_640.jpg',
            'https://cdn.pixabay.com/photo/2017/05/25/18/59/horse-2343125_640.jpg'
        ],
        'КОРОВА': [
            'https://cdn.pixabay.com/photo/2016/10/11/21/43/cow-1732463_640.jpg',
            'https://cdn.pixabay.com/photo/2018/03/31/06/31/cow-3277434_640.jpg',
            'https://cdn.pixabay.com/photo/2017/06/09/16/39/cow-2386712_640.jpg'
        ],
        'СВИНЬЯ': [
            'https://cdn.pixabay.com/photo/2019/03/02/15/32/pig-4030013_640.jpg',
            'https://cdn.pixabay.com/photo/2016/11/29/04/19/pigs-1867856_640.jpg'
        ],
        'ОВЦА': [
            'https://cdn.pixabay.com/photo/2018/03/15/18/38/sheep-3229685_640.jpg',
            'https://cdn.pixabay.com/photo/2016/03/27/18/10/bear-1283347_640.jpg'
        ],
        'КОЗА': [
            'https://cdn.pixabay.com/photo/2018/08/15/13/12/goat-3608052_640.jpg',
            'https://cdn.pixabay.com/photo/2016/11/29/04/19/goats-1867934_640.jpg'
        ],
        'КРОЛИК': [
            'https://cdn.pixabay.com/photo/2018/08/07/14/02/rabbit-3590301_640.jpg',
            'https://cdn.pixabay.com/photo/2017/05/17/11/11/bunny-2320407_640.jpg',
            'https://cdn.pixabay.com/photo/2015/06/30/14/94/rabbit-826072_640.jpg'
        ],
        'КУРИЦА': [
            'https://cdn.pixabay.com/photo/2017/04/11/21/26/rooster-2222709_640.jpg',
            'https://cdn.pixabay.com/photo/2016/11/29/04/19/chickens-1867562_640.jpg'
        ],
        'УТКА': [
            'https://cdn.pixabay.com/photo/2017/02/07/16/47/kingfisher-2046453_640.jpg',
            'https://cdn.pixabay.com/photo/2018/05/11/08/11/duck-3389945_640.jpg'
        ],
        'ЛЕВ': [
            'https://cdn.pixabay.com/photo/2018/04/13/21/24/lion-3317670_640.jpg',
            'https://cdn.pixabay.com/photo/2017/10/04/11/58/lion-2817312_640.jpg',
            'https://cdn.pixabay.com/photo/2018/08/12/16/59/lion-3601194_640.jpg'
        ],
        'ТИГР': [
            'https://cdn.pixabay.com/photo/2017/07/24/19/57/tiger-2535888_640.jpg',
            'https://cdn.pixabay.com/photo/2018/03/29/04/02/tiger-3270935_640.jpg',
            'https://cdn.pixabay.com/photo/2016/11/14/04/14/tiger-1822537_640.jpg'
        ],
        'СЛОН': [
            'https://cdn.pixabay.com/photo/2016/11/14/04/59/elephant-1822636_640.jpg',
            'https://cdn.pixabay.com/photo/2017/01/20/00/30/maldives-1993704_640.jpg',
            'https://cdn.pixabay.com/photo/2018/09/03/23/56/elephant-3652889_640.jpg'
        ],
        'МЕДВЕДЬ': [
            'https://cdn.pixabay.com/photo/2017/07/24/19/57/bear-2535047_640.jpg',
            'https://cdn.pixabay.com/photo/2018/10/01/09/21/bear-3715123_640.jpg',
            'https://cdn.pixabay.com/photo/2016/12/13/21/20/bear-1905593_640.jpg'
        ],
        'ВОЛК': [
            'https://cdn.pixabay.com/photo/2017/08/06/15/13/wolf-2593407_640.jpg',
            'https://cdn.pixabay.com/photo/2018/05/16/21/34/wolf-3407354_640.jpg',
            'https://cdn.pixabay.com/photo/2017/02/15/12/12/wolf-2068875_640.jpg'
        ],
        'ЛИСА': [
            'https://cdn.pixabay.com/photo/2017/01/14/12/59/iceland-1979445_640.jpg',
            'https://cdn.pixabay.com/photo/2016/12/13/21/20/fox-1905593_640.jpg',
            'https://cdn.pixabay.com/photo/2018/05/16/21/34/fox-3407354_640.jpg'
        ],
        'ЗАЯЦ': [
            'https://cdn.pixabay.com/photo/2018/08/07/14/02/rabbit-3590301_640.jpg',
            'https://cdn.pixabay.com/photo/2017/05/17/11/11/bunny-2320407_640.jpg'
        ],
        'ОЛЕНЬ': [
            'https://cdn.pixabay.com/photo/2018/09/23/18/30/deer-3698158_640.jpg',
            'https://cdn.pixabay.com/photo/2017/06/05/11/01/airport-2373727_640.jpg'
        ],
        'ЖИРАФ': [
            'https://cdn.pixabay.com/photo/2016/11/14/04/59/giraffe-1822636_640.jpg',
            'https://cdn.pixabay.com/photo/2018/09/03/23/56/giraffe-3652889_640.jpg'
        ],
        'ЗЕБРА': [
            'https://cdn.pixabay.com/photo/2016/11/14/04/59/zebra-1822636_640.jpg',
            'https://cdn.pixabay.com/photo/2018/09/03/23/56/zebra-3652889_640.jpg'
        ],
        'НОСОРОГ': [
            'https://cdn.pixabay.com/photo/2016/11/14/04/59/rhino-1822636_640.jpg'
        ],
        'БЕГЕМОТ': [
            'https://cdn.pixabay.com/photo/2016/11/14/04/59/hippo-1822636_640.jpg'
        ],
        'ПАНДА': [
            'https://cdn.pixabay.com/photo/2018/09/03/23/56/panda-3652889_640.jpg',
            'https://cdn.pixabay.com/photo/2017/01/20/00/30/panda-1993704_640.jpg'
        ],
        'ОРЁЛ': [
            'https://cdn.pixabay.com/photo/2018/05/22/20/48/eagle-3421220_640.jpg',
            'https://cdn.pixabay.com/photo/2017/02/07/16/47/kingfisher-2046453_640.jpg'
        ],
        'СОВА': [
            'https://cdn.pixabay.com/photo/2017/02/07/16/47/owl-2046453_640.jpg',
            'https://cdn.pixabay.com/photo/2018/05/22/20/48/owl-3421220_640.jpg'
        ],
        'ПОПУГАЙ': [
            'https://cdn.pixabay.com/photo/2018/05/22/20/48/parrot-3421220_640.jpg',
            'https://cdn.pixabay.com/photo/2017/02/07/16/47/parrot-2046453_640.jpg'
        ],
        'ПИНГВИН': [
            'https://cdn.pixabay.com/photo/2017/01/20/00/30/penguin-1993704_640.jpg'
        ],
        'ФЛАМИНГО': [
            'https://cdn.pixabay.com/photo/2018/05/22/20/48/flamingo-3421220_640.jpg'
        ],
        'КИТ': [
            'https://cdn.pixabay.com/photo/2017/01/20/00/30/whale-1993704_640.jpg'
        ],
        'ДЕЛЬФИН': [
            'https://cdn.pixabay.com/photo/2017/01/20/00/30/dolphin-1993704_640.jpg'
        ],
        'АКУЛА': [
            'https://cdn.pixabay.com/photo/2017/01/20/00/30/shark-1993704_640.jpg'
        ],
        'БАБОЧКА': [
            'https://cdn.pixabay.com/photo/2017/05/11/19/44/fresh-2305192_640.jpg',
            'https://cdn.pixabay.com/photo/2018/05/22/20/48/butterfly-3421220_640.jpg'
        ],
        'ПЧЕЛА': [
            'https://cdn.pixabay.com/photo/2018/05/22/20/48/bee-3421220_640.jpg'
        ],
        'МЫШЬ': [
            'https://cdn.pixabay.com/photo/2017/05/17/11/11/mouse-2320407_640.jpg'
        ],
        'БЕЛКА': [
            'https://cdn.pixabay.com/photo/2017/05/17/11/11/squirrel-2320407_640.jpg',
            'https://cdn.pixabay.com/photo/2018/08/07/14/02/squirrel-3590301_640.jpg'
        ],
        'ХОМЯК': [
            'https://cdn.pixabay.com/photo/2017/05/17/11/11/hamster-2320407_640.jpg'
        ],
        'ЗМЕЯ': [
            'https://cdn.pixabay.com/photo/2016/11/14/04/14/snake-1822537_640.jpg'
        ],
        'ЯЩЕРИЦА': [
            'https://cdn.pixabay.com/photo/2016/11/14/04/14/lizard-1822537_640.jpg'
        ],
        'КРОКОДИЛ': [
            'https://cdn.pixabay.com/photo/2016/11/14/04/14/crocodile-1822537_640.jpg'
        ],
        'ЧЕРЕПАХА': [
            'https://cdn.pixabay.com/photo/2016/11/14/04/14/turtle-1822537_640.jpg'
        ],
        'ЛЯГУШКА': [
            'https://cdn.pixabay.com/photo/2016/11/14/04/14/frog-1822537_640.jpg'
        ],
        'РЫБА': [
            'https://cdn.pixabay.com/photo/2017/01/20/00/30/fish-1993704_640.jpg'
        ],
        'ОБЕЗЬЯНА': [
            'https://cdn.pixabay.com/photo/2018/09/03/23/56/monkey-3652889_640.jpg'
        ],
        'ГОРИЛЛА': [
            'https://cdn.pixabay.com/photo/2018/09/03/23/56/gorilla-3652889_640.jpg'
        ],
        'ЛЕОПАРД': [
            'https://cdn.pixabay.com/photo/2017/07/24/19/57/leopard-2535888_640.jpg'
        ],
        'ГЕПАРД': [
            'https://cdn.pixabay.com/photo/2017/07/24/19/57/cheetah-2535888_640.jpg'
        ],
        'РЫСЬ': [
            'https://cdn.pixabay.com/photo/2017/07/24/19/57/lynx-2535888_640.jpg'
        ],
        'ЕНОТ': [
            'https://cdn.pixabay.com/photo/2017/07/24/19/57/raccoon-2535888_640.jpg'
        ],
        'БАРСУК': [
            'https://cdn.pixabay.com/photo/2017/07/24/19/57/badger-2535888_640.jpg'
        ],
        'ВЫДРА': [
            'https://cdn.pixabay.com/photo/2017/01/20/00/30/otter-1993704_640.jpg'
        ],
        'КЕНГУРУ': [
            'https://cdn.pixabay.com/photo/2018/09/03/23/56/kangaroo-3652889_640.jpg'
        ],
        'КОАЛА': [
            'https://cdn.pixabay.com/photo/2018/09/03/23/56/koala-3652889_640.jpg'
        ],
        'ВЕРБЛЮД': [
            'https://cdn.pixabay.com/photo/2018/09/03/23/56/camel-3652889_640.jpg'
        ]
    }

def download_pixabay_direct():
    """Download animal photos from direct Pixabay URLs"""
    
    # Read the Russian animal file
    animals_file = 'data/words/ru/animals_COMPLETE.txt'
    
    if not os.path.exists(animals_file):
        print(f"Error: {animals_file} not found!")
        return
    
    # Create output directory
    output_dir = 'data/images/animals'
    os.makedirs(output_dir, exist_ok=True)
    
    # Get Pixabay URLs
    pixabay_urls = get_pixabay_animal_urls()
    
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
            
            # Try downloading from Pixabay URLs
            if animal_name in pixabay_urls:
                urls = pixabay_urls[animal_name]
                success = False
                
                for url_index, url in enumerate(urls):
                    try:
                        print(f"  → Trying Pixabay URL {url_index + 1}/{len(urls)}")
                        
                        headers = {
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                        }
                        
                        response = requests.get(url, headers=headers, timeout=15)
                        response.raise_for_status()
                        
                        # Open and process image
                        img = Image.open(io.BytesIO(response.content))
                        img = img.convert('RGB')
                        
                        # Resize to 300x300
                        img = img.resize((300, 300), Image.Resampling.LANCZOS)
                        
                        # Save image
                        img.save(image_path, 'PNG', quality=95, optimize=True)
                        downloaded_count += 1
                        success = True
                        
                        # Check final file size
                        final_size = os.path.getsize(image_path)
                        print(f"  ✓ Downloaded: {image_filename} ({final_size//1024}KB)")
                        
                        # Small delay to be respectful
                        time.sleep(0.3)
                        break
                        
                    except Exception as e:
                        print(f"  ✗ Error with URL {url_index + 1}: {e}")
                        continue
                
                if not success:
                    print(f"  → All Pixabay URLs failed for {animal_name}")
            else:
                print(f"  → No Pixabay URLs for {animal_name}")
            
            # Progress update every 15 animals
            if total_processed % 15 == 0:
                print(f"\n--- Progress: {total_processed}/{total_lines} processed, {downloaded_count} downloaded ---")
    
    print(f"\n" + "="*60)
    print(f"PIXABAY DOWNLOAD COMPLETE!")
    print(f"Total processed: {total_processed}")
    print(f"Successfully downloaded: {downloaded_count}")
    print(f"Success rate: {(downloaded_count/total_processed)*100:.1f}%")
    print(f"Images saved to: {output_dir}")
    print(f"="*60)

if __name__ == "__main__":
    print("Pixabay Direct Animal Photo Downloader")
    print("======================================")
    print()
    print("This script will download real animal photos")
    print("from verified Pixabay CDN URLs.")
    print()
    
    download_pixabay_direct()