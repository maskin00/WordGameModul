// modules/DataManager.js
class DataManager {
    constructor() {
        this.categories = {};
        this.wordData = {};
        this.wordMapping = {}; // Сопоставление слов с изображениями
        this.isLoaded = false;
        this.supportedImageFormats = ['png', 'jpg', 'jpeg'];
        this.maxImageSize = 100 * 1024; // 100KB максимальный размер
    }

    async loadConfig() {
        try {
            // Загружаем конфигурацию категорий
            const categoriesResponse = await fetch('data/config/categories.json');
            const categoriesData = await categoriesResponse.json();
            
            // Преобразуем массив в объект для обратной совместимости
            this.categories = {};
            categoriesData.categories.forEach(category => {
                this.categories[category.id] = category;
            });

            console.log('DataManager: Категории загружены', this.categories);
            this.isLoaded = true;
            return true;
        } catch (error) {
            console.error('DataManager: Ошибка загрузки конфигурации:', error);
            return false;
        }
    }

    async loadWordData(categoryId, language) {
        try {
            const category = this.categories[categoryId];
            if (!category) {
                throw new Error(`Категория ${categoryId} не найдена`);
            }

            const wordFile = category.wordFiles[language] || category.wordFiles['ru'];
            const response = await fetch(`data/words/${language}/${wordFile}`);
            const text = await response.text();
            
            // Парсим новый формат: номер - СЛОВО - код_изображения
            const words = text.split('\n')
                .map(line => line.trim())
                .filter(line => line && !line.startsWith('#'))
                .map(line => {
                    const parts = line.split(' - ');
                    if (parts.length >= 3) {
                        const imageCode = parts[2];
                        let imagePath;
                        
                        // Определяем путь к изображению на основе категории
                        if (categoryId === 'capitals') {
                            imagePath = `data/images/capitals/${imageCode}.png`;
                        }
                        else if (categoryId === 'footballers') {
                            imagePath = `data/images/footballers/${imageCode}.png`;
                        }
                        // Для животных и динозавров - imageCode уже содержит расширение
                        else if (categoryId === 'animals' || categoryId === 'dinosaurs') {
                            imagePath = `data/images/${category.imageFolder}/${imageCode}`;
                        }
                        else {
                            imagePath = `data/images/${category.imageFolder}/${imageCode}.png`;
                        }
                        
                        return {
                            id: parseInt(parts[0]),
                            word: parts[1].toUpperCase(),
                            imageCode: imageCode,
                            imagePath: imagePath
                        };
                    }
                    return null;
                })
                .filter(item => item !== null);

            const cacheKey = `${categoryId}_${language}`;
            this.wordData[cacheKey] = words;
            
            console.log(`DataManager: Загружено ${words.length} слов для ${categoryId}/${language}`);
            return words;
        } catch (error) {
            console.error(`DataManager: Ошибка загрузки слов для ${categoryId}/${language}:`, error);
            return [];
        }
    }

    getWordData(categoryId, language) {
        const cacheKey = `${categoryId}_${language}`;
        return this.wordData[cacheKey] || [];
    }

    getCategories() {
        return Object.keys(this.categories).map(id => ({
            id: id,
            ...this.categories[id]
        }));
    }

    getCategoryById(categoryId) {
        return this.categories[categoryId];
    }

    getRandomWords(categoryId, language, count = 10) {
        const words = this.getWordData(categoryId, language);
        if (words.length === 0) {
            return [];
        }

        const shuffled = [...words].sort(() => Math.random() - 0.5);
        return shuffled.slice(0, Math.min(count, shuffled.length));
    }

    // Проверка существования изображения
    async checkImageExists(imagePath) {
        try {
            const response = await fetch(imagePath, { method: 'HEAD' });
            return response.ok;
        } catch {
            return false;
        }
    }

    // Получение альтернативного изображения если основное не найдено
    getFallbackImage(category) {
        return `data/images/${category.imageFolder}/default.png`;
    }

    // Получить категории для определенного языка
    getCategoriesForLanguage(languageCode) {
        const availableCategories = [];
        
        for (const [categoryId, categoryData] of Object.entries(this.categories)) {
            // Проверяем поддержку языка в новой структуре
            if (categoryData.wordFiles && categoryData.wordFiles[languageCode]) {
                availableCategories.push({
                    id: categoryId,
                    name: categoryData.names[languageCode] || categoryData.names.ru || categoryId,
                    icon: '📁', // Убрали иконки из новой структуры
                    description: categoryData.description[languageCode] || categoryData.description.ru
                });
            }
        }
        
        return availableCategories;
    }

    // Загрузить данные слов для категории и языка
    async loadCategoryData(categoryId, languageCode) {
        const cacheKey = `${categoryId}_${languageCode}`;
        
        // Проверяем кэш
        if (this.wordData.hasOwnProperty(cacheKey)) {
            return this.wordData[cacheKey];
        }

        try {
            const words = await this.loadWordData(categoryId, languageCode);
            
            // Кэшируем результат
            this.wordData[cacheKey] = words;
            
            console.log(`Загружены данные для ${categoryId} (${languageCode}):`, words.length, 'слов');
            return words;
            
        } catch (error) {
            console.error(`Ошибка загрузки данных для ${categoryId} (${languageCode}):`, error);
            return [];
        }
    }

