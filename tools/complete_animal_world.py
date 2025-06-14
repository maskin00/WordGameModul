#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json

def create_animal_translations():
    """Create Spanish and French translations for animals"""
    
    # Animal translations dictionary
    translations = {
        "aardvark": {"es": "oso hormiguero", "fr": "oryctérope"},
        "african_lion": {"es": "león africano", "fr": "lion d'Afrique"},
        "albatross": {"es": "albatros", "fr": "albatros"},
        "alligator": {"es": "caimán", "fr": "alligator"},
        "alpaca": {"es": "alpaca", "fr": "alpaga"},
        "angelfish": {"es": "pez ángel", "fr": "poisson-ange"},
        "ant": {"es": "hormiga", "fr": "fourmi"},
        "anteater": {"es": "oso hormiguero", "fr": "fourmilier"},
        "antelope": {"es": "antílope", "fr": "antilope"},
        "arctic_fox": {"es": "zorro ártico", "fr": "renard arctique"},
        "armadillo": {"es": "armadillo", "fr": "tatou"},
        "baboon": {"es": "babuino", "fr": "babouin"},
        "badger": {"es": "tejón", "fr": "blaireau"},
        "bald_eagle": {"es": "águila calva", "fr": "pygargue à tête blanche"},
        "bat": {"es": "murciélago", "fr": "chauve-souris"},
        "bear": {"es": "oso", "fr": "ours"},
        "beaver": {"es": "castor", "fr": "castor"},
        "bee": {"es": "abeja", "fr": "abeille"},
        "beetle": {"es": "escarabajo", "fr": "scarabée"},
        "bison": {"es": "bisonte", "fr": "bison"},
        "butterfly": {"es": "mariposa", "fr": "papillon"},
        "camel": {"es": "camello", "fr": "chameau"},
        "cat": {"es": "gato", "fr": "chat"},
        "cheetah": {"es": "guepardo", "fr": "guépard"},
        "chimpanzee": {"es": "chimpancé", "fr": "chimpanzé"},
        "cobra": {"es": "cobra", "fr": "cobra"},
        "cow": {"es": "vaca", "fr": "vache"},
        "coyote": {"es": "coyote", "fr": "coyote"},
        "crab": {"es": "cangrejo", "fr": "crabe"},
        "crocodile": {"es": "cocodrilo", "fr": "crocodile"},
        "deer": {"es": "ciervo", "fr": "cerf"},
        "dog": {"es": "perro", "fr": "chien"},
        "dolphin": {"es": "delfín", "fr": "dauphin"},
        "donkey": {"es": "burro", "fr": "âne"},
        "dragonfly": {"es": "libélula", "fr": "libellule"},
        "duck": {"es": "pato", "fr": "canard"},
        "eagle": {"es": "águila", "fr": "aigle"},
        "elephant": {"es": "elefante", "fr": "éléphant"},
        "elk": {"es": "alce", "fr": "élan"},
        "falcon": {"es": "halcón", "fr": "faucon"},
        "ferret": {"es": "hurón", "fr": "furet"},
        "fish": {"es": "pez", "fr": "poisson"},
        "flamingo": {"es": "flamenco", "fr": "flamant rose"},
        "fox": {"es": "zorro", "fr": "renard"},
        "frog": {"es": "rana", "fr": "grenouille"},
        "giraffe": {"es": "jirafa", "fr": "girafe"},
        "goat": {"es": "cabra", "fr": "chèvre"},
        "gorilla": {"es": "gorila", "fr": "gorille"},
        "hamster": {"es": "hámster", "fr": "hamster"},
        "hawk": {"es": "halcón", "fr": "faucon"},
        "hedgehog": {"es": "erizo", "fr": "hérisson"},
        "hippopotamus": {"es": "hipopótamo", "fr": "hippopotame"},
        "horse": {"es": "caballo", "fr": "cheval"},
        "hummingbird": {"es": "colibrí", "fr": "colibri"},
        "hyena": {"es": "hiena", "fr": "hyène"},
        "iguana": {"es": "iguana", "fr": "iguane"},
        "jaguar": {"es": "jaguar", "fr": "jaguar"},
        "jellyfish": {"es": "medusa", "fr": "méduse"},
        "kangaroo": {"es": "canguro", "fr": "kangourou"},
        "koala": {"es": "koala", "fr": "koala"},
        "ladybug": {"es": "mariquita", "fr": "coccinelle"},
        "leopard": {"es": "leopardo", "fr": "léopard"},
        "lion": {"es": "león", "fr": "lion"},
        "lizard": {"es": "lagarto", "fr": "lézard"},
        "llama": {"es": "llama", "fr": "lama"},
        "lobster": {"es": "langosta", "fr": "homard"},
        "monkey": {"es": "mono", "fr": "singe"},
        "moose": {"es": "alce", "fr": "orignal"},
        "mouse": {"es": "ratón", "fr": "souris"},
        "octopus": {"es": "pulpo", "fr": "pieuvre"},
        "otter": {"es": "nutria", "fr": "loutre"},
        "owl": {"es": "búho", "fr": "hibou"},
        "panda": {"es": "panda", "fr": "panda"},
        "parrot": {"es": "loro", "fr": "perroquet"},
        "peacock": {"es": "pavo real", "fr": "paon"},
        "penguin": {"es": "pingüino", "fr": "pingouin"},
        "pig": {"es": "cerdo", "fr": "cochon"},
        "polar_bear": {"es": "oso polar", "fr": "ours polaire"},
        "rabbit": {"es": "conejo", "fr": "lapin"},
        "raccoon": {"es": "mapache", "fr": "raton laveur"},
        "rhinoceros": {"es": "rinoceronte", "fr": "rhinocéros"},
        "seal": {"es": "foca", "fr": "phoque"},
        "shark": {"es": "tiburón", "fr": "requin"},
        "sheep": {"es": "oveja", "fr": "mouton"},
        "snake": {"es": "serpiente", "fr": "serpent"},
        "snow_leopard": {"es": "leopardo de las nieves", "fr": "léopard des neiges"},
        "spider": {"es": "araña", "fr": "araignée"},
        "squirrel": {"es": "ardilla", "fr": "écureuil"},
        "tiger": {"es": "tigre", "fr": "tigre"},
        "turtle": {"es": "tortuga", "fr": "tortue"},
        "whale": {"es": "ballena", "fr": "baleine"},
        "wolf": {"es": "lobo", "fr": "loup"},
        "zebra": {"es": "cebra", "fr": "zèbre"}
    }
    
    return translations

