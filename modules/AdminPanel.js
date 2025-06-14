// modules/AdminPanel.js
class AdminPanel {
    constructor(dataManager, languageManager, categoryManager) {
        this.dataManager = dataManager;
        this.languageManager = languageManager;
        this.categoryManager = categoryManager;
        
        this.validationData = null;
        this.uploadedFiles = {
            words: null,
            images: []
        };
    }

    async initialize() {
        try {
            this.setupEventListeners();
            this.setupLanguageSelector();
            console.log('AdminPanel инициализирован');
            return true;
        } catch (error) {
            console.error('Ошибка инициализации AdminPanel:', error);
            return false;
        }
    }

    setupEventListeners() {
        // Кнопка валидации
        document.getElementById('validateButton').addEventListener('click', () => {
            this.validateCategory();
        });

        // Кнопка сохранения
        document.getElementById('saveButton').addEventListener('click', () => {
            this.saveCategory();
        });

        // Обработчики файлов
        document.getElementById('wordsFile').addEventListener('change', (e) => {
            this.handleWordsFile(e.target.files[0]);
        });

        document.getElementById('imagesFiles').addEventListener('change', (e) => {
            this.handleImagesFiles(Array.from(e.target.files));
        });
    }

    setupLanguageSelector() {
        const select = document.getElementById('categoryLanguage');
        select.innerHTML = '';
        
        this.languageManager.getAvailableLanguages().forEach(lang => {
            const option = document.createElement('option');
            option.value = lang.code;
            option.textContent = lang.name;
            select.appendChild(option);
        });
    }

    async handleWordsFile(file) {
        if (!file) return;
        
        try {
            const content = await this.readFileAsText(file);
            this.uploadedFiles.words = {
                file: file,
                content: content
            };
            
            console.log('Файл со словами загружен');
        } catch (error) {
            console.error('Ошибка чтения файла со словами:', error);
            alert('Ошибка чтения файла со словами');
        }
    }

    handleImagesFiles(files) {
        this.uploadedFiles.images = files;
        console.log(`Загружено ${files.length} изображений`);
    }

    async validateCategory() {
        if (!this.uploadedFiles.words) {
            alert(this.languageManager.getText('uploadWords') || 'Загрузите файл со словами');
            return;
        }

        if (this.uploadedFiles.images.length === 0) {
            alert(this.languageManager.getText('uploadImages') || 'Загрузите изображения');
            return;
        }

        try {
            // Валидация файла со словами
            const wordsValidation = this.dataManager.validateWordsFile(this.uploadedFiles.words.content);
            
            // Валидация изображений
            const imagesValidation = await this.dataManager.validateImages(
                this.uploadedFiles.images, 
                wordsValidation.words
            );

            this.validationData = {
                words: wordsValidation,
                images: imagesValidation,
                isValid: wordsValidation.isValid && imagesValidation.matchedPairs.length > 0
            };

            this.showValidationResult();
            
            // Включение кнопки сохранения
            document.getElementById('saveButton').disabled = !this.validationData.isValid;
            
        } catch (error) {
            console.error('Ошибка валидации:', error);
            alert('Ошибка при валидации данных');
        }
    }

