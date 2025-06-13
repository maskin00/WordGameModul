// Скрипт для исправления сопоставлений изображений
class ImageMappingFixer {
    constructor() {
        this.availableImages = {
            capitals: [],
            footballers: []
        };
        this.wordData = {
            capitals: [],
            footballers: []
        };
    }

    async analyzeAvailableImages() {
        console.log('[Fix] Анализ доступных изображений...');
        
        // Получаем список файлов изображений через HTTP запросы
        await this.scanImageDirectory('capitals');
        await this.scanImageDirectory('footballers');
    }

    async scanImageDirectory(category) {
        console.log(`[Fix] Сканирование папки ${category}...`);
        
        // Список известных файлов на основе ранее увиденных
        const knownImages = await this.getKnownImages(category);
        const validImages = [];
        
        for (const imageName of knownImages) {
            try {
                const response = await fetch(`/data/images/${category}/${imageName}`, { method: 'HEAD' });
                if (response.ok) {
                    validImages.push(imageName);
                    console.log(`[Fix] ✓ Найдено изображение: ${imageName}`);
                }
            } catch (error) {
                console.log(`[Fix] ✗ Недоступно: ${imageName}`);
            }
        }
        
        this.availableImages[category] = validImages;
        console.log(`[Fix] Найдено ${validImages.length} изображений для ${category}`);
    }

