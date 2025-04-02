import rpm
from .package_format import PackageFormat

class RpmPackage(PackageFormat):
    """Поддержка RPM пакетов (RedHat/Fedora)"""

    def extract_metadata(self) -> Dict:
        ts = rpm.TransactionSet()
        fd = os.open(self.file_path, os.O_RDONLY)
        hdr = ts.hdrFromFdno(fd)
        os.close(fd)

        self.metadata = {
            'name': hdr['name'],
            'version': hdr['version'],
            'release': hdr['release'],
            'arch': hdr['arch'],
            'requires': list(hdr['requires']),
            'description': hdr['description']
        }
        return self.metadata
