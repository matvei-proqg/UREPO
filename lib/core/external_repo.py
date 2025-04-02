import json
import subprocess
from pathlib import Path
from typing import Dict, List, Optional
from .package import Package
from .compatibility import check_compatibility

class ExternalRepoManager:
    def __init__(self, config_path: str = "config/repositories.json"):
        self.config = self._load_config(config_path)
        self.supported_types = ["flatpak", "rpm", "deb", "aur"]

    def _load_config(self, path: str) -> Dict:
        with open(path) as f:
            return json.load(f)

    def enable_repo(self, repo_name: str) -> bool:
        """Активировать внешний репозиторий"""
        if repo_name not in self.config["external_repositories"]:
            return False

        if not check_compatibility(self.config["external_repositories"][repo_name]):
            print(f"Repository {repo_name} is not compatible with your system")
            return False

        self.config["external_repositories"][repo_name]["enabled"] = True

        # Специфичная для типа репозитория настройка
        repo = self.config["external_repositories"][repo_name]
        if repo["type"] == "flatpak":
            return self._setup_flatpak(repo["url"])
        elif repo["type"] == "aur":
            return self._check_aur_dependencies()

        return True

    def _setup_flatpak(self, repo_url: str) -> bool:
        """Настройка Flatpak репозитория"""
        try:
            subprocess.run(["flatpak", "remote-add", "--if-not-exists", "flathub", repo_url], check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"Failed to add Flatpak repo: {e}")
            return False

    def _check_aur_dependencies(self) -> bool:
        """Проверка зависимостей для AUR"""
        try:
            subprocess.run(["which", "makepkg"], check=True)
            return True
        except subprocess.CalledProcessError:
            print("AUR support requires 'makepkg' (part of pacman)")
            return False

    def search_in_external(self, query: str) -> List[Package]:
        """Поиск пакета во всех внешних репозиториях"""
        results = []
        for repo_name, repo_data in self.config["external_repositories"].items():
            if not repo_data["enabled"]:
                continue

            if repo_data["type"] == "flatpak":
                results.extend(self._search_flatpak(query, repo_name))
            elif repo_data["type"] == "aur":
                results.extend(self._search_aur(query, repo_name))

        return results

    def _search_flatpak(self, query: str, repo_name: str) -> List[Package]:
        """Поиск в Flatpak"""
        try:
            output = subprocess.run(
                ["flatpak", "search", query],
                capture_output=True,
                text=True
            ).stdout

            packages = []
            for line in output.split('\n')[1:]:  # Пропускаем заголовок
                if not line.strip():
                    continue
                parts = line.split('\t')
                packages.append(Package(
                    name=parts[0],
                    version=parts[1],
                    description=parts[2],
                    repo=repo_name,
                    external=True,
                    package_type="flatpak"
                ))
            return packages
        except Exception as e:
            print(f"Flatpak search error: {e}")
            return []

    def _search_aur(self, query: str, repo_name: str) -> List[Package]:
        """Поиск в AUR"""
        try:
            import requests
            response = requests.get(
                f"https://aur.archlinux.org/rpc/?v=5&type=search&arg={query}"
            )
            data = response.json()

            return [
                Package(
                    name=pkg["Name"],
                    version=pkg["Version"],
                    description=pkg["Description"],
                    repo=repo_name,
                    external=True,
                    package_type="aur",
                    metadata={
                        "maintainer": pkg["Maintainer"],
                        "votes": pkg["NumVotes"]
                    }
                ) for pkg in data.get("results", [])
            ]
        except Exception as e:
            print(f"AUR search error: {e}")
            return []

    def install_from_external(self, package: Package) -> bool:
        """Установка пакета из внешнего репозитория"""
        if not package.external:
            return False

        if package.package_type == "flatpak":
            return self._install_flatpak(package.name)
        elif package.package_type == "aur":
            return self._install_aur(package.name)

        return False

    def _install_flatpak(self, package_id: str) -> bool:
        """Установка Flatpak пакета"""
        try:
            subprocess.run(
                ["flatpak", "install", "-y", "flathub", package_id],
                check=True
            )
            return True
        except subprocess.CalledProcessError as e:
            print(f"Flatpak install failed: {e}")
            return False

    def _install_aur(self, package_name: str) -> bool:
        """Установка пакета из AUR"""
        try:
            # Создаем временный каталог для сборки
            with tempfile.TemporaryDirectory() as tmpdir:
                # Клонируем PKGBUILD
                subprocess.run(
                    ["git", "clone",
                     f"https://aur.archlinux.org/{package_name}.git",
                     tmpdir],
                    check=True
                )

                # Собираем и устанавливаем пакет
                subprocess.run(
                    ["makepkg", "-si", "--noconfirm"],
                    cwd=tmpdir,
                    check=True
                )
            return True
        except Exception as e:
            print(f"AUR install failed: {e}")
            return False