    // Парсинг файла со словами
    parseWordsFile(textData, categoryId) {
        console.log(`[DataManager] Parsing words file for category: ${categoryId}`);
        const lines = textData.split('\n')
            .map(line => line.trim())
            .filter(line => line.length > 0);
        
        console.log(`[DataManager] Found ${lines.length} lines to parse`);
        const parsedWords = [];
        
        for (let i = 0; i < lines.length; i++) {
            const line = lines[i];
            // Новый формат: номер - СЛОВО - код_изображения
            const parts = line.split(' - ');
            if (parts.length >= 2) {
                const number = parseInt(parts[0].trim(), 10);
                const word = parts[1].trim();
                const imageCode = parts.length > 2 ? parts[2].trim() : number.toString();
                
                if (!isNaN(number) && word) {
                    // Определяем путь к изображению на основе категории
                    let imagePath = `data/images/${categoryId}/${imageCode}`;
                    
                    // Для столиц - используем коды стран
                    if (categoryId === 'capitals') {
                        imagePath = `data/images/capitals/${imageCode}.png`;
                    }
                    // Для футболистов - используем прямой код
                    else if (categoryId === 'footballers') {
                        imagePath = `data/images/footballers/${imageCode}.png`;
                    }
                    // Для животных и динозавров - imageCode уже содержит расширение
                    else if (categoryId === 'animals' || categoryId === 'dinosaurs') {
                        imagePath = `data/images/${categoryId}/${imageCode}`;
                    }
                    else {
                        imagePath = `data/images/${categoryId}/${imageCode}.png`;
                    }
                    
                    const wordData = {
                        id: number,
                        word: word,
                        imageCode: imageCode,
                        imagePath: imagePath,
                        originalLine: line
                    };
                    
                    console.log(`[DataManager] Line ${i + 1}: "${word}" -> "${imageCode}" -> "${imagePath}"`);
                    parsedWords.push(wordData);
                } else {
                    console.warn(`[DataManager] Invalid data in line ${i + 1}: number=${number}, word="${word}"`);
                }
            } else {
                console.warn(`[DataManager] Invalid format line ${i + 1}: "${line}" (${parts.length} parts)`);
            }
        }
        
        // Сортируем по номеру
        parsedWords.sort((a, b) => a.id - b.id);
        
        return parsedWords;
    }

    // Валидация данных категории (проверка существования изображений)
    async validateCategoryData(categoryId, wordsData) {
        const validatedData = [];
        
        for (const wordItem of wordsData) {
            const imagePath = await this.findImageForWord(categoryId, wordItem.id);
            if (imagePath) {
                validatedData.push({
                    ...wordItem,
                    imagePath: imagePath
                });
            } else {
                console.warn(`Изображение не найдено для слова: ${wordItem.word} (ID: ${wordItem.id})`);
            }
        }
        
        return validatedData;
    }

    // Поиск изображения для слова по ID
    async findImageForWord(categoryId, wordId) {
        for (const format of this.supportedImageFormats) {
            const imagePath = `data/images/${categoryId}/${wordId}.${format}`;
            
            if (await this.checkImageExists(imagePath)) {
                return imagePath;
            }
        }
        return null;
    }

    // Валидация нового файла со словами
    validateWordsFile(fileContent, categoryId = 'unknown') {
        const parsedWords = this.parseWordsFile(fileContent, categoryId);
        const validation = {
            isValid: parsedWords.length > 0,
            wordCount: parsedWords.length,
            words: parsedWords,
            errors: [],
            duplicateIds: []
        };

        // Проверка на дубликаты ID
        const idSet = new Set();
        const duplicates = new Set();
        
        for (const word of parsedWords) {
            if (idSet.has(word.id)) {
                duplicates.add(word.id);
            } else {
                idSet.add(word.id);
            }
        }
        
        validation.duplicateIds = Array.from(duplicates);
        
        if (validation.duplicateIds.length > 0) {
            validation.errors.push(`Найдены дублирующиеся ID: ${validation.duplicateIds.join(', ')}`);
        }

        // Проверка на пропуски в нумерации
        const sortedIds = parsedWords.map(w => w.id).sort((a, b) => a - b);
        const gaps = [];
        
        for (let i = 1; i < sortedIds.length; i++) {
            const expected = sortedIds[i - 1] + 1;
            if (sortedIds[i] !== expected && sortedIds[i] > expected) {
                for (let missing = expected; missing < sortedIds[i]; missing++) {
                    gaps.push(missing);
                }
            }
        }
        
        if (gaps.length > 0) {
            validation.errors.push(`Пропущены ID: ${gaps.join(', ')}`);
        }

        return validation;
    }

