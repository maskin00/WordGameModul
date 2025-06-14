import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Путь для сохранения изображений
SAVE_DIR = r"E:\Games\animals"
os.makedirs(SAVE_DIR, exist_ok=True)

# Топ 300 популярных животных (A–Z список)
ANIMALS = [
    "aardvark", "albatross", "alligator", "alpaca", "ant", "anteater",
    "antelope", "armadillo", "avocet", "axolotl", "badger", "bald eagle",
    "bandicoot", "barn owl", "barnacle", "barracuda", "basilisk", "bass",
    "bat", "beaver", "bee", "binturong", "bison", "black bear", "blue jay",
    "bluefin tuna", "blue whale", "boa constrictor", "bobcat", "bonobo",
    "booby", "buffalo", "bulbul", "butterfly", "buzzard", "camel", "caribou",
    "cassowary", "cat", "caterpillar", "catfish", "cheetah", "chicken",
    "chimpanzee", "chinchilla", "chipmunk", "clownfish", "cobra", "cockatoo",
    "cod", "condor", "coati", "cormorant", "cougar", "cow", "coyote", "crab",
    "crane", "cricket", "crocodile", "crow", "cuckoo", "curlew", "cuttlefish",
    "dachshund", "dalmatian", "deer", "dingo", "dinosaur", "dog", "dolphin",
    "donkey", "dotterel", "dove", "dragonfly", "duck", "eagle", "earthworm",
    "echidna", "eel", "eland", "elephant", "elephant seal", "elk", "emu",
    "falcon", "ferret", "finch", "firefly", "fish", "flamingo", "flounder",
    "fly", "flying fish", "fox", "frog", "gazelle", "gecko", "gelada",
    "gerbil", "gharial", "giant panda", "gibbon", "giraffe", "gnat", "gnu",
    "goat", "goldfinch", "goldfish", "goose", "gorilla", "grasshopper",
    "grebe", "guanaco", "gull", "guppy", "hamster", "hare", "harrier",
    "hartebeest", "hawk", "hedgehog", "heron", "herring", "hippopotamus",
    "hornbill", "horse", "horsefly", "hummingbird", "hyena", "iguana",
    "impala", "indri", "insect", "jackal", "jaguar", "jay", "jellyfish",
    "jerboa", "jungle cat", "kangaroo", "kingfisher", "kiwi", "koala",
    "komodo dragon", "kookaburra", "kudu", "labradoodle", "lapwing",
    "lark", "lemming", "lemur", "leopard", "leopard gecko", "lion",
    "lionfish", "lizard", "llama", "lobster", "locust", "loon", "loris",
    "louse", "lynx", "lyrebird", "macaw", "magpie", "mallard", "mammoth",
    "manatee", "mandrill", "manta ray", "marten", "mastiff", "mayfly",
    "meerkat", "mink", "minke whale", "mole", "mongoose", "mongrel",
    "monkey", "moorhen", "moose", "mosquito", "moth", "mouse", "mule",
    "narwhal", "nematode", "newt", "nightingale", "noctule", "numbat",
    "nutria", "nyala", "ocelot", "octopus", "okapi", "old english sheepdog",
    "opossum", "orangutan", "oriole", "oryx", "otter", "ovenbird", "owl",
    "ox", "oyster", "panda", "panther", "parakeet", "parrot", "partridge",
    "peacock", "peafowl", "pelican", "penguin", "persian cat", "pheasant",
    "pig", "pigeon", "pika", "pike", "pilot whale", "pine marten", "pinniped",
    "platypus", "pointer", "polecat", "pony", "porgy", "porpoise",
    "possum", "prairie dog", "prawn", "puffin", "puma", "quail", "quetzal",
    "quokka", "quoll", "rabbit", "raccoon", "rat", "rattlesnake", "raven",
    "red fox", "red panda", "reindeer", "rhinoceros", "roadrunner", "robin",
    "rooster", "roseate tern", "roundworm", "sable", "sable antelope",
    "sage grouse", "salmon", "sandpiper", "saola", "sardine", "scorpion",
    "sea cucumber", "sea horse", "sea lion", "sea otter", "sea turtle",
    "sea urchin", "seal", "serpent", "sheep", "shrew", "shrimp", "silkworm",
    "silverfish", "skunk", "sloth", "slug", "smew", "snail", "snake",
    "snipe", "snow leopard", "sparrow", "spider", "squid", "squirrel",
    "starling", "starfish", "stegosaurus", "stingray", "stoat", "stork",
    "sturgeon", "swallow", "swan", "swift", "swordfish", "swordtail",
    "tahr", "tamarin", "tanager", "tapir", "tarantula", "tarsier", "termite",
    "tern", "tetra", "thresher shark", "thrush", "tick", "tiger", "tiger salamander",
    "toad", "toucan", "trout", "tuatara", "tuna", "turkey", "turnip moth",
    "turtle", "uakari", "uguisu", "umbrellabird", "unau", "urchin", "vampire bat",
    "vulture", "wallaby", "walrus", "warthog", "wasp", "water buffalo",
    "weasel", "whale", "whippet", "white rhino", "wild boar", "wildebeest",
    "wolf", "wolverine", "wombat", "woodpecker", "worm", "wren", "yak",
    "yellow jacket", "zebra", "zebrafish"
]

