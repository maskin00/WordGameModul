/**
 * LanguageManager.js - Модуль управления языками и раскладками клавиатуры
 * 
 * НАЗНАЧЕНИЕ:
 * Этот модуль отвечает за полное управление многоязычностью в игре, включая:
 * - Загрузку и управление языковыми конфигурациями
 * - Переключение между языками интерфейса
 * - Управление различными раскладками клавиатуры (QWERTY, Dvorak, Colemak)
 * - Создание и управление виртуальной клавиатурой для мобильных устройств
 * - Автоматическую локализацию DOM элементов
 * 
 * АРХИТЕКТУРА:
 * - Singleton паттерн для глобального доступа к языковым настройкам
 * - Асинхронная загрузка конфигурации из JSON файлов
 * - Система callback'ов для уведомления других модулей об изменениях
 * - Адаптивная виртуальная клавиатура с оптимизацией для мобильных устройств
 * 
 * ПОДДЕРЖИВАЕМЫЕ ЯЗЫКИ:
 * - Русский (ru): 33 буквы кириллицы + дефис + пробел
 * - Английский (en): 26 букв латиницы + дефис + пробел  
 * - Испанский (es): 27 букв (включая Ñ) + дефис + пробел
 * 
 * ПОДДЕРЖИВАЕМЫЕ РАСКЛАДКИ:
 * - QWERTY: Стандартная раскладка для каждого языка
 * - Dvorak: Оптимизированная раскладка для скорости печати
 * - Colemak: Эргономичная раскладка, компромисс между QWERTY и Dvorak
 * 
 * МОБИЛЬНАЯ ОПТИМИЗАЦИЯ:
 * - Автоматическое разбиение клавиш на строки для каждой раскладки
 * - Адаптивные размеры кнопок для разных размеров экрана
 * - Минимальные отступы для максимального использования пространства
 * - Поддержка touch событий для мобильных устройств
 */

// modules/LanguageManager.js
class LanguageManager {
    /**
     * Конструктор класса LanguageManager
     * Инициализирует базовые свойства и устанавливает значения по умолчанию
     */
    constructor() {
        // Объект со всеми загруженными языковыми конфигурациями
        this.languages = {};
        
        // Текущий активный язык (по умолчанию русский)
        this.currentLanguage = 'ru';
        
        // Текущая активная раскладка клавиатуры (по умолчанию QWERTY)
        this.currentKeyboardLayout = 'qwerty';
        
        // Callback функция, вызываемая при смене языка
        // Позволяет другим модулям реагировать на изменение языка
        this.onLanguageChange = null;
        
        // Callback функция, вызываемая при смене раскладки клавиатуры
        // Используется для обновления виртуальной клавиатуры
        this.onKeyboardLayoutChange = null;
    }

