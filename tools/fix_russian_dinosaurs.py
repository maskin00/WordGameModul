#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

def create_russian_dinosaur_translations():
    """Create proper Russian translations for dinosaurs"""
    
    # Русские переводы названий динозавров
    russian_translations = {
        "aegyptosaurus": "ЕГИПТОЗАВР",
        "agnosphitys": "АГНОСФИТИС", 
        "agrosaurus": "АГРОЗАВР",
        "alaskacephale": "АЛЯСКАЦЕФАЛ",
        "albalophosaurus": "АЛЬБАЛОФОЗАВР",
        "alexeyisaurus": "АЛЕКСЕЙЗАВР",
        "alioramus": "АЛИОРАМ",
        "alwalkeria": "АЛВАЛКЕРИЯ",
        "amtocephale": "АМТОЦЕФАЛ",
        "angaturama": "АНГАТУРАМА",
        "anhanguera": "АНХАНГЕРА",
        "antarctopelta": "АНТАРКТОПЕЛЬТА",
        "astrodon": "АСТРОДОН",
        "augustasaurus": "АВГУСТАЗАВР",
        "aurornis": "АУРОРНИС",
        "barilium": "БАРИЛИУМ",
        "beipiaosaurus": "БЕЙПЯОЗАВР",
        "bishanopliosaurus": "БИШАНОПЛИОЗАВР",
        "camelotia": "КАМЕЛОТИЯ",
        "campylognathoides": "КАМПИЛОГНАТОИДЕС",
        "carcharodontosaurus": "КАРХАРОДОНТОЗАВР",
        "centrosaurus": "ЦЕНТРОЗАВР",
        "cetiosaurus": "ЦЕТИОЗАВР",
        "chebsaurus": "ЧЕБЗАВР",
        "chindesaurus": "ЧИНДЕЗАВР",
        "chirostenotes": "ХИРОСТЕНОТЕС",
        "clasmodosaurus": "КЛАСМОДОЗАВР",
        "colepiocephale": "КОЛЕПИОЦЕФАЛ",
        "coloradisaurus": "КОЛОРАДИЗАВР",
        "daanosaurus": "ДАНОЗАВР",
        "deinonychus": "ДЕЙНОНИХ",
        "diabloceratops": "ДИАБЛОЦЕРАТОПС",
        "dorygnathus": "ДОРИГНАТ",
        "dracopelta": "ДРАКОПЕЛЬТА",
        "duriatitan": "ДУРИАТИТАН",
        "duriavenator": "ДУРИАВЕНАТОР",
        "edmarka": "ЭДМАРКА",
        "edmontonia": "ЭДМОНТОНИЯ",
        "einiosaurus": "ЭЙНИОЗАВР",
        "eotyrannus": "ЭОТИРАНН",
        "eudimorphodon": "ЭУДИМОРФОДОН",
        "eugongbusaurus": "ЭУГОНГБУЗАВР",
        "euhelopus": "ЭУХЕЛОПУС",
        "eustreptospondylus": "ЭУСТРЕПТОСПОНДИЛ",
        "falcarius": "ФАЛЬКАРИУС",
        "fusuisaurus": "ФУСУИЗАВР",
        "futalognkosaurus": "ФУТАЛОГНКОЗАВР",
        "gargoyleosaurus": "ГАРГОЙЛЕОЗАВР",
        "gnathosaurus": "ГНАТОЗАВР",
        "gojirasaurus": "ГОДЗИЛЛАЗАВР",
        "guanlong": "ГУАНЛОНГ",
        "herrerasaurus": "ХЕРРЕРАЗАВР",
        "iliosuchus": "ИЛИОЗУХ",
        "isanosaurus": "ИЗАНОЗАВР",
        "isisaurus": "ИЗИЗАВР",
        "istegosaurusi skeleton in the earth hall": "СКЕЛЕТ СТЕГОЗАВРА В ЗАЛЕ ЗЕМЛИ",
        "kaatedocus": "КААТЕДОКУС",
        "kileskus": "КИЛЕСК",
        "kunbarrasaurus": "КУНБАРРАЗАВР",
        "kunpengopterus": "КУНПЕНГОПТЕР",
        "labocania": "ЛАБОКАНИЯ",
        "lambeosaurus": "ЛАМБЕОЗАВР",
        "laquintasaura": "ЛАКИНТАЗАВРА",
        "malarguesaurus": "МАЛАРГЕЗАВР",
        "maleevus": "МАЛЕЕВ",
        "mamenchisaurus": "МАМЕНЧИЗАВР",
        "medusaceratops": "МЕДУЗАЦЕРАТОПС",
        "megapnosaurus": "МЕГАПНОЗАВР",
        "melanorosaurus": "МЕЛАНОРОЗАВР",
        "mercuriceratops": "МЕРКУРИЦЕРАТОПС",
        "metriacanthosaurus": "МЕТРИАКАНТОЗАВР",
        "mojoceratops": "МОДЖОЦЕРАТОПС",
        "mongolosaurus": "МОНГОЛОЗАВР",
        "mononykus": "МОНОНИХ",
        "mussaurus": "МУССАВР",
        "mythunga": "МИТУНГА",
        "nanosaurus": "НАНОЗАВР",
        "nasutoceratops": "НАЗУТОЦЕРАТОПС",
        "newtonsaurus": "НЬЮТОНЗАВР",
        "nyasasaurus": "НЬЯСАЗАВР",
        "ohmdenosaurus": "ОМДЕНОЗАВР",
        "ornithomimus": "ОРНИТОМИМ",
        "ostafrikasaurus": "ОСТАФРИКАЗАВР",
        "pachysuchus": "ПАХИЗУХ",
        "pampadromaeus": "ПАМПАДРОМЕЙ",
        "parvicursor": "ПАРВИКУРСОР",
        "pentaceratops": "ПЕНТАЦЕРАТОПС",
        "pisanosaurus": "ПИЗАНОЗАВР",
        "pradhania": "ПРАДХАНИЯ",
        "preondactylus": "ПРЕОНДАКТИЛЬ",
        "procompsognathus": "ПРОКОМПСОГНАТ",
        "pycnonemosaurus": "ПИКНОНЕМОЗАВР",
        "qantassaurus": "КВАНТАЗАВР",
        "rubeosaurus": "РУБЕОЗАВР",
        "saltriovenator": "САЛТРИОВЕНАТОР",
        "sanpasaurus": "САНПАЗАВР",
        "saturnalia": "САТУРНАЛИЯ",
        "sciurumimus": "СЦИУРУМИМ",
        "seeleyosaurus": "СИЛЕОЗАВР",
        "shanyangosaurus": "ШАНЬЯНГОЗАВР",
        "shunosaurus": "ШУНОЗАВР",
        "siamotyrannus": "СИАМОТИРАНН",
        "spinophorosaurus": "СПИНОФОРОЗАВР",
        "stokesosaurus": "СТОКЕЗАВР",
        "sugiyamasaurus": "СУГИЯМАЗАВР",
        "tehuelchesaurus": "ТЕУЭЛЬЧЕЗАВР",
        "thalassodromeus": "ТАЛАССОДРОМЕЙ",
        "thecodontosaurus": "ТЕКОДОНТОЗАВР",
        "titanoceratops": "ТИТАНОЦЕРАТОПС",
        "tochisaurus": "ТОЧИЗАВР",
        "tonouchisaurus": "ТОНОЧИЗАВР",
        "trinisaura": "ТРИНИЗАВРА",
        "unenlagia": "УНЕНЛАГИЯ",
        "vouivria": "ВУИВРИЯ",
        "wannanosaurus": "ВАННАНОЗАВР",
        "wellnhoferia": "ВЕЛЛЬНХОФЕРИЯ",
        "westphaliasaurus": "ВЕСТФАЛИАЗАВР",
        "yixianosaurus": "ИКСИАНОЗАВР",
        "yueosaurus": "ЮЕОЗАВР",
        "yunnanosaurus": "ЮННАНОЗАВР",
        "zapsalis": "ЗАПСАЛИС",
        "zhongornis": "ЧЖОНГОРНИС"
    }
    
    print("🦕 ИСПРАВЛЕНИЕ РУССКИХ ПЕРЕВОДОВ ДИНОЗАВРОВ")
    print("=" * 50)
    
    # Читаем существующий файл
    with open('data/words/ru/dinosaurs_COMPLETE.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    print(f"📝 Найдено {len(lines)} записей в файле")
    
    # Создаем новый файл с правильными переводами
    new_lines = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        parts = line.split(' - ')
        if len(parts) >= 3:
            number = parts[0]
            english_name = parts[1]
            image_file = parts[2]
            
            # Извлекаем ключ для перевода из имени файла
            key = image_file.replace('.jpg', '').split('-', 1)[1] if '-' in image_file else english_name.lower()
            
            # Получаем русский перевод
            russian_name = russian_translations.get(key, english_name)
            
            new_line = f"{number} - {russian_name} - {image_file}"
            new_lines.append(new_line)
            
            if russian_name != english_name:
                print(f"   ✅ {english_name} → {russian_name}")
    
    # Записываем новый файл
    with open('data/words/ru/dinosaurs_COMPLETE.txt', 'w', encoding='utf-8') as f:
        for line in new_lines:
            f.write(line + '\n')
    
    print(f"\n✅ РУССКИЕ ПЕРЕВОДЫ ОБНОВЛЕНЫ!")
    print(f"   📁 Обработано записей: {len(new_lines)}")

if __name__ == "__main__":
    create_russian_dinosaur_translations() 