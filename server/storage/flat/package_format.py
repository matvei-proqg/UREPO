from abc import ABC, abstractmethod
from typing import Dict, List
import os
import tempfile

class PackageFormat(ABC):
    """Абстрактный базовый класс для всех форматов пакетов"""

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.metadata = {}

    @abstractmethod
    def extract_metadata(self) -> Dict:
        """Извлечение метаданных пакета"""
        pass

    @abstractmethod
    def install(self, dest_dir: str) -> bool:
        """Установка пакета в систему"""
        pass

    @abstractmethod
    def verify(self) -> bool:
        """Проверка целостности пакета"""
        pass

    @classmethod
    @abstractmethod
    def create(cls, source_dir: str, output_path: str, metadata: Dict) -> bool:
        """Создание пакета из исходников"""
        pass
