// modules/GameEngine.js
class GameEngine {
    constructor(dataManager, languageManager, categoryManager) {
        this.dataManager = dataManager;
        this.languageManager = languageManager;
        this.categoryManager = categoryManager;
        
        this.canvas = null;
        this.ctx = null;
        this.words = [];
        this.score = 0;
        this.level = 1;
        this.spawnDelay = 2000;
        this.lastSpawn = 0;
        this.input = '';
        this.isPaused = false;
        this.isActive = false;
        this.gameLoop = null;
        this.particles = [];
        
        // Новые параметры для контроля спавна
        this.maxWordsOnScreen = 1; // Только одно слово одновременно
        this.lastCategoryId = null; // Отслеживание смены категории
        
        // Адаптивные параметры
        this.baseSpeed = 1;
        this.baseFontSize = 28;
        this.baseImageSize = 200;
    }

    async initialize() {
        try {
            this.canvas = document.getElementById('gameCanvas');
            this.ctx = this.canvas.getContext('2d');
            this.canvas.width = 800;
            this.canvas.height = 600;
            
            // Инициализируем адаптивные параметры
            this.updateGameScale(this.canvas.width, this.canvas.height);
            
            this.setupEventListeners();
            console.log('GameEngine инициализирован');
            return true;
        } catch (error) {
            console.error('Ошибка инициализации GameEngine:', error);
            return false;
        }
    }

    handleResize(width, height) {
        if (!this.canvas) return;
        
        // Сохраняем старые размеры для пересчета позиций
        const oldWidth = this.canvas.width;
        const oldHeight = this.canvas.height;
        
        // Устанавливаем новые размеры
        this.canvas.width = width;
        this.canvas.height = height;
        
        // Пересчитываем позиции слов пропорционально
        if (oldWidth > 0 && oldHeight > 0) {
            const scaleX = width / oldWidth;
            const scaleY = height / oldHeight;
            
            this.words.forEach(word => {
                word.x = word.x * scaleX;
                word.y = word.y * scaleY;
                // Корректируем скорость падения пропорционально высоте
                word.speed = word.speed * scaleY;
                
                // Обновляем масштаб изображения если есть
                if (word.image) {
                    word.updateScale(width, height);
                }
            });
        }
        
        // Обновляем базовые параметры для новых слов
        this.updateGameScale(width, height);
        
        console.log(`Canvas resized to ${width}x${height}`);
    }

    updateGameScale(width, height) {
        // Адаптируем параметры игры под размер экрана
        
        // Более плавная адаптация скорости
        this.baseSpeed = Math.max(0.5, Math.min(2.0, height / 700));
        
        // Определяем тип устройства и размер экрана
        const isMobile = window.innerWidth <= 480;
        const isTablet = window.innerWidth <= 1024 && window.innerWidth > 480;
        const canvasArea = width * height;
        
        if (isMobile) {
            // Мобильные - увеличиваем изображения на 30%
            this.baseFontSize = Math.max(18, Math.min(26, Math.sqrt(canvasArea) / 23));
            this.baseImageSize = Math.max(104, Math.min(208, Math.sqrt(canvasArea) / 12)); // +30% от предыдущих значений
        } else if (isTablet) {
            // Планшеты - промежуточные размеры
            this.baseFontSize = Math.max(18, Math.min(30, Math.sqrt(canvasArea) / 28));
            this.baseImageSize = Math.max(140, Math.min(250, Math.sqrt(canvasArea) / 14));
        } else {
            // Десктоп - крупные изображения для лучшей видимости
            this.baseFontSize = Math.max(22, Math.min(40, Math.sqrt(canvasArea) / 30));
            this.baseImageSize = Math.max(200, Math.min(400, Math.sqrt(canvasArea) / 8));
        }
        
        console.log(`Game scale updated: speed=${this.baseSpeed.toFixed(2)}, fontSize=${this.baseFontSize}, imageSize=${this.baseImageSize}, canvas=${width}x${height}, area=${canvasArea}, device=${isMobile ? 'mobile' : isTablet ? 'tablet' : 'desktop'}`);
    }

