// Скрипт для создания полных переводов столиц и футболистов
// Запускать в браузере на странице игры

// Словарь переводов столиц с русского на английский
const capitalTranslations = {
    'АНДОРРА-ЛА-ВЕЛЬЯ': 'ANDORRA LA VELLA',
    'АБУ-ДАБИ': 'ABU DHABI',
    'КАБУЛ': 'KABUL',
    'СЕНТ-ДЖОНС': 'SAINT JOHNS',
    'ОСТРОВ АНГИЛЬЯ': 'THE VALLEY',
    'ТИРАНА': 'TIRANA',
    'ЕРЕВАН': 'YEREVAN',
    'ЛУАНДА': 'LUANDA',
    'БУЭНОС-АЙРЕС': 'BUENOS AIRES',
    'СТАНЦИЯ МАК-МЕРДО': 'MCMURDO STATION',
    'ПАГО-ПАГО': 'PAGO PAGO',
    'ВЕНА': 'VIENNA',
    'КАНБЕРРА': 'CANBERRA',
    'ОРАНЬЕСТАД': 'ORANJESTAD',
    'МАРИЕХАМН': 'MARIEHAMN',
    'БАКУ': 'BAKU',
    'САРАЕВО': 'SARAJEVO',
    'БРИДЖТАУН': 'BRIDGETOWN',
    'ДАККА': 'DHAKA',
    'БРЮССЕЛЬ': 'BRUSSELS',
    'УАГАДУГУ': 'OUAGADOUGOU',
    'СОФИЯ': 'SOFIA',
    'МАНАМА': 'MANAMA',
    'ГИТЕГА': 'GITEGA',
    'ПОРТО-НОВО': 'PORTO NOVO',
    'ГУСТАВИЯ': 'GUSTAVIA',
    'ГАМИЛЬТОН': 'HAMILTON',
    'БАНДАР-СЕРИ-БЕГАВАН': 'BANDAR SERI BEGAWAN',
    'СУКРЕ': 'SUCRE',
    'КРАЛЕНДЕЙК': 'KRALENDIJK',
    'БРАЗИЛИА': 'BRASILIA',
    'НАССАУ': 'NASSAU',
    'ТХИМПХУ': 'THIMPHU',
    'БУВЕ': 'BOUVET',
    'ГАБОРОНЕ': 'GABORONE',
    'МИНСК': 'MINSK',
    'БЕЛЬМОПАН': 'BELMOPAN',
    'ОТТАВА': 'OTTAWA',
    'УЭСТ-АЙЛЕНД': 'WEST ISLAND',
    'КИНШАСА': 'KINSHASA',
    'БАНГИ': 'BANGUI',
    'БРАЗЗАВИЛЬ': 'BRAZZAVILLE',
    'БЕРН': 'BERN',
    'ЯМУСУКРО': 'YAMOUSSOUKRO',
    'АВАРАМАНГА': 'AVARUA',
    'САНТЬЯГО': 'SANTIAGO',
    'ЯУНДЕ': 'YAOUNDE',
    'ПЕКИН': 'BEIJING',
    'БОГОТА': 'BOGOTA',
    'САН-ХОСЕ': 'SAN JOSE',
    'ГАВАНА': 'HAVANA',
    'ПРАЯ': 'PRAIA',
    'ВИЛЛЕМСТАД': 'WILLEMSTAD',
    'ФЛАЙИНГ-ФИШ-КОВ': 'FLYING FISH COVE',
    'НИКОСИЯ': 'NICOSIA',
    'ПРАГА': 'PRAGUE',
    'БЕРЛИН': 'BERLIN',
    'ДЖИБУТИ': 'DJIBOUTI',
    'КОПЕНГАГЕН': 'COPENHAGEN',
    'РОЗО': 'ROSEAU',
    'САНТО-ДОМИНГО': 'SANTO DOMINGO',
    'АЛЖИР': 'ALGIERS',
    'КИТО': 'QUITO',
    'ТАЛЛИН': 'TALLINN',
    'КАИР': 'CAIRO',
    'ЭЛЬ-АЮН': 'EL AAIUN',
    'АСМЭРА': 'ASMARA',
    'МАДРИД': 'MADRID',
    'АДДИС-АБЕБА': 'ADDIS ABABA',
    'ХЕЛЬСИНКИ': 'HELSINKI',
    'СУВА': 'SUVA',
    'СТЭНЛИ': 'STANLEY',
    'ПАЛИКИР': 'PALIKIR',
    'ТОРСХАВН': 'TORSHAVN',
    'ПАРИЖ': 'PARIS',
    'ЛИБРЕВИЛЬ': 'LIBREVILLE',
    'ЛОНДОН': 'LONDON',
    'БЕЛФАСТ': 'BELFAST',
    'ЭДИНБУРГ': 'EDINBURGH',
    'КАРДИФФ': 'CARDIFF',
    'СЕНТ-ДЖОРДЖЕС': 'SAINT GEORGES',
    'ТБИЛИСИ': 'TBILISI',
    'КАЙЕННА': 'CAYENNE',
    'СЕНТ-ПИТЕР-ПОРТ': 'SAINT PETER PORT',
    'АККРА': 'ACCRA',
    'ГИБРАЛТАР': 'GIBRALTAR',
    'НУУК': 'NUUK',
    'БАНЖУЛ': 'BANJUL',
    'КОНАКРИ': 'CONAKRY',
    'БАСТЕР': 'BASSE TERRE',
    'МАЛАБО': 'MALABO',
    'АФИНЫ': 'ATHENS',
    'КИНГ-ЭДУАРД-ПОЙНТ': 'KING EDWARD POINT',
    'ГВАТЕМАЛА': 'GUATEMALA CITY',
    'ХАГАТНА': 'HAGATNA',
    'БИСАУ': 'BISSAU',
    'ДЖОРДЖТАУН': 'GEORGETOWN',
    'ГОНКОНГ': 'HONG KONG',
    'ХЕРД': 'HEARD ISLAND',
    'ТЕГУСИГАЛЬПА': 'TEGUCIGALPA',
    'ЗАГРЕБ': 'ZAGREB',
    'ПОРТ-О-ПРЕНС': 'PORT AU PRINCE',
    'БУДАПЕШТ': 'BUDAPEST',
    'ДЖАКАРТА': 'JAKARTA',
    'ДУБЛИН': 'DUBLIN',
    'ИЕРУСАЛИМ': 'JERUSALEM',
    'ДУГЛАС': 'DOUGLAS',
    'НЬЮ-ДЕЛИ': 'NEW DELHI',
    'ДИЕГО-ГАРСИЯ': 'DIEGO GARCIA',
    'БАГДАД': 'BAGHDAD',
    'ТЕГЕРАН': 'TEHRAN',
    'РЕЙКЬЯВИК': 'REYKJAVIK',
    'РИМ': 'ROME',
    'СЕНТ-ХЕЛИЕР': 'SAINT HELIER',
    'КИНГСТОН': 'KINGSTON',
    'АММАН': 'AMMAN',
    'ТОКИО': 'TOKYO',
    'НАЙРОБИ': 'NAIROBI',
    'БИШКЕК': 'BISHKEK',
    'ПНОМПЕНЬ': 'PHNOM PENH',
    'ТАРАВА': 'TARAWA',
    'МОРОНИ': 'MORONI',
    'ПХЕНЬЯН': 'PYONGYANG',
    'СЕУЛ': 'SEOUL',
    'ЭЛЬКУВЕЙТ': 'KUWAIT CITY',
    'АСТАНА': 'ASTANA',
    'ВЬЕНТЬЯН': 'VIENTIANE',
    'БЕЙРУТ': 'BEIRUT',
    'КАСТРИ': 'CASTRIES',
    'ВАДУЦ': 'VADUZ',
    'КОЛОМБО': 'COLOMBO',
    'МОНРОВИЯ': 'MONROVIA',
    'МАСЕРУ': 'MASERU',
    'ВИЛЬНЮС': 'VILNIUS',
    'ЛЮКСЕМБУРГ': 'LUXEMBOURG',
    'РИГА': 'RIGA',
    'ТРИПОЛИ': 'TRIPOLI',
    'РАБАТ': 'RABAT',
    'МОНАКО': 'MONACO',
    'КИШИНЕВ': 'CHISINAU',
    'ПОДГОРИЦА': 'PODGORICA',
    'МАРИГО': 'MARIGOT',
    'АНТАНАНАРИВУ': 'ANTANANARIVO',
    'МАДЖУРО': 'MAJURO',
    'СКОПЬЕ': 'SKOPJE',
    'БАМАКО': 'BAMAKO',
    'НЕЙПЬИДО': 'NAYPYIDAW',
    'УЛАН-БАТОР': 'ULAANBAATAR',
    'МАКАО': 'MACAU',
    'САЙПАН': 'SAIPAN',
    'ФОР-ДЕ-ФРАНС': 'FORT DE FRANCE',
    'НУАКШОТ': 'NOUAKCHOTT',
    'ПЛИМУТ': 'PLYMOUTH',
    'ВАЛЛЕТТА': 'VALLETTA',
    'ПОРТ-ЛУИ': 'PORT LOUIS',
    'МАЛЕ': 'MALE',
    'ЛИЛОНГВЕ': 'LILONGWE',
    'МЕХИКО': 'MEXICO CITY',
    'КУАЛА-ЛУМПУР': 'KUALA LUMPUR',
    'МАПУТУ': 'MAPUTO',
    'ВИНДХУК': 'WINDHOEK',
    'НУМЕА': 'NOUMEA',
    'НИАМЕЙ': 'NIAMEY',
    'АБУДЖА': 'ABUJA',
    'МАНАГУА': 'MANAGUA',
    'АМСТЕРДАМ': 'AMSTERDAM',
    'ОСЛО': 'OSLO',
    'КАТМАНДУ': 'KATHMANDU',
    'ЯРЕН': 'YAREN',
    'АЛОФИ': 'ALOFI',
    'ВЕЛЛИНГТОН': 'WELLINGTON',
    'МАСКАТ': 'MUSCAT',
    'ПАНАМА': 'PANAMA CITY',
    'ЛИМА': 'LIMA',
    'ПАПЕЭТЕ': 'PAPEETE',
    'ПОРТ-МОРСБИ': 'PORT MORESBY',
    'МАНИЛА': 'MANILA',
    'ИСЛАМАБАД': 'ISLAMABAD',
    'ВАРШАВА': 'WARSAW',
    'СЕН-ПЬЕР': 'SAINT PIERRE',
    'АДАМСТАУН': 'ADAMSTOWN',
    'САН-ХУАН': 'SAN JUAN',
    'РАМАЛЛА': 'RAMALLAH',
    'ЛИССАБОН': 'LISBON',
    'НГЕРУЛМУД': 'NGERULMUD',
    'АСУНСЬОН': 'ASUNCION',
    'ДОХА': 'DOHA',
    'САН-ДЕНИ': 'SAINT DENIS',
    'БУХАРЕСТ': 'BUCHAREST',
    'БЕЛГРАД': 'BELGRADE',
    'МОСКВА': 'MOSCOW',
    'КИГАЛИ': 'KIGALI',
    'ЭР-РИЯД': 'RIYADH',
    'ХОНИАРА': 'HONIARA',
    'ВИКТОРИЯ': 'VICTORIA',
    'ХАРТУМ': 'KHARTOUM',
    'СТОКГОЛЬМ': 'STOCKHOLM',
    'СИНГАПУР': 'SINGAPORE',
    'ДЖЕЙМСТАУН': 'JAMESTOWN',
    'ЛЮБЛЯНА': 'LJUBLJANA',
    'ЛОНГЬИР': 'LONGYEARBYEN',
    'БРАТИСЛАВА': 'BRATISLAVA',
    'ФРИТАУН': 'FREETOWN',
    'САН-МАРИНО': 'SAN MARINO',
    'ДАКАР': 'DAKAR',
    'МОГАДИШО': 'MOGADISHU',
    'ПАРАМАРИБО': 'PARAMARIBO',
    'ДЖУБА': 'JUBA',
    'САН-ТОМЕ': 'SAO TOME',
    'САН-САЛЬВАДОР': 'SAN SALVADOR',
    'ФИЛИПСБУРГ': 'PHILIPSBURG',
    'ДАМАСК': 'DAMASCUS',
    'МБАБАНЕ': 'MBABANE',
    'КОБЕРН-ТАУН': 'COCKBURN TOWN',
    'НДЖАМЕНА': 'NDJAMENA',
    'ПОРТ-ОФ-СПЕЙН': 'PORT OF SPAIN',
    'ЛОМЕ': 'LOME',
    'БАНГКОК': 'BANGKOK',
    'ДУШАНБЕ': 'DUSHANBE',
    'НУКУАЛОФА': 'NUKUALOFA',
    'ДИЛИ': 'DILI',
    'АШХАБАД': 'ASHGABAT',
    'ТУНИС': 'TUNIS',
    'АНКАРА': 'ANKARA',
    'ФУНАФУТИ': 'FUNAFUTI',
    'ТАЙБЭЙ': 'TAIPEI',
    'ДОДОМА': 'DODOMA',
    'КИЕВ': 'KYIV',
    'КАМПАЛА': 'KAMPALA',
    'АТОЛЛ': 'WAKE ISLAND',
    'ВАШИНГТОН': 'WASHINGTON',
    'МОНТЕВИДЕО': 'MONTEVIDEO',
    'ТАШКЕНТ': 'TASHKENT',
    'ВАТИКАН': 'VATICAN CITY',
    'КИНГСТАУН': 'KINGSTOWN',
    'КАРАКАС': 'CARACAS',
    'РОУД-ТАУН': 'ROAD TOWN',
    'ШАРЛОТТА-АМАЛИЯ': 'CHARLOTTE AMALIE',
    'ХАНОЙ': 'HANOI',
    'ПОРТ-ВИЛА': 'PORT VILA',
    'МАТА-УТУ': 'MATA UTU',
    'АПИА': 'APIA',
    'ПРИШТИНА': 'PRISTINA',
    'САНА': 'SANAA',
    'МАЙОТТА': 'MAMOUDZOU',
    'КЕЙПТАУН': 'CAPE TOWN',
    'ЛУСАКА': 'LUSAKA',
    'ХАРАРЕ': 'HARARE'
};

