// Сканер всех изображений через HTTP запросы
class ImageScanner {
    constructor() {
        this.foundImages = {
            capitals: [],
            footballers: []
        };
    }

    // Генерируем все возможные коды стран для проверки
    generateAllCountryCodes() {
        const codes = [];
        // Основные коды стран (наиболее вероятные)
        const knownCodes = [
            'AD', 'AE', 'AF', 'AG', 'AI', 'AL', 'AM', 'AO', 'AQ', 'AR', 'AS', 'AT', 'AU', 'AW', 'AX', 'AZ',
            'BA', 'BB', 'BD', 'BE', 'BF', 'BG', 'BH', 'BI', 'BJ', 'BL', 'BM', 'BN', 'BO', 'BQ', 'BR', 'BS', 'BT', 'BV', 'BW', 'BY', 'BZ',
            'CA', 'CC', 'CD', 'CF', 'CG', 'CH', 'CI', 'CK', 'CL', 'CM', 'CN', 'CO', 'CR', 'CU', 'CV', 'CW', 'CX', 'CY', 'CZ',
            'DE', 'DJ', 'DK', 'DM', 'DO', 'DZ',
            'EC', 'EE', 'EG', 'EH', 'ER', 'ES', 'ET',
            'FI', 'FJ', 'FK', 'FM', 'FO', 'FR',
            'GA', 'GB', 'GD', 'GE', 'GF', 'GG', 'GH', 'GI', 'GL', 'GM', 'GN', 'GP', 'GQ', 'GR', 'GS', 'GT', 'GU', 'GW', 'GY',
            'HK', 'HM', 'HN', 'HR', 'HT', 'HU',
            'ID', 'IE', 'IL', 'IM', 'IN', 'IO', 'IQ', 'IR', 'IS', 'IT',
            'JE', 'JM', 'JO', 'JP',
            'KE', 'KG', 'KH', 'KI', 'KM', 'KN', 'KP', 'KR', 'KW', 'KY', 'KZ',
            'LA', 'LB', 'LC', 'LI', 'LK', 'LR', 'LS', 'LT', 'LU', 'LV', 'LY',
            'MA', 'MC', 'MD', 'ME', 'MF', 'MG', 'MH', 'MK', 'ML', 'MM', 'MN', 'MO', 'MP', 'MQ', 'MR', 'MS', 'MT', 'MU', 'MV', 'MW', 'MX', 'MY', 'MZ',
            'NA', 'NC', 'NE', 'NF', 'NG', 'NI', 'NL', 'NO', 'NP', 'NR', 'NU', 'NZ',
            'OM',
            'PA', 'PE', 'PF', 'PG', 'PH', 'PK', 'PL', 'PM', 'PN', 'PR', 'PS', 'PT', 'PW', 'PY',
            'QA',
            'RE', 'RO', 'RS', 'RU', 'RW',
            'SA', 'SB', 'SC', 'SD', 'SE', 'SG', 'SH', 'SI', 'SJ', 'SK', 'SL', 'SM', 'SN', 'SO', 'SR', 'SS', 'ST', 'SV', 'SX', 'SY', 'SZ',
            'TC', 'TD', 'TF', 'TG', 'TH', 'TJ', 'TK', 'TL', 'TM', 'TN', 'TO', 'TR', 'TT', 'TV', 'TW', 'TZ',
            'UA', 'UG', 'UM', 'US', 'UY', 'UZ',
            'VA', 'VC', 'VE', 'VG', 'VI', 'VN', 'VU',
            'WF', 'WS',
            'YE', 'YT',
            'ZA', 'ZM', 'ZW'
        ];
        return knownCodes;
    }

    async scanCapitals() {
        console.log('🏛️ Сканирование изображений столиц...');
        
        const countryCodes = this.generateAllCountryCodes();
        const foundCapitals = [];
        
        let processed = 0;
        const total = countryCodes.length;
        
        for (const code of countryCodes) {
            try {
                const response = await fetch(`/data/images/capitals/${code}.png`, { method: 'HEAD' });
                if (response.ok) {
                    foundCapitals.push(code);
                    console.log(`✅ ${foundCapitals.length}: ${code}.png найден`);
                } else {
                    console.log(`❌ ${code}.png отсутствует`);
                }
            } catch (error) {
                console.log(`💥 Ошибка ${code}.png: ${error.message}`);
            }
            
            processed++;
            if (processed % 20 === 0) {
                console.log(`📊 Обработано: ${processed}/${total}, найдено: ${foundCapitals.length}`);
            }
        }
        
        this.foundImages.capitals = foundCapitals;
        console.log(`\n🎯 ИТОГО найдено изображений столиц: ${foundCapitals.length}`);
        return foundCapitals;
    }