    setupEventListeners() {
        document.getElementById('startButton').addEventListener('click', () => {
            this.startGame();
        });
        document.getElementById('pauseButton').addEventListener('click', () => {
            this.pauseGame();
        });
        document.getElementById('stopButton').addEventListener('click', () => {
            this.stopGame();
        });
        document.addEventListener('keydown', (e) => {
            if (this.isPaused || !this.isActive) return;
            const key = e.key;
            
            // Поддержка дефисов, пробелов и букв
            if (this.languageManager.isKeySupported(key) || key === 'Backspace' || key === '-' || key === ' ') {
                if (key === 'Backspace') {
                    this.handleKeyPress('CLEAR');
                } else {
                    this.handleKeyPress(key.toUpperCase());
                }
                e.preventDefault();
            }
        });
    }

    startGame() {
        if (!this.categoryManager.isReadyForGame()) {
            alert(this.languageManager.getText('selectCategory') || 'Выберите категорию для игры');
            return;
        }
        
        // Проверяем смену категории
        this.checkCategoryChange();
        
        if (this.isPaused) {
            this.isPaused = false;
            this.resumeGameLoop();
        } else {
            this.resetGameState();
            this.isActive = true;
            this.resumeGameLoop();
        }
        this.updateUI();
        console.log('Игра запущена');
    }

    // Проверка смены категории и очистка экрана
    checkCategoryChange() {
        const currentCategoryId = this.categoryManager.getCurrentCategory();
        if (this.lastCategoryId !== currentCategoryId) {
            console.log(`Категория изменена с ${this.lastCategoryId} на ${currentCategoryId}, очищаем экран`);
            this.clearAllWords();
            this.lastCategoryId = currentCategoryId;
        }
    }

    // Очистка всех слов с экрана
    clearAllWords() {
        this.words = [];
        this.particles = [];
        this.input = '';
        this.lastSpawn = 0; // Сбрасываем время последнего спавна
        console.log('Экран очищен, lastSpawn сброшен');
    }

    pauseGame() {
        if (!this.isActive) return;
        this.isPaused = !this.isPaused;
        if (this.isPaused) {
            this.stopGameLoop();
        } else {
            this.resumeGameLoop();
        }
        console.log(this.isPaused ? 'Игра приостановлена' : 'Игра возобновлена');
    }

    stopGame() {
        this.isActive = false;
        this.isPaused = false;
        this.stopGameLoop();
        this.resetGameState();
        this.updateUI();
        console.log('Игра остановлена');
    }

    resetGameState() {
        this.words = [];
        this.score = 0;
        this.level = 1;
        this.spawnDelay = 2000;
        this.lastSpawn = 0;
        this.input = '';
        this.particles = [];
        this.lastCategoryId = this.categoryManager.getCurrentCategory();
    }

    resumeGameLoop() {
        if (this.gameLoop) {
            cancelAnimationFrame(this.gameLoop);
        }
        const loop = (timestamp) => {
            if (!this.isActive || this.isPaused) return;
            this.update(timestamp);
            this.draw();
            this.gameLoop = requestAnimationFrame(loop);
        };
        this.gameLoop = requestAnimationFrame(loop);
    }

    stopGameLoop() {
        if (this.gameLoop) {
            cancelAnimationFrame(this.gameLoop);
            this.gameLoop = null;
        }
    }

