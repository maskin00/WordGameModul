# 🔄 РУКОВОДСТВО ПО РАБОТЕ С GIT

## 📋 **ОСНОВНЫЕ ПРИНЦИПЫ**

### **Структура веток:**
```
main (production)     ← Стабильная версия
├── develop           ← Основная ветка разработки  
├── feature/category  ← Новые категории
├── feature/ui        ← Изменения интерфейса
├── hotfix/dinosaurs  ← Критические исправления
└── docs/guides       ← Документация
```

### **Соглашения по именованию:**
```bash
# Новые функции
feature/add-sports-category
feature/keyboard-layouts
feature/mobile-ui

# Исправления багов  
bugfix/image-loading
bugfix/translation-missing
hotfix/critical-game-crash

# Документация
docs/setup-guide
docs/api-reference

# Рефакторинг
refactor/datamanager-cleanup
refactor/css-optimization
```

## 🚀 **РАБОЧИЙ ПРОЦЕСС**

### **Начало работы над задачей:**
```bash
# 1. Обновить main ветку
git checkout main
git pull origin main

# 2. Создать новую ветку
git checkout -b feature/your-task-name

# 3. Убедиться что работаете в правильной ветке
git branch --show-current
```

### **Во время работы:**
```bash
# Частые коммиты с понятными сообщениями
git add .
git commit -m "feat: добавлена категория животных"

# Периодически синхронизироваться с main
git fetch origin
git rebase origin/main
```

### **Завершение задачи:**
```bash
# 1. Финальный коммит
git add .
git commit -m "feat: завершена категория животных с тестами"

# 2. Обновить ветку
git rebase origin/main

# 3. Отправить на сервер
git push origin feature/your-task-name

# 4. Создать Pull Request
```

## 📝 **СОГЛАШЕНИЯ ПО КОММИТАМ**

### **Формат сообщения:**
```
<тип>(<область>): <описание>

<детальное описание (опционально)>

<ссылки на задачи (опционально)>
```

### **Типы коммитов:**
```bash
feat:     # Новая функциональность
fix:      # Исправление бага
docs:     # Изменения в документации
style:    # Форматирование, отступы (не влияет на код)
refactor: # Рефакторинг кода
test:     # Добавление тестов
chore:    # Обновление зависимостей, конфигурации
```

### **Примеры хороших коммитов:**
```bash
feat(categories): добавлена категория динозавров с переводами
fix(images): исправлена загрузка изображений для новых категорий  
docs(setup): обновлено руководство по установке
refactor(datamanager): упрощена логика загрузки изображений
test(categories): добавлены тесты для всех категорий
```

## 🔍 **ПРОВЕРКА ПЕРЕД КОММИТОМ**

### **Чек-лист:**
- [ ] Код работает локально
- [ ] Все файлы добавлены в коммит
- [ ] Сообщение коммита понятное
- [ ] Нет временных/отладочных файлов
- [ ] Обновлена документация (если нужно)

### **Команды для проверки:**
```bash
# Статус репозитория
git status

# Что будет закоммичено
git diff --cached

# История коммитов
git log --oneline -10

# Проверка на конфликты
git rebase --dry-run origin/main
```

## 🚨 **РАБОТА С КОНФЛИКТАМИ**

### **При возникновении конфликта:**
```bash
# 1. Посмотреть конфликтующие файлы
git status

# 2. Открыть файл и разрешить конфликт
# Найти маркеры: <<<<<<< ======= >>>>>>>
# Выбрать нужный код, удалить маркеры

# 3. Добавить разрешенный файл
git add conflicted-file.js

# 4. Продолжить rebase
git rebase --continue
```

### **Типичные конфликты в проекте:**
```javascript
// DataManager.js - добавление новых категорий
<<<<<<< HEAD
else if (categoryId === 'animals') {
=======
else if (categoryId === 'animals' || categoryId === 'dinosaurs') {
>>>>>>> feature/dinosaurs

// Решение: объединить условия
else if (categoryId === 'animals' || categoryId === 'dinosaurs') {
```

## 📦 **УПРАВЛЕНИЕ РЕЛИЗАМИ**

### **Подготовка к релизу:**
```bash
# 1. Создать ветку релиза
git checkout -b release/v1.2.0

# 2. Обновить версию в файлах
# - package.json (если есть)
# - README.md
# - CHANGELOG.md

# 3. Финальное тестирование
python -m http.server 8000
# Проверить все функции

# 4. Коммит релиза
git commit -m "chore: подготовка релиза v1.2.0"
```

### **Создание тега:**
```bash
# Создать аннотированный тег
git tag -a v1.2.0 -m "Релиз v1.2.0: добавлены динозавры и исправления"

# Отправить тег на сервер
git push origin v1.2.0

# Посмотреть все теги
git tag -l
```

## 🔧 **ПОЛЕЗНЫЕ КОМАНДЫ**

### **Навигация по истории:**
```bash
# Красивый лог
git log --oneline --graph --decorate --all

# Изменения в файле
git log -p filename.js

# Кто изменял строки
git blame filename.js

# Поиск в коммитах
git log --grep="dinosaur"
```

### **Отмена изменений:**
```bash
# Отменить последний коммит (сохранить изменения)
git reset --soft HEAD~1

# Отменить изменения в файле
git checkout -- filename.js

# Отменить все локальные изменения
git reset --hard HEAD
```

### **Работа с удаленным репозиторием:**
```bash
# Добавить удаленный репозиторий
git remote add origin https://github.com/user/repo.git

# Посмотреть удаленные репозитории
git remote -v

# Синхронизация с удаленным репозиторием
git fetch origin
git pull origin main
```

## 📁 **ФАЙЛЫ ДЛЯ ИГНОРИРОВАНИЯ**

### **Создать .gitignore:**
```bash
# Временные файлы
*.tmp
*.temp
*~

# Логи
*.log
logs/

# Кэш браузера
.cache/

# Системные файлы
.DS_Store
Thumbs.db

# Редакторы
.vscode/
.idea/
*.swp

# Локальные настройки
config.local.js
.env.local

# Тестовые файлы (если не нужны в репозитории)
test_*.html
debug_*.py
```

## 🎯 **ЛУЧШИЕ ПРАКТИКИ**

### **DO (Делайте):**
- ✅ Частые коммиты с понятными сообщениями
- ✅ Тестируйте перед каждым коммитом
- ✅ Используйте осмысленные имена веток
- ✅ Синхронизируйтесь с main регулярно
- ✅ Документируйте крупные изменения

### **DON'T (Не делайте):**
- ❌ Коммиты с сообщением "fix" или "update"
- ❌ Коммиты сломанного кода
- ❌ Работа в main ветке напрямую
- ❌ Коммиты временных/отладочных файлов
- ❌ Принудительный push (git push --force)

## 🚀 **АВТОМАТИЗАЦИЯ**

### **Git хуки (hooks):**
```bash
# pre-commit: проверка перед коммитом
#!/bin/sh
echo "Проверка синтаксиса JavaScript..."
for file in $(git diff --cached --name-only | grep '\.js$'); do
    node -c "$file"
    if [ $? -ne 0 ]; then
        echo "Ошибка синтаксиса в $file"
        exit 1
    fi
done
```

### **Алиасы для удобства:**
```bash
# Добавить в ~/.gitconfig
[alias]
    st = status
    co = checkout
    br = branch
    ci = commit
    lg = log --oneline --graph --decorate --all
    unstage = reset HEAD --
```

---

*Последнее обновление: 15.06.2025*  
*Версия: 1.0* 