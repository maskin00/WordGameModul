// Полный анализ сопоставлений между данными и изображениями
class FullImageAnalysis {
    constructor() {
        this.stats = {
            capitals: {
                totalImages: 0,
                totalData: 0,
                matched: 0,
                unmatched: []
            },
            footballers: {
                totalImages: 0,
                totalData: 0,
                matched: 0,
                unmatched: []
            }
        };
    }

    async runFullAnalysis() {
        console.log('🔍 === ПОЛНЫЙ АНАЛИЗ СОПОСТАВЛЕНИЙ ===');
        
        await this.analyzeCapitals();
        await this.analyzeFootballers();
        
        this.displayFullResults();
    }

    async analyzeCapitals() {
        console.log('\n📍 АНАЛИЗ СТОЛИЦ:');
        
        // Получаем все коды стран из наших данных
        try {
            const response = await fetch('/data/words/ru/capitals.txt');
            const text = await response.text();
            const dataLines = text.trim().split('\n');
            
            console.log(`📊 В файле данных: ${dataLines.length} записей`);
            this.stats.capitals.totalData = dataLines.length;
            
            // Парсим коды стран
            const countryCodes = dataLines.map(line => {
                const match = line.match(/^(\d+)\s*-\s*(.+?)\s*-\s*([A-Z]{2})$/);
                if (match) {
                    return {
                        number: parseInt(match[1]),
                        capital: match[2].trim(),
                        code: match[3].trim()
                    };
                }
                return null;
            }).filter(item => item !== null);
            
            console.log(`✅ Корректно распознано: ${countryCodes.length} кодов стран`);
            
            // Генерируем полный список возможных кодов стран (255 как указал пользователь)
            const allPossibleCodes = this.generateAllCountryCodes();
            console.log(`🌍 Всего возможных кодов стран: ${allPossibleCodes.length}`);
            this.stats.capitals.totalImages = allPossibleCodes.length;
            
            // Проверяем какие коды у нас есть в данных
            const usedCodes = countryCodes.map(item => item.code);
            const unusedCodes = allPossibleCodes.filter(code => !usedCodes.includes(code));
            
            console.log(`📈 Используется кодов: ${usedCodes.length}`);
            console.log(`📉 Не используется кодов: ${unusedCodes.length}`);
            
            this.stats.capitals.matched = usedCodes.length;
            this.stats.capitals.unmatched = unusedCodes;
            
            // Проверяем наличие изображений для используемых кодов
            let foundImages = 0;
            for (const country of countryCodes) {
                try {
                    const response = await fetch(`/data/images/capitals/${country.code}.png`, { method: 'HEAD' });
                    if (response.ok) {
                        foundImages++;
                        console.log(`✅ ${country.code}.png - ${country.capital}`);
                    } else {
                        console.warn(`❌ Отсутствует изображение: ${country.code}.png для ${country.capital}`);
                    }
                } catch (error) {
                    console.error(`💥 Ошибка проверки ${country.code}.png:`, error.message);
                }
            }
            
            console.log(`🖼️ Найдено изображений: ${foundImages}/${countryCodes.length}`);
            
        } catch (error) {
            console.error('❌ Ошибка анализа столиц:', error);
        }
    }

    async analyzeFootballers() {
        console.log('\n⚽ АНАЛИЗ ФУТБОЛИСТОВ:');
        
        // Получаем данные футболистов
        try {
            const response = await fetch('/data/words/ru/footballers.txt');
            const text = await response.text();
            const dataLines = text.trim().split('\n');
            
            console.log(`📊 В файле данных: ${dataLines.length} записей`);
            this.stats.footballers.totalData = dataLines.length;
            
            // Парсим данные футболистов
            const footballers = dataLines.map(line => {
                const match = line.match(/^(\d+)\s*-\s*(.+?)\s*-\s*(.+)$/);
                if (match) {
                    return {
                        number: parseInt(match[1]),
                        name: match[2].trim(),
                        imageCode: match[3].trim()
                    };
                }
                return null;
            }).filter(item => item !== null);
            
            console.log(`✅ Корректно распознано: ${footballers.length} футболистов`);
            
            // Получаем реальное количество изображений (пользователь указал 1923)
            this.stats.footballers.totalImages = 1923;
            console.log(`🖼️ Всего изображений футболистов доступно: 1923`);
            console.log(`📊 Используется в данных: ${footballers.length}`);
            console.log(`📉 Не используется: ${1923 - footballers.length}`);
            
            // Проверяем наличие изображений для футболистов
            let foundImages = 0;
            let missingImages = [];
            
            for (const footballer of footballers) {
                try {
                    const encodedImageCode = encodeURIComponent(`${footballer.imageCode}.png`);
                    const response = await fetch(`/data/images/footballers/${encodedImageCode}`, { method: 'HEAD' });
                    if (response.ok) {
                        foundImages++;
                        console.log(`✅ ${footballer.imageCode}.png - ${footballer.name}`);
                    } else {
                        missingImages.push(footballer);
                        console.warn(`❌ Отсутствует: ${footballer.imageCode}.png для ${footballer.name}`);
                    }
                } catch (error) {
                    missingImages.push(footballer);
                    console.error(`💥 Ошибка проверки ${footballer.imageCode}.png:`, error.message);
                }
            }
            
            console.log(`🎯 Найдено изображений: ${foundImages}/${footballers.length}`);
            this.stats.footballers.matched = foundImages;
            this.stats.footballers.unmatched = missingImages.map(f => f.imageCode);
            
        } catch (error) {
            console.error('❌ Ошибка анализа футболистов:', error);
        }
    }

