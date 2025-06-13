// modules/CategoryManager.js
class CategoryManager {
    constructor(dataManager, languageManager) {
        this.dataManager = dataManager;
        this.languageManager = languageManager;
        this.currentCategory = null;
        this.currentLanguage = 'ru';
        this.wordsForGame = []; // Данные слов для текущей игры
    }

    async initialize() {
        try {
            // Инициализируем DataManager если еще не инициализирован
            if (!this.dataManager.isLoaded) {
                await this.dataManager.loadConfig();
            }
            
            console.log('CategoryManager инициализирован');
            return true;
        } catch (error) {
            console.error('Ошибка инициализации CategoryManager:', error);
            return false;
        }
    }

    async setCategory(categoryId, language = null) {
        try {
            if (language) {
                this.currentLanguage = language;
            }
            
            // Проверяем существование категории
            const category = this.dataManager.getCategoryById(categoryId);
            if (!category) {
                throw new Error(`Категория ${categoryId} не найдена`);
            }

            this.currentCategory = categoryId;
            
            // Загружаем данные слов для категории
            this.wordsForGame = await this.dataManager.loadWordData(categoryId, this.currentLanguage);
            
            console.log(`CategoryManager: Установлена категория ${categoryId} для языка ${this.currentLanguage}`);
            console.log(`Загружено ${this.wordsForGame.length} слов`);
            
            return true;
        } catch (error) {
            console.error('Ошибка установки категории:', error);
            return false;
        }
    }

    getCurrentCategory() {
        return this.currentCategory;
    }

    getCurrentLanguage() {
        return this.currentLanguage;
    }

    getCategories() {
        return this.dataManager.getCategories();
    }

    getCategoryName(categoryId, language = null) {
        const category = this.dataManager.getCategoryById(categoryId);
        if (!category) return categoryId;
        
        const lang = language || this.currentLanguage;
        return category.names[lang] || category.names['ru'] || categoryId;
    }

    isReadyForGame() {
        return this.currentCategory !== null && this.wordsForGame.length > 0;
    }

    getRandomWord() {
        if (!this.isReadyForGame()) {
            console.warn('CategoryManager: Игра не готова, категория не установлена');
            return null;
        }

        const randomIndex = Math.floor(Math.random() * this.wordsForGame.length);
        const wordData = this.wordsForGame[randomIndex];
        
        return {
            word: wordData.word,
            imagePath: wordData.imagePath,
            imageCode: wordData.imageCode,
            id: wordData.id
        };
    }

    getWordsCount() {
        return this.wordsForGame.length;
    }

    // Получить все слова для текущей категории и языка
    getAllWords() {
        return [...this.wordsForGame];
    }

    // Проверить поддержку языка для категории
    isLanguageSupported(categoryId, language) {
        const category = this.dataManager.getCategoryById(categoryId);
        if (!category) return false;
        
        return Object.keys(category.wordFiles).includes(language);
    }

    // Получить поддерживаемые языки для категории
    getSupportedLanguages(categoryId) {
        const category = this.dataManager.getCategoryById(categoryId);
        if (!category) return [];
        
        return Object.keys(category.wordFiles);
    }

    // Сброс текущей категории
    reset() {
        this.currentCategory = null;
        this.wordsForGame = [];
    }

    // Статистика категории
    getCategoryStats() {
        if (!this.currentCategory) return null;
        
        const category = this.dataManager.getCategoryById(this.currentCategory);
        return {
            id: this.currentCategory,
            name: this.getCategoryName(this.currentCategory),
            language: this.currentLanguage,
            wordsCount: this.wordsForGame.length,
            supportedLanguages: this.getSupportedLanguages(this.currentCategory),
            description: category.description[this.currentLanguage] || category.description['ru']
        };
    }
}

// Экспорт для использования в других модулях
if (typeof module !== 'undefined' && module.exports) {
    module.exports = CategoryManager;
} else {
    window.CategoryManager = CategoryManager;
}