    async getKnownImages(category) {
        if (category === 'capitals') {
            // Коды стран для столиц
            return [
                'AD.png', 'AE.png', 'AF.png', 'AG.png', 'AI.png', 'AL.png', 'AM.png', 'AO.png',
                'AR.png', 'AS.png', 'AT.png', 'AU.png', 'AW.png', 'AX.png', 'AZ.png', 'BA.png',
                'BB.png', 'BD.png', 'BE.png', 'BF.png', 'BG.png', 'BH.png', 'BI.png', 'BJ.png',
                'BL.png', 'BM.png', 'BN.png', 'BO.png', 'BQ.png', 'BR.png', 'BS.png', 'BT.png',
                'BV.png', 'BW.png', 'BY.png', 'BZ.png', 'CA.png', 'CC.png', 'CD.png', 'CF.png',
                'CG.png', 'CH.png', 'CI.png', 'CK.png', 'CL.png', 'CM.png', 'CN.png', 'CO.png',
                'CR.png', 'CU.png', 'CV.png', 'CW.png', 'CX.png', 'CY.png', 'CZ.png', 'DE.png',
                'DJ.png', 'DK.png', 'DM.png', 'DO.png', 'DZ.png', 'EC.png', 'EE.png', 'EG.png',
                'EH.png', 'ER.png', 'ES.png', 'ET.png', 'FI.png', 'FJ.png', 'FK.png', 'FM.png',
                'FO.png', 'FR.png', 'GA.png', 'GB.png', 'GD.png', 'GE.png', 'GF.png', 'GG.png',
                'GH.png', 'GI.png', 'GL.png', 'GM.png', 'GN.png', 'GP.png', 'GQ.png', 'GR.png',
                'GS.png', 'GT.png', 'GU.png', 'GW.png', 'GY.png', 'HK.png', 'HM.png', 'HN.png',
                'HR.png', 'HT.png', 'HU.png', 'ID.png', 'IE.png', 'IL.png', 'IM.png', 'IN.png',
                'IO.png', 'IQ.png', 'IR.png', 'IS.png', 'IT.png', 'JE.png', 'JM.png', 'JO.png',
                'JP.png', 'KE.png', 'KG.png', 'KH.png', 'KI.png', 'KM.png', 'KN.png', 'KP.png',
                'KR.png', 'KW.png', 'KY.png', 'KZ.png', 'LA.png', 'LB.png', 'LC.png', 'LI.png',
                'LK.png', 'LR.png', 'LS.png', 'LT.png', 'LU.png', 'LV.png', 'LY.png', 'MA.png',
                'MC.png', 'MD.png', 'ME.png', 'MF.png', 'MG.png', 'MH.png', 'MK.png', 'ML.png',
                'MM.png', 'MN.png', 'MO.png', 'MP.png', 'MQ.png', 'MR.png', 'MS.png', 'MT.png',
                'MU.png', 'MV.png', 'MW.png', 'MX.png', 'MY.png', 'MZ.png', 'NA.png', 'NC.png',
                'NE.png', 'NF.png', 'NG.png', 'NI.png', 'NL.png', 'NO.png', 'NP.png', 'NR.png',
                'NU.png', 'NZ.png', 'OM.png', 'PA.png', 'PE.png', 'PF.png', 'PG.png', 'PH.png',
                'PK.png', 'PL.png', 'PM.png', 'PN.png', 'PR.png', 'PS.png', 'PT.png', 'PW.png',
                'PY.png', 'QA.png', 'RE.png', 'RO.png', 'RS.png', 'RU.png', 'RW.png', 'SA.png',
                'SB.png', 'SC.png', 'SD.png', 'SE.png', 'SG.png', 'SH.png', 'SI.png', 'SJ.png',
                'SK.png', 'SL.png', 'SM.png', 'SN.png', 'SO.png', 'SR.png', 'SS.png', 'ST.png',
                'SV.png', 'SX.png', 'SY.png', 'SZ.png', 'TC.png', 'TD.png', 'TF.png', 'TG.png',
                'TH.png', 'TJ.png', 'TK.png', 'TL.png', 'TM.png', 'TN.png', 'TO.png', 'TR.png',
                'TT.png', 'TV.png', 'TW.png', 'TZ.png', 'UA.png', 'UG.png', 'UM.png', 'US.png',
                'UY.png', 'UZ.png', 'VA.png', 'VC.png', 'VE.png', 'VG.png', 'VI.png', 'VN.png',
                'VU.png', 'WF.png', 'WS.png', 'YE.png', 'YT.png', 'ZA.png', 'ZM.png', 'ZW.png'
            ];
        } else if (category === 'footballers') {
            // Получаем список существующих изображений футболистов из папки
            // Данный список основан на том, что мы видели в directory listing
            return [
                'А БАИРАМИ-257.png',
                'А ВАН ХООРЕНБЕЕЦК-1439.png',
                'А ВАРГА-1555.png',
                'А ГЛУШЧЕНКО-1716.png',
                'А КХАЛАИЛИ-1874.png',
                'А РАН-730.png',
                'А ТАХО-644.png',
                'АБДУЛКЕРИМ БАРДАКЧИ-472.png',
                'АБЕЛЬ РУИС-634.png',
                'ААРОН ГРИН-1739.png',
                'КРИС БЕДИА-1921.png',
                'ЖОЭЛЬ МОНТЕИРУ-1923.png',
                'ФАСИНЕ КОНТЕ-1922.png',
                'АЛАН ВИРЖИНИУС-1920.png',
                'ЭБРИМА КОЛЛИ-1919.png',
                'РАИАН РАВЕЛСОН-1916.png',
                'СЕДРИК ИТТЕН-1918.png',
                'САНДРО ЛАУПЕР-1914.png',
                'ДАРИАН МАЛЕШ-1915.png',
                'КАСТРИОТ ИМЕРИ-1911.png',
                'И ДЕМА-1917.png',
                'МИГЕЛЬ ЧАНГА ЧАИВА-1912.png',
                'КРИСТИАН ФАССНАХТ-1913.png',
                // Добавим еще известные...
                'НИКОЛАС ГОНСАЛЕС-915.png',
                'АБДУЛЛА ЗУБИР-690.png'
            ];
        }
        return [];
    }

    async loadCurrentWordData() {
        console.log('[Fix] Загрузка текущих данных...');
        
        // Загружаем столицы
        try {
            const capitalsResponse = await fetch('/data/words/ru/capitals.txt');
            const capitalsText = await capitalsResponse.text();
            this.wordData.capitals = this.parseWordFile(capitalsText);
            console.log(`[Fix] Загружено ${this.wordData.capitals.length} записей столиц`);
        } catch (error) {
            console.error('[Fix] Ошибка загрузки столиц:', error);
        }

        // Загружаем футболистов
        try {
            const footballersResponse = await fetch('/data/words/ru/footballers.txt');
            const footballersText = await footballersResponse.text();
            this.wordData.footballers = this.parseWordFile(footballersText);
            console.log(`[Fix] Загружено ${this.wordData.footballers.length} записей футболистов`);
        } catch (error) {
            console.error('[Fix] Ошибка загрузки футболистов:', error);
        }
    }

