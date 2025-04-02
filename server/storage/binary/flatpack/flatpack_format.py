import json
from .package_format import PackageFormat

class FlatpakPackage(PackageFormat):
    """Поддержка Flatpak пакетов"""

    def extract_metadata(self) -> Dict:
        with tempfile.TemporaryDirectory() as tmpdir:
            cmd = f"flatpak build-export --metadata {tmpdir} {self.file_path}"
            subprocess.run(cmd, shell=True, check=True)

            with open(os.path.join(tmpdir, 'metadata')) as f:
                self.metadata = json.load(f)

        return self.metadata