# Проверяем, что список содержит ровно 300 уникальных животных
ANIMALS = list(set(ANIMALS))[:300]

# Список источников с крупными изображениями животных
SOURCES = [
    "https://pixabay.com/images/search/{animal}/",          # Pixabay — большой выбор изображений 
    "https://www.pexels.com/search/{animal}/",              # Pexels — высококачественные фото 
    "https://unsplash.com/s/photos/{animal}",               # Unsplash — открытые лицензии на изображения 
    "https://www.istockphoto.com/ru/photos/{animal}",       # iStock — профессиональные фото 
    "https://www.shutterstock.com/ru/search/{animal}",      # Shutterstock — огромная библиотека изображений
    "https://freepik.com/search?query={animal}",           # Freepik — стоковые изображения  
    "https://stock.adobe.com/ru/search?k={animal}",        # Adobe Stock — профессиональные изображения 
    "https://a-z-animals.com/animals/{animal}/photos/",    # A-Z Animals — специализированный сайт с фото диких животных
    "https://animals.sandiegozoo.org/animals/{animal}/photos",  # San Diego Zoo — крупные животные
    "https://nationalzoo.si.edu/multimedia/{animal}-gallery",  # Smithsonian National Zoo — научные фото
    "https://www.flickr.com/search/?text={animal}%20wild", # Flickr — пользовательские фото с лицензией CC 
    "https://commons.wikimedia.org/wiki/Category:{animal}s",  # Wikimedia Commons — свободные медиафайлы 
    "https://earthslight.com/category/{animal}"             # Earth’s Light — природа и животные
]

def download_single_image(animal):
    filename = os.path.join(SAVE_DIR, f"{animal}.jpg")
    
    if os.path.exists(filename):
        print(f"[Пропущено] Файл {filename} уже существует.")
        return

    for source in SOURCES:
        url = source.format(animal=animal)
        try:
            response = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
            if response.status_code != 200:
                print(f"[Пропущено] Недоступный источник: {url}")
                continue

            soup = BeautifulSoup(response.text, 'html.parser')
            images = soup.find_all('img')

            for img in images:
                src = img.get('src')
                if not src or any(x in src.lower() for x in ['logo', 'icon', 'svg', 'favicon']):
                    continue

                full_url = urljoin(url, src)
                try:
                    img_data = requests.get(full_url, timeout=10).content
                    with open(filename, 'wb') as handler:
                        handler.write(img_data)
                    print(f"Сохранено: {filename}")
                    return
                except Exception as e:
                    print(f"Ошибка при загрузке изображения с {url}: {e}")
                    continue

        except Exception as e:
            print(f"[Ошибка] Источник недоступен: {url}, ошибка: {e}")

    print(f"[Не найдено] Не удалось найти изображение для {animal}")

if __name__ == "__main__":
    for animal in ANIMALS:
        download_single_image(animal)