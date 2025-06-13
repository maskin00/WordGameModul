// modules/LanguageManager.js
class LanguageManager {
    constructor() {
        this.languages = {};
        this.currentLanguage = 'ru'; // По умолчанию русский
        this.currentKeyboardLayout = 'qwerty'; // По умолчанию QWERTY
        this.onLanguageChange = null; // Callback для уведомления об изменении языка
        this.onKeyboardLayoutChange = null; // Callback для уведомления об изменении раскладки
    }

    async initialize() {
        try {
            const response = await fetch('data/config/languages.json');
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            this.languages = await response.json();
            console.log('Языки загружены:', Object.keys(this.languages));
            return true;
        } catch (error) {
            console.error('Ошибка загрузки языков:', error);
            // Fallback на базовый русский язык
            this.languages = {
                'ru': {
                    name: 'Русский',
                    keyboards: {
                        'qwerty': {
                            name: 'QWERTY',
                            layout: ['Й','Ц','У','К','Е','Н','Г','Ш','Щ','З','Х','Ъ',
                                   'Ф','Ы','В','А','П','Р','О','Л','Д','Ж','Э',
                                   'Я','Ч','С','М','И','Т','Ь','Б','Ю','-',' ']
                        }
                    },
                    keyboard: ['Й','Ц','У','К','Е','Н','Г','Ш','Щ','З','Х','Ъ',
                               'Ф','Ы','В','А','П','Р','О','Л','Д','Ж','Э',
                               'Я','Ч','С','М','И','Т','Ь','Б','Ю','-',' '],
                    ui: {
                        score: 'Очки',
                        level: 'Уровень',
                        start: 'Старт',
                        pause: 'Пауза',
                        stop: 'Стоп',
                        selectLanguage: 'Выберите язык',
                        selectCategory: 'Выберите категорию',
                        selectKeyboardLayout: 'Раскладка клавиатуры'
                    }
                }
            };
            return false;
        }
    }

    // Получить все доступные языки
    getAvailableLanguages() {
        return Object.keys(this.languages).map(code => ({
            code: code,
            name: this.languages[code].name
        }));
    }

    // Получить доступные раскладки для текущего языка
    getAvailableKeyboardLayouts() {
        const language = this.languages[this.currentLanguage];
        if (!language || !language.keyboards) {
            return [];
        }
        
        return Object.keys(language.keyboards).map(code => ({
            code: code,
            name: language.keyboards[code].name
        }));
    }

    // Установить текущий язык
    setLanguage(languageCode) {
        if (this.languages[languageCode]) {
            this.currentLanguage = languageCode;
            console.log(`Язык изменен на: ${this.languages[languageCode].name}`);
            
            // Сбрасываем раскладку на первую доступную для нового языка
            const availableLayouts = this.getAvailableKeyboardLayouts();
            if (availableLayouts.length > 0) {
                this.currentKeyboardLayout = availableLayouts[0].code;
            }
            
            // Уведомляем о смене языка
            if (this.onLanguageChange) {
                this.onLanguageChange(languageCode);
            }
            
            return true;
        } else {
            console.error(`Язык ${languageCode} не найден`);
            return false;
        }
    }

    // Установить раскладку клавиатуры
    setKeyboardLayout(layoutCode) {
        const language = this.languages[this.currentLanguage];
        if (language && language.keyboards && language.keyboards[layoutCode]) {
            this.currentKeyboardLayout = layoutCode;
            console.log(`Раскладка клавиатуры изменена на: ${language.keyboards[layoutCode].name}`);
            
            // Уведомляем о смене раскладки
            if (this.onKeyboardLayoutChange) {
                this.onKeyboardLayoutChange(layoutCode);
            }
            
            return true;
        } else {
            console.error(`Раскладка ${layoutCode} не найдена для языка ${this.currentLanguage}`);
            return false;
        }
    }

    // Получить текущий язык
    getCurrentLanguage() {
        return this.currentLanguage;
    }

    // Получить текущую раскладку
    getCurrentKeyboardLayout() {
        return this.currentKeyboardLayout;
    }

