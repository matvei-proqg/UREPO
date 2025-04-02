class DnfManager(PackageManager):
    """Реализация для DNF (Fedora/RHEL)"""

    def install(self, package: str) -> bool:
        cmd = f"dnf install -y {package}"
        return subprocess.call(cmd, shell=True) == 0

    def add_repo(self, repo_config: Dict) -> bool:
        repo_file = f"/etc/yum.repos.d/{repo_config['name']}.repo"
        with open(repo_file, 'w') as f:
            f.write(f"[{repo_config['name']}]\n")
            f.write(f"name={repo_config['name']}\n")
            f.write(f"baseurl={repo_config['url']}\n")
            f.write("enabled=1\n")
            f.write("gpgcheck=1\n")
            if 'gpg_key' in repo_config:
                f.write(f"gpgkey={repo_config['gpg_key']}\n")

        return True
