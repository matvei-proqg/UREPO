from abc import ABC, abstractmethod
from typing import List, Dict

class PackageManager(ABC):
    """Абстрактный базовый класс для пакетных менеджеров"""

    @abstractmethod
    def install(self, package: str) -> bool:
        pass

    @abstractmethod
    def remove(self, package: str) -> bool:
        pass

    @abstractmethod
    def search(self, query: str) -> List[Dict]:
        pass

    @abstractmethod
    def add_repo(self, repo_config: Dict) -> bool:
        pass

    @abstractmethod
    def remove_repo(self, repo_name: str) -> bool:
        pass
