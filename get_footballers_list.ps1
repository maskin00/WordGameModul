# PowerShell скрипт для получения списка всех файлов футболистов
# Запустите из корневой папки проекта

Write-Host "🔍 Сканирование папки футболистов..." -ForegroundColor Green

$footballersPath = "data\images\footballers"

if (Test-Path $footballersPath) {
    Write-Host "📁 Найдена папка: $footballersPath" -ForegroundColor Yellow
    
    $files = Get-ChildItem -Path $footballersPath -Filter "*.png" | Sort-Object Name
    $totalFiles = $files.Count
    
    Write-Host "📊 Найдено файлов: $totalFiles" -ForegroundColor Cyan
    Write-Host ""
    
    # Создаем JavaScript массив с именами файлов
    $jsArray = "const allFootballerFiles = [`n"
    
    for ($i = 0; $i -lt $files.Count; $i++) {
        $filename = $files[$i].Name
        $jsArray += "    '$filename'"
        
        if ($i -lt $files.Count - 1) {
            $jsArray += ","
        }
        $jsArray += "`n"
        
        # Показываем прогресс каждые 100 файлов
        if (($i + 1) % 100 -eq 0) {
            Write-Host "  📋 Обработано: $($i + 1)/$totalFiles" -ForegroundColor Gray
        }
    }
    
    $jsArray += "];"
    
    # Записываем в файл
    $outputFile = "footballers_files_list.js"
    $jsArray | Out-File -FilePath $outputFile -Encoding UTF8
    
    Write-Host ""
    Write-Host "✅ Список сохранен в файл: $outputFile" -ForegroundColor Green
    Write-Host "📊 Всего файлов: $totalFiles" -ForegroundColor Green
    
    # Показываем первые 10 файлов для проверки
    Write-Host ""
    Write-Host "🔍 Первые 10 файлов:" -ForegroundColor Yellow
    for ($i = 0; $i -lt [Math]::Min(10, $files.Count); $i++) {
        Write-Host "  $($i + 1). $($files[$i].Name)" -ForegroundColor White
    }
    
    if ($files.Count -gt 10) {
        Write-Host "  ... и ещё $($files.Count - 10) файлов" -ForegroundColor Gray
    }
    
    Write-Host ""
    Write-Host "💡 Теперь вы можете использовать этот файл в генераторе данных!" -ForegroundColor Magenta
    
} else {
    Write-Host "❌ Папка не найдена: $footballersPath" -ForegroundColor Red
    Write-Host "💡 Убедитесь, что запускаете скрипт из корневой папки проекта" -ForegroundColor Yellow
} 