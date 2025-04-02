import yaml
from .package_format import PackageFormat

class SnapPackage(PackageFormat):
    """Поддержка Snap пакетов"""

    def extract_metadata(self) -> Dict:
        with open(os.path.join(self.file_path, 'snapcraft.yaml')) as f:
            snap_meta = yaml.safe_load(f)

        return {
            'name': snap_meta['name'],
            'version': snap_meta['version'],
            'confinement': snap_meta.get('confinement', 'strict')
        }

    def install(self, dest_dir: str) -> bool:
        cmd = f"snap install --dangerous {self.file_path}"
        return subprocess.call(cmd, shell=True) == 0
