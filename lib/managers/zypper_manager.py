class ZypperManager(PackageManager):
    """Менеджер для Zypper (openSUSE)"""

    def install(self, package: str) -> bool:
        cmd = f"zypper install -y {package}"
        return subprocess.call(cmd, shell=True) == 0

    def add_repo(self, repo_config: Dict) -> bool:
        cmd = f"zypper addrepo {repo_config['url']} {repo_config['name']}"
        if 'gpg_key' in repo_config:
            cmd += f" && zypper --gpg-auto-import-keys refresh"
        return subprocess.call(cmd, shell=True) == 0
