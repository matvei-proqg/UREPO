import docker
import tempfile
import subprocess
from typing import Dict, List
from pathlib import Path

class BuildSystem:
    def __init__(self):
        self.client = docker.from_env()
        self.cache_dir = Path("build_cache")
        self.cache_dir.mkdir(exist_ok=True)

    def build_in_container(self, config: Dict) -> bool:
        """Сборка в изолированном контейнере"""
        try:
            with tempfile.NamedTemporaryFile(mode='w+') as dockerfile:
                dockerfile.write(self._generate_dockerfile(config))
                dockerfile.flush()

                image, logs = self.client.images.build(
                    path=".",
                    dockerfile=dockerfile.name,
                    tag=f"build-{config['name']}",
                    rm=True
                )

                container = self.client.containers.run(
                    image.id,
                    detach=True,
                    volumes={str(self.cache_dir): {'bind': '/cache', 'mode': 'rw'}}
                )

                result = container.wait()
                if result['StatusCode'] != 0:
                    print(container.logs())
                    return False

                return True
        except Exception as e:
            print(f"Build failed: {e}")
            return False

    def _generate_dockerfile(self, config: Dict) -> str:
        """Генерация Dockerfile для сборки"""
        return f"""
FROM {config['base_image']}
WORKDIR /build
COPY . .
RUN {config['build_command']}
RUN mkdir -p /cache && cp {config['artifact_path']} /cache/
"""