    update(timestamp) {
        // Проверяем смену категории на каждом кадре
        this.checkCategoryChange();
        
        // Подсчитываем активные (не взрывающиеся) слова
        const activeWords = this.words.filter(word => !word.exploding);
        
        // Спавн нового слова ТОЛЬКО если:
        // 1. На экране НЕТ активных слов
        // 2. Прошло достаточно времени с последнего спавна
        if (activeWords.length === 0 && (timestamp - this.lastSpawn > this.spawnDelay)) {
            this.spawnWord();
            this.lastSpawn = timestamp;
        }
        
        // Обновление слов
        for (let i = this.words.length - 1; i >= 0; i--) {
            const word = this.words[i];
            word.update();
            
            // Удаляем слова которые упали за экран
            if (word.y > this.canvas.height + 100) {
                this.words.splice(i, 1);
                console.log('Слово упало за экран, разрешаем новый спавн');
            } 
            // Удаляем взорвавшиеся слова без частиц
            else if (word.exploding && word.particles.length === 0) {
                this.words.splice(i, 1);
                console.log('Взорвавшееся слово удалено, разрешаем новый спавн');
            }
        }
        
        // Обновление частиц
        for (let i = this.particles.length - 1; i >= 0; i--) {
            this.particles[i].update();
            if (this.particles[i].life <= 0) {
                this.particles.splice(i, 1);
            }
        }
        
        this.updateDifficulty();
    }

    draw() {
        // Очищаем канвас
        this.ctx.fillStyle = 'black';
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
        
        // Рисуем слова
        this.words.forEach(word => {
            word.draw(this.ctx, this.input);
        });
        
        // Рисуем частицы
        this.particles.forEach(particle => {
            particle.draw(this.ctx);
        });
        
        // Рисуем интерфейс ввода
        this.drawInput();
    }

    drawInput() {
        this.ctx.font = '24px Arial';
        this.ctx.fillStyle = 'white';
        this.ctx.fillText(`Ввод: ${this.input}`, 10, this.canvas.height - 20);
        
        // Показываем статус соответствия
        if (this.words.length > 0 && !this.words[0].exploding) {
            const word = this.words[0];
            const isPartialMatch = this.isPartialMatch(this.input, word.text);
            const statusText = isPartialMatch ? '✓ Правильно' : '✗ Ошибка';
            this.ctx.fillStyle = isPartialMatch ? 'lime' : 'red';
            this.ctx.fillText(statusText, 200, this.canvas.height - 20);
        }
    }

    spawnWord() {
        const wordData = this.categoryManager.getRandomWord();
        if (!wordData) {
            console.warn('Не удалось получить слово для спавна');
            return;
        }
        
        const activeWords = this.words.filter(word => !word.exploding);
        console.log(`СПАВН: Попытка создать слово "${wordData.word}". Активных слов на экране: ${activeWords.length}`);
        
        if (activeWords.length > 0) {
            console.warn('СПАВН ОТМЕНЕН: На экране уже есть активное слово');
            return;
        }
        
        const x = this.canvas.width / 2; // Спавним по центру
        const word = new Word(wordData.word, x, wordData.imagePath, this);
        word.speed = Math.min(1.5, this.baseSpeed + (this.level - 1) * 0.1);
        this.words.push(word);
        console.log(`СПАВН УСПЕШЕН: Заспавнено слово "${wordData.word}". Всего слов: ${this.words.length}`);
    }

    // Проверка частичного соответствия с поддержкой дефисов и пробелов
    isPartialMatch(input, targetWord) {
        if (!input) return true; // Пустой ввод всегда валиден
        
        const inputUpper = input.toUpperCase().replace(/\s+/g, ' '); // нормализуем пробелы
        const targetUpper = targetWord.toUpperCase();
        
        // Проверяем что введенная часть соответствует началу слова
        return targetUpper.startsWith(inputUpper);
    }

    handleKeyPress(key) {
        if (!this.isActive || this.isPaused) return;
        
        if (key === 'CLEAR') {
            this.input = '';
            return;
        }
        
        // Находим текущее активное слово
        const activeWord = this.words.find(word => !word.exploding);
        if (!activeWord) return;
        
        const newInput = this.input + key;
        
        // Проверяем соответствие с поддержкой дефисов и пробелов
        if (this.isPartialMatch(newInput, activeWord.text)) {
            this.input = newInput;
            
            // Проверяем полное совпадение
            if (this.input.toUpperCase().replace(/\s+/g, ' ') === activeWord.text.toUpperCase()) {
                this.onWordGuessed(activeWord);
            }
        } else {
            // Неправильная буква - сбрасываем ввод
            this.input = '';
            console.log('Неправильная буква, сброс ввода');
        }
    }