    // Получить название текущего языка
    getCurrentLanguageName() {
        return this.languages[this.currentLanguage]?.name || 'Неизвестный';
    }

    // Получить название текущей раскладки
    getCurrentKeyboardLayoutName() {
        const language = this.languages[this.currentLanguage];
        return language?.keyboards?.[this.currentKeyboardLayout]?.name || 'Неизвестная';
    }

    // Получить клавиатуру для текущего языка и раскладки
    getKeyboard() {
        const language = this.languages[this.currentLanguage];
        
        // Проверяем, есть ли поддержка раскладок
        if (language?.keyboards?.[this.currentKeyboardLayout]) {
            return language.keyboards[this.currentKeyboardLayout].layout;
        }
        
        // Fallback на старую систему
        return language?.keyboard || [];
    }

    // Получить локализованный текст
    getText(key) {
        const ui = this.languages[this.currentLanguage]?.ui;
        return ui?.[key] || key; // Возвращаем ключ если перевод не найден
    }

    // Получить все UI тексты для текущего языка
    getAllTexts() {
        return this.languages[this.currentLanguage]?.ui || {};
    }

    // Локализация элементов DOM
    localizeElement(element, textKey) {
        if (element) {
            element.textContent = this.getText(textKey);
        }
    }

    // Локализация всех элементов с data-i18n атрибутом
    localizeDOM() {
        const elements = document.querySelectorAll('[data-i18n]');
        elements.forEach(element => {
            const key = element.getAttribute('data-i18n');
            element.textContent = this.getText(key);
        });
    }

    // Создание выпадающего списка языков
    createLanguageSelector(containerId, onChangeCallback) {
        const container = document.getElementById(containerId);
        if (!container) {
            console.error(`Контейнер ${containerId} не найден`);
            return null;
        }

        const select = document.createElement('select');
        select.id = 'languageSelect';
        select.className = 'language-select';

        // Добавляем опции
        this.getAvailableLanguages().forEach(lang => {
            const option = document.createElement('option');
            option.value = lang.code;
            option.textContent = lang.name;
            option.selected = lang.code === this.currentLanguage;
            select.appendChild(option);
        });

        // Обработчик изменения
        select.addEventListener('change', (e) => {
            const newLanguage = e.target.value;
            this.setLanguage(newLanguage);
            this.localizeDOM();
            
            if (onChangeCallback) {
                onChangeCallback(newLanguage);
            }
        });

        container.appendChild(select);
        return select;
    }

    // Создание выпадающего списка раскладок клавиатуры
    createKeyboardLayoutSelector(containerId, onChangeCallback) {
        const container = document.getElementById(containerId);
        if (!container) {
            console.error(`Контейнер ${containerId} не найден`);
            return null;
        }

        // Очищаем контейнер
        container.innerHTML = '';

        const availableLayouts = this.getAvailableKeyboardLayouts();
        
        // Если нет раскладок или только одна, не создаем селектор
        if (availableLayouts.length <= 1) {
            return null;
        }

        const select = document.createElement('select');
        select.id = 'keyboardLayoutSelect';
        select.className = 'keyboard-layout-select';

        // Добавляем опции
        availableLayouts.forEach(layout => {
            const option = document.createElement('option');
            option.value = layout.code;
            option.textContent = layout.name;
            option.selected = layout.code === this.currentKeyboardLayout;
            select.appendChild(option);
        });

        // Обработчик изменения
        select.addEventListener('change', (e) => {
            const newLayout = e.target.value;
            this.setKeyboardLayout(newLayout);
            
            if (onChangeCallback) {
                onChangeCallback(newLayout);
            }
        });

        container.appendChild(select);
        return select;
    }

