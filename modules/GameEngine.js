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
        this.gameStarted = false; // Флаг для контроля начала игры
        
        // Адаптивные параметры (базовая скорость уменьшена на 25%)
        this.baseSpeed = 0.75; // Было 1, стало 0.75 (-25%)
        this.baseFontSize = 28;
        this.baseImageSize = 200;
        
        // 🎨 АНИМАЦИОННЫЕ ЭФФЕКТЫ
        this.keyPressEffects = []; // Эффекты нажатия клавиш
        this.letterHighlights = []; // Подсветка букв
        this.shootingEffects = []; // Эффекты "выстрелов"
        this.pulseEffects = []; // Эффекты пульсации
        
        // Thematic decorations system
        this.decorations = [];
        this.decorationAnimations = [];
        this.currentTheme = null;
    }

    async initialize() {
        try {
            this.canvas = document.getElementById('gameCanvas');
            this.ctx = this.canvas.getContext('2d');
            this.canvas.width = 800;
            this.canvas.height = 600;
            
            // Инициализируем адаптивные параметры
            this.updateGameScale(this.canvas.width, this.canvas.height);
            
            // Настраиваем обработчики событий ПОСЛЕ того, как DOM готов
            this.setupEventListeners();
            console.log('GameEngine инициализирован, обработчики событий настроены');
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
        
        // Более плавная адаптация скорости (замедлено на 40% + дополнительно на 25%)
        this.baseSpeed = Math.max(0.225, Math.min(0.9, height / 700 * 0.45)); // Уменьшено на 25%
        
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
        
        console.log(`Game scale updated: speed=${this.baseSpeed.toFixed(3)}, fontSize=${this.baseFontSize}, imageSize=${this.baseImageSize}, canvas=${width}x${height}, area=${canvasArea}, device=${isMobile ? 'mobile' : isTablet ? 'tablet' : 'desktop'}`);
    }

    setupEventListeners() {
        // Проверяем существование кнопок перед добавлением обработчиков
        const startButton = document.getElementById('startButton');
        const pauseButton = document.getElementById('pauseButton');
        const stopButton = document.getElementById('stopButton');
        
        console.log('🔧 Настройка обработчиков событий:');
        console.log(`  startButton: ${startButton ? '✅ найдена' : '❌ не найдена'}`);
        console.log(`  pauseButton: ${pauseButton ? '✅ найдена' : '❌ не найдена'}`);
        console.log(`  stopButton: ${stopButton ? '✅ найдена' : '❌ не найдена'}`);
        
        if (startButton) {
            startButton.addEventListener('click', () => {
                this.startGame();
            });
        }
        
        if (pauseButton) {
            pauseButton.addEventListener('click', () => {
                this.pauseGame();
            });
        }
        
        if (stopButton) {
            stopButton.addEventListener('click', () => {
                this.stopGame();
            });
        }
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
        console.log(`🔵 startGame() вызван. isActive: ${this.isActive}, isPaused: ${this.isPaused}, gameStarted: ${this.gameStarted}`);
        
        if (!this.categoryManager.isReadyForGame()) {
            alert(this.languageManager.getText('selectCategory') || 'Выберите категорию для игры');
            return;
        }
        
        // Проверяем смену категории
        this.checkCategoryChange();
        
        if (this.isPaused) {
            // Возобновляем паузу
            console.log('↪️ Возобновляем игру из паузы');
            this.isPaused = false;
            this.resumeGameLoop();
        } else {
            // Начинаем новую игру
            console.log('🚀 Запускаем новую игру');
            this.resetGameState();
            this.isActive = true;
            this.gameStarted = true;
            
            // Initialize theme decorations
            const currentCategoryId = this.categoryManager.getCurrentCategory();
            this.initializeThemeDecorations(currentCategoryId);
            
            this.resumeGameLoop();
        }
        this.updateUI();
        console.log(`✅ Игра запущена. Новое состояние: isActive: ${this.isActive}, isPaused: ${this.isPaused}, gameStarted: ${this.gameStarted}`);
    }

    // Проверка смены категории и очистка экрана
    checkCategoryChange() {
        const currentCategoryId = this.categoryManager.getCurrentCategory();
        if (this.lastCategoryId !== currentCategoryId) {
            console.log(`Категория изменена с ${this.lastCategoryId} на ${currentCategoryId}, очищаем экран`);
            this.clearAllWords();
            this.lastCategoryId = currentCategoryId;
            // При смене категории игра не запускается автоматически
            if (this.isActive && this.gameStarted) {
                // Если игра была активна, останавливаем её
                this.stopGame();
            }
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
        console.log(`🟡 pauseGame() вызван. isActive: ${this.isActive}, isPaused: ${this.isPaused}, gameStarted: ${this.gameStarted}`);
        
        if (!this.isActive) {
            console.log('❌ Игра не активна, пауза невозможна');
            return;
        }
        
        this.isPaused = !this.isPaused;
        
        if (this.isPaused) {
            console.log('⏸️ Игра приостановлена');
            this.stopGameLoop();
        } else {
            console.log('▶️ Игра возобновлена');
            this.resumeGameLoop();
        }
        
        console.log(`✅ Новое состояние: isActive: ${this.isActive}, isPaused: ${this.isPaused}`);
    }

    stopGame() {
        this.isActive = false;
        this.isPaused = false;
        this.gameStarted = false;
        this.stopGameLoop();
        this.resetGameState();
        this.clearCanvas(); // Очищаем канвас при остановке
        this.updateUI();
        console.log('Игра остановлена и сброшена, экран очищен');
    }

    resetGameState() {
        this.words = [];
        this.particles = [];
        this.score = 0; // Сбрасываем очки при остановке
        this.level = 1; // Сбрасываем уровень
        this.input = '';
        this.lastSpawn = 0;
        this.spawnDelay = 2000; // Сбрасываем задержку спавна
        console.log('Игровое состояние сброшено');
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
        
        // Спавн слов происходит только если игра запущена
        if (!this.gameStarted) {
            return;
        }
        
        // Подсчитываем активные (не взрывающиеся) слова
        const activeWords = this.words.filter(word => !word.exploding);
        
        // Спавн нового слова ТОЛЬКО если:
        // 1. На экране НЕТ активных слов
        // 2. Прошло достаточно времени с последнего спавна
        // 3. Игра запущена
        if (activeWords.length === 0 && (timestamp - this.lastSpawn > this.spawnDelay)) {
            this.spawnWord();
            this.lastSpawn = timestamp;
        }
        
        // Обновление слов
        for (let i = this.words.length - 1; i >= 0; i--) {
            const word = this.words[i];
            word.update();
            
            // Удаляем слова которые упали за экран (штраф за пропуск)
            if (word.y > this.canvas.height + 100) {
                if (!word.exploding) {
                    // Штраф за пропущенное слово
                    this.score = Math.max(0, this.score - 5);
                    console.log(`Слово "${word.text}" пропущено, -5 очков. Текущий счет: ${this.score}`);
                    this.updateUI();
                }
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
        
        // 🎨 ОБНОВЛЯЕМ АНИМАЦИОННЫЕ ЭФФЕКТЫ
        this.updateAnimationEffects();
        
        // 🎨 ОБНОВЛЯЕМ АНИМАЦИИ ДЕКОРАЦИЙ
        this.updateDecorationAnimations();
        
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
        
        // Рисуем тематические украшения
        if (this.isActive && this.decorations.length > 0) {
            this.drawDecorations();
        }
        
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
        // Применяем текущую скорость с учетом уровня
        word.speed = this.getCurrentSpeed();
        this.words.push(word);
        console.log(`СПАВН УСПЕШЕН: Заспавнено слово "${wordData.word}" со скоростью ${word.speed.toFixed(3)}. Всего слов: ${this.words.length}`);
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
        if (!this.isActive || this.isPaused || !this.gameStarted) return;
        
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
            
            // 🎯 ПРАВИЛЬНАЯ БУКВА - СОЗДАЕМ ЭФФЕКТЫ
            this.createKeyPressEffect(key, true, activeWord);
            this.createLetterHighlight(activeWord, this.input.length - 1);
            this.createShootingEffect(activeWord, this.input.length - 1);
            
            // Проверяем полное совпадение
            if (this.input.toUpperCase().replace(/\s+/g, ' ') === activeWord.text.toUpperCase()) {
                this.onWordGuessed(activeWord);
            }
        } else {
            // ❌ НЕПРАВИЛЬНАЯ БУКВА - СОЗДАЕМ ЭФФЕКТ ОШИБКИ
            this.createKeyPressEffect(key, false, activeWord);
            this.createErrorEffect(activeWord);
            
            // Неправильная буква - штраф и сброс ввода
            this.score = Math.max(0, this.score - 5);
            this.input = '';
            console.log(`Неправильная буква, -5 очков. Текущий счет: ${this.score}`);
            this.updateUI();
        }
    }

    checkInput() {
        // Эта функция больше не нужна, логика перенесена в handleKeyPress
    }

    onWordGuessed(word) {
        // Простая система очков: +10 за каждое правильно набранное слово
        const points = 10;
        
        this.score += points;
        
        // 🎉 СЛОВО УГАДАНО - СОЗДАЕМ МОЩНЫЕ ЭФФЕКТЫ
        this.createWordCompleteEffect(word);
        this.createPulseEffect(word);
        
        word.explode();
        
        // Создаем частицы
        for (let i = 0; i < 15; i++) {
            this.particles.push(new Particle(word.x, word.y));
        }
        
        this.input = '';
        this.updateUI();
        console.log(`Слово угадано: ${word.text}, +${points} очков. Общий счет: ${this.score}. Текущая скорость: ${this.getCurrentSpeed().toFixed(3)}`);
    }

    updateDifficulty() {
        // Новая система: каждые 300 очков = новый уровень скорости
        const newLevel = Math.floor(this.score / 300) + 1;
        if (newLevel > this.level) {
            this.level = newLevel;
            
            // Обновляем скорость существующих слов
            const newSpeed = this.getCurrentSpeed();
            this.words.forEach(word => {
                word.speed = newSpeed;
            });
            
            console.log(`Уровень скорости повышен до ${this.level} (${this.score} очков). Новая скорость: ${newSpeed.toFixed(3)}`);
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
        if (this.isActive && this.gameStarted) {
            console.log('Игровое состояние обновлено - смена категории, останавливаем игру');
            this.stopGame(); // Останавливаем игру при смене категории
        } else {
            console.log('Игровое состояние обновлено - смена категории, игра не активна');
            this.clearAllWords(); // Просто очищаем экран если игра не запущена
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

    // Новый метод для очистки канваса
    clearCanvas() {
        if (this.ctx) {
            this.ctx.fillStyle = 'black';
            this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
        }
    }

    // Новый метод для расчета текущей скорости
    getCurrentSpeed() {
        // Каждые 300 очков увеличиваем скорость на 10%
        const speedLevel = Math.floor(this.score / 300);
        const speedMultiplier = Math.pow(1.1, speedLevel); // 1.1^n для увеличения на 10% за каждый уровень
        const currentSpeed = this.baseSpeed * speedMultiplier;
        
        // Ограничиваем максимальную скорость
        return Math.min(2.0, currentSpeed);
    }

    // 🎨 ========== АНИМАЦИОННЫЕ ЭФФЕКТЫ ==========

    /**
     * Создает эффект нажатия клавиши
     */
    createKeyPressEffect(key, isCorrect, word) {
        this.keyPressEffects.push({
            key: key,
            x: word.x,
            y: word.y - 50,
            isCorrect: isCorrect,
            life: 30,
            maxLife: 30,
            scale: 1.0,
            alpha: 1.0
        });
    }

    /**
     * Создает подсветку буквы в слове
     */
    createLetterHighlight(word, letterIndex) {
        this.letterHighlights.push({
            word: word,
            letterIndex: letterIndex,
            life: 20,
            maxLife: 20,
            intensity: 1.0
        });
    }

    /**
     * Создает эффект "выстрела" в букву
     */
    createShootingEffect(word, letterIndex) {
        const letterX = this.calculateLetterPosition(word, letterIndex);
        this.shootingEffects.push({
            startX: this.canvas.width / 2,
            startY: this.canvas.height - 100,
            targetX: letterX,
            targetY: word.y + 100,
            currentX: this.canvas.width / 2,
            currentY: this.canvas.height - 100,
            life: 15,
            maxLife: 15,
            speed: 8
        });
    }

    /**
     * Создает эффект ошибки
     */
    createErrorEffect(word) {
        // Красная вспышка вокруг слова
        this.keyPressEffects.push({
            key: '❌',
            x: word.x,
            y: word.y,
            isCorrect: false,
            life: 20,
            maxLife: 20,
            scale: 2.0,
            alpha: 0.8
        });
        
        // Дрожание слова
        word.shakeEffect = {
            life: 15,
            intensity: 5
        };
    }

    /**
     * Создает эффект завершения слова
     */
    createWordCompleteEffect(word) {
        // Золотая вспышка
        this.keyPressEffects.push({
            key: '🎉',
            x: word.x,
            y: word.y,
            isCorrect: true,
            life: 40,
            maxLife: 40,
            scale: 3.0,
            alpha: 1.0
        });
        
        // Звездочки вокруг слова
        for (let i = 0; i < 8; i++) {
            const angle = (i / 8) * Math.PI * 2;
            const distance = 80;
            this.keyPressEffects.push({
                key: '⭐',
                x: word.x + Math.cos(angle) * distance,
                y: word.y + Math.sin(angle) * distance,
                isCorrect: true,
                life: 30,
                maxLife: 30,
                scale: 1.5,
                alpha: 1.0
            });
        }
    }

    /**
     * Создает эффект пульсации
     */
    createPulseEffect(word) {
        this.pulseEffects.push({
            x: word.x,
            y: word.y,
            life: 25,
            maxLife: 25,
            radius: 10,
            maxRadius: 100
        });
    }

    /**
     * Вычисляет позицию буквы в слове
     */
    calculateLetterPosition(word, letterIndex) {
        const fontSize = this.baseFontSize;
        const letterWidth = fontSize * 0.6; // Примерная ширина буквы
        const wordWidth = word.text.length * letterWidth;
        const startX = word.x - wordWidth / 2;
        return startX + letterIndex * letterWidth;
    }

    /**
     * Обновляет все анимационные эффекты
     */
    updateAnimationEffects() {
        // Обновляем эффекты нажатия клавиш
        for (let i = this.keyPressEffects.length - 1; i >= 0; i--) {
            const effect = this.keyPressEffects[i];
            effect.life--;
            effect.alpha = effect.life / effect.maxLife;
            effect.scale = 1.0 + (1 - effect.alpha) * 0.5;
            
            if (effect.life <= 0) {
                this.keyPressEffects.splice(i, 1);
            }
        }

        // Обновляем подсветки букв
        for (let i = this.letterHighlights.length - 1; i >= 0; i--) {
            const highlight = this.letterHighlights[i];
            highlight.life--;
            highlight.intensity = highlight.life / highlight.maxLife;
            
            if (highlight.life <= 0) {
                this.letterHighlights.splice(i, 1);
            }
        }

        // Обновляем эффекты выстрелов
        for (let i = this.shootingEffects.length - 1; i >= 0; i--) {
            const shot = this.shootingEffects[i];
            shot.life--;
            
            // Движение к цели
            const dx = shot.targetX - shot.currentX;
            const dy = shot.targetY - shot.currentY;
            const distance = Math.sqrt(dx * dx + dy * dy);
            
            if (distance > shot.speed) {
                shot.currentX += (dx / distance) * shot.speed;
                shot.currentY += (dy / distance) * shot.speed;
            } else {
                shot.currentX = shot.targetX;
                shot.currentY = shot.targetY;
            }
            
            if (shot.life <= 0) {
                this.shootingEffects.splice(i, 1);
            }
        }

        // Обновляем эффекты пульсации
        for (let i = this.pulseEffects.length - 1; i >= 0; i--) {
            const pulse = this.pulseEffects[i];
            pulse.life--;
            const progress = 1 - (pulse.life / pulse.maxLife);
            pulse.radius = pulse.maxRadius * progress;
            
            if (pulse.life <= 0) {
                this.pulseEffects.splice(i, 1);
            }
        }
    }

    /**
     * Рисует все анимационные эффекты
     */
    drawAnimationEffects() {
        // Рисуем эффекты нажатия клавиш
        this.keyPressEffects.forEach(effect => {
            this.ctx.save();
            this.ctx.globalAlpha = effect.alpha;
            this.ctx.font = `${24 * effect.scale}px Arial`;
            this.ctx.textAlign = 'center';
            this.ctx.fillStyle = effect.isCorrect ? '#00ff00' : '#ff0000';
            this.ctx.fillText(effect.key, effect.x, effect.y);
            this.ctx.restore();
        });

        // Рисуем подсветки букв
        this.letterHighlights.forEach(highlight => {
            if (highlight.word && !highlight.word.exploding) {
                const letterX = this.calculateLetterPosition(highlight.word, highlight.letterIndex);
                const letterY = highlight.word.y + 120;
                
                this.ctx.save();
                this.ctx.globalAlpha = highlight.intensity * 0.5;
                this.ctx.fillStyle = '#ffff00';
                this.ctx.beginPath();
                this.ctx.arc(letterX, letterY, 20, 0, Math.PI * 2);
                this.ctx.fill();
                this.ctx.restore();
            }
        });

        // Рисуем эффекты выстрелов
        this.shootingEffects.forEach(shot => {
            this.ctx.save();
            this.ctx.strokeStyle = '#00ffff';
            this.ctx.lineWidth = 3;
            this.ctx.beginPath();
            this.ctx.moveTo(shot.startX, shot.startY);
            this.ctx.lineTo(shot.currentX, shot.currentY);
            this.ctx.stroke();
            
            // Точка на конце
            this.ctx.fillStyle = '#ffffff';
            this.ctx.beginPath();
            this.ctx.arc(shot.currentX, shot.currentY, 4, 0, Math.PI * 2);
            this.ctx.fill();
            this.ctx.restore();
        });

        // Рисуем эффекты пульсации
        this.pulseEffects.forEach(pulse => {
            this.ctx.save();
            this.ctx.globalAlpha = 0.3 * (pulse.life / pulse.maxLife);
            this.ctx.strokeStyle = '#ffd700';
            this.ctx.lineWidth = 4;
            this.ctx.beginPath();
            this.ctx.arc(pulse.x, pulse.y, pulse.radius, 0, Math.PI * 2);
            this.ctx.stroke();
            this.ctx.restore();
        });
    }

    // Thematic Decorations System
    initializeThemeDecorations(categoryId) {
        this.decorations = [];
        this.decorationAnimations = [];
        this.currentTheme = categoryId;
        
        const themes = {
            'capitals': this.createCapitalsDecorations.bind(this),
            'countries': this.createCountriesDecorations.bind(this),
            'animals': this.createAnimalsDecorations.bind(this),
            'dinosaurs': this.createDinosaursDecorations.bind(this),
            'animal_world': this.createAnimalWorldDecorations.bind(this),
            'footballers': this.createFootballersDecorations.bind(this)
        };
        
        if (themes[categoryId]) {
            themes[categoryId]();
        }
    }
    
    createCapitalsDecorations() {
        // Городские элементы: здания, флаги, звезды
        const decorations = [
            // Здания по краям
            { type: 'building', x: 50, y: 400, width: 40, height: 80, color: '#4a90e2' },
            { type: 'building', x: 100, y: 380, width: 35, height: 100, color: '#357abd' },
            { type: 'building', x: this.canvas.width - 90, y: 390, width: 40, height: 90, color: '#4a90e2' },
            { type: 'building', x: this.canvas.width - 140, y: 370, width: 35, height: 110, color: '#357abd' },
            
            // Флаги
            { type: 'flag', x: 30, y: 50, size: 25, colors: ['#ff6b6b', '#4ecdc4', '#45b7d1'] },
            { type: 'flag', x: this.canvas.width - 55, y: 50, size: 25, colors: ['#96ceb4', '#feca57', '#ff9ff3'] },
            
            // Звезды столиц
            { type: 'star', x: 80, y: 80, size: 8, color: '#ffd700', twinkle: true },
            { type: 'star', x: this.canvas.width - 80, y: 90, size: 8, color: '#ffd700', twinkle: true },
            { type: 'star', x: 120, y: 120, size: 6, color: '#ffed4e', twinkle: true }
        ];
        
        this.decorations = decorations;
    }
    
    createCountriesDecorations() {
        // Географические элементы: горы, облака, компас
        const decorations = [
            // Горы
            { type: 'mountain', x: 20, y: 350, width: 100, height: 80, color: '#8e9aaf' },
            { type: 'mountain', x: 60, y: 370, width: 80, height: 60, color: '#a8b5c8' },
            { type: 'mountain', x: this.canvas.width - 120, y: 360, width: 90, height: 70, color: '#8e9aaf' },
            
            // Облака
            { type: 'cloud', x: 150, y: 60, size: 30, drift: true },
            { type: 'cloud', x: this.canvas.width - 180, y: 80, size: 25, drift: true },
            { type: 'cloud', x: 200, y: 100, size: 20, drift: true },
            
            // Компас
            { type: 'compass', x: this.canvas.width - 60, y: this.canvas.height - 60, size: 40, rotate: true }
        ];
        
        this.decorations = decorations;
    }
    
    createAnimalsDecorations() {
        // Природные элементы: деревья, листья, следы
        const decorations = [
            // Деревья
            { type: 'tree', x: 40, y: 320, width: 30, height: 100, leafColor: '#4caf50' },
            { type: 'tree', x: this.canvas.width - 70, y: 310, width: 35, height: 110, leafColor: '#66bb6a' },
            
            // Кусты
            { type: 'bush', x: 90, y: 400, size: 25, color: '#4caf50' },
            { type: 'bush', x: this.canvas.width - 115, y: 390, size: 30, color: '#66bb6a' },
            
            // Летающие листья
            { type: 'leaf', x: 120, y: 150, size: 8, color: '#4caf50', float: true },
            { type: 'leaf', x: this.canvas.width - 140, y: 180, size: 10, color: '#8bc34a', float: true },
            { type: 'leaf', x: 180, y: 120, size: 6, color: '#66bb6a', float: true },
            
            // Следы животных
            { type: 'pawprint', x: 150, y: 420, size: 12, color: '#8d6e63' },
            { type: 'pawprint', x: 170, y: 430, size: 12, color: '#8d6e63' },
            { type: 'pawprint', x: this.canvas.width - 190, y: 425, size: 12, color: '#8d6e63' }
        ];
        
        this.decorations = decorations;
    }
    
    createDinosaursDecorations() {
        // Доисторические элементы: вулканы, папоротники, метеоры
        const decorations = [
            // Вулканы
            { type: 'volcano', x: 30, y: 350, width: 80, height: 90, active: true },
            { type: 'volcano', x: this.canvas.width - 110, y: 340, width: 70, height: 100, active: false },
            
            // Папоротники
            { type: 'fern', x: 120, y: 380, size: 40, color: '#2e7d32' },
            { type: 'fern', x: this.canvas.width - 160, y: 370, size: 45, color: '#388e3c' },
            
            // Летающие метеоры
            { type: 'meteor', x: 200, y: 80, size: 8, trail: true, speed: 2 },
            { type: 'meteor', x: this.canvas.width - 220, y: 100, size: 6, trail: true, speed: 1.5 },
            
            // Доисторические растения
            { type: 'prehistoric_plant', x: 80, y: 400, size: 35, color: '#1b5e20' },
            { type: 'prehistoric_plant', x: this.canvas.width - 120, y: 410, size: 30, color: '#2e7d32' }
        ];
        
        this.decorations = decorations;
    }
    
    createAnimalWorldDecorations() {
        // Смешанные природные элементы
        const decorations = [
            // Деревья разных типов
            { type: 'tree', x: 35, y: 320, width: 25, height: 90, leafColor: '#4caf50' },
            { type: 'palm_tree', x: this.canvas.width - 65, y: 300, height: 120, leafColor: '#66bb6a' },
            
            // Цветы
            { type: 'flower', x: 100, y: 420, size: 15, color: '#e91e63' },
            { type: 'flower', x: 130, y: 410, size: 12, color: '#9c27b0' },
            { type: 'flower', x: this.canvas.width - 130, y: 415, size: 14, color: '#ff5722' },
            
            // Бабочки
            { type: 'butterfly', x: 160, y: 200, size: 12, colors: ['#ff9800', '#ffeb3b'], flutter: true },
            { type: 'butterfly', x: this.canvas.width - 180, y: 180, size: 10, colors: ['#e91e63', '#9c27b0'], flutter: true },
            
            // Солнце
            { type: 'sun', x: this.canvas.width - 80, y: 80, size: 30, rays: true }
        ];
        
        this.decorations = decorations;
    }

    createFootballersDecorations() {
        // Футбольные элементы: поле, мячи, ворота, стадион
        const decorations = [
            // Футбольное поле (трава)
            { type: 'grass', x: 0, y: this.canvas.height - 30, width: this.canvas.width, height: 30 },
            
            // Футбольные мячи
            { type: 'football', x: 80, y: this.canvas.height - 60, size: 25, bounce: true },
            { type: 'football', x: this.canvas.width - 120, y: this.canvas.height - 55, size: 20, bounce: true },
            
            // Ворота
            { type: 'goal', x: 30, y: this.canvas.height - 100, width: 60, height: 40 },
            { type: 'goal', x: this.canvas.width - 90, y: this.canvas.height - 100, width: 60, height: 40 },
            
            // Флаги команд (размещаем по краям как в категории столиц)
            { type: 'team_flag', x: 30, y: 50, size: 25, colors: ['#ff0000', '#ffffff', '#0000ff'] },
            { type: 'team_flag', x: this.canvas.width - 55, y: 60, size: 25, colors: ['#ffff00', '#008000'] },
            
            // Стадионные огни (только по краям)
            { type: 'stadium_light', x: 50, y: 30, size: 15 },
            { type: 'stadium_light', x: this.canvas.width - 50, y: 30, size: 15 },
            
            // Небольшие трибуны только по краям (убираем полосу на весь экран)
            { type: 'stadium', x: 10, y: 20, width: 80, height: 25 },
            { type: 'stadium', x: this.canvas.width - 90, y: 20, width: 80, height: 25 },
            
            // Конфетти
            { type: 'confetti', x: -10, y: 100, size: 3, colors: ['#ff0000', '#00ff00', '#0000ff', '#ffff00'], float: true },
            { type: 'confetti', x: -15, y: 150, size: 4, colors: ['#ff69b4', '#00ffff', '#ffa500'], float: true }
        ];
        
        this.decorations = decorations;
    }
    
    updateDecorationAnimations() {
        const time = Date.now() * 0.001; // Время в секундах для плавной анимации
        
        this.decorations.forEach(decoration => {
            // Инициализируем анимационные параметры если их нет
            if (!decoration.animTime) decoration.animTime = Math.random() * Math.PI * 2;
            if (!decoration.baseY) decoration.baseY = decoration.y;
            if (!decoration.baseX) decoration.baseX = decoration.x;
            
            switch (decoration.type) {
                case 'cloud':
                    if (decoration.drift) {
                        decoration.x += 0.3 + Math.sin(time * 0.5) * 0.1; // Переменная скорость
                        decoration.y = decoration.baseY + Math.sin(time * 0.3 + decoration.animTime) * 5; // Вертикальное покачивание
                        if (decoration.x > this.canvas.width + 80) {
                            decoration.x = -80;
                            decoration.baseY = 50 + Math.random() * 100;
                        }
                    }
                    break;
                    
                case 'leaf':
                    if (decoration.float) {
                        decoration.x += 0.2 + Math.sin(time * 0.8 + decoration.animTime) * 0.1;
                        decoration.y = decoration.baseY + Math.sin(time * 1.2 + decoration.animTime) * 8; // Более выраженное покачивание
                        decoration.rotation = (decoration.rotation || 0) + 0.02; // Вращение листьев
                        if (decoration.x > this.canvas.width + 30) {
                            decoration.x = -30;
                            decoration.baseY = 100 + Math.random() * 150;
                        }
                    }
                    break;
                    
                case 'meteor':
                    if (decoration.trail) {
                        decoration.x += decoration.speed * (1 + Math.sin(time * 2) * 0.1);
                        decoration.y += decoration.speed * 0.5;
                        // Добавляем мерцание
                        decoration.opacity = 0.7 + Math.sin(time * 8 + decoration.animTime) * 0.3;
                        if (decoration.x > this.canvas.width + 100) {
                            decoration.x = -100;
                            decoration.y = 30 + Math.random() * 120;
                            decoration.opacity = 1;
                        }
                    }
                    break;
                    
                case 'butterfly':
                    if (decoration.flutter) {
                        // Более реалистичный полет бабочки
                        decoration.x += Math.sin(time * 2 + decoration.animTime) * 1.5 + 0.3;
                        decoration.y = decoration.baseY + Math.cos(time * 3 + decoration.animTime) * 12;
                        decoration.wingPhase = time * 15 + decoration.animTime; // Быстрое махание крыльями
                        if (decoration.x > this.canvas.width + 40) {
                            decoration.x = -40;
                            decoration.baseY = 100 + Math.random() * 200;
                        }
                    }
                    break;
                    
                case 'compass':
                    if (decoration.rotate) {
                        decoration.rotation = time * 0.5 + decoration.animTime; // Плавное вращение
                        decoration.glow = 0.5 + Math.sin(time * 2) * 0.3; // Пульсирующее свечение
                    }
                    break;
                    
                case 'star':
                    if (decoration.twinkle) {
                        decoration.brightness = 0.4 + Math.sin(time * 3 + decoration.animTime) * 0.6;
                        decoration.scale = 0.8 + Math.sin(time * 2 + decoration.animTime) * 0.3;
                    }
                    break;
                    
                case 'flag':
                    // Развевание флага
                    decoration.wave = time * 4 + decoration.animTime;
                    break;
                    
                case 'building':
                    // Мерцание окон
                    if (!decoration.windowStates) {
                        decoration.windowStates = Array(9).fill().map(() => Math.random() > 0.5);
                    }
                    if (Math.random() < 0.02) { // 2% шанс изменения каждый кадр
                        decoration.windowStates[Math.floor(Math.random() * decoration.windowStates.length)] = Math.random() > 0.3;
                    }
                    break;
                    
                case 'volcano':
                    // Пульсирующая лава
                    decoration.lavaGlow = 0.6 + Math.sin(time * 2 + decoration.animTime) * 0.4;
                    // Случайные искры
                    if (Math.random() < 0.1) {
                        if (!decoration.sparks) decoration.sparks = [];
                        decoration.sparks.push({
                            x: decoration.x + decoration.width * 0.5 + (Math.random() - 0.5) * 20,
                            y: decoration.y,
                            vx: (Math.random() - 0.5) * 4,
                            vy: -Math.random() * 6 - 2,
                            life: 1,
                            decay: 0.02
                        });
                    }
                    // Обновляем искры
                    if (decoration.sparks) {
                        decoration.sparks = decoration.sparks.filter(spark => {
                            spark.x += spark.vx;
                            spark.y += spark.vy;
                            spark.vy += 0.1; // Гравитация
                            spark.life -= spark.decay;
                            return spark.life > 0;
                        });
                    }
                    break;
                    
                case 'sun':
                    // Пульсирующее солнце с лучами
                    decoration.pulse = 0.9 + Math.sin(time * 1.5) * 0.1;
                    decoration.rayRotation = time * 0.3;
                    break;
                    
                case 'flower':
                    // Легкое покачивание цветов
                    decoration.sway = Math.sin(time * 1.5 + decoration.animTime) * 2;
                    break;
                    
                case 'tree':
                case 'palm_tree':
                    // Покачивание деревьев
                    decoration.sway = Math.sin(time * 0.8 + decoration.animTime) * 3;
                    break;
                    
                case 'football':
                    // Прыгающий мяч
                    if (decoration.bounce) {
                        decoration.y = decoration.baseY + Math.abs(Math.sin(time * 3 + decoration.animTime)) * 20;
                        decoration.rotation = (decoration.rotation || 0) + 0.1;
                    }
                    break;
                    
                case 'stadium_light':
                    // Мерцающие огни стадиона
                    decoration.brightness = 0.7 + Math.sin(time * 4 + decoration.animTime) * 0.3;
                    break;
                    
                case 'confetti':
                    // Падающее конфетти
                    if (decoration.float) {
                        decoration.x += 0.5 + Math.sin(time * 1.5 + decoration.animTime) * 0.3;
                        decoration.y = decoration.baseY + Math.sin(time * 2 + decoration.animTime) * 15;
                        decoration.rotation = (decoration.rotation || 0) + 0.05;
                        if (decoration.x > this.canvas.width + 20) {
                            decoration.x = -20;
                            decoration.baseY = 80 + Math.random() * 100;
                        }
                    }
                    break;
                    
                case 'team_flag':
                    // Развевание флагов команд
                    decoration.wave = time * 5 + decoration.animTime;
                    break;
            }
        });
    }
    
    drawDecorations() {
        this.decorations.forEach(decoration => {
            this.ctx.save();
            
            switch (decoration.type) {
                case 'building':
                    this.drawBuilding(decoration);
                    break;
                case 'flag':
                    this.drawFlag(decoration);
                    break;
                case 'star':
                    this.drawStar(decoration);
                    break;
                case 'mountain':
                    this.drawMountain(decoration);
                    break;
                case 'cloud':
                    this.drawCloud(decoration);
                    break;
                case 'compass':
                    this.drawCompass(decoration);
                    break;
                case 'tree':
                    this.drawTree(decoration);
                    break;
                case 'palm_tree':
                    this.drawPalmTree(decoration);
                    break;
                case 'bush':
                    this.drawBush(decoration);
                    break;
                case 'leaf':
                    this.drawLeaf(decoration);
                    break;
                case 'pawprint':
                    this.drawPawprint(decoration);
                    break;
                case 'volcano':
                    this.drawVolcano(decoration);
                    break;
                case 'fern':
                    this.drawFern(decoration);
                    break;
                case 'meteor':
                    this.drawMeteor(decoration);
                    break;
                case 'prehistoric_plant':
                    this.drawPrehistoricPlant(decoration);
                    break;
                case 'flower':
                    this.drawFlower(decoration);
                    break;
                case 'butterfly':
                    this.drawButterfly(decoration);
                    break;
                case 'sun':
                    this.drawSun(decoration);
                    break;
                case 'grass':
                    this.drawGrass(decoration);
                    break;
                case 'football':
                    this.drawFootball(decoration);
                    break;
                case 'goal':
                    this.drawGoal(decoration);
                    break;
                case 'team_flag':
                    this.drawTeamFlag(decoration);
                    break;
                case 'stadium_light':
                    this.drawStadiumLight(decoration);
                    break;
                case 'stadium':
                    this.drawStadium(decoration);
                    break;
                case 'confetti':
                    this.drawConfetti(decoration);
                    break;
            }
            
            this.ctx.restore();
        });
    }
    
    // Drawing methods for different decoration types
    drawBuilding(decoration) {
        // Тень здания
        this.ctx.fillStyle = 'rgba(0, 0, 0, 0.3)';
        this.ctx.fillRect(decoration.x + 3, decoration.y + 3, decoration.width, decoration.height);
        
        // Градиент для здания
        const gradient = this.ctx.createLinearGradient(
            decoration.x, decoration.y, 
            decoration.x + decoration.width, decoration.y
        );
        gradient.addColorStop(0, decoration.color);
        gradient.addColorStop(1, this.darkenColor(decoration.color, 0.3));
        
        this.ctx.fillStyle = gradient;
        this.ctx.fillRect(decoration.x, decoration.y, decoration.width, decoration.height);
        
        // Окна с анимацией
        const windowStates = decoration.windowStates || Array(9).fill(true);
        for (let i = 0; i < 3; i++) {
            for (let j = 0; j < Math.floor(decoration.height / 20); j++) {
                const windowIndex = i + j * 3;
                if (windowIndex < windowStates.length && windowStates[windowIndex]) {
                    // Светящиеся окна
                    this.ctx.shadowColor = '#ffeb3b';
                    this.ctx.shadowBlur = 5;
                    this.ctx.fillStyle = '#ffeb3b';
                } else {
                    // Темные окна
                    this.ctx.shadowBlur = 0;
                    this.ctx.fillStyle = '#2c3e50';
                }
                
                this.ctx.fillRect(
                    decoration.x + 5 + i * 10,
                    decoration.y + 10 + j * 15,
                    6, 8
                );
            }
        }
        this.ctx.shadowBlur = 0;
    }
    
    drawFlag(decoration) {
        // Флагшток с тенью
        this.ctx.strokeStyle = 'rgba(0, 0, 0, 0.3)';
        this.ctx.lineWidth = 4;
        this.ctx.beginPath();
        this.ctx.moveTo(decoration.x + 2, decoration.y + 2);
        this.ctx.lineTo(decoration.x + 2, decoration.y + 62);
        this.ctx.stroke();
        
        this.ctx.strokeStyle = '#8d6e63';
        this.ctx.lineWidth = 3;
        this.ctx.beginPath();
        this.ctx.moveTo(decoration.x, decoration.y);
        this.ctx.lineTo(decoration.x, decoration.y + 60);
        this.ctx.stroke();
        
        // Развевающийся флаг
        const wave = decoration.wave || 0;
        decoration.colors.forEach((color, index) => {
            this.ctx.fillStyle = color;
            
            // Создаем волнистый эффект
            this.ctx.beginPath();
            const y = decoration.y + index * 8;
            const segments = 8;
            
            for (let i = 0; i <= segments; i++) {
                const x = decoration.x + 3 + (i / segments) * decoration.size;
                const waveOffset = Math.sin(wave + i * 0.5) * 3;
                const waveY = y + waveOffset;
                
                if (i === 0) {
                    this.ctx.moveTo(x, y);
                    this.ctx.lineTo(x, y + 8);
                } else if (i === segments) {
                    this.ctx.lineTo(x, waveY + 8);
                    this.ctx.lineTo(x, waveY);
                } else {
                    this.ctx.lineTo(x, waveY);
                }
            }
            
            // Замыкаем контур
            for (let i = segments; i >= 0; i--) {
                const x = decoration.x + 3 + (i / segments) * decoration.size;
                const waveOffset = Math.sin(wave + i * 0.5) * 3;
                const waveY = y + waveOffset;
                this.ctx.lineTo(x, waveY + 8);
            }
            
            this.ctx.closePath();
            this.ctx.fill();
        });
    }
    
    drawStar(decoration) {
        const brightness = decoration.brightness || 1;
        const scale = decoration.scale || 1;
        const size = decoration.size * scale;
        
        // Свечение звезды
        if (decoration.twinkle) {
            this.ctx.shadowColor = decoration.color;
            this.ctx.shadowBlur = 10 * brightness;
        }
        
        this.ctx.globalAlpha = brightness;
        this.ctx.fillStyle = decoration.color;
        this.ctx.beginPath();
        
        // Рисуем 5-конечную звезду
        for (let i = 0; i < 10; i++) {
            const angle = (i * Math.PI) / 5;
            const radius = i % 2 === 0 ? size : size * 0.4;
            const x = decoration.x + Math.cos(angle) * radius;
            const y = decoration.y + Math.sin(angle) * radius;
            
            if (i === 0) this.ctx.moveTo(x, y);
            else this.ctx.lineTo(x, y);
        }
        
        this.ctx.closePath();
        this.ctx.fill();
        this.ctx.shadowBlur = 0;
        this.ctx.globalAlpha = 1;
    }
    
    drawMountain(decoration) {
        this.ctx.fillStyle = decoration.color;
        this.ctx.beginPath();
        this.ctx.moveTo(decoration.x, decoration.y + decoration.height);
        this.ctx.lineTo(decoration.x + decoration.width / 2, decoration.y);
        this.ctx.lineTo(decoration.x + decoration.width, decoration.y + decoration.height);
        this.ctx.closePath();
        this.ctx.fill();
        
        // Snow cap
        this.ctx.fillStyle = '#ffffff';
        this.ctx.beginPath();
        this.ctx.moveTo(decoration.x + decoration.width * 0.3, decoration.y + decoration.height * 0.3);
        this.ctx.lineTo(decoration.x + decoration.width / 2, decoration.y);
        this.ctx.lineTo(decoration.x + decoration.width * 0.7, decoration.y + decoration.height * 0.3);
        this.ctx.closePath();
        this.ctx.fill();
    }
    
    drawCloud(decoration) {
        this.ctx.fillStyle = '#ffffff';
        this.ctx.globalAlpha = 0.8;
        
        // Cloud circles
        for (let i = 0; i < 4; i++) {
            this.ctx.beginPath();
            this.ctx.arc(
                decoration.x + i * decoration.size * 0.3,
                decoration.y + Math.sin(i) * decoration.size * 0.2,
                decoration.size * (0.4 + i * 0.1),
                0, 2 * Math.PI
            );
            this.ctx.fill();
        }
        
        this.ctx.globalAlpha = 1;
    }
    
    drawCompass(decoration) {
        this.ctx.translate(decoration.x, decoration.y);
        if (decoration.rotation) {
            this.ctx.rotate(decoration.rotation);
        }
        
        // Compass body
        this.ctx.fillStyle = '#8d6e63';
        this.ctx.beginPath();
        this.ctx.arc(0, 0, decoration.size, 0, 2 * Math.PI);
        this.ctx.fill();
        
        // Compass needle
        this.ctx.fillStyle = '#f44336';
        this.ctx.beginPath();
        this.ctx.moveTo(0, -decoration.size * 0.7);
        this.ctx.lineTo(-decoration.size * 0.1, 0);
        this.ctx.lineTo(decoration.size * 0.1, 0);
        this.ctx.closePath();
        this.ctx.fill();
        
        // N marker
        this.ctx.fillStyle = '#ffffff';
        this.ctx.font = '12px Arial';
        this.ctx.textAlign = 'center';
        this.ctx.fillText('N', 0, -decoration.size * 0.5);
    }
    
    drawTree(decoration) {
        // Trunk
        this.ctx.fillStyle = '#8d6e63';
        this.ctx.fillRect(
            decoration.x - decoration.width * 0.1,
            decoration.y,
            decoration.width * 0.2,
            decoration.height * 0.6
        );
        
        // Leaves
        this.ctx.fillStyle = decoration.leafColor;
        this.ctx.beginPath();
        this.ctx.arc(
            decoration.x,
            decoration.y - decoration.height * 0.2,
            decoration.width * 0.6,
            0, 2 * Math.PI
        );
        this.ctx.fill();
    }
    
    drawPalmTree(decoration) {
        // Trunk
        this.ctx.strokeStyle = '#8d6e63';
        this.ctx.lineWidth = 8;
        this.ctx.beginPath();
        this.ctx.moveTo(decoration.x, decoration.y + decoration.height);
        this.ctx.quadraticCurveTo(
            decoration.x + 20,
            decoration.y + decoration.height * 0.5,
            decoration.x,
            decoration.y
        );
        this.ctx.stroke();
        
        // Palm leaves
        this.ctx.strokeStyle = decoration.leafColor;
        this.ctx.lineWidth = 4;
        for (let i = 0; i < 6; i++) {
            const angle = (i * Math.PI) / 3;
            this.ctx.beginPath();
            this.ctx.moveTo(decoration.x, decoration.y);
            this.ctx.lineTo(
                decoration.x + Math.cos(angle) * 40,
                decoration.y + Math.sin(angle) * 20
            );
            this.ctx.stroke();
        }
    }
    
    drawBush(decoration) {
        this.ctx.fillStyle = decoration.color;
        
        // Multiple circles for bush shape
        for (let i = 0; i < 3; i++) {
            this.ctx.beginPath();
            this.ctx.arc(
                decoration.x + (i - 1) * decoration.size * 0.3,
                decoration.y + Math.sin(i) * decoration.size * 0.2,
                decoration.size * (0.6 + i * 0.1),
                0, 2 * Math.PI
            );
            this.ctx.fill();
        }
    }
    
    drawLeaf(decoration) {
        this.ctx.fillStyle = decoration.color;
        this.ctx.beginPath();
        this.ctx.ellipse(decoration.x, decoration.y, decoration.size, decoration.size * 0.6, 
                        Math.PI / 4, 0, 2 * Math.PI);
        this.ctx.fill();
    }
    
    drawPawprint(decoration) {
        this.ctx.fillStyle = decoration.color;
        
        // Main pad
        this.ctx.beginPath();
        this.ctx.ellipse(decoration.x, decoration.y, decoration.size * 0.6, decoration.size * 0.8, 0, 0, 2 * Math.PI);
        this.ctx.fill();
        
        // Toes
        for (let i = 0; i < 4; i++) {
            const angle = (i * Math.PI) / 6 - Math.PI / 4;
            this.ctx.beginPath();
            this.ctx.arc(
                decoration.x + Math.cos(angle) * decoration.size * 0.8,
                decoration.y - Math.sin(angle) * decoration.size * 0.8,
                decoration.size * 0.25,
                0, 2 * Math.PI
            );
            this.ctx.fill();
        }
    }
    
    drawVolcano(decoration) {
        // Тень вулкана
        this.ctx.fillStyle = 'rgba(0, 0, 0, 0.3)';
        this.ctx.beginPath();
        this.ctx.moveTo(decoration.x + 3, decoration.y + decoration.height + 3);
        this.ctx.lineTo(decoration.x + decoration.width * 0.2 + 3, decoration.y + 3);
        this.ctx.lineTo(decoration.x + decoration.width * 0.8 + 3, decoration.y + 3);
        this.ctx.lineTo(decoration.x + decoration.width + 3, decoration.y + decoration.height + 3);
        this.ctx.closePath();
        this.ctx.fill();
        
        // Тело вулкана с градиентом
        const volcanoGradient = this.ctx.createLinearGradient(
            decoration.x, decoration.y,
            decoration.x + decoration.width, decoration.y
        );
        volcanoGradient.addColorStop(0, '#6d4c41');
        volcanoGradient.addColorStop(0.5, decoration.color || '#8d6e63');
        volcanoGradient.addColorStop(1, '#5d4037');
        
        this.ctx.fillStyle = volcanoGradient;
        this.ctx.beginPath();
        this.ctx.moveTo(decoration.x, decoration.y + decoration.height);
        this.ctx.lineTo(decoration.x + decoration.width * 0.2, decoration.y);
        this.ctx.lineTo(decoration.x + decoration.width * 0.8, decoration.y);
        this.ctx.lineTo(decoration.x + decoration.width, decoration.y + decoration.height);
        this.ctx.closePath();
        this.ctx.fill();
        
        // Пульсирующая лава
        const lavaGlow = decoration.lavaGlow || 1;
        const lavaGradient = this.ctx.createRadialGradient(
            decoration.x + decoration.width * 0.5, decoration.y,
            0,
            decoration.x + decoration.width * 0.5, decoration.y,
            decoration.width * 0.3
        );
        lavaGradient.addColorStop(0, `rgba(255, 193, 7, ${lavaGlow})`);
        lavaGradient.addColorStop(0.5, `rgba(255, 87, 34, ${lavaGlow * 0.8})`);
        lavaGradient.addColorStop(1, `rgba(183, 28, 28, ${lavaGlow * 0.6})`);
        
        this.ctx.fillStyle = lavaGradient;
        this.ctx.fillRect(
            decoration.x + decoration.width * 0.3,
            decoration.y,
            decoration.width * 0.4,
            decoration.height * 0.3
        );
        
        // Рисуем искры
        if (decoration.sparks) {
            decoration.sparks.forEach(spark => {
                this.ctx.globalAlpha = spark.life;
                this.ctx.fillStyle = `hsl(${30 + Math.random() * 30}, 100%, 60%)`;
                this.ctx.beginPath();
                this.ctx.arc(spark.x, spark.y, 2, 0, Math.PI * 2);
                this.ctx.fill();
            });
            this.ctx.globalAlpha = 1;
        }
    }
    
    drawFern(decoration) {
        this.ctx.strokeStyle = decoration.color;
        this.ctx.lineWidth = 3;
        
        // Main stem
        this.ctx.beginPath();
        this.ctx.moveTo(decoration.x, decoration.y + decoration.size);
        this.ctx.lineTo(decoration.x, decoration.y);
        this.ctx.stroke();
        
        // Fronds
        this.ctx.lineWidth = 1;
        for (let i = 0; i < 8; i++) {
            const y = decoration.y + (i * decoration.size) / 8;
            const length = decoration.size * 0.3 * (1 - i / 8);
            
            this.ctx.beginPath();
            this.ctx.moveTo(decoration.x, y);
            this.ctx.lineTo(decoration.x - length, y - length * 0.3);
            this.ctx.moveTo(decoration.x, y);
            this.ctx.lineTo(decoration.x + length, y - length * 0.3);
            this.ctx.stroke();
        }
    }
    
    drawMeteor(decoration) {
        // Meteor body
        this.ctx.fillStyle = '#ffeb3b';
        this.ctx.beginPath();
        this.ctx.arc(decoration.x, decoration.y, decoration.size, 0, 2 * Math.PI);
        this.ctx.fill();
        
        // Trail
        if (decoration.trail) {
            this.ctx.strokeStyle = '#ff9800';
            this.ctx.lineWidth = decoration.size;
            this.ctx.globalAlpha = 0.5;
            this.ctx.beginPath();
            this.ctx.moveTo(decoration.x - 20, decoration.y - 10);
            this.ctx.lineTo(decoration.x, decoration.y);
            this.ctx.stroke();
            this.ctx.globalAlpha = 1;
        }
    }
    
    drawPrehistoricPlant(decoration) {
        this.ctx.strokeStyle = decoration.color;
        this.ctx.lineWidth = 4;
        
        // Main stem
        this.ctx.beginPath();
        this.ctx.moveTo(decoration.x, decoration.y + decoration.size);
        this.ctx.quadraticCurveTo(
            decoration.x + decoration.size * 0.3,
            decoration.y + decoration.size * 0.5,
            decoration.x,
            decoration.y
        );
        this.ctx.stroke();
        
        // Large leaves
        this.ctx.fillStyle = decoration.color;
        for (let i = 0; i < 3; i++) {
            const y = decoration.y + (i * decoration.size) / 3;
            this.ctx.beginPath();
            this.ctx.ellipse(decoration.x + decoration.size * 0.3, y, 
                           decoration.size * 0.4, decoration.size * 0.2, 0, 0, 2 * Math.PI);
            this.ctx.fill();
        }
    }
    
    drawFlower(decoration) {
        // Petals
        this.ctx.fillStyle = decoration.color;
        for (let i = 0; i < 6; i++) {
            const angle = (i * Math.PI) / 3;
            this.ctx.beginPath();
            this.ctx.ellipse(
                decoration.x + Math.cos(angle) * decoration.size * 0.5,
                decoration.y + Math.sin(angle) * decoration.size * 0.5,
                decoration.size * 0.4, decoration.size * 0.2, angle, 0, 2 * Math.PI
            );
            this.ctx.fill();
        }
        
        // Center
        this.ctx.fillStyle = '#ffeb3b';
        this.ctx.beginPath();
        this.ctx.arc(decoration.x, decoration.y, decoration.size * 0.3, 0, 2 * Math.PI);
        this.ctx.fill();
    }
    
    drawButterfly(decoration) {
        const wingPhase = decoration.wingPhase || 0;
        const wingScale = 0.8 + Math.sin(wingPhase) * 0.3; // Анимация махания крыльями
        
        // Тень бабочки
        this.ctx.fillStyle = 'rgba(0, 0, 0, 0.2)';
        this.ctx.beginPath();
        this.ctx.ellipse(decoration.x + 2, decoration.y + decoration.size * 0.8, 
                        decoration.size * 0.6, decoration.size * 0.2, 0, 0, 2 * Math.PI);
        this.ctx.fill();
        
        // Крылья с анимацией
        decoration.colors.forEach((color, index) => {
            const wingGradient = this.ctx.createRadialGradient(
                decoration.x, decoration.y, 0,
                decoration.x, decoration.y, decoration.size
            );
            wingGradient.addColorStop(0, color);
            wingGradient.addColorStop(1, this.darkenColor(color, 0.3));
            
            this.ctx.fillStyle = wingGradient;
            
            // Верхние крылья с анимацией
            this.ctx.save();
            this.ctx.translate(decoration.x, decoration.y);
            this.ctx.scale(wingScale, 1);
            this.ctx.beginPath();
            this.ctx.ellipse(
                (index === 0 ? -decoration.size * 0.3 : decoration.size * 0.3),
                -decoration.size * 0.2,
                decoration.size * 0.4, decoration.size * 0.6, 0, 0, 2 * Math.PI
            );
            this.ctx.fill();
            this.ctx.restore();
            
            // Нижние крылья
            this.ctx.save();
            this.ctx.translate(decoration.x, decoration.y);
            this.ctx.scale(wingScale * 0.8, 1);
            this.ctx.beginPath();
            this.ctx.ellipse(
                (index === 0 ? -decoration.size * 0.2 : decoration.size * 0.2),
                decoration.size * 0.2,
                decoration.size * 0.3, decoration.size * 0.4, 0, 0, 2 * Math.PI
            );
            this.ctx.fill();
            this.ctx.restore();
            
            // Узоры на крыльях
            this.ctx.fillStyle = 'rgba(255, 255, 255, 0.6)';
            this.ctx.beginPath();
            this.ctx.arc(
                decoration.x + (index === 0 ? -decoration.size * 0.2 : decoration.size * 0.2),
                decoration.y - decoration.size * 0.1,
                decoration.size * 0.1, 0, 2 * Math.PI
            );
            this.ctx.fill();
        });
        
        // Тело бабочки с градиентом
        const bodyGradient = this.ctx.createLinearGradient(
            decoration.x, decoration.y - decoration.size * 0.5,
            decoration.x, decoration.y + decoration.size * 0.5
        );
        bodyGradient.addColorStop(0, '#6d4c41');
        bodyGradient.addColorStop(1, '#3e2723');
        
        this.ctx.strokeStyle = bodyGradient;
        this.ctx.lineWidth = 3;
        this.ctx.beginPath();
        this.ctx.moveTo(decoration.x, decoration.y - decoration.size * 0.5);
        this.ctx.lineTo(decoration.x, decoration.y + decoration.size * 0.5);
        this.ctx.stroke();
        
        // Усики
        this.ctx.strokeStyle = '#3e2723';
        this.ctx.lineWidth = 1;
        this.ctx.beginPath();
        this.ctx.moveTo(decoration.x - 2, decoration.y - decoration.size * 0.4);
        this.ctx.lineTo(decoration.x - 5, decoration.y - decoration.size * 0.6);
        this.ctx.moveTo(decoration.x + 2, decoration.y - decoration.size * 0.4);
        this.ctx.lineTo(decoration.x + 5, decoration.y - decoration.size * 0.6);
        this.ctx.stroke();
    }
    
    // Вспомогательная функция для затемнения цветов
    darkenColor(color, factor) {
        if (color.startsWith('#')) {
            const r = parseInt(color.slice(1, 3), 16);
            const g = parseInt(color.slice(3, 5), 16);
            const b = parseInt(color.slice(5, 7), 16);
            return `rgb(${Math.floor(r * (1 - factor))}, ${Math.floor(g * (1 - factor))}, ${Math.floor(b * (1 - factor))})`;
        }
        return color;
    }

    drawSun(decoration) {
        const pulse = decoration.pulse || 1;
        const rayRotation = decoration.rayRotation || 0;
        
        // Свечение солнца
        const gradient = this.ctx.createRadialGradient(
            decoration.x, decoration.y, 0,
            decoration.x, decoration.y, decoration.size * pulse * 2
        );
        gradient.addColorStop(0, 'rgba(255, 235, 59, 0.8)');
        gradient.addColorStop(0.5, 'rgba(255, 193, 7, 0.4)');
        gradient.addColorStop(1, 'rgba(255, 193, 7, 0)');
        
        this.ctx.fillStyle = gradient;
        this.ctx.beginPath();
        this.ctx.arc(decoration.x, decoration.y, decoration.size * pulse * 2, 0, Math.PI * 2);
        this.ctx.fill();
        
        // Основное солнце с градиентом
        const sunGradient = this.ctx.createRadialGradient(
            decoration.x - decoration.size * 0.3, decoration.y - decoration.size * 0.3, 0,
            decoration.x, decoration.y, decoration.size * pulse
        );
        sunGradient.addColorStop(0, '#fff59d');
        sunGradient.addColorStop(1, '#ffb300');
        
        this.ctx.fillStyle = sunGradient;
        this.ctx.beginPath();
        this.ctx.arc(decoration.x, decoration.y, decoration.size * pulse, 0, Math.PI * 2);
        this.ctx.fill();
        
        // Анимированные лучи
        if (decoration.rays) {
            this.ctx.strokeStyle = '#ffeb3b';
            this.ctx.lineWidth = 2;
            this.ctx.globalAlpha = 0.8;
            
            for (let i = 0; i < 12; i++) {
                const angle = (i * Math.PI) / 6 + rayRotation;
                const rayLength = decoration.size + 10 + Math.sin(rayRotation * 3 + i) * 5;
                const startX = decoration.x + Math.cos(angle) * (decoration.size * pulse + 3);
                const startY = decoration.y + Math.sin(angle) * (decoration.size * pulse + 3);
                const endX = decoration.x + Math.cos(angle) * rayLength;
                const endY = decoration.y + Math.sin(angle) * rayLength;
                
                this.ctx.beginPath();
                this.ctx.moveTo(startX, startY);
                this.ctx.lineTo(endX, endY);
                this.ctx.stroke();
            }
            this.ctx.globalAlpha = 1;
        }
    }

    // Методы рисования футбольных элементов
    drawGrass(decoration) {
        // Градиент травы
        const grassGradient = this.ctx.createLinearGradient(
            decoration.x, decoration.y,
            decoration.x, decoration.y + decoration.height
        );
        grassGradient.addColorStop(0, '#4caf50');
        grassGradient.addColorStop(1, '#2e7d32');
        
        this.ctx.fillStyle = grassGradient;
        this.ctx.fillRect(decoration.x, decoration.y, decoration.width, decoration.height);
        
        // Полоски на поле
        this.ctx.strokeStyle = 'rgba(255, 255, 255, 0.3)';
        this.ctx.lineWidth = 2;
        for (let i = 0; i < decoration.width; i += 50) {
            this.ctx.beginPath();
            this.ctx.moveTo(decoration.x + i, decoration.y);
            this.ctx.lineTo(decoration.x + i, decoration.y + decoration.height);
            this.ctx.stroke();
        }
    }

    drawFootball(decoration) {
        const rotation = decoration.rotation || 0;
        
        // Тень мяча
        this.ctx.fillStyle = 'rgba(0, 0, 0, 0.3)';
        this.ctx.beginPath();
        this.ctx.ellipse(decoration.x + 3, decoration.y + decoration.size + 5, 
                        decoration.size * 0.8, decoration.size * 0.3, 0, 0, 2 * Math.PI);
        this.ctx.fill();
        
        // Основа мяча
        this.ctx.fillStyle = '#ffffff';
        this.ctx.beginPath();
        this.ctx.arc(decoration.x, decoration.y, decoration.size, 0, 2 * Math.PI);
        this.ctx.fill();
        
        // Черные пятна (пентагоны)
        this.ctx.save();
        this.ctx.translate(decoration.x, decoration.y);
        this.ctx.rotate(rotation);
        
        this.ctx.fillStyle = '#000000';
        for (let i = 0; i < 5; i++) {
            const angle = (i * 2 * Math.PI) / 5;
            const x = Math.cos(angle) * decoration.size * 0.4;
            const y = Math.sin(angle) * decoration.size * 0.4;
            
            this.ctx.beginPath();
            for (let j = 0; j < 5; j++) {
                const pentAngle = (j * 2 * Math.PI) / 5;
                const px = x + Math.cos(pentAngle) * decoration.size * 0.15;
                const py = y + Math.sin(pentAngle) * decoration.size * 0.15;
                
                if (j === 0) this.ctx.moveTo(px, py);
                else this.ctx.lineTo(px, py);
            }
            this.ctx.closePath();
            this.ctx.fill();
        }
        
        this.ctx.restore();
    }

    drawGoal(decoration) {
        // Стойки ворот
        this.ctx.strokeStyle = '#ffffff';
        this.ctx.lineWidth = 4;
        this.ctx.beginPath();
        this.ctx.moveTo(decoration.x, decoration.y + decoration.height);
        this.ctx.lineTo(decoration.x, decoration.y);
        this.ctx.lineTo(decoration.x + decoration.width, decoration.y);
        this.ctx.lineTo(decoration.x + decoration.width, decoration.y + decoration.height);
        this.ctx.stroke();
        
        // Сетка
        this.ctx.strokeStyle = 'rgba(255, 255, 255, 0.6)';
        this.ctx.lineWidth = 1;
        
        // Вертикальные линии сетки
        for (let i = 10; i < decoration.width; i += 10) {
            this.ctx.beginPath();
            this.ctx.moveTo(decoration.x + i, decoration.y);
            this.ctx.lineTo(decoration.x + i, decoration.y + decoration.height);
            this.ctx.stroke();
        }
        
        // Горизонтальные линии сетки
        for (let i = 8; i < decoration.height; i += 8) {
            this.ctx.beginPath();
            this.ctx.moveTo(decoration.x, decoration.y + i);
            this.ctx.lineTo(decoration.x + decoration.width, decoration.y + i);
            this.ctx.stroke();
        }
    }

    drawTeamFlag(decoration) {
        const wave = decoration.wave || 0;
        
        // Флагшток
        this.ctx.strokeStyle = '#8d6e63';
        this.ctx.lineWidth = 3;
        this.ctx.beginPath();
        this.ctx.moveTo(decoration.x, decoration.y);
        this.ctx.lineTo(decoration.x, decoration.y + 60);
        this.ctx.stroke();
        
        // Развевающийся флаг команды
        decoration.colors.forEach((color, index) => {
            this.ctx.fillStyle = color;
            
            this.ctx.beginPath();
            const y = decoration.y + index * 10;
            const segments = 6;
            
            for (let i = 0; i <= segments; i++) {
                const x = decoration.x + 3 + (i / segments) * decoration.size;
                const waveOffset = Math.sin(wave + i * 0.8) * 4;
                const waveY = y + waveOffset;
                
                if (i === 0) {
                    this.ctx.moveTo(x, y);
                    this.ctx.lineTo(x, y + 10);
                } else if (i === segments) {
                    this.ctx.lineTo(x, waveY + 10);
                    this.ctx.lineTo(x, waveY);
                } else {
                    this.ctx.lineTo(x, waveY);
                }
            }
            
            for (let i = segments; i >= 0; i--) {
                const x = decoration.x + 3 + (i / segments) * decoration.size;
                const waveOffset = Math.sin(wave + i * 0.8) * 4;
                const waveY = y + waveOffset;
                this.ctx.lineTo(x, waveY + 10);
            }
            
            this.ctx.closePath();
            this.ctx.fill();
        });
    }

    drawStadiumLight(decoration) {
        const brightness = decoration.brightness || 1;
        
        // Свечение
        this.ctx.shadowColor = '#ffeb3b';
        this.ctx.shadowBlur = 20 * brightness;
        
        // Основа прожектора
        this.ctx.fillStyle = '#424242';
        this.ctx.fillRect(decoration.x - decoration.size/2, decoration.y, decoration.size, decoration.size/2);
        
        // Свет
        this.ctx.globalAlpha = brightness;
        this.ctx.fillStyle = '#ffeb3b';
        this.ctx.beginPath();
        this.ctx.arc(decoration.x, decoration.y + decoration.size/4, decoration.size/3, 0, 2 * Math.PI);
        this.ctx.fill();
        
        this.ctx.shadowBlur = 0;
        this.ctx.globalAlpha = 1;
    }

    drawStadium(decoration) {
        // Трибуны с градиентом
        const stadiumGradient = this.ctx.createLinearGradient(
            decoration.x, decoration.y,
            decoration.x, decoration.y + decoration.height
        );
        stadiumGradient.addColorStop(0, '#616161');
        stadiumGradient.addColorStop(1, '#424242');
        
        this.ctx.fillStyle = stadiumGradient;
        this.ctx.fillRect(decoration.x, decoration.y, decoration.width, decoration.height);
        
        // Ряды сидений
        this.ctx.strokeStyle = '#757575';
        this.ctx.lineWidth = 1;
        for (let i = 5; i < decoration.height; i += 8) {
            this.ctx.beginPath();
            this.ctx.moveTo(decoration.x, decoration.y + i);
            this.ctx.lineTo(decoration.x + decoration.width, decoration.y + i);
            this.ctx.stroke();
        }
        
        // Случайные зрители (точки)
        this.ctx.fillStyle = '#ffeb3b';
        for (let i = 0; i < decoration.width; i += 15) {
            for (let j = 8; j < decoration.height; j += 8) {
                if (Math.random() > 0.3) {
                    this.ctx.beginPath();
                    this.ctx.arc(decoration.x + i + Math.random() * 10, 
                               decoration.y + j, 2, 0, 2 * Math.PI);
                    this.ctx.fill();
                }
            }
        }
    }

    drawConfetti(decoration) {
        const rotation = decoration.rotation || 0;
        
        // Случайный цвет из палитры
        const color = decoration.colors[Math.floor(Math.random() * decoration.colors.length)];
        
        this.ctx.save();
        this.ctx.translate(decoration.x, decoration.y);
        this.ctx.rotate(rotation);
        
        this.ctx.fillStyle = color;
        this.ctx.fillRect(-decoration.size/2, -decoration.size/2, decoration.size, decoration.size);
        
        this.ctx.restore();
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
        this.shakeEffect = null; // 🎨 Эффект дрожания
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
        
        // 🎨 Обновляем эффект дрожания
        if (this.shakeEffect) {
            this.shakeEffect.life--;
            if (this.shakeEffect.life <= 0) {
                this.shakeEffect = null;
            }
        }
    }

    draw(ctx, input) {
        if (this.exploding) {
            this.particles.forEach(p => p.draw(ctx));
            return;
        }

        // 🎨 Применяем эффект дрожания
        let shakeX = 0, shakeY = 0;
        if (this.shakeEffect) {
            const intensity = this.shakeEffect.intensity * (this.shakeEffect.life / 15);
            shakeX = (Math.random() - 0.5) * intensity;
            shakeY = (Math.random() - 0.5) * intensity;
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
            ctx.drawImage(this.image, this.x - scaledWidth / 2 + shakeX, this.y - scaledHeight / 2 + shakeY, scaledWidth, scaledHeight);
        } else {
            // Заглушка для изображения с адаптивным размером
            const placeholderSize = maxSize * 0.8;
            ctx.fillStyle = 'lightgray';
            ctx.fillRect(this.x - placeholderSize / 2 + shakeX, this.y - placeholderSize / 2 + shakeY, placeholderSize, placeholderSize);
            ctx.fillStyle = 'black';
            const fontSize = Math.max(20, placeholderSize / 3);
            ctx.font = `${fontSize}px Arial`;
            ctx.textAlign = 'center';
            ctx.fillText('?', this.x + shakeX, this.y + fontSize / 3 + shakeY);
            scaledHeight = placeholderSize;
        }

        // Рисуем текст с улучшенным отображением
        this.drawWordText(ctx, input, scaledHeight, shakeX, shakeY);
    }

    drawWordText(ctx, input, imageHeight, shakeX = 0, shakeY = 0) {
        const fontSize = this.gameEngine ? this.gameEngine.baseFontSize : 28;
        ctx.font = `${fontSize}px Arial`;
        ctx.textAlign = 'center';
        
        const inputUpper = input.toUpperCase().replace(/\s+/g, ' '); // нормализуем пробелы
        const textY = this.y + imageHeight / 2 + fontSize * 1.5 + shakeY;
        
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
        const startX = this.x - totalWidth / 2 + shakeX;
        
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
