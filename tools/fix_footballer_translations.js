// Скрипт для исправления переводов футболистов
// Заменяет русские названия на латинские транслитерации

const fs = require('fs');
const path = require('path');

// Функция транслитерации с русского на латиницу
function transliterate(text) {
    const translitMap = {
        'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D', 'Е': 'E', 'Ё': 'YO', 'Ж': 'ZH', 'З': 'Z',
        'И': 'I', 'Й': 'Y', 'К': 'K', 'Л': 'L', 'М': 'M', 'Н': 'N', 'О': 'O', 'П': 'P', 'Р': 'R',
        'С': 'S', 'Т': 'T', 'У': 'U', 'Ф': 'F', 'Х': 'KH', 'Ц': 'TS', 'Ч': 'CH', 'Ш': 'SH', 'Щ': 'SHCH',
        'Ъ': '', 'Ы': 'Y', 'Ь': '', 'Э': 'E', 'Ю': 'YU', 'Я': 'YA',
        ' ': ' ', '-': '-'
    };
    
    return text.split('').map(char => translitMap[char] || char).join('');
}

// Функция для обработки файла
function processFile(filePath, language) {
    console.log(`Обрабатываем файл: ${filePath}`);
    
    try {
        const content = fs.readFileSync(filePath, 'utf8');
        const lines = content.split('\n');
        
        const processedLines = lines.map(line => {
            if (line.trim() === '' || line.startsWith('#')) {
                return line;
            }
            
            // Парсим строку: номер - СЛОВО - код_изображения
            const parts = line.split(' - ');
            if (parts.length >= 3) {
                const number = parts[0];
                const russianName = parts[1];
                const imageCode = parts[2];
                
                // Транслитерируем русское название
                const transliteratedName = transliterate(russianName);
                
                return `${number} - ${transliteratedName} - ${imageCode}`;
            }
            
            return line;
        });
        
        // Записываем обработанный файл
        fs.writeFileSync(filePath, processedLines.join('\n'), 'utf8');
        console.log(`✓ Файл ${filePath} успешно обработан`);
        
    } catch (error) {
        console.error(`✗ Ошибка обработки файла ${filePath}:`, error.message);
    }
}

// Основная функция
function main() {
    console.log('Начинаем исправление переводов футболистов...\n');
    
    const languages = ['en', 'fr', 'es'];
    const files = ['footballers_FULL.txt', 'footballers.txt'];
    
    languages.forEach(lang => {
        files.forEach(file => {
            const filePath = path.join(__dirname, '..', 'data', 'words', lang, file);
            
            if (fs.existsSync(filePath)) {
                processFile(filePath, lang);
            } else {
                console.log(`⚠ Файл не найден: ${filePath}`);
            }
        });
    });
    
    console.log('\n✓ Исправление переводов завершено!');
}

// Запускаем скрипт
if (require.main === module) {
    main();
}

module.exports = { transliterate, processFile }; 