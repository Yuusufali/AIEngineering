# Установка зависимостей при работе через прокси
# Замените user, password, proxy-host и port на свои значения.
# Запуск: .\install_with_proxy.ps1

# Пример: $env:HTTPS_PROXY = "http://user:password@proxy.company.com:8080"
# Раскомментируйте и отредактируйте следующую строку:
# $env:HTTPS_PROXY = "http://ВАШ_ЛОГИН:ВАШ_ПАРОЛЬ@адрес_прокси:порт"
# $env:HTTP_PROXY = $env:HTTPS_PROXY

# Установка без кэша (иногда помогает при прокси)
py -m pip install --proxy $env:HTTPS_PROXY -r requirements.txt

# Если прокси не требует авторизации:
# py -m pip install --proxy http://proxy.company.com:8080 -r requirements.txt
