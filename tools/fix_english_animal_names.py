#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Fix English animal names in the animal_world.txt file
Convert current names to proper English format
"""

import os

def get_english_translations():
    """Get proper English translations for animal names"""
    return {
        'AARDVARK': 'AARDVARK',
        'AFRICAN LION': 'AFRICAN LION',
        'ALBATROSS': 'ALBATROSS', 
        'ALLIGATOR': 'ALLIGATOR',
        'ALPACA': 'ALPACA',
        'ANTEATER': 'ANTEATER',
        'ANTELOPE': 'ANTELOPE',
        'ASIATIC LION': 'ASIATIC LION',
        'AVOCET': 'AVOCET',
        'AXOLOTL': 'AXOLOTL',
        'BADGER': 'BADGER',
        'BALD EAGLE': 'BALD EAGLE',
        'BARBARY LION': 'BARBARY LION',
        'BARRACUDA': 'BARRACUDA',
        'BASILISK': 'BASILISK',
        'BASS': 'BASS',
        'BAT': 'BAT',
        'BAT EARED FOX': 'BAT-EARED FOX',
        'BEAR': 'BEAR',
        'BISON': 'BISON',
        'BLACK BEAR': 'BLACK BEAR',
        'BLEAK': 'BLEAK',
        'BLUE JAY': 'BLUE JAY',
        'BLUEFIN TUNA': 'BLUEFIN TUNA',
        'BOA CONSTRICTOR': 'BOA CONSTRICTOR',
        'BOBCAT': 'BOBCAT',
        'BULL SHARK': 'BULL SHARK',
        'BUTTERFLY': 'BUTTERFLY',
        'BUZZARD': 'BUZZARD',
        'CAMEL': 'CAMEL',
        'CARIBOU': 'CARIBOU',
        'CASSOWARY': 'CASSOWARY',
        'CAT': 'CAT',
        'CHEETAH': 'CHEETAH',
        'CHICKEN': 'CHICKEN',
        'CHIMPANZEE': 'CHIMPANZEE',
        'CHIPMUNK': 'CHIPMUNK',
        'CLOWNFISH': 'CLOWNFISH',
        'COATI': 'COATI',
        'COCKATOO': 'COCKATOO',
        'CONDOR': 'CONDOR',
        'CORMORANT': 'CORMORANT',
        'COUGAR': 'COUGAR',
        'COW': 'COW',
        'COYOTE': 'COYOTE',
        'CRAB EATING MONGOOSE': 'CRAB-EATING MONGOOSE',
        'CRAB EATING RACCOON': 'CRAB-EATING RACCOON',
        'CROCODILE': 'CROCODILE',
        'CROW': 'CROW',
        'CRUCIAN CARP': 'CRUCIAN CARP',
        'CURLEW': 'CURLEW',
        'DACE': 'DACE',
        'DACHSHUND': 'DACHSHUND',
        'DEER': 'DEER',
        'DINGO': 'DINGO',
        'DINOSAUR': 'DINOSAUR',
        'DOG': 'DOG',
        'DOLPHIN': 'DOLPHIN',
        'DONKEY': 'DONKEY',
        'DOTTEREL': 'DOTTEREL',
        'ECHIDNA': 'ECHIDNA',
        'EEL': 'EEL',
        'ELAND': 'ELAND',
        'ELECTRIC EEL': 'ELECTRIC EEL',
        'ELEPHANT': 'ELEPHANT',
        'ELEPHANT SEAL': 'ELEPHANT SEAL',
        'ELK': 'ELK',
        'EMU': 'EMU',
        'ETHIOPIAN WOLF': 'ETHIOPIAN WOLF',
        'EUROPEAN MINK': 'EUROPEAN MINK',
        'FALCON': 'FALCON',
        'FERRET': 'FERRET',
        'FINCH': 'FINCH',
        'FLY': 'FLY',
        'FOX': 'FOX',
        'GAZELLE': 'GAZELLE',
        'GECKO': 'GECKO',
        'GERBIL': 'GERBIL',
        'GHARIAL': 'GHARIAL',
        'GIANT PANDA': 'GIANT PANDA',
        'GIRAFFE': 'GIRAFFE',
        'GNU': 'GNU',
        'GOLDFINCH': 'GOLDFINCH',
        'GOLDFISH': 'GOLDFISH',
        'GOOSE': 'GOOSE',
        'GORILLA': 'GORILLA',
        'GRAY WOLF': 'GRAY WOLF',
        'GREAT WHITE SHARK': 'GREAT WHITE SHARK',
        'GREENLAND SHARK': 'GREENLAND SHARK',
        'GUANACO': 'GUANACO',
        'GUPPY': 'GUPPY',
        'HAMMERHEAD SHARK': 'HAMMERHEAD SHARK',
        'HAMSTER': 'HAMSTER',
        'HARTEBEEST': 'HARTEBEEST',
        'HATCHETFISH': 'HATCHETFISH',
        'HAWK': 'HAWK',
        'HEDGEHOG': 'HEDGEHOG',
        'HIPPO': 'HIPPO',
        'HORNBILL': 'HORNBILL',
        'HUMMINGBIRD': 'HUMMINGBIRD',
        'HYENA': 'HYENA',
        'IDE': 'IDE',
        'IGUANA': 'IGUANA',
        'IMPALA': 'IMPALA',
        'INDRI': 'INDRI',
        'INSECT': 'INSECT',
        'JACKAL': 'JACKAL',
        'JAGUAR': 'JAGUAR',
        'JAY': 'JAY',
        'JELLYFISH': 'JELLYFISH',
        'JUNGLE CAT': 'JUNGLE CAT',
        'KANGAROO': 'KANGAROO',
        'KOALA': 'KOALA',
        'KOMODO DRAGON': 'KOMODO DRAGON',
        'KOOKABURRA': 'KOOKABURRA',
        'KUDU': 'KUDU',
        'LABRADOODLE': 'LABRADOODLE',
        'LAPWING': 'LAPWING',
        'LEMMING': 'LEMMING',
        'LEMUR': 'LEMUR',
        'LEOPARD': 'LEOPARD',
        'LEOPARD GECKO': 'LEOPARD GECKO',
        'LION': 'LION',
        'LIONFISH': 'LIONFISH',
        'LIZARD': 'LIZARD',
        'LLAMA': 'LLAMA',
        'LOON': 'LOON',
        'LORIS': 'LORIS',
        'LYNX': 'LYNX',
        'LYREBIRD': 'LYREBIRD',
        'MACAW': 'MACAW',
        'MAGPIE': 'MAGPIE',
        'MALLARD': 'MALLARD',
        'MANATEE': 'MANATEE',
        'MANDRILL': 'MANDRILL',
        'MARSH MONGOOSE': 'MARSH MONGOOSE',
        'MARTEN': 'MARTEN',
        'MASTIFF': 'MASTIFF',
        'MEERKAT': 'MEERKAT',
        'MINK': 'MINK',
        'MOLE': 'MOLE',
        'MONGOOSE': 'MONGOOSE',
        'MONGREL': 'MONGREL',
        'MONKEY': 'MONKEY',
        'MOORHEN': 'MOORHEN',
        'MOOSE': 'MOOSE',
        'MOTH': 'MOTH',
        'MUDSKIPPER': 'MUDSKIPPER',
        'MULE': 'MULE',
        'NEWT': 'NEWT',
        'NIGHTINGALE': 'NIGHTINGALE',
        'NUTRIA': 'NUTRIA',
        'OCELOT': 'OCELOT',
        'OKAPI': 'OKAPI',
        'OPOSSUM': 'OPOSSUM',
        'ORANGUTAN': 'ORANGUTAN',
        'ORYX': 'ORYX',
        'OTTER': 'OTTER',
        'OWL': 'OWL',
        'OX': 'OX',
        'PANDA': 'PANDA',
        'PANTHER': 'PANTHER',
        'PARAKEET': 'PARAKEET',
        'PARROT': 'PARROT',
        'PARTRIDGE': 'PARTRIDGE',
        'PEACOCK': 'PEACOCK',
        'PEAFOWL': 'PEAFOWL',
        'PELICAN': 'PELICAN',
        'PENGUIN': 'PENGUIN',
        'PERSIAN CAT': 'PERSIAN CAT',
        'PIGEON': 'PIGEON',
        'PIKA': 'PIKA',
        'PIKE': 'PIKE',
        'PINE MARTEN': 'PINE MARTEN',
        'PINK SALMON': 'PINK SALMON',
        'PINNIPED': 'PINNIPED',
        'PLATYPUS': 'PLATYPUS',
        'POLECAT': 'POLECAT',
        'PONY': 'PONY',
        'PORGY': 'PORGY',
        'PORPOISE': 'PORPOISE',
        'POSSUM': 'POSSUM',
        'PRAIRIE DOG': 'PRAIRIE DOG',
        'PUFFIN': 'PUFFIN',
        'PUMA': 'PUMA',
        'QUAIL': 'QUAIL',
        'QUETZAL': 'QUETZAL',
        'QUOLL': 'QUOLL',
        'RABBIT': 'RABBIT',
        'RACCOON': 'RACCOON',
        'RAT': 'RAT',
        'RATTLESNAKE': 'RATTLESNAKE',
        'RAVEN': 'RAVEN',
        'RED FOX': 'RED FOX',
        'RED PANDA': 'RED PANDA',
        'REINDEER': 'REINDEER',
        'RHINO': 'RHINO',
        'RHINOCEROS': 'RHINOCEROS',
        'ROADRUNNER': 'ROADRUNNER',
        'ROOSTER': 'ROOSTER',
        'SABLE': 'SABLE',
        'SABLE ANTELOPE': 'SABLE ANTELOPE',
        'SANDPIPER': 'SANDPIPER',
        'SCORPION': 'SCORPION',
        'SEA HORSE': 'SEAHORSE',
        'SEA LION': 'SEA LION',
        'SEA TURTLE': 'SEA TURTLE',
        'SEAHORSE': 'SEAHORSE',
        'SERPENT': 'SERPENT',
        'SHARK': 'SHARK',
        'SHEEP': 'SHEEP',
        'SHREW': 'SHREW',
        'SIXGILL SHARK': 'SIXGILL SHARK',
        'SKUNK': 'SKUNK',
        'SMEW': 'SMEW',
        'SNAIL': 'SNAIL',
        'SNIPE': 'SNIPE',
        'SNOW LEOPARD': 'SNOW LEOPARD',
        'SPARROW': 'SPARROW',
        'SPIDER': 'SPIDER',
        'SPIRLIN': 'SPIRLIN',
        'SQUIRREL': 'SQUIRREL',
        'STARFISH': 'STARFISH',
        'STEGOSAURUS': 'STEGOSAURUS',
        'STINGRAY': 'STINGRAY',
        'STOAT': 'STOAT',
        'STORK': 'STORK',
        'STURGEON': 'STURGEON',
        'SUNFISH': 'SUNFISH',
        'SWAN': 'SWAN',
        'SWORDFISH': 'SWORDFISH',
        'SWORDTAIL': 'SWORDTAIL',
        'TAHR': 'TAHR',
        'TAMARIN': 'TAMARIN',
        'TANAGER': 'TANAGER',
        'TAPIR': 'TAPIR',
        'TARANTULA': 'TARANTULA',
        'TARSIER': 'TARSIER',
        'TERN': 'TERN',
        'TETRA': 'TETRA',
        'TIGER': 'TIGER',
        'TIGER SALAMANDER': 'TIGER SALAMANDER',
        'TIGER SHARK': 'TIGER SHARK',
        'TOAD': 'TOAD',
        'TOUCAN': 'TOUCAN',
        'TURKEY': 'TURKEY',
        'TURTLE': 'TURTLE',
        'UMBRELLABIRD': 'UMBRELLABIRD',
        'UNAU': 'UNAU',
        'URCHIN': 'URCHIN',
        'VOLGA ZANDER': 'VOLGA ZANDER',
        'WALLABY': 'WALLABY',
        'WALRUS': 'WALRUS',
        'WARTHOG': 'WARTHOG',
        'WATER BUFFALO': 'WATER BUFFALO',
        'WHALE': 'WHALE',
        'WHALE SHARK': 'WHALE SHARK',
        'WHITE RHINO': 'WHITE RHINO',
        'WHITEFISH': 'WHITEFISH',
        'WILD BOAR': 'WILD BOAR',
        'WILDEBEEST': 'WILDEBEEST',
        'WOLF': 'WOLF',
        'WOLVERINE': 'WOLVERINE',
        'WOMBAT': 'WOMBAT',
        'WOODPECKER': 'WOODPECKER',
        'WORM': 'WORM',
        'WREN': 'WREN',
        'YAK': 'YAK',
        'ZANDER': 'ZANDER',
        'ZEBRA': 'ZEBRA',
        'ZEBRAFISH': 'ZEBRAFISH'
    }

def fix_english_animal_names():
    """Fix the English animal names file"""
    
    print("🔧 Fixing English Animal Names")
    print("=" * 40)
    
    # Read current file
    en_file_path = 'data/words/en/animal_world.txt'
    
    if not os.path.exists(en_file_path):
        print(f"❌ File not found: {en_file_path}")
        return
    
    # Get translations
    translations = get_english_translations()
    
    # Read and process file
    fixed_lines = []
    
    with open(en_file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Parse line: "1 - ANIMAL NAME - ANIMAL-001"
        parts = line.split(' - ')
        if len(parts) != 3:
            fixed_lines.append(line)
            continue
            
        number = parts[0]
        current_name = parts[1]
        code = parts[2]
        
        # Get proper English name
        if current_name in translations:
            proper_name = translations[current_name]
            fixed_line = f"{number} - {proper_name} - {code}"
            fixed_lines.append(fixed_line)
            print(f"  {number:3s}. {current_name} → {proper_name}")
        else:
            fixed_lines.append(line)
            print(f"  {number:3s}. {current_name} (no change)")
    
    # Write fixed file
    with open(en_file_path, 'w', encoding='utf-8') as f:
        for line in fixed_lines:
            f.write(line + '\n')
    
    print(f"\n✅ Fixed English animal names file: {en_file_path}")
    print(f"Total animals: {len(fixed_lines)}")

if __name__ == "__main__":
    fix_english_animal_names() 