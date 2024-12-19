# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2024 Univention GmbH


from base64 import b64decode

from kubernetes import client

from e2e.kubernetes import KubernetesCluster


class ProvisioningApi:
    """
    Represents a deployment of the Provisioning API.
    """

    service_port = 80

    def __init__(self, k8s: KubernetesCluster, release_name: str):
        self._k8s = k8s
        self.release_name = release_name
        self.service_name = self._apply_release_prefix("provisioning-api")
        self._discover_from_cluster()

    def _apply_release_prefix(self, name):
        if not self.release_name or self.release_name == name:
            return name
        return f"{self.release_name}-{name}"

    def _discover_from_cluster(self):
        secret_name = self._apply_release_prefix("provisioning-api-credentials")
        v1 = client.CoreV1Api()

        secret = v1.read_namespaced_secret(
            name=secret_name,
            namespace=self._k8s.namespace,
        )

        self.admin_username = b64decode(secret.data["ADMIN_USERNAME"]).decode()
        self.admin_password = b64decode(secret.data["ADMIN_PASSWORD"]).decode()
