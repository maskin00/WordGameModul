# Структура модульного проекта

```
typing-game/
├── index.html
├── styles.css
├── modules/
│   ├── DataManager.js          # Управление данными
│   ├── CategoryManager.js      # Управление категориями  
│   ├── LanguageManager.js      # Управление языками
│   ├── GameEngine.js          # Основная логика игры
│   └── AdminPanel.js          # Панель администратора
├── data/
│   ├── config/
│   │   ├── languages.json     # Конфигурация языков
│   │   └── categories.json    # Метаданные категорий
│   ├── words/
│   │   ├── ru/
│   │   │   ├── cities.txt
│   │   │   └── footballers.txt
│   │   ├── en/
│   │   │   ├── cities.txt
│   │   │   └── footballers.txt
│   │   └── es/
│   │       ├── cities.txt
│   │       └── footballers.txt
│   └── images/
│       ├── cities/
│       │   ├── 1.png
│       │   ├── 2.jpg
│       │   └── 3.jpeg
│       ├── footballers/
│       │   ├── 1.png
│       │   └── 2.png
│       └── [custom-category]/
│           ├── 1.png
│           └── 2.png
└── admin.html                 # Страница администрирования
```

## Форматы файлов

### Файлы со словами (data/words/[lang]/[category].txt)
```
1 - Москва
2 - Париж
3 - Лондон
4 - Берлин
5 - Токио
```

### languages.json
```json
{
  "ru": {
    "name": "Русский",
    "keyboard": ["Й","Ц","У","К","Е","Н","Г","Ш","Щ","З","Х","Ъ",
                 "Ф","Ы","В","А","П","Р","О","Л","Д","Ж","Э",
                 "Я","Ч","С","М","И","Т","Ь","Б","Ю","-"," "],
    "ui": {
      "score": "Очки",
      "level": "Уровень", 
      "start": "Старт",
      "pause": "Пауза",
      "stop": "Стоп",
      "selectLanguage": "Выберите язык",
      "selectCategory": "Выберите категорию",
      "addCategory": "Добавить категорию",
      "categoryName": "Название категории",
      "uploadWords": "Загрузить файл со словами",
      "uploadImages": "Загрузить изображения",
      "validate": "Проверить",
      "save": "Сохранить"
    }
  },
  "en": {
    "name": "English",
    "keyboard": ["Q","W","E","R","T","Y","U","I","O","P",
                 "A","S","D","F","G","H","J","K","L",
                 "Z","X","C","V","B","N","M","-"," "],
    "ui": {
      "score": "Score",
      "level": "Level",
      "start": "Start",
      "pause": "Pause", 
      "stop": "Stop",
      "selectLanguage": "Select Language",
      "selectCategory": "Select Category",
      "addCategory": "Add Category",
      "categoryName": "Category Name",
      "uploadWords": "Upload Words File",
      "uploadImages": "Upload Images",
      "validate": "Validate",
      "save": "Save"
    }
  },
  "es": {
    "name": "Español",
    "keyboard": ["Q","W","E","R","T","Y","U","I","O","P",
                 "A","S","D","F","G","H","J","K","L","Ñ",
                 "Z","X","C","V","B","N","M","-"," "],
    "ui": {
      "score": "Puntos",
      "level": "Nivel",
      "start": "Iniciar",
      "pause": "Pausa",
      "stop": "Parar",
      "selectLanguage": "Seleccionar Idioma",
      "selectCategory": "Seleccionar Categoría",
      "addCategory": "Añadir Categoría",
      "categoryName": "Nombre de Categoría",
      "uploadWords": "Subir Archivo de Palabras",
      "uploadImages": "Subir Imágenes",
      "validate": "Validar",
      "save": "Guardar"
    }
  }
}
```

### categories.json
```json
{
  "cities": {
    "name": {
      "ru": "Столицы",
      "en": "Capitals", 
      "es": "Capitales"
    },
    "icon": "🏛️",
    "languages": ["ru", "en", "es"]
  },
  "footballers": {
    "name": {
      "ru": "Футболисты",
      "en": "Footballers",
      "es": "Futbolistas"  
    },
    "icon": "⚽",
    "languages": ["ru", "en"]
  }
}
```

## Этапы реализации

### 1. DataManager.js
- Загрузка конфигурационных файлов
- Парсинг файлов со словами
- Валидация соответствия слов и изображений
- Проверка существования файлов изображений

### 2. LanguageManager.js  
- Управление текущим языком
- Локализация интерфейса
- Генерация клавиатуры для выбранного языка

### 3. CategoryManager.js
- Загрузка доступных категорий для языка
- Добавление новых категорий
- Валидация новых категорий

### 4. AdminPanel.js
- Интерфейс добавления категорий
- Загрузка файлов
- Предпросмотр и валидация

### 5. GameEngine.js
- Рефакторинг существующей логики игры
- Интеграция с новыми модулями

## Алгоритм добавления новой категории

1. Пользователь вводит название категории
2. Выбирает язык для категории  
3. Загружает .txt файл со списком слов
4. Загружает папку/файлы изображений
5. Система валидирует:
   - Формат файла со словами (номер - слово)
   - Наличие изображений для каждого номера
   - Поддерживаемые форматы изображений (png, jpg, jpeg)
6. Показывает результат валидации
7. Предлагает сохранить только совпадающие элементы
8. Создает папку с изображениями
9. Обновляет categories.json
10. Перезагружает доступные категории