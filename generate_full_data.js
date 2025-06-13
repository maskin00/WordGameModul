// Генератор полных файлов данных из всех изображений
class FullDataGenerator {
    constructor() {
        this.countriesData = this.getCountriesData();
        this.footballersData = [];
    }

    // Полный список стран и столиц (ISO 3166-1)
    getCountriesData() {
        return {
            'AD': 'АНДОРРА-ЛА-ВЕЛЬЯ', 'AE': 'АБУ-ДАБИ', 'AF': 'КАБУЛ', 'AG': 'СЕНТ-ДЖОНС',
            'AI': 'ОСТРОВ АНГИЛЬЯ', 'AL': 'ТИРАНА', 'AM': 'ЕРЕВАН', 'AO': 'ЛУАНДА',
            'AR': 'БУЭНОС-АЙРЕС', 'AS': 'ПАГО-ПАГО', 'AT': 'ВЕНА', 'AU': 'КАНБЕРРА',
            'AW': 'ОРАНЬЕСТАД', 'AX': 'МАРИЕХАМН', 'AZ': 'БАКУ', 'BA': 'САРАЕВО',
            'BB': 'БРИДЖТАУН', 'BD': 'ДАККА', 'BE': 'БРЮССЕЛЬ', 'BF': 'УАГАДУГУ',
            'BG': 'СОФИЯ', 'BH': 'МАНАМА', 'BI': 'ГИТЕГА', 'BJ': 'ПОРТО-НОВО',
            'BL': 'ГУСТАВИЯ', 'BM': 'ГАМИЛЬТОН', 'BN': 'БАНДАР-СЕРИ-БЕГАВАН', 'BO': 'СУКРЕ',
            'BQ': 'КРАЛЕНДЕЙК', 'BR': 'БРАЗИЛИА', 'BS': 'НАССАУ', 'BT': 'ТХИМПХУ',
            'BV': 'БУВЕ', 'BW': 'ГАБОРОНЕ', 'BY': 'МИНСК', 'BZ': 'БЕЛЬМОПАН',
            'CA': 'ОТТАВА', 'CC': 'УЭСТ-АЙЛЕНД', 'CD': 'КИНШАСА', 'CF': 'БАНГИ',
            'CG': 'БРАЗЗАВИЛЬ', 'CH': 'БЕРН', 'CI': 'ЯМУСУКРО', 'CK': 'АВАРАМАНГА',
            'CL': 'САНТЬЯГО', 'CM': 'ЯУНДЕ', 'CN': 'ПЕКИН', 'CO': 'БОГОТА',
            'CR': 'САН-ХОСЕ', 'CU': 'ГАВАНА', 'CV': 'ПРАЯ', 'CW': 'ВИЛЛЕМСТАД',
            'CX': 'ФЛАЙИНГ-ФИШ-КОВ', 'CY': 'НИКОСИЯ', 'CZ': 'ПРАГА', 'DE': 'БЕРЛИН',
            'DJ': 'ДЖИБУТИ', 'DK': 'КОПЕНГАГЕН', 'DM': 'РОЗО', 'DO': 'САНТО-ДОМИНГО',
            'DZ': 'АЛЖИР', 'EC': 'КИТО', 'EE': 'ТАЛЛИН', 'EG': 'КАИР',
            'EH': 'ЭЛЬ-АЮН', 'ER': 'АСМЭРА', 'ES': 'МАДРИД', 'ET': 'АДДИС-АБЕБА',
            'FI': 'ХЕЛЬСИНКИ', 'FJ': 'СУВА', 'FK': 'СТЭНЛИ', 'FM': 'ПАЛИКИР',
            'FO': 'ТОРСХАВН', 'FR': 'ПАРИЖ', 'GA': 'ЛИБРЕВИЛЬ', 'GB': 'ЛОНДОН',
            'GD': 'СЕНТ-ДЖОРДЖЕС', 'GE': 'ТБИЛИСИ', 'GF': 'КАЙЕННА', 'GG': 'СЕНТ-ПИТЕР-ПОРТ',
            'GH': 'АККРА', 'GI': 'ГИБРАЛТАР', 'GL': 'НУУК', 'GM': 'БАНЖУЛ',
            'GN': 'КОНАКРИ', 'GP': 'БАСТЕР', 'GQ': 'МАЛАБО', 'GR': 'АФИНЫ',
            'GS': 'КИНГ-ЭДУАРД-ПОЙНТ', 'GT': 'ГВАТЕМАЛА', 'GU': 'ХАГАТНА', 'GW': 'БИСАУ',
            'GY': 'ДЖОРДЖТАУН', 'HK': 'ГОНКОНГ', 'HM': 'ХЕРД', 'HN': 'ТЕГУСИГАЛЬПА',
            'HR': 'ЗАГРЕБ', 'HT': 'ПОРТ-О-ПРЕНС', 'HU': 'БУДАПЕШТ', 'ID': 'ДЖАКАРТА',
            'IE': 'ДУБЛИН', 'IL': 'ИЕРУСАЛИМ', 'IM': 'ДУГЛАС', 'IN': 'НЬЮ-ДЕЛИ',
            'IO': 'ДИЕГО-ГАРСИЯ', 'IQ': 'БАГДАД', 'IR': 'ТЕГЕРАН', 'IS': 'РЕЙКЬЯВИК',
            'IT': 'РИМ', 'JE': 'СЕНТ-ХЕЛИЕР', 'JM': 'КИНГСТОН', 'JO': 'АММАН',
            'JP': 'ТОКИО', 'KE': 'НАЙРОБИ', 'KG': 'БИШКЕК', 'KH': 'ПНОМПЕНЬ',
            'KI': 'ТАРАВА', 'KM': 'МОРОНИ', 'KN': 'БАСТЕР', 'KP': 'ПХЕНЬЯН',
            'KR': 'СЕУЛ', 'KW': 'ЭЛЬКУВЕЙТ', 'KY': 'ДЖОРДЖТАУН', 'KZ': 'АСТАНА',
            'LA': 'ВЬЕНТЬЯН', 'LB': 'БЕЙРУТ', 'LC': 'КАСТРИ', 'LI': 'ВАДУЦ',
            'LK': 'КОЛОМБО', 'LR': 'МОНРОВИЯ', 'LS': 'МАСЕРУ', 'LT': 'ВИЛЬНЮС',
            'LU': 'ЛЮКСЕМБУРГ', 'LV': 'РИГА', 'LY': 'ТРИПОЛИ', 'MA': 'РАБАТ',
            'MC': 'МОНАКО', 'MD': 'КИШИНЕВ', 'ME': 'ПОДГОРИЦА', 'MF': 'МАРИГО',
            'MG': 'АНТАНАНАРИВУ', 'MH': 'МАДЖУРО', 'MK': 'СКОПЬЕ', 'ML': 'БАМАКО',
            'MM': 'НЕЙПЬИДО', 'MN': 'УЛАН-БАТОР', 'MO': 'МАКАО', 'MP': 'САЙПАН',
            'MQ': 'ФОР-ДЕ-ФРАНС', 'MR': 'НУАКШОТ', 'MS': 'ПЛИМУТ', 'MT': 'ВАЛЛЕТТА',
            'MU': 'ПОРТ-ЛУИ', 'MV': 'МАЛЕ', 'MW': 'ЛИЛОНГВЕ', 'MX': 'МЕХИКО',
            'MY': 'КУАЛА-ЛУМПУР', 'MZ': 'МАПУТУ', 'NA': 'ВИНДХУК', 'NC': 'НУМЕА',
            'NE': 'НИАМЕЙ', 'NF': 'КИНГСТОН', 'NG': 'АБУДЖА', 'NI': 'МАНАГУА',
            'NL': 'АМСТЕРДАМ', 'NO': 'ОСЛО', 'NP': 'КАТМАНДУ', 'NR': 'ЯРЕН',
            'NU': 'АЛОФИ', 'NZ': 'ВЕЛЛИНГТОН', 'OM': 'МАСКАТ', 'PA': 'ПАНАМА',
            'PE': 'ЛИМА', 'PF': 'ПАПЕЭТЕ', 'PG': 'ПОРТ-МОРСБИ', 'PH': 'МАНИЛА',
            'PK': 'ИСЛАМАБАД', 'PL': 'ВАРШАВА', 'PM': 'СЕН-ПЬЕР', 'PN': 'АДАМСТАУН',
            'PR': 'САН-ХУАН', 'PS': 'РАМАЛЛА', 'PT': 'ЛИССАБОН', 'PW': 'НГЕРУЛМУД',
            'PY': 'АСУНСЬОН', 'QA': 'ДОХА', 'RE': 'САН-ДЕНИ', 'RO': 'БУХАРЕСТ',
            'RS': 'БЕЛГРАД', 'RU': 'МОСКВА', 'RW': 'КИГАЛИ', 'SA': 'ЭР-РИЯД',
            'SB': 'ХОНИАРА', 'SC': 'ВИКТОРИЯ', 'SD': 'ХАРТУМ', 'SE': 'СТОКГОЛЬМ',
            'SG': 'СИНГАПУР', 'SH': 'ДЖЕЙМСТАУН', 'SI': 'ЛЮБЛЯНА', 'SJ': 'ЛОНГЬИР',
            'SK': 'БРАТИСЛАВА', 'SL': 'ФРИТАУН', 'SM': 'САН-МАРИНО', 'SN': 'ДАКАР',
            'SO': 'МОГАДИШО', 'SR': 'ПАРАМАРИБО', 'SS': 'ДЖУБА', 'ST': 'САН-ТОМЕ',
            'SV': 'САН-САЛЬВАДОР', 'SX': 'ФИЛИПСБУРГ', 'SY': 'ДАМАСК', 'SZ': 'МБАБАНЕ',
            'TC': 'КОБЕРН-ТАУН', 'TD': 'НДЖАМЕНА', 'TF': 'ПОРТ-О-ФРАНСЕ', 'TG': 'ЛОМЕ',
            'TH': 'БАНГКОК', 'TJ': 'ДУШАНБЕ', 'TK': 'НУКУАЛОФА', 'TL': 'ДИЛИ',
            'TM': 'АШХАБАД', 'TN': 'ТУНИС', 'TO': 'НУКУАЛОФА', 'TR': 'АНКАРА',
            'TT': 'ПОРТ-ОФ-СПЕЙН', 'TV': 'ФУНАФУТИ', 'TW': 'ТАЙБЭЙ', 'TZ': 'ДОДОМА',
            'UA': 'КИЕВ', 'UG': 'КАМПАЛА', 'UM': 'АТОЛЛ', 'US': 'ВАШИНГТОН',
            'UY': 'МОНТЕВИДЕО', 'UZ': 'ТАШКЕНТ', 'VA': 'ВАТИКАН', 'VC': 'КИНГСТАУН',
            'VE': 'КАРАКАС', 'VG': 'РОУД-ТАУН', 'VI': 'ШАРЛОТТА-АМАЛИЯ', 'VN': 'ХАНОЙ',
            'VU': 'ПОРТ-ВИЛА', 'WF': 'МАТА-УТУ', 'WS': 'АПИА', 'YE': 'САНА',
            'YT': 'МАМУДЗУ', 'ZA': 'КЕЙПТАУН', 'ZM': 'ЛУСАКА', 'ZW': 'ХАРАРЕ'
        };
    }

