class ApxPackage(PackageFormat):
    """Поддержка Apx пакетов (Vanilla OS)"""

    def install(self, dest_dir: str) -> bool:
        cmd = f"apx install {self.file_path}"
        return subprocess.call(cmd, shell=True) == 0