    // Создание мобильной клавиатуры
    createMobileKeyboard(containerId, onKeyPress) {
        const container = document.getElementById(containerId);
        if (!container) {
            console.error(`Контейнер ${containerId} не найден`);
            return;
        }

        // Очищаем контейнер
        container.innerHTML = '';

        const keyboard = this.getKeyboard();
        
        // Определяем расположение клавиш по строкам для разных языков
        const keyboardRows = this.getKeyboardRows(keyboard);
        
        // Создаем строки клавиатуры
        keyboardRows.forEach(row => {
            const rowDiv = document.createElement('div');
            rowDiv.className = 'keyboard-row';
            
            row.forEach(letter => {
                const key = document.createElement('button');
                key.className = 'key';
                key.textContent = letter === ' ' ? this.getText('space') || 'Пробел' : letter;
                
                if (letter === ' ' || letter === '-') {
                    key.className += ' special';
                }

                // Обработчики событий
                const handleKeyPress = (e) => {
                    e.preventDefault();
                    if (onKeyPress) {
                        onKeyPress(letter.toUpperCase());
                    }
                };

                key.addEventListener('click', handleKeyPress);
                key.addEventListener('touchstart', handleKeyPress, { passive: false });
                
                rowDiv.appendChild(key);
            });
            
            container.appendChild(rowDiv);
        });

        // Кнопки управления в отдельной строке
        const controlRow = document.createElement('div');
        controlRow.className = 'keyboard-row control-row';
        
        // Кнопка очистки
        const clearButton = document.createElement('button');
        clearButton.className = 'key special';
        clearButton.textContent = '← ' + (this.getText('clear') || 'Очистить');
        
        const handleClear = (e) => {
            e.preventDefault();
            if (onKeyPress) {
                onKeyPress('CLEAR');
            }
        };

        clearButton.addEventListener('click', handleClear);
        clearButton.addEventListener('touchstart', handleClear, { passive: false });
        
        controlRow.appendChild(clearButton);
        container.appendChild(controlRow);
    }

    // Разбиение клавиатуры на строки
    getKeyboardRows(keyboard) {
        const lang = this.getCurrentLanguage();
        
        if (lang === 'ru') {
            // Русская клавиатура: 3 строки + служебные символы
            return [
                keyboard.slice(0, 12),   // Й Ц У К Е Н Г Ш Щ З Х Ъ
                keyboard.slice(12, 23),  // Ф Ы В А П Р О Л Д Ж Э  
                keyboard.slice(23, 32),  // Я Ч С М И Т Ь Б Ю
                keyboard.slice(32)       // - и пробел
            ].filter(row => row.length > 0);
        } else if (lang === 'en') {
            // Английская клавиатура: 3 строки + служебные символы
            return [
                keyboard.slice(0, 10),   // Q W E R T Y U I O P
                keyboard.slice(10, 19),  // A S D F G H J K L
                keyboard.slice(19, 26),  // Z X C V B N M
                keyboard.slice(26)       // - и пробел
            ].filter(row => row.length > 0);
        } else if (lang === 'es') {
            // Испанская клавиатура: 3 строки + служебные символы
            return [
                keyboard.slice(0, 10),   // Q W E R T Y U I O P
                keyboard.slice(10, 20),  // A S D F G H J K L Ñ
                keyboard.slice(20, 27),  // Z X C V B N M
                keyboard.slice(27)       // - и пробел
            ].filter(row => row.length > 0);
        } else {
            // Fallback: по 10 символов в строке
            const rows = [];
            for (let i = 0; i < keyboard.length; i += 10) {
                rows.push(keyboard.slice(i, i + 10));
            }
            return rows;
        }
    }

    // Проверка поддержки языка клавиатурой
    isKeySupported(key) {
        const keyboard = this.getKeyboard();
        return keyboard.includes(key.toUpperCase()) || keyboard.includes(key.toLowerCase());
    }

    // Получение регулярного выражения для валидации символов текущего языка
    getValidationRegex() {
        const keyboard = this.getKeyboard();
        const escapedChars = keyboard.map(char => {
            // Экранируем специальные символы для регулярных выражений
            return char.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
        }).join('');
        
        return new RegExp(`^[${escapedChars}]+$`, 'i');
    }
}

// Экспорт для использования в других модулях
if (typeof module !== 'undefined' && module.exports) {
    module.exports = LanguageManager;
}