    // Расширенный список имен файлов футболистов для проверки
    getFootballerFilenamesToCheck() {
        return [
            // Известные файлы
            'А БАИРАМИ-257.png', 'А КХАЛАИЛИ-1874.png', 'Б ЗОУКРОУ-1902.png',
            'М СЕИЛЕР-1909.png', 'И ДЕМА-1917.png', 'З АТХЕКАМЕ-1907.png',
            'Ц ПОЛАК-1881.png', 'Л ФЛАЧ-1891.png', 'Н САДИКИ-1868.png',
            'Х ТЕКЛАБ-1864.png', 'О НИАНГ-1866.png', 'Ф ЛЕСЕН-1858.png',
            'Д ТШИЛАНДА-1859.png', 'К ВАН ДЕ ПЕРРЕ-1862.png',
            'КРИС БЕДИА-1921.png', 'ЖОЭЛЬ МОНТЕИРУ-1923.png',
            'ФАСИНЕ КОНТЕ-1922.png', 'АЛАН ВИРЖИНИУС-1920.png',
            'ЭБРИМА КОЛЛИ-1919.png', 'РАИАН РАВЕЛСОН-1916.png',
            'СЕДРИК ИТТЕН-1918.png', 'САНДРО ЛАУПЕР-1914.png',
            'ДАРИАН МАЛЕШ-1915.png', 'КАСТРИОТ ИМЕРИ-1911.png',
            'МИГЕЛЬ ЧАНГА ЧАИВА-1912.png', 'КРИСТИАН ФАССНАХТ-1913.png',
            'ФИЛИП УГРИНИЧ-1910.png', 'ЛЕВИН БЛЮМ-1908.png',
            'ЛОРИС БЕНИТО-1906.png', 'МОХАМЕД АЛИ КАМАРА-1903.png',
            'НИКОЛАС ГОНСАЛЕС-915.png', 'ВИК ЧАМБАЕРЕ-1850.png',
            'Д ПУГНО-1848.png', 'Ф ПАГНУЦЦО-1834.png',
            'М КЕЛЛЕР-1899.png', 'М СТРИЕК-1877.png', 'М ФУСЕИНИ-1876.png',
            'М АСРИ-1875.png', 'М ГИГЕР-1872.png', 'М БАРР-1860.png',
            'М АСАИДИ-1857.png'
        ];
    }

    async scanFootballers() {
        console.log('⚽ Сканирование изображений футболистов...');
        
        const filenamesToCheck = this.getFootballerFilenamesToCheck();
        const foundFootballers = [];
        
        for (const filename of filenamesToCheck) {
            try {
                const encodedFilename = encodeURIComponent(filename);
                const response = await fetch(`/data/images/footballers/${encodedFilename}`, { method: 'HEAD' });
                if (response.ok) {
                    foundFootballers.push(filename);
                    console.log(`✅ ${foundFootballers.length}: ${filename} найден`);
                } else {
                    console.log(`❌ ${filename} отсутствует`);
                }
            } catch (error) {
                console.log(`💥 Ошибка ${filename}: ${error.message}`);
            }
        }
        
        this.foundImages.footballers = foundFootballers;
        console.log(`\n🎯 ИТОГО найдено изображений футболистов: ${foundFootballers.length}`);
        return foundFootballers;
    }

    async scanAllImages() {
        console.log('🔍 === ПОЛНОЕ СКАНИРОВАНИЕ ИЗОБРАЖЕНИЙ ===\n');
        
        const capitals = await this.scanCapitals();
        console.log('\n' + '='.repeat(80) + '\n');
        const footballers = await this.scanFootballers();
        
        console.log('\n📊 === ИТОГОВАЯ СТАТИСТИКА ===');
        console.log(`📍 Столицы: ${capitals.length} изображений найдено`);
        console.log(`⚽ Футболисты: ${footballers.length} изображений найдено`);
        console.log(`🎯 Всего изображений: ${capitals.length + footballers.length}`);
        
        return {
            capitals: capitals,
            footballers: footballers,
            total: capitals.length + footballers.length
        };
    }
}

// Глобальные функции
window.scanAllImages = async function() {
    const scanner = new ImageScanner();
    return await scanner.scanAllImages();
};

window.scanCapitalsOnly = async function() {
    const scanner = new ImageScanner();
    return await scanner.scanCapitals();
};

window.scanFootballersOnly = async function() {
    const scanner = new ImageScanner();
    return await scanner.scanFootballers();
};

window.addEventListener('load', () => {
    console.log('🔍 Сканер изображений загружен. Используйте:');
    console.log('- scanAllImages() - сканировать все изображения');
    console.log('- scanCapitalsOnly() - только столицы');
    console.log('- scanFootballersOnly() - только футболисты');
}); 