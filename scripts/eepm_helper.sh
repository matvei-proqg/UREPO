#!/bin/bash

# Установка пакета из EEPM
eepm_install() {
    package=$1
    epm install "$package"
}

# Поиск в EEPM
eepm_search() {
    query=$1
    epm search "$query"
}

# Обновление репозиториев EEPM
eepm_update() {
    epm update
}