    showValidationResult() {
        const resultDiv = document.getElementById('validationResult');
        const detailsDiv = document.getElementById('validationDetails');
        
        if (!this.validationData) {
            resultDiv.style.display = 'none';
            return;
        }

        resultDiv.style.display = 'block';
        
        const { words, images } = this.validationData;
        
        let html = `
            <div class="validation-summary ${this.validationData.isValid ? 'success' : 'error'}">
                <h4>${this.validationData.isValid ? 
                    this.languageManager.getText('success') || 'Успешно' : 
                    this.languageManager.getText('failed') || 'Ошибка'}</h4>
            </div>
            
            <div class="validation-details">
                <div class="words-validation">
                    <h5>Файл со словами:</h5>
                    <p>${this.languageManager.getText('wordsFound') || 'Найдено слов'}: ${words.wordCount}</p>
                    ${words.errors.length > 0 ? 
                        `<div class="errors"><strong>Ошибки:</strong><ul>${words.errors.map(err => `<li>${err}</li>`).join('')}</ul></div>` : 
                        ''}
                </div>
                
                <div class="images-validation">
                    <h5>Изображения:</h5>
                    <p>${this.languageManager.getText('imagesFound') || 'Найдено изображений'}: ${images.validImages.length}</p>
                    <p>${this.languageManager.getText('matchedPairs') || 'Совпадающих пар'}: ${images.matchedPairs.length}</p>
                    
                    ${images.unmatchedWords.length > 0 ? 
                        `<div class="unmatched-words">
                            <strong>Слова без изображений:</strong>
                            <ul>${images.unmatchedWords.map(word => `<li>${word.id} - ${word.word}</li>`).join('')}</ul>
                        </div>` : ''}
                    
                    ${images.unmatchedImages.length > 0 ? 
                        `<div class="unmatched-images">
                            <strong>Изображения без слов:</strong>
                            <ul>${images.unmatchedImages.map(img => `<li>${img.file}</li>`).join('')}</ul>
                        </div>` : ''}
                </div>
            </div>
        `;
        
        detailsDiv.innerHTML = html;
    }

    async saveCategory() {
        if (!this.validationData || !this.validationData.isValid) {
            alert('Сначала выполните валидацию');
            return;
        }

        const categoryName = document.getElementById('newCategoryName').value.trim();
        if (!categoryName) {
            alert(this.languageManager.getText('categoryName') || 'Введите название категории');
            return;
        }

        const languageCode = document.getElementById('categoryLanguage').value;

        try {
            // Создание категории в новом формате
            const categoryId = this.generateCategoryId(categoryName);
            const categoryData = {
                id: categoryId,
                name: categoryName,
                icon: '📁',
                language: languageCode,
                wordsFile: this.uploadedFiles.words.content,
                imageFiles: this.uploadedFiles.images
            };

            const result = await this.dataManager.addCategory(categoryData);
            const success = result && result.success;
            
            if (success) {
                alert(this.languageManager.getText('success') || 'Категория успешно добавлена!');
                this.resetForm();
                
                // Обновление списка категорий
                await this.dataManager.initialize();
                
                // Уведомление categoryManager об изменениях
                if (this.categoryManager.onCategoriesUpdated) {
                    this.categoryManager.onCategoriesUpdated();
                }
            } else {
                alert(this.languageManager.getText('failed') || 'Ошибка при сохранении категории');
            }
            
        } catch (error) {
            console.error('Ошибка сохранения категории:', error);
            alert('Ошибка при сохранении категории');
        }
    }

    generateCategoryId(name) {
        // Создание ID на основе названия
        return name.toLowerCase()
                  .replace(/\s+/g, '_')
                  .replace(/[^a-z0-9_]/g, '')
                  .substring(0, 20);
    }

    resetForm() {
        document.getElementById('newCategoryName').value = '';
        document.getElementById('wordsFile').value = '';
        document.getElementById('imagesFiles').value = '';
        document.getElementById('saveButton').disabled = true;
        document.getElementById('validationResult').style.display = 'none';
        
        this.validationData = null;
        this.uploadedFiles = {
            words: null,
            images: []
        };
    }

    readFileAsText(file) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onload = (e) => resolve(e.target.result);
            reader.onerror = (e) => reject(e);
            reader.readAsText(file, 'UTF-8');
        });
    }

    // Показать/скрыть панель администратора
    show() {
        document.getElementById('adminPanel').style.display = 'block';
        this.setupLanguageSelector(); // Обновляем селектор языков
    }

    hide() {
        document.getElementById('adminPanel').style.display = 'none';
        this.resetForm();
    }
} 