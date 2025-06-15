#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import webbrowser
import time

def create_animation_test_page():
    """Создает HTML страницу для тестирования анимаций"""
    
    html_content = '''<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🎨 Тест Анимаций - Word Game</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #1e3c72, #2a5298);
            color: white;
            margin: 0;
            padding: 20px;
            min-height: 100vh;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        
        .header {
            text-align: center;
            margin-bottom: 30px;
        }
        
        .test-section {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 20px;
            backdrop-filter: blur(10px);
        }
        
        .animation-demo {
            display: flex;
            flex-wrap: wrap;
            gap: 20px;
            justify-content: center;
            margin: 20px 0;
        }
        
        .demo-item {
            background: rgba(0, 0, 0, 0.3);
            border-radius: 10px;
            padding: 15px;
            text-align: center;
            min-width: 200px;
        }
        
        .effect-preview {
            width: 150px;
            height: 100px;
            background: #000;
            border-radius: 8px;
            margin: 10px auto;
            position: relative;
            overflow: hidden;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
        }
        
        /* Анимации для демонстрации */
        .key-press {
            animation: keyPress 1s ease-out infinite;
        }
        
        @keyframes keyPress {
            0% { transform: scale(1); color: #fff; }
            50% { transform: scale(1.2); color: #0f0; }
            100% { transform: scale(1); color: #fff; }
        }
        
        .letter-highlight {
            animation: letterHighlight 1.5s ease-in-out infinite;
        }
        
        @keyframes letterHighlight {
            0%, 100% { background: #000; }
            50% { background: radial-gradient(circle, #ff0 30%, #000 70%); }
        }
        
        .shooting-effect {
            position: relative;
        }
        
        .shooting-effect::before {
            content: '→';
            position: absolute;
            left: 10px;
            top: 50%;
            transform: translateY(-50%);
            color: #0ff;
            animation: shoot 2s linear infinite;
        }
        
        @keyframes shoot {
            0% { left: 10px; opacity: 1; }
            100% { left: 130px; opacity: 0; }
        }
        
        .pulse-effect {
            animation: pulse 2s ease-in-out infinite;
        }
        
        @keyframes pulse {
            0%, 100% { transform: scale(1); box-shadow: 0 0 0 0 rgba(255, 215, 0, 0.7); }
            50% { transform: scale(1.1); box-shadow: 0 0 0 20px rgba(255, 215, 0, 0); }
        }
        
        .shake-effect {
            animation: shake 0.5s ease-in-out infinite;
        }
        
        @keyframes shake {
            0%, 100% { transform: translateX(0); }
            25% { transform: translateX(-5px); }
            75% { transform: translateX(5px); }
        }
        
        .word-complete {
            animation: wordComplete 3s ease-in-out infinite;
        }
        
        @keyframes wordComplete {
            0% { transform: scale(1) rotate(0deg); color: #fff; }
            25% { transform: scale(1.3) rotate(5deg); color: #ffd700; }
            50% { transform: scale(1.5) rotate(-5deg); color: #ff6b6b; }
            75% { transform: scale(1.2) rotate(3deg); color: #4ecdc4; }
            100% { transform: scale(1) rotate(0deg); color: #fff; }
        }
        
        .controls {
            text-align: center;
            margin: 20px 0;
        }
        
        .btn {
            background: linear-gradient(45deg, #667eea, #764ba2);
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 25px;
            cursor: pointer;
            font-size: 16px;
            margin: 5px;
            transition: all 0.3s ease;
        }
        
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
        }
        
        .info {
            background: rgba(255, 255, 255, 0.1);
            border-left: 4px solid #4ecdc4;
            padding: 15px;
            margin: 20px 0;
            border-radius: 5px;
        }
        
        .success {
            background: rgba(76, 175, 80, 0.2);
            border-left-color: #4caf50;
        }
        
        .warning {
            background: rgba(255, 193, 7, 0.2);
            border-left-color: #ffc107;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎨 Тестирование Анимаций</h1>
            <p>Демонстрация всех анимационных эффектов в игре</p>
        </div>
        
        <div class="test-section">
            <h2>🎯 Эффекты Нажатия Клавиш</h2>
            <div class="animation-demo">
                <div class="demo-item">
                    <h3>Правильная Буква</h3>
                    <div class="effect-preview key-press">А</div>
                    <p>Зеленая подсветка при правильном вводе</p>
                </div>
                <div class="demo-item">
                    <h3>Неправильная Буква</h3>
                    <div class="effect-preview shake-effect" style="color: #f00;">Б</div>
                    <p>Красная подсветка + дрожание при ошибке</p>
                </div>
            </div>
        </div>
        
        <div class="test-section">
            <h2>💡 Подсветка Букв</h2>
            <div class="animation-demo">
                <div class="demo-item">
                    <h3>Активная Буква</h3>
                    <div class="effect-preview letter-highlight">К</div>
                    <p>Желтое свечение вокруг текущей буквы</p>
                </div>
            </div>
        </div>
        
        <div class="test-section">
            <h2>🎯 Эффекты Выстрелов</h2>
            <div class="animation-demo">
                <div class="demo-item">
                    <h3>Выстрел в Букву</h3>
                    <div class="effect-preview shooting-effect">🎯</div>
                    <p>Голубая линия от клавиатуры к букве</p>
                </div>
            </div>
        </div>
        
        <div class="test-section">
            <h2>💫 Эффекты Завершения</h2>
            <div class="animation-demo">
                <div class="demo-item">
                    <h3>Слово Угадано</h3>
                    <div class="effect-preview word-complete">🎉</div>
                    <p>Золотая вспышка + звездочки</p>
                </div>
                <div class="demo-item">
                    <h3>Пульсация</h3>
                    <div class="effect-preview pulse-effect">⭐</div>
                    <p>Расширяющиеся кольца</p>
                </div>
            </div>
        </div>
        
        <div class="controls">
            <button class="btn" onclick="window.open('/', '_blank')">🎮 Открыть Игру</button>
            <button class="btn" onclick="location.reload()">🔄 Перезапустить Демо</button>
        </div>
        
        <div class="info success">
            <h3>✅ Реализованные Эффекты:</h3>
            <ul>
                <li><strong>Подсветка клавиш:</strong> Зеленая для правильных, красная для неправильных</li>
                <li><strong>Подсветка букв:</strong> Желтое свечение вокруг активной буквы</li>
                <li><strong>Эффекты выстрелов:</strong> Голубые линии от клавиатуры к буквам</li>
                <li><strong>Дрожание:</strong> При неправильном вводе слово дрожит</li>
                <li><strong>Завершение слова:</strong> Золотая вспышка + звездочки вокруг</li>
                <li><strong>Пульсация:</strong> Расширяющиеся кольца при успехе</li>
            </ul>
        </div>
        
        <div class="info warning">
            <h3>⚡ Технические Детails:</h3>
            <ul>
                <li>Все эффекты работают на Canvas API</li>
                <li>Анимации оптимизированы для производительности</li>
                <li>Поддержка мобильных устройств</li>
                <li>Автоматическая очистка завершенных эффектов</li>
            </ul>
        </div>
        
        <div class="info">
            <h3>🎨 Как Тестировать:</h3>
            <ol>
                <li>Откройте игру в новой вкладке</li>
                <li>Выберите любую категорию</li>
                <li>Начните игру и вводите буквы</li>
                <li>Наблюдайте за анимациями при правильном/неправильном вводе</li>
                <li>Завершите слово чтобы увидеть эффекты успеха</li>
            </ol>
        </div>
    </div>
</body>
</html>'''
    
    return html_content

def main():
    print("🎨 СОЗДАНИЕ ТЕСТА АНИМАЦИЙ")
    print("=" * 40)
    
    # Создаем HTML файл
    html_content = create_animation_test_page()
    
    with open('tools/test_animations.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("✅ Создан файл: tools/test_animations.html")
    
    # Открываем в браузере
    file_path = os.path.abspath('tools/test_animations.html')
    webbrowser.open(f'file://{file_path}')
    
    print("🌐 Страница открыта в браузере")
    print("\n🎯 ИНСТРУКЦИИ ПО ТЕСТИРОВАНИЮ:")
    print("1. Откройте игру в новой вкладке")
    print("2. Выберите категорию 'Динозавры' или 'Животные'")
    print("3. Начните игру и вводите буквы")
    print("4. Наблюдайте за анимациями:")
    print("   - Зеленые буквы при правильном вводе")
    print("   - Красные буквы + дрожание при ошибках")
    print("   - Желтая подсветка активной буквы")
    print("   - Голубые 'выстрелы' в буквы")
    print("   - Золотые эффекты при завершении слова")
    print("   - Пульсирующие кольца при успехе")

if __name__ == "__main__":
    main() 