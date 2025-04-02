class PacmanManager(PackageManager):
    """Менеджер для Pacman (Arch Linux)"""

    def install(self, package: str) -> bool:
        cmd = f"pacman -S --noconfirm {package}"
        return subprocess.call(cmd, shell=True) == 0

    def add_repo(self, repo_config: Dict) -> bool:
        # Для pacman нужно редактировать /etc/pacman.conf
        with open("/etc/pacman.conf", "a") as f:
            f.write(f"\n[{repo_config['name']}]\n")
            f.write(f"SigLevel = Optional TrustAll\n")
            f.write(f"Server = {repo_config['url']}\n")

        return subprocess.call("pacman -Sy", shell=True) == 0
