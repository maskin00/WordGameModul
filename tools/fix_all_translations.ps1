# PowerShell скрипт для исправления переводов футболистов
# Заменяет русские названия на латинские транслитерации

function Transliterate-Russian {
    param([string]$text)
    
    $translitMap = @{
        'А' = 'A'; 'Б' = 'B'; 'В' = 'V'; 'Г' = 'G'; 'Д' = 'D'; 'Е' = 'E'; 'Ё' = 'YO'; 'Ж' = 'ZH'; 'З' = 'Z';
        'И' = 'I'; 'Й' = 'Y'; 'К' = 'K'; 'Л' = 'L'; 'М' = 'M'; 'Н' = 'N'; 'О' = 'O'; 'П' = 'P'; 'Р' = 'R';
        'С' = 'S'; 'Т' = 'T'; 'У' = 'U'; 'Ф' = 'F'; 'Х' = 'KH'; 'Ц' = 'TS'; 'Ч' = 'CH'; 'Ш' = 'SH'; 'Щ' = 'SHCH';
        'Ъ' = ''; 'Ы' = 'Y'; 'Ь' = ''; 'Э' = 'E'; 'Ю' = 'YU'; 'Я' = 'YA';
        ' ' = ' '; '-' = '-'
    }
    
    $result = ""
    for ($i = 0; $i -lt $text.Length; $i++) {
        $char = $text[$i]
        if ($translitMap.ContainsKey($char)) {
            $result += $translitMap[$char]
        } else {
            $result += $char
        }
    }
    
    return $result
}

function Process-File {
    param([string]$filePath, [string]$language)
    
    Write-Host "Обрабатываем файл: $filePath"
    
    if (-not (Test-Path $filePath)) {
        Write-Host "⚠ Файл не найден: $filePath" -ForegroundColor Yellow
        return
    }
    
    try {
        $lines = Get-Content $filePath -Encoding UTF8
        $processedLines = @()
        
        foreach ($line in $lines) {
            if ([string]::IsNullOrWhiteSpace($line) -or $line.StartsWith('#')) {
                $processedLines += $line
                continue
            }
            
            # Парсим строку: номер - СЛОВО - код_изображения
            $parts = $line -split ' - '
            if ($parts.Length -ge 3) {
                $number = $parts[0]
                $russianName = $parts[1]
                $imageCode = $parts[2]
                
                # Транслитерируем русское название
                $transliteratedName = Transliterate-Russian $russianName
                
                $processedLines += "$number - $transliteratedName - $imageCode"
            } else {
                $processedLines += $line
            }
        }
        
        # Записываем обработанный файл
        $processedLines | Out-File -FilePath $filePath -Encoding UTF8
        Write-Host "✓ Файл $filePath успешно обработан" -ForegroundColor Green
        
    } catch {
        Write-Host "✗ Ошибка обработки файла ${filePath}: $($_.Exception.Message)" -ForegroundColor Red
    }
}

# Основная функция
Write-Host "Начинаем исправление переводов футболистов...`n" -ForegroundColor Cyan

$languages = @('en', 'fr', 'es')
$file = 'footballers_FULL.txt'

foreach ($lang in $languages) {
    $filePath = Join-Path $PSScriptRoot "..\data\words\$lang\$file"
    Process-File -filePath $filePath -language $lang
}

Write-Host "`n✓ Исправление переводов завершено!" -ForegroundColor Green 