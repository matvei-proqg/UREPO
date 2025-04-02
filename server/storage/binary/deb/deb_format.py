import subprocess
from .package_format import PackageFormat
import apt_pkg

class DebPackage(PackageFormat):
    """Поддержка DEB пакетов (Debian/Ubuntu)"""

    def extract_metadata(self) -> Dict:
        apt_pkg.init()
        deb = apt_pkg.TagFile(self.file_path)
        section = next(deb)

        self.metadata = {
            'name': section.get('Package'),
            'version': section.get('Version'),
            'arch': section.get('Architecture'),
            'deps': section.get('Depends', '').split(', '),
            'description': section.get('Description')
        }
        return self.metadata

    def install(self, dest_dir: str) -> bool:
        cmd = f"dpkg -x {self.file_path} {dest_dir}"
        return subprocess.call(cmd, shell=True) == 0

    @classmethod
    def create(cls, source_dir: str, output_path: str, metadata: Dict) -> bool:
        # Генерация DEBIAN/control файла
        control_file = os.path.join(source_dir, 'DEBIAN', 'control')
        os.makedirs(os.path.dirname(control_file), exist_ok=True)

        with open(control_file, 'w') as f:
            f.write(f"Package: {metadata['name']}\n")
            f.write(f"Version: {metadata['version']}\n")
            f.write(f"Architecture: {metadata['arch']}\n")
            f.write(f"Maintainer: {metadata['maintainer']}\n")
            f.write(f"Description: {metadata['description']}\n")

        cmd = f"dpkg-deb --build {source_dir} {output_path}"
        return subprocess.call(cmd, shell=True) == 0
