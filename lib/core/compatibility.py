import platform
import distro
from typing import Dict

def get_system_info() -> Dict:
    """Получение информации о системе"""
    return {
        "architecture": platform.machine(),
        "distro": distro.id(),
        "distro_like": distro.like().split(),
        "distro_version": distro.version()
    }

def check_compatibility(repo_config: Dict) -> bool:
    """Проверка совместимости репозитория с системой"""
    system = get_system_info()

    # Проверка архитектуры
    if system["architecture"] not in repo_config["compatibility"]["arches"]:
        return False

    # Проверка дистрибутива
    compatible_distros = repo_config["compatibility"]["distros"]
    if system["distro"] in compatible_distros:
        return True

    # Проверка производных дистрибутивов (например Ubuntu -> Debian)
    for distro_like in system["distro_like"]:
        if distro_like in compatible_distros:
            return True

    return False

def get_alternative_package(package_name: str, target_repo: str) -> Optional[str]:
    """Получение альтернативного имени пакета для другого репозитория"""
    # Загрузка конфига из предыдущего примера
    with open("config/repositories.json") as f:
        config = json.load(f)

    # Проверка прямого соответствия
    if package_name in config["compatibility_matrix"]["packages"]:
        return config["compatibility_matrix"]["packages"][package_name].get(target_repo)

    # Проверка по wildcard (например python-*)
    for pkg_pattern, mappings in config["compatibility_matrix"]["packages"].items():
        if pkg_pattern.endswith('*') and package_name.startswith(pkg_pattern[:-1]):
            return mappings.get(target_repo, {}).get(
                "prefix", pkg_pattern[:-1]) + package_name[len(pkg_pattern)-1:]

    return None
