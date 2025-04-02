import gnupg
import hashlib
from pathlib import Path

class PackageSigner:
    def __init__(self, gpg_home: str = "~/.gnupg"):
        self.gpg = gnupg.GPG(gnupghome=gpg_home)

    def sign_package(self, package_path: str, key_id: str, passphrase: str = None) -> bool:
        """Подписать пакет GPG"""
        with open(package_path, 'rb') as f:
            return bool(self.gpg.sign_file(
                f,
                keyid=key_id,
                passphrase=passphrase,
                detach=True,
                output=f"{package_path}.sig"
            ))

    def verify_package(self, package_path: str, signature_path: str) -> bool:
        """Проверить подпись пакета"""
        with open(signature_path, 'rb') as sig:
            return bool(self.gpg.verify_file(sig, package_path))

    def calculate_checksum(self, package_path: str, algorithm: str = "sha256") -> str:
        """Вычислить контрольную сумму"""
        hasher = hashlib.new(algorithm)
        with open(package_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hasher.update(chunk)
        return hasher.hexdigest()