    // Валидация изображений
    async validateImages(imageFiles, wordsData) {
        const validation = {
            validImages: [],
            invalidImages: [],
            matchedPairs: [],
            unmatchedWords: [],
            unmatchedImages: []
        };

        // Создаем карту ID слов
        const wordIds = new Set(wordsData.map(w => w.id));
        
        // Обрабатываем каждое изображение
        for (const file of imageFiles) {
            const imageValidation = await this.validateSingleImage(file);
            
            if (imageValidation.isValid) {
                validation.validImages.push({
                    file: file,
                    id: imageValidation.id,
                    format: imageValidation.format
                });
                
                // Проверяем соответствие со словами
                if (wordIds.has(imageValidation.id)) {
                    validation.matchedPairs.push({
                        id: imageValidation.id,
                        word: wordsData.find(w => w.id === imageValidation.id)?.word,
                        image: file.name
                    });
                } else {
                    validation.unmatchedImages.push({
                        file: file.name,
                        id: imageValidation.id,
                        reason: 'Нет соответствующего слова'
                    });
                }
            } else {
                validation.invalidImages.push({
                    file: file.name,
                    errors: imageValidation.errors
                });
            }
        }

        // Находим слова без изображений
        const imageIds = new Set(validation.validImages.map(img => img.id));
        validation.unmatchedWords = wordsData
            .filter(word => !imageIds.has(word.id))
            .map(word => ({
                id: word.id,
                word: word.word,
                reason: 'Нет соответствующего изображения'
            }));

        return validation;
    }

    // Валидация одного изображения
    async validateSingleImage(file) {
        const validation = {
            isValid: false,
            id: null,
            format: null,
            errors: []
        };

        // Проверка размера файла
        if (file.size > this.maxImageSize) {
            validation.errors.push(`Размер файла превышает ${this.maxImageSize / 1024}KB`);
        }

        // Извлечение ID из имени файла
        const nameMatch = file.name.match(/^(\d+)\.(\w+)$/);
        if (!nameMatch) {
            validation.errors.push('Неверный формат имени файла (ожидается: номер.расширение)');
            return validation;
        }

        const [, idStr, extension] = nameMatch;
        const id = parseInt(idStr, 10);
        
        if (isNaN(id) || id < 1) {
            validation.errors.push('Неверный номер в имени файла');
            return validation;
        }

        // Проверка формата
        if (!this.supportedImageFormats.includes(extension.toLowerCase())) {
            validation.errors.push(`Неподдерживаемый формат изображения (поддерживаются: ${this.supportedImageFormats.join(', ')})`);
            return validation;
        }

        // Проверка типа файла
        if (!file.type.startsWith('image/')) {
            validation.errors.push('Файл не является изображением');
            return validation;
        }

        validation.isValid = validation.errors.length === 0;
        validation.id = id;
        validation.format = extension.toLowerCase();

        return validation;
    }

    // Создание URL для изображения из файла
    createImageURL(file) {
        return URL.createObjectURL(file);
    }

    // Освобождение URL изображения
    revokeImageURL(url) {
        URL.revokeObjectURL(url);
    }

    // Добавление новой категории
    async addCategory(categoryData) {
        const { id, name, icon, language, wordsFile, imageFiles } = categoryData;
        
        try {
            // Валидация данных
            const wordsValidation = this.validateWordsFile(wordsFile);
            if (!wordsValidation.isValid) {
                throw new Error(`Ошибки в файле со словами: ${wordsValidation.errors.join(', ')}`);
            }

            const imagesValidation = await this.validateImages(imageFiles, wordsValidation.words);
            
            if (imagesValidation.matchedPairs.length === 0) {
                throw new Error('Нет совпадающих пар слово-изображение');
            }

            // Обновляем конфигурацию категорий
            if (!this.categories[id]) {
                this.categories[id] = {
                    name: {},
                    icon: icon || '📁',
                    languages: []
                };
            }

            this.categories[id].name[language] = name;
            if (!this.categories[id].languages.includes(language)) {
                this.categories[id].languages.push(language);
            }

            // Возвращаем результат валидации для показа пользователю
            return {
                success: true,
                categoryId: id,
                language: language,
                wordsValidation: wordsValidation,
                imagesValidation: imagesValidation,
                matchedPairs: imagesValidation.matchedPairs
            };

        } catch (error) {
            return {
                success: false,
                error: error.message
            };
        }
    }

    // Получить случайное слово из категории
    getRandomWord(categoryData) {
        if (!categoryData || categoryData.length === 0) {
            return null;
        }
        
        const randomIndex = Math.floor(Math.random() * categoryData.length);
        return categoryData[randomIndex];
    }

    // Очистка кэша
    clearCache() {
        this.wordData = {};
    }

    // Получить статистику загруженных данных  
    getLoadedDataStats() {
        const stats = {
            totalCategories: Object.keys(this.categories).length,
            loadedCombinations: Object.keys(this.wordData).length,
            cacheKeys: Object.keys(this.wordData)
        };
        
        return stats;
    }
}

// Экспорт для использования в других модулях
if (typeof module !== 'undefined' && module.exports) {
    module.exports = DataManager;
} else {
    window.DataManager = DataManager;
}