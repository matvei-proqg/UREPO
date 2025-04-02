import subprocess
from .package_manager import PackageManager

class ApxManager(PackageManager):
    """Реализация для APX (VanillaOS)"""

    def install(self, package: str) -> bool:
        cmd = f"apx-get install -y {package}"
        return subprocess.call(cmd, shell=True) == 0

    def add_repo(self, repo_config: Dict) -> bool:
        repo_file = f"/etc/apx/sources.list.d/{repo_config['name']}.list"
        with open(repo_file, 'w') as f:
            f.write(f"deb {repo_config['url']} {repo_config['dist']} {repo_config['components']}\n")

        # Импорт ключа
        if 'gpg_key' in repo_config:
            subprocess.run(f"apx-key add {repo_config['gpg_key']}", shell=True)

        return subprocess.call("apx-get update", shell=True) == 0
