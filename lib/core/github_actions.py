import yaml
from pathlib import Path

class GitHubActions:
    def generate_workflow(self, config: Dict) -> bool:
        """Генерация GitHub Actions workflow"""
        workflow = {
            "name": "Package Build",
            "on": {"push": {"branches": ["main"]}},
            "jobs": {
                "build": {
                    "runs-on": "ubuntu-latest",
                    "steps": [
                        {"uses": "actions/checkout@v3"},
                        {"name": "Build package", "run": config["build_command"]},
                        {"name": "Upload artifact", "uses": "actions/upload-artifact@v3"}
                    ]
                }
            }
        }

        workflows_dir = Path(".github/workflows")
        workflows_dir.mkdir(parents=True, exist_ok=True)

        with open(workflows_dir / "build.yml", "w") as f:
            yaml.dump(workflow, f)
        return True