    parseWordFile(text) {
        return text.trim().split('\n').map((line, index) => {
            const parts = line.split(' - ');
            if (parts.length >= 3) {
                return {
                    number: parseInt(parts[0]),
                    word: parts[1].trim(),
                    imageCode: parts[2].trim(),
                    originalLine: line,
                    lineNumber: index + 1
                };
            }
            return null;
        }).filter(item => item !== null);
    }

    async generateFixedFiles() {
        console.log('[Fix] Генерация исправленных файлов...');
        
        await this.analyzeAvailableImages();
        await this.loadCurrentWordData();
        
        // Исправляем столицы
        const fixedCapitals = this.fixCapitalsMapping();
        
        // Исправляем футболистов
        const fixedFootballers = this.fixFootballersMapping();
        
        // Выводим результаты
        this.displayResults(fixedCapitals, fixedFootballers);
    }

    fixCapitalsMapping() {
        console.log('[Fix] Исправление сопоставлений столиц...');
        const fixed = [];
        const missing = [];
        
        for (const capital of this.wordData.capitals) {
            const imageFile = `${capital.imageCode}.png`;
            if (this.availableImages.capitals.includes(imageFile)) {
                fixed.push(capital);
                console.log(`[Fix] ✓ ${capital.word} -> ${capital.imageCode}`);
            } else {
                missing.push(capital);
                console.warn(`[Fix] ✗ Отсутствует изображение для ${capital.word}: ${imageFile}`);
            }
        }
        
        return { fixed, missing, total: this.wordData.capitals.length };
    }

    fixFootballersMapping() {
        console.log('[Fix] Исправление сопоставлений футболистов...');
        const fixed = [];
        const corrections = [];
        
        for (const footballer of this.wordData.footballers) {
            // Проверяем, нужно ли добавить префикс "А "
            if (!footballer.imageCode.startsWith('А ')) {
                const corrected = {
                    ...footballer,
                    imageCode: `А ${footballer.imageCode}`,
                    corrected: true
                };
                corrections.push(corrected);
                console.log(`[Fix] 🔧 Исправлено: ${footballer.word} -> А ${footballer.imageCode}`);
            } else {
                fixed.push(footballer);
                console.log(`[Fix] ✓ ${footballer.word} -> ${footballer.imageCode}`);
            }
        }
        
        return { fixed, corrections, total: this.wordData.footballers.length };
    }

    displayResults(capitalsResult, footballersResult) {
        console.log('\n=== РЕЗУЛЬТАТЫ АНАЛИЗА ===');
        
        console.log(`\nСТОЛИЦЫ:`);
        console.log(`- Корректных: ${capitalsResult.fixed.length}/${capitalsResult.total}`);
        console.log(`- Отсутствующих: ${capitalsResult.missing.length}`);
        
        console.log(`\nФУТБОЛИСТЫ:`);
        console.log(`- Корректных: ${footballersResult.fixed.length}/${footballersResult.total}`);
        console.log(`- Исправленных: ${footballersResult.corrections.length}`);
        
        if (footballersResult.corrections.length > 0) {
            console.log('\n=== ИСПРАВЛЕННЫЙ ФАЙЛ ФУТБОЛИСТОВ ===');
            const correctedData = [
                ...footballersResult.fixed,
                ...footballersResult.corrections
            ].sort((a, b) => a.number - b.number);
            
            correctedData.forEach(item => {
                console.log(`${item.number} - ${item.word} - ${item.imageCode}`);
            });
            
            // Генерируем содержимое для нового файла
            console.log('\n=== СОДЕРЖИМОЕ ДЛЯ КОПИРОВАНИЯ ===');
            const fileContent = correctedData.map(item => 
                `${item.number} - ${item.word} - ${item.imageCode}`
            ).join('\n');
            console.log(fileContent);
        }
    }
}

// Глобальная функция для запуска исправления
window.fixImageMapping = async function() {
    const fixer = new ImageMappingFixer();
    await fixer.generateFixedFiles();
};

// Автозапуск при загрузке
window.addEventListener('load', () => {
    console.log('Система исправления сопоставлений загружена. Используйте fixImageMapping() для запуска.');
}); 