import os
import tempfile
from typing import Optional

def convert_package(
    src_path: str,
    src_format: str,
    dest_format: str,
    output_dir: str
) -> Optional[str]:
    """Конвертация между форматами пакетов"""
    # Создание временного каталога
    with tempfile.TemporaryDirectory() as tmpdir:
        # Извлечение исходного пакета
        src_pkg = get_format_handler(src_format)(src_path)
        src_pkg.extract(tmpdir)

        # Создание нового пакета
        metadata = src_pkg.extract_metadata()
        dest_pkg = get_format_handler(dest_format)

        output_path = os.path.join(
            output_dir,
            f"{metadata['name']}-{metadata['version']}.{dest_format}"
        )

        if dest_pkg.create(tmpdir, output_path, metadata):
            return output_path

    return None
