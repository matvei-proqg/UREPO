import os
import json
import hashlib
from typing import Dict, List
from lib.formats import get_format_handler

class StorageManager:
    """Управление хранилищем пакетов"""

    def __init__(self, root_dir: str):
        self.root_dir = os.path.abspath(root_dir)
        self._init_structure()

    def _init_structure(self):
        """Создание структуры каталогов"""
        dirs = [
            'binary/deb',
            'binary/rpm',
            'binary/flatpak',
            'source/tar',
            'source/git',
            'source/spec',
            'db/versions'
        ]

        for d in dirs:
            os.makedirs(os.path.join(self.root_dir, d), exist_ok=True)

        if not os.path.exists(os.path.join(self.root_dir, 'db/packages.json')):
            with open(os.path.join(self.root_dir, 'db/packages.json'), 'w') as f:
                json.dump({}, f)

    def add_package(self, pkg_path: str, pkg_type: str) -> bool:
        """Добавление пакета в хранилище"""
        handler = get_format_handler(pkg_type)
        if not handler:
            return False

        pkg = handler(pkg_path)
        metadata = pkg.extract_metadata()

        # Сохранение в соответствующей директории
        dest_dir = os.path.join(
            self.root_dir,
            'binary',
            pkg_type,
            metadata['name']
        )
        os.makedirs(dest_dir, exist_ok=True)

        # Генерация имени файла
        pkg_filename = f"{metadata['name']}-{metadata['version']}.{pkg_type}"
        dest_path = os.path.join(dest_dir, pkg_filename)

        # Копирование файла
        shutil.copy2(pkg_path, dest_path)

        # Обновление базы данных
        self._update_db(metadata, pkg_type, dest_path)
        return True

    def _update_db(self, metadata: Dict, pkg_type: str, path: str):
        """Обновление базы данных пакетов"""
        db_path = os.path.join(self.root_dir, 'db/packages.json')
        with open(db_path, 'r+') as f:
            db = json.load(f)
            pkg_id = f"{metadata['name']}::{pkg_type}"

            if pkg_id not in db:
                db[pkg_id] = {
                    'versions': {},
                    'latest': None,
                    'type': pkg_type
                }

            version_id = metadata['version']
            db[pkg_id]['versions'][version_id] = {
                'path': path,
                'metadata': metadata,
                'checksum': self._calculate_checksum(path)
            }

            db[pkg_id]['latest'] = version_id
            f.seek(0)
            json.dump(db, f, indent=2)

    def _calculate_checksum(self, file_path: str) -> str:
        """Расчет контрольной суммы файла"""
        hash_sha256 = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha256.update(chunk)
        return hash_sha256.hexdigest()
