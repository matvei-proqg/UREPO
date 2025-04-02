class NixManager(PackageManager):
    """Менеджер для Nix"""

    def install(self, package: str) -> bool:
        cmd = f"nix-env -iA {package}"
        return subprocess.call(cmd, shell=True) == 0

    def add_repo(self, repo_config: Dict) -> bool:
        cmd = f"nix-channel --add {repo_config['url']} {repo_config['name']}"
        return subprocess.call(cmd, shell=True) == 0
