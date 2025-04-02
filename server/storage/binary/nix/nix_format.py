import json
from .package_format import PackageFormat

class NixPackage(PackageFormat):
    """Поддержка Nix пакетов"""

    def extract_metadata(self) -> Dict:
        with open(self.file_path) as f:
            nix_expr = f.read()

        # Упрощенный парсинг (в реальности нужно использовать nix eval)
        return {
            'name': re.search(r'name\s*=\s*"(.+?)"', nix_expr).group(1),
            'version': re.search(r'version\s*=\s*"(.+?)"', nix_expr).group(1)
        }

    def install(self, dest_dir: str) -> bool:
        cmd = f"nix-env -i {self.file_path}"
        return subprocess.call(cmd, shell=True) == 0