    checkInput() {
        // Эта функция больше не нужна, логика перенесена в handleKeyPress
    }

    onWordGuessed(word) {
        const basePoints = word.text.length * 10;
        const speedBonus = Math.max(0, this.canvas.height - word.y) / 10;
        const totalPoints = Math.floor(basePoints + speedBonus);
        
        this.score += totalPoints;
        word.explode();
        
        // Создаем частицы
        for (let i = 0; i < 15; i++) {
            this.particles.push(new Particle(word.x, word.y));
        }
        
        this.input = '';
        this.updateUI();
        console.log(`Слово угадано: ${word.text}, +${totalPoints} очков`);
    }

    updateDifficulty() {
        const newLevel = Math.floor(this.score / 1000) + 1;
        if (newLevel > this.level) {
            this.level = newLevel;
            this.spawnDelay = Math.max(800, 2000 - (this.level - 1) * 150);
            
            // Увеличиваем скорость существующих слов
            this.words.forEach(word => {
                word.speed = Math.min(1.5, this.baseSpeed + (this.level - 1) * 0.1);
            });
            
            console.log(`Уровень повышен до ${this.level}`);
        }
    }

    updateUI() {
        const scoreElement = document.getElementById('score');
        if (scoreElement) {
            const scoreText = this.languageManager.getText('score') || 'Очки';
            const levelText = this.languageManager.getText('level') || 'Уровень';
            scoreElement.textContent = `${scoreText}: ${this.score} (${levelText} ${this.level})`;
        }
    }

    updateGameState() {
        // Вызывается при смене категории
        if (this.isActive) {
            console.log('Игровое состояние обновлено - смена категории');
            this.clearAllWords(); // Очищаем экран но не останавливаем игру
        }
    }

    isGameActive() {
        return this.isActive && !this.isPaused;
    }

    getGameStats() {
        return {
            score: this.score,
            level: this.level,
            wordsOnScreen: this.words.length,
            input: this.input,
            isActive: this.isActive,
            isPaused: this.isPaused
        };
    }
}

class Particle {
    constructor(x, y) {
        this.x = x;
        this.y = y;
        this.radius = Math.random() * 5 + 2;
        this.speedX = (Math.random() - 0.5) * 4;
        this.speedY = (Math.random() - 0.5) * 4;
        this.life = 30;
        this.maxLife = 30;
    }

    update() {
        this.x += this.speedX;
        this.y += this.speedY;
        this.life--;
    }

    draw(ctx) {
        const alpha = this.life / this.maxLife;
        ctx.fillStyle = `rgba(255, 165, 0, ${alpha})`;
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
        ctx.fill();
    }
}

class Word {
    constructor(text, x, imgSrc, gameEngine) {
        this.text = text.toUpperCase();
        this.x = x;
        this.y = 0;
        this.speed = gameEngine ? gameEngine.baseSpeed : 0.3;
        this.imgSrc = imgSrc;
        this.image = new Image();
        this.image.src = imgSrc;
        this.gameEngine = gameEngine;
        this.image.onload = () => {
            console.log(`[GameEngine] ✓ Successfully loaded image for word "${this.text}": ${this.imgSrc}`);
        };
        this.image.onerror = () => {
            console.warn(`[GameEngine] ✗ Failed to load image for word "${this.text}": ${this.imgSrc}`);
        };
        this.particles = [];
        this.exploding = false;
    }

    updateScale(canvasWidth, canvasHeight) {
        // Обновляем масштаб изображения при изменении размера канваса
        if (this.gameEngine) {
            this.maxImageSize = this.gameEngine.baseImageSize;
        }
    }

