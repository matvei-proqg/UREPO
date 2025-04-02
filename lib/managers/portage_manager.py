class PortageManager(PackageManager):
    """Менеджер для Portage (Gentoo)"""

    def install(self, package: str) -> bool:
        cmd = f"emerge -av {package}"
        return subprocess.call(cmd, shell=True) == 0

    def add_repo(self, repo_config: Dict) -> bool:
        repo_file = f"/etc/portage/repos.conf/{repo_config['name']}.conf"
        with open(repo_file, 'w') as f:
            f.write(f"[{repo_config['name']}]\n")
            f.write(f"location = {repo_config['location']}\n")
            f.write("sync-type = git\n")
            f.write(f"sync-uri = {repo_config['sync_uri']}\n")

        return subprocess.call("emerge --sync", shell=True) == 0