    async generateCapitalsFile() {
        console.log('🏛️ Генерация полного файла столиц...');
        
        const availableCodes = [];
        
        // Проверяем какие коды стран действительно доступны как изображения
        for (const [code, capital] of Object.entries(this.countriesData)) {
            try {
                const response = await fetch(`/data/images/capitals/${code}.png`, { method: 'HEAD' });
                if (response.ok) {
                    availableCodes.push({ code, capital });
                    console.log(`✅ ${code} -> ${capital}`);
                } else {
                    console.log(`❌ Отсутствует: ${code}.png`);
                }
            } catch (error) {
                console.log(`💥 Ошибка: ${code}.png`);
            }
        }
        
        // Генерируем содержимое файла
        const fileContent = availableCodes
            .sort((a, b) => a.code.localeCompare(b.code))
            .map((item, index) => `${index + 1} - ${item.capital} - ${item.code}`)
            .join('\n');
        
        console.log(`\n📊 Создано записей столиц: ${availableCodes.length}`);
        console.log('\n📄 СОДЕРЖИМОЕ ФАЙЛА capitals.txt:');
        console.log('=' .repeat(50));
        console.log(fileContent);
        console.log('=' .repeat(50));
        
        return fileContent;
    }

    extractPlayerName(filename) {
        // Убираем расширение .png
        let name = filename.replace('.png', '');
        
        // Убираем номер в конце (например -1923, -257)
        name = name.replace(/-\d+$/, '');
        
        // Убираем односимвольные префиксы в начале (А, Б, М, И, З, etc.)
        if (name.match(/^[А-Я]\s/)) {
            name = name.substring(2); // Убираем "А " или "Б " etc.
        }
        
        return name.trim();
    }