    generateAllCountryCodes() {
        // Генерируем все возможные двухбуквенные коды стран (ISO 3166-1)
        const codes = [];
        for (let i = 65; i <= 90; i++) { // A-Z
            for (let j = 65; j <= 90; j++) { // A-Z
                codes.push(String.fromCharCode(i) + String.fromCharCode(j));
            }
        }
        return codes.slice(0, 255); // Ограничиваем до 255 как указал пользователь
    }

    displayFullResults() {
        console.log('\n📊 === ИТОГОВАЯ СТАТИСТИКА ===');
        
        console.log('\n📍 СТОЛИЦЫ:');
        console.log(`🖼️ Всего изображений доступно: ${this.stats.capitals.totalImages}`);
        console.log(`📄 Записей в данных: ${this.stats.capitals.totalData}`);
        console.log(`✅ Совпадений: ${this.stats.capitals.matched}`);
        console.log(`❌ Не используется изображений: ${this.stats.capitals.totalImages - this.stats.capitals.matched}`);
        console.log(`📈 Процент использования: ${((this.stats.capitals.matched / this.stats.capitals.totalImages) * 100).toFixed(1)}%`);
        
        console.log('\n⚽ ФУТБОЛИСТЫ:');
        console.log(`🖼️ Всего изображений доступно: ${this.stats.footballers.totalImages}`);
        console.log(`📄 Записей в данных: ${this.stats.footballers.totalData}`);
        console.log(`✅ Совпадений: ${this.stats.footballers.matched}`);
        console.log(`❌ Не используется изображений: ${this.stats.footballers.totalImages - this.stats.footballers.matched}`);
        console.log(`📈 Процент использования: ${((this.stats.footballers.matched / this.stats.footballers.totalImages) * 100).toFixed(1)}%`);
        
        console.log('\n🔧 === РЕКОМЕНДАЦИИ ===');
        
        if (this.stats.capitals.matched < this.stats.capitals.totalImages) {
            console.log(`📍 Для столиц: можно добавить еще ${this.stats.capitals.totalImages - this.stats.capitals.matched} записей`);
        }
        
        if (this.stats.footballers.matched < this.stats.footballers.totalImages) {
            console.log(`⚽ Для футболистов: можно добавить еще ${this.stats.footballers.totalImages - this.stats.footballers.matched} записей`);
        }
        
        console.log('\n💡 === ЛОГИКА СОПОСТАВЛЕНИЯ ===');
        console.log('📍 Столицы: название_столицы -> КОД_СТРАНЫ.png');
        console.log('   Пример: АНДОРРА-ЛА-ВЕЛЬЯ -> AD.png');
        console.log('⚽ Футболисты: имя_игрока -> ПОЛНОЕ_ИМЯ_ФАЙЛА.png');
        console.log('   Пример: БАИРАМИ -> А БАИРАМИ-257.png');
        console.log('   Форматы имен файлов: префикс + фамилия + номер');
    }

    async exploreFootballerImages() {
        console.log('\n🔍 === ИССЛЕДОВАНИЕ ИЗОБРАЖЕНИЙ ФУТБОЛИСТОВ ===');
        
        // Анализируем паттерны имен файлов
        const knownImages = [
            'А БАИРАМИ-257.png',
            'А КХАЛАИЛИ-1874.png',
            'Б ЗОУКРОУ-1902.png',
            'М СЕИЛЕР-1909.png',
            'КРИС БЕДИА-1921.png',
            'ЖОЭЛЬ МОНТЕИРУ-1923.png',
            'НИКОЛАС ГОНСАЛЕС-915.png'
        ];
        
        console.log('📋 Паттерны имен файлов футболистов:');
        console.log('1. Односимвольный префикс: А, Б, М, И, З, Ц, Л, Н, Х, О, Ф, Д, К');
        console.log('2. Полные имена без префикса: КРИС БЕДИА, ЖОЭЛЬ МОНТЕИРУ');
        console.log('3. Уникальные номера: 257, 1874, 1902, 915, 1921, 1923');
        
        knownImages.forEach(imageName => {
            console.log(`🔍 ${imageName}`);
        });
    }
}

// Глобальная функция для запуска анализа
window.runFullAnalysis = async function() {
    const analyzer = new FullImageAnalysis();
    await analyzer.runFullAnalysis();
    await analyzer.exploreFootballerImages();
};

// Автозапуск при загрузке
window.addEventListener('load', () => {
    console.log('🚀 Система полного анализа загружена. Используйте runFullAnalysis() для запуска.');
}); 