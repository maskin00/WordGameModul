#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

def create_decorations_test():
    """Create test page for thematic decorations"""
    
    html_content = '''<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Тест тематических декораций</title>
    <style>
        body {
            margin: 0;
            padding: 20px;
            font-family: Arial, sans-serif;
            background: #1a1a1a;
            color: white;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        
        h1 {
            text-align: center;
            color: #4CAF50;
            margin-bottom: 30px;
        }
        
        .controls {
            text-align: center;
            margin-bottom: 30px;
        }
        
        .category-btn {
            background: #4CAF50;
            color: white;
            border: none;
            padding: 10px 20px;
            margin: 5px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
            transition: background 0.3s;
        }
        
        .category-btn:hover {
            background: #45a049;
        }
        
        .category-btn.active {
            background: #ff6b6b;
        }
        
        .canvas-container {
            text-align: center;
            margin: 20px 0;
        }
        
        canvas {
            border: 2px solid #4CAF50;
            border-radius: 10px;
            background: black;
        }
        
        .info {
            background: #2a2a2a;
            padding: 20px;
            border-radius: 10px;
            margin-top: 20px;
        }
        
        .decoration-list {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }
        
        .decoration-item {
            background: #333;
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid #4CAF50;
        }
        
        .decoration-item h4 {
            margin: 0 0 10px 0;
            color: #4CAF50;
        }
        
        .decoration-item p {
            margin: 5px 0;
            font-size: 14px;
        }
        
        .legend {
            background: #2a2a2a;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
        }
        
        .legend h3 {
            margin: 0 0 15px 0;
            color: #4CAF50;
        }
        
        .legend-item {
            display: inline-block;
            margin: 5px 15px 5px 0;
            font-size: 14px;
        }
        
        .legend-color {
            display: inline-block;
            width: 20px;
            height: 20px;
            margin-right: 8px;
            vertical-align: middle;
            border-radius: 3px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎨 Тематические декорации игрового поля</h1>
        
        <div class="legend">
            <h3>Легенда анимаций:</h3>
            <div class="legend-item">
                <span class="legend-color" style="background: #ffeb3b;"></span>
                Мерцающие элементы
            </div>
            <div class="legend-item">
                <span class="legend-color" style="background: #4caf50;"></span>
                Плавающие объекты
            </div>
            <div class="legend-item">
                <span class="legend-color" style="background: #ff5722;"></span>
                Движущиеся элементы
            </div>
            <div class="legend-item">
                <span class="legend-color" style="background: #2196f3;"></span>
                Вращающиеся объекты
            </div>
        </div>
        
        <div class="controls">
            <button class="category-btn active" onclick="switchCategory('capitals')">🏛️ Столицы</button>
            <button class="category-btn" onclick="switchCategory('countries')">🗺️ Страны</button>
            <button class="category-btn" onclick="switchCategory('animals')">🐾 Животные</button>
            <button class="category-btn" onclick="switchCategory('dinosaurs')">🦕 Динозавры</button>
            <button class="category-btn" onclick="switchCategory('animal_world')">🌍 Животный мир</button>
        </div>
        
        <div class="canvas-container">
            <canvas id="decorationCanvas" width="800" height="600"></canvas>
        </div>
        
        <div class="info">
            <h3 id="categoryTitle">🏛️ Столицы - Городская атмосфера</h3>
            <p id="categoryDescription">Здания, флаги и мерцающие звезды создают атмосферу мегаполиса</p>
            
            <div id="decorationsList" class="decoration-list">
                <!-- Динамически заполняется JavaScript -->
            </div>
        </div>
    </div>

    <script>
        class DecorationEngine {
            constructor(canvas) {
                this.canvas = canvas;
                this.ctx = canvas.getContext('2d');
                this.decorations = [];
                this.currentTheme = 'capitals';
                this.animationId = null;
                
                this.initializeTheme('capitals');
                this.startAnimation();
            }
            
            initializeTheme(categoryId) {
                this.decorations = [];
                this.currentTheme = categoryId;
                
                const themes = {
                    'capitals': this.createCapitalsDecorations.bind(this),
                    'countries': this.createCountriesDecorations.bind(this),
                    'animals': this.createAnimalsDecorations.bind(this),
                    'dinosaurs': this.createDinosaursDecorations.bind(this),
                    'animal_world': this.createAnimalWorldDecorations.bind(this)
                };
                
                if (themes[categoryId]) {
                    themes[categoryId]();
                }
                
                this.updateInfo();
            }
            
            createCapitalsDecorations() {
                this.decorations = [
                    { type: 'building', x: 50, y: 400, width: 40, height: 80, color: '#4a90e2' },
                    { type: 'building', x: 100, y: 380, width: 35, height: 100, color: '#357abd' },
                    { type: 'building', x: this.canvas.width - 90, y: 390, width: 40, height: 90, color: '#4a90e2' },
                    { type: 'building', x: this.canvas.width - 140, y: 370, width: 35, height: 110, color: '#357abd' },
                    { type: 'flag', x: 30, y: 50, size: 25, colors: ['#ff6b6b', '#4ecdc4', '#45b7d1'] },
                    { type: 'flag', x: this.canvas.width - 55, y: 50, size: 25, colors: ['#96ceb4', '#feca57', '#ff9ff3'] },
                    { type: 'star', x: 80, y: 80, size: 8, color: '#ffd700', twinkle: true },
                    { type: 'star', x: this.canvas.width - 80, y: 90, size: 8, color: '#ffd700', twinkle: true },
                    { type: 'star', x: 120, y: 120, size: 6, color: '#ffed4e', twinkle: true }
                ];
            }
            
            createCountriesDecorations() {
                this.decorations = [
                    { type: 'mountain', x: 20, y: 350, width: 100, height: 80, color: '#8e9aaf' },
                    { type: 'mountain', x: 60, y: 370, width: 80, height: 60, color: '#a8b5c8' },
                    { type: 'mountain', x: this.canvas.width - 120, y: 360, width: 90, height: 70, color: '#8e9aaf' },
                    { type: 'cloud', x: 150, y: 60, size: 30, drift: true },
                    { type: 'cloud', x: this.canvas.width - 180, y: 80, size: 25, drift: true },
                    { type: 'cloud', x: 200, y: 100, size: 20, drift: true },
                    { type: 'compass', x: this.canvas.width - 60, y: this.canvas.height - 60, size: 40, rotate: true }
                ];
            }
            
            createAnimalsDecorations() {
                this.decorations = [
                    { type: 'tree', x: 40, y: 320, width: 30, height: 100, leafColor: '#4caf50' },
                    { type: 'tree', x: this.canvas.width - 70, y: 310, width: 35, height: 110, leafColor: '#66bb6a' },
                    { type: 'bush', x: 90, y: 400, size: 25, color: '#4caf50' },
                    { type: 'bush', x: this.canvas.width - 115, y: 390, size: 30, color: '#66bb6a' },
                    { type: 'leaf', x: 120, y: 150, size: 8, color: '#4caf50', float: true },
                    { type: 'leaf', x: this.canvas.width - 140, y: 180, size: 10, color: '#8bc34a', float: true },
                    { type: 'leaf', x: 180, y: 120, size: 6, color: '#66bb6a', float: true },
                    { type: 'pawprint', x: 150, y: 420, size: 12, color: '#8d6e63' },
                    { type: 'pawprint', x: 170, y: 430, size: 12, color: '#8d6e63' },
                    { type: 'pawprint', x: this.canvas.width - 190, y: 425, size: 12, color: '#8d6e63' }
                ];
            }
            
            createDinosaursDecorations() {
                this.decorations = [
                    { type: 'volcano', x: 30, y: 350, width: 80, height: 90, active: true },
                    { type: 'volcano', x: this.canvas.width - 110, y: 340, width: 70, height: 100, active: false },
                    { type: 'fern', x: 120, y: 380, size: 40, color: '#2e7d32' },
                    { type: 'fern', x: this.canvas.width - 160, y: 370, size: 45, color: '#388e3c' },
                    { type: 'meteor', x: 200, y: 80, size: 8, trail: true, speed: 2 },
                    { type: 'meteor', x: this.canvas.width - 220, y: 100, size: 6, trail: true, speed: 1.5 },
                    { type: 'prehistoric_plant', x: 80, y: 400, size: 35, color: '#1b5e20' },
                    { type: 'prehistoric_plant', x: this.canvas.width - 120, y: 410, size: 30, color: '#2e7d32' }
                ];
            }
            
            createAnimalWorldDecorations() {
                this.decorations = [
                    { type: 'tree', x: 35, y: 320, width: 25, height: 90, leafColor: '#4caf50' },
                    { type: 'palm_tree', x: this.canvas.width - 65, y: 300, height: 120, leafColor: '#66bb6a' },
                    { type: 'flower', x: 100, y: 420, size: 15, color: '#e91e63' },
                    { type: 'flower', x: 130, y: 410, size: 12, color: '#9c27b0' },
                    { type: 'flower', x: this.canvas.width - 130, y: 415, size: 14, color: '#ff5722' },
                    { type: 'butterfly', x: 160, y: 200, size: 12, colors: ['#ff9800', '#ffeb3b'], flutter: true },
                    { type: 'butterfly', x: this.canvas.width - 180, y: 180, size: 10, colors: ['#e91e63', '#9c27b0'], flutter: true },
                    { type: 'sun', x: this.canvas.width - 80, y: 80, size: 30, rays: true }
                ];
            }
            
            updateAnimations() {
                this.decorations.forEach(decoration => {
                    switch (decoration.type) {
                        case 'cloud':
                            if (decoration.drift) {
                                decoration.x += 0.2;
                                if (decoration.x > this.canvas.width + 50) {
                                    decoration.x = -50;
                                }
                            }
                            break;
                            
                        case 'leaf':
                            if (decoration.float) {
                                decoration.y += Math.sin(Date.now() * 0.002 + decoration.x * 0.01) * 0.3;
                                decoration.x += 0.1;
                                if (decoration.x > this.canvas.width + 20) {
                                    decoration.x = -20;
                                    decoration.y = 100 + Math.random() * 100;
                                }
                            }
                            break;
                            
                        case 'meteor':
                            if (decoration.trail) {
                                decoration.x += decoration.speed;
                                decoration.y += decoration.speed * 0.5;
                                if (decoration.x > this.canvas.width + 50) {
                                    decoration.x = -50;
                                    decoration.y = 50 + Math.random() * 100;
                                }
                            }
                            break;
                            
                        case 'butterfly':
                            if (decoration.flutter) {
                                decoration.x += Math.sin(Date.now() * 0.003) * 0.5;
                                decoration.y += Math.cos(Date.now() * 0.004) * 0.3;
                            }
                            break;
                            
                        case 'compass':
                            if (decoration.rotate) {
                                decoration.rotation = (decoration.rotation || 0) + 0.01;
                            }
                            break;
                    }
                });
            }
            
            draw() {
                // Clear canvas
                this.ctx.fillStyle = 'black';
                this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
                
                // Draw decorations
                this.decorations.forEach(decoration => {
                    this.ctx.save();
                    this.drawDecoration(decoration);
                    this.ctx.restore();
                });
            }
            
            drawDecoration(decoration) {
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
                }
            }
            
            // Drawing methods (simplified versions)
            drawBuilding(decoration) {
                this.ctx.fillStyle = decoration.color;
                this.ctx.fillRect(decoration.x, decoration.y, decoration.width, decoration.height);
                
                // Windows
                this.ctx.fillStyle = '#ffeb3b';
                for (let i = 0; i < 3; i++) {
                    for (let j = 0; j < Math.floor(decoration.height / 20); j++) {
                        if (Math.random() > 0.3) {
                            this.ctx.fillRect(
                                decoration.x + 5 + i * 10,
                                decoration.y + 10 + j * 15,
                                6, 8
                            );
                        }
                    }
                }
            }
            
            drawFlag(decoration) {
                // Flag pole
                this.ctx.strokeStyle = '#8d6e63';
                this.ctx.lineWidth = 3;
                this.ctx.beginPath();
                this.ctx.moveTo(decoration.x, decoration.y);
                this.ctx.lineTo(decoration.x, decoration.y + 60);
                this.ctx.stroke();
                
                // Flag
                decoration.colors.forEach((color, index) => {
                    this.ctx.fillStyle = color;
                    this.ctx.fillRect(
                        decoration.x + 3,
                        decoration.y + index * 8,
                        decoration.size,
                        8
                    );
                });
            }
            
            drawStar(decoration) {
                const alpha = decoration.twinkle ? 
                    0.5 + 0.5 * Math.sin(Date.now() * 0.005 + decoration.x * 0.01) : 1;
                
                this.ctx.globalAlpha = alpha;
                this.ctx.fillStyle = decoration.color;
                this.ctx.beginPath();
                
                for (let i = 0; i < 5; i++) {
                    const angle = (i * 4 * Math.PI) / 5;
                    const x = decoration.x + Math.cos(angle) * decoration.size;
                    const y = decoration.y + Math.sin(angle) * decoration.size;
                    
                    if (i === 0) this.ctx.moveTo(x, y);
                    else this.ctx.lineTo(x, y);
                }
                
                this.ctx.closePath();
                this.ctx.fill();
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
                // Volcano body
                this.ctx.fillStyle = decoration.color || '#5d4037';
                this.ctx.beginPath();
                this.ctx.moveTo(decoration.x, decoration.y + decoration.height);
                this.ctx.lineTo(decoration.x + decoration.width * 0.2, decoration.y);
                this.ctx.lineTo(decoration.x + decoration.width * 0.8, decoration.y);
                this.ctx.lineTo(decoration.x + decoration.width, decoration.y + decoration.height);
                this.ctx.closePath();
                this.ctx.fill();
                
                // Lava/smoke if active
                if (decoration.active) {
                    this.ctx.fillStyle = '#ff5722';
                    this.ctx.globalAlpha = 0.7;
                    this.ctx.beginPath();
                    this.ctx.arc(decoration.x + decoration.width * 0.5, decoration.y - 10, 15, 0, 2 * Math.PI);
                    this.ctx.fill();
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
                // Wings
                decoration.colors.forEach((color, index) => {
                    this.ctx.fillStyle = color;
                    
                    // Upper wings
                    this.ctx.beginPath();
                    this.ctx.ellipse(
                        decoration.x + (index === 0 ? -decoration.size * 0.3 : decoration.size * 0.3),
                        decoration.y - decoration.size * 0.2,
                        decoration.size * 0.4, decoration.size * 0.6, 0, 0, 2 * Math.PI
                    );
                    this.ctx.fill();
                    
                    // Lower wings
                    this.ctx.beginPath();
                    this.ctx.ellipse(
                        decoration.x + (index === 0 ? -decoration.size * 0.2 : decoration.size * 0.2),
                        decoration.y + decoration.size * 0.2,
                        decoration.size * 0.3, decoration.size * 0.4, 0, 0, 2 * Math.PI
                    );
                    this.ctx.fill();
                });
                
                // Body
                this.ctx.strokeStyle = '#3e2723';
                this.ctx.lineWidth = 2;
                this.ctx.beginPath();
                this.ctx.moveTo(decoration.x, decoration.y - decoration.size * 0.5);
                this.ctx.lineTo(decoration.x, decoration.y + decoration.size * 0.5);
                this.ctx.stroke();
            }
            
            drawSun(decoration) {
                // Sun body
                this.ctx.fillStyle = '#ffeb3b';
                this.ctx.beginPath();
                this.ctx.arc(decoration.x, decoration.y, decoration.size, 0, 2 * Math.PI);
                this.ctx.fill();
                
                // Rays
                if (decoration.rays) {
                    this.ctx.strokeStyle = '#ffc107';
                    this.ctx.lineWidth = 3;
                    
                    for (let i = 0; i < 8; i++) {
                        const angle = (i * Math.PI) / 4;
                        this.ctx.beginPath();
                        this.ctx.moveTo(
                            decoration.x + Math.cos(angle) * decoration.size * 1.2,
                            decoration.y + Math.sin(angle) * decoration.size * 1.2
                        );
                        this.ctx.lineTo(
                            decoration.x + Math.cos(angle) * decoration.size * 1.6,
                            decoration.y + Math.sin(angle) * decoration.size * 1.6
                        );
                        this.ctx.stroke();
                    }
                }
            }
            
            updateInfo() {
                const themes = {
                    'capitals': {
                        title: '🏛️ Столицы - Городская атмосфера',
                        description: 'Здания, флаги и мерцающие звезды создают атмосферу мегаполиса',
                        decorations: [
                            { name: 'Здания', description: 'Небоскребы с освещенными окнами', animation: 'Статичные' },
                            { name: 'Флаги', description: 'Национальные флаги на флагштоках', animation: 'Статичные' },
                            { name: 'Звезды', description: 'Мерцающие звезды над городом', animation: 'Мерцание' }
                        ]
                    },
                    'countries': {
                        title: '🗺️ Страны - Географический ландшафт',
                        description: 'Горы, облака и компас создают атмосферу путешествий',
                        decorations: [
                            { name: 'Горы', description: 'Заснеженные горные вершины', animation: 'Статичные' },
                            { name: 'Облака', description: 'Плывущие по небу облака', animation: 'Дрейф' },
                            { name: 'Компас', description: 'Вращающийся навигационный компас', animation: 'Вращение' }
                        ]
                    },
                    'animals': {
                        title: '🐾 Животные - Природная среда',
                        description: 'Деревья, листья и следы создают атмосферу дикой природы',
                        decorations: [
                            { name: 'Деревья', description: 'Лиственные деревья и кусты', animation: 'Статичные' },
                            { name: 'Листья', description: 'Падающие и плавающие листья', animation: 'Плавание' },
                            { name: 'Следы', description: 'Отпечатки лап животных', animation: 'Статичные' }
                        ]
                    },
                    'dinosaurs': {
                        title: '🦕 Динозавры - Доисторический мир',
                        description: 'Вулканы, папоротники и метеоры создают атмосферу юрского периода',
                        decorations: [
                            { name: 'Вулканы', description: 'Активные и потухшие вулканы', animation: 'Дым/лава' },
                            { name: 'Папоротники', description: 'Древние доисторические растения', animation: 'Статичные' },
                            { name: 'Метеоры', description: 'Падающие космические тела', animation: 'Движение' }
                        ]
                    },
                    'animal_world': {
                        title: '🌍 Животный мир - Разнообразие природы',
                        description: 'Смешанная экосистема с разными видами растений и животных',
                        decorations: [
                            { name: 'Деревья', description: 'Обычные и пальмовые деревья', animation: 'Статичные' },
                            { name: 'Цветы', description: 'Яркие цветы разных видов', animation: 'Статичные' },
                            { name: 'Бабочки', description: 'Порхающие разноцветные бабочки', animation: 'Порхание' },
                            { name: 'Солнце', description: 'Яркое солнце с лучами', animation: 'Статичные' }
                        ]
                    }
                };
                
                const theme = themes[this.currentTheme];
                document.getElementById('categoryTitle').textContent = theme.title;
                document.getElementById('categoryDescription').textContent = theme.description;
                
                const decorationsList = document.getElementById('decorationsList');
                decorationsList.innerHTML = theme.decorations.map(decoration => `
                    <div class="decoration-item">
                        <h4>${decoration.name}</h4>
                        <p><strong>Описание:</strong> ${decoration.description}</p>
                        <p><strong>Анимация:</strong> ${decoration.animation}</p>
                    </div>
                `).join('');
            }
            
            startAnimation() {
                const animate = () => {
                    this.updateAnimations();
                    this.draw();
                    this.animationId = requestAnimationFrame(animate);
                };
                animate();
            }
            
            stopAnimation() {
                if (this.animationId) {
                    cancelAnimationFrame(this.animationId);
                    this.animationId = null;
                }
            }
        }
        
        // Initialize
        let decorationEngine;
        
        window.addEventListener('load', () => {
            const canvas = document.getElementById('decorationCanvas');
            decorationEngine = new DecorationEngine(canvas);
        });
        
        function switchCategory(categoryId) {
            // Update button states
            document.querySelectorAll('.category-btn').forEach(btn => {
                btn.classList.remove('active');
            });
            event.target.classList.add('active');
            
            // Switch theme
            if (decorationEngine) {
                decorationEngine.initializeTheme(categoryId);
            }
        }
    </script>
</body>
</html>'''
    
    with open('tools/test_decorations.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("✅ Создана тестовая страница декораций: tools/test_decorations.html")
    print("🌐 Откройте файл в браузере для просмотра всех тематических декораций")

if __name__ == "__main__":
    create_decorations_test() 