    async scanFootballersDirectory() {
        console.log('⚽ Загрузка полного списка футболистов...');
        
        // Проверяем наличие файла со списком всех футболистов
        let allFiles = [];
        try {
            const response = await fetch('/footballers_files_list.js');
            if (response.ok) {
                const jsContent = await response.text();
                // Извлекаем массив из JavaScript файла
                const match = jsContent.match(/const allFootballerFiles = \[([\s\S]*?)\];/);
                if (match) {
                    const arrayContent = match[1];
                    allFiles = arrayContent
                        .split('\n')
                        .map(line => line.trim())
                        .filter(line => line.startsWith("'") && line.endsWith("',") || line.endsWith("'"))
                        .map(line => line.replace(/^'|'[,]?$/g, ''));
                    
                    console.log(`📁 Загружен список из файла: ${allFiles.length} файлов`);
                }
            }
        } catch (error) {
            console.log('⚠️ Не удалось загрузить файл списка, используем базовый набор');
        }
        
        // Если файл не загрузился, используем базовый набор
        if (allFiles.length === 0) {
            allFiles = [
                'А БАИРАМИ-257.png', 'А КХАЛАИЛИ-1874.png', 'Б ЗОУКРОУ-1902.png',
                'КРИС БЕДИА-1921.png', 'ЖОЭЛЬ МОНТЕИРУ-1923.png', 'НИКОЛАС ГОНСАЛЕС-915.png',
                'М СЕИЛЕР-1909.png', 'И ДЕМА-1917.png', 'З АТХЕКАМЕ-1907.png',
                'АЛАН ВИРЖИНИУС-1920.png', 'ЭБРИМА КОЛЛИ-1919.png'
            ];
            console.log(`📦 Используем базовый набор: ${allFiles.length} файлов`);
        }
        
        const footballers = [];
        
        console.log(`🔄 Обработка ${allFiles.length} файлов...`);
        
        for (let i = 0; i < allFiles.length; i++) {
            const filename = allFiles[i];
            const playerName = this.extractPlayerName(filename);
            const imageCode = filename.replace('.png', '');
            
            footballers.push({
                id: i + 1,
                name: playerName,
                imageCode: imageCode,
                filename: filename
            });
            
            // Показываем прогресс каждые 100 файлов
            if ((i + 1) % 100 === 0) {
                console.log(`📊 Обработано: ${i + 1}/${allFiles.length}`);
            }
            
            // Показываем первые 10 для примера
            if (i < 10) {
                console.log(`⚽ ${i + 1}: ${playerName} -> ${imageCode}`);
            }
        }
        
        return footballers;
    }

