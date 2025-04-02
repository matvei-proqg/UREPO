#!/bin/bash

# Проверка наличия Flatpak
check_flatpak() {
    if ! command -v flatpak &> /dev/null; then
        echo "Flatpak is not installed. Installing..."
        sudo apt install flatpak || sudo dnf install flatpak || sudo pacman -S flatpak
        flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo
    fi
}

# Установка приложения из Flatpak
flatpak_install() {
    app_id=$1
    flatpak install -y flathub "$app_id"
}