    update() {
        if (this.exploding) {
            this.particles.forEach(p => p.update());
            this.particles = this.particles.filter(p => p.life > 0);
        } else {
            this.y += this.speed;
        }
    }

    draw(ctx, input) {
        if (this.exploding) {
            this.particles.forEach(p => p.draw(ctx));
            return;
        }

        // Рисуем изображение с адаптивным размером
        let scaledWidth = 0;
        let scaledHeight = 0;
        const maxSize = this.gameEngine ? this.gameEngine.baseImageSize : 200;
        
        if (this.image.complete && this.image.naturalWidth !== 0) {
            const width = this.image.naturalWidth;
            const height = this.image.naturalHeight;
            const scale = Math.min(maxSize / width, maxSize / height);
            scaledWidth = width * scale;
            scaledHeight = height * scale;
            ctx.drawImage(this.image, this.x - scaledWidth / 2, this.y - scaledHeight / 2, scaledWidth, scaledHeight);
        } else {
            // Заглушка для изображения с адаптивным размером
            const placeholderSize = maxSize * 0.8;
            ctx.fillStyle = 'lightgray';
            ctx.fillRect(this.x - placeholderSize / 2, this.y - placeholderSize / 2, placeholderSize, placeholderSize);
            ctx.fillStyle = 'black';
            const fontSize = Math.max(20, placeholderSize / 3);
            ctx.font = `${fontSize}px Arial`;
            ctx.textAlign = 'center';
            ctx.fillText('?', this.x, this.y + fontSize / 3);
            scaledHeight = placeholderSize;
        }

        // Рисуем текст с улучшенным отображением
        this.drawWordText(ctx, input, scaledHeight);
    }

    drawWordText(ctx, input, imageHeight) {
        const fontSize = this.gameEngine ? this.gameEngine.baseFontSize : 28;
        ctx.font = `${fontSize}px Arial`;
        ctx.textAlign = 'center';
        
        const inputUpper = input.toUpperCase().replace(/\s+/g, ' '); // нормализуем пробелы
        const textY = this.y + imageHeight / 2 + fontSize * 1.5;
        
        // Определяем количество правильно введенных символов
        let matchedLength = 0;
        for (let i = 0; i < inputUpper.length && i < this.text.length; i++) {
            if (inputUpper[i] === this.text[i]) {
                matchedLength++;
            } else {
                break; // прерываем при первом несовпадении
            }
        }
        
        // Вычисляем общую ширину текста для центрирования
        const charWidth = ctx.measureText('M').width; // примерная ширина символа
        const spacing = 1.1; // увеличенное расстояние между буквами
        const totalWidth = this.text.length * charWidth * spacing;
        const startX = this.x - totalWidth / 2;
        
        // Рисуем каждый символ отдельно
        for (let i = 0; i < this.text.length; i++) {
            const char = this.text[i];
            const charX = startX + (i * charWidth * spacing);
            
            // Выбираем цвет в зависимости от статуса
            if (i < matchedLength) {
                // Правильно введенные символы - зеленые
                ctx.fillStyle = '#00FF00';
            } else if (i === matchedLength && input.length > matchedLength) {
                // Текущий неправильный символ - красный
                ctx.fillStyle = '#FF4444';
            } else {
                // Еще не введенные символы - белые
                ctx.fillStyle = '#FFFFFF';
            }
            
            // Добавляем тень для лучшей читаемости
            ctx.strokeStyle = 'black';
            ctx.lineWidth = 4; // увеличиваем толщину обводки для лучшей читаемости
            ctx.strokeText(char, charX, textY);
            ctx.fillText(char, charX, textY);
        }
        
        ctx.textAlign = 'start'; // возвращаем стандартное выравнивание
    }

    explode() {
        this.exploding = true;
        for (let i = 0; i < 20; i++) {
            this.particles.push(new Particle(this.x, this.y));
        }
    }
}