    async generateFootballersFile() {
        console.log('⚽ Генерация файла футболистов...');
        
        const footballers = await this.scanFootballersDirectory();
        
        const fileContent = footballers
            .map(player => `${player.id} - ${player.name} - ${player.imageCode}`)
            .join('\n');
        
        console.log(`\n📊 Создано записей футболистов: ${footballers.length}`);
        console.log('\n📄 СОДЕРЖИМОЕ ФАЙЛА footballers.txt:');
        console.log('=' .repeat(50));
        console.log(fileContent);
        console.log('=' .repeat(50));
        
        return fileContent;
    }

    async generateAllFiles() {
        console.log('🚀 === ГЕНЕРАЦИЯ ПОЛНЫХ ФАЙЛОВ ДАННЫХ ===\n');
        
        const capitalsContent = await this.generateCapitalsFile();
        console.log('\n' + '='.repeat(80) + '\n');
        const footballersContent = await this.generateFootballersFile();
        
        console.log('\n🎯 === ИТОГО ===');
        console.log('📍 Столицы: готов файл с максимальным количеством записей');
        console.log('⚽ Футболисты: создан расширенный файл (можно добавить больше)');
        console.log('\n💡 Файлы готовы для копирования в data/words/ru/');
        
        return {
            capitals: capitalsContent,
            footballers: footballersContent
        };
    }
}

// Глобальные функции
window.generateAllData = async function() {
    const generator = new FullDataGenerator();
    await generator.generateAllFiles();
};

window.generateCapitalsOnly = async function() {
    const generator = new FullDataGenerator();
    await generator.generateCapitalsFile();
};

window.generateFootballersOnly = async function() {
    const generator = new FullDataGenerator();
    await generator.generateFootballersFile();
};

// Функция для создания готовых файлов, которые можно скопировать
window.createFullDataFiles = async function() {
    console.log('💾 === СОЗДАНИЕ ГОТОВЫХ ФАЙЛОВ ДАННЫХ ===\n');
    
    const generator = new FullDataGenerator();
    const results = await generator.generateAllFiles();
    
    console.log('\n' + '='.repeat(100));
    console.log('📄 ГОТОВЫЕ ФАЙЛЫ ДЛЯ КОПИРОВАНИЯ:');
    console.log('='.repeat(100));
    
    // Создаем downloadable links (эмуляция)
    console.log('\n🎯 Данные готовы! Скопируйте содержимое в соответствующие файлы:');
    console.log('\n1️⃣ Файл data/words/ru/capitals.txt');
    console.log('2️⃣ Файл data/words/ru/footballers.txt');
    console.log('\n📋 Содержимое файлов показано выше в консоли');
    
    return results;
};

window.addEventListener('load', () => {
    console.log('🛠️ Генератор полных данных загружен. Используйте:');
    console.log('- generateAllData() - для всех файлов');
    console.log('- generateCapitalsOnly() - только столицы');
    console.log('- generateFootballersOnly() - только футболисты');
    console.log('- createFullDataFiles() - создать готовые файлы');
}); 