    /**
     * Асинхронная инициализация модуля
     * Загружает языковые конфигурации из JSON файла
     * 
     * @returns {Promise<boolean>} true если загрузка успешна, false при ошибке
     */
    async initialize() {
        try {
            // Загружаем конфигурацию языков из JSON файла
            const response = await fetch('data/config/languages.json');
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            // Парсим JSON и сохраняем в объект languages
            this.languages = await response.json();
            console.log('Языки загружены:', Object.keys(this.languages));
            return true;
        } catch (error) {
            console.error('Ошибка загрузки языков:', error);
            
            // Fallback конфигурация - минимальный русский язык
            // Используется если основной файл конфигурации недоступен
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
                    // Старая система клавиатуры для обратной совместимости
                    keyboard: ['Й','Ц','У','К','Е','Н','Г','Ш','Щ','З','Х','Ъ',
                               'Ф','Ы','В','А','П','Р','О','Л','Д','Ж','Э',
                               'Я','Ч','С','М','И','Т','Ь','Б','Ю','-',' '],
                    // Базовые UI тексты
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

    /**
     * Получить список всех доступных языков
     * 
     * @returns {Array<{code: string, name: string}>} Массив объектов с кодом и названием языка
     */
    getAvailableLanguages() {
        return Object.keys(this.languages).map(code => ({
            code: code,
            name: this.languages[code].name
        }));
    }

    /**
     * Получить список доступных раскладок клавиатуры для текущего языка
     * 
     * @returns {Array<{code: string, name: string}>} Массив объектов с кодом и названием раскладки
     */
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

    /**
     * Установить активный язык интерфейса и игры
     * При смене языка автоматически сбрасывается раскладка на первую доступную
     * 
     * @param {string} languageCode - Код языка (ru, en, es)
     * @returns {boolean} true если язык успешно установлен, false при ошибке
     */
    setLanguage(languageCode) {
        if (this.languages[languageCode]) {
            this.currentLanguage = languageCode;
            console.log(`Язык изменен на: ${this.languages[languageCode].name}`);
            
            // Автоматически сбрасываем раскладку на первую доступную для нового языка
            // Это предотвращает ситуации когда выбранная раскладка недоступна для нового языка
            const availableLayouts = this.getAvailableKeyboardLayouts();
            if (availableLayouts.length > 0) {
                this.currentKeyboardLayout = availableLayouts[0].code;
            }
            
            // Уведомляем подписчиков о смене языка
            // Это позволяет другим модулям (например, GameEngine) обновить свое состояние
            if (this.onLanguageChange) {
                this.onLanguageChange(languageCode);
            }
            
            return true;
        } else {
            console.error(`Язык ${languageCode} не найден`);
            return false;
        }
    }

    /**
     * Установить активную раскладку клавиатуры
     * 
     * @param {string} layoutCode - Код раскладки (qwerty, dvorak, colemak)
     * @returns {boolean} true если раскладка успешно установлена, false при ошибке
     */
    setKeyboardLayout(layoutCode) {
        const language = this.languages[this.currentLanguage];
        if (language && language.keyboards && language.keyboards[layoutCode]) {
            this.currentKeyboardLayout = layoutCode;
            console.log(`Раскладка клавиатуры изменена на: ${language.keyboards[layoutCode].name}`);
            
            // Уведомляем подписчиков о смене раскладки
            // Это триггерит обновление виртуальной клавиатуры
            if (this.onKeyboardLayoutChange) {
                this.onKeyboardLayoutChange(layoutCode);
            }
            
            return true;
        } else {
            console.error(`Раскладка ${layoutCode} не найдена для языка ${this.currentLanguage}`);
            return false;
        }
    }

    /**
     * Получить код текущего активного языка
     * 
     * @returns {string} Код языка (ru, en, es)
     */
    getCurrentLanguage() {
        return this.currentLanguage;
    }

    /**
     * Получить код текущей активной раскладки клавиатуры
     * 
     * @returns {string} Код раскладки (qwerty, dvorak, colemak)
     */
    getCurrentKeyboardLayout() {
        return this.currentKeyboardLayout;
    }

    /**
     * Получить человекочитаемое название текущего языка
     * 
     * @returns {string} Название языка на соответствующем языке
     */
    getCurrentLanguageName() {
        return this.languages[this.currentLanguage]?.name || 'Неизвестный';
    }

    /**
     * Получить человекочитаемое название текущей раскладки клавиатуры
     * 
     * @returns {string} Название раскладки
     */
    getCurrentKeyboardLayoutName() {
        const language = this.languages[this.currentLanguage];
        return language?.keyboards?.[this.currentKeyboardLayout]?.name || 'Неизвестная';
    }

    /**
     * Получить массив символов клавиатуры для текущего языка и раскладки
     * Возвращает полный набор символов включая буквы, дефис и пробел
     * 
     * @returns {Array<string>} Массив символов клавиатуры
     */
    getKeyboard() {
        const language = this.languages[this.currentLanguage];
        
        // Проверяем, есть ли поддержка новой системы раскладок
        if (language?.keyboards?.[this.currentKeyboardLayout]) {
            return language.keyboards[this.currentKeyboardLayout].layout;
        }
        
        // Fallback на старую систему для обратной совместимости
        return language?.keyboard || [];
    }

    /**
     * Получить локализованный текст по ключу
     * Используется для перевода UI элементов
     * 
     * @param {string} key - Ключ текста в конфигурации
     * @returns {string} Локализованный текст или сам ключ если перевод не найден
     */
    getText(key) {
        const ui = this.languages[this.currentLanguage]?.ui;
        return ui?.[key] || key; // Возвращаем ключ если перевод не найден
    }

    /**
     * Получить все UI тексты для текущего языка
     * Полезно для массовой локализации или отладки
     * 
     * @returns {Object} Объект со всеми переводами UI
     */
    getAllTexts() {
        return this.languages[this.currentLanguage]?.ui || {};
    }

    /**
     * Локализовать конкретный DOM элемент
     * 
     * @param {HTMLElement} element - DOM элемент для локализации
     * @param {string} textKey - Ключ текста для перевода
     */
    localizeElement(element, textKey) {
        if (element) {
            element.textContent = this.getText(textKey);
        }
    }

    /**
     * Автоматическая локализация всех элементов с атрибутом data-i18n
     * Сканирует весь DOM и обновляет тексты элементов
     * Используется при смене языка для обновления всего интерфейса
     */
    localizeDOM() {
        const elements = document.querySelectorAll('[data-i18n]');
        elements.forEach(element => {
            const key = element.getAttribute('data-i18n');
            element.textContent = this.getText(key);
        });
    }

    /**
     * Создание выпадающего списка для выбора языка интерфейса
     * Динамически генерирует HTML select элемент со всеми доступными языками
     * 
     * @param {string} containerId - ID контейнера для размещения селектора
     * @param {Function} onChangeCallback - Callback функция, вызываемая при смене языка
     * @returns {HTMLSelectElement|null} Созданный select элемент или null при ошибке
     */
    createLanguageSelector(containerId, onChangeCallback) {
        const container = document.getElementById(containerId);
        if (!container) {
            console.error(`Контейнер ${containerId} не найден`);
            return null;
        }

        // Создаем select элемент с соответствующими классами
        const select = document.createElement('select');
        select.id = 'languageSelect';
        select.className = 'language-select';

        // Добавляем опции для каждого доступного языка
        this.getAvailableLanguages().forEach(lang => {
            const option = document.createElement('option');
            option.value = lang.code;
            option.textContent = lang.name;
            option.selected = lang.code === this.currentLanguage;
            select.appendChild(option);
        });

        // Обработчик изменения языка
        select.addEventListener('change', (e) => {
            const newLanguage = e.target.value;
            this.setLanguage(newLanguage);
            this.localizeDOM(); // Обновляем весь интерфейс
            
            // Вызываем пользовательский callback если он предоставлен
            if (onChangeCallback) {
                onChangeCallback(newLanguage);
            }
        });

        container.appendChild(select);
        return select;
    }

    /**
     * Создание выпадающего списка для выбора раскладки клавиатуры
     * Показывается только если для текущего языка доступно несколько раскладок
     * 
     * @param {string} containerId - ID контейнера для размещения селектора
     * @param {Function} onChangeCallback - Callback функция, вызываемая при смене раскладки
     * @returns {HTMLSelectElement|null} Созданный select элемент или null если раскладка одна
     */
    createKeyboardLayoutSelector(containerId, onChangeCallback) {
        const container = document.getElementById(containerId);
        if (!container) {
            console.error(`Контейнер ${containerId} не найден`);
            return null;
        }

        // Очищаем контейнер от предыдущего содержимого
        container.innerHTML = '';

        const availableLayouts = this.getAvailableKeyboardLayouts();
        
        // Если доступна только одна раскладка или их нет, селектор не нужен
        if (availableLayouts.length <= 1) {
            return null;
        }

        // Создаем select элемент для раскладок
        const select = document.createElement('select');
        select.id = 'keyboardLayoutSelect';
        select.className = 'keyboard-layout-select';

        // Добавляем опции для каждой доступной раскладки
        availableLayouts.forEach(layout => {
            const option = document.createElement('option');
            option.value = layout.code;
            option.textContent = layout.name;
            option.selected = layout.code === this.currentKeyboardLayout;
            select.appendChild(option);
        });

        // Обработчик изменения раскладки
        select.addEventListener('change', (e) => {
            const newLayout = e.target.value;
            this.setKeyboardLayout(newLayout);
            
            // Вызываем пользовательский callback если он предоставлен
            if (onChangeCallback) {
                onChangeCallback(newLayout);
            }
        });

        container.appendChild(select);
        return select;
    }

    /**
     * Создание адаптивной виртуальной клавиатуры для мобильных устройств
     * Автоматически подстраивается под текущий язык и раскладку
     * Оптимизирована для touch-устройств с минимальными отступами
     * 
     * @param {string} containerId - ID контейнера для размещения клавиатуры
     * @param {Function} onKeyPress - Callback функция, вызываемая при нажатии клавиши
     */
    createMobileKeyboard(containerId, onKeyPress) {
        const container = document.getElementById(containerId);
        if (!container) {
            console.error(`Контейнер ${containerId} не найден`);
            return;
        }

        // Очищаем контейнер от предыдущей клавиатуры
        container.innerHTML = '';

        // Получаем массив символов для текущего языка и раскладки
        const keyboard = this.getKeyboard();
        
        // Разбиваем символы на строки в соответствии с раскладкой
        // Каждая раскладка имеет свое оптимальное распределение по строкам
        const keyboardRows = this.getKeyboardRows(keyboard);
        
        // Создаем HTML структуру клавиатуры по строкам
        keyboardRows.forEach(row => {
            // Создаем контейнер для строки клавиш
            const rowDiv = document.createElement('div');
            rowDiv.className = 'keyboard-row';
            
            // Создаем кнопки для каждого символа в строке
            row.forEach(letter => {
                const key = document.createElement('button');
                key.className = 'key';
                
                // Специальная обработка для пробела - показываем локализованный текст
                key.textContent = letter === ' ' ? this.getText('space') || 'Пробел' : letter;
                
                // Добавляем специальный класс для служебных символов
                if (letter === ' ' || letter === '-') {
                    key.className += ' special';
                }

                // Универсальный обработчик нажатий для mouse и touch событий
                const handleKeyPress = (e) => {
                    e.preventDefault(); // Предотвращаем стандартное поведение
                    if (onKeyPress) {
                        // Передаем символ в верхнем регистре для единообразия
                        onKeyPress(letter.toUpperCase());
                    }
                };

                // Поддержка как мыши, так и touch-устройств
                key.addEventListener('click', handleKeyPress);
                key.addEventListener('touchstart', handleKeyPress, { passive: false });
                
                rowDiv.appendChild(key);
            });
            
            container.appendChild(rowDiv);
        });

        // Примечание: кнопки управления (Clear, Enter и т.д.) намеренно исключены
        // так как они не нужны для игрового процесса
    }

    /**
     * Разбиение символов клавиатуры на строки для мобильного отображения
     * Каждая комбинация языка и раскладки имеет оптимизированное распределение
     * Учитывает ограничения мобильных экранов и эргономику использования
     * 
     * @param {Array<string>} keyboard - Массив всех символов клавиатуры
     * @returns {Array<Array<string>>} Двумерный массив строк клавиатуры
     */
    getKeyboardRows(keyboard) {
        const lang = this.getCurrentLanguage();
        const layout = this.getCurrentKeyboardLayout();
        
        // Русский язык - специальная обработка для каждой раскладки
        if (lang === 'ru') {
            if (layout === 'dvorak') {
                // Русская Dvorak: 10 + 11 + 11 + 4 (оптимизировано для мобильных)
                return [
                    keyboard.slice(0, 10),   // Я Ч Е О У И К Н Г Ш
                    keyboard.slice(10, 21),  // А Т Р С В Л Д М П Ю Ь
                    keyboard.slice(21, 32),  // Ы Ф Й Б З Х Ц Щ Ъ Ж
                    keyboard.slice(32)       // Э Ё - пробел
                ].filter(row => row.length > 0);
            } else if (layout === 'colemak') {
                // Русская Colemak: 10 + 10 + 11 + 4 (оптимизированное распределение)
                return [
                    keyboard.slice(0, 10),   // Й В Ф П Г Ж Л У Ы Ъ
                    keyboard.slice(10, 20),  // А Р С Т Д Х Н Е И О
                    keyboard.slice(20, 31),  // Я Ч Ц М Б К Ш Щ З Э Ю
                    keyboard.slice(31)       // Ё - пробел Ь
                ].filter(row => row.length > 0);
            } else {
                // Русская QWERTY: 11 + 11 + 11 + 2 (Ъ перемещен в третий ряд)
                return [
                    keyboard.slice(0, 11),   // Й Ц У К Е Н Г Ш Щ З Х
                    keyboard.slice(11, 22),  // Ф Ы В А П Р О Л Д Ж Э  
                    keyboard.slice(22, 33),  // Я Ч С М И Т Ь Б Ю Ё Ъ
                    keyboard.slice(33)       // - и пробел
                ].filter(row => row.length > 0);
            }
        } else if (lang === 'en') {
            // Английский язык: все раскладки имеют одинаковое разбиение
            // 26 букв + дефис + пробел = 28 символов
            return [
                keyboard.slice(0, 10),   // Первая строка (10 букв)
                keyboard.slice(10, 19),  // Вторая строка (9 букв)
                keyboard.slice(19, 26),  // Третья строка (7 букв)
                keyboard.slice(26)       // Служебные символы (- и пробел)
            ].filter(row => row.length > 0);
        } else if (lang === 'es') {
            // Испанский язык: все раскладки имеют одинаковое разбиение
            // 27 букв (включая Ñ) + дефис + пробел = 29 символов
            return [
                keyboard.slice(0, 10),   // Первая строка (10 букв)
                keyboard.slice(10, 20),  // Вторая строка (10 букв, включая Ñ)
                keyboard.slice(20, 27),  // Третья строка (7 букв)
                keyboard.slice(27)       // Служебные символы (- и пробел)
            ].filter(row => row.length > 0);
        } else {
            // Fallback для неизвестных языков: равномерное разбиение по 10 символов
            const rows = [];
            for (let i = 0; i < keyboard.length; i += 10) {
                rows.push(keyboard.slice(i, i + 10));
            }
            return rows;
        }
    }

    /**
     * Проверка поддержки символа текущей клавиатурой
     * Используется для валидации пользовательского ввода
     * 
     * @param {string} key - Символ для проверки
     * @returns {boolean} true если символ поддерживается, false иначе
     */
    isKeySupported(key) {
        const keyboard = this.getKeyboard();
        // Проверяем как в верхнем, так и в нижнем регистре
        return keyboard.includes(key.toUpperCase()) || keyboard.includes(key.toLowerCase());
    }

    /**
     * Создание регулярного выражения для валидации текста на текущем языке
     * Используется для проверки корректности введенных слов
     * Автоматически экранирует специальные символы regex
     * 
     * @returns {RegExp} Регулярное выражение для валидации
     */
    getValidationRegex() {
        const keyboard = this.getKeyboard();
        
        // Экранируем все специальные символы регулярных выражений
        const escapedChars = keyboard.map(char => {
            return char.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
        }).join('');
        
        // Создаем regex для проверки что строка содержит только допустимые символы
        // Флаг 'i' делает проверку нечувствительной к регистру
        return new RegExp(`^[${escapedChars}]+$`, 'i');
    }
}

// Экспорт для использования в других модулях
if (typeof module !== 'undefined' && module.exports) {
    module.exports = LanguageManager;
}