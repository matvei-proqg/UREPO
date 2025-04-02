from typing import Dict, List, Set
import itertools

class DependencySolver:
    def __init__(self):
        self.dependency_graph: Dict[str, Set[str]] = {}

    def add_package(self, name: str, deps: List[str]):
        """Добавление пакета и его зависимостей в граф"""
        self.dependency_graph[name] = set(deps)

    def resolve(self, packages: List[str]) -> List[str]:
        """Разрешение зависимостей с алгоритмом SAT"""
        all_packages = set(packages)
        for pkg in packages:
            all_packages.update(self._get_all_dependencies(pkg))

        # Простое топологическое упорядочивание
        ordered = []
        while all_packages:
            # Находим пакеты без зависимостей
            ready = {pkg for pkg in all_packages
                    if not self.dependency_graph.get(pkg, set())}
            if not ready:
                raise ValueError("Cyclic dependency detected")

            ordered.extend(sorted(ready))
            all_packages -= ready

            # Удаляем выбранные пакеты из зависимостей других
            for pkg in list(self.dependency_graph):
                self.dependency_graph[pkg] -= ready
                if not self.dependency_graph[pkg]:
                    del self.dependency_graph[pkg]

        return ordered

    def _get_all_dependencies(self, pkg: str) -> Set[str]:
        """Рекурсивное получение всех зависимостей"""
        deps = set()
        to_process = [pkg]
        while to_process:
            current = to_process.pop()
            if current not in deps and current in self.dependency_graph:
                deps.add(current)
                to_process.extend(self.dependency_graph[current])
        return deps
