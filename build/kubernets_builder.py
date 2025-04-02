from kubernetes import client, config
import yaml

class KubernetesBuilder:
    def __init__(self):
        config.load_kube_config()
        self.batch_api = client.BatchV1Api()

    def create_build_job(self, name: str, config: Dict) -> bool:
        """Создание Job для сборки в Kubernetes"""
        job_manifest = {
            "apiVersion": "batch/v1",
            "kind": "Job",
            "metadata": {"name": f"build-{name}"},
            "spec": {
                "template": {
                    "spec": {
                        "containers": [{
                            "name": "builder",
                            "image": config["builder_image"],
                            "command": ["/bin/sh", "-c"],
                            "args": [config["build_script"]],
                            "volumeMounts": [{
                                "name": "cache",
                                "mountPath": "/cache"
                            }]
                        }],
                        "volumes": [{
                            "name": "cache",
                            "emptyDir": {}
                        }],
                        "restartPolicy": "Never"
                    }
                },
                "backoffLimit": 0
            }
        }

        try:
            self.batch_api.create_namespaced_job(
                body=job_manifest,
                namespace="default"
            )
            return True
        except Exception as e:
            print(f"Failed to create job: {e}")
            return False
