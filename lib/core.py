import os
import json
import hashlib
import shutil
import subprocess
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict

@dataclass
class Package:
    name: str
    version: str
    description: str
    arch: str
    license: str
    dependencies: List[str]
    provides: List[str]
    conflicts: List[str]
    maintainer: str
    repo: str = "main"
    metadata: Dict = None
    build_script: str = None

class Repository:
    def __init__(self, root_dir: str):
        self.root_dir = os.path.abspath(root_dir)
        self.packages_db = os.path.join(self.root_dir, "db", "packages.json")
        self._ensure_dirs()

    def _ensure_dirs(self):
        dirs = [
            "db",
            "storage/binary",
            "storage/source",
            "storage/flat",
            "tmp/build"
        ]
        for d in dirs:
            os.makedirs(os.path.join(self.root_dir, d), exist_ok=True)

    def add_package(self, pkg: Package, pkg_files: List[str]) -> bool:
        """Добавляет пакет в репозиторий"""
        # Сохраняем файлы пакета
        pkg_dir = os.path.join(self.root_dir, "storage/binary", pkg.name)
        os.makedirs(pkg_dir, exist_ok=True)

        for file in pkg_files:
            shutil.copy2(file, pkg_dir)

        # Обновляем базу данных
        db = self._load_db()
        db[pkg.name] = asdict(pkg)
        self._save_db(db)

        return True

    def build_package(self, pkg: Package) -> bool:
        """Собирает пакет из исходников"""
        build_dir = os.path.join(self.root_dir, "tmp/build", pkg.name)
        os.makedirs(build_dir, exist_ok=True)

        # Сохраняем скрипт сборки
        if pkg.build_script:
            with open(os.path.join(build_dir, "build.sh"), "w") as f:
                f.write(pkg.build_script)

            # Выполняем сборку
            try:
                subprocess.run(
                    ["/bin/bash", "build.sh"],
                    cwd=build_dir,
                    check=True,
                    capture_output=True
                )
            except subprocess.CalledProcessError as e:
                print(f"Build failed: {e.stderr.decode()}")
                return False

            # Ищем созданные файлы пакета
            pkg_files = []
            for root, _, files in os.walk(build_dir):
                for file in files:
                    if file.endswith((".deb", ".rpm", ".tar.gz", ".pkg.tar.zst")):
                        pkg_files.append(os.path.join(root, file))

            if not pkg_files:
                print("No package files were created")
                return False

            return self.add_package(pkg, pkg_files)

        return False

    def search(self, query: str) -> List[Package]:
        """Поиск пакетов"""
        db = self._load_db()
        results = []

        for name, data in db.items():
            if (query.lower() in name.lower() or
                query.lower() in data.get("description", "").lower()):
                results.append(Package(**data))

        return results

    def _load_db(self) -> Dict:
        """Загружает базу данных пакетов"""
        if os.path.exists(self.packages_db):
            with open(self.packages_db, "r") as f:
                return json.load(f)
        return {}

    def _save_db(self, db: Dict):
        """Сохраняет базу данных пакетов"""
        with open(self.packages_db, "w") as f:
            json.dump(db, f, indent=2)
