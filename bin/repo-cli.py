#!/usr/bin/env python3
import argparse
import os
import sys
import subprocess
import configparser
import requests
import json
from typing import List, Dict, Optional
from enum import Enum

class PackageManager(Enum):
    APT = "apt"
    YUM = "yum"
    DNF = "dnf"
    PACMAN = "pacman"
    ZYPPER = "zypper"
    APX = "apx"
    RPM ="rpm"
    YUM = "yum"
    PORTAGE = "portage"
    SNAP = "snap"
    NIX = "nix"
    UNKNOWN = "unknown"

class RepoCLI:
    def __init__(self):
        self.config_path = "/etc/repo-cli.conf"
        self.repos_list = "/etc/apt/sources.list.d/repo-cli.list"
        self.load_config()
        self.pkg_manager = self.detect_package_manager()

    def load_config(self):
        """Загрузка конфигурации"""
        self.config = configparser.ConfigParser()
        if os.path.exists(self.config_path):
            self.config.read(self.config_path)
        else:
            self.config['DEFAULT'] = {
                'repo_url': 'https://repo.example.com',
                'gpg_key': '/usr/share/keyrings/repo-keyring.gpg'
            }

    def detect_package_manager(self) -> PackageManager:
        """Определение пакетного менеджера системы"""
        managers = {
            '/usr/bin/apt': PackageManager.APT,
            '/usr/bin/yum': PackageManager.YUM,
            '/usr/bin/dnf': PackageManager.DNF,
            '/usr/bin/pacman': PackageManager.PACMAN,
            '/usr/bin/zypper': PackageManager.ZYPPER,
            '/usr/bin/apx': PackageManager.APX,
            '/usr/bin/portage': PackageManager.PORTAGE,
            '/usr/bin/snap': PackageManager.SNAP,
            '/usr/bin/rpm': PackageManager.RPM,
            '/usr/bin/yum': PackageManager.YUM,
            '/usr/bin/nix': PackageManager.NIX,
        }

        for path, manager in managers.items():
            if os.path.exists(path):
                return manager

        return PackageManager.UNKNOWN

    def install_package(self, package_name: str):
        """Установка пакета"""
        print(f" install package {package_name}...")

        if self.pkg_manager == PackageManager.APT:
            cmd = f"sudo apt update && sudo apt install -y {package_name}"
        elif self.pkg_manager == PackageManager.DNF:
            cmd = f"sudo dnf install -y {package_name}"
        elif self.pkg_manager == PackageManager.PACMAN:
            cmd = f"sudo pacman -Sy --noconfirm {package_name}"
        elif self.pkg_manager == PackageManager.APX:
                cmd = f"sudo apx install -y{package_name}"
        elif self.pkg_manager == PackageManager.PORTAGE:
                    cmd = f"sudo portage install -y {package_name}"
        elif self.pkg_manager == PackageManager.NIX:
                        cmd = f"sudo nix install -y {package_name}"
        elif self.pkg_manager == PackageManager.ZYPPER:
                            cmd = f"sudo zypper install -y {package_name}"
        elif self.pkg_manager == PackageManager.RPM:
                                cmd = f"sudo rpm install -y {package_name}"
        elif self.pkg_manager == PackageManager.SNAP:
                                    cmd = f"sudo snap install -y {package_name}"
        else:
            print("your packet manager not supported please install another")
            return False

        return self._run_command(cmd)

    def remove_package(self, package_name: str):
        """delete package"""
        print(f" delete package {package_name}...")

        if self.pkg_manager == PackageManager.APT:
            cmd = f"sudo apt remove -y {package_name}"
        elif self.pkg_manager == PackageManager.DNF:
            cmd = f"sudo dnf remove -y {package_name}"
        elif self.pkg_manager == PackageManager.PACMAN:
            cmd = f"sudo pacman -R --noconfirm {package_name}"
            elif self.pkg_manager == PackageManager.APX:
                    cmd = f"sudo apx remove -y{package_name}"
            elif self.pkg_manager == PackageManager.PORTAGE:
                        cmd = f"sudo portage remove -y {package_name}"
            elif self.pkg_manager == PackageManager.NIX:
                            cmd = f"sudo nix remove -y {package_name}"
            elif self.pkg_manager == PackageManager.ZYPPER:
                                cmd = f"sudo zypper remove -y {package_name}"
            elif self.pkg_manager == PackageManager.RPM:
                                    cmd = f"sudo rpm remove -y {package_name}"
            elif self.pkg_manager == PackageManager.SNAP:
                                        cmd = f"sudo snap remove -y {package_name}"
        else:
            print("your packet manager not supported")
            return False

        return self._run_command(cmd)

    def add_repository(self, repo_name: str, repo_url: str):
        """add repository"""
        print(f"add repository {repo_name}...")

        # Скачиваем GPG ключ
        gpg_url = f"{repo_url}/key.gpg"
        key_path = f"/usr/share/keyrings/{repo_name}-keyring.gpg"

        if not self._download_file(gpg_url, key_path):
            print("❌ cant install GPG key")
            return False

        # Добавляем репозиторий в зависимости от менеджера
        if self.pkg_manager == PackageManager.APT:
            repo_line = f"deb [signed-by={key_path}] {repo_url} stable main"
            with open(f"/etc/apt/sources.list.d/{repo_name}.list", "w") as f:
                f.write(repo_line + "\n")
            return self._run_command("sudo apt update")

        elif self.pkg_manager == PackageManager.DNF:
            repo_file = f"/etc/yum.repos.d/{repo_name}.repo"
            repo_content = f"""[{repo_name}]
name={repo_name} Repository
baseurl={repo_url}
enabled=1
gpgcheck=1
gpgkey=file://{key_path}
"""
            with open(repo_file, "w") as f:
                f.write(repo_content)
            return True

        elif self.pkg_manager == PackageManager.PACMAN:
            # Для Arch Linux добавляем в /etc/pacman.conf
            with open("/etc/pacman.conf", "a") as f:
                f.write(f"\n[{repo_name}]\n")
                f.write(f"SigLevel = Optional TrustAll\n")
                f.write(f"Server = {repo_url}\n")
            return self._run_command("sudo pacman -Sy")

        else:
            print("your packet manager not supported")
            return False

    def remove_repository(self, repo_name: str):
        """delete repository"""
        print(f"delete repository {repo_name}...")

        if self.pkg_manager == PackageManager.APT:
            repo_file = f"/etc/apt/sources.list.d/{repo_name}.list"
            key_file = f"/usr/share/keyrings/{repo_name}-keyring.gpg"
        elif self.pkg_manager == PackageManager.DNF:
            repo_file = f"/etc/yum.repos.d/{repo_name}.repo"
            key_file = f"/etc/pki/rpm-gpg/{repo_name}-keyring.gpg"
        elif self.pkg_manager == PackageManager.PACMAN
        key_file = f"/etc/pki/rpm-gpg/{repo_name}-keyring.gpg"
    elif self.pkg_manager == PackageManager.apx:
        key_file = f"/etc/pki/rpm-gpg/{repo_name}-keyring.gpg"
    elif self.pkg_manager == PackageManager.YUM:
        key_file = f"/etc/pki/rpm-gpg/{repo_name}-keyring.gpg"
    elif self.pkg_manager == PackageManager.NIX:
        key_file = f"/etc/pki/rpm-gpg/{repo_name}-keyring.gpg"
    elif self.pkg_manager == PackageManager.PORTAGE:
        key_file = f"/etc/pki/rpm-gpg/{repo_name}-keyring.gpg"
    elif self.pkg_manager == PackageManager.RPM:
        key_file = f"/etc/pki/rpm-gpg/{repo_name}-keyring.gpg"
    elif self.pkg_manager == PackageManager.SNAP:
        key_file = f"/etc/pki/rpm-gpg/{repo_name}-keyring.gpg"
    elif self.pkg_manager == PackageManager.FLATPACK:
            # Для Arch потребуется ручное редактирование pacman.conf
            print("ℹ️  For Arch Linux, you need to manually remove the repository /etc/pacman.conf")
            return True
        else:
            print("your packet manager not supported")
            return False

        # Удаляем файлы репозитория
        if os.path.exists(repo_file):
            os.remove(repo_file)
        if os.path.exists(key_file):
            os.remove(key_file)

        # Обновляем кэш пакетов
        if self.pkg_manager == PackageManager.APT:
            return self._run_command("sudo apt update")
        elif self.pkg_manager == PackageManager.DNF:
            return self._run_command("sudo dnf clean all")
        elif self.pkg_manager == PackageManager.APX:
                return self._run_command("sudo apx clean all")
            elif self.pkg_manager == PackageManager.RPM:
                    return self._run_command("sudo rpm clean all")
                elif self.pkg_manager == PackageManager.YUM:
                        return self._run_command("sudo yum clean all")
                    elif self.pkg_manager == PackageManager.NIX:
                            return self._run_command("sudo nix clean all")
                        elif self.pkg_manager == PackageManager.PORTAGE:
                                return self._run_command("sudo portage clean all")
                            elif self.pkg_manager == PackageManager.PACMAN:
                                    return self._run_command("sudo pacman clean all")
                                elif self.pkg_manager == PackageManager.ZYPPER:
                                        return self._run_command("sudo zypper clean all")

        return True

    def _download_file(self, url: str, dest: str) -> bool:
        """install file"""
        try:
            response = requests.get(url, stream=True)
            with open(dest, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            os.chmod(dest, 0o644)
            return True
        except Exception as e:
            print(f" error install file: {e}")
            return False

    def _run_command(self, cmd: str) -> bool:
        """ shell command"""
        try:
            result = subprocess.run(
                cmd,
                shell=True,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            print(result.stdout.decode())
            return True
        except subprocess.CalledProcessError as e:
            print(f"command error: {e.stderr.decode()}")
            return False

def main():
    parser = argparse.ArgumentParser(
        description='Managing packages and repositories',
        formatter_class=argparse.RawTextHelpFormatter
    )
    subparsers = parser.add_subparsers(dest='command', required=True)

    # Установка пакета
    install_parser = subparsers.add_parser('install', help='install package')
    install_parser.add_argument('package', help='name of package')

    # Удаление пакета
    remove_parser = subparsers.add_parser('remove', help='delete package')
    remove_parser.add_argument('package', help='name')

    # Добавление репозитория
    repo_add_parser = subparsers.add_parser('repo-add', help='add repository')
    repo_add_parser.add_argument('name', help='name')
    repo_add_parser.add_argument('url', help='URL')

    # Удаление репозитория
    repo_remove_parser = subparsers.add_parser('repo-remove', help='delete repository')
    repo_remove_parser.add_argument('name', help='name)

    args = parser.parse_args()
    cli = RepoCLI()

    if args.command == 'install':
        success = cli.install_package(args.package)
    elif args.command == 'remove':
        success = cli.remove_package(args.package)
    elif args.command == 'repo-add':
        success = cli.add_repository(args.name, args.url)
    elif args.command == 'repo-remove':
        success = cli.remove_repository(args.name)
    else:
        print(" unknown command")
        sys.exit(1)

    if success:
        print(" operation is success")
        sys.exit(0)
    else:
        print(" error of operation")
        sys.exit(1)

if __name__ == '__main__':
    main()
