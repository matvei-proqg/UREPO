#!/usr/bin/env python3
import os
import sys
import argparse
from lib.core.repository import Repository, Package

def main():
    parser = argparse.ArgumentParser(description="Package build system")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Сборка из spec-файла
    build_parser = subparsers.add_parser("build", help="Build package from spec")
    build_parser.add_argument("spec_file", help="Path to package spec file")
    build_parser.add_argument("--output", help="Output directory", default=".")

    # Инициализация репозитория
    init_parser = subparsers.add_parser("init", help="Initialize new repository")
    init_parser.add_argument("path", help="Path to repository")

    args = parser.parse_args()

    if args.command == "init":
        repo = Repository(args.path)
        print(f"Initialized empty repository at {args.path}")
        return

    if args.command == "build":
        # Загружаем spec-файл
        try:
            with open(args.spec_file, "r") as f:
                spec = json.load(f)
        except Exception as e:
            print(f"Error loading spec: {e}")
            return 1

        # Создаем объект пакета
        pkg = Package(
            name=spec["name"],
            version=spec["version"],
            description=spec.get("description", ""),
            arch=spec.get("arch", "x86_64"),
            license=spec.get("license", "MIT"),
            dependencies=spec.get("dependencies", []),
            provides=spec.get("provides", []),
            conflicts=spec.get("conflicts", []),
            maintainer=spec.get("maintainer", ""),
            build_script=spec.get("build_script", "")
        )

        # Собираем пакет
        repo = Repository(os.getcwd())
        if repo.build_package(pkg):
            print("Package built successfully!")
            return 0
        else:
            print("Package build failed!")
            return 1

if __name__ == "__main__":
    sys.exit(main())