// Функция для создания полного файла столиц на английском
function createEnglishCapitals() {
    const russianCapitals = `1 - АНДОРРА-ЛА-ВЕЛЬЯ - AD
2 - АБУ-ДАБИ - AE
3 - КАБУЛ - AF
4 - СЕНТ-ДЖОНС - AG
5 - ОСТРОВ АНГИЛЬЯ - AI
6 - ТИРАНА - AL
7 - ЕРЕВАН - AM
8 - ЛУАНДА - AO
9 - БУЭНОС-АЙРЕС - AR
10 - СТАНЦИЯ МАК-МЕРДО - AQ
11 - ПАГО-ПАГО - AS
12 - ВЕНА - AT
13 - КАНБЕРРА - AU
14 - ОРАНЬЕСТАД - AW
15 - МАРИЕХАМН - AX
16 - БАКУ - AZ
17 - САРАЕВО - BA
18 - БРИДЖТАУН - BB
19 - ДАККА - BD
20 - БРЮССЕЛЬ - BE
21 - УАГАДУГУ - BF
22 - СОФИЯ - BG
23 - МАНАМА - BH
24 - ГИТЕГА - BI
25 - ПОРТО-НОВО - BJ
26 - ГУСТАВИЯ - BL
27 - ГАМИЛЬТОН - BM
28 - БАНДАР-СЕРИ-БЕГАВАН - BN
29 - СУКРЕ - BO
30 - КРАЛЕНДЕЙК - BQ
31 - БРАЗИЛИА - BR
32 - НАССАУ - BS
33 - ТХИМПХУ - BT
34 - БУВЕ - BV
35 - ГАБОРОНЕ - BW
36 - МИНСК - BY
37 - БЕЛЬМОПАН - BZ
38 - ОТТАВА - CA
39 - УЭСТ-АЙЛЕНД - CC
40 - КИНШАСА - CD
41 - БАНГИ - CF
42 - БРАЗЗАВИЛЬ - CG
43 - БЕРН - CH
44 - ЯМУСУКРО - CI
45 - АВАРАМАНГА - CK
46 - САНТЬЯГО - CL
47 - ЯУНДЕ - CM
48 - ПЕКИН - CN
49 - БОГОТА - CO
50 - САН-ХОСЕ - CR`;

    const lines = russianCapitals.split('\n');
    const englishLines = lines.map(line => {
        const parts = line.split(' - ');
        const number = parts[0];
        const russianName = parts[1];
        const code = parts[2];
        const englishName = capitalTranslations[russianName] || russianName;
        return `${number} - ${englishName} - ${code}`;
    });

    return englishLines.join('\n');
}

console.log('Скрипт для создания переводов загружен');
console.log('Используйте createEnglishCapitals() для создания английских столиц'); 