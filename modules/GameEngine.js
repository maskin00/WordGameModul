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
    }

    async initialize() {
        try {
            this.canvas = document.getElementById('gameCanvas');
            this.ctx = this.canvas.getContext('2d');
            this.canvas.width = 800;
            this.canvas.height = 600;
            this.setupEventListeners();
            console.log('GameEngine инициализирован');
            return true;
        } catch (error) {
            console.error('Ошибка инициализации GameEngine:', error);
            return false;
        }
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
            if (this.languageManager.isKeySupported(key) || key === 'Backspace') {
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
        if (timestamp - this.lastSpawn > this.spawnDelay) {
            this.spawnWord();
            this.lastSpawn = timestamp;
        }
        for (let i = this.words.length - 1; i >= 0; i--) {
            const word = this.words[i];
            word.update();
            if (word.y > this.canvas.height + 100) {
                this.words.splice(i, 1);
            } else if (word.exploding && word.particles.length === 0) {
                this.words.splice(i, 1);
            }
        }
        for (let i = this.particles.length - 1; i >= 0; i--) {
            this.particles[i].update();
            if (this.particles[i].life <= 0) {
                this.particles.splice(i, 1);
            }
        }
        this.updateDifficulty();
    }

    draw() {
        this.ctx.fillStyle = 'black';
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
        this.words.forEach(word => {
            word.draw(this.ctx, this.input);
        });
        this.particles.forEach(particle => {
            particle.draw(this.ctx);
        });
        this.drawInput();
    }

    drawInput() {
        this.ctx.font = '24px Arial';
        this.ctx.fillStyle = 'white';
        this.ctx.fillText(`Ввод: ${this.input}`, 10, this.canvas.height - 20);
    }

    spawnWord() {
        const wordData = this.categoryManager.getRandomWord();
        if (!wordData) return;
        const x = Math.random() * (this.canvas.width - 200) + 100;
        const word = new Word(wordData.word, x, wordData.imagePath);
        this.words.push(word);
    }

    handleKeyPress(key) {
        if (!this.isActive || this.isPaused) return;
        if (key === 'CLEAR') {
            this.input = '';
        } else {
            this.input += key;
        }
        this.checkInput();
    }

    checkInput() {
        const inputUpper = this.input.toUpperCase();
        for (let i = 0; i < this.words.length; i++) {
            const word = this.words[i];
            if (word.exploding) continue;
            if (word.text === inputUpper) {
                this.onWordGuessed(word, i);
                return;
            }
        }
    }

    onWordGuessed(word, index) {
        const basePoints = word.text.length * 10;
        const speedBonus = Math.max(0, this.canvas.height - word.y) / 10;
        const totalPoints = Math.floor(basePoints + speedBonus);
        this.score += totalPoints;
        word.explode();
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
            this.words.forEach(word => {
                word.speed = Math.min(1.5, 0.3 + (this.level - 1) * 0.1);
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
        if (this.isActive) {
            console.log('Игровое состояние обновлено, перезапуск игры');
            this.stopGame();
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
    constructor(text, x, imgSrc) {
        this.text = text.toUpperCase();
        this.x = x;
        this.y = 0;
        this.speed = 0.3;
        this.imgSrc = imgSrc;
        this.image = new Image();
        this.image.src = imgSrc;
        this.image.onerror = () => console.warn(`Не удалось загрузить изображение: ${this.imgSrc}`);
        this.particles = [];
        this.exploding = false;
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
        let scaledWidth = 0;
        let scaledHeight = 0;
        if (this.image.complete && this.image.naturalWidth !== 0) {
            const maxSize = 200;
            const width = this.image.naturalWidth;
            const height = this.image.naturalHeight;
            const scale = Math.min(maxSize / width, maxSize / height);
            scaledWidth = width * scale;
            scaledHeight = height * scale;
            ctx.drawImage(this.image, this.x - scaledWidth / 2, this.y - scaledHeight / 2, scaledWidth, scaledHeight);
        } else {
            ctx.fillStyle = 'lightgray';
            ctx.fillRect(this.x - 50, this.y - 50, 100, 100);
            ctx.fillStyle = 'black';
            ctx.font = '40px Arial';
            ctx.textAlign = 'center';
            ctx.fillText('?', this.x, this.y + 10);
            scaledHeight = 100;
        }
        ctx.font = '25px Arial';
        ctx.textAlign = 'center';
        const inputUpper = input.toUpperCase();
        let matchedLength = 0;
        for (let i = 0; i < inputUpper.length && i < this.text.length; i++) {
            if (inputUpper[i] === this.text[i]) {
                matchedLength++;
            } else {
                break;
            }
        }
        for (let i = 0; i < this.text.length; i++) {
            ctx.fillStyle = i < matchedLength ? 'lime' : 'white';
            const textX = this.x + (i * 20) - (this.text.length * 10);
            const textY = this.y + scaledHeight / 2 + 30;
            ctx.fillText(this.text[i], textX, textY);
        }
        ctx.textAlign = 'start';
    }

    explode() {
        this.exploding = true;
        for (let i = 0; i < 20; i++) {
            this.particles.push(new Particle(this.x, this.y));
        }
    }
}
