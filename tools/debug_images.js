// Диагностический скрипт для проверки соответствий изображений
async function debugImageMapping() {
    console.log('=== ДИАГНОСТИКА ИЗОБРАЖЕНИЙ ===');
    
    // Проверяем столицы
    console.log('\n1. АНАЛИЗ СТОЛИЦ:');
    try {
        const capitalsResponse = await fetch('/data/words/ru/capitals.txt');
        const capitalsText = await capitalsResponse.text();
        const capitalsData = capitalsText.trim().split('\n');
        
        console.log(`Загружено ${capitalsData.length} записей столиц`);
        
        // Извлекаем коды стран
        const countryCodes = [];
        capitalsData.forEach((line, index) => {
            const match = line.match(/^(\d+)\s*-\s*(.+?)\s*-\s*([A-Z]{2})$/);
            if (match) {
                const [, number, capital, code] = match;
                countryCodes.push({
                    number: parseInt(number),
                    capital: capital.trim(),
                    code: code.trim(),
                    line: index + 1
                });
            } else {
                console.warn(`Строка ${index + 1} не соответствует формату:`, line);
            }
        });
        
        console.log(`Найдено ${countryCodes.length} корректных кодов стран`);
        
        // Проверяем наличие изображений
        let foundCapitals = 0;
        let missingCapitals = [];
        
        for (const country of countryCodes) {
            try {
                const response = await fetch(`/data/images/capitals/${country.code}.png`);
                if (response.ok) {
                    foundCapitals++;
                    console.log(`✓ ${country.code}.png - ${country.capital}`);
                } else {
                    missingCapitals.push(country);
                    console.warn(`✗ Отсутствует: ${country.code}.png для ${country.capital}`);
                }
            } catch (error) {
                missingCapitals.push(country);
                console.error(`✗ Ошибка загрузки ${country.code}.png:`, error.message);
            }
        }
        
        console.log(`\nСТОЛИЦЫ - Найдено: ${foundCapitals}, Отсутствует: ${missingCapitals.length}`);
        
    } catch (error) {
        console.error('Ошибка анализа столиц:', error);
    }
    
    // Проверяем футболистов
    console.log('\n2. АНАЛИЗ ФУТБОЛИСТОВ:');
    try {
        const footballersResponse = await fetch('/data/words/ru/footballers.txt');
        const footballersText = await footballersResponse.text();
        const footballersData = footballersText.trim().split('\n');
        
        console.log(`Загружено ${footballersData.length} записей футболистов`);
        
        // Извлекаем коды изображений
        const playerCodes = [];
        footballersData.forEach((line, index) => {
            const match = line.match(/^(\d+)\s*-\s*(.+?)\s*-\s*(.+)$/);
            if (match) {
                const [, number, name, imageCode] = match;
                playerCodes.push({
                    number: parseInt(number),
                    name: name.trim(),
                    imageCode: imageCode.trim(),
                    line: index + 1
                });
            } else {
                console.warn(`Строка ${index + 1} не соответствует формату:`, line);
            }
        });
        
        console.log(`Найдено ${playerCodes.length} корректных кодов футболистов`);
        
        // Проверяем наличие изображений
        let foundFootballers = 0;
        let missingFootballers = [];
        
        for (const player of playerCodes) {
            try {
                // Кодируем имя файла для URL
                const encodedImageCode = encodeURIComponent(`${player.imageCode}.png`);
                const response = await fetch(`/data/images/footballers/${encodedImageCode}`);
                if (response.ok) {
                    foundFootballers++;
                    console.log(`✓ ${player.imageCode}.png - ${player.name}`);
                } else {
                    missingFootballers.push(player);
                    console.warn(`✗ Отсутствует: ${player.imageCode}.png для ${player.name}`);
                }
            } catch (error) {
                missingFootballers.push(player);
                console.error(`✗ Ошибка загрузки ${player.imageCode}.png:`, error.message);
            }
        }
        
        console.log(`\nФУТБОЛИСТЫ - Найдено: ${foundFootballers}, Отсутствует: ${missingFootballers.length}`);
        
        if (missingFootballers.length > 0) {
            console.log('\nОтсутствующие изображения футболистов:');
            missingFootballers.forEach(player => {
                console.log(`- ${player.name}: ${player.imageCode}.png`);
            });
        }
        
    } catch (error) {
        console.error('Ошибка анализа футболистов:', error);
    }
    
    console.log('\n=== ДИАГНОСТИКА ЗАВЕРШЕНА ===');
}

// Запускаем диагностику при загрузке страницы
window.addEventListener('load', () => {
    debugImageMapping();
}); 