def complete_animal_world():
    """Complete the animal world category setup"""
    
    print("🦁 COMPLETING ANIMAL WORLD CATEGORY")
    print("=" * 40)
    
    # Read English animal list
    with open('data/words/en/animal_world.txt', 'r', encoding='utf-8') as f:
        en_lines = f.readlines()
    
    # Extract animal names from English file
    animals = []
    for line in en_lines:
        parts = line.strip().split(' - ')
        if len(parts) >= 2:
            animal_name = parts[1].lower()
            animals.append(animal_name)
    
    print(f"📝 Found {len(animals)} animals from English file")
    
    # Get translations
    translations = create_animal_translations()
    
    # Create Spanish translations
    print("🇪🇸 Creating Spanish translations...")
    os.makedirs('data/words/es', exist_ok=True)
    with open('data/words/es/animal_world.txt', 'w', encoding='utf-8') as f:
        for i, animal in enumerate(animals, 1):
            spanish = translations.get(animal, {}).get('es', animal.replace('_', ' '))
            image_file = f"{i:03d}-{animal}.png"
            f.write(f"{i} - {spanish.upper()} - {image_file}\n")
    
    # Create French translations
    print("🇫🇷 Creating French translations...")
    os.makedirs('data/words/fr', exist_ok=True)
    with open('data/words/fr/animal_world.txt', 'w', encoding='utf-8') as f:
        for i, animal in enumerate(animals, 1):
            french = translations.get(animal, {}).get('fr', animal.replace('_', ' '))
            image_file = f"{i:03d}-{animal}.png"
            f.write(f"{i} - {french.upper()} - {image_file}\n")
    
    # Create categories.json
    print("📋 Creating categories.json...")
    categories = [
        {
            "id": "animal_world",
            "name": {
                "en": "Animal World",
                "ru": "Животный мир", 
                "es": "Mundo Animal",
                "fr": "Monde Animal"
            },
            "description": {
                "en": "Discover amazing animals from around the world",
                "ru": "Откройте для себя удивительных животных со всего мира",
                "es": "Descubre animales increíbles de todo el mundo", 
                "fr": "Découvrez des animaux incroyables du monde entier"
            },
            "icon": "🦁",
            "difficulty": "medium",
            "wordCount": len(animals)
        }
    ]
    
    with open('data/categories.json', 'w', encoding='utf-8') as f:
        json.dump(categories, f, ensure_ascii=False, indent=2)
    
    # Create image mappings
    print("🖼️ Creating image mappings...")
    os.makedirs('data/image_mappings', exist_ok=True)
    
    for lang in ['en', 'ru', 'es', 'fr']:
        mappings = {}
        for i, animal in enumerate(animals, 1):
            image_file = f"{i:03d}-{animal}.png"
            mappings[str(i)] = f"animal_world/{image_file}"
        
        with open(f'data/image_mappings/animal_world_{lang}.json', 'w', encoding='utf-8') as f:
            json.dump(mappings, f, ensure_ascii=False, indent=2)
    
    print("\n✅ ANIMAL WORLD CATEGORY COMPLETED!")
    print(f"   📁 Word files: 4 languages ({len(animals)} animals each)")
    print(f"   🖼️ Images: {len(animals)} files")
    print(f"   📋 Categories: 1 definition")
    print(f"   🗺️ Mappings: 4 language mappings")

if __name__ == "__main__":
    complete_animal_world() 