import re
import subprocess
from .package_format import PackageFormat

class EbuildPackage(PackageFormat):
    """Поддержка ebuild (Gentoo Portage)"""

    def extract_metadata(self) -> Dict:
        metadata = {}
        with open(self.file_path, 'r') as f:
            content = f.read()

        # Парсинг ebuild-файла
        metadata['name'] = re.search(r'^NAME="(.+)"', content, re.M).group(1)
        metadata['version'] = re.search(r'^VERSION="(.+)"', content, re.M).group(1)
        metadata['deps'] = re.findall(r'^DEPEND="(.+)"', content, re.M)

        return metadata

    @classmethod
    def create(cls, source_dir: str, output_path: str, metadata: Dict) -> bool:
        # Создание ebuild-файла
        ebuild_content = f"""# Copyright 1999-2023 Gentoo Authors
EAPI=8

DESCRIPTION="{metadata['description']}"
HOMEPAGE="{metadata.get('homepage', '')}"
SRC_URI=""

LICENSE="{metadata.get('license', 'GPL-2')}"
SLOT="0"
KEYWORDS="~amd64 ~x86"

DEPEND="{' '.join(metadata.get('deps', []))}"
RDEPEND="$DEPEND"
"""
        ebuild_file = os.path.join(source_dir, f"{metadata['name']}-{metadata['version']}.ebuild")
        with open(ebuild_file, 'w') as f:
            f.write(ebuild_content)

        return True
