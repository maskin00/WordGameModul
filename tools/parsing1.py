import os
import time
import re
import requests
from bs4 import BeautifulSoup
from PIL import Image
import io
from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# Целевая папка для сохранения изображений
SAVE_DIR = r"E:\Games\animals wild"

# Создание папки, если она не существует
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

# Функция для сжатия изображения
def compress_image(image):
    img_byte_arr = io.BytesIO()
    quality = 85  # Среднее качество для оптимизации
    image.save(img_byte_arr, format='JPEG', quality=quality)
    return img_byte_arr.getvalue()

# Функция для очистки имени файла
def clean_filename(alt_text):
    # Удаляем недопустимые символы и заменяем пробелы на подчеркивания
    cleaned = re.sub(r'[^\w\s-]', '', alt_text).strip().replace(' ', '_')
    return cleaned if cleaned else None

# Функция для загрузки и обработки изображения
def download_image(url, alt_text):
    try:
        # Пропускаем, если имя файла не осмысленное
        cleaned_filename = clean_filename(alt_text)
        if not cleaned_filename:
            print(f"Пропущено изображение {url}: невалидное имя ({alt_text})")
            return

        # Загружаем изображение
        response = requests.get(url, stream=True, timeout=10)
        if response.status_code == 200:
            # Открываем изображение с помощью Pillow
            image = Image.open(io.BytesIO(response.content))
            if image.mode != 'RGB':
                image = image.convert('RGB')

            # Сжимаем изображение для оптимизации
            image_data = compress_image(image)

            # Сохраняем изображение
            filepath = os.path.join(SAVE_DIR, f"{cleaned_filename}.jpg")
            with open(filepath, 'wb') as f:
                f.write(image_data)
            print(f"Сохранено: {filepath} ({len(image_data)/1024:.2f} КБ)")
        else:
            print(f"Ошибка загрузки {url}: Код состояния {response.status_code}")
    except Exception as e:
        print(f"Ошибка обработки {url}: {str(e)}")

# Функция для получения ссылок на статьи и каталоги
def get_article_links(driver, url):
    try:
        driver.get(url)
        time.sleep(2)  # Ждем загрузки страницы
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        article_links = set()
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            # Фильтруем ссылки на рубрики, страницы каталога и статьи
            if re.search(r'/(zemnovodnye|ptitsy|mlekopitayushhie|ryby|presmykayushhiesya|xishhnye-zhivotnye)/.*\.html$', href) or \
               re.search(r'/(zemnovodnye|ptitsy|mlekopitayushhie|ryby|presmykayushhiesya|xishhnye-zhivotnye)/$', href) or \
               re.search(r'/catalog/[A-Z]+/$', href):
                article_links.add(urljoin(url, href))
        return article_links
    except Exception as e:
        print(f"Ошибка при получении ссылок с {url}: {str(e)}")
        return set()

# Основная функция для парсинга сайта и загрузки изображений
def parse_and_download_images():
    base_url = "https://animals-wild.ru/"
    catalog_base = "https://animals-wild.ru/catalog/"

    # Настройка Selenium
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Запуск в фоновом режиме
    driver = webdriver.Chrome(options=chrome_options)

    try:
        visited_urls = set()
        urls_to_visit = {base_url}
        max_depth = 3  # Глубина парсинга: главная + каталог/рубрики + статьи

        # Добавляем страницы каталога по буквам (A-Z, Л в т.ч.)
        for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZЛ':
            catalog_url = f"{catalog_base}{letter}/"
            urls_to_visit.add(catalog_url)

        for depth in range(max_depth):
            next_urls = set()
            for url in urls_to_visit:
                if url in visited_urls:
                    continue
                visited_urls.add(url)
                print(f"Парсинг страницы: {url} (глубина {depth+1})")
                try:
                    driver.get(url)
                    time.sleep(2)  # Ждем загрузки динамического контента
                    soup = BeautifulSoup(driver.page_source, 'html.parser')

                    # Находим все изображения
                    img_tags = soup.find_all('img')
                    if not img_tags:
                        print(f"Изображения не найдены на {url}")
                    else:
                        for img in img_tags:
                            img_url = img.get('src') or img.get('data-src')  # Учитываем lazy loading
                            if not img_url or 'yandex.ru' in img_url:  # Пропускаем баннеры/информеры
                                continue
                            img_url = urljoin(url, img_url)
                            # Получаем alt-текст или пропускаем, если его нет
                            alt_text = img.get('alt', '')
                            if not alt_text or 'animal_' in alt_text:
                                continue  # Пропускаем изображения без осмысленного alt
                            download_image(img_url, alt_text)

                    # Собираем ссылки на рубрики, каталоги и статьи
                    if depth < max_depth - 1:
                        next_urls.update(get_article_links(driver, url))

                    # Задержка, чтобы не нагружать сервер
                    time.sleep(1)
                except Exception as e:
                    print(f"Ошибка при парсинге {url}: {str(e)}")

            urls_to_visit = next_urls

    finally:
        driver.quit()

if __name__ == "__main__":
    parse_and_download_images()