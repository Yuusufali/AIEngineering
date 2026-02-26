# Установка Python через winget (Windows Package Manager)
# Запуск: правый клик -> "Выполнить с PowerShell" или в терминале: .\install_python.ps1

$ErrorActionPreference = "Stop"

Write-Host "Проверка winget..." -ForegroundColor Cyan
if (!(Get-Command winget -ErrorAction SilentlyContinue)) {
    Write-Host "winget не найден. Установите App Installer из Microsoft Store или обновите Windows." -ForegroundColor Red
    Write-Host "Альтернатива: скачайте Python с https://www.python.org/downloads/" -ForegroundColor Yellow
    exit 1
}

Write-Host "Установка Python 3.12..." -ForegroundColor Cyan
winget install Python.Python.3.12 --accept-package-agreements --accept-source-agreements

if ($LASTEXITCODE -eq 0) {
    Write-Host "`nГотово. Закройте и снова откройте терминал, затем проверьте: python --version" -ForegroundColor Green
} else {
    Write-Host "`nЕсли установка не удалась, попробуйте другую версию:" -ForegroundColor Yellow
    Write-Host "  winget install Python.Python.3.11" -ForegroundColor Gray
    Write-Host "Или скачайте установщик с https://www.python.org/downloads/" -ForegroundColor Gray
}
