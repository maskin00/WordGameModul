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
            // Возобновляем паузу
            this.isPaused = false;
            this.resumeGameLoop();
        } else {
            // Начинаем новую игру
            this.resetGameState();
            this.isActive = true;
            this.gameStarted = true;
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
        if (!this.isActive || !this.gameStarted) return;
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
        
        // 🎨 РИСУЕМ АНИМАЦИОННЫЕ ЭФФЕКТЫ
        this.drawAnimationEffects();